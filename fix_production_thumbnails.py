"""
Fix Google Drive image URLs to use direct view format that works in production
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import re

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']


def convert_to_direct_url(thumbnail_url):
    """Convert thumbnail URL to direct view URL that works in production"""
    # Extract file ID from URL
    match = re.search(r'id=([a-zA-Z0-9_-]+)', thumbnail_url)
    if match:
        file_id = match.group(1)
        # Use direct view format that works with CORS
        return f"https://lh3.googleusercontent.com/d/{file_id}"
    return thumbnail_url


async def fix_production_urls():
    """Fix all ebook image URLs to work in production"""
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    try:
        # Get all ebooks
        ebooks = await db.ebooks.find({}).to_list(length=None)
        print(f"Found {len(ebooks)} ebooks")
        
        updated_count = 0
        for ebook in ebooks:
            if 'pages' in ebook and ebook['pages']:
                # Convert all page imageUrls
                for page in ebook['pages']:
                    if 'imageUrl' in page:
                        old_url = page['imageUrl']
                        new_url = convert_to_direct_url(old_url)
                        page['imageUrl'] = new_url
                        print(f"  Ebook {ebook['id']}, Page {page['page']}: Updated to production URL")
                
                # Update in database
                result = await db.ebooks.update_one(
                    {'id': ebook['id']},
                    {'$set': {'pages': ebook['pages']}}
                )
                
                if result.modified_count > 0:
                    updated_count += 1
                    print(f"✅ Updated ebook ID {ebook['id']}")
        
        print(f"\n🎉 Update completed!")
        print(f"📚 Total ebooks updated: {updated_count}")
        
    except Exception as e:
        print(f"❌ Error fixing URLs: {str(e)}")
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(fix_production_urls())
