#!/usr/bin/env python3
"""
Quick import script for adding sample YouTube channels
"""

from database import db

# Sample channels provided by the user
SAMPLE_CHANNELS = [
    "https://www.youtube.com/@JOJOCARTOON-p7p",
    "https://www.youtube.com/@Rasingcartoon",
    "https://www.youtube.com/@RonaldoNo1-j6j",
    "https://www.youtube.com/@Iconiccartoon-y5i",
    "https://www.youtube.com/@ilukpaaaa",
    "https://www.youtube.com/@Fibzy%E0%B8%88%E0%B8%B0%E0%B9%82%E0%B8%9A%E0%B8%99%E0%B8%9A%E0%B8%B4%E0%B8%99",
    "https://www.youtube.com/@XcghFs",
    "https://www.youtube.com/@Rolando7k-z9d",
    "https://www.youtube.com/@ttsundayxremix468",
    "https://www.youtube.com/@%E0%B8%84%E0%B8%99%E0%B8%95%E0%B8%B7%E0%B9%88%E0%B8%99%E0%B8%9A%E0%B8%B21",
    "https://www.youtube.com/@LyricsxThailand7",
]

def import_channels():
    """Import sample channels"""
    print("📥 Importing sample YouTube channels...")
    print()
    
    added_count = 0
    for channel_url in SAMPLE_CHANNELS:
        result = db.add_channel(channel_url)
        if result['success']:
            print(f"✅ Added: {channel_url}")
            added_count += 1
        else:
            print(f"⚠️  Already exists or error: {channel_url}")
    
    print()
    print(f"✅ Successfully added {added_count} channels!")
    print()
    print("Next steps:")
    print("1. Run: python app.py (in terminal 1)")
    print("2. Run: python bot.py (in terminal 2)")
    print("3. Open: http://localhost:5000")
    print("4. Click 'Check Now' to verify channels")

if __name__ == '__main__':
    import_channels()
