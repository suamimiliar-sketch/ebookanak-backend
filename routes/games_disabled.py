"""
Games API Routes
Handles game generation, access, and management
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from services.game_generator_service import game_generator
from services.game_access_service import create_game_access_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/games", tags=["games"])

# Request/Response Models
class GenerateGameRequest(BaseModel):
    gameType: str  # matching, memory, sorting, puzzle, coloring
    theme: Optional[str] = "general"
    difficulty: Optional[str] = "easy"

class CreateAccessTokenRequest(BaseModel):
    orderId: str
    customerEmail: EmailStr
    gameIds: List[int]
    durationHours: Optional[int] = 24

class AccessTokenResponse(BaseModel):
    success: bool
    token: Optional[dict] = None
    error: Optional[str] = None

class VerifyTokenResponse(BaseModel):
    valid: bool
    token: Optional[dict] = None
    timeRemaining: Optional[dict] = None
    reason: Optional[str] = None


@router.post("/generate", summary="Generate a new mini-game")
async def generate_game(request: GenerateGameRequest):
    """
    Generate a new mini-game using AI
    
    Game types:
    - matching: Match pairs of items
    - memory: Memory card game
    - sorting: Sort items by category
    - puzzle: Pattern or sequence puzzle
    - coloring: Coloring activity
    """
    try:
        game_type = request.gameType.lower()
        theme = request.theme or "general"
        difficulty = request.difficulty or "easy"
        
        # Generate game based on type
        if game_type == "matching":
            game_data = await game_generator.generate_matching_game(theme)
        elif game_type == "memory":
            game_data = await game_generator.generate_memory_game(theme)
        elif game_type == "sorting":
            game_data = await game_generator.generate_sorting_game(theme)
        elif game_type == "puzzle":
            game_data = await game_generator.generate_puzzle_game(difficulty)
        elif game_type == "coloring":
            game_data = await game_generator.generate_coloring_game(theme)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid game type: {game_type}. Must be one of: matching, memory, sorting, puzzle, coloring"
            )
        
        logger.info(f"Generated {game_type} game with theme: {theme}")
        
        return {
            "success": True,
            "game": game_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating game: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate game: {str(e)}"
        )


@router.post("/access/create", response_model=AccessTokenResponse, summary="Create game access token")
async def create_access_token(request: CreateAccessTokenRequest):
    """
    Create a 24-hour access token for purchased games
    
    This token will be sent to the customer via email
    and allows them to access the games for the specified duration.
    """
    from server import db
    
    try:
        game_access_service = create_game_access_service(db)
        
        result = await game_access_service.create_access_token(
            order_id=request.orderId,
            customer_email=request.customerEmail,
            game_ids=request.gameIds,
            duration_hours=request.durationHours
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Failed to create access token")
            )
        
        logger.info(f"Created access token for order: {request.orderId}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating access token: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create access token: {str(e)}"
        )


@router.get("/access/verify/{token_id}", response_model=VerifyTokenResponse, summary="Verify access token")
async def verify_access_token(token_id: str):
    """
    Verify if an access token is valid and not expired
    
    Returns token details and remaining time if valid.
    """
    from server import db
    
    try:
        game_access_service = create_game_access_service(db)
        
        result = await game_access_service.verify_access_token(token_id)
        
        return result
        
    except Exception as e:
        logger.error(f"Error verifying access token: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to verify access token: {str(e)}"
        )


@router.get("/access/user/{email}", summary="Get user's active tokens")
async def get_user_tokens(email: str):
    """
    Get all active access tokens for a user
    """
    from server import db
    
    try:
        game_access_service = create_game_access_service(db)
        
        result = await game_access_service.get_user_active_tokens(email)
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting user tokens: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get user tokens: {str(e)}"
        )


@router.post("/access/revoke/{token_id}", summary="Revoke access token")
async def revoke_access_token(token_id: str):
    """
    Revoke an access token (admin only in production)
    """
    from server import db
    
    try:
        game_access_service = create_game_access_service(db)
        
        result = await game_access_service.revoke_access_token(token_id)
        
        if not result.get("success"):
            raise HTTPException(
                status_code=404,
                detail=result.get("message", "Token not found")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error revoking access token: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to revoke access token: {str(e)}"
        )


@router.get("/{game_id}", summary="Get game details")
async def get_game(game_id: int):
    """
    Get details for a specific game
    """
    from server import db
    
    try:
        game = await db.minigames.find_one({"id": game_id})
        
        if not game:
            raise HTTPException(
                status_code=404,
                detail="Game not found"
            )
        
        # Remove MongoDB _id
        game.pop('_id', None)
        
        return {
            "success": True,
            "game": game
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting game: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get game: {str(e)}"
        )


@router.post("/cleanup", summary="Cleanup expired tokens")
async def cleanup_expired_tokens():
    """
    Maintenance endpoint to clean up expired tokens
    (Should be called by a scheduled job in production)
    """
    from server import db
    
    try:
        game_access_service = create_game_access_service(db)
        
        result = await game_access_service.cleanup_expired_tokens()
        
        return result
        
    except Exception as e:
        logger.error(f"Error cleaning up tokens: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to cleanup tokens: {str(e)}"
        )
