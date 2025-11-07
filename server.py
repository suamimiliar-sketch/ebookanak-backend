# server.py
from fastapi import FastAPI, APIRouter, status
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pathlib import Path
import logging
import subprocess
import os

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

client: AsyncIOMotorClient | None = None
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
# FastAPI app with API prefix & docs under /api
# -----------------------------------------------------------------------------
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    docs_url="/api/docs",
    redoc_url=None,
    openapi_url="/api/openapi.json",
)

api_router = APIRouter(prefix="/api")

# -----------------------------------------------------------------------------
# CORS
# -----------------------------------------------------------------------------
raw_origins = os.getenv("FRONTEND_URL", "").strip()
allow_origins = [o.strip() for o in raw_origins.split(",") if o.strip()] if raw_origins else []
if not allow_origins:
    allow_origins = ["*"]
    logger.warning("FRONTEND_URL not set → CORS allow_origins='*' (dev mode)")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=allow_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# ROUTES: root (sanity) & health
# -----------------------------------------------------------------------------
@api_router.get("/", include_in_schema=False)
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

@api_router.get("/health", include_in_schema=False)
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

@api_router.get("/health/deep", include_in_schema=False)
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
# Import & include sub-routers (TANPA games)
# -----------------------------------------------------------------------------
from routes import (
    ebooks,
    orders,
    webhooks,
    proxy,
    admin,
    game_access,
    test_notifications,
)

api_router.include_router(ebooks.router)
api_router.include_router(orders.router)
api_router.include_router(webhooks.router)
api_router.include_router(proxy.router)
api_router.include_router(admin.router)
api_router.include_router(game_access.router)
api_router.include_router(test_notifications.router)

# Daftarkan api_router ke app utama
app.include_router(api_router)

# -----------------------------------------------------------------------------
# Startup tasks (auto-seed jika DB kosong)
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
# Shutdown (tutup koneksi)
# -----------------------------------------------------------------------------
@app.on_event("shutdown")
async def shutdown_db_client():
    try:
        if client is not None:
            client.close()
            logger.info("MongoDB client closed")
    except Exception as e:
        logger.error(f"Error on MongoDB client close: {e}")

# Tips run:
# uvicorn server:app --host 0.0.0.0 --port 8000
# Swagger: /api/docs | OpenAPI: /api/openapi.json | Health: /api/health, /api/health/deep
