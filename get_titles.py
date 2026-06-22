import yt_dlp
import sys
import re

urls = [
    "https://youtube.com/playlist?list=RDLRJo0fxoHHs&playnext=1&si=qu2cMM47i7Rt25OZ",
    "https://youtu.be/z720peSmYSQ?si=bXB_DSipqwwE9BAm",
    "https://youtu.be/pjRR_-BHces?si=zK9_K1S6tn5V-7I5",
    "https://youtu.be/2pRdvJF1rCY?si=8eevsToBbW8-Y9T4",
    "https://youtube.com/playlist?list=RDinDEsr8UuWQ&playnext=1&si=ZKMsx2eAeiiH3Pam",
    "https://youtu.be/2CE1i-l3xaI?si=BBUN4OeBin8AVdUF"
]

ydl_opts = {
    'extract_flat': True,
    'skip_download': True,
}

def clean_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    for url in urls:
        try:
            info = ydl.extract_info(url, download=False)
            title = info.get('title')
            print(f"URL: {url} -> Title: {title} (Type: {info.get('_type', 'video')})")
        except Exception as e:
            print(f"URL: {url} -> Error: {e}")
