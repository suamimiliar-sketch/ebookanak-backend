"""
Test endpoint for email notifications
This allows you to test email delivery without completing actual payments
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from services.notification_service import send_email, send_game_links_email
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/test", tags=["testing"])


class TestEbookEmail(BaseModel):
    email: EmailStr
    customerName: str
    orderId: str = "TEST-ORDER-123"
    ebookTitles: Optional[List[str]] = ["Test Ebook 1", "Test Ebook 2"]


class TestGameEmail(BaseModel):
    email: EmailStr
    customerName: str
    orderId: str = "TEST-GAME-ORDER-456"
    gameIds: Optional[List[int]] = [1, 2]


@router.post("/send-ebook-email")
async def test_ebook_email(data: TestEbookEmail):
    """
    Test ebook download email
    
    Example:
    POST /api/test/send-ebook-email
    {
        "email": "your-email@example.com",
        "customerName": "Test User",
        "orderId": "TEST-123",
        "ebookTitles": ["Shapes Activity Book", "Colors Book"]
    }
    """
    try:
        # Create dummy ebook data with Google Drive links
        ebooks = []
        for title in data.ebookTitles:
            ebooks.append({
                'title': title,
                'downloadLink': 'https://drive.google.com/file/d/1_DUMMY_FILE_ID/view?usp=sharing'
            })
        
        # Send test email
        success = send_email(
            to_email=data.email,
            customer_name=data.customerName,
            order_id=data.orderId,
            ebooks=ebooks
        )
        
        if success:
            return {
                'success': True,
                'message': f'Test ebook email sent successfully to {data.email}',
                'order_id': data.orderId,
                'ebooks_count': len(ebooks)
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to send email. Check SMTP configuration.")
            
    except Exception as e:
        logger.error(f"Error sending test ebook email: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/send-game-email")
async def test_game_email(data: TestGameEmail):
    """
    Test game access email with 24-hour expiring links
    
    Example:
    POST /api/test/send-game-email
    {
        "email": "your-email@example.com",
        "customerName": "Test User",
        "orderId": "TEST-GAME-456",
        "gameIds": [1, 2]
    }
    """
    from server import db
    
    try:
        # Fetch real game data from database
        games = []
        for game_id in data.gameIds:
            game_data = await db.minigames.find_one({"id": game_id})
            if game_data:
                games.append({
                    'id': game_id,
                    'title': game_data.get('title', f'Mini Game {game_id}'),
                    'gameUrl': f'/api/game-access/TEST-TOKEN-{game_id}',  # Test proxy URL
                    'icon': game_data.get('icon', '🎮')
                })
        
        if not games:
            raise HTTPException(status_code=404, detail="No games found with provided IDs")
        
        # Send test email
        success = send_game_links_email(
            to_email=data.email,
            customer_name=data.customerName,
            order_id=data.orderId,
            games=games,
            expires_hours=24
        )
        
        if success:
            return {
                'success': True,
                'message': f'Test game email sent successfully to {data.email}',
                'order_id': data.orderId,
                'games_count': len(games),
                'games': [{'id': g['id'], 'title': g['title']} for g in games]
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to send email. Check SMTP configuration.")
            
    except Exception as e:
        logger.error(f"Error sending test game email: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/smtp-status")
async def check_smtp_status():
    """
    Check if SMTP is configured properly
    """
    import os
    
    smtp_host = os.environ.get('SMTP_HOST')
    smtp_email = os.environ.get('SMTP_EMAIL')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    smtp_port = os.environ.get('SMTP_PORT', '465')
    
    return {
        'smtp_configured': all([smtp_host, smtp_email, smtp_password]),
        'smtp_host': smtp_host if smtp_host else 'NOT_CONFIGURED',
        'smtp_email': smtp_email if smtp_email else 'NOT_CONFIGURED',
        'smtp_port': smtp_port,
        'smtp_password_set': bool(smtp_password)
    }
