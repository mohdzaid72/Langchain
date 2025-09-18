'''it download the transcript file into the local .vtt, then fatch it and converted into the single text'''


import yt_dlp
from pathlib import Path
import os

def download_subtitles(video_url, lang='en'):
    video_id = video_url.split("v=")[-1].split("&")[0]
    ydl_opts = {
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': [lang],
        'skip_download': True,
        'outtmpl': f'{video_id}.%(ext)s',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(video_url, download=True)
        return video_id

def vtt_to_text(vtt_path):
    lines = Path(vtt_path).read_text(encoding='utf-8').splitlines()
    text_lines = [line for line in lines if not line.startswith(('WEBVTT', '00:', '-->')) and line.strip()]
    return ' '.join(text_lines)

# 🔧 Replace with your target video URL
video_url = "https://www.youtube.com/watch?v=YbJOTdZBX1g"
lang = "en"  # ✅ Define language here

# Step 1: Download subtitles
video_id = download_subtitles(video_url, lang)

# Step 2: Convert .vtt to plain text
vtt_file = f"{video_id}.{lang}.vtt"
if os.path.exists(vtt_file):
    transcript = vtt_to_text(vtt_file)
    print("Transcript loaded successfully.\n")
    print(transcript[:500] + "...")
else:
    transcript = ""
    print("Transcript file not found.")

# ✅ Now `transcript` contains the full text