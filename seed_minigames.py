import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "pelangi_pintar")

# Sample mini-games data
minigames_data = [
    {
        "id": 1,
        "title": "Animal Memory Match",
        "description": "Temukan pasangan hewan yang sama! Game memori yang menyenangkan untuk melatih daya ingat anak.",
        "ageGroup": "5-9",
        "ageLabel": "Usia 5-9 tahun",
        "price": 5000,  # 5rb
        "thumbnailUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1762265021/Untitled_design_3_os4ij4.png",
        "gameUrl": "https://rosebud.ai/games/a3989da1-a697-4d12-9b09-dfa668deacc7",
        "category": "Mini Game",
        "productType": "minigame",
        "icon": "🐾"
    },
    {
        "id": 2,
        "title": "Fruit Counting Game",
        "description": "Hitung buah-buahan dan belajar angka dengan cara yang menyenangkan!",
        "ageGroup": "5-9",
        "ageLabel": "Usia 5-9 tahun",
        "price": 5000,  # 5rb
        "thumbnailUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1762265021/Untitled_design_4_xrdzzl.png",
        "gameUrl": "https://rosebud.ai/games/bacc1369-f557-49e4-9563-6aea565523f2",
        "category": "Mini Game",
        "productType": "minigame",
        "icon": "🍎"
    },
    {
        "id": 3,
        "title": "Color Sorting Game",
        "description": "Urutkan warna-warna yang tepat! Belajar mengenal warna sambil bermain.",
        "ageGroup": "5-9",
        "ageLabel": "Usia 5-9 tahun",
        "price": 5000,  # 5rb
        "thumbnailUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1762265021/Untitled_design_5_mzhmkn.png",
        "gameUrl": "/games/warna-ceria.html",
        "category": "Mini Game",
        "productType": "minigame",
        "icon": "🎨"
    }
]

async def seed_minigames():
    """Seed mini-games collection"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    try:
        # Drop existing collection
        await db.minigames.drop()
        print("✓ Dropped existing minigames collection")
        
        # Insert mini-games
        if minigames_data:
            result = await db.minigames.insert_many(minigames_data)
            print(f"✓ Inserted {len(result.inserted_ids)} mini-games")
        
        # Verify
        count = await db.minigames.count_documents({})
        print(f"✓ Total mini-games in database: {count}")
        
        # Sample mini-game
        sample = await db.minigames.find_one({})
        if sample:
            print(f"\n📚 Sample mini-game:")
            print(f"   ID: {sample['id']}")
            print(f"   Title: {sample['title']}")
            print(f"   Price: Rp {sample['price']:,}")
            print(f"   Age: {sample['ageLabel']}")
        
        print("\n✅ Mini-games seeding completed successfully!")
        
    except Exception as e:
        print(f"❌ Error seeding mini-games: {e}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(seed_minigames())
