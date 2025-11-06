"""
Database seeding script for Pelangi Pintar
Seeds the ebooks collection with initial data
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

# Ebook data
ebooks_data = [
    # Tracing Books - Usia 3-4
    {
        "id": 1,
        "title": "Shapes Activity Book",
        "category": "Tracing Book",
        "ageGroup": "3-4",
        "ageLabel": "Usia 3-4 tahun",
        "description": "Belajar mengenal berbagai bentuk dengan cara menyenangkan melalui aktivitas tracing",
        "price": 10000,
        "fileName": "Shapes Activity book.pdf",
        "coverColor": "#FFE4E1",
        "pages": [
            {"page": 1, "color": "#FFE4E1"},
            {"page": 2, "color": "#FFD6D9"},
            {"page": 3, "color": "#FFC9CE"}
        ],
        "isBonus": False,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=YOUR_FILE_ID_HERE_1"
    },
    {
        "id": 2,
        "title": "Shape Book",
        "category": "Tracing Book",
        "ageGroup": "3-4",
        "ageLabel": "Usia 3-4 tahun",
        "description": "Kenali bentuk-bentuk dasar dengan Huto dan teman-temannya",
        "price": 10000,
        "fileName": "Shape Book.pdf",
        "coverColor": "#E6F3FF",
        "pages": [
            {"page": 1, "color": "#E6F3FF"},
            {"page": 2, "color": "#D6EBFF"},
            {"page": 3, "color": "#C6E3FF"}
        ],
        "isBonus": False
    },
    {
        "id": 3,
        "title": "Trace and Color",
        "category": "Tracing Book",
        "ageGroup": "3-4",
        "ageLabel": "Usia 3-4 tahun",
        "description": "Latih motorik halus dengan aktivitas tracing dan mewarnai",
        "price": 10000,
        "fileName": "TRACE AND COLOR CF.pdf",
        "coverColor": "#FFF9E6",
        "pages": [
            {"page": 1, "color": "#FFF9E6"},
            {"page": 2, "color": "#FFF4D6"},
            {"page": 3, "color": "#FFEFC6"}
        ],
        "isBonus": False
    },
    {
        "id": 4,
        "title": "Trace Numbers 1-100",
        "category": "Tracing Book",
        "ageGroup": "3-4",
        "ageLabel": "Usia 3-4 tahun",
        "description": "Belajar menulis angka 1 sampai 100 dengan cara yang menyenangkan",
        "price": 10000,
        "fileName": "Trace the numbers 1-100.pdf",
        "coverColor": "#E8F5E9",
        "pages": [
            {"page": 1, "color": "#E8F5E9"},
            {"page": 2, "color": "#D8EDD9"},
            {"page": 3, "color": "#C8E5C9"}
        ],
        "isBonus": False
    },
    {
        "id": 5,
        "title": "Transport Tracing Book",
        "category": "Tracing Book",
        "ageGroup": "3-4",
        "ageLabel": "Usia 3-4 tahun",
        "description": "Kenali berbagai alat transportasi sambil belajar menulis",
        "price": 10000,
        "fileName": "Transport Tracing book - Copy.pdf",
        "coverColor": "#F3E5F5",
        "pages": [
            {"page": 1, "color": "#F3E5F5"},
            {"page": 2, "color": "#E9D8F0"},
            {"page": 3, "color": "#DFCBEB"}
        ],
        "isBonus": False
    },
    {
        "id": 6,
        "title": "Easter Tracing Handwriting",
        "category": "Tracing Book",
        "ageGroup": "3-4",
        "ageLabel": "Usia 3-4 tahun",
        "description": "Latihan menulis dengan tema Easter yang ceria",
        "price": 10000,
        "fileName": "Easter Tracing Handwriting Practice Book.pdf",
        "coverColor": "#FFF3E0",
        "pages": [
            {"page": 1, "color": "#FFF3E0"},
            {"page": 2, "color": "#FFEAD0"},
            {"page": 3, "color": "#FFE1C0"}
        ],
        "isBonus": False
    },
    # Flash Card Dasar - Usia 3-4
    {
        "id": 7,
        "title": "Alphabet Flashcards A4",
        "category": "Flash Card Dasar",
        "ageGroup": "3-4",
        "ageLabel": "Usia 3-4 tahun",
        "description": "Kenali huruf A-Z dengan flashcard penuh warna",
        "price": 10000,
        "fileName": "Alphabet Flashcards A4.pdf",
        "coverColor": "#E1F5FE",
        "pages": [
            {"page": 1, "color": "#E1F5FE"},
            {"page": 2, "color": "#D1EDFE"},
            {"page": 3, "color": "#C1E5FE"}
        ],
        "isBonus": False
    },
    {
        "id": 8,
        "title": "Learn About Colours",
        "category": "Flash Card Dasar",
        "ageGroup": "3-4",
        "ageLabel": "Usia 3-4 tahun",
        "description": "Belajar mengenal berbagai warna dengan cara menyenangkan",
        "price": 10000,
        "fileName": "Learn About Colours.pdf",
        "coverColor": "#FCE4EC",
        "pages": [
            {"page": 1, "color": "#FCE4EC"},
            {"page": 2, "color": "#FAD4E0"},
            {"page": 3, "color": "#F8C4D4"}
        ],
        "isBonus": False
    },
    {
        "id": 9,
        "title": "Alphabet Flashcards for Kids",
        "category": "Flash Card Dasar",
        "ageGroup": "3-4",
        "ageLabel": "Usia 3-4 tahun",
        "description": "Flashcard huruf dengan ilustrasi menarik untuk anak",
        "price": 10000,
        "fileName": "Alphabet flashcards for kids.pdf",
        "coverColor": "#FFF9C4",
        "pages": [
            {"page": 1, "color": "#FFF9C4"},
            {"page": 2, "color": "#FFF5B4"},
            {"page": 3, "color": "#FFF1A4"}
        ],
        "isBonus": False
    },
    {
        "id": 10,
        "title": "Fruits Flashcards A4",
        "category": "Flash Card Dasar",
        "ageGroup": "3-4",
        "ageLabel": "Usia 3-4 tahun",
        "description": "Kenali berbagai buah-buahan dengan flashcard cantik",
        "price": 10000,
        "fileName": "Fruits Flashcards A4.pdf",
        "coverColor": "#F1F8E9",
        "pages": [
            {"page": 1, "color": "#F1F8E9"},
            {"page": 2, "color": "#E8F3DC"},
            {"page": 3, "color": "#DFEECD"}
        ],
        "isBonus": False
    },
    {
        "id": 11,
        "title": "Number Flashcards",
        "category": "Flash Card Dasar",
        "ageGroup": "3-4",
        "ageLabel": "Usia 3-4 tahun",
        "description": "Belajar angka 1-20 dengan flashcard interaktif",
        "price": 10000,
        "fileName": "Number Flashcards.pdf",
        "coverColor": "#E8EAF6",
        "pages": [
            {"page": 1, "color": "#E8EAF6"},
            {"page": 2, "color": "#DCDFF3"},
            {"page": 3, "color": "#D0D4F0"}
        ],
        "isBonus": False
    },
    # Flashcards Tema - Usia 5-6
    {
        "id": 12,
        "title": "Skip Counting",
        "category": "Flashcards Tema",
        "ageGroup": "5-6",
        "ageLabel": "Usia 5-6 tahun",
        "description": "Belajar menghitung melompat dengan cara asyik",
        "price": 10000,
        "fileName": "Skip Counting.pdf",
        "coverColor": "#E0F2F1",
        "pages": [
            {"page": 1, "color": "#E0F2F1"},
            {"page": 2, "color": "#D0EBE9"},
            {"page": 3, "color": "#C0E4E1"}
        ],
        "isBonus": False
    },
    {
        "id": 13,
        "title": "Weather Vocabulary Worksheet",
        "category": "Flashcards Tema",
        "ageGroup": "5-6",
        "ageLabel": "Usia 5-6 tahun",
        "description": "Kenali cuaca dan iklim dengan worksheet penuh warna",
        "price": 10000,
        "fileName": "Colorful Illustrative Weather Vocabulary Worksheet.pdf",
        "coverColor": "#FFF8E1",
        "pages": [
            {"page": 1, "color": "#FFF8E1"},
            {"page": 2, "color": "#FFF3D1"},
            {"page": 3, "color": "#FFEEC1"}
        ],
        "isBonus": False
    },
    {
        "id": 14,
        "title": "Weather Flashcards",
        "category": "Flashcards Tema",
        "ageGroup": "5-6",
        "ageLabel": "Usia 5-6 tahun",
        "description": "Flashcard cuaca untuk belajar bahasa Inggris",
        "price": 10000,
        "fileName": "Weather Flashcards.pdf",
        "coverColor": "#E3F2FD",
        "pages": [
            {"page": 1, "color": "#E3F2FD"},
            {"page": 2, "color": "#D3EBFD"},
            {"page": 3, "color": "#C3E4FD"}
        ],
        "isBonus": False
    },
    # Workbook - Usia 5-6
    {
        "id": 15,
        "title": "Preschool Alphabet Workbook",
        "category": "Workbook Latihan Huruf / Angka",
        "ageGroup": "5-6",
        "ageLabel": "Usia 5-6 tahun",
        "description": "Workbook lengkap untuk latihan menulis huruf A-Z",
        "price": 10000,
        "fileName": "Preschool Alphabet Workbook.pdf",
        "coverColor": "#F3E5F5",
        "pages": [
            {"page": 1, "color": "#F3E5F5"},
            {"page": 2, "color": "#E9D8F0"},
            {"page": 3, "color": "#DFCBEB"}
        ],
        "isBonus": False
    },
    # Emotional Learning - Usia 7-9
    {
        "id": 16,
        "title": "Feelings Book",
        "category": "Emotional Learning Book",
        "ageGroup": "7-9",
        "ageLabel": "Usia 7-9 tahun",
        "description": "Belajar mengenali dan mengekspresikan perasaan dengan sehat",
        "price": 10000,
        "fileName": "feelings.pdf",
        "coverColor": "#FFE4E1",
        "pages": [
            {"page": 1, "color": "#FFE4E1"},
            {"page": 2, "color": "#FFD6D9"},
            {"page": 3, "color": "#FFC9CE"}
        ],
        "isBonus": False
    },
    {
        "id": 17,
        "title": "Emotions Book",
        "category": "Emotional Learning Book",
        "ageGroup": "7-9",
        "ageLabel": "Usia 7-9 tahun",
        "description": "Memahami berbagai emosi dan cara mengelolanya",
        "price": 10000,
        "fileName": "emotions.pdf",
        "coverColor": "#FCE4EC",
        "pages": [
            {"page": 1, "color": "#FCE4EC"},
            {"page": 2, "color": "#FAD4E0"},
            {"page": 3, "color": "#F8C4D4"}
        ],
        "isBonus": False
    },
    # Science Flashcards - Usia 7-9
    {
        "id": 18,
        "title": "Animal Alphabet Flashcard",
        "category": "Science Flashcards",
        "ageGroup": "7-9",
        "ageLabel": "Usia 7-9 tahun",
        "description": "Kenali hewan dari A sampai Z dengan fakta menarik",
        "price": 10000,
        "fileName": "Animal Alphabet Flashcard.pdf",
        "coverColor": "#E8F5E9",
        "pages": [
            {"page": 1, "color": "#E8F5E9"},
            {"page": 2, "color": "#D8EDD9"},
            {"page": 3, "color": "#C8E5C9"}
        ],
        "isBonus": False
    },
    {
        "id": 19,
        "title": "Animals Flashcards A4",
        "category": "Science Flashcards",
        "ageGroup": "7-9",
        "ageLabel": "Usia 7-9 tahun",
        "description": "Pelajari berbagai hewan dan habitatnya",
        "price": 10000,
        "fileName": "Animals Flashcards A4.pdf",
        "coverColor": "#F1F8E9",
        "pages": [
            {"page": 1, "color": "#F1F8E9"},
            {"page": 2, "color": "#E8F3DC"},
            {"page": 3, "color": "#DFEECD"}
        ],
        "isBonus": False
    },
    {
        "id": 20,
        "title": "Solar System Flashcards",
        "category": "Science Flashcards",
        "ageGroup": "7-9",
        "ageLabel": "Usia 7-9 tahun",
        "description": "Jelajahi tata surya dengan flashcard edukatif",
        "price": 10000,
        "fileName": "Solar-System-Flashcards.pdf",
        "coverColor": "#E8EAF6",
        "pages": [
            {"page": 1, "color": "#E8EAF6"},
            {"page": 2, "color": "#DCDFF3"},
            {"page": 3, "color": "#D0D4F0"}
        ],
        "isBonus": False
    },
    {
        "id": 21,
        "title": "Human Body Flashcards",
        "category": "Science Flashcards",
        "ageGroup": "7-9",
        "ageLabel": "Usia 7-9 tahun",
        "description": "Kenali bagian-bagian tubuh manusia dengan detail",
        "price": 10000,
        "fileName": "human budy Flashcards.pdf",
        "coverColor": "#FFF3E0",
        "pages": [
            {"page": 1, "color": "#FFF3E0"},
            {"page": 2, "color": "#FFEAD0"},
            {"page": 3, "color": "#FFE1C0"}
        ],
        "isBonus": False
    },
    # Emotional Learning - Usia 7-9 (continued)
    {
        "id": 23,
        "title": "Feelings Book 2",
        "category": "Emotional Learning Book",
        "ageGroup": "7-9",
        "ageLabel": "Usia 7-9 tahun",
        "description": "Belajar mengenali dan mengekspresikan perasaan dengan sehat - Edisi 2",
        "price": 10000,
        "fileName": "feelings2.pdf",
        "coverColor": "#FFE4E1",
        "pages": [
            {"page": 1, "color": "#FFE4E1"},
            {"page": 2, "color": "#FFD6D9"},
            {"page": 3, "color": "#FFC9CE"}
        ],
        "isBonus": False
    },
    {
        "id": 24,
        "title": "Emotions Book 2",
        "category": "Emotional Learning Book",
        "ageGroup": "7-9",
        "ageLabel": "Usia 7-9 tahun",
        "description": "Memahami berbagai emosi dan cara mengelolanya - Edisi 2",
        "price": 10000,
        "fileName": "emotions2.pdf",
        "coverColor": "#FCE4EC",
        "pages": [
            {"page": 1, "color": "#FCE4EC"},
            {"page": 2, "color": "#FAD4E0"},
            {"page": 3, "color": "#F8C4D4"}
        ],
        "isBonus": False
    },
    # Science Flashcards - Usia 7-9 (continued)
    {
        "id": 25,
        "title": "Animal Alphabet Flashcard 2",
        "category": "Science Flashcards",
        "ageGroup": "7-9",
        "ageLabel": "Usia 7-9 tahun",
        "description": "Kenali hewan dari A sampai Z dengan fakta menarik - Edisi 2",
        "price": 10000,
        "fileName": "Animal Alphabet Flashcard 2.pdf",
        "coverColor": "#E8F5E9",
        "pages": [
            {"page": 1, "color": "#E8F5E9"},
            {"page": 2, "color": "#D8EDD9"},
            {"page": 3, "color": "#C8E5C9"}
        ],
        "isBonus": False
    },
    {
        "id": 26,
        "title": "Animals Flashcards A4 - 2",
        "category": "Science Flashcards",
        "ageGroup": "7-9",
        "ageLabel": "Usia 7-9 tahun",
        "description": "Pelajari berbagai hewan dan habitatnya - Edisi 2",
        "price": 10000,
        "fileName": "Animals Flashcards A4-2.pdf",
        "coverColor": "#F1F8E9",
        "pages": [
            {"page": 1, "color": "#F1F8E9"},
            {"page": 2, "color": "#E8F3DC"},
            {"page": 3, "color": "#DFEECD"}
        ],
        "isBonus": False
    },
    {
        "id": 27,
        "title": "Solar System Flashcards 2",
        "category": "Science Flashcards",
        "ageGroup": "7-9",
        "ageLabel": "Usia 7-9 tahun",
        "description": "Jelajahi tata surya dengan flashcard edukatif - Edisi 2",
        "price": 10000,
        "fileName": "Solar-System-Flashcards-2.pdf",
        "coverColor": "#E8EAF6",
        "pages": [
            {"page": 1, "color": "#E8EAF6"},
            {"page": 2, "color": "#DCDFF3"},
            {"page": 3, "color": "#D0D4F0"}
        ],
        "isBonus": False
    },
    {
        "id": 28,
        "title": "Human Body Flashcards 2",
        "category": "Science Flashcards",
        "ageGroup": "7-9",
        "ageLabel": "Usia 7-9 tahun",
        "description": "Kenali bagian-bagian tubuh manusia dengan detail - Edisi 2",
        "price": 10000,
        "fileName": "human body Flashcards 2.pdf",
        "coverColor": "#FFF3E0",
        "pages": [
            {"page": 1, "color": "#FFF3E0"},
            {"page": 2, "color": "#FFEAD0"},
            {"page": 3, "color": "#FFE1C0"}
        ],
        "isBonus": False
    },
    # Bonus Pack
    {
        "id": 29,
        "title": "300+ Positive Affirmations for Kids",
        "category": "BONUS PACK",
        "ageGroup": "all",
        "ageLabel": "Semua Usia",
        "description": "Koleksi lengkap afirmasi positif untuk membangun kepercayaan diri anak",
        "price": 0,
        "fileName": "300+ Positive Affirmations for Kids.pdf",
        "coverColor": "#FFD700",
        "isBonus": True,
        "pages": [
            {"page": 1, "color": "#FFD700"},
            {"page": 2, "color": "#FFC700"},
            {"page": 3, "color": "#FFB700"}
        ]
    },
    {
        "id": 30,
        "title": "Growth Mindset Activities",
        "category": "BONUS PACK",
        "ageGroup": "all",
        "ageLabel": "Semua Usia",
        "description": "Aktivitas menarik untuk mengembangkan pola pikir bertumbuh",
        "price": 0,
        "fileName": "Growth Mindset Activities.pdf",
        "coverColor": "#FFD700",
        "isBonus": True,
        "pages": [
            {"page": 1, "color": "#FFD700"},
            {"page": 2, "color": "#FFC700"},
            {"page": 3, "color": "#FFB700"}
        ]
    }
]


async def seed_database():
    """Seed the database with initial ebook data"""
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    try:
        # Clear existing ebooks
        result = await db.ebooks.delete_many({})
        print(f"✅ Cleared {result.deleted_count} existing ebooks")
        
        # Insert new ebooks
        result = await db.ebooks.insert_many(ebooks_data)
        print(f"✅ Inserted {len(result.inserted_ids)} ebooks")
        
        # Create indexes
        await db.ebooks.create_index("id", unique=True)
        await db.ebooks.create_index("category")
        await db.ebooks.create_index("ageGroup")
        print("✅ Created indexes")
        
        # Create indexes for orders
        await db.orders.create_index("orderId", unique=True)
        await db.orders.create_index("customerEmail")
        await db.orders.create_index("paymentStatus")
        print("✅ Created order indexes")
        
        # Create indexes for payments
        await db.payments.create_index("orderId")
        await db.payments.create_index("midtransTransactionId")
        print("✅ Created payment indexes")
        
        print("\n🎉 Database seeding completed successfully!")
        print(f"📚 Total ebooks: {len(ebooks_data)}")
        
    except Exception as e:
        print(f"❌ Error seeding database: {str(e)}")
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(seed_database())
