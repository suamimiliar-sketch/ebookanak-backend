import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "pelangi_pintar")

# Sample exclusive ebooks data
exclusive_ebooks_data = [
    {
        "id": 1,
        "title": "Interactive Alphabet Adventure",
        "category": "Interactive Learning",
        "ageGroup": "3-4",
        "ageLabel": "Usia 3-4 tahun",
        "description": "Learn the alphabet with interactive visuals and audio narration!",
        "price": 50000,  # 50rb
        "fileName": "exclusive_alphabet.pdf",
        "coverColor": "#FFB6C1",
        "pages": [
            {"page": 1, "color": "#FFB6C1", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1730000000/dummy-exclusive-1.jpg"},
            {"page": 2, "color": "#87CEEB", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1730000000/dummy-exclusive-2.jpg"},
            {"page": 3, "color": "#98FB98", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1730000000/dummy-exclusive-3.jpg"}
        ],
        "driveDownloadLink": "https://drive.google.com/file/d/dummy-exclusive-alphabet/view",
        "downloadLink": "https://drive.google.com/uc?id=dummy-exclusive-alphabet&export=download",
        "hasAudio": True,
        "hasInteractive": True,
        "productType": "ebook_exclusive"
    },
    {
        "id": 2,
        "title": "Angka Ajaib",
        "category": "Matematika",
        "ageGroup": "5-6",
        "ageLabel": "Usia 5-6 tahun",
        "description": "Belajar angka dengan cara yang menyenangkan dan interaktif!",
        "price": 50000,
        "fileName": "exclusive_numbers.pdf",
        "coverColor": "#FFE4B5",
        "pages": [
            {"page": 1, "color": "#FFE4B5", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1730000000/dummy-numbers-1.jpg"},
            {"page": 2, "color": "#FFB6C1", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1730000000/dummy-numbers-2.jpg"},
            {"page": 3, "color": "#DDA0DD", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1730000000/dummy-numbers-3.jpg"}
        ],
        "driveDownloadLink": "https://drive.google.com/file/d/dummy-exclusive-numbers/view",
        "downloadLink": "https://drive.google.com/uc?id=dummy-exclusive-numbers&export=download",
        "hasAudio": True,
        "hasInteractive": True,
        "productType": "ebook_exclusive"
    },
    {
        "id": 3,
        "title": "Petualangan Hewan",
        "category": "Cerita",
        "ageGroup": "7-9",
        "ageLabel": "Usia 7-9 tahun",
        "description": "Jelajahi dunia hewan dengan suara dan animasi yang menarik!",
        "price": 50000,
        "fileName": "exclusive_animals.pdf",
        "coverColor": "#98FB98",
        "pages": [
            {"page": 1, "color": "#98FB98", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1730000000/dummy-animals-1.jpg"},
            {"page": 2, "color": "#87CEEB", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1730000000/dummy-animals-2.jpg"},
            {"page": 3, "color": "#FFB6C1", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1730000000/dummy-animals-3.jpg"}
        ],
        "driveDownloadLink": "https://drive.google.com/file/d/dummy-exclusive-animals/view",
        "downloadLink": "https://drive.google.com/uc?id=dummy-exclusive-animals&export=download",
        "hasAudio": True,
        "hasInteractive": True,
        "productType": "ebook_exclusive"
    },
    {
        "id": 4,
        "title": "Dunia Warna Interaktif",
        "category": "Seni",
        "ageGroup": "3-4",
        "ageLabel": "Usia 3-4 tahun",
        "description": "Kenali warna-warna dengan audio dan visual yang mengagumkan!",
        "price": 50000,
        "fileName": "exclusive_colors.pdf",
        "coverColor": "#DDA0DD",
        "pages": [
            {"page": 1, "color": "#DDA0DD", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1730000000/dummy-colors-1.jpg"},
            {"page": 2, "color": "#FFE4B5", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1730000000/dummy-colors-2.jpg"},
            {"page": 3, "color": "#98FB98", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1730000000/dummy-colors-3.jpg"}
        ],
        "driveDownloadLink": "https://drive.google.com/file/d/dummy-exclusive-colors/view",
        "downloadLink": "https://drive.google.com/uc?id=dummy-exclusive-colors&export=download",
        "hasAudio": True,
        "hasInteractive": True,
        "productType": "ebook_exclusive"
    }
]

async def seed_exclusive_ebooks():
    """Seed exclusive ebooks collection"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    try:
        # Drop existing collection
        await db.ebooks_exclusive.drop()
        print("✓ Dropped existing ebooks_exclusive collection")
        
        # Insert exclusive ebooks
        if exclusive_ebooks_data:
            result = await db.ebooks_exclusive.insert_many(exclusive_ebooks_data)
            print(f"✓ Inserted {len(result.inserted_ids)} exclusive ebooks")
        
        # Verify
        count = await db.ebooks_exclusive.count_documents({})
        print(f"✓ Total exclusive ebooks in database: {count}")
        
        # Sample exclusive ebook
        sample = await db.ebooks_exclusive.find_one({})
        if sample:
            print(f"\n📚 Sample exclusive ebook:")
            print(f"   ID: {sample['id']}")
            print(f"   Title: {sample['title']}")
            print(f"   Price: Rp {sample['price']:,}")
            print(f"   Age: {sample['ageLabel']}")
            print(f"   Has Audio: {sample['hasAudio']}")
            print(f"   Has Interactive: {sample['hasInteractive']}")
        
        print("\n✅ Exclusive ebooks seeding completed successfully!")
        
    except Exception as e:
        print(f"❌ Error seeding exclusive ebooks: {e}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(seed_exclusive_ebooks())
