import yt_dlp
import os
import re
from urllib.parse import urlparse, parse_qs
import logging

def clean_url(url):
    """Convert any YouTube URL format to channel URL."""
    if not url:
        return None
        
    # Handle channel URLs
    patterns = {
        'channel': r'youtube.com/channel/',
        'user': r'youtube.com/user/',
        'custom': r'youtube.com/c/',
        'handle': r'youtube.com/@'
    }
    
    for pattern in patterns.values():
        if pattern in url:
            return url.split('?')[0]  # Remove any query parameters
            
    # Handle video URLs - extract channel from video
    if 'youtube.com/watch' in url:
        return url
        
    # Handle playlist URLs
    if 'youtube.com/playlist' in url:
        return url
        
    return url

def get_all_videos(channel_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
        'ignoreerrors': True,
        'no_warnings': True,
        'playlistend': 5000  # Limit to prevent timeout on huge channels
    }

    all_videos = []
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Clean and verify URL
            cleaned_url = clean_url(channel_url)
            if not cleaned_url:
                logging.info("Invalid URL format")
                return None, None

            try:
                result = ydl.extract_info(cleaned_url, download=False)
            except Exception as e:
                logging.info(f"Error accessing URL: {str(e)}")
                return None, None

            if not result:
                logging.info("Could not fetch channel information")
                return None, None

            # Handle different types of responses
            if 'entries' in result:
                channel_name = result.get('title', 'Unknown_Channel')
                entries = result['entries']
                
                # Filter out None entries and extend the list
                all_videos.extend([entry for entry in entries if entry is not None])
                
                # Handle pagination
                while result and 'entries' in result and '_next' in result:
                    try:
                        result = ydl.extract_info(result['_next'], download=False)
                        if result and 'entries' in result:
                            all_videos.extend([entry for entry in result['entries'] if entry is not None])
                    except Exception as e:
                        logging.info(f"Error fetching more videos: {str(e)}")
                        break
                
                # Create video links dictionary with error handling
                video_links = {}
                for index, video in enumerate(all_videos, 1):
                    if video and isinstance(video, dict):
                        title = video.get('title', 'Untitled Video')
                        url = video.get('url', video.get('id', ''))
                        if url:  # Only add if we have a URL
                            video_links[index] = (title, url)
                
                if video_links:
                    return video_links, channel_name
                else:
                    logging.info("No valid videos found in channel")
            else:
                logging.info("This URL doesn't contain a playlist of videos")
                
    except Exception as e:
        logging.info(f"Error processing channel: {str(e)}")
    
    return None, None

def format_video_url(url):
    """Format video URL correctly."""
    if not url:
        return None
    
    # Handle already formatted URLs
    if url.startswith(("https://", "http://")):
        return url
        
    # Handle shorts
    if "/shorts/" in url:
        return f"https://www.youtube.com{url}"
        
    # Handle video IDs
    if not url.startswith(('https://', 'http://', '/')):
        return f"https://www.youtube.com/watch?v={url}"
        
    return url