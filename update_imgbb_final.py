"""
Update database dengan ImgBB URLs yang BENAR
Fix typo: i.ibb.co.com -> i.ibb.co
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

# ImgBB URLs - FIXED format (i.ibb.co bukan i.ibb.co.com)
imgbb_urls = {
    1: [
        "https://i.ibb.co/Fkdp2Nxr/1-page1.png",
        "https://i.ibb.co/XfrxTjd3/1-page2.png",
        "https://i.ibb.co/fYWzv1q9/1-page3.png"
    ],
    2: [
        "https://i.ibb.co/7dFgYNVp/2-page1.png",
        "https://i.ibb.co/rG6xSrcH/2-page2.png",
        "https://i.ibb.co/spPqSVT5/2-page3.png"
    ],
    3: [
        "https://i.ibb.co/Q3RnCBvk/3-page1.png",
        "https://i.ibb.co/4Rh2hZ6T/3-page2.png",
        "https://i.ibb.co/W4Bj9shN/3-page3.png"
    ],
    4: [
        "https://i.ibb.co/hwybk2C/4-page1.png",
        "https://i.ibb.co/6JwVVYRJ/4-page2.png",
        "https://i.ibb.co/fzz61pL9/4-page3.png"
    ],
    5: [
        "https://i.ibb.co/fz9LqLSM/5-page1.png",
        "https://i.ibb.co/HDvvhhWf/5-page2.png",
        "https://i.ibb.co/cfH9MZc/5-page3.png"
    ],
    6: [
        "https://i.ibb.co/pvgP7FN4/6-page1.png",
        "https://i.ibb.co/Q7b9gkyZ/6-page2.png",
        "https://i.ibb.co/fzk9zfNK/6-page3.png"
    ],
    7: [
        "https://i.ibb.co/nMyZNL4k/7-page1.png",
        "https://i.ibb.co/BK2BTVnh/7-page2.png",
        "https://i.ibb.co/0yDQRDms/7-page3.png"
    ],
    8: [
        "https://i.ibb.co/WpYZYnj6/8-page1.png",
        "https://i.ibb.co/0y9DtKpx/8-page2.png",
        "https://i.ibb.co/6JpTthWd/8-page3.png"
    ],
    9: [
        "https://i.ibb.co/8G6r00z/9-page1.png",
        "https://i.ibb.co/bgYnJ7qr/9-page2.png",
        "https://i.ibb.co/Hpd8GZKf/9-page3.png"
    ],
    10: [
        "https://i.ibb.co/HpM3Sw5d/10-page1.png",
        "https://i.ibb.co/Cppm9sws/10-page2.png",
        "https://i.ibb.co/VWTFpQYx/10-page3.png"
    ],
    11: [
        "https://i.ibb.co/HDQYD6TZ/11-page1.png",
        "https://i.ibb.co/jZfMDjKy/11-page2.png",
        "https://i.ibb.co/7dsLDFbf/11-page3.png"
    ],
    12: [
        "https://i.ibb.co/rfQtTKsQ/12-page1.png",
        "https://i.ibb.co/BptdBXH/12-page2.png",
        "https://i.ibb.co/8L2BRqx2/12-page3.png"
    ],
    13: [
        "https://i.ibb.co/MxKPxYMM/13-page1.png",
        "https://i.ibb.co/VcXvxqQZ/13-page2.png",
        "https://i.ibb.co/7xtxC0rR/13-page3.png"
    ],
    14: [
        "https://i.ibb.co/kgLb9RyL/14-page1.png",
        "https://i.ibb.co/gFwzLx3F/14-page2.png",
        "https://i.ibb.co/nMWS7rtK/14-page3.png"
    ],
    15: [
        "https://i.ibb.co/4wPtrq7s/15-page1.png",
        "https://i.ibb.co/4Cj46Lq/15-page2.png",
        "https://i.ibb.co/gF3nG2tB/15-page3.png"
    ],
    16: [
        "https://i.ibb.co/hFFhXmZ2/16-page1.png",
        "https://i.ibb.co/SDhw1rNQ/16-page2.png",
        "https://i.ibb.co/x0KQHsW/16-page3.png"
    ],
    17: [
        "https://i.ibb.co/Nq0bJBw/17-page1.png",
        "https://i.ibb.co/1yhGKwp/17-page2.png",
        "https://i.ibb.co/n8nPS5zY/17-page3.png"
    ],
    18: [
        "https://i.ibb.co/fYftddFD/18-page1.png",
        "https://i.ibb.co/d0SgYXwD/18-page2.png",
        "https://i.ibb.co/fGXR64KN/18-page3.png"
    ],
    19: [
        "https://i.ibb.co/Kxn3JByy/19-page1.png",
        "https://i.ibb.co/hRBxgtWt/19-page2.png",
        "https://i.ibb.co/cKyqKbW0/19-page3.png"
    ],
    20: [
        "https://i.ibb.co/6czn5nsG/20-page1.png",
        "https://i.ibb.co/yBmkzHNM/20-page2.png",
        "https://i.ibb.co/1Dn31JL/20-page3.png"
    ],
    21: [
        "https://i.ibb.co/hRSzSGkN/21-page1.png",
        "https://i.ibb.co/ps87zYX/21-page2.png",
        "https://i.ibb.co/jP46tqPc/21-page3.png"
    ],
    22: [
        "https://i.ibb.co/Vpz0n6Lp/22-page1.png",
        "https://i.ibb.co/5hd5fQ2Y/22-page2.png",
        "https://i.ibb.co/xqxgfLw7/22-page3.png"
    ],
    23: [
        "https://i.ibb.co/7JMBm9bm/23-page1.png",
        "https://i.ibb.co/6Lbjj3V/23-page2.png",
        "https://i.ibb.co/SXwwb65Y/23-page3.png"
    ],
    24: [
        "https://i.ibb.co/F4c7DYWG/24-page1.png",
        "https://i.ibb.co/5xjRx1c6/24-page2.png",
        "https://i.ibb.co/xq6HFQS6/24-page3.png"
    ],
    25: [
        "https://i.ibb.co/jPZycF7f/25-page1.png",
        "https://i.ibb.co/dwJMM3z8/25-page2.png",
        "https://i.ibb.co/dwJMM3z8/25-page2.png"
    ],
    26: [
        "https://i.ibb.co/RpyJxj61/26-page1.png",
        "https://i.ibb.co/dsCZBXC9/26-page2.png",
        "https://i.ibb.co/S792bQFT/26-page3.png"
    ],
    27: [
        "https://i.ibb.co/mmkvwVP/27-page1.png",
        "https://i.ibb.co/xS85cRKY/27-page2.png",
        "https://i.ibb.co/jvtQ7zcr/27-page3.png"
    ],
    28: [
        "https://i.ibb.co/mVvbdmyK/28-page1.png",
        "https://i.ibb.co/20xKVtZL/28-page2.png",
        "https://i.ibb.co/99Ppdnyd/28-page3.png"
    ],
    29: [
        "https://i.ibb.co/mCpMqs9n/29-page1.png",
        "https://i.ibb.co/gbKsvS2Z/29-page2.png",
        "https://i.ibb.co/PGQzTB8d/29-page3.png"
    ],
    30: [
        "https://i.ibb.co/jkxkWL9f/30-page1.png",
        "https://i.ibb.co/mCsG9nSc/30-page2.png",
        "https://i.ibb.co/R40XM08W/30-page3.png"
    ]
}


async def update_final():
    """Update database dengan ImgBB URLs - FINAL VERSION"""
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    try:
        print("🖼️  Updating dengan ImgBB URLs (FINAL)...\n")
        
        updated = 0
        for ebook_id, urls in imgbb_urls.items():
            existing = await db.ebooks.find_one({'id': ebook_id})
            if not existing:
                print(f"⚠️  Ebook {ebook_id} not found, skipping...")
                continue
            
            updated_pages = []
            for i, url in enumerate(urls, 1):
                existing_page = next((p for p in existing.get('pages', []) if p['page'] == i), None)
                updated_page = {
                    'page': i,
                    'imageUrl': url,
                    'color': existing_page.get('color', '#F5F5F5') if existing_page else '#F5F5F5'
                }
                updated_pages.append(updated_page)
            
            await db.ebooks.update_one(
                {'id': ebook_id},
                {'$set': {'pages': updated_pages}}
            )
            updated += 1
            print(f"✅ Ebook {ebook_id} - {existing.get('title', 'Unknown')}")
        
        print(f"\n🎉 SUCCESS! Updated {updated}/{len(imgbb_urls)} ebooks")
        
        # Verify
        sample = await db.ebooks.find_one({'id': 1})
        if sample and 'pages' in sample:
            print(f"\n📸 Sample URL (Ebook 1):")
            print(f"   {sample['pages'][0]['imageUrl']}")
            print(f"\n✅ Format benar: i.ibb.co dengan extension .png")
    
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(update_final())
