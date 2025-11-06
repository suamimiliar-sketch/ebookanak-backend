"""
Kembalikan ke format URL asli yang sudah terbukti working
Menggunakan format uc?export=view yang sudah diberikan user
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

# Data asli yang diberikan user dengan format yang sudah working
original_urls = {
    1: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=1MVHReqJ9QPoLhpSC35Wt24laF7WC9j0i"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=1j8z4lO95hZahk4YhCwCXbRqOea2uach9"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=1wuWNMfJe99JuYOKgHR0YW3OWwZAETBxq"}
        ]
    },
    2: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=1_ahIeVEE_-JnDgUGETl0fGGmePYlyqRZ"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=1QnlHsdMTOfbq_Ka4II6XFrEaJBtV2mTp"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=1GYnbb9V8_D5ohLWxi-zV1q998dGWVI0Z"}
        ]
    },
    3: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=11wBu20wWGx42pV3wEt-gms6WJg8XjRJK"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=1eNhlYpsgZYanlp6zdXjB8YYdTD3PrSE4"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=1B4g2tq9T4i9zjmHxvBrnqVcIcpPc-3Fs"}
        ]
    },
    4: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=1pnndnS3F7fm9aj2-5NBOe_lmMEXogIef"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=1s453I_LySbVLP8eNm15DoWx2zNlL5Sn7"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=18Rd20AX84K-kjJBdvUJmB4zPGJCwvgOo"}
        ]
    },
    5: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=11ltuN3_fIIL1eg1pRVpBJCukNjdI21dH"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=1mktn2vt3og8SMjJYa19X0_AkMyKbfqu5"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=1PuJdeuuQiZ4VzfGV3ip5-UCp2HTAGn9b"}
        ]
    },
    6: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=19g-kSODAYygZeEVWnIQTZIfAUcnPnq7r"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=1LufsKGjeFUgz8xujDD0g-9sa9iIsIuTf"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=1ympENCDRHW8RrvITnVo9mZnoz-uA9BHJ"}
        ]
    },
    7: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=1pV3Zu2hOFWKz_eNvAbY8ax5DUUwfLjA3"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=1A_nS6rr18STa1dUO2DNMjmPoikeWzOa2"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=1rn5Bu-7_dh_c46BdB9hLmdRNff3qQ3-F"}
        ]
    },
    8: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=1zUppKuNfl6zI24le7V-pvf64iatQpS32"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=15yvngtaH2jve2ZNtSN7cQLHYaGlq1Gz4"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=1dqLUg5lY4q4_6pPEv7gegBr5JNf3vhdM"}
        ]
    },
    9: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=1FrsyAb2mDXXLQbhS3OjI0ZOs70URyimf"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=1lQ5rSSI_ygsGqemFBEuSVElyaYSrdX1Y"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=11D9H8LzHIOCCFlhom_kQL82-JOv9-mgr"}
        ]
    },
    10: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=1ONI52E-YSNuFN8mDSOE-ywb5KDCPbOUb"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=12SRaebnH4B4_nSgeEsRiqKcMPkXXlI-X"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=1YBuv3mEVuRdyUco2oLklUzQ9WDiZe31i"}
        ]
    },
    11: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=1QZHVo8GTnsAlmbYWbb52WiW9Hj_ezHn1"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=1JMM_RLVLRWBNAebG3pw6IArVQsi4ZH3r"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=1eNh0wo6XLKapj40AuOMVMJvYA-lvEVLb"}
        ]
    },
    12: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=108kTUOSrAJFxTwAp71eTt7skzHy-3Slz"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=1HMYuzT3nzKOwExrJU9JwB2CZX8gIQ5tp"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=1tX5Kv5yUZvxcltnuqo7dTGCn8BFbvH6n"}
        ]
    },
    13: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=1xgwkhrNKHTyWfSKnqjBBm3EmJ43IBWcW"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=1KlPGZSXTgG4U8OdXZW-WeGtkWlvJEDU1"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=1dKp7moqNz-xLCBcdeNpgNO7o68ByVYNU"}
        ]
    },
    14: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=13aEaauqdbl_FYSQ29n44-0zsISgJ1b3v"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=1bgDLVBCTRqgEZ_x8dSk-ayMVJ_4tLPz1"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=1cQfuT8GjkGNBc2L_1LDY88uaELLSxojy"}
        ]
    },
    15: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=1R6DEpjFQKCMIDwalee8w9Vu2rvkkIeMK"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=1XS2Mr2RqTxE8R5oI-z3xb3_ZJT4BqLow"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=1NZEVZsbO79n83j8P_rTvCzhWHR8J8Edg"}
        ]
    },
    16: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=1E_zmObkaiUP3c9bqafZFqLMO9821nTE1"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=1apKgJppS2reRiGvijbbQm6Mu2kAktT8H"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=1FOTeiivpNwOIEaE5jEqg6OT8M3M054MI"}
        ]
    },
    17: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=1sulXoO8-IL2g22mxleLCZ1IkTFfy_Bcq"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=1G6UQt8YzRc_G9ceQBtRCzHJhEsMcFwDa"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=1WY8q1UXbrRrHFfEIBVvl5qbrhyg2UXje"}
        ]
    },
    18: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=1ULZLBfJwk0CwsB00DRvz8oq5HiR15ShR"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=11RKa6eJiTvQbJY5FhP9I6M-raLhondL6"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=1FEIwG2S0FVCXy7_CQWx0wZgMBbTlhfMX"}
        ]
    },
    19: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=1nR8JFVxnE9ymYFXfgI2R5NSs2U4cqfzL"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=1_us6cgf2LBrgEMR-4e8IMrVvZsuCAINv"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=17ZNP4Dc3Kh6fqPUGWgpLGsOmbvjj2IPT"}
        ]
    },
    20: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=1pF6tU9e8U0isDIGSnocm3qvFrreYYNyH"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=1-o-GuFcUY-rolGsD9A84H9H7gs70VhNY"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=1ACPiPlqA6rcHWYPGWIx3J-LPbwLdBkeR"}
        ]
    },
    21: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=1ACPiPlqA6rcHWYPGWIx3J-LPbwLdBkeR"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=1l-aNc4x0U8AqRWJipHiJoBWshzD3q9zb"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=1HhXbNSlrevZxmI_U6orqiYoskPAOEHfN"}
        ]
    },
    22: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=1T6oa4-mqmVmA0I42ZWul7X1UINQmBz_D"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=1dSVTVUr-QmRNjf4zdrhsnD2o3ibBzGSE"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=1vi-diAYGvOuRtqAwyRky4RC_qGyBJlDU"}
        ]
    },
    23: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=1rxhtlVu2uHaULybIgd6wZ4s2mg7nMYYY"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=10U80dqdTddUzJJJMf-quqzoiSsKN3YhB"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=1HeATgcXHHo3WXNz3eBJbD0b9Yq6dfcRY"}
        ]
    },
    24: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=1_tuJEQ6OPuvJwLcBsysLTMw6an9rCq-P"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=1J9r_b_2s7iJ3qqjZYcXukTJtliXERvq2"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=1ZQpABiPDyEbH-_2gKfVMqwOBOpYzZMZ4"}
        ]
    },
    25: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=1o_8fbMgeL_7tJTOevf43GJbR3jCv_t_L"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=1HokfUObPjBDaywkyzCFrphaZOaEjxVE0"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=1HokfUObPjBDaywkyzCFrphaZOaEjxVE0"}
        ]
    },
    26: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=1XSwS_mWV3l5sarCS3QEZe-zc45dWUk_N"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=1VuImT2BUAa_9ddcECoxXATaoL7eTgoO0"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=1TUmBxzbkg09E2mQOiP_12Rxcif4hlc0h"}
        ]
    },
    27: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=1it5dEjdpeEggWcfWAaVv6EELY9Y4d5db"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=11iJ6VeWXsOzal0HX8ma-dSXOIr44n8XY"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=1z1Wmy1r98ijlRv1VSP37svqjMSeUVo8m"}
        ]
    },
    28: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=1yF_Tscr_k_FVCfDO5c5RQEEGyO44xofl"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=1heHo5ygZ8UcqFWfHL3PlfcvOWN_jzP7j"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=1WQquaF-b3_KOh_1uN7JEOrdpRMhAkQ2S"}
        ]
    },
    29: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=1Nt7sOgRDRG8l4wL0JvGPf_O-F0eDzIbb"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=1A3KqDObKlNrEGNCEmjGInwoEX9ttEHAz"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=16RbDn98Ka8dMlyxZ8DJqDKHk0fZC-HJu"}
        ]
    },
    30: {
        "pages": [
            {"page": 1, "imageUrl": "https://drive.google.com/uc?export=view&id=1-tEkYOYa-B7r2aG7Oj88kFRrLtvAq0Re"},
            {"page": 2, "imageUrl": "https://drive.google.com/uc?export=view&id=1lEgg7NGL9n4SgUDDnETatC03thv-K800"},
            {"page": 3, "imageUrl": "https://drive.google.com/uc?export=view&id=1JCsWitOZZHbEg8eTnk2Ffs4j2xTaKEp5"}
        ]
    }
}


async def restore_original_urls():
    """Kembalikan ke format URL asli yang sudah working"""
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    try:
        print("🔄 Mengembalikan ke format URL asli...\n")
        
        updated_count = 0
        for ebook_id, data in original_urls.items():
            # Get existing ebook to preserve color field
            existing = await db.ebooks.find_one({'id': ebook_id})
            if not existing:
                print(f"⚠️  Ebook ID {ebook_id} not found in DB")
                continue
            
            # Merge imageUrl with existing color
            updated_pages = []
            for new_page in data['pages']:
                # Find matching page in existing data
                existing_page = next((p for p in existing.get('pages', []) if p['page'] == new_page['page']), None)
                updated_page = {
                    'page': new_page['page'],
                    'imageUrl': new_page['imageUrl'],
                    'color': existing_page.get('color', '#F5F5F5') if existing_page else '#F5F5F5'
                }
                updated_pages.append(updated_page)
            
            result = await db.ebooks.update_one(
                {'id': ebook_id},
                {'$set': {'pages': updated_pages}}
            )
            
            if result.modified_count > 0:
                updated_count += 1
                print(f"✅ Ebook ID {ebook_id} restored with colors preserved")
        
        print(f"\n🎉 Restore selesai!")
        print(f"📊 Total ebooks updated: {updated_count}/{len(original_urls)}")
        
        # Verifikasi
        example = await db.ebooks.find_one({'id': 1})
        if example and 'pages' in example:
            print(f"\n📸 Format sekarang:")
            print(f"   URL: {example['pages'][0]['imageUrl']}")
            print(f"   Color: {example['pages'][0].get('color', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(restore_original_urls())
