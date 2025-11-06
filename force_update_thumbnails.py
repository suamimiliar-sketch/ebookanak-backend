"""
FORCE UPDATE THUMBNAILS - Update ALL ebook pages with Cloudinary imageURLs
This script will forcefully update all ebook pages regardless of current state
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

# Import ebooks_updates from update_links_complete
from update_links_complete import ebooks_updates

async def force_update_thumbnails():
    """Force update all ebook thumbnails"""
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print(f"🔄 Force updating thumbnails for database: {db_name}")
    print(f"📊 Total ebooks to update: {len(ebooks_updates)}\n")
    
    updated_count = 0
    
    for ebook_update in ebooks_updates:
        ebook_id = ebook_update["id"]
        pages = ebook_update["pages"]
        
        # Force update regardless of current state
        result = await db.ebooks.update_one(
            {"id": ebook_id},
            {"$set": {"pages": pages}}
        )
        
        if result.matched_count > 0:
            updated_count += 1
            first_image = pages[0]["imageUrl"] if pages else "none"
            print(f"✅ ID {ebook_id}: Updated with {len(pages)} pages - {first_image[:60]}...")
        else:
            print(f"❌ ID {ebook_id}: Not found in database")
    
    # Verify
    total_with_images = await db.ebooks.count_documents({"pages.0.imageUrl": {"$ne": None, "$exists": True}})
    
    print(f"\n🎉 Force update completed!")
    print(f"📚 Ebooks processed: {updated_count}/{len(ebooks_updates)}")
    print(f"✅ Total ebooks with images: {total_with_images}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(force_update_thumbnails())
