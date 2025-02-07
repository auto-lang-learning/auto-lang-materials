import yt_dlp
import os
import re
import time
import json

def download_video(url, output_dir, cookies_path=None, proxy=None, retries=3):
    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'format': 'best',  # 下载最佳格式
        'retries': retries,  # 重试次数
        'writesubtitles': True,  # 下载字幕
        'subtitleslangs': ['en'],  # 指定字幕语言
        'subtitlesformat': 'vtt',  # 指定字幕格式
        'proxy': proxy
    }

    if cookies_path:
        ydl_opts['cookies'] = cookies_path  # 使用 cookies 文件

    video_info = {
        'video_title': '',
        'video_path': '',  # 视频文件路径
        'subtitles_available': False
    }

    for attempt in range(retries):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # 获取视频信息
                info_dict = ydl.extract_info(url, download=False)
                video_title = info_dict.get('title', 'video')
                video_info['video_title'] = video_title
                # 设置输出文件路径
                output_path = os.path.join(output_dir, f"{video_title}.mp4")
                video_info['video_path'] = output_path
                ydl_opts['outtmpl'] = output_path
                # 重新创建 YoutubeDL 对象以应用新的 outtmpl
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # 检查是否包含字幕
                if info_dict.get('requested_subtitles'):
                    video_info['subtitles_available'] = True
                    # 获取字幕文件路径
                    subtitle_path = os.path.join(output_dir, f"{video_title}.en.vtt")
                    if os.path.exists(subtitle_path):
                        # 读取字幕文件并删除时间轴
                        with open(subtitle_path, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                        
                        text_lines = []
                        for line in lines:
                            if not re.match(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}', line):
                                text_lines.append(line.strip())
                        
                        # 保存纯文本文件
                        text_output_path = os.path.join(output_dir, f"{video_title}.txt")
                        with open(text_output_path, 'w', encoding='utf-8') as f:
                            f.write('\n'.join(text_lines))
                else:
                    print('No subtitles available.')
            break  # 成功下载后退出循环
        except yt_dlp.utils.DownloadError as e:
            print(f"下载失败，重试 {attempt + 1}/{retries} 次...")
            time.sleep(5)  # 等待一段时间后重试
    else:
        print("下载失败，请检查网络连接或URL是否正确。")

    # 保存视频信息到 JSON 文件
    save_video_info(output_dir, video_info)

def save_video_info(output_dir, video_info):
    json_output_path = os.path.join(output_dir, "output_result.json")
    if os.path.exists(json_output_path):
        with open(json_output_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
    else:
        data = []

    # 添加视频序号
    video_info_with_index = {str(len(data) + 1): video_info}
    data.append(video_info_with_index)

    with open(json_output_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=F_DfaUVa3Bs"
    output_dir = "videos"  # 确保这是一个目录
    cookies_path = "path/to/your/cookies.txt"  # 替换为实际的 cookies 文件路径
    proxy = os.environ.get("HTTP_PROXY")  # 从环境变量中获取代理设置
    download_video(video_url, output_dir, cookies_path, proxy)