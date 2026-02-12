import requests
from urllib.parse import urlparse, parse_qs
import re
from config import YOUTUBE_API_KEY

class YouTubeHandler:
    def __init__(self):
        self.api_key = YOUTUBE_API_KEY
        self.base_url = 'https://www.googleapis.com/youtube/v3'
    
    def extract_channel_id_from_url(self, channel_url):
        """Extract channel ID or handle from YouTube URL"""
        try:
            # Handle @username format (custom URLs)
            if '@' in channel_url:
                handle = channel_url.split('@')[-1].split('?')[0]
                return self.get_channel_id_from_handle(handle)
            
            # Handle /channel/CHANNELID format
            if '/channel/' in channel_url:
                channel_id = channel_url.split('/channel/')[-1].split('?')[0]
                return channel_id
            
            # If it's just a URL, try to figure it out
            parsed = urlparse(channel_url)
            path = parsed.path
            
            if '/channel/' in path:
                return path.split('/channel/')[-1].split('?')[0]
            elif '/user/' in path:
                username = path.split('/user/')[-1].split('?')[0]
                return self.get_channel_id_from_username(username)
        except Exception as e:
            print(f"Error extracting channel ID: {e}")
        
        return None
    
    def get_channel_id_from_handle(self, handle):
        """Get channel ID from @handle using YouTube search API"""
        if not self.api_key:
            return None
        
        try:
            response = requests.get(f'{self.base_url}/search', params={
                'key': self.api_key,
                'q': f'@{handle}',
                'type': 'channel',
                'part': 'snippet',
                'maxResults': 1
            }, timeout=5)
            
            if response.status_code == 200 and response.json().get('items'):
                return response.json()['items'][0]['id']['channelId']
        except Exception as e:
            print(f"Error getting channel ID from handle: {e}")
        
        return None
    
    def get_channel_id_from_username(self, username):
        """Get channel ID from username"""
        if not self.api_key:
            return None
        
        try:
            response = requests.get(f'{self.base_url}/channels', params={
                'key': self.api_key,
                'forUsername': username,
                'part': 'id'
            }, timeout=5)
            
            if response.status_code == 200 and response.json().get('items'):
                return response.json()['items'][0]['id']
        except Exception as e:
            print(f"Error getting channel ID from username: {e}")
        
        return None
    
    def check_channel_status(self, channel_url):
        """
        Check if channel exists and get channel info
        Returns: {
            'accessible': bool,
            'channel_name': str,
            'channel_id': str,
            'error': str (if any)
        }
        """
        try:
            # Check if URL is accessible
            response = requests.head(channel_url, allow_redirects=True, timeout=5)
            
            if response.status_code == 404 or 'not found' in response.text.lower():
                return {
                    'accessible': False,
                    'channel_name': None,
                    'channel_id': None,
                    'error': 'Channel not found (404)'
                }
            
            if response.status_code != 200:
                return {
                    'accessible': False,
                    'channel_name': None,
                    'channel_id': None,
                    'error': f'HTTP {response.status_code}'
                }
            
            # Get full page to extract channel name
            response = requests.get(channel_url, timeout=5)
            
            if response.status_code == 200:
                # Extract channel name from page title or metadata
                channel_name = self.extract_channel_name(response.text, channel_url)
                channel_id = self.extract_channel_id_from_url(channel_url)
                
                return {
                    'accessible': True,
                    'channel_name': channel_name,
                    'channel_id': channel_id
                }
            else:
                return {
                    'accessible': False,
                    'channel_name': None,
                    'channel_id': None,
                    'error': f'HTTP {response.status_code}'
                }
        except requests.exceptions.RequestException as e:
            return {
                'accessible': False,
                'channel_name': None,
                'channel_id': None,
                'error': str(e)
            }
    
    def extract_channel_name(self, html_content, channel_url):
        """Extract channel name from HTML content"""
        try:
            # Try to find channel name in meta tags
            name_match = re.search(r'<meta\s+property=["\']og:title["\']\s+content=["\']([^"\']+)["\']', html_content)
            if name_match:
                return name_match.group(1).strip()
            
            # Try title tag
            title_match = re.search(r'<title>([^<]+)</title>', html_content)
            if title_match:
                title = title_match.group(1).strip()
                # Remove " - YouTube" suffix
                if ' - YouTube' in title:
                    return title.replace(' - YouTube', '').strip()
                return title
        except Exception as e:
            print(f"Error extracting channel name: {e}")
        
        return channel_url.split('@')[-1] if '@' in channel_url else 'Unknown'
    
    def get_latest_video(self, channel_id):
        """
        Get latest video from channel (excluding shorts)
        Returns: {
            'title': str,
            'views': int,
            'video_id': str,
            'url': str
        }
        """
        if not self.api_key or not channel_id:
            return None
        
        try:
            # Get uploads playlist ID for the channel
            channel_resp = requests.get(f'{self.base_url}/channels', params={
                'key': self.api_key,
                'id': channel_id,
                'part': 'contentDetails'
            }, timeout=10)
            
            if channel_resp.status_code != 200 or not channel_resp.json().get('items'):
                return None
            
            uploads_playlist_id = channel_resp.json()['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # Get videos from uploads playlist
            videos_resp = requests.get(f'{self.base_url}/playlistItems', params={
                'key': self.api_key,
                'playlistId': uploads_playlist_id,
                'part': 'contentDetails',
                'maxResults': 50
            }, timeout=10)
            
            if videos_resp.status_code != 200 or not videos_resp.json().get('items'):
                return None
            
            # Get video details to filter out shorts
            video_ids = [item['contentDetails']['videoId'] for item in videos_resp.json()['items']]
            
            for video_id in video_ids:
                video_detail_resp = requests.get(f'{self.base_url}/videos', params={
                    'key': self.api_key,
                    'id': video_id,
                    'part': 'snippet,statistics,contentDetails'
                }, timeout=10)
                
                if video_detail_resp.status_code != 200:
                    continue
                
                items = video_detail_resp.json().get('items', [])
                if not items:
                    continue
                
                video = items[0]
                
                # Check if it's a short (duration <= 60 seconds)
                duration = video['contentDetails']['duration']
                # Parse ISO 8601 duration
                is_short = self.is_short_video(duration)
                
                if not is_short:
                    return {
                        'title': video['snippet']['title'],
                        'views': int(video['statistics'].get('viewCount', 0)),
                        'video_id': video_id,
                        'url': f'https://www.youtube.com/watch?v={video_id}'
                    }
        
        except Exception as e:
            print(f"Error getting latest video: {e}")
        
        return None
    
    def is_short_video(self, duration_str):
        """Check if video duration is <= 60 seconds (YouTube Shorts)"""
        try:
            # Duration format: PT1H2M3S
            import re
            pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
            match = re.match(pattern, duration_str)
            
            if not match:
                return False
            
            hours = int(match.group(1)) if match.group(1) else 0
            minutes = int(match.group(2)) if match.group(2) else 0
            seconds = int(match.group(3)) if match.group(3) else 0
            
            total_seconds = hours * 3600 + minutes * 60 + seconds
            
            return total_seconds <= 60
        except:
            return False
