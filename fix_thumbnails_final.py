"""
Fix Google Drive URLs untuk tampil di production dan preview
Menggunakan format yang paling reliable untuk public sharing
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


def convert_to_reliable_url(url):
    """Convert to most reliable Google Drive URL format for public images"""
    # Extract file ID from any Google Drive URL format
    file_id = None
    
    # Try different patterns
    patterns = [
        r'id=([a-zA-Z0-9_-]+)',
        r'd/([a-zA-Z0-9_-]+)',
        r'file/d/([a-zA-Z0-9_-]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            file_id = match.group(1)
            break
    
    if file_id:
        # Use the direct thumbnail format that works best in production
        return f"https://drive.google.com/thumbnail?id={file_id}&sz=w500"
    
    return url


async def fix_all_thumbnails():
    """Fix all thumbnail URLs to reliable format"""
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    try:
        ebooks = await db.ebooks.find({}).to_list(length=None)
        print(f"📚 Found {len(ebooks)} ebooks to update\n")
        
        updated_count = 0
        for ebook in ebooks:
            if 'pages' in ebook and ebook['pages']:
                updated = False
                for page in ebook['pages']:
                    if 'imageUrl' in page:
                        old_url = page['imageUrl']
                        new_url = convert_to_reliable_url(old_url)
                        if old_url != new_url:
                            page['imageUrl'] = new_url
                            updated = True
                            print(f"  📖 Ebook {ebook['id']}, Page {page['page']}: Updated")
                
                if updated:
                    result = await db.ebooks.update_one(
                        {'id': ebook['id']},
                        {'$set': {'pages': ebook['pages']}}
                    )
                    
                    if result.modified_count > 0:
                        updated_count += 1
                        print(f"✅ Ebook ID {ebook['id']} updated successfully\n")
        
        print(f"\n🎉 Update completed!")
        print(f"📊 Total ebooks updated: {updated_count}/{len(ebooks)}")
        
        # Show example URL
        example = await db.ebooks.find_one({'id': 1})
        if example and 'pages' in example:
            print(f"\n📸 Example thumbnail URL:")
            print(f"   {example['pages'][0]['imageUrl']}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(fix_all_thumbnails())
