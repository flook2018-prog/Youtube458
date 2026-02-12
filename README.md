# 🎬 YouTube Channel Monitor Bot

A Telegram bot with web dashboard that monitors YouTube channels and notifies their status. Easily manage channels through a beautiful web interface without editing code.

## ✨ Features

- **📱 Telegram Bot**: Send `/status` command to check all monitored channels
- **🌐 Web Dashboard**: User-friendly interface to add/remove channels  
- **✅ Channel Status**: Real-time status checking (active/inactive)
- **📊 Video Analytics**: Latest video title and view count from each channel
- **🎯 Smart Filtering**: Only counts regular videos, excludes YouTube Shorts
- **🔐 Password Protected**: Secure web UI with authentication
- **💾 SQLite Database**: Persistent storage of channel data
- **🚀 Easy Setup**: No code editing needed for managing channels

## 📋 Requirements

- Python 3.8+
- Telegram Bot Token (from BotFather)  
- YouTube API Key (from Google Cloud Console)
- Telegram Chat/Group ID

## 🛠️ Setup Instructions

### 1. Clone and Install

\`\`\`bash
cd Youtube458
pip install -r requirements.txt
\`\`\`

### 2. Configure Environment

Copy \`.env.example\` to \`.env\` and fill in your credentials:

\`\`\`bash
cp .env.example .env
# Edit .env with your credentials
\`\`\`

### 3. Get Your Credentials

#### Telegram Bot Token:
1. Open Telegram and search for \`@BotFather\`
2. Send \`/start\` then \`/newbot\`
3. Follow the instructions to create a bot
4. Copy the token

#### Telegram Chat ID:
1. Add your bot to a group or chat
2. Send a message in the chat
3. Go to: \`https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates\`
4. Find your chat ID in the response

#### YouTube API Key:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable "YouTube Data API v3"
4. Create an API key (Credentials > Create Credentials > API Key)
5. Copy the key

### 4. Run the Application

\`\`\`bash
# Make the script executable
chmod +x start.sh

# Run the application
./start.sh
\`\`\`

Or manually:

\`\`\`bash
# Terminal 1 - Run Flask web app
python app.py

# Terminal 2 - Run Telegram bot
python bot.py
\`\`\`

## 📖 Usage

### 🌐 Web Interface

Open your browser to: \`http://localhost:5000\`

**Default credentials:** Use the password from \`WEB_UI_SECRET\` in your \`.env\` file

**Features:**
- ➕ **Add Channel**: Paste YouTube channel URL
- 🔍 **Check Status**: Click "Check Now" to manually verify a channel
- 🗑️ **Remove Channel**: Delete channels you no longer want to monitor
- 📊 **View Stats**: See latest video and view count for each channel

### 🤖 Telegram Bot Commands

\`\`\`
/start    - Show available commands
/status   - Check status of all monitored channels
/list     - List all monitored channels
\`\`\`

### Supported YouTube URL Formats

- \`https://www.youtube.com/@channelname\`
- \`https://www.youtube.com/channel/UCXXXXXXXXX\`
- \`https://www.youtube.com/user/username\`

## 📁 Project Structure

\`\`\`
Youtube458/
├── app.py                 # Flask web application
├── bot.py                 # Telegram bot
├── database.py            # Database operations
├── youtube_handler.py     # YouTube API integration
├── config.py              # Configuration
├── templates/
│   ├── login.html        # Login page
│   └── index.html        # Dashboard
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
└── README.md             # This file
\`\`\`

## 🔑 Configuration Options

Edit \`.env\` file:

\`\`\`env
# Telegram
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# YouTube API
YOUTUBE_API_KEY=your_api_key_here

# Flask
FLASK_PORT=5000
FLASK_HOST=0.0.0.0

# Web Security
WEB_UI_SECRET=strong-password-here
\`\`\`

## 📝 Notes

- Video statistics are cached at check time
- Shorts are automatically filtered out
- Only regular videos from the channel are counted
- Web interface auto-refreshes every 5 minutes
- Status checks are not real-time, run "Check Now" for immediate update

---

Made with ❤️ for YouTube enthusiasts
