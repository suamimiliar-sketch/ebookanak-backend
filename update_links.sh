#!/bin/bash
# Easy script to update Google Drive links
# Usage: ./update_links.sh

echo "📚 Updating Pelangi Pintar Ebook Download Links"
echo "================================================"
echo ""

# Use the correct Python environment
/root/.venv/bin/python /app/backend/update_drive_links.py

echo ""
echo "✅ Done! Backend will use these links on next order."
echo "💡 Don't forget to test by making a payment!"
