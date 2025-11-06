import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def fix_double_https():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    # Find ebook 7
    ebook = await db.ebooks.find_one({'id': 7})
    
    if ebook and 'pages' in ebook:
        fixed = False
        for page in ebook['pages']:
            if 'imageUrl' in page and page['imageUrl'].startswith('hhttps://'):
                old_url = page['imageUrl']
                page['imageUrl'] = page['imageUrl'].replace('hhttps://', 'https://', 1)
                print(f"✅ Fixed: {old_url} -> {page['imageUrl']}")
                fixed = True
        
        if fixed:
            await db.ebooks.update_one({'id': 7}, {'$set': {'pages': ebook['pages']}})
            print(f"✅ Updated ebook ID 7 in database")
        else:
            print("No URLs needed fixing")
    else:
        print("Ebook 7 not found")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_double_https())
