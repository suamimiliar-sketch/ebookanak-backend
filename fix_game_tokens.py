"""
Fix existing game access tokens with correct game URLs
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def fix_game_tokens():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["pelangi_pintar"]
    
    print("=== Fixing game access tokens ===\n")
    
    # Get all active tokens
    tokens = await db.game_access_tokens.find({"isActive": True}).to_list(length=None)
    
    print(f"Found {len(tokens)} active tokens to check\n")
    
    fixed_count = 0
    for token in tokens:
        token_id = token.get('tokenId')
        game_id = token.get('gameId')
        current_url = token.get('gameUrl')
        
        # Get the correct game URL from minigames collection
        game = await db.minigames.find_one({"id": game_id})
        
        if not game:
            print(f"⚠️ Token {token_id}: Game {game_id} not found in database")
            continue
        
        correct_url = game.get('gameUrl')
        
        if current_url != correct_url:
            print(f"🔧 Fixing token {token_id}:")
            print(f"   Game ID: {game_id}")
            print(f"   Old URL: {current_url}")
            print(f"   New URL: {correct_url}")
            
            # Update the token
            result = await db.game_access_tokens.update_one(
                {"tokenId": token_id},
                {"$set": {"gameUrl": correct_url}}
            )
            
            if result.modified_count > 0:
                fixed_count += 1
                print(f"   ✅ Fixed!\n")
            else:
                print(f"   ❌ Failed to update\n")
        else:
            print(f"✓ Token {token_id}: URL already correct")
    
    print(f"\n=== Summary ===")
    print(f"Total tokens checked: {len(tokens)}")
    print(f"Tokens fixed: {fixed_count}")
    print(f"Tokens already correct: {len(tokens) - fixed_count}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_game_tokens())
