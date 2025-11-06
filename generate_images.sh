#!/bin/bash
# Quick start script for PDF auto-generation

echo "╔══════════════════════════════════════════════════════════╗"
echo "║  🚀 Pelangi Pintar - PDF Auto Image Generator            ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check if credentials.json exists
if [ ! -f "/app/backend/credentials.json" ]; then
    echo "❌ credentials.json not found!"
    echo ""
    echo "📝 Setup Instructions:"
    echo "1. Follow the guide in AUTO_GENERATE_SETUP_GUIDE.md"
    echo "2. Create OAuth credentials in Google Cloud Console"
    echo "3. Download and place credentials.json in /app/backend/"
    echo ""
    echo "Quick link: https://console.cloud.google.com/apis/credentials"
    echo ""
    exit 1
fi

echo "✅ Found credentials.json"
echo ""
echo "🚀 Starting PDF processing..."
echo ""

# Run the script
/root/.venv/bin/python /app/backend/auto_generate_images.py

echo ""
echo "✅ Done! Check the output above for results."
echo ""
echo "📝 Next steps:"
echo "1. Restart services: sudo supervisorctl restart all"
echo "2. Visit your website to see real PDF preview images!"
echo ""
