import yt_dlp
import os
import time

def download_video(url, output_path, cookies_path=None, retries=0):
    # 创建输出目录（如果不存在）
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    ydl_opts = {
        'outtmpl': output_path,  # 输出文件路径
        'format': 'best',  # 下载最佳格式
        'retries': retries,  # 重试次数
    }

    if cookies_path:
        ydl_opts['cookies'] = cookies_path  # 使用 cookies 文件

    for attempt in range(retries):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            break  # 成功下载后退出循环
        except yt_dlp.utils.DownloadError as e:
            print(f"下载失败，重试 {attempt + 1}/{retries} 次...")
            time.sleep(5)  # 等待一段时间后重试
    else:
        print("下载失败，请检查网络连接或URL是否正确。")

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=tRxB5k3HnFY&list=PLr_tnA_jkyAHirt7FBlq2crn3anmaZzCE&index=21"
    output_path = "videos/video1.mp4"  # 确保包含文件名和扩展名
    cookies_path = "dependencies/youtube.json"  # 替换为实际的 cookies 文件路径
    download_video(video_url, output_path, cookies_path)


# from pytube import YouTube
# from pathlib import Path
# import sys

# def download_youtube_video(url, output_path="."):
#     try:
#         # 创建YouTube对象
#         yt = YouTube(url)
        
#         # 获取最高分辨率的渐进式流（包含音频+视频）
#         stream = yt.streams.filter(
#             progressive=True,
#             file_extension='mp4'
#         ).order_by('resolution').desc().first()
        
#         if not stream:
#             print("未找到符合条件的视频流")
#             return

#         # 确保输出目录存在
#         output_dir = Path(output_path)
#         output_dir.mkdir(parents=True, exist_ok=True)
        
#         # 下载视频
#         print(f"正在下载: {yt.title} [{stream.resolution}]...")
#         stream.download(output_path=output_path)
#         print("下载完成！保存至:", output_dir.resolve() / stream.default_filename)
        
#     except Exception as e:
#         print(f"下载失败: {str(e)}")

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("使用方法: python youtube_downloader.py <视频URL> [输出目录]")
#         sys.exit(1)
    
#     url = sys.argv[1]
#     output_path = sys.argv[2] if len(sys.argv) > 2 else "."
    
#     download_youtube_video("https://www.youtube.com/watch?v=NZITlyMfLCM&list=PLr_tnA_jkyAHirt7FBlq2crn3anmaZzCE", "videos")


