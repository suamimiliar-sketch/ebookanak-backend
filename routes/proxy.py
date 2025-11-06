from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
import httpx
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/proxy/image")
async def proxy_image(url: str):
    """
    Proxy images from external sources to bypass CORS/CSP issues
    """
    try:
        # Validate URL is from trusted image CDN
        allowed_domains = [
            "https://i.ibb.co/",
            "https://res.cloudinary.com/"
        ]
        
        if not any(url.startswith(domain) for domain in allowed_domains):
            raise HTTPException(status_code=400, detail="Invalid image URL - must be from trusted CDN")
        
        # Fetch image from CDN
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            
            # Return image with proper content type
            content_type = response.headers.get("content-type", "image/png")
            return Response(
                content=response.content,
                media_type=content_type,
                headers={
                    "Cache-Control": "public, max-age=31536000",
                    "Access-Control-Allow-Origin": "*"
                }
            )
    
    except httpx.HTTPStatusError as e:
        logger.error(f"Failed to fetch image {url}: {e}")
        raise HTTPException(status_code=404, detail="Image not found")
    except Exception as e:
        logger.error(f"Error proxying image: {e}")
        raise HTTPException(status_code=500, detail="Failed to load image")
