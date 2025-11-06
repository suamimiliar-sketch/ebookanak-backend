from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from models import Ebook
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ebooks", tags=["ebooks"])


@router.get("", response_model=List[Ebook])
async def get_ebooks(
    ageGroup: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    productType: Optional[str] = Query("ebook")
):
    """
    Get all products with optional filters
    Support for ebook, minigame, and ebook_exclusive types
    """
    from server import db
    
    try:
        # Build query
        query = {}
        
        # Filter by age group and category (but not productType initially)
        if ageGroup and ageGroup != "all":
            query["ageGroup"] = ageGroup
        if category and category != "all":
            query["category"] = category
        
        # Fetch from appropriate collection based on productType
        if productType == "minigame":
            products = await db.minigames.find(query).to_list(100)
        elif productType == "ebook_exclusive":
            products = await db.exclusive_ebooks.find(query).to_list(100)
        else:
            # Default to ebooks collection - filter for non-bonus items in Python
            all_ebooks = await db.ebooks.find(query).to_list(100)
            # Filter out bonus items
            products = [e for e in all_ebooks if not e.get('isBonus', False)]
        
        # Convert MongoDB _id to string and remove it
        for product in products:
            product.pop('_id', None)
        
        return products
    
    except Exception as e:
        logger.error(f"Error fetching products: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch products")


@router.get("/debug/raw")
async def get_raw_ebook():
    """
    Debug endpoint - get raw ebook data
    """
    from server import db
    
    try:
        # Get one ebook without any filters
        ebook = await db.ebooks.find_one({})
        
        if ebook:
            ebook['_id'] = str(ebook['_id'])
            return {
                "raw_document": ebook,
                "isBonus_type": type(ebook.get('isBonus')).__name__,
                "isBonus_value": ebook.get('isBonus'),
                "productType": ebook.get('productType')
            }
        return {"error": "No ebooks found"}
    except Exception as e:
        return {"error": str(e)}


@router.get("/{ebook_id}", response_model=Ebook)
async def get_ebook(ebook_id: int):
    """
    Get single ebook by ID
    """
    from server import db
    
    try:
        ebook = await db.ebooks.find_one({"id": ebook_id})
        
        if not ebook:
            raise HTTPException(status_code=404, detail="Ebook not found")
        
        ebook.pop('_id', None)
        return ebook
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching ebook {ebook_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch ebook")
