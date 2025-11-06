from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path

# Import routes
from routes import ebooks, orders, webhooks, proxy, admin, games, game_access, test_notifications


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Original hello world endpoint
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

# Include new routes
api_router.include_router(ebooks.router)
api_router.include_router(orders.router)
api_router.include_router(webhooks.router)
api_router.include_router(proxy.router)
api_router.include_router(admin.router)
api_router.include_router(games.router)
api_router.include_router(game_access.router)
api_router.include_router(test_notifications.router)

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_db_seed():
    """
    Auto-seed database on startup if empty
    """
    try:
        ebook_count = await db.ebooks.count_documents({})
        minigame_count = await db.minigames.count_documents({})
        exclusive_count = await db.exclusive_ebooks.count_documents({})
        
        logger.info(f"Database status: {ebook_count} ebooks, {minigame_count} minigames, {exclusive_count} exclusive ebooks")
        
        # If database is completely empty, seed it
        if ebook_count == 0:
            logger.info("Empty database detected, triggering auto-seed...")
            import subprocess
            import sys
            
            # Run seed scripts
            subprocess.run([sys.executable, '/app/backend/seed_db.py'], cwd='/app/backend')
            subprocess.run([sys.executable, '/app/backend/seed_minigames.py'], cwd='/app/backend')
            subprocess.run([sys.executable, '/app/backend/seed_exclusive_ebooks.py'], cwd='/app/backend')
            
            logger.info("Auto-seed completed")
    except Exception as e:
        logger.error(f"Error during startup seed check: {str(e)}")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()