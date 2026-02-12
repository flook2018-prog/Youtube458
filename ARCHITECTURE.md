# 🏗️ Architecture & API Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                      │
├─────────────────────────────────────────────────────────────┤
│  🌐 Web Dashboard (Flask)     │  🤖 Telegram Bot             │
│  - Channel Management UI      │  - /status command           │
│  - Real-time Status Display   │  - /list command             │
│  - Video Analytics            │  - /start command            │
└────────────────┬──────────────┴────────────────┬─────────────┘
                 │                              │
         ┌───────▼──────────────────────────────▼──┐
         │   Business Logic Layer                   │
         ├────────────────────────────────────────┤
         │  - YouTubeHandler (API Integration)    │
         │  - Channel Status Checking             │
         │  - Video Information Extraction        │
         │  - Shorts Filtering                    │
         └───────┬────────────────────────────┬───┘
                 │                            │
      ┌──────────▼─┐              ┌──────────▼──┐
      │  YouTube   │              │  Telegram   │
      │  Data API  │              │   Bot API   │
      └────────────┘              └─────────────┘
                 │                            │
         ┌───────▼──────────────────────────▼───┐
         │  Data Storage Layer                   │
         ├────────────────────────────────────┤
         │  SQLite Database (channels.db)      │
         │  - Channel URLs                     │
         │  - Channel Names                    │
         │  - Video Statistics                 │
         │  - Status History                   │
         └────────────────────────────────────┘
```

## File Structure

```
Youtube458/
│
├── Core Application
│   ├── app.py                    # Flask web application
│   ├── bot.py                    # Telegram bot handler
│   ├── config.py                 # Configuration management
│   ├── database.py               # SQLite database operations
│   └── youtube_handler.py        # YouTube API wrapper
│
├── Web Interface
│   └── templates/
│       ├── login.html            # Authentication page
│       └── index.html            # Main dashboard
│
├── Configuration
│   ├── .env.example              # Environment template
│   ├── .gitignore                # Git ignore rules
│   └── requirements.txt           # Python dependencies
│
├── Utilities & Documentation
│   ├── import_sample_channels.py # Bulk import utility
│   ├── check_setup.py            # Setup verification
│   ├── README.md                 # Full documentation
│   ├── QUICKSTART.md             # Quick setup guide
│   ├── ARCHITECTURE.md           # This file
│   └── start.sh                  # Start script
└── Database
    └── channels.db               # SQLite database (created at runtime)
```

## API Endpoints

### Web API (Flask)

#### Authentication
```
POST /login
  - POST form: password
  - Returns: Session cookie if correct
  - Redirects to / on success
```

#### Channel Management
```
GET /api/channels
  - Auth: Required (session)
  - Returns: JSON array of all channels
  - Response: [
      {
        "id": 1,
        "channel_url": "https://www.youtube.com/@channelname",
        "channel_id": "UCXX...",
        "channel_name": "Channel Name",
        "status": "active",
        "last_video_title": "Video Title",
        "last_video_views": 12345,
        "last_checked": "2024-02-12T10:30:00",
        "created_at": "2024-02-12T10:00:00",
        "updated_at": "2024-02-12T10:30:00"
      }
    ]

POST /api/channels/add
  - Auth: Required (session)
  - Body: {"url": "https://www.youtube.com/@channelname"}
  - Returns: {"success": true, "id": 1, "channel_name": "...", "status": "..."}

POST /api/channels/<id>/remove
  - Auth: Required (session)
  - Returns: {"success": true}

POST /api/channels/<id>/check
  - Auth: Required (session)
  - Returns: Channel status with latest video info
  - Response: {
      "success": true,
      "channel_id": 1,
      "accessible": true,
      "channel_name": "Channel Name",
      "status": "active",
      "latest_video_title": "Video Title",
      "latest_video_views": 12345,
      "latest_video_url": "https://www.youtube.com/watch?v=XXX"
    }
```

## Database Schema

### Channels Table
```sql
CREATE TABLE channels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_url TEXT UNIQUE NOT NULL,
    channel_id TEXT,
    channel_name TEXT,
    status TEXT DEFAULT 'unknown',  -- 'active', 'inactive', 'pending', 'unknown'
    last_video_title TEXT,
    last_video_views INTEGER DEFAULT 0,
    last_checked TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## YouTube URL Formats Supported

The system handles multiple YouTube URL formats:

```
1. Custom Handle (Modern)
   https://www.youtube.com/@channelhandle
   Extracted: @channelhandle

2. Channel ID (Direct Access)
   https://www.youtube.com/channel/UCXXXXXXXXXXXXXXXXXXXXXXXXXX
   Extracted: UCXXXXXXXXXXXXXXXXXXXXXXXXXX

3. Legacy Username
   https://www.youtube.com/user/username
   Extracted: username

4. Short URL
   https://youtu.be/XXXXX
   Extracted: Video ID (not channel)
```

## Video Filtering Logic

The system implements smart filtering:

```python
# Shorts Detection
def is_short_video(duration_str):
    # Parse ISO 8601 duration: PT1H2M3S
    # If total_seconds <= 60: YouTube Short
    # Otherwise: Regular video
    return total_seconds <= 60

# Video Selection
for video in channel_uploads:
    if not is_short_video(video.duration):
        # This is a regular video, use it
        return video
```

## Status Codes

### Channel Status Values
- `active`: Channel accessible, videos available
- `inactive`: Channel not found or deleted  
- `pending`: Initial state before first check
- `unknown`: Error checking status

### API Response Status
- `200 OK`: Request successful
- `201 Created`: Resource created
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Not authenticated
- `404 Not Found`: Resource not found
- `500 Server Error`: Internal server error

## Rate Limiting & Quotas

### YouTube API
- Daily quota limit (default 10,000 units)
- Each videos.list call = ~1 unit
- Each channels.list call = ~1 unit
- Quota resets at 00:00 PST

### Telegram API
- Rate limit: 30 messages per second per bot
- No daily limit for media files

## Configuration Environment Variables

```env
# Telegram Configuration
TELEGRAM_BOT_TOKEN      # Bot token from BotFather
TELEGRAM_CHAT_ID        # Target chat/group ID

# YouTube Configuration  
YOUTUBE_API_KEY         # API key from Google Cloud

# Flask Configuration
FLASK_PORT              # Web server port (default: 5000)
FLASK_HOST              # Web server host (default: 0.0.0.0)

# Security
WEB_UI_SECRET           # Web UI password (change this!)
```

## Error Handling

### Common Errors

```
YouTube API
└─ 404 Not Found: Channel doesn't exist
└─ 403 Forbidden: API key invalid or quota exceeded
└─ 401 Unauthorized: Invalid credentials
└─ 400 Bad Request: Invalid parameters

Telegram API
└─ 400 Bad Request: Invalid message format
└─ 401 Unauthorized: Invalid token
└─ 429 Too Many Requests: Rate limited

Database
└─ IntegrityError: Duplicate channel URL
└─ OperationalError: Database locked
└─ DatabaseError: Corruption or permission issue
```

## Performance Considerations

### Channel Status Check
- Network request: ~2-3 seconds
- API calls: ~3-5 seconds (multiple API requests)
- Database update: <100ms
- Total: ~5-10 seconds per channel

### Web Dashboard Load
- Initial page load: 100-200ms
- Channel list fetch: 50-100ms  
- Auto-refresh (5 min interval): Minimal overhead

### Bot Command Response
- /status on 10 channels: ~60 seconds
- /list: <1 second
- /start: <1 second

## Security Considerations

1. **Authentication**: Simple password-based
   - Change default `WEB_UI_SECRET`
   - Use HTTPS in production

2. **API Keys**: Stored in `.env`
   - Never commit to version control
   - Rotate keys regularly
   - Use environment variables only

3. **Database**: SQLite
   - No password protection
   - File-based storage
   - Backup regularly

4. **Telegram**: Token security
   - Keep token private
   - Regenerate if compromised
   - Use in production environment only

## Deployment Considerations

### Linux/Mac with PM2
```bash
npm install -g pm2
pm2 start app.py --name youtube-web
pm2 start bot.py --name youtube-bot
pm2 save
```

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1
CMD ["python", "app.py"]
```

### Systemd Service (Linux)
```ini
[Unit]
Description=YouTube Monitor Bot
After=network.target

[Service]
Type=simple
User=nobody
WorkingDirectory=/opt/youtube-monitor
ExecStart=/usr/bin/python3 /opt/youtube-monitor/bot.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

---

For more information, see [README.md](README.md) and [QUICKSTART.md](QUICKSTART.md)
