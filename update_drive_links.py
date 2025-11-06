"""
Update Google Drive download links for ebooks
Run this script after you've uploaded your PDFs to Google Drive
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


# INSTRUCTIONS TO GET GOOGLE DRIVE LINKS:
# 1. Upload your PDF to Google Drive
# 2. Right-click the file → Share → Change to "Anyone with the link"
# 3. Copy the link (looks like: https://drive.google.com/file/d/FILE_ID/view?usp=sharing)
# 4. Extract the FILE_ID from the link
# 5. Use format: https://drive.google.com/uc?export=download&id=FILE_ID

# Update these links with your actual Google Drive file IDs
EBOOK_LINKS = {
    # Tracing Books - Usia 3-4
        1: "https://drive.google.com/uc?export=download&id=1iGl7vqscYDnfby6xe2zozIiUDeE7DmUa",
            2: "https://drive.google.com/uc?export=download&id=1Ia3n9s95DalVPiUCQ7lmaeKo3wIyZSFd",
                3: "https://drive.google.com/uc?export=download&id=1tK7zovj_02BedXORuTFqiLFFSV6AGzjH",
                    4: "https://drive.google.com/uc?export=download&id=18_bkh3kni5VIY_-S0Br_a7pc3Enx8qMZ",
                        5: "https://drive.google.com/uc?export=download&id=1Nmd_aVkd9D7b-vkubfyQSForP2vANrZ1",
                            6: "https://drive.google.com/uc?export=download&id=1v4gZ0gRQiDMxy0OujuIjjly_k2k2i7Al",
                                7: "https://drive.google.com/uc?export=download&id=1x4_7rUoaTZ0dd8I7RRKTfDEh7bxeWL0-",
                                    8: "https://drive.google.com/uc?export=download&id=1EaurW2uzF9M7nz1hNwlERXz499KgU3qE",
                                        9: "https://drive.google.com/uc?export=download&id=1Uvu_9Y8hYlNZ3iYywgKPt9OkSi08iht6g",
                                            10: "https://drive.google.com/uc?export=download&id=1WHK0dwY1e4PvKPwyp59edmQ2PGnpb5Ll",
                                                11: "https://drive.google.com/uc?export=download&id=1cqCdCoPx1JD6CBYnN2yvxVLxCditxll3",
                                                    12: "https://drive.google.com/uc?export=download&id=12n7vTJX0JEVwr10lAc1WcRBNNsvSEz43g",
                                                        13: "https://drive.google.com/uc?export=download&id=1pWnwE8ON-XibXZ383U3HJr0--KzY7CCe",

                                                            # Flash Card Dasar - Usia 3-4
                                                                14: "https://drive.google.com/uc?export=download&id=1eJlnu7U9BO72prBdjWPNMX8C7hfpDWHE",
                                                                    15: "https://drive.google.com/uc?export=download&id=1Y9NRssfnEm5GjQ7gtvkJU61GHL7HHsa6",
                                                                        16: "https://drive.google.com/uc?export=download&id=1jTkxSvdiD0GYKEMGABNgn86TpItXyE1Y",
                                                                            17: "https://drive.google.com/uc?export=download&id=1F2O1vh2EHO3zbfujxrAF0Wsb5uRDqZ_t",
                                                                                18: "https://drive.google.com/uc?export=download&id=1D8DDdEqlTlI33Epwbg9qLx_yTaZLHFN9",
                                                                                    
                                                                                        # Flashcards Tema - Usia 5-6
                                                                                            19: "https://drive.google.com/uc?export=download&id=1dMOhPZ4h0Mct5RSLlcUNNC3aFa563Lz4",
                                                                                                20: "https://drive.google.com/uc?export=download&id=1qXtm7mpI-jr6hvZUncJgqY-tUfXDgqw2",
                                                                                                    21: "https://drive.google.com/uc?export=download&id=1IEC-MLoS9luEi00ZXQiuUZnCxKzmI0sb",
                                                                                                        
                                                                                                            # Workbook - Usia 5-6
                                                                                                                22: "https://drive.google.com/uc?export=download&id=1mtKg0AsAfJX800O3J97__S4Bdt0kW8wT",
                                                                                                                    
                                                                                                                        # Emotional Learning - Usia 7-9
                                                                                                                            23: "https://drive.google.com/uc?export=download&id=1bI1JykmqckIjE_YDwAqN4AWlnRkMo-tJ",
                                                                                                                                24: "https://drive.google.com/uc?export=download&id=157tzCiugu0RTn2f-_2Q8OpHi2TsR6o1j",
                                                                                                                                    
                                                                                                                                        # Science Flashcards - Usia 7-9
                                                                                                                                            25: "https://drive.google.com/uc?export=download&id=16xp5fMcq6TlppWb3hGjiHYWZa8tTc2YN",
                                                                                                                                                26: "https://drive.google.com/uc?export=download&id=1ta0FACS2lIUpyKc5QcmO-zxYgmbuRQsQ",
                                                                                                                                                    27: "https://drive.google.com/uc?export=download&id=1KwwNrOmuPFFCgBZfn6Pl4np8Rh2y9J5L",
                                                                                                                                                        28: "https://drive.google.com/uc?export=download&id=1hSZyf5dIayJ9-5yzppKMvWFbQwvciSTM",
    
    # Bonus Pack
    29: "https://drive.google.com/uc?export=download&id=1Btcj4erfb-ighSRmcVh_10Y6jZfRUsJP",
    30: "https://drive.google.com/uc?export=download&id=1LAcoxx57yUVBkXyV4S5XkpS8_VN_7pRe",
}


async def update_drive_links():
    """Update Google Drive download links in database"""
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    try:
        updated_count = 0
        
        for ebook_id, drive_link in EBOOK_LINKS.items():
            result = await db.ebooks.update_one(
                {"id": ebook_id},
                {"$set": {"driveDownloadLink": drive_link}}
            )
            
            if result.modified_count > 0:
                updated_count += 1
                print(f"✅ Updated ebook ID {ebook_id}")
        
        print(f"\n🎉 Updated {updated_count} ebook download links!")
        
        # Verify updates
        ebooks_with_links = await db.ebooks.count_documents({"driveDownloadLink": {"$exists": True, "$ne": None}})
        print(f"📚 Total ebooks with download links: {ebooks_with_links}")
        
    except Exception as e:
        print(f"❌ Error updating links: {str(e)}")
    finally:
        client.close()


if __name__ == "__main__":
    print("🔗 Updating Google Drive download links...\n")
    print("⚠️  Make sure you've updated the EBOOK_LINKS dictionary with your actual Google Drive file IDs!\n")
    asyncio.run(update_drive_links())
