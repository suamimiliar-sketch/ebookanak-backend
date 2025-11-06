"""
Game Access Routes
Handles temporary 24-hour access links for external games
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/game-access", tags=["game-access"])


@router.get("/{token}")
async def access_game(token: str):
    """
    Verify access token and redirect to game
    Token is valid for 24 hours from purchase
    """
    from server import db
    
    try:
        # Find token in database
        access_token = await db.game_access_tokens.find_one({"tokenId": token})
        
        if not access_token:
            raise HTTPException(
                status_code=404,
                detail="Link game tidak ditemukan. Silakan hubungi customer service."
            )
        
        # Check if token is active
        if not access_token.get("isActive", True):
            raise HTTPException(
                status_code=403,
                detail="Link game ini sudah tidak aktif."
            )
        
        # Check expiration
        expires_at_str = access_token.get("expiresAt")
        if expires_at_str:
            expires_at = datetime.fromisoformat(expires_at_str)
            now = datetime.now(timezone.utc)
            
            if now > expires_at:
                # Mark as expired
                await db.game_access_tokens.update_one(
                    {"tokenId": token},
                    {"$set": {"isActive": False}}
                )
                
                raise HTTPException(
                    status_code=403,
                    detail="Link game Anda sudah expired (24 jam). Silakan beli kembali untuk mengakses game."
                )
        
        # Update access count
        await db.game_access_tokens.update_one(
            {"tokenId": token},
            {"$inc": {"accessCount": 1}}
        )
        
        # Get game URL
        game_url = access_token.get("gameUrl")
        if not game_url:
            raise HTTPException(
                status_code=500,
                detail="Game URL tidak ditemukan."
            )
        
        logger.info(f"Access granted for token {token}, redirecting to {game_url}")
        
        # Redirect to actual game
        return RedirectResponse(url=game_url, status_code=302)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error accessing game with token {token}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Terjadi kesalahan saat mengakses game. Silakan coba lagi."
        )
