import os
import re
import sys
import yt_dlp

urls = [
    ("https://youtube.com/playlist?list=RDLRJo0fxoHHs&playnext=1&si=qu2cMM47i7Rt25OZ", "playlist"),
    ("https://youtu.be/z720peSmYSQ?si=bXB_DSipqwwE9BAm", "video"),
    ("https://youtu.be/pjRR_-BHces?si=zK9_K1S6tn5V-7I5", "video"),
    ("https://youtu.be/2pRdvJF1rCY?si=8eevsToBbW8-Y9T4", "video"),
    ("https://youtube.com/playlist?list=RDinDEsr8UuWQ&playnext=1&si=ZKMsx2eAeiiH3Pam", "playlist"),
    ("https://youtu.be/2CE1i-l3xaI?si=BBUN4OeBin8AVdUF", "video")
]

def clean_filename(name):
    # Hapus karakter yang tidak diperbolehkan di nama folder Windows
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

def progress_hook(d):
    status = d.get("status")
    if status == "downloading":
        filename = os.path.basename(d.get("filename", ""))
        downloaded = d.get("downloaded_bytes", 0)
        total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
        speed = d.get("speed", 0) or 0
        eta = d.get("eta", 0) or 0

        if total > 0:
            pct = downloaded / total * 100
            speed_kb = speed / 1024
            try:
                print(f"\r  [{pct:5.1f}%] {filename[:40]:<40} {speed_kb:6.1f} KB/s ETA {eta}s", end="", flush=True)
            except Exception:
                print(f"\r  [{pct:5.1f}%] downloading... {speed_kb:6.1f} KB/s ETA {eta}s", end="", flush=True)
    elif status == "finished":
        fname = os.path.basename(d.get('filename', ''))
        try:
            print(f"\n  [OK] Selesai download: {fname}")
        except Exception:
            print(f"\n  [OK] Selesai download")

def download_link(url, type_):
    print(f"\n==================================================")
    print(f"Menganalisa: {url}")
    
    # 1. Dapatkan Judul untuk Folder
    ydl_opts_info = {
        'extract_flat': True,
        'skip_download': True,
    }
    
    title = "Unknown"
    with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown')
        except Exception as e:
            print(f"Gagal menganalisa judul: {e}")
            title = "Download_" + re.sub(r'\W+', '_', url[-10:])
            
    folder_name = clean_filename(title)
    output_dir = os.path.join("F:\\lagu", folder_name)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Judul/Folder: {folder_name}")
    print(f"Lokasi Save : {output_dir}")
    print(f"Tipe        : {type_}")
    print(f"==================================================")
    
    # 2. Config options untuk Download
    if type_ == "playlist":
        outtmpl = os.path.join(output_dir, "%(playlist_index)03d - %(title)s.%(ext)s")
    else:
        outtmpl = os.path.join(output_dir, "%(title)s.%(ext)s")
        
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "ignoreerrors": True,
        "no_warnings": False,
        "progress_hooks": [progress_hook],
        "noplaylist": True if type_ == "video" else False,
        "concurrent_fragment_downloads": 4,
        "retries": 5,
        "fragment_retries": 5,
        "skip_unavailable_fragments": True,
        "nooverwrites": True,
        "continue_dl": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            },
            {"key": "FFmpegMetadata"}
        ]
    }
    
    # Batasi 50 teratas jika ini playlist Mix (biasanya mengandung list=RD di URL)
    if type_ == "playlist" and "list=RD" in url:
        print("Playlist Mix terdeteksi. Membatasi ke 50 lagu teratas...")
        ydl_opts["playlist_items"] = "1-50"
        
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():
    print("Memulai Batch Download ke Drive F:\\lagu...")
    for idx, (url, type_) in enumerate(urls, 1):
        print(f"\nProcessing Link {idx}/{len(urls)}")
        try:
            download_link(url, type_)
        except Exception as e:
            print(f"Gagal mendownload link ke-{idx}: {e}")
            
    print("\n[OK] Semua proses download batch selesai!")

if __name__ == "__main__":
    main()
