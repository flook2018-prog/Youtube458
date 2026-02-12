import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

# YouTube API
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', '')

# Database
DATABASE_PATH = 'channels.db'

# Flask
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_DEBUG = os.getenv('FLASK_ENV') == 'development'

# Web UI
WEB_UI_SECRET = os.getenv('WEB_UI_SECRET', 'mongodb2024')  # Default fallback

# Environment
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Production Domain
RAILWAY_DOMAIN = 'youtube458-production.up.railway.app'
CUSTOM_DOMAINS = os.getenv('CUSTOM_DOMAINS', '').split(',') if os.getenv('CUSTOM_DOMAINS') else []

# Allowed hosts for production
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    RAILWAY_DOMAIN,
    'youtube458-production-env.railway.app'
]
ALLOWED_HOSTS.extend(CUSTOM_DOMAINS)

# CORS Settings
CORS_ORIGINS = [
    'http://localhost:5000',
    'http://127.0.0.1:5000',
    f'https://{RAILWAY_DOMAIN}',
    'https://youtube458-production-env.railway.app'
]
CORS_ORIGINS.extend([f'https://{domain}' for domain in CUSTOM_DOMAINS])

# Security
SESSION_COOKIE_SECURE = ENVIRONMENT == 'production'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
