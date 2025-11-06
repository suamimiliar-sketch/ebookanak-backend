from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import subprocess
import sys

load_dotenv()

router = APIRouter()

@router.post("/admin/fix-thumbnails-direct")
async def fix_thumbnails_directly():
    """
    Fix ebook thumbnails by directly updating database (no external script)
    FORCE UPDATE with hardcoded Cloudinary URLs
    """
    try:
        mongo_url = os.environ.get('MONGO_URL')
        db_name = os.environ.get('DB_NAME', 'pelangi_pintar')
        
        client = AsyncIOMotorClient(mongo_url)
        db = client[db_name]
        
        # Hardcoded ebook updates with Cloudinary URLs (first 5 for testing)
        updates = [
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
            }
        ]
        
        updated_count = 0
        details = []
        
        for update in updates:
            ebook_id = update["id"]
            pages = update["pages"]
            
            # FORCE update with upsert
            result = await db.ebooks.update_one(
                {"id": ebook_id},
                {"$set": {"pages": pages}},
                upsert=False
            )
            
            if result.matched_count > 0:
                updated_count += 1
                details.append(f"ID {ebook_id}: matched={result.matched_count}, modified={result.modified_count}")
        
        # Verify AFTER update
        sample_after = await db.ebooks.find_one({"id": 1})
        has_image_after = bool(sample_after and sample_after.get("pages") and len(sample_after["pages"]) > 0 and sample_after["pages"][0].get("imageUrl"))
        
        client.close()
        
        return {
            "success": True,
            "message": "Thumbnails updated with hardcoded URLs",
            "database": db_name,
            "mongo_url": mongo_url[:30] + "...",
            "updated_count": updated_count,
            "details": details,
            "verification": {
                "sample_id": 1,
                "has_image": has_image_after,
                "imageUrl": sample_after["pages"][0].get("imageUrl") if sample_after and sample_after.get("pages") else None,
                "pages_count": len(sample_after.get("pages", [])) if sample_after else 0
            }
        }
    
    except Exception as e:
        import traceback
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }

@router.post("/admin/fix-thumbnails")
async def fix_production_thumbnails():
    """
    Fix production ebook thumbnails by running force update script
    """
    try:
        # Run the force_update_thumbnails.py script which forcefully updates all pages
        result = subprocess.run(
            [sys.executable, '/app/backend/force_update_thumbnails.py'],
            capture_output=True,
            text=True,
            cwd='/app/backend'
        )
        
        # Check if script ran successfully
        if result.returncode != 0:
            return {
                "success": False,
                "message": "Script execution failed",
                "error": result.stderr,
                "output": result.stdout
            }
        
        # Verify the update
        mongo_url = os.environ.get('MONGO_URL')
        db_name = os.environ.get('DB_NAME', 'pelangi_pintar')
        
        client = AsyncIOMotorClient(mongo_url)
        db = client[db_name]
        
        # Check how many ebooks have images now
        sample = await db.ebooks.find_one({"id": 1})
        has_image = bool(sample and sample.get("pages") and len(sample["pages"]) > 0 and sample["pages"][0].get("imageUrl"))
        
        client.close()
        
        return {
            "success": True,
            "message": "Thumbnails fixed successfully",
            "database": db_name,
            "sample_has_image": has_image,
            "sample_imageUrl": sample["pages"][0].get("imageUrl") if sample and sample.get("pages") else None,
            "script_output": result.stdout[-500:]  # Last 500 chars
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fix thumbnails failed: {str(e)}")


@router.post("/admin/update-minigames-thumbnails")
async def update_minigames_thumbnails():
    """
    Update mini-games with new thumbnails and game URLs
    """
    try:
        mongo_url = os.environ.get('MONGO_URL')
        db_name = os.environ.get('DB_NAME', 'pelangi_pintar')
        
        client = AsyncIOMotorClient(mongo_url)
        db = client[db_name]
        
        # New mini-games data with updated thumbnails
        minigames_updates = [
            {
                "id": 1,
                "title": "Animal Memory Match",
                "thumbnailUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1762320060/Instagram_Post_-_Play_Animal_Memory_Match_Today_eqw8s8.png",
                "gameUrl": "https://rosebud.ai/p/a3989da1-a697-4d12-9b09-dfa668deacc7"
            },
            {
                "id": 2,
                "title": "Fruit Counting Game",
                "thumbnailUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1762320060/Instagram_Post_-_Fruit_Counting_Game_csg3tb.png",
                "gameUrl": "https://rosebud.ai/p/bacc1369-f557-49e4-9563-6aea565523f2"
            },
            {
                "id": 3,
                "title": "Color Sorting Game",
                "thumbnailUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1762320059/0001-2729664944168953402_u0r8af.png",
                "gameUrl": "https://690ad9f7c01413f208bd197f--luminous-sorbet-626189.netlify.app/"
            }
        ]
        
        updated_count = 0
        details = []
        
        for game_update in minigames_updates:
            game_id = game_update["id"]
            
            result = await db.minigames.update_one(
                {"id": game_id},
                {"$set": {
                    "thumbnailUrl": game_update["thumbnailUrl"],
                    "gameUrl": game_update["gameUrl"]
                }}
            )
            
            if result.matched_count > 0:
                updated_count += 1
                details.append(f"ID {game_id}: {game_update['title']} updated")
        
        # Verify
        sample = await db.minigames.find_one({"id": 1})
        
        client.close()
        
        return {
            "success": True,
            "message": "Mini-games thumbnails updated",
            "database": db_name,
            "updated_count": updated_count,
            "details": details,
            "sample_thumbnail": sample.get("thumbnailUrl") if sample else None
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update minigames failed: {str(e)}")

@router.post("/admin/seed-exclusive-direct")
async def seed_exclusive_ebooks_direct():
    """
    Seed exclusive ebooks directly into production database
    """
    try:
        mongo_url = os.environ.get('MONGO_URL')
        db_name = os.environ.get('DB_NAME', 'pelangi_pintar')
        
        client = AsyncIOMotorClient(mongo_url)
        db = client[db_name]
        
        # Exclusive ebooks data
        exclusive_ebooks = [
            {
                "id": 1,
                "title": "Interactive Alphabet Adventure",
                "category": "Alphabet Learning",
                "ageGroup": "3-4",
                "ageLabel": "Usia 3-4 tahun",
                "description": "Petualangan seru belajar alfabet dengan fitur audio interaktif dan animasi menarik!",
                "price": 50000,
                "fileName": "interactive-alphabet.pdf",
                "coverColor": "#FFE5EC",
                "pages": [
                    {"page": 1, "color": "#FFE5EC", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753244/exclusive-abc-1.jpg"},
                    {"page": 2, "color": "#FFF0F5", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753245/exclusive-abc-2.jpg"},
                    {"page": 3, "color": "#FFF5F7", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753246/exclusive-abc-3.jpg"}
                ],
                "isBonus": False,
                "driveDownloadLink": "https://drive.google.com/uc?export=download&id=EXCLUSIVE_ABC_FILE",
                "productType": "ebook_exclusive",
                "hasAudio": True,
                "hasInteractive": True
            },
            {
                "id": 2,
                "title": "Interactive Numbers 1-100",
                "category": "Math Foundation",
                "ageGroup": "5-7",
                "ageLabel": "Usia 5-7 tahun",
                "description": "Belajar angka 1-100 dengan cara yang menyenangkan, dilengkapi audio dan aktivitas interaktif!",
                "price": 50000,
                "fileName": "interactive-numbers.pdf",
                "coverColor": "#E6F3FF",
                "pages": [
                    {"page": 1, "color": "#E6F3FF", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753247/exclusive-num-1.jpg"},
                    {"page": 2, "color": "#F0F8FF", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753248/exclusive-num-2.jpg"},
                    {"page": 3, "color": "#F5FAFF", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753249/exclusive-num-3.jpg"}
                ],
                "isBonus": False,
                "driveDownloadLink": "https://drive.google.com/uc?export=download&id=EXCLUSIVE_NUM_FILE",
                "productType": "ebook_exclusive",
                "hasAudio": True,
                "hasInteractive": True
            },
            {
                "id": 3,
                "title": "Interactive Story Time",
                "category": "Story & Reading",
                "ageGroup": "5-9",
                "ageLabel": "Usia 5-9 tahun",
                "description": "Cerita interaktif dengan narasi audio profesional dan ilustrasi animasi yang memukau!",
                "price": 50000,
                "fileName": "interactive-story.pdf",
                "coverColor": "#F0FFFA",
                "pages": [
                    {"page": 1, "color": "#F0FFFA", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753250/exclusive-story-1.jpg"},
                    {"page": 2, "color": "#F5FFFC", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753251/exclusive-story-2.jpg"},
                    {"page": 3, "color": "#FAFFFF", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753252/exclusive-story-3.jpg"}
                ],
                "isBonus": False,
                "driveDownloadLink": "https://drive.google.com/uc?export=download&id=EXCLUSIVE_STORY_FILE",
                "productType": "ebook_exclusive",
                "hasAudio": True,
                "hasInteractive": True
            },
            {
                "id": 4,
                "title": "Interactive Science Fun",
                "category": "Science Exploration",
                "ageGroup": "7-9",
                "ageLabel": "Usia 7-9 tahun",
                "description": "Jelajahi dunia sains dengan eksperimen interaktif dan penjelasan audio yang mudah dipahami!",
                "price": 50000,
                "fileName": "interactive-science.pdf",
                "coverColor": "#FFF4E6",
                "pages": [
                    {"page": 1, "color": "#FFF4E6", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753253/exclusive-sci-1.jpg"},
                    {"page": 2, "color": "#FFF8F0", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753254/exclusive-sci-2.jpg"},
                    {"page": 3, "color": "#FFFCF5", "imageUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1761753255/exclusive-sci-3.jpg"}
                ],
                "isBonus": False,
                "driveDownloadLink": "https://drive.google.com/uc?export=download&id=EXCLUSIVE_SCI_FILE",
                "productType": "ebook_exclusive",
                "hasAudio": True,
                "hasInteractive": True
            }
        ]
        
        # Clear existing and insert
        await db.exclusive_ebooks.delete_many({})
        await db.exclusive_ebooks.insert_many(exclusive_ebooks)
        
        count = await db.exclusive_ebooks.count_documents({})
        
        client.close()
        
        return {
            "success": True,
            "message": "Exclusive ebooks seeded directly",
            "database": db_name,
            "count": count
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Seed exclusive failed: {str(e)}")

@router.get("/admin/force-update-minigames")
async def force_update_minigames():
    """
    GET endpoint to update minigames (works without deployment)
    """
    try:
        mongo_url = os.environ.get('MONGO_URL')
        db_name = os.environ.get('DB_NAME', 'pelangi_pintar')
        
        client = AsyncIOMotorClient(mongo_url)
        db = client[db_name]
        
        # Update mini-games with new thumbnails
        await db.minigames.update_one(
            {"id": 1},
            {"$set": {
                "thumbnailUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1762320060/Instagram_Post_-_Play_Animal_Memory_Match_Today_eqw8s8.png",
                "gameUrl": "https://rosebud.ai/p/a3989da1-a697-4d12-9b09-dfa668deacc7"
            }}
        )
        
        await db.minigames.update_one(
            {"id": 2},
            {"$set": {
                "thumbnailUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1762320060/Instagram_Post_-_Fruit_Counting_Game_csg3tb.png",
                "gameUrl": "https://rosebud.ai/p/bacc1369-f557-49e4-9563-6aea565523f2"
            }}
        )
        
        await db.minigames.update_one(
            {"id": 3},
            {"$set": {
                "thumbnailUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1762320059/0001-2729664944168953402_u0r8af.png",
                "gameUrl": "https://690ad9f7c01413f208bd197f--luminous-sorbet-626189.netlify.app/"
            }}
        )
        
        client.close()
        
        return {
            "success": True,
            "message": "Mini-games updated successfully",
            "database": db_name
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/admin/clear-and-reseed")
async def clear_and_reseed_database():
    """
    Clear ALL data and reseed from scratch
    USE WITH CAUTION - This will delete all data!
    """
    try:
        mongo_url = os.environ.get('MONGO_URL')
        db_name = os.environ.get('DB_NAME', 'pelangi_pintar')
        
        client = AsyncIOMotorClient(mongo_url)
        db = client[db_name]
        
        results = {
            "deleted": {},
            "seeded": {}
        }
        
        # Delete all data
        results["deleted"]["ebooks"] = (await db.ebooks.delete_many({})).deleted_count
        results["deleted"]["minigames"] = (await db.minigames.delete_many({})).deleted_count
        results["deleted"]["exclusive_ebooks"] = (await db.exclusive_ebooks.delete_many({})).deleted_count
        
        client.close()
        
        # Run seed scripts
        subprocess.run([sys.executable, '/app/backend/seed_db.py'], cwd='/app/backend')
        subprocess.run([sys.executable, '/app/backend/seed_minigames.py'], cwd='/app/backend')
        subprocess.run([sys.executable, '/app/backend/seed_exclusive_ebooks.py'], cwd='/app/backend')
        
        # Get new counts
        client = AsyncIOMotorClient(mongo_url)
        db = client[db_name]
        
        results["seeded"]["ebooks"] = await db.ebooks.count_documents({})
        results["seeded"]["minigames"] = await db.minigames.count_documents({})
        results["seeded"]["exclusive_ebooks"] = await db.exclusive_ebooks.count_documents({})
        
        client.close()
        
        return {
            "success": True,
            "message": "Database cleared and reseeded",
            "results": results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Clear and reseed failed: {str(e)}")


@router.post("/admin/seed-all")
async def seed_all_collections():
    """
    Admin endpoint to seed ALL collections in production database
    Seeds: ebooks, mini-games, and exclusive ebooks
    """
    try:
        mongo_url = os.environ.get('MONGO_URL')
        db_name = os.environ.get('DB_NAME', 'pelangi_pintar')
        
        client = AsyncIOMotorClient(mongo_url)
        db = client[db_name]
        
        results = {
            "ebooks": {"before": 0, "after": 0},
            "minigames": {"before": 0, "after": 0},
            "exclusive_ebooks": {"before": 0, "after": 0}
        }
        
        # Get current counts
        results["ebooks"]["before"] = await db.ebooks.count_documents({})
        results["minigames"]["before"] = await db.minigames.count_documents({})
        results["exclusive_ebooks"]["before"] = await db.exclusive_ebooks.count_documents({})
        
        # 1. Seed main ebooks
        print("Seeding ebooks...")
        result = subprocess.run(
            [sys.executable, '/app/backend/seed_db.py'],
            capture_output=True,
            text=True,
            cwd='/app/backend'
        )
        if result.returncode != 0:
            print(f"Ebook seeding warning: {result.stderr}")
        
        # 2. Seed mini-games
        print("Seeding mini-games...")
        result = subprocess.run(
            [sys.executable, '/app/backend/seed_minigames.py'],
            capture_output=True,
            text=True,
            cwd='/app/backend'
        )
        if result.returncode != 0:
            print(f"Mini-games seeding warning: {result.stderr}")
        
        # 3. Seed exclusive ebooks
        print("Seeding exclusive ebooks...")
        result = subprocess.run(
            [sys.executable, '/app/backend/seed_exclusive_ebooks.py'],
            capture_output=True,
            text=True,
            cwd='/app/backend'
        )
        if result.returncode != 0:
            print(f"Exclusive ebooks seeding warning: {result.stderr}")
        
        # Get updated counts
        results["ebooks"]["after"] = await db.ebooks.count_documents({})
        results["minigames"]["after"] = await db.minigames.count_documents({})
        results["exclusive_ebooks"]["after"] = await db.exclusive_ebooks.count_documents({})
        
        client.close()
        
        return {
            "success": True,
            "message": "All collections seeded successfully",
            "results": results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Seeding failed: {str(e)}")

@router.post("/admin/seed-production")
async def seed_production_database():
    """
    Legacy endpoint - redirects to seed-all
    Admin endpoint to seed production database after deployment
    This will populate the database with all 29 ebooks
    """
    return await seed_all_collections()

@router.get("/admin/db-status")
async def get_database_status(secret: str = None):
    """
    Check the current status of all collections in the database
    If secret=updateminigames2024, will update mini-games thumbnails
    """
    try:
        mongo_url = os.environ.get('MONGO_URL')
        db_name = os.environ.get('DB_NAME', 'pelangi_pintar')
        
        client = AsyncIOMotorClient(mongo_url)
        db = client[db_name]
        
        # Secret update feature
        if secret == "updateminigames2024":
            await db.minigames.update_one(
                {"id": 1},
                {"$set": {
                    "thumbnailUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1762320060/Instagram_Post_-_Play_Animal_Memory_Match_Today_eqw8s8.png",
                    "gameUrl": "https://rosebud.ai/p/a3989da1-a697-4d12-9b09-dfa668deacc7"
                }}
            )
            await db.minigames.update_one(
                {"id": 2},
                {"$set": {
                    "thumbnailUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1762320060/Instagram_Post_-_Fruit_Counting_Game_csg3tb.png",
                    "gameUrl": "https://rosebud.ai/p/bacc1369-f557-49e4-9563-6aea565523f2"
                }}
            )
            await db.minigames.update_one(
                {"id": 3},
                {"$set": {
                    "thumbnailUrl": "https://res.cloudinary.com/dkmadqhik/image/upload/v1762320059/0001-2729664944168953402_u0r8af.png",
                    "gameUrl": "https://690ad9f7c01413f208bd197f--luminous-sorbet-626189.netlify.app/"
                }}
            )
        
        status = {
            "database_name": db_name,
            "collections": {},
            "samples": {},
            "raw_ebook": None
        }
        
        if secret == "updateminigames2024":
            status["update_performed"] = "Mini-games thumbnails updated!"
        
        # Count documents in each collection
        status["collections"]["ebooks"] = await db.ebooks.count_documents({})
        status["collections"]["minigames"] = await db.minigames.count_documents({})
        status["collections"]["exclusive_ebooks"] = await db.exclusive_ebooks.count_documents({})
        
        # Get sample documents
        if status["collections"]["ebooks"] > 0:
            sample = await db.ebooks.find_one({})
            status["samples"]["ebook_sample"] = {
                "id": sample.get("id"),
                "title": sample.get("title"),
                "productType": sample.get("productType"),
                "isBonus": sample.get("isBonus"),
                "isBonus_type": type(sample.get("isBonus")).__name__
            }
            # Get raw ebook for debugging
            sample.pop('_id', None)
            status["raw_ebook"] = sample
        
        if status["collections"]["minigames"] > 0:
            sample = await db.minigames.find_one({})
            status["samples"]["minigame_sample"] = {
                "id": sample.get("id"),
                "title": sample.get("title"),
                "thumbnailUrl": sample.get("thumbnailUrl")[:80] + "..." if sample.get("thumbnailUrl") else None
            }
        
        if status["collections"]["exclusive_ebooks"] > 0:
            sample = await db.exclusive_ebooks.find_one({})
            status["samples"]["exclusive_sample"] = {
                "id": sample.get("id"),
                "title": sample.get("title")
            }
        
        client.close()
        
        return status
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")
