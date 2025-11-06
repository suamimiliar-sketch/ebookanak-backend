"""
Fix production database - Add Cloudinary image URLs to ebook pages
Run this to update production database with correct thumbnails
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# Production database (change if needed)
MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "fun-learning-7-pelangi_pintar"  # Production DB name

# Cloudinary image URLs for each ebook
ebook_image_updates = [
    {
        "id": 1,
        "pages": [
            {"page": 1, "color": "#FFE4E1", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753244/1_page1_soiffs.jpg"},
            {"page": 2, "color": "#FFD6D9", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753244/1_page2_soxveh.jpg"},
            {"page": 3, "color": "#FFC9CE", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753245/1_page3_ln78ii.jpg"}
        ]
    },
    {
        "id": 2,
        "pages": [
            {"page": 1, "color": "#E6F3FF", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753245/2_page1_oyfvqf.jpg"},
            {"page": 2, "color": "#D6EBFF", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753245/2_page2_fqppxz.jpg"},
            {"page": 3, "color": "#C6E3FF", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753245/2_page3_hbdqf5.jpg"}
        ]
    },
    {
        "id": 3,
        "pages": [
            {"page": 1, "color": "#FFF9E6", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753245/3_page1_m45z1a.jpg"},
            {"page": 2, "color": "#FFF4D6", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753246/3_page2_r7fkxe.jpg"},
            {"page": 3, "color": "#FFEFC6", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753246/3_page3_abxq0m.jpg"}
        ]
    },
    {
        "id": 4,
        "pages": [
            {"page": 1, "color": "#E8F5E9", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753246/4_page1_o2fmxa.jpg"},
            {"page": 2, "color": "#D8EDD9", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753246/4_page2_gnxgqt.jpg"},
            {"page": 3, "color": "#C8E5C9", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753247/4_page3_xf3cst.jpg"}
        ]
    },
    {
        "id": 5,
        "pages": [
            {"page": 1, "color": "#FFF3E0", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753247/5_page1_r25uyh.jpg"},
            {"page": 2, "color": "#FFEBD0", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753247/5_page2_hcx0os.jpg"},
            {"page": 3, "color": "#FFE3C0", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753248/5_page3_t0qrxd.jpg"}
        ]
    },
    {
        "id": 6,
        "pages": [
            {"page": 1, "color": "#F3E5F5", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753248/6_page1_gvmtkf.jpg"},
            {"page": 2, "color": "#EBDAF3", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753248/6_page2_nysppn.jpg"},
            {"page": 3, "color": "#E3D0F1", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753248/6_page3_fzdnth.jpg"}
        ]
    },
    {
        "id": 7,
        "pages": [
            {"page": 1, "color": "#FCE4EC", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753249/7_page1_b52fcv.jpg"},
            {"page": 2, "color": "#F8D8E4", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753249/7_page2_kq0xhp.jpg"},
            {"page": 3, "color": "#F4CCDC", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753249/7_page3_qhkhud.jpg"}
        ]
    },
    {
        "id": 8,
        "pages": [
            {"page": 1, "color": "#E1F5FE", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753250/8_page1_tqilwj.jpg"},
            {"page": 2, "color": "#D3EDFC", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753250/8_page2_vb7hms.jpg"},
            {"page": 3, "color": "#C5E5FA", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753250/8_page3_igzlqt.jpg"}
        ]
    },
    {
        "id": 9,
        "pages": [
            {"page": 1, "color": "#FFF8E1", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753251/9_page1_okjmgf.jpg"},
            {"page": 2, "color": "#FFF3D1", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753251/9_page2_lj7wgf.jpg"},
            {"page": 3, "color": "#FFEEC1", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753251/9_page3_yjupcd.jpg"}
        ]
    },
    {
        "id": 10,
        "pages": [
            {"page": 1, "color": "#F1F8E9", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753252/10_page1_hwowqz.jpg"},
            {"page": 2, "color": "#E6F3DA", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753252/10_page2_wr6ajj.jpg"},
            {"page": 3, "color": "#DBEECB", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753252/10_page3_kpn62d.jpg"}
        ]
    },
    {
        "id": 11,
        "pages": [
            {"page": 1, "color": "#FFE0E0", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753253/11_page1_fzm5qx.jpg"},
            {"page": 2, "color": "#FFD2D2", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753253/11_page2_zmhsmd.jpg"},
            {"page": 3, "color": "#FFC4C4", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753254/11_page3_vpk5wb.jpg"}
        ]
    },
    {
        "id": 12,
        "pages": [
            {"page": 1, "color": "#E0F2F7", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753254/12_page1_gltnk9.jpg"},
            {"page": 2, "color": "#D1EAF3", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753254/12_page2_pxf7nm.jpg"},
            {"page": 3, "color": "#C2E2EF", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753255/12_page3_u3p8nc.jpg"}
        ]
    },
    {
        "id": 13,
        "pages": [
            {"page": 1, "color": "#FFF9C4", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753255/13_page1_c6hqix.jpg"},
            {"page": 2, "color": "#FFF6B4", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753255/13_page2_yxlhad.jpg"},
            {"page": 3, "color": "#FFF3A4", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753256/13_page3_uqziqz.jpg"}
        ]
    },
    # Continue for all 29 ebooks...
    # (IDs 14-29 with their respective Cloudinary URLs)
]

async def update_production_database():
    """Update production database with image URLs"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    updated_count = 0
    
    print(f"🔄 Updating database: {DB_NAME}")
    print(f"📊 Total ebooks to update: {len(ebook_image_updates)}")
    
    for ebook_update in ebook_image_updates:
        ebook_id = ebook_update["id"]
        new_pages = ebook_update["pages"]
        
        # Update the ebook with new pages data
        result = await db.ebooks.update_one(
            {"id": ebook_id},
            {"$set": {"pages": new_pages}}
        )
        
        if result.modified_count > 0:
            updated_count += 1
            print(f"✅ Updated ebook ID {ebook_id}")
        else:
            print(f"⚠️  Ebook ID {ebook_id} not found or already updated")
    
    # Verify update
    total_with_images = await db.ebooks.count_documents({"pages.0.imageUrl": {"$ne": None}})
    
    client.close()
    
    print(f"\n🎉 Update completed!")
    print(f"📚 Ebooks updated: {updated_count}/{len(ebook_image_updates)}")
    print(f"✅ Total ebooks with images: {total_with_images}")

if __name__ == "__main__":
    asyncio.run(update_production_database())
