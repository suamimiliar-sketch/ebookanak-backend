"""
Update database with ImgBB image URLs
Fix format from ibb.co.com to i.ibb.co
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

# ImgBB URLs - fixed format
imgbb_urls = {
    1: [
        "https://i.ibb.co/1Y4c1hvg",
        "https://i.ibb.co/kVs2F5r9",
        "https://i.ibb.co/WWX4txG0"
    ],
    2: [
        "https://i.ibb.co/RkWhv4P6",
        "https://i.ibb.co/1fqr5WdT",
        "https://i.ibb.co/JWdHLsYx"
    ],
    3: [
        "https://i.ibb.co/rRSMcP23",
        "https://i.ibb.co/SwFcFXhn",
        "https://i.ibb.co/zTPDcNMW"
    ],
    4: [
        "https://i.ibb.co/BFtbmTw",
        "https://i.ibb.co/mFT11JCF",
        "https://i.ibb.co/hJJQ7Wwc"
    ],
    5: [
        "https://i.ibb.co/678LrLZY",
        "https://i.ibb.co/zhcc66yT",
        "https://i.ibb.co/x90bPBS"
    ],
    6: [
        "https://i.ibb.co/C5qtcG4V",
        "https://i.ibb.co/zWnsMFq1",
        "https://i.ibb.co/Kp2DpdsQ"
    ],
    7: [
        "https://i.ibb.co/TMGpxgJh",
        "https://i.ibb.co/CsKQV5Pj",
        "https://i.ibb.co/Wvxs4xGV"
    ],
    8: [
        "https://i.ibb.co/84SqSMt0",
        "https://i.ibb.co/CK9126pf",
        "https://i.ibb.co/QjqTHBK5"
    ],
    9: [
        "https://i.ibb.co/xwJ1DDm",
        "https://i.ibb.co/d0Xyg71Q",
        "https://i.ibb.co/1J6WRc0t"
    ],
    10: [
        "https://i.ibb.co/4gD3qvhd",
        "https://i.ibb.co/p66bKr1r",
        "https://i.ibb.co/hRVG1ZFc"
    ],
    11: [
        "https://i.ibb.co/VW8DWRY6",
        "https://i.ibb.co/sJRwqXSK",
        "https://i.ibb.co/Ndcbqz7v"
    ],
    12: [
        "https://i.ibb.co/jZ85B9R8",
        "https://i.ibb.co/dTr1Dds",
        "https://i.ibb.co/wFCLbVQC"
    ],
    13: [
        "https://i.ibb.co/mVdhVL66",
        "https://i.ibb.co/q3bRCrWf",
        "https://i.ibb.co/bj5jmGN2"
    ],
    14: [
        "https://i.ibb.co/GvZYtKJZ",
        "https://i.ibb.co/HpYnfjVp",
        "https://i.ibb.co/8ghVrMtQ"
    ],
    15: [
        "https://i.ibb.co/kVQBC7x3",
        "https://i.ibb.co/LBC9LyF",
        "https://i.ibb.co/tP4dSGYW"
    ],
    16: [
        "https://i.ibb.co/PGG3T691",
        "https://i.ibb.co/20D3LNq8",
        "https://i.ibb.co/RmGWySf"
    ],
    17: [
        "https://i.ibb.co/6SKLTC6",
        "https://i.ibb.co/69V0bfp",
        "https://i.ibb.co/CsMPFThY"
    ],
    18: [
        "https://i.ibb.co/QFLnvvQD",
        "https://i.ibb.co/0jktb1Rr",
        "https://i.ibb.co/VpLyn2hC"
    ],
    19: [
        "https://i.ibb.co/hF0tSr88",
        "https://i.ibb.co/SXtD69n9",
        "https://i.ibb.co/ZRf9RHQ5"
    ],
    20: [
        "https://i.ibb.co/xKWCQC5w",
        "https://i.ibb.co/vvCdN0cr",
        "https://i.ibb.co/v7BbpvH"
    ],
    21: [
        "https://i.ibb.co/1fkWkC3N",
        "https://i.ibb.co/S18jnFv",
        "https://i.ibb.co/C301L43k"
    ],
    22: [
        "https://i.ibb.co/tPvwjRHP",
        "https://i.ibb.co/chPN7Wxb",
        "https://i.ibb.co/m5fyXTdc"
    ],
    23: [
        "https://i.ibb.co/xS9wT43T",
        "https://i.ibb.co/P04qq73",
        "https://i.ibb.co/kg22jG5b"
    ],
    24: [
        "https://i.ibb.co/9HBYr4vR",
        "https://i.ibb.co/LhgZh0p8",
        "https://i.ibb.co/DHgWW6S0"
    ],
    25: [
        "https://i.ibb.co/Kpz2MHCh",
        "https://i.ibb.co/DHgWW6S0",
        "https://i.ibb.co/DHgWW6S0"
    ],
    26: [
        "https://i.ibb.co/5WFJNKjd",
        "https://i.ibb.co/mrZpJdZs",
        "https://i.ibb.co/WpYQZDm9"
    ],
    27: [
        "https://i.ibb.co/62zvx7q",
        "https://i.ibb.co/8D48RSnb",
        "https://i.ibb.co/qM6cbCtr"
    ],
    28: [
        "https://i.ibb.co/fz8qZbNW",
        "https://i.ibb.co/4wzNvT1D",
        "https://i.ibb.co/xSZ2rhzr"
    ],
    29: [
        "https://i.ibb.co/TByF8X4Q",
        "https://i.ibb.co/9m5RwbDH",
        "https://i.ibb.co/qY5F0bwv"
    ],
    30: [
        "https://i.ibb.co/whbhwKZg",
        "https://i.ibb.co/BVDtyhwC",
        "https://i.ibb.co/fGp3KpJ7"
    ]
}


async def update_with_imgbb():
    """Update database dengan ImgBB URLs"""
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    try:
        print("🖼️  Updating dengan ImgBB URLs...\n")
        
        updated = 0
        for ebook_id, urls in imgbb_urls.items():
            existing = await db.ebooks.find_one({'id': ebook_id})
            if not existing:
                print(f"⚠️  Ebook {ebook_id} not found")
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
            print(f"✅ Ebook {ebook_id} updated with ImgBB URLs")
        
        print(f"\n🎉 Success! Updated {updated} ebooks")
        
        # Verify
        sample = await db.ebooks.find_one({'id': 1})
        if sample and 'pages' in sample:
            print(f"\n📸 Sample URL: {sample['pages'][0]['imageUrl']}")
    
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(update_with_imgbb())
