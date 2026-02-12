#!/bin/bash

# YouTube Channel Monitor - Startup Script

echo "🎬 Starting YouTube Channel Monitor..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "⚠️  Please edit the .env file with your credentials:"
    echo "   - TELEGRAM_BOT_TOKEN: Get from BotFather on Telegram"
    echo "   - TELEGRAM_CHAT_ID: Your Telegram chat/group ID"
    echo "   - YOUTUBE_API_KEY: Get from Google Cloud Console"
    echo "   - WEB_UI_SECRET: Change to a strong password"
    echo ""
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt --quiet
echo "✅ Dependencies installed"
echo ""

# Run both the web app and the bot
echo "🚀 Starting services..."
echo "   - Web UI: http://localhost:5000"
echo "   - Telegram Bot: Listening for commands"
echo ""

# Start Flask app in background
python app.py &
FLASK_PID=$!

# Start Telegram bot
python bot.py

# If bot terminates, kill Flask too
kill $FLASK_PID 2>/dev/null
