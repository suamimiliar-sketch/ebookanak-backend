"""
Game Access Service
Manages 24-hour expiring access tokens for mini-games
"""
import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class GameAccessService:
    """Service for managing game access tokens"""
    
    def __init__(self, db):
        self.db = db
        self.collection = db.game_access_tokens
    
    async def create_access_token(
        self, 
        order_id: str, 
        customer_email: str,
        game_ids: list,
        duration_hours: int = 24
    ) -> Dict[str, Any]:
        """
        Create a new access token for games
        
        Args:
            order_id: The order ID associated with the purchase
            customer_email: Customer's email address
            game_ids: List of game IDs purchased
            duration_hours: Token validity duration (default 24 hours)
            
        Returns:
            Dictionary containing token details
        """
        try:
            token_id = str(uuid.uuid4())
            now = datetime.now(timezone.utc)
            expires_at = now + timedelta(hours=duration_hours)
            
            access_token = {
                "tokenId": token_id,
                "orderId": order_id,
                "customerEmail": customer_email,
                "gameIds": game_ids,
                "createdAt": now.isoformat(),
                "expiresAt": expires_at.isoformat(),
                "isActive": True,
                "accessCount": 0
            }
            
            # Insert into database
            await self.collection.insert_one(access_token)
            
            logger.info(f"Created access token {token_id} for order {order_id}")
            
            # Remove MongoDB _id for response
            access_token.pop('_id', None)
            
            return {
                "success": True,
                "token": access_token
            }
            
        except Exception as e:
            logger.error(f"Error creating access token: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def verify_access_token(self, token_id: str) -> Dict[str, Any]:
        """
        Verify if an access token is valid
        
        Args:
            token_id: The token ID to verify
            
        Returns:
            Dictionary containing verification result
        """
        try:
            token = await self.collection.find_one({"tokenId": token_id})
            
            if not token:
                return {
                    "valid": False,
                    "reason": "Token not found"
                }
            
            # Check if token is active
            if not token.get("isActive"):
                return {
                    "valid": False,
                    "reason": "Token is inactive"
                }
            
            # Check expiration
            expires_at = datetime.fromisoformat(token["expiresAt"])
            now = datetime.now(timezone.utc)
            
            if now > expires_at:
                # Mark token as expired
                await self.collection.update_one(
                    {"tokenId": token_id},
                    {"$set": {"isActive": False}}
                )
                
                return {
                    "valid": False,
                    "reason": "Token has expired"
                }
            
            # Update access count
            await self.collection.update_one(
                {"tokenId": token_id},
                {"$inc": {"accessCount": 1}}
            )
            
            # Remove _id for response
            token.pop('_id', None)
            
            # Calculate time remaining
            time_remaining = expires_at - now
            hours_remaining = int(time_remaining.total_seconds() / 3600)
            minutes_remaining = int((time_remaining.total_seconds() % 3600) / 60)
            
            return {
                "valid": True,
                "token": token,
                "timeRemaining": {
                    "hours": hours_remaining,
                    "minutes": minutes_remaining,
                    "expiresAt": token["expiresAt"]
                }
            }
            
        except Exception as e:
            logger.error(f"Error verifying access token: {str(e)}")
            return {
                "valid": False,
                "reason": f"Error: {str(e)}"
            }
    
    async def revoke_access_token(self, token_id: str) -> Dict[str, Any]:
        """
        Revoke an access token
        
        Args:
            token_id: The token ID to revoke
            
        Returns:
            Dictionary containing revocation result
        """
        try:
            result = await self.collection.update_one(
                {"tokenId": token_id},
                {"$set": {"isActive": False}}
            )
            
            if result.modified_count > 0:
                logger.info(f"Revoked access token {token_id}")
                return {
                    "success": True,
                    "message": "Token revoked successfully"
                }
            else:
                return {
                    "success": False,
                    "message": "Token not found"
                }
                
        except Exception as e:
            logger.error(f"Error revoking access token: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_user_active_tokens(self, customer_email: str) -> Dict[str, Any]:
        """
        Get all active tokens for a user
        
        Args:
            customer_email: Customer's email address
            
        Returns:
            Dictionary containing list of active tokens
        """
        try:
            now = datetime.now(timezone.utc).isoformat()
            
            tokens = await self.collection.find({
                "customerEmail": customer_email,
                "isActive": True,
                "expiresAt": {"$gt": now}
            }).to_list(length=100)
            
            # Remove _id from each token
            for token in tokens:
                token.pop('_id', None)
            
            return {
                "success": True,
                "tokens": tokens,
                "count": len(tokens)
            }
            
        except Exception as e:
            logger.error(f"Error getting user tokens: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "tokens": []
            }
    
    async def cleanup_expired_tokens(self) -> Dict[str, Any]:
        """
        Clean up expired tokens (for maintenance tasks)
        
        Returns:
            Dictionary containing cleanup result
        """
        try:
            now = datetime.now(timezone.utc).isoformat()
            
            result = await self.collection.update_many(
                {
                    "expiresAt": {"$lt": now},
                    "isActive": True
                },
                {"$set": {"isActive": False}}
            )
            
            logger.info(f"Cleaned up {result.modified_count} expired tokens")
            
            return {
                "success": True,
                "deactivatedCount": result.modified_count
            }
            
        except Exception as e:
            logger.error(f"Error cleaning up tokens: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }


def create_game_access_service(db):
    """Factory function to create GameAccessService"""
    return GameAccessService(db)
