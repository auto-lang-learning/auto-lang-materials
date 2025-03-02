import requests
import json

# JSON array with file details
file_details = [
    {
        "ext": "json3",
        "name": "Russian",
        "url": "https://www.youtube.com/api/timedtext?v=pDn95P8hhkc&ei=ftO1Z8DUGbPW2roP-9i_iA0&caps=asr&opi=112496729&xoaf=5&hl=en&ip=0.0.0.0&ipbits=0&expire=1739994606&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=5336A2656E084CBA5F461DA5AD5FBB70C6CF3BB8.233EF80824C505275D3D9EBF14DFB5F1698C45D6&key=yt8&lang=ru&fmt=json3"
    },
    {
        "ext": "srv1",
        "name": "Russian",
        "url": "https://www.youtube.com/api/timedtext?v=pDn95P8hhkc&ei=ftO1Z8DUGbPW2roP-9i_iA0&caps=asr&opi=112496729&xoaf=5&hl=en&ip=0.0.0.0&ipbits=0&expire=1739994606&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=5336A2656E084CBA5F461DA5AD5FBB70C6CF3BB8.233EF80824C505275D3D9EBF14DFB5F1698C45D6&key=yt8&lang=ru&fmt=srv1"
    },
    {
        "ext": "srv2",
        "name": "Russian",
        "url": "https://www.youtube.com/api/timedtext?v=pDn95P8hhkc&ei=ftO1Z8DUGbPW2roP-9i_iA0&caps=asr&opi=112496729&xoaf=5&hl=en&ip=0.0.0.0&ipbits=0&expire=1739994606&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=5336A2656E084CBA5F461DA5AD5FBB70C6CF3BB8.233EF80824C505275D3D9EBF14DFB5F1698C45D6&key=yt8&lang=ru&fmt=srv2"
    },
    {
        "ext": "srv3",
        "name": "Russian",
        "url": "https://www.youtube.com/api/timedtext?v=pDn95P8hhkc&ei=ftO1Z8DUGbPW2roP-9i_iA0&caps=asr&opi=112496729&xoaf=5&hl=en&ip=0.0.0.0&ipbits=0&expire=1739994606&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=5336A2656E084CBA5F461DA5AD5FBB70C6CF3BB8.233EF80824C505275D3D9EBF14DFB5F1698C45D6&key=yt8&lang=ru&fmt=srv3"
    },
    {
        "ext": "ttml",
        "name": "Russian",
        "url": "https://www.youtube.com/api/timedtext?v=pDn95P8hhkc&ei=ftO1Z8DUGbPW2roP-9i_iA0&caps=asr&opi=112496729&xoaf=5&hl=en&ip=0.0.0.0&ipbits=0&expire=1739994606&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=5336A2656E084CBA5F461DA5AD5FBB70C6CF3BB8.233EF80824C505275D3D9EBF14DFB5F1698C45D6&key=yt8&lang=ru&fmt=ttml"
    },
    {
        "ext": "vtt",
        "name": "Russian",
        "url": "https://www.youtube.com/api/timedtext?v=pDn95P8hhkc&ei=ftO1Z8DUGbPW2roP-9i_iA0&caps=asr&opi=112496729&xoaf=5&hl=en&ip=0.0.0.0&ipbits=0&expire=1739994606&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cei%2Ccaps%2Copi%2Cxoaf&signature=5336A2656E084CBA5F461DA5AD5FBB70C6CF3BB8.233EF80824C505275D3D9EBF14DFB5F1698C45D6&key=yt8&lang=ru&fmt=vtt"
    }
]

# Function to download and save files
def download_files(file_details):
    for file in file_details:
        response = requests.get(file["url"])
        if response.status_code == 200:
            file_name = f"{file['name']}.{file['ext']}"
            with open(file_name, "wb") as f:
                f.write(response.content)
            print(f"Downloaded and saved: {file_name}")
        else:
            print(f"Failed to download: {file['url']}")

# Download the files
download_files(file_details)
