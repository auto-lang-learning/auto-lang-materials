from flask import Flask, request, jsonify
from yt_helper import get_subtitle
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
proxy=os.getenv('HTTP_PROXY')
assert proxy is not None

@app.route('/download_subtitles', methods=['POST'])
def download_subtitles():
    data = request.json
    video_url = data.get('video_url')
    language=data.get('language')
    format=data.get('format')
   
    # Download the video
    subtitle = get_subtitle(video_url, 'downloads', proxy=proxy,language=language,subtitlesformat=format)
  
    return jsonify(subtitle)


if __name__ == '__main__':
    app.run(debug=True)
