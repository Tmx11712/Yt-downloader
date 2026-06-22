import os
import re
import sys

import yt_dlp


try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


URLS = [
    ("https://youtube.com/playlist?list=RDLRJo0fxoHHs&playnext=1&si=qu2cMM47i7Rt25OZ", "playlist"),
    ("https://youtu.be/z720peSmYSQ?si=bXB_DSipqwwE9BAm", "video"),
    ("https://youtu.be/pjRR_-BHces?si=ZK9_K1S6tn5V-7I5", "video"),
    ("https://youtu.be/2pRdvJF1rCY?si=8eevsToBbW8-Y9T4", "video"),
    ("https://youtube.com/playlist?list=RDinDEsr8UuWQ&playnext=1&si=ZKMsx2eAeiiH3Pam", "playlist"),
    ("https://youtu.be/2CE1i-l3xaI?si=BBUN4OeBin8AVdUF", "video"),
]


def clean_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()


def final_mp3_exists(folder, prefix=None):
    if not os.path.isdir(folder):
        return False

    for name in os.listdir(folder):
        lower = name.lower()
        if not lower.endswith(".mp3") or lower.endswith(".temp.mp3"):
            continue
        if prefix is None or name.startswith(prefix):
            return True
    return False


def progress_hook(d):
    status = d.get("status")
    if status == "downloading":
        downloaded = d.get("downloaded_bytes") or 0
        total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
        if total:
            pct = downloaded / total * 100
            speed = (d.get("speed") or 0) / 1024
            eta = d.get("eta") or 0
            print(f"\r  {pct:5.1f}% | {speed:7.1f} KB/s | ETA {eta:4}s", end="", flush=True)
    elif status == "finished":
        print("\n  Download selesai, konversi ke MP3...")


def base_ydl_opts(outtmpl):
    return {
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "ignoreerrors": True,
        "no_warnings": False,
        "progress_hooks": [progress_hook],
        "noplaylist": True,
        "concurrent_fragment_downloads": 4,
        "retries": 10,
        "fragment_retries": 10,
        "continuedl": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            },
            {"key": "FFmpegMetadata"},
        ],
    }


def extract_info(url):
    with yt_dlp.YoutubeDL({"extract_flat": True, "skip_download": True, "quiet": True}) as ydl:
        return ydl.extract_info(url, download=False)


def download_video(url, folder, prefix=None):
    os.makedirs(folder, exist_ok=True)
    outtmpl = os.path.join(folder, f"{prefix} - %(title)s.%(ext)s" if prefix else "%(title)s.%(ext)s")
    with yt_dlp.YoutubeDL(base_ydl_opts(outtmpl)) as ydl:
        ydl.download([url])


def entry_url(entry):
    url = entry.get("url") or entry.get("webpage_url")
    if not url:
        return None
    if url.startswith("http"):
        return url
    return f"https://www.youtube.com/watch?v={url}"


def process_playlist(index, url):
    info = extract_info(url)
    title = clean_filename(info.get("title") or f"playlist_{index}")
    folder = os.path.join("F:\\lagu", title)
    entries = list(info.get("entries") or [])[:50]

    print(f"\nLink {index}/6 playlist: {title}")
    print(f"Target: {folder}")
    print("Batas: 50 lagu teratas")

    for item_index, entry in enumerate(entries, 1):
        prefix = f"{item_index:03d}"
        if final_mp3_exists(folder, prefix=f"{prefix} - "):
            print(f"  SKIP {prefix}: MP3 final sudah ada")
            continue

        url_to_download = entry_url(entry)
        if not url_to_download:
            print(f"  LEWAT {prefix}: URL tidak tersedia")
            continue

        title_hint = entry.get("title") or url_to_download
        print(f"  DOWNLOAD {prefix}: {title_hint}")
        download_video(url_to_download, folder, prefix=prefix)


def process_video(index, url):
    info = extract_info(url)
    title = clean_filename(info.get("title") or f"video_{index}")
    folder = os.path.join("F:\\lagu", title)

    print(f"\nLink {index}/6 video: {title}")
    print(f"Target: {folder}")

    if final_mp3_exists(folder):
        print("  SKIP: MP3 final sudah ada")
        return

    download_video(url, folder)


def main():
    print("Resume batch download ke F:\\lagu")
    for index, (url, kind) in enumerate(URLS, 1):
        try:
            if kind == "playlist":
                process_playlist(index, url)
            else:
                process_video(index, url)
        except Exception as exc:
            print(f"ERROR link {index}/6: {exc}")
    print("\nSelesai menjalankan semua link.")


if __name__ == "__main__":
    main()
