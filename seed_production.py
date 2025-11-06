"""
Production Database Seeding Script
Run this after deployment to ensure production DB has correct data
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def seed_production():
    # Connect to MongoDB
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'pelangi_ebooks')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("🔄 Starting production database update...")
    
    # Run the update script
    try:
        # Import and run the regular seed script
        import seed_db
        print("✅ Running seed_db to populate ebooks...")
        
        # Clear existing
        result = await db.ebooks.delete_many({})
        print(f"✅ Cleared {result.deleted_count} existing ebooks")
        
        # Now we need to insert with Cloudinary URLs
        # Run the update_links_complete script
        exec(open('update_links_complete.py').read())
        
        print("✅ Production database updated successfully!")
        
        # Verify
        count = await db.ebooks.count_documents({})
        sample = await db.ebooks.find_one({'id': 1})
        
        print(f"\n📊 Verification:")
        print(f"   Total ebooks: {count}")
        if sample and 'pages' in sample:
            print(f"   Sample thumbnail URL: {sample['pages'][0].get('imageUrl', 'NOT FOUND')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(seed_production())
