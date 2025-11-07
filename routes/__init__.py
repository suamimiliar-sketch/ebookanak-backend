# routes/__init__.py
"""
Expose only the available route modules.
Intentionally NO 'games' here.
"""
__all__ = [
    "ebooks",
    "orders",
    "webhooks",
    "proxy",
    "admin",
    "game_access",
    "test_notifications",
]
