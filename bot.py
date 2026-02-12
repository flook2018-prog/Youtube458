import logging
from telegram import Update, ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes
from database import db
from youtube_handler import YouTubeHandler
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

youtube = YouTubeHandler()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command"""
    await update.message.reply_text(
        "🎬 *YouTube Channel Monitor Bot*\n\n"
        "Commands:\n"
        "/status - Check status of all monitored channels\n"
        "/add <url> - Add a channel to monitor\n"
        "/list - List all monitored channels\n",
        parse_mode=ParseMode.MARKDOWN
    )

async def check_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check status of all channels"""
    try:
        await update.message.reply_text("🔄 Checking channel status...", parse_mode=ParseMode.MARKDOWN)
        
        channels = db.get_all_channels()
        
        if not channels:
            await update.message.reply_text("No channels monitored yet.")
            return
        
        message = "📊 *Channel Status Report*\n\n"
        
        for channel in channels:
            channel_url = channel['channel_url']
            channel_id = channel['id']
            
            # Check if channel is accessible
            status_info = youtube.check_channel_status(channel_url)
            
            if status_info['accessible']:
                channel_name = status_info['channel_name'] or channel['channel_name'] or 'Unknown'
                status_text = "✅ Active"
                
                # Try to get latest video info
                yt_channel_id = status_info['channel_id']
                if yt_channel_id:
                    latest_video = youtube.get_latest_video(yt_channel_id)
                    
                    if latest_video:
                        views = latest_video['views']
                        views_text = f"{views:,}" if views > 0 else "0"
                        message += (
                            f"{status_text} {channel_name}\n"
                            f"├─ Latest: {latest_video['title']}\n"
                            f"├─ Views: {views_text}\n"
                            f"└─ Link: {latest_video['url']}\n\n"
                        )
                    else:
                        message += f"{status_text} {channel_name}\n"
                        message += f"└─ No videos found\n\n"
                else:
                    message += f"{status_text} {channel_name}\n"
                    message += f"└─ (Could not fetch video info)\n\n"
                
                # Update database
                db.update_channel_status(
                    channel_id,
                    channel_name,
                    channel_url,
                    'active',
                    latest_video['title'] if latest_video else None,
                    latest_video['views'] if latest_video else 0
                )
            else:
                status_text = "❌ Inactive"
                channel_name = channel['channel_name'] or channel_url.split('@')[-1]
                message += f"{status_text} {channel_name}\n"
                message += f"└─ Error: {status_info.get('error', 'Unknown error')}\n\n"
                
                # Update database
                db.update_channel_status(
                    channel_id,
                    channel_name,
                    channel_url,
                    'inactive',
                    None,
                    0
                )
        
        # Split message if too long
        if len(message) > 4096:
            for i in range(0, len(message), 4096):
                await update.message.reply_text(message[i:i+4096], parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    
    except Exception as e:
        logger.error(f"Error checking status: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def list_channels(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List all monitored channels"""
    try:
        channels = db.get_all_channels()
        
        if not channels:
            await update.message.reply_text("No channels monitored yet.")
            return
        
        message = "*📺 Monitored Channels*\n\n"
        
        for i, channel in enumerate(channels, 1):
            channel_name = channel['channel_name'] or 'Unknown'
            status = channel['status'] or 'unknown'
            status_icon = "✅" if status == 'active' else "❌" if status == 'inactive' else "⏳"
            
            message += f"{i}. {status_icon} {channel_name}\n"
            message += f"   URL: {channel['channel_url']}\n"
            
            if channel['last_video_title']:
                message += f"   Last: {channel['last_video_title'][:50]}...\n"
                message += f"   Views: {channel['last_video_views']:,}\n"
            
            message += "\n"
        
        # Split message if too long
        if len(message) > 4096:
            for i in range(0, len(message), 4096):
                await update.message.reply_text(message[i:i+4096], parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    
    except Exception as e:
        logger.error(f"Error listing channels: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")

def run_bot():
    """Run the Telegram bot"""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set in environment")
        return
    
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", check_status))
    application.add_handler(CommandHandler("list", list_channels))
    
    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    run_bot()
