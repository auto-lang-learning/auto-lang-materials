from flask import Flask, request, jsonify
from download_video import download_video
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
proxy=os.getenv('PROXY')

@app.route('/download_subtitles', methods=['POST'])
def download_subtitles():
    data = request.json
    video_url = data.get('video_url')
    language = data.get('language', 'en')

    # Download the video
    video_path = download_video(video_url, 'downloads')

 
    return video_path

if __name__ == '__main__':
    app.run(debug=True)
