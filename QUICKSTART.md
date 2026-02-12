# 🚀 Quick Start Guide

## 1️⃣ Prerequisites Setup (One-time)

### Get Telegram Bot Token:
```
1. Open Telegram → Search "@BotFather"
2. Send: /newbot
3. Follow the instructions
4. Copy the token provided
```

### Get Telegram Chat ID:
```
1. Add your bot to a group or direct conversation
2. Send any message in that chat
3. Go to: https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
   (Replace <YOUR_TOKEN> with your bot token)
4. Find "chat": { "id": XXXXX }  ← This is your Chat ID
```

### Get YouTube API Key:
```
1. Go to https://console.cloud.google.com/
2. Create a new project
3. Search for "YouTube Data API v3"
4. Click Enable
5. Go to Credentials → Create Credentials → API Key
6. Copy the key
```

---

## 2️⃣ Initial Setup

### Step 1: Create .env File
```bash
cp .env.example .env
```

### Step 2: Edit .env with Your Credentials
```env
TELEGRAM_BOT_TOKEN=paste_your_bot_token_here
TELEGRAM_CHAT_ID=paste_your_chat_id_here
YOUTUBE_API_KEY=paste_your_api_key_here
WEB_UI_SECRET=change-me-to-a-strong-password
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 3️⃣ Running the Application

### Option A: Automatic (Linux/Mac)
```bash
chmod +x start.sh
./start.sh
```

### Option B: Manual (Windows or preferred method)

**Terminal 1** - Run Web Dashboard:
```bash
python app.py
```

**Terminal 2** - Run Telegram Bot:
```bash
python bot.py
```

---

## 4️⃣ Access the System

### 🌐 Web Dashboard
- URL: `http://localhost:5000`
- Password: Use whatever you set in `WEB_UI_SECRET`

### 🤖 Telegram Bot
- Send `/start` to your bot for help
- Send `/status` to check all channels
- Send `/list` to see all monitored channels

---

## 5️⃣ Add Sample Channels (Optional)

Want to test with the sample channels you provided?

```bash
python import_sample_channels.py
```

This will add all 11 sample channels automatically!

---

## 📊 How to Use

### Adding Channels via Web UI
1. Open http://localhost:5000
2. Login with your password
3. Paste a YouTube channel URL
4. Click "Add Channel"

### Checking Channel Status
- Click "Check Now" on any channel card to verify it exists
- The bot will fetch the latest video and view count

### Telegram Commands
```
/status     → See all channel statuses with latest videos
/list       → Quick list of all monitored channels
/start      → Show help menu
```

---

## ⚠️ Important Notes

- Shorts are automatically filtered out (only counts regular videos)
- Only videos from the specific channel are counted
- Channel checks take 5-10 seconds due to API calls
- Free YouTube API has daily quota limits
- Save your API key and bot token safely!

---

## 🆘 Need Help?

### Common Issues

**Bot not responding?**
- Check TELEGRAM_BOT_TOKEN in .env
- Verify bot is added to the group/chat
- Make sure python bot.py is running

**Web UI won't load?**
- Check if port 5000 is available
- Try: python app.py (look for errors)
- Verify dependencies: pip install -r requirements.txt

**YouTube API errors?**
- Verify API is enabled in Google Cloud
- Check your API quota limit
- Some private channels may not be accessible

---

## 📝 Supported Channel URL Formats

✅ Works with:
- `https://www.youtube.com/@channelname`
- `https://www.youtube.com/channel/UCXXXXXXXXX`
- `https://www.youtube.com/user/username`

---

Enjoy monitoring your YouTube channels! 🎬
