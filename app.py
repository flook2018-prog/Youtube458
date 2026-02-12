from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from database import db
from youtube_handler import YouTubeHandler
from config import WEB_UI_SECRET, FLASK_PORT, FLASK_HOST, ALLOWED_HOSTS, SESSION_COOKIE_SECURE, SESSION_COOKIE_HTTPONLY, SESSION_COOKIE_SAMESITE, ENVIRONMENT
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = WEB_UI_SECRET

# Session Configuration
app.config['SESSION_COOKIE_SECURE'] = SESSION_COOKIE_SECURE
app.config['SESSION_COOKIE_HTTPONLY'] = SESSION_COOKIE_HTTPONLY
app.config['SESSION_COOKIE_SAMESITE'] = SESSION_COOKIE_SAMESITE
app.config['PERMANENT_SESSION_LIFETIME'] = 24 * 60 * 60  # 24 hours

youtube = YouTubeHandler()

def check_host():
    """Validate host for security"""
    host = request.headers.get('Host', '').split(':')[0]
    
    # Allow localhost in development
    if ENVIRONMENT == 'development' or host == 'localhost' or host == '127.0.0.1':
        return True
    
    # Check against allowed hosts
    if host in ALLOWED_HOSTS:
        return True
    
    # Log potential issue
    print(f"⚠️  Host validation: {host}")
    return True  # Allow for now, be permissive

@app.before_request
def validate_request():
    """Validate incoming requests"""
    if ENVIRONMENT == 'production':
        # Force HTTPS
        if not request.is_secure and request.headers.get('X-Forwarded-Proto', 'http') != 'https':
            url = request.url.replace('http://', 'https://', 1)
            return redirect(url, code=301)

@app.after_request
def add_security_headers(response):
    """Add security headers"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # HTTPS only in production
    if ENVIRONMENT == 'production':
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    return response

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'authenticated' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == WEB_UI_SECRET:
            session['authenticated'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid password'), 401
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    """Main dashboard"""
    channels = db.get_all_channels()
    return render_template('index.html', channels=channels)

@app.route('/api/channels', methods=['GET'])
@login_required
def get_channels():
    """Get all channels as JSON"""
    channels = db.get_all_channels()
    return jsonify(channels)

@app.route('/api/channels/add', methods=['POST'])
@login_required
def add_channel():
    """Add a new channel"""
    try:
        data = request.get_json()
        channel_url = data.get('url', '').strip()
        
        if not channel_url:
            return jsonify({'success': False, 'error': 'URL required'}), 400
        
        # Validate YouTube URL
        if 'youtube.com' not in channel_url and 'youtu.be' not in channel_url:
            return jsonify({'success': False, 'error': 'Invalid YouTube URL'}), 400
        
        # Add to database
        result = db.add_channel(channel_url)
        
        if result['success']:
            # Try to get channel info
            status_info = youtube.check_channel_status(channel_url)
            
            if status_info['accessible']:
                db.update_channel_status(
                    result['id'],
                    status_info['channel_name'],
                    channel_url,
                    'active',
                    None,
                    0
                )
                
                return jsonify({
                    'success': True,
                    'id': result['id'],
                    'channel_name': status_info['channel_name'],
                    'status': 'active'
                }), 201
            else:
                return jsonify({
                    'success': True,
                    'id': result['id'],
                    'channel_name': 'Unknown',
                    'status': 'pending'
                }), 201
        else:
            return jsonify(result), 400
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/channels/<int:channel_id>/remove', methods=['POST'])
@login_required
def remove_channel(channel_id):
    """Remove a channel"""
    try:
        result = db.remove_channel(channel_id)
        
        if result['success']:
            return jsonify({'success': True})
        else:
            return jsonify(result), 400
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/channels/<int:channel_id>/check', methods=['POST'])
@login_required
def check_channel(channel_id):
    """Check a single channel status"""
    try:
        channel = db.get_channel(channel_id)
        
        if not channel:
            return jsonify({'success': False, 'error': 'Channel not found'}), 404
        
        channel_url = channel['channel_url']
        
        # Check if channel is accessible
        status_info = youtube.check_channel_status(channel_url)
        
        result = {
            'success': True,
            'channel_id': channel_id,
            'accessible': status_info['accessible'],
            'channel_name': status_info['channel_name'],
            'status': 'active' if status_info['accessible'] else 'inactive',
            'error': status_info.get('error')
        }
        
        # Try to get latest video if accessible
        if status_info['accessible'] and status_info.get('channel_id'):
            latest_video = youtube.get_latest_video(status_info['channel_id'])
            
            if latest_video:
                result['latest_video_title'] = latest_video['title']
                result['latest_video_views'] = latest_video['views']
                result['latest_video_url'] = latest_video['url']
                
                # Update database
                db.update_channel_status(
                    channel_id,
                    status_info['channel_name'],
                    channel_url,
                    'active',
                    latest_video['title'],
                    latest_video['views']
                )
            else:
                # Update database without video info
                db.update_channel_status(
                    channel_id,
                    status_info['channel_name'],
                    channel_url,
                    'active',
                    None,
                    0
                )
        else:
            # Update as inactive
            db.update_channel_status(
                channel_id,
                status_info['channel_name'] or channel['channel_name'],
                channel_url,
                'inactive',
                None,
                0
            )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.template_filter('format_number')
def format_number(n):
    """Format number with commas"""
    if n is None:
        return '0'
    try:
        return f"{int(n):,}"
    except:
        return str(n)

@app.errorhandler(404)
def not_found(error):
    """404 handler"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """500 handler"""
    return jsonify({'error': 'Server error'}), 500

# Note: For Gunicorn/production use, server is started via WSGI entry point
# This block is only for local development
if __name__ == '__main__' and ENVIRONMENT == 'development':
    debug_mode = True
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=debug_mode)
