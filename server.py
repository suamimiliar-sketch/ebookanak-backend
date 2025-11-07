# server.py
from fastapi import FastAPI, APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pathlib import Path
import logging
import subprocess
import os
import importlib
from typing import Optional

# -----------------------------------------------------------------------------
# Init & ENV
# -----------------------------------------------------------------------------
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

APP_NAME = "ebookanak-backend"
APP_VERSION = os.getenv("APP_VERSION", "dev")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(APP_NAME)
logger.warning(f"Starting {APP_NAME} → APP_VERSION={APP_VERSION}")

# -----------------------------------------------------------------------------
# Database (Mongo)
# -----------------------------------------------------------------------------
MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

client: Optional[AsyncIOMotorClient] = None
db = None

if not MONGO_URL or not DB_NAME:
    logger.error("ENV missing: MONGO_URL and/or DB_NAME")
else:
    try:
        client = AsyncIOMotorClient(MONGO_URL)
        db = client[DB_NAME]
        logger.info("MongoDB client initialized")
    except Exception as e:
        logger.exception(f"Failed to init MongoDB client: {e}")
        client = None
        db = None

# -----------------------------------------------------------------------------
# FastAPI app (docs under /api)
# -----------------------------------------------------------------------------
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    docs_url="/api/docs",
    redoc_url=None,
    openapi_url="/api/openapi.json",
)

# -----------------------------------------------------------------------------
# CORS (PASANG SEDINI MUNGKIN)
# -----------------------------------------------------------------------------
# FRONTEND_URL dapat diisi koma-separated di Render Env, mis:
# https://ebookanak.store, https://www.ebookanak.store, https://<preview>.preview.emergentagent.com
raw_origins = (os.getenv("FRONTEND_URL", "") or "").strip()
env_origins = [o.strip() for o in raw_origins.split(",") if o.strip()]

# Fallback aman (produksi + contoh preview). Ganti/ tambah sesuai kebutuhanmu.
fallback_origins = [
    "https://ebookanak.store",
    "https://www.ebookanak.store",
    # isi preview kamu saat ini agar langsung jalan:
    "https://pelangi-ecom-debug.preview.emergentagent.com",
]

allow_origins = env_origins or fallback_origins

# Untuk kasus domain preview yang sering berubah, kita sediakan regex ini.
# (Boleh dibiarkan; tidak wajib terpakai jika allow_origins sudah cukup.)
allow_origin_regex = r"https://([a-z0-9-]+)\.preview\.emergentagent\.com"

logger.info(f"CORS allow_origins={allow_origins}")
logger.info(f"CORS allow_origin_regex={allow_origin_regex}")

# PENTING:
# - Jangan set allow_credentials=True bila pakai wildcard "*"
# - Di sini kita TIDAK pakai wildcard dan pakai credentials=False (karena kita tidak kirim cookie)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_origin_regex=allow_origin_regex,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=False,
)

# -----------------------------------------------------------------------------
# API Router (prefix /api)
# -----------------------------------------------------------------------------
api = APIRouter(prefix="/api")

@api.get("/", include_in_schema=False)
async def root():
    return {"message": f"Hello From {APP_NAME} {APP_VERSION}"}

async def _mongo_ping_ok() -> tuple[bool, str]:
    if client is None:
        return False, "mongo not initialized (ENV missing or client failed)"
    try:
        await client.admin.command("ping")
        return True, "mongo ok"
    except Exception as e:
        return False, f"mongo fail: {e}"

@api.get("/health", include_in_schema=False)
async def health():
    return {
        "status": "ok",
        "service": APP_NAME,
        "version": APP_VERSION,
        "env": {
            "FRONTEND_URL": raw_origins or "unset",
            "MIDTRANS_IS_PRODUCTION": os.getenv("MIDTRANS_IS_PRODUCTION", "unset"),
        },
    }

@api.get("/health/deep", include_in_schema=False)
async def health_deep():
    mongo_ok, mongo_msg = await _mongo_ping_ok()
    midtrans_key = "set" if os.getenv("MIDTRANS_SERVER_KEY") else "missing"
    overall_ok = mongo_ok and (midtrans_key == "set")
    payload = {
        "status": "ok" if overall_ok else "degraded",
        "checks": {
            "mongo": mongo_msg,
            "midtrans_server_key": midtrans_key,
        },
        "version": APP_VERSION,
    }
    return JSONResponse(
        status_code=status.HTTP_200_OK if overall_ok else status.HTTP_503_SERVICE_UNAVAILABLE,
        content=payload,
    )

# -----------------------------------------------------------------------------
# SAFE include routers (tanpa from routes import ... langsung pecah)
# -----------------------------------------------------------------------------
def include_router_safe(module_path: str, attr: str = "router"):
    """
    Import aman: jika modul tidak ada/ error, hanya log warning—tidak mematikan server.
    """
    try:
        mod = importlib.import_module(module_path)
        router = getattr(mod, attr)
        api.include_router(router)
        logger.info(f"Included {module_path}.{attr}")
    except Exception as e:
        logger.warning(f"Skip {module_path}.{attr}: {e}")

# HANYA modul yang ada. Jangan menyebut 'games' atau 'game_access' jika sudah dihapus.
include_router_safe("routes.ebooks")               # routes/ebooks.py -> router
include_router_safe("routes.orders")
include_router_safe("routes.webhooks")
include_router_safe("routes.proxy")
include_router_safe("routes.admin")
include_router_safe("routes.test_notifications")

# Daftarkan API group ke app (setelah middleware terpasang)
app.include_router(api)

# -----------------------------------------------------------------------------
# Startup: auto-seed jika DB kosong
# -----------------------------------------------------------------------------
@app.on_event("startup")
async def startup_db_seed():
    if db is None:
        logger.error("Skip auto-seed: DB not initialized")
        return
    try:
        ebook_count = await db.ebooks.count_documents({})
        minigame_count = await db.minigames.count_documents({})
        exclusive_count = await db.exclusive_ebooks.count_documents({})

        logger.info(
            f"Database status: {ebook_count} ebooks, "
            f"{minigame_count} minigames, {exclusive_count} exclusive ebooks"
        )

        if ebook_count == 0:
            logger.info("Empty database detected, triggering auto-seed...")
            subprocess.run([os.sys.executable, "/app/backend/seed_db.py"], cwd="/app/backend", check=False)
            subprocess.run([os.sys.executable, "/app/backend/seed_minigames.py"], cwd="/app/backend", check=False)
            subprocess.run([os.sys.executable, "/app/backend/seed_exclusive_ebooks.py"], cwd="/app/backend", check=False)
            logger.info("Auto-seed completed")
    except Exception as e:
        logger.error(f"Error during startup seed check: {e}")

# -----------------------------------------------------------------------------
# Shutdown
# -----------------------------------------------------------------------------
@app.on_event("shutdown")
async def shutdown_db_client():
    try:
        if client is not None:
            client.close()
            logger.info("MongoDB client closed")
    except Exception as e:
        logger.error(f"Error on MongoDB client close: {e}")

# -----------------------------------------------------------------------------
# Run hint (Render Docker Command):
# uvicorn server:app --host 0.0.0.0 --port $PORT
# -----------------------------------------------------------------------------
