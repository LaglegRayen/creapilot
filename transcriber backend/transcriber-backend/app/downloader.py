from flask import current_app
import instaloader
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def download_reel(url):
    try:
        loader = instaloader.Instaloader()
        logging.info(f"Downloading Instagram Reel from URL: {url}")
        loader.download_post(instaloader.Post.from_shortcode(loader.context, url.split('/')[-2]), target='reel')
        
        video_file = [f for f in os.listdir('reel') if f.endswith('.mp4')]
        if not video_file:
            raise FileNotFoundError("No video file found after download.")
        
        video_path = os.path.join('reel', video_file[0])
        logging.info(f"Downloaded video file: {video_path}")
        return video_path
    except Exception as e:
        logging.error(f"Error downloading reel: {e}")
        current_app.logger.error(f"Error downloading reel: {e}")
        return None