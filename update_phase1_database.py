"""
Update database with new pricing and add mini games + exclusive ebooks
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

async def update_database():
    # Connect to MongoDB
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'pelangi_ebooks')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("🔄 Starting database update...")
    
    # 1. Update all existing ebooks to new price (10,000 IDR)
    print("\n📚 Updating ebook prices to 10,000 IDR...")
    result = await db.ebooks.update_many(
        {},
        {"$set": {"price": 10000, "productType": "ebook"}}
    )
    print(f"✅ Updated {result.modified_count} ebooks")
    
    # 2. Create mini games collection
    print("\n🎮 Creating mini games collection...")
    
    # Check if minigames collection exists
    existing_games = await db.minigames.count_documents({})
    if existing_games > 0:
        print(f"   Found {existing_games} existing games, clearing...")
        await db.minigames.delete_many({})
    
    # Create 1 sample mini game
    mini_game = {
        "id": 1,
        "title": "Memory Card Game",
        "description": "Game kartu memori yang menyenangkan untuk melatih daya ingat anak",
        "ageGroup": "5-9",
        "ageLabel": "5-9 tahun",
        "price": 5000,  # 5,000 IDR per day
        "thumbnailUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753244/memory-game-thumbnail.jpg",
        "gameUrl": "/games/memory-card",
        "category": "Mini Game",
        "productType": "minigame",
        "accessDuration": 24,  # 24 hours
        "createdAt": datetime.utcnow()
    }
    
    await db.minigames.insert_one(mini_game)
    print(f"✅ Created 1 mini game: {mini_game['title']}")
    
    # 3. Create exclusive ebooks collection
    print("\n⭐ Creating exclusive ebooks collection...")
    
    # Check if exclusive_ebooks collection exists
    existing_exclusive = await db.exclusive_ebooks.count_documents({})
    if existing_exclusive > 0:
        print(f"   Found {existing_exclusive} existing exclusive ebooks, clearing...")
        await db.exclusive_ebooks.delete_many({})
    
    # Create 4 sample exclusive ebooks
    exclusive_ebooks = [
        {
            "id": 1,
            "title": "Interactive ABC Learning",
            "category": "Alphabet",
            "ageGroup": "3-5",
            "ageLabel": "3-5 tahun",
            "description": "Belajar ABC dengan fitur audio dan interaktif",
            "price": 50000,
            "fileName": "interactive-abc.pdf",
            "coverColor": "#FFE5EC",
            "pages": [
                {"page": 1, "color": "#FFE5EC", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753244/exclusive-abc-1.jpg"},
                {"page": 2, "color": "#FFF0F5", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753245/exclusive-abc-2.jpg"},
                {"page": 3, "color": "#FFF5F7", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753246/exclusive-abc-3.jpg"}
            ],
            "driveDownloadLink": "https://drive.google.com/uc?export=download&id=YOUR_FILE_ID_EXCLUSIVE_1",
            "hasAudio": True,
            "hasInteractive": True,
            "productType": "ebook_exclusive",
            "createdAt": datetime.utcnow()
        },
        {
            "id": 2,
            "title": "Interactive Numbers 1-100",
            "category": "Numbers",
            "ageGroup": "5-7",
            "ageLabel": "5-7 tahun",
            "description": "Belajar angka 1-100 dengan audio dan aktivitas interaktif",
            "price": 50000,
            "fileName": "interactive-numbers.pdf",
            "coverColor": "#E6F3FF",
            "pages": [
                {"page": 1, "color": "#E6F3FF", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753247/exclusive-num-1.jpg"},
                {"page": 2, "color": "#F0F8FF", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753248/exclusive-num-2.jpg"},
                {"page": 3, "color": "#F5FAFF", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753249/exclusive-num-3.jpg"}
            ],
            "driveDownloadLink": "https://drive.google.com/uc?export=download&id=YOUR_FILE_ID_EXCLUSIVE_2",
            "hasAudio": True,
            "hasInteractive": True,
            "productType": "ebook_exclusive",
            "createdAt": datetime.utcnow()
        },
        {
            "id": 3,
            "title": "Interactive Story Time",
            "category": "Story",
            "ageGroup": "5-9",
            "ageLabel": "5-9 tahun",
            "description": "Cerita interaktif dengan narasi audio dan animasi",
            "price": 50000,
            "fileName": "interactive-story.pdf",
            "coverColor": "#F0FFFA",
            "pages": [
                {"page": 1, "color": "#F0FFFA", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753250/exclusive-story-1.jpg"},
                {"page": 2, "color": "#F5FFFD", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753251/exclusive-story-2.jpg"},
                {"page": 3, "color": "#FAFFFF", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753252/exclusive-story-3.jpg"}
            ],
            "driveDownloadLink": "https://drive.google.com/uc?export=download&id=YOUR_FILE_ID_EXCLUSIVE_3",
            "hasAudio": True,
            "hasInteractive": True,
            "productType": "ebook_exclusive",
            "createdAt": datetime.utcnow()
        },
        {
            "id": 4,
            "title": "Interactive Science Fun",
            "category": "Science",
            "ageGroup": "7-9",
            "ageLabel": "7-9 tahun",
            "description": "Eksplorasi sains interaktif dengan audio dan eksperimen virtual",
            "price": 50000,
            "fileName": "interactive-science.pdf",
            "coverColor": "#FFF8E7",
            "pages": [
                {"page": 1, "color": "#FFF8E7", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753253/exclusive-sci-1.jpg"},
                {"page": 2, "color": "#FFFBF0", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753254/exclusive-sci-2.jpg"},
                {"page": 3, "color": "#FFFEF5", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753255/exclusive-sci-3.jpg"}
            ],
            "driveDownloadLink": "https://drive.google.com/uc?export=download&id=YOUR_FILE_ID_EXCLUSIVE_4",
            "hasAudio": True,
            "hasInteractive": True,
            "productType": "ebook_exclusive",
            "createdAt": datetime.utcnow()
        }
    ]
    
    await db.exclusive_ebooks.insert_many(exclusive_ebooks)
    print(f"✅ Created {len(exclusive_ebooks)} exclusive ebooks")
    
    # 4. Create indexes
    print("\n📊 Creating indexes...")
    await db.minigames.create_index("id", unique=True)
    await db.exclusive_ebooks.create_index("id", unique=True)
    await db.game_access_tokens.create_index("tokenId", unique=True)
    await db.game_access_tokens.create_index("expiresAt")
    print("✅ Indexes created")
    
    # 5. Verify updates
    print("\n🔍 Verification:")
    ebook_count = await db.ebooks.count_documents({})
    game_count = await db.minigames.count_documents({})
    exclusive_count = await db.exclusive_ebooks.count_documents({})
    
    # Check sample ebook price
    sample_ebook = await db.ebooks.find_one({"id": 1})
    
    print(f"   📚 Total ebooks: {ebook_count}")
    print(f"   🎮 Total mini games: {game_count}")
    print(f"   ⭐ Total exclusive ebooks: {exclusive_count}")
    if sample_ebook:
        print(f"   💰 Sample ebook price: Rp {sample_ebook.get('price', 0):,}")
    
    print("\n🎉 Database update completed successfully!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(update_database())
