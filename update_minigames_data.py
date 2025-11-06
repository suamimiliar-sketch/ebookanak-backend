"""
Update Mini-Games with New Thumbnails and Game URLs
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
db_name = os.environ.get('DB_NAME', 'pelangi_pintar')

# New mini-games data
minigames_updates = [
    {
        "id": 1,
        "title": "Animal Memory Match",
        "thumbnailUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1762320060/Instagram_Post_-_Play_Animal_Memory_Match_Today_eqw8s8.png",
        "gameUrl": "https://rosebud.ai/p/a3989da1-a697-4d12-9b09-dfa668deacc7"
    },
    {
        "id": 2,
        "title": "Fruit Counting Game",
        "thumbnailUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1762320060/Instagram_Post_-_Fruit_Counting_Game_csg3tb.png",
        "gameUrl": "https://rosebud.ai/p/bacc1369-f557-49e4-9563-6aea565523f2"
    },
    {
        "id": 3,
        "title": "Color Sorting Game",
        "thumbnailUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1762320059/0001-2729664944168953402_u0r8af.png",
        "gameUrl": "https://690ad9f7c01413f208bd197f--luminous-sorbet-626189.netlify.app/"
    }
]

async def update_minigames():
    """Update mini-games with new thumbnails and URLs"""
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print(f"🔄 Updating mini-games in database: {db_name}")
    print(f"📊 Total games to update: {len(minigames_updates)}\n")
    
    updated_count = 0
    
    for game_update in minigames_updates:
        game_id = game_update["id"]
        thumbnail_url = game_update["thumbnailUrl"]
        game_url = game_update["gameUrl"]
        
        result = await db.minigames.update_one(
            {"id": game_id},
            {"$set": {
                "thumbnailUrl": thumbnail_url,
                "gameUrl": game_url
            }}
        )
        
        if result.matched_count > 0:
            updated_count += 1
            print(f"✅ ID {game_id}: {game_update['title']}")
            print(f"   Thumbnail: {thumbnail_url[:60]}...")
            print(f"   Game URL: {game_url[:60]}...")
        else:
            print(f"❌ ID {game_id}: Not found in database")
    
    print(f"\n🎉 Update completed!")
    print(f"📚 Mini-games updated: {updated_count}/{len(minigames_updates)}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(update_minigames())
