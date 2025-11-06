"""
Complete update script to add all 30 ebooks with download and thumbnail links
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

# All ebooks with download and thumbnail links
ebooks_updates = [
    # Tracing Books - Usia 3-4 (IDs 1-13)
    {
        "id": 1,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=1iGl7vqscYDnfby6xe2zozIiUDeE7DmUa",
        "pages": [
            {"page": 1, "color": "#FFE4E1", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753244/1_page1_soiffs.jpg"},
            {"page": 2, "color": "#FFD6D9", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753244/1_page2_soxveh.jpg"},
            {"page": 3, "color": "#FFC9CE", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753245/1_page3_ln78ii.jpg"}
        ]
    },
    {
        "id": 2,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=1Ia3n9s95DalVPiUCQ7lmaeKo3wIyZSFd",
        "pages": [
            {"page": 1, "color": "#E6F3FF", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753245/2_page1_oyfvqf.jpg"},
            {"page": 2, "color": "#D6EBFF", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753245/2_page2_fqppxz.jpg"},
            {"page": 3, "color": "#C6E3FF", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753245/2_page3_hbdqf5.jpg"}
        ]
    },
    {
        "id": 3,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=1tK7zovj_02BedXORuTFqiLFFSV6AGzjH",
        "pages": [
            {"page": 1, "color": "#FFF9E6", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753245/3_page1_m45z1a.jpg"},
            {"page": 2, "color": "#FFF4D6", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753246/3_page2_r7fkxe.jpg"},
            {"page": 3, "color": "#FFEFC6", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753246/3_page3_abxq0m.jpg"}
        ]
    },
    {
        "id": 4,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=18_bkh3kni5VIY_-S0Br_a7pc3Enx8qMZ",
        "pages": [
            {"page": 1, "color": "#E8F5E9", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753246/4_page1_vhsrdf.jpg"},
            {"page": 2, "color": "#D8EDD9", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753246/4_page2_xxod9y.jpg"},
            {"page": 3, "color": "#C8E5C9", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753246/4_page3_c31lff.jpg"}
        ]
    },
    {
        "id": 5,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=1Nmd_aVkd9D7b-vkubfyQSForP2vANrZ1",
        "pages": [
            {"page": 1, "color": "#F3E5F5", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753247/5_page1_dmocyv.jpg"},
            {"page": 2, "color": "#E9D8F0", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753247/5_page2_gqjux8.jpg"},
            {"page": 3, "color": "#DFCBEB", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753247/5_page3_lkmpxw.jpg"}
        ]
    },
    {
        "id": 6,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=1v4gZ0gRQiDMxy0OujuIjjly_k2k2i7Al",
        "pages": [
            {"page": 1, "color": "#FFF3E0", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753248/6_page1_zzmcin.jpg"},
            {"page": 2, "color": "#FFEAD0", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753248/6_page2_bbsspx.jpg"},
            {"page": 3, "color": "#FFE1C0", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753249/6_page3_pysijs.jpg"}
        ]
    },
    {
        "id": 7,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=1x4_7rUoaTZ0dd8I7RRKTfDEh7bxeWL0-",
        "pages": [
            {"page": 1, "color": "#E1F5FE", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753249/7_page1_z2zks5.jpg"},
            {"page": 2, "color": "#D1EDFE", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753244/7_page2_lbb7gb.jpg"},
            {"page": 3, "color": "#C1E5FE", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753245/7_page3_ur37wu.jpg"}
        ]
    },
    {
        "id": 8,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=1EaurW2uzF9M7nz1hNwlERXz499KgU3qE",
        "pages": [
            {"page": 1, "color": "#FCE4EC", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753245/8_page1_jnopza.jpg"},
            {"page": 2, "color": "#FAD4E0", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753245/8_page2_hzfgbp.jpg"},
            {"page": 3, "color": "#F8C4D4", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753246/8_page3_ydah1b.jpg"}
        ]
    },
    {
        "id": 9,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=1Uvu_9Y8hYlNZ3iYywgKPt9OkSi08iht6",
        "pages": [
            {"page": 1, "color": "#FFF9C4", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753246/9_page1_swqihq.jpg"},
            {"page": 2, "color": "#FFF5B4", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753246/9_page2_gyl26t.jpg"},
            {"page": 3, "color": "#FFF1A4", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753246/9_page3_njew0e.jpg"}
        ]
    },
    {
        "id": 10,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=1WHK0dwY1e4PvKPwyp59edmQ2PGnpb5Ll",
        "pages": [
            {"page": 1, "color": "#F1F8E9", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753247/10_page1_yni4cy.jpg"},
            {"page": 2, "color": "#E8F3DC", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753247/10_page2_ufhzul.jpg"},
            {"page": 3, "color": "#DFEECD", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753247/10_page3_aj8dfa.jpg"}
        ]
    },
    {
        "id": 11,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=1cqCdCoPx1JD6CBYnN2yvxVLxCditxll3",
        "pages": [
            {"page": 1, "color": "#E8EAF6", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753248/11_page1_i8pa3t.jpg"},
            {"page": 2, "color": "#DCDFF3", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753248/11_page2_vkzzfn.jpg"},
            {"page": 3, "color": "#D0D4F0", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753248/11_page3_ysk8wn.jpg"}
        ]
    },
    {
        "id": 12,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=12n7vTJX0JEVwr10lAc1WcRBNNsvSEz43",
        "pages": [
            {"page": 1, "color": "#E0F2F1", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753248/12_page1_v7eyv0.jpg"},
            {"page": 2, "color": "#D0EBE9", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753248/12_page2_ti8yko.jpg"},
            {"page": 3, "color": "#C0E4E1", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753248/12_page3_jigasx.jpg"}
        ]
    },
    {
        "id": 13,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=1pWnwE8ON-XibXZ383U3HJr0--KzY7CCe",
        "pages": [
            {"page": 1, "color": "#FFF8E1", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753249/13_page1_jvllmu.jpg"},
            {"page": 2, "color": "#FFF3D1", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753249/13_page2_bcqe4f.jpg"},
            {"page": 3, "color": "#FFEEC1", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753249/13_page3_wa2uam.jpg"}
        ]
    },
    # Flash Card Dasar - Usia 3-4 (IDs 14-18)
    {
        "id": 14,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=1eJlnu7U9BO72prBdjWPNMX8C7hfpDWHE",
        "pages": [
            {"page": 1, "color": "#E3F2FD", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753249/14_page1_x1q8ns.jpg"},
            {"page": 2, "color": "#D3EBFD", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753249/14_page2_szzhrh.jpg"},
            {"page": 3, "color": "#C3E4FD", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753250/14_page3_bceftm.jpg"}
        ]
    },
    {
        "id": 15,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=1Y9NRssfnEm5GjQ7gtvkJU61GHL7HHsa6",
        "pages": [
            {"page": 1, "color": "#F3E5F5", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753250/15_page1_wxg7ec.jpg"},
            {"page": 2, "color": "#E9D8F0", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753250/15_page2_wqzg8i.jpg"},
            {"page": 3, "color": "#DFCBEB", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753250/15_page3_mmxgkf.jpg"}
        ]
    },
    {
        "id": 16,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=1jTkxSvdiD0GYKEMGABNgn86TpItXyE1Y",
        "pages": [
            {"page": 1, "color": "#E1F5FE", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753250/16_page1_mm17pc.jpg"},
            {"page": 2, "color": "#D1EDFE", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753250/16_page2_qijazi.jpg"},
            {"page": 3, "color": "#C1E5FE", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753250/16_page3_gc3nhf.jpg"}
        ]
    },
    {
        "id": 17,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=1F2O1vh2EHO3zbfujxrAF0Wsb5uRDqZ_t",
        "pages": [
            {"page": 1, "color": "#FCE4EC", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753250/17_page1_spqqd2.jpg"},
            {"page": 2, "color": "#FAD4E0", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753252/17_page2_crq7qn.jpg"},
            {"page": 3, "color": "#F8C4D4", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753285/17_page3_g6cjh7.jpg"}
        ]
    },
    {
        "id": 18,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=1D8DDdEqlTlI33Epwbg9qLx_yTaZLHFN9",
        "pages": [
            {"page": 1, "color": "#FFF9C4", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753285/18_page1_usedsb.jpg"},
            {"page": 2, "color": "#FFF5B4", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753285/18_page2_zr2hgq.jpg"},
            {"page": 3, "color": "#FFF1A4", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753285/18_page3_s1vgdo.jpg"}
        ]
    },
    # Flashcards Tema - Usia 5-6 (IDs 19-21)
    {
        "id": 19,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=1dMOhPZ4h0Mct5RSLlcUNNC3aFa563Lz4",
        "pages": [
            {"page": 1, "color": "#F1F8E9", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753285/19_page1_hd4deu.jpg"},
            {"page": 2, "color": "#E8F3DC", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753286/19_page2_fpt29d.jpg"},
            {"page": 3, "color": "#DFEECD", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753286/19_page3_bxxhsi.jpg"}
        ]
    },
    {
        "id": 20,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=1qXtm7mpI-jr6hvZUncJgqY-tUfXDgqw2",
        "pages": [
            {"page": 1, "color": "#E8EAF6", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753286/20_page1_v1ul4y.jpg"},
            {"page": 2, "color": "#DCDFF3", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753287/20_page2_dti99m.jpg"},
            {"page": 3, "color": "#D0D4F0", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753299/20_page3_lkyxxn.jpg"}
        ]
    },
    {
        "id": 21,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=1IEC-MLoS9luEi00ZXQiuUZnCxKzmI0sb",
        "pages": [
            {"page": 1, "color": "#E0F2F1", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753299/21_page1_zljgn2.jpg"},
            {"page": 2, "color": "#D0EBE9", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753299/21_page2_xjhqly.jpg"},
            {"page": 3, "color": "#C0E4E1", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753299/21_page3_ypbaga.jpg"}
        ]
    },
    # Workbook - Usia 5-6 (ID 22)
    {
        "id": 22,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=1mtKg0AsAfJX800O3J97__S4Bdt0kW8wT",
        "pages": [
            {"page": 1, "color": "#FFF3E0", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753299/22_page1_nvrxcz.jpg"},
            {"page": 2, "color": "#FFEAD0", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753299/22_page2_invhtg.jpg"},
            {"page": 3, "color": "#FFE1C0", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753299/22_page3_xrxiy8.jpg"}
        ]
    },
    # Emotional Learning - Usia 7-9 (IDs 23-24)
    {
        "id": 23,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=1bI1JykmqckIjE_YDwAqN4AWlnRkMo-tJ",
        "pages": [
            {"page": 1, "color": "#FFE4E1", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753299/23_page1_msukfh.jpg"},
            {"page": 2, "color": "#FFD6D9", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753299/23_page2_emzmhu.jpg"},
            {"page": 3, "color": "#FFC9CE", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753300/23_page3_qzvxze.jpg"}
        ]
    },
    {
        "id": 24,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=157tzCiugu0RTn2f-_2Q8OpHi2TsR6o1j",
        "pages": [
            {"page": 1, "color": "#FCE4EC", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753300/24_page1_qttrks.jpg"},
            {"page": 2, "color": "#FAD4E0", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753300/24_page2_p3kzwt.jpg"},
            {"page": 3, "color": "#F8C4D4", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753300/24_page3_wsmdqm.jpg"}
        ]
    },
    # Science Flashcards - Usia 7-9 (IDs 25-28)
    {
        "id": 25,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=16xp5fMcq6TlppWb3hGjiHYWZa8tTc2YN",
        "pages": [
            {"page": 1, "color": "#E8F5E9", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753300/25_page1_gvvkll.jpg"},
            {"page": 2, "color": "#D8EDD9", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753300/25_page2_jsoeqb.jpg"},
            {"page": 3, "color": "#C8E5C9", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753300/25_page2_jsoeqb.jpg"}
        ]
    },
    {
        "id": 26,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=1ta0FACS2lIUpyKc5QcmO-zxYgmbuRQsQ",
        "pages": [
            {"page": 1, "color": "#F1F8E9", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753321/26_page1_ev1m6a.jpg"},
            {"page": 2, "color": "#E8F3DC", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753321/26_page2_l9z965.jpg"},
            {"page": 3, "color": "#DFEECD", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753321/26_page3_i7ojm9.jpg"}
        ]
    },
    {
        "id": 27,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=1KwwNrOmuPFFCgBZfn6Pl4np8Rh2y9J5L",
        "pages": [
            {"page": 1, "color": "#E8EAF6", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753321/27_page1_q1qkpw.jpg"},
            {"page": 2, "color": "#DCDFF3", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753321/27_page2_jjq0gg.jpg"},
            {"page": 3, "color": "#D0D4F0", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753321/27_page3_atc9op.jpg"}
        ]
    },
    {
        "id": 28,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=1hSZyf5dIayJ9-5yzppKMvWFbQwvciSTM",
        "pages": [
            {"page": 1, "color": "#FFF3E0", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753321/28_page1_nehmkv.jpg"},
            {"page": 2, "color": "#FFEAD0", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753322/28_page2_fj6fvf.jpg"},
            {"page": 3, "color": "#FFE1C0", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753321/28_page3_f9efag.jpg"}
        ]
    },
    # Bonus Pack (IDs 29-30)
    {
        "id": 29,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=1Btcj4erfb-ighSRmcVh_10Y6jZfRUsJP",
        "pages": [
            {"page": 1, "color": "#FFD700", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753321/29_page1_trhsqr.jpg"},
            {"page": 2, "color": "#FFC700", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753322/29_page2_c1jzzd.jpg"},
            {"page": 3, "color": "#FFB700", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753322/29_page3_nm3tsl.jpg"}
        ]
    },
    {
        "id": 30,
        "driveDownloadLink": "https://drive.google.com/uc?export=download&id=1LAcoxx57yUVBkXyV4S5XkpS8_VN_7pRe",
        "pages": [
            {"page": 1, "color": "#FFD700", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753323/30_page1_cpzij4.jpg"},
            {"page": 2, "color": "#FFC700", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753323/30_page1_cpzij4.jpg"},
            {"page": 3, "color": "#FFB700", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753338/30_page3_cuman2.jpg"}
        ]
    }
]


async def update_database():
    """Update all ebooks with download and thumbnail links"""
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    try:
        updated_count = 0
        for ebook_update in ebooks_updates:
            ebook_id = ebook_update["id"]
            result = await db.ebooks.update_one(
                {"id": ebook_id},
                {"$set": {
                    "driveDownloadLink": ebook_update["driveDownloadLink"],
                    "pages": ebook_update["pages"]
                }}
            )
            if result.modified_count > 0:
                updated_count += 1
                print(f"✅ Updated ebook ID {ebook_id}")
            else:
                print(f"⚠️  Ebook ID {ebook_id} not found or already up to date")
        
        print(f"\n🎉 Update completed!")
        print(f"📚 Total ebooks updated: {updated_count}/{len(ebooks_updates)}")
        
    except Exception as e:
        print(f"❌ Error updating database: {str(e)}")
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(update_database())
