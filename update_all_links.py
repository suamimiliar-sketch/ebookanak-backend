"""
Update Pelangi Pintar - Download Links & Thumbnail Images
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

# Download links and thumbnail images
EBOOK_DATA = {
    1: {
        "download": "https://drive.google.com/uc?export=download&id=1iGl7vqscYDnfby6xe2zozIiUDeE7DmUa",
        "images": [
            "https://drive.google.com/uc?export=view&id=1MVHReqJ9QPoLhpSC35Wt24laF7WC9j0i",
            "https://drive.google.com/uc?export=view&id=1j8z4lO95hZahk4YhCwCXbRqOea2uach9",
            "https://drive.google.com/uc?export=view&id=1wuWNMfJe99JuYOKgHR0YW3OWwZAETBxq"
        ]
    },
    2: {
        "download": "https://drive.google.com/uc?export=download&id=1Ia3n9s95DalVPiUCQ7lmaeKo3wIyZSFd",
        "images": [
            "https://drive.google.com/uc?export=view&id=1_ahIeVEE_-JnDgUGETl0fGGmePYlyqRZ",
            "https://drive.google.com/uc?export=view&id=1QnlHsdMTOfbq_Ka4II6XFrEaJBtV2mTp",
            "https://drive.google.com/uc?export=view&id=1GYnbb9V8_D5ohLWxi-zV1q998dGWVI0Z"
        ]
    },
    3: {
        "download": "https://drive.google.com/uc?export=download&id=1tK7zovj_02BedXORuTFqiLFFSV6AGzjH",
        "images": [
            "https://drive.google.com/uc?export=view&id=11wBu20wWGx42pV3wEt-gms6WJg8XjRJK",
            "https://drive.google.com/uc?export=view&id=1eNhlYpsgZYanlp6zdXjB8YYdTD3PrSE4",
            "https://drive.google.com/uc?export=view&id=1B4g2tq9T4i9zjmHxvBrnqVcIcpPc-3Fs"
        ]
    },
    4: {
        "download": "https://drive.google.com/uc?export=download&id=18_bkh3kni5VIY_-S0Br_a7pc3Enx8qMZ",
        "images": [
            "https://drive.google.com/uc?export=view&id=1pnndnS3F7fm9aj2-5NBOe_lmMEXogIef",
            "https://drive.google.com/uc?export=view&id=1s453I_LySbVLP8eNm15DoWx2zNlL5Sn7",
            "https://drive.google.com/uc?export=view&id=18Rd20AX84K-kjJBdvUJmB4zPGJCwvgOo"
        ]
    },
    5: {
        "download": "https://drive.google.com/uc?export=download&id=1Nmd_aVkd9D7b-vkubfyQSForP2vANrZ1",
        "images": [
            "https://drive.google.com/uc?export=view&id=11ltuN3_fIIL1eg1pRVpBJCukNjdI21dH",
            "https://drive.google.com/uc?export=view&id=1mktn2vt3og8SMjJYa19X0_AkMyKbfqu5",
            "https://drive.google.com/uc?export=view&id=1PuJdeuuQiZ4VzfGV3ip5-UCp2HTAGn9b"
        ]
    },
    6: {
        "download": "https://drive.google.com/uc?export=download&id=1v4gZ0gRQiDMxy0OujuIjjly_k2k2i7Al",
        "images": [
            "https://drive.google.com/uc?export=view&id=19g-kSODAYygZeEVWnIQTZIfAUcnPnq7r",
            "https://drive.google.com/uc?export=view&id=1LufsKGjeFUgz8xujDD0g-9sa9iIsIuTf",
            "https://drive.google.com/uc?export=view&id=1ympENCDRHW8RrvITnVo9mZnoz-uA9BHJ"
        ]
    },
    7: {
        "download": "https://drive.google.com/uc?export=download&id=1x4_7rUoaTZ0dd8I7RRKTfDEh7bxeWL0-",
        "images": [
            "https://drive.google.com/uc?export=view&id=1pV3Zu2hOFWKz_eNvAbY8ax5DUUwfLjA3",
            "https://drive.google.com/uc?export=view&id=1A_nS6rr18STa1dUO2DNMjmPoikeWzOa2",
            "https://drive.google.com/uc?export=view&id=1rn5Bu-7_dh_c46BdB9hLmdRNff3qQ3-F"
        ]
    },
    8: {
        "download": "https://drive.google.com/uc?export=download&id=1EaurW2uzF9M7nz1hNwlERXz499KgU3qE",
        "images": [
            "https://drive.google.com/uc?export=view&id=1zUppKuNfl6zI24le7V-pvf64iatQpS32",
            "https://drive.google.com/uc?export=view&id=15yvngtaH2jve2ZNtSN7cQLHYaGlq1Gz4",
            "https://drive.google.com/uc?export=view&id=1dqLUg5lY4q4_6pPEv7gegBr5JNf3vhdM"
        ]
    },
    9: {
        "download": "https://drive.google.com/uc?export=download&id=1Uvu_9Y8hYlNZ3iYywgKPt9OkSi08iht6",
        "images": [
            "https://drive.google.com/uc?export=view&id=1FrsyAb2mDXXLQbhS3OjI0ZOs70URyimf",
            "https://drive.google.com/uc?export=view&id=1lQ5rSSI_ygsGqemFBEuSVElyaYSrdX1Y",
            "https://drive.google.com/uc?export=view&id=11D9H8LzHIOCCFlhom_kQL82-JOv9-mgr"
        ]
    },
    10: {
        "download": "https://drive.google.com/uc?export=download&id=1WHK0dwY1e4PvKPwyp59edmQ2PGnpb5Ll",
        "images": [
            "https://drive.google.com/uc?export=view&id=1ONI52E-YSNuFN8mDSOE-ywb5KDCPbOUb",
            "https://drive.google.com/uc?export=view&id=12SRaebnH4B4_nSgeEsRiqKcMPkXXlI-X",
            "https://drive.google.com/uc?export=view&id=1YBuv3mEVuRdyUco2oLklUzQ9WDiZe31i"
        ]
    },
    11: {
        "download": "https://drive.google.com/uc?export=download&id=1cqCdCoPx1JD6CBYnN2yvxVLxCditxll3",
        "images": [
            "https://drive.google.com/uc?export=view&id=1QZHVo8GTnsAlmbYWbb52WiW9Hj_ezHn1",
            "https://drive.google.com/uc?export=view&id=1JMM_RLVLRWBNAebG3pw6IArVQsi4ZH3r",
            "https://drive.google.com/uc?export=view&id=1eNh0wo6XLKapj40AuOMVMJvYA-lvEVLb"
        ]
    },
    12: {
        "download": "https://drive.google.com/uc?export=download&id=12n7vTJX0JEVwr10lAc1WcRBNNsvSEz43",
        "images": [
            "https://drive.google.com/uc?export=view&id=108kTUOSrAJFxTwAp71eTt7skzHy-3Slz",
            "https://drive.google.com/uc?export=view&id=1HMYuzT3nzKOwExrJU9JwB2CZX8gIQ5tp",
            "https://drive.google.com/uc?export=view&id=1tX5Kv5yUZvxcltnuqo7dTGCn8BFbvH6n"
        ]
    },
    13: {
        "download": "https://drive.google.com/uc?export=download&id=1pWnwE8ON-XibXZ383U3HJr0--KzY7CCe",
        "images": [
            "https://drive.google.com/uc?export=view&id=1xgwkhrNKHTyWfSKnqjBBm3EmJ43IBWcW",
            "https://drive.google.com/uc?export=view&id=1KlPGZSXTgG4U8OdXZW-WeGtkWlvJEDU1",
            "https://drive.google.com/uc?export=view&id=1dKp7moqNz-xLCBcdeNpgNO7o68ByVYNU"
        ]
    },
    14: {
        "download": "https://drive.google.com/uc?export=download&id=1eJlnu7U9BO72prBdjWPNMX8C7hfpDWHE",
        "images": [
            "https://drive.google.com/uc?export=view&id=13aEaauqdbl_FYSQ29n44-0zsISgJ1b3v",
            "https://drive.google.com/uc?export=view&id=1bgDLVBCTRqgEZ_x8dSk-ayMVJ_4tLPz1",
            "https://drive.google.com/uc?export=view&id=1cQfuT8GjkGNBc2L_1LDY88uaELLSxojy"
        ]
    },
    15: {
        "download": "https://drive.google.com/uc?export=download&id=1Y9NRssfnEm5GjQ7gtvkJU61GHL7HHsa6",
        "images": [
            "https://drive.google.com/uc?export=view&id=1R6DEpjFQKCMIDwalee8w9Vu2rvkkIeMK",
            "https://drive.google.com/uc?export=view&id=1XS2Mr2RqTxE8R5oI-z3xb3_ZJT4BqLow",
            "https://drive.google.com/uc?export=view&id=1NZEVZsbO79n83j8P_rTvCzhWHR8J8Edg"
        ]
    },
    16: {
        "download": "https://drive.google.com/uc?export=download&id=1jTkxSvdiD0GYKEMGABNgn86TpItXyE1Y",
        "images": [
            "https://drive.google.com/uc?export=view&id=1E_zmObkaiUP3c9bqafZFqLMO9821nTE1",
            "https://drive.google.com/uc?export=view&id=1apKgJppS2reRiGvijbbQm6Mu2kAktT8H",
            "https://drive.google.com/uc?export=view&id=1FOTeiivpNwOIEaE5jEqg6OT8M3M054MI"
        ]
    },
    17: {
        "download": "https://drive.google.com/uc?export=download&id=1F2O1vh2EHO3zbfujxrAF0Wsb5uRDqZ_t",
        "images": [
            "https://drive.google.com/uc?export=view&id=1sulXoO8-IL2g22mxleLCZ1IkTFfy_Bcq",
            "https://drive.google.com/uc?export=view&id=1G6UQt8YzRc_G9ceQBtRCzHJhEsMcFwDa",
            "https://drive.google.com/uc?export=view&id=1WY8q1UXbrRrHFfEIBVvl5qbrhyg2UXje"
        ]
    },
    18: {
        "download": "https://drive.google.com/uc?export=download&id=1D8DDdEqlTlI33Epwbg9qLx_yTaZLHFN9",
        "images": [
            "https://drive.google.com/uc?export=view&id=1ULZLBfJwk0CwsB00DRvz8oq5HiR15ShR",
            "https://drive.google.com/uc?export=view&id=11RKa6eJiTvQbJY5FhP9I6M-raLhondL6",
            "https://drive.google.com/uc?export=view&id=1FEIwG2S0FVCXy7_CQWx0wZgMBbTlhfMX"
        ]
    },
    19: {
        "download": "https://drive.google.com/uc?export=download&id=1dMOhPZ4h0Mct5RSLlcUNNC3aFa563Lz4",
        "images": [
            "https://drive.google.com/uc?export=view&id=1nR8JFVxnE9ymYFXfgI2R5NSs2U4cqfzL",
            "https://drive.google.com/uc?export=view&id=1_us6cgf2LBrgEMR-4e8IMrVvZsuCAINv",
            "https://drive.google.com/uc?export=view&id=17ZNP4Dc3Kh6fqPUGWgpLGsOmbvjj2IPT"
        ]
    },
    20: {
        "download": "https://drive.google.com/uc?export=download&id=1qXtm7mpI-jr6hvZUncJgqY-tUfXDgqw2",
        "images": [
            "https://drive.google.com/uc?export=view&id=1pF6tU9e8U0isDIGSnocm3qvFrreYYNyH",
            "https://drive.google.com/uc?export=view&id=1-o-GuFcUY-rolGsD9A84H9H7gs70VhNY",
            "https://drive.google.com/uc?export=view&id=1ACPiPlqA6rcHWYPGWIx3J-LPbwLdBkeR"
        ]
    },
    21: {
        "download": "https://drive.google.com/uc?export=download&id=1IEC-MLoS9luEi00ZXQiuUZnCxKzmI0sb",
        "images": [
            "https://drive.google.com/uc?export=view&id=1ACPiPlqA6rcHWYPGWIx3J-LPbwLdBkeR",
            "https://drive.google.com/uc?export=view&id=1l-aNc4x0U8AqRWJipHiJoBWshzD3q9zb",
            "https://drive.google.com/uc?export=view&id=1HhXbNSlrevZxmI_U6orqiYoskPAOEHfN"
        ]
    },
    22: {
        "download": "https://drive.google.com/uc?export=download&id=1mtKg0AsAfJX800O3J97__S4Bdt0kW8wT",
        "images": [
            "https://drive.google.com/uc?export=view&id=1T6oa4-mqmVmA0I42ZWul7X1UINQmBz_D",
            "https://drive.google.com/uc?export=view&id=1dSVTVUr-QmRNjf4zdrhsnD2o3ibBzGSE",
            "https://drive.google.com/uc?export=view&id=1vi-diAYGvOuRtqAwyRky4RC_qGyBJlDU"
        ]
    },
}


async def update_all_links():
    """Update download links and thumbnail images"""
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    try:
        print("🔗 Updating download links and thumbnail images...")
        print("=" * 60)
        
        updated_count = 0
        
        for ebook_id, data in EBOOK_DATA.items():
            # Create pages array with images
            pages = [
                {"page": 1, "color": "", "imageUrl": data["images"][0]},
                {"page": 2, "color": "", "imageUrl": data["images"][1]},
                {"page": 3, "color": "", "imageUrl": data["images"][2]}
            ]
            
            result = await db.ebooks.update_one(
                {"id": ebook_id},
                {
                    "$set": {
                        "driveDownloadLink": data["download"],
                        "pages": pages,
                        "hasRealImages": True
                    }
                }
            )
            
            if result.modified_count > 0:
                updated_count += 1
                print(f"✅ Updated ebook ID {ebook_id}")
        
        print()
        print("=" * 60)
        print(f"🎉 Successfully updated {updated_count} ebooks!")
        print("=" * 60)
        print()
        print("📊 Summary:")
        print(f"  - Download links: {updated_count}")
        print(f"  - Thumbnail images: {updated_count * 3}")
        print()
        print("🚀 Next steps:")
        print("  1. Restart backend: sudo supervisorctl restart backend")
        print("  2. Restart frontend: sudo supervisorctl restart frontend")
        print("  3. Visit your website to see real PDF previews!")
        print()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(update_all_links())
