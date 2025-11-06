"""
Game Generator Service using OpenAI GPT-5
Generates interactive mini-games for children aged 5-9
"""
import os
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage
import logging

load_dotenv()

logger = logging.getLogger(__name__)

class GameGeneratorService:
    """Service for generating AI-powered mini-games"""
    
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY")
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment variables")
        
        self.system_message = """You are a creative educational game designer for children aged 5-9.
Your task is to create engaging, age-appropriate mini-games that are:
- Educational and fun
- Easy to understand with simple instructions
- Colorful and visually appealing
- Safe and child-friendly
- Interactive and engaging

Game types you can create:
1. Matching Games: Match pairs of items (animals, shapes, colors, etc.)
2. Coloring Games: Simple coloring activities with themes
3. Sorting Games: Sort items by category, size, color, etc.
4. Puzzle Games: Simple jigsaw or pattern puzzles
5. Memory Games: Card flip memory games

Return your response as valid JSON with this structure:
{
    "title": "Game Title",
    "description": "Brief description",
    "ageGroup": "5-9",
    "gameType": "matching|coloring|sorting|puzzle|memory",
    "difficulty": "easy|medium",
    "instructions": "Step by step instructions for children",
    "gameData": {
        // Game-specific data structure
    },
    "educationalValue": "What children learn from this game"
}"""
    
    def _create_chat_session(self, session_id: str) -> LlmChat:
        """Create a new LLM chat session"""
        chat = LlmChat(
            api_key=self.api_key,
            session_id=session_id,
            system_message=self.system_message
        )
        # Use OpenAI GPT-5
        chat.with_model("openai", "gpt-5")
        return chat
    
    async def generate_matching_game(self, theme: str = "animals") -> Dict[str, Any]:
        """Generate a matching game"""
        session_id = f"matching-{uuid.uuid4()}"
        chat = self._create_chat_session(session_id)
        
        prompt = f"""Create a matching game with theme: {theme}.
The game should have 6-8 pairs of items to match.
Include colorful emojis or simple descriptions for each item.
Make it educational and fun for children aged 5-9."""
        
        user_message = UserMessage(text=prompt)
        
        try:
            response = await chat.send_message(user_message)
            logger.info(f"Generated matching game: {theme}")
            
            # Parse JSON response
            game_data = self._parse_game_response(response)
            return game_data
            
        except Exception as e:
            logger.error(f"Error generating matching game: {str(e)}")
            # Return a default fallback game
            return self._get_fallback_matching_game(theme)
    
    async def generate_memory_game(self, theme: str = "shapes") -> Dict[str, Any]:
        """Generate a memory card game"""
        session_id = f"memory-{uuid.uuid4()}"
        chat = self._create_chat_session(session_id)
        
        prompt = f"""Create a memory card game with theme: {theme}.
The game should have 8-12 cards (4-6 pairs).
Each card should have a simple emoji or icon.
Include colorful descriptions and make it engaging for kids."""
        
        user_message = UserMessage(text=prompt)
        
        try:
            response = await chat.send_message(user_message)
            logger.info(f"Generated memory game: {theme}")
            
            game_data = self._parse_game_response(response)
            return game_data
            
        except Exception as e:
            logger.error(f"Error generating memory game: {str(e)}")
            return self._get_fallback_memory_game(theme)
    
    async def generate_sorting_game(self, theme: str = "colors") -> Dict[str, Any]:
        """Generate a sorting game"""
        session_id = f"sorting-{uuid.uuid4()}"
        chat = self._create_chat_session(session_id)
        
        prompt = f"""Create a sorting game with theme: {theme}.
The game should have 3-4 categories and 10-12 items to sort.
Make it visually appealing with emojis or simple icons.
Include clear instructions for children."""
        
        user_message = UserMessage(text=prompt)
        
        try:
            response = await chat.send_message(user_message)
            logger.info(f"Generated sorting game: {theme}")
            
            game_data = self._parse_game_response(response)
            return game_data
            
        except Exception as e:
            logger.error(f"Error generating sorting game: {str(e)}")
            return self._get_fallback_sorting_game(theme)
    
    async def generate_puzzle_game(self, difficulty: str = "easy") -> Dict[str, Any]:
        """Generate a puzzle game"""
        session_id = f"puzzle-{uuid.uuid4()}"
        chat = self._create_chat_session(session_id)
        
        prompt = f"""Create a puzzle game with difficulty: {difficulty}.
The game should have a simple pattern or sequence puzzle.
Include visual elements and clear instructions.
Make it appropriate for children aged 5-9."""
        
        user_message = UserMessage(text=prompt)
        
        try:
            response = await chat.send_message(user_message)
            logger.info(f"Generated puzzle game: {difficulty}")
            
            game_data = self._parse_game_response(response)
            return game_data
            
        except Exception as e:
            logger.error(f"Error generating puzzle game: {str(e)}")
            return self._get_fallback_puzzle_game(difficulty)
    
    async def generate_coloring_game(self, theme: str = "nature") -> Dict[str, Any]:
        """Generate a coloring game"""
        session_id = f"coloring-{uuid.uuid4()}"
        chat = self._create_chat_session(session_id)
        
        prompt = f"""Create a coloring game with theme: {theme}.
The game should describe a simple coloring activity.
Include color palette suggestions and creative ideas.
Make it fun and creative for children."""
        
        user_message = UserMessage(text=prompt)
        
        try:
            response = await chat.send_message(user_message)
            logger.info(f"Generated coloring game: {theme}")
            
            game_data = self._parse_game_response(response)
            return game_data
            
        except Exception as e:
            logger.error(f"Error generating coloring game: {str(e)}")
            return self._get_fallback_coloring_game(theme)
    
    def _parse_game_response(self, response: str) -> Dict[str, Any]:
        """Parse the AI response and extract game data"""
        try:
            # Try to find JSON in the response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                game_data = json.loads(json_str)
                return game_data
            else:
                # If no JSON found, create a structured response
                return {
                    "title": "Generated Game",
                    "description": response[:200],
                    "ageGroup": "5-9",
                    "gameType": "custom",
                    "difficulty": "medium",
                    "instructions": response,
                    "gameData": {},
                    "educationalValue": "Learning through play"
                }
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {str(e)}")
            return {
                "title": "Generated Game",
                "description": "An engaging game for children",
                "ageGroup": "5-9",
                "gameType": "custom",
                "difficulty": "medium",
                "instructions": response,
                "gameData": {},
                "educationalValue": "Learning through play"
            }
    
    def _get_fallback_matching_game(self, theme: str) -> Dict[str, Any]:
        """Fallback matching game if AI generation fails"""
        return {
            "title": f"Match the {theme.title()}",
            "description": f"Find and match pairs of {theme}!",
            "ageGroup": "5-9",
            "gameType": "matching",
            "difficulty": "easy",
            "instructions": "Click on two cards to flip them. Find all matching pairs!",
            "gameData": {
                "pairs": [
                    {"id": 1, "emoji": "🐶", "name": "Dog"},
                    {"id": 2, "emoji": "🐱", "name": "Cat"},
                    {"id": 3, "emoji": "🐭", "name": "Mouse"},
                    {"id": 4, "emoji": "🐰", "name": "Rabbit"},
                    {"id": 5, "emoji": "🦊", "name": "Fox"},
                    {"id": 6, "emoji": "🐻", "name": "Bear"}
                ]
            },
            "educationalValue": "Improves memory, concentration, and visual recognition"
        }
    
    def _get_fallback_memory_game(self, theme: str) -> Dict[str, Any]:
        """Fallback memory game"""
        return {
            "title": f"Memory Challenge: {theme.title()}",
            "description": "Flip cards and find matching pairs!",
            "ageGroup": "5-9",
            "gameType": "memory",
            "difficulty": "easy",
            "instructions": "Click cards to reveal them. Find all matching pairs with the fewest flips!",
            "gameData": {
                "cards": [
                    {"id": 1, "emoji": "⭐", "name": "Star"},
                    {"id": 2, "emoji": "🌙", "name": "Moon"},
                    {"id": 3, "emoji": "☀️", "name": "Sun"},
                    {"id": 4, "emoji": "🌈", "name": "Rainbow"},
                    {"id": 5, "emoji": "⚡", "name": "Lightning"},
                    {"id": 6, "emoji": "💧", "name": "Water"}
                ]
            },
            "educationalValue": "Enhances memory, focus, and pattern recognition"
        }
    
    def _get_fallback_sorting_game(self, theme: str) -> Dict[str, Any]:
        """Fallback sorting game"""
        return {
            "title": f"Sort by {theme.title()}",
            "description": "Put items in the right category!",
            "ageGroup": "5-9",
            "gameType": "sorting",
            "difficulty": "easy",
            "instructions": "Drag each item to its matching category!",
            "gameData": {
                "categories": ["Red", "Blue", "Yellow"],
                "items": [
                    {"id": 1, "emoji": "🍎", "name": "Apple", "category": "Red"},
                    {"id": 2, "emoji": "🌊", "name": "Ocean", "category": "Blue"},
                    {"id": 3, "emoji": "🌞", "name": "Sun", "category": "Yellow"},
                    {"id": 4, "emoji": "🍓", "name": "Strawberry", "category": "Red"},
                    {"id": 5, "emoji": "💙", "name": "Heart", "category": "Blue"},
                    {"id": 6, "emoji": "⭐", "name": "Star", "category": "Yellow"}
                ]
            },
            "educationalValue": "Develops categorization skills and logical thinking"
        }
    
    def _get_fallback_puzzle_game(self, difficulty: str) -> Dict[str, Any]:
        """Fallback puzzle game"""
        return {
            "title": "Pattern Puzzle",
            "description": "Complete the pattern!",
            "ageGroup": "5-9",
            "gameType": "puzzle",
            "difficulty": difficulty,
            "instructions": "Look at the pattern and choose the missing piece!",
            "gameData": {
                "pattern": ["🔴", "🔵", "🔴", "🔵", "?"],
                "options": ["🔴", "🔵", "🟡", "🟢"],
                "answer": "🔴"
            },
            "educationalValue": "Builds pattern recognition and problem-solving skills"
        }
    
    def _get_fallback_coloring_game(self, theme: str) -> Dict[str, Any]:
        """Fallback coloring game"""
        return {
            "title": f"Color the {theme.title()}",
            "description": "Get creative with colors!",
            "ageGroup": "5-9",
            "gameType": "coloring",
            "difficulty": "easy",
            "instructions": "Choose your favorite colors and create a beautiful picture!",
            "gameData": {
                "theme": theme,
                "colorPalette": ["🔴 Red", "🔵 Blue", "🟡 Yellow", "🟢 Green", "🟣 Purple", "🟠 Orange"],
                "suggestions": [
                    "Start with light colors",
                    "Stay inside the lines",
                    "Mix colors to create new ones",
                    "Have fun and be creative!"
                ]
            },
            "educationalValue": "Encourages creativity, fine motor skills, and color recognition"
        }


# Create singleton instance
game_generator = GameGeneratorService()
