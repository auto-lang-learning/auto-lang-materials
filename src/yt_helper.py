import yt_dlp
import os
import re
import time 
from io import StringIO
import json

def get_subtitle(url,cookies_path=None, retries=3, proxy=None,subtitlesformat='vtt',
                   language='en'):
    
    temp_dir = os.path.join(os.getcwd(), 'temp')
    os.makedirs(temp_dir, exist_ok=True)

    ydl_opts = {
        'retries': retries,  # Number of retries
        'proxy': proxy,  # Proxy setting
        'writesubtitles': True,
        'skip_download': True,
        'outtmpl': os.path.join(temp_dir, '%(id)s.%(ext)s'),  # Save subtitles to temp directory
        'subtitlesformat': subtitlesformat,
        'subtitleslangs': [language],
    }

    if cookies_path:
        ydl_opts['cookies'] = cookies_path  # Use cookies file

    for attempt in range(retries):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get video information
                info_dict = ydl.extract_info(url, download=True) 
                subtitle_content = StringIO()
                if language not in info_dict['subtitles']:
                    return f"No subtitles found for language :{language}"
                if subtitlesformat not in [fmt['ext'] for fmt in info_dict['subtitles'][language]]:
                    return f"No subtitles found in {subtitlesformat} format for the language :{language}"
                with open(os.path.join(temp_dir, f"{info_dict['id']}.{language}.{subtitlesformat}"), 'r') as f:
                    subtitle_content.write(f.read())
                
                subtitle_content.seek(0)
                return subtitle_content.getvalue()

            break  
        except yt_dlp.utils.DownloadError as e:
            print(f"Download failed, retrying {attempt + 1}/{retries} times...")
            time.sleep(3) 
    else:
        print("Download failed, please check network connection or the URL.")



if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=iAplA7l1am0"
    output_dir = "downloads"  
    cookies_path = "path/to/your/cookies.txt"  
    