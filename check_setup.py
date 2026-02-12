#!/usr/bin/env python3
"""
Verify that all dependencies are installed and system is ready to run
"""

import sys

def check_dependencies():
    """Check if all required packages are installed"""
    
    print("🔍 Checking System Requirements...")
    print()
    
    dependencies = {
        'flask': 'Flask Web Framework',
        'telegram': 'Python Telegram Bot',
        'google.auth': 'Google Authentication',
        'google.oauth2': 'Google OAuth2',
        'googleapiclient': 'Google API Client',
        'requests': 'HTTP Requests Library',
        'dotenv': 'Environment Configuration'
    }
    
    missing = []
    installed = []
    
    for package, description in dependencies.items():
        try:
            __import__(package)
            installed.append(f"✅ {description} ({package})")
        except ImportError:
            missing.append(f"❌ {description} ({package})")
    
    # Print results
    print("INSTALLED PACKAGES:")
    for item in installed:
        print(f"  {item}")
    
    print()
    
    if missing:
        print("MISSING PACKAGES:")
        for item in missing:
            print(f"  {item}")
        print()
        print("⚠️  Run this to install dependencies:")
        print("  pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies are installed!")
        print()
        print("NEXT STEPS:")
        print("1. Configure .env file:")
        print("   cp .env.example .env")
        print("   # Edit .env with your tokens")
        print()
        print("2. Start the application:")
        print("   # Terminal 1:")
        print("   python app.py")
        print()
        print("   # Terminal 2:")
        print("   python bot.py")
        print()
        print("3. Open web UI:")
        print("   http://localhost:5000")
        print()
        return True

if __name__ == '__main__':
    success = check_dependencies()
    sys.exit(0 if success else 1)
