import sqlite3
import json
from datetime import datetime
from config import DATABASE_PATH

class Database:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.init_db()
    
    def init_db(self):
        """Initialize the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_url TEXT UNIQUE NOT NULL,
                channel_id TEXT,
                channel_name TEXT,
                status TEXT DEFAULT 'unknown',
                last_video_title TEXT,
                last_video_views INTEGER DEFAULT 0,
                last_checked TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_channel(self, channel_url):
        """Add a new channel"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO channels (channel_url, status, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            ''', (channel_url, 'pending', datetime.now(), datetime.now()))
            
            conn.commit()
            channel_id = cursor.lastrowid
            conn.close()
            
            return {'success': True, 'id': channel_id}
        except sqlite3.IntegrityError:
            return {'success': False, 'error': 'Channel already exists'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def remove_channel(self, channel_id):
        """Remove a channel"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM channels WHERE id = ?', (channel_id,))
            
            conn.commit()
            conn.close()
            
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_all_channels(self):
        """Get all channels"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM channels ORDER BY created_at DESC')
            channels = [dict(row) for row in cursor.fetchall()]
            
            conn.close()
            
            return channels
        except Exception as e:
            return []
    
    def get_channel(self, channel_id):
        """Get a specific channel"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM channels WHERE id = ?', (channel_id,))
            channel = cursor.fetchone()
            
            conn.close()
            
            return dict(channel) if channel else None
        except Exception as e:
            return None
    
    def update_channel_status(self, channel_id, channel_name, channel_url, status, last_video_title, last_video_views):
        """Update channel status and video info"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE channels 
                SET channel_name = ?, status = ?, last_video_title = ?, 
                    last_video_views = ?, last_checked = ?, updated_at = ?,
                    channel_url = ?
                WHERE id = ?
            ''', (channel_name, status, last_video_title, last_video_views, 
                  datetime.now(), datetime.now(), channel_url, channel_id))
            
            conn.commit()
            conn.close()
            
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}

# Initialize database
db = Database()
