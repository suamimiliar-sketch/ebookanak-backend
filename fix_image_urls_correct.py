"""
Update dengan format URL yang BENAR untuk tag <img>
Format: https://drive.google.com/uc?id=FILE_ID (tanpa export parameter)
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

# Data dengan format URL yang BENAR untuk <img> tag
image_urls = {
    1: [
        "https://drive.google.com/uc?id=1MVHReqJ9QPoLhpSC35Wt24laF7WC9j0i",
        "https://drive.google.com/uc?id=1j8z4lO95hZahk4YhCwCXbRqOea2uach9",
        "https://drive.google.com/uc?id=1wuWNMfJe99JuYOKgHR0YW3OWwZAETBxq"
    ],
    2: [
        "https://drive.google.com/uc?id=1_ahIeVEE_-JnDgUGETl0fGGmePYlyqRZ",
        "https://drive.google.com/uc?id=1QnlHsdMTOfbq_Ka4II6XFrEaJBtV2mTp",
        "https://drive.google.com/uc?id=1GYnbb9V8_D5ohLWxi-zV1q998dGWVI0Z"
    ],
    3: [
        "https://drive.google.com/uc?id=11wBu20wWGx42pV3wEt-gms6WJg8XjRJK",
        "https://drive.google.com/uc?id=1eNhlYpsgZYanlp6zdXjB8YYdTD3PrSE4",
        "https://drive.google.com/uc?id=1B4g2tq9T4i9zjmHxvBrnqVcIcpPc-3Fs"
    ],
    4: [
        "https://drive.google.com/uc?id=1pnndnS3F7fm9aj2-5NBOe_lmMEXogIef",
        "https://drive.google.com/uc?id=1s453I_LySbVLP8eNm15DoWx2zNlL5Sn7",
        "https://drive.google.com/uc?id=18Rd20AX84K-kjJBdvUJmB4zPGJCwvgOo"
    ],
    5: [
        "https://drive.google.com/uc?id=11ltuN3_fIIL1eg1pRVpBJCukNjdI21dH",
        "https://drive.google.com/uc?id=1mktn2vt3og8SMjJYa19X0_AkMyKbfqu5",
        "https://drive.google.com/uc?id=1PuJdeuuQiZ4VzfGV3ip5-UCp2HTAGn9b"
    ],
    6: [
        "https://drive.google.com/uc?id=19g-kSODAYygZeEVWnIQTZIfAUcnPnq7r",
        "https://drive.google.com/uc?id=1LufsKGjeFUgz8xujDD0g-9sa9iIsIuTf",
        "https://drive.google.com/uc?id=1ympENCDRHW8RrvITnVo9mZnoz-uA9BHJ"
    ],
    7: [
        "https://drive.google.com/uc?id=1pV3Zu2hOFWKz_eNvAbY8ax5DUUwfLjA3",
        "https://drive.google.com/uc?id=1A_nS6rr18STa1dUO2DNMjmPoikeWzOa2",
        "https://drive.google.com/uc?id=1rn5Bu-7_dh_c46BdB9hLmdRNff3qQ3-F"
    ],
    8: [
        "https://drive.google.com/uc?id=1zUppKuNfl6zI24le7V-pvf64iatQpS32",
        "https://drive.google.com/uc?id=15yvngtaH2jve2ZNtSN7cQLHYaGlq1Gz4",
        "https://drive.google.com/uc?id=1dqLUg5lY4q4_6pPEv7gegBr5JNf3vhdM"
    ],
    9: [
        "https://drive.google.com/uc?id=1FrsyAb2mDXXLQbhS3OjI0ZOs70URyimf",
        "https://drive.google.com/uc?id=1lQ5rSSI_ygsGqemFBEuSVElyaYSrdX1Y",
        "https://drive.google.com/uc?id=11D9H8LzHIOCCFlhom_kQL82-JOv9-mgr"
    ],
    10: [
        "https://drive.google.com/uc?id=1ONI52E-YSNuFN8mDSOE-ywb5KDCPbOUb",
        "https://drive.google.com/uc?id=12SRaebnH4B4_nSgeEsRiqKcMPkXXlI-X",
        "https://drive.google.com/uc?id=1YBuv3mEVuRdyUco2oLklUzQ9WDiZe31i"
    ],
    11: [
        "https://drive.google.com/uc?id=1QZHVo8GTnsAlmbYWbb52WiW9Hj_ezHn1",
        "https://drive.google.com/uc?id=1JMM_RLVLRWBNAebG3pw6IArVQsi4ZH3r",
        "https://drive.google.com/uc?id=1eNh0wo6XLKapj40AuOMVMJvYA-lvEVLb"
    ],
    12: [
        "https://drive.google.com/uc?id=108kTUOSrAJFxTwAp71eTt7skzHy-3Slz",
        "https://drive.google.com/uc?id=1HMYuzT3nzKOwExrJU9JwB2CZX8gIQ5tp",
        "https://drive.google.com/uc?id=1tX5Kv5yUZvxcltnuqo7dTGCn8BFbvH6n"
    ],
    13: [
        "https://drive.google.com/uc?id=1xgwkhrNKHTyWfSKnqjBBm3EmJ43IBWcW",
        "https://drive.google.com/uc?id=1KlPGZSXTgG4U8OdXZW-WeGtkWlvJEDU1",
        "https://drive.google.com/uc?id=1dKp7moqNz-xLCBcdeNpgNO7o68ByVYNU"
    ],
    14: [
        "https://drive.google.com/uc?id=13aEaauqdbl_FYSQ29n44-0zsISgJ1b3v",
        "https://drive.google.com/uc?id=1bgDLVBCTRqgEZ_x8dSk-ayMVJ_4tLPz1",
        "https://drive.google.com/uc?id=1cQfuT8GjkGNBc2L_1LDY88uaELLSxojy"
    ],
    15: [
        "https://drive.google.com/uc?id=1R6DEpjFQKCMIDwalee8w9Vu2rvkkIeMK",
        "https://drive.google.com/uc?id=1XS2Mr2RqTxE8R5oI-z3xb3_ZJT4BqLow",
        "https://drive.google.com/uc?id=1NZEVZsbO79n83j8P_rTvCzhWHR8J8Edg"
    ],
    16: [
        "https://drive.google.com/uc?id=1E_zmObkaiUP3c9bqafZFqLMO9821nTE1",
        "https://drive.google.com/uc?id=1apKgJppS2reRiGvijbbQm6Mu2kAktT8H",
        "https://drive.google.com/uc?id=1FOTeiivpNwOIEaE5jEqg6OT8M3M054MI"
    ],
    17: [
        "https://drive.google.com/uc?id=1sulXoO8-IL2g22mxleLCZ1IkTFfy_Bcq",
        "https://drive.google.com/uc?id=1G6UQt8YzRc_G9ceQBtRCzHJhEsMcFwDa",
        "https://drive.google.com/uc?id=1WY8q1UXbrRrHFfEIBVvl5qbrhyg2UXje"
    ],
    18: [
        "https://drive.google.com/uc?id=1ULZLBfJwk0CwsB00DRvz8oq5HiR15ShR",
        "https://drive.google.com/uc?id=11RKa6eJiTvQbJY5FhP9I6M-raLhondL6",
        "https://drive.google.com/uc?id=1FEIwG2S0FVCXy7_CQWx0wZgMBbTlhfMX"
    ],
    19: [
        "https://drive.google.com/uc?id=1nR8JFVxnE9ymYFXfgI2R5NSs2U4cqfzL",
        "https://drive.google.com/uc?id=1_us6cgf2LBrgEMR-4e8IMrVvZsuCAINv",
        "https://drive.google.com/uc?id=17ZNP4Dc3Kh6fqPUGWgpLGsOmbvjj2IPT"
    ],
    20: [
        "https://drive.google.com/uc?id=1pF6tU9e8U0isDIGSnocm3qvFrreYYNyH",
        "https://drive.google.com/uc?id=1-o-GuFcUY-rolGsD9A84H9H7gs70VhNY",
        "https://drive.google.com/uc?id=1ACPiPlqA6rcHWYPGWIx3J-LPbwLdBkeR"
    ],
    21: [
        "https://drive.google.com/uc?id=1ACPiPlqA6rcHWYPGWIx3J-LPbwLdBkeR",
        "https://drive.google.com/uc?id=1l-aNc4x0U8AqRWJipHiJoBWshzD3q9zb",
        "https://drive.google.com/uc?id=1HhXbNSlrevZxmI_U6orqiYoskPAOEHfN"
    ],
    22: [
        "https://drive.google.com/uc?id=1T6oa4-mqmVmA0I42ZWul7X1UINQmBz_D",
        "https://drive.google.com/uc?id=1dSVTVUr-QmRNjf4zdrhsnD2o3ibBzGSE",
        "https://drive.google.com/uc?id=1vi-diAYGvOuRtqAwyRky4RC_qGyBJlDU"
    ],
    23: [
        "https://drive.google.com/uc?id=1rxhtlVu2uHaULybIgd6wZ4s2mg7nMYYY",
        "https://drive.google.com/uc?id=10U80dqdTddUzJJJMf-quqzoiSsKN3YhB",
        "https://drive.google.com/uc?id=1HeATgcXHHo3WXNz3eBJbD0b9Yq6dfcRY"
    ],
    24: [
        "https://drive.google.com/uc?id=1_tuJEQ6OPuvJwLcBsysLTMw6an9rCq-P",
        "https://drive.google.com/uc?id=1J9r_b_2s7iJ3qqjZYcXukTJtliXERvq2",
        "https://drive.google.com/uc?id=1ZQpABiPDyEbH-_2gKfVMqwOBOpYzZMZ4"
    ],
    25: [
        "https://drive.google.com/uc?id=1o_8fbMgeL_7tJTOevf43GJbR3jCv_t_L",
        "https://drive.google.com/uc?id=1HokfUObPjBDaywkyzCFrphaZOaEjxVE0",
        "https://drive.google.com/uc?id=1HokfUObPjBDaywkyzCFrphaZOaEjxVE0"
    ],
    26: [
        "https://drive.google.com/uc?id=1XSwS_mWV3l5sarCS3QEZe-zc45dWUk_N",
        "https://drive.google.com/uc?id=1VuImT2BUAa_9ddcECoxXATaoL7eTgoO0",
        "https://drive.google.com/uc?id=1TUmBxzbkg09E2mQOiP_12Rxcif4hlc0h"
    ],
    27: [
        "https://drive.google.com/uc?id=1it5dEjdpeEggWcfWAaVv6EELY9Y4d5db",
        "https://drive.google.com/uc?id=11iJ6VeWXsOzal0HX8ma-dSXOIr44n8XY",
        "https://drive.google.com/uc?id=1z1Wmy1r98ijlRv1VSP37svqjMSeUVo8m"
    ],
    28: [
        "https://drive.google.com/uc?id=1yF_Tscr_k_FVCfDO5c5RQEEGyO44xofl",
        "https://drive.google.com/uc?id=1heHo5ygZ8UcqFWfHL3PlfcvOWN_jzP7j",
        "https://drive.google.com/uc?id=1WQquaF-b3_KOh_1uN7JEOrdpRMhAkQ2S"
    ],
    29: [
        "https://drive.google.com/uc?id=1Nt7sOgRDRG8l4wL0JvGPf_O-F0eDzIbb",
        "https://drive.google.com/uc?id=1A3KqDObKlNrEGNCEmjGInwoEX9ttEHAz",
        "https://drive.google.com/uc?id=16RbDn98Ka8dMlyxZ8DJqDKHk0fZC-HJu"
    ],
    30: [
        "https://drive.google.com/uc?id=1-tEkYOYa-B7r2aG7Oj88kFRrLtvAq0Re",
        "https://drive.google.com/uc?id=1lEgg7NGL9n4SgUDDnETatC03thv-K800",
        "https://drive.google.com/uc?id=1JCsWitOZZHbEg8eTnk2Ffs4j2xTaKEp5"
    ]
}


async def update_correct_format():
    """Update dengan format URL yang benar untuk <img> tag"""
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    try:
        print("🔄 Updating dengan format URL yang BENAR untuk <img>...\n")
        
        updated_count = 0
        for ebook_id, urls in image_urls.items():
            # Get existing ebook
            existing = await db.ebooks.find_one({'id': ebook_id})
            if not existing:
                print(f"⚠️  Ebook ID {ebook_id} not found")
                continue
            
            # Update pages dengan URL yang benar
            updated_pages = []
            for i, url in enumerate(urls, 1):
                existing_page = next((p for p in existing.get('pages', []) if p['page'] == i), None)
                updated_page = {
                    'page': i,
                    'imageUrl': url,
                    'color': existing_page.get('color', '#F5F5F5') if existing_page else '#F5F5F5'
                }
                updated_pages.append(updated_page)
            
            result = await db.ebooks.update_one(
                {'id': ebook_id},
                {'$set': {'pages': updated_pages}}
            )
            
            if result.modified_count > 0:
                updated_count += 1
                print(f"✅ Ebook ID {ebook_id} updated")
        
        print(f"\n🎉 Update selesai!")
        print(f"📊 Total: {updated_count}/{len(image_urls)}")
        
        # Verify
        example = await db.ebooks.find_one({'id': 1})
        if example and 'pages' in example:
            print(f"\n📸 Format BARU (untuk <img> tag):")
            print(f"   {example['pages'][0]['imageUrl']}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(update_correct_format())
