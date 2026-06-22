#!/usr/bin/env python3
"""
YouTube Playlist Downloader
Menggunakan yt-dlp sebagai backend.

Install dependensi:
    pip install yt-dlp

Penggunaan:
    python yt_playlist_downloader.py <URL> [opsi]

Contoh:
    python yt_playlist_downloader.py "https://www.youtube.com/playlist?list=PLxxx"
    python yt_playlist_downloader.py "https://www.youtube.com/playlist?list=PLxxx" --audio-only
    python yt_playlist_downloader.py "https://www.youtube.com/playlist?list=PLxxx" --quality 720
    python yt_playlist_downloader.py "https://www.youtube.com/playlist?list=PLxxx" --output ./downloads --start 5 --end 20
"""

import argparse
import sys
import os

try:
    import yt_dlp
except ImportError:
    print("[ERROR] yt-dlp belum terinstall.")
    print("Install dulu dengan perintah: pip install yt-dlp")
    sys.exit(1)


def build_format_string(quality: int | None, audio_only: bool) -> str:
    """Bangun format selector yt-dlp berdasarkan preferensi kualitas."""
    if audio_only:
        return "bestaudio/best"

    if quality is None:
        # Default: video terbaik dengan audio
        return "bestvideo+bestaudio/best"

    # Pilih resolusi tertentu, fallback ke yang lebih rendah jika tidak ada
    return (
        f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]/best"
    )


def progress_hook(d: dict) -> None:
    """Callback untuk menampilkan progress download."""
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
                print(
                    f"\r  [{pct:5.1f}%] {filename[:40]:<40} "
                    f"{speed_kb:6.1f} KB/s  ETA {eta}s   ",
                    end="",
                    flush=True,
                )
            except UnicodeEncodeError:
                print(
                    f"\r  [{pct:5.1f}%] downloading... "
                    f"{speed_kb:6.1f} KB/s  ETA {eta}s   ",
                    end="",
                    flush=True,
                )

    elif status == "finished":
        fname = os.path.basename(d.get('filename', ''))
        try:
            print(f"\n  [OK] Selesai: {fname}")
        except UnicodeEncodeError:
            print(f"\n  [OK] Selesai download")

    elif status == "error":
        try:
            print(f"\n  [ERROR] Error: {d.get('filename', 'unknown')}")
        except UnicodeEncodeError:
            print(f"\n  [ERROR] Download error")


def download_playlist(
    url: str,
    output_dir: str = "./downloads",
    audio_only: bool = False,
    quality: int | None = None,
    start_index: int | None = None,
    end_index: int | None = None,
    skip_existing: bool = True,
    write_thumbnail: bool = False,
    write_metadata: bool = True,
    concurrent_fragments: int = 4,
) -> None:
    """
    Download playlist YouTube.

    Args:
        url             : URL playlist atau video YouTube
        output_dir      : Folder tujuan download
        audio_only      : Jika True, hanya download audio (mp3)
        quality         : Resolusi maksimum video (misal: 720, 1080)
        start_index     : Download mulai dari video ke-N (1-based)
        end_index       : Download sampai video ke-N (1-based)
        skip_existing   : Lewati file yang sudah ada
        write_thumbnail : Simpan thumbnail sebagai gambar
        write_metadata  : Embed metadata (judul, artis, dll.)
        concurrent_fragments : Jumlah fragment yang diunduh bersamaan
    """
    os.makedirs(output_dir, exist_ok=True)

    # Template nama file: folder/nomor - judul.ekstensi
    if audio_only:
        outtmpl = os.path.join(output_dir, "%(playlist_index)s - %(title)s.%(ext)s")
    else:
        outtmpl = os.path.join(output_dir, "%(playlist_index)s - %(title)s.%(ext)s")

    ydl_opts: dict = {
        "format": build_format_string(quality, audio_only),
        "outtmpl": outtmpl,
        "ignoreerrors": True,        # Lanjut walau ada video error/private
        "no_warnings": False,
        "progress_hooks": [progress_hook],
        "noplaylist": False,
        "concurrent_fragment_downloads": concurrent_fragments,
        "retries": 5,
        "fragment_retries": 5,
        "skip_unavailable_fragments": True,
    }

    # Batasi range playlist
    if start_index is not None or end_index is not None:
        ydl_opts["playlist_items"] = _build_playlist_range(start_index, end_index)

    # Lewati yang sudah ada
    if skip_existing:
        ydl_opts["nooverwrites"] = True
        ydl_opts["continue_dl"] = True

    # Audio only: konversi ke mp3
    if audio_only:
        ydl_opts["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ]
        if write_metadata:
            ydl_opts["postprocessors"].append({"key": "FFmpegMetadata"})
            ydl_opts["postprocessors"].append({"key": "EmbedThumbnail"})
    else:
        # Video: merge ke mkv/mp4
        ydl_opts["merge_output_format"] = "mp4"
        if write_metadata:
            ydl_opts["postprocessors"] = [{"key": "FFmpegMetadata"}]

    if write_thumbnail:
        ydl_opts["writethumbnail"] = True

    quality_label = "Audio MP3" if audio_only else f"Video (maks {quality or 'best'}p)"
    print(f"\n{'='*60}")
    print(f"  URL          : {url}")
    print(f"  Output       : {os.path.abspath(output_dir)}")
    print(f"  Mode         : {quality_label}")
    if start_index or end_index:
        print(f"  Range        : video {start_index or 1} - {end_index or 'akhir'}")
    print(f"{'='*60}\n")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ret = ydl.download([url])

    if ret == 0:
        print(f"\n[OK] Download selesai. File disimpan di: {os.path.abspath(output_dir)}")
    else:
        print(f"\n[WARNING] Selesai dengan beberapa error (kode: {ret}). Cek log di atas.")


def _build_playlist_range(start: int | None, end: int | None) -> str:
    """Buat string range untuk yt-dlp playlist_items."""
    if start and end:
        return f"{start}:{end}"
    elif start:
        return f"{start}:"
    elif end:
        return f":{end}"
    return ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download playlist YouTube menggunakan yt-dlp",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("url", help="URL playlist atau video YouTube")
    parser.add_argument(
        "-o", "--output",
        default="./downloads",
        help="Folder tujuan download (default: ./downloads)",
    )
    parser.add_argument(
        "--audio-only",
        action="store_true",
        help="Hanya download audio, convert ke MP3",
    )
    parser.add_argument(
        "--quality",
        type=int,
        choices=[144, 240, 360, 480, 720, 1080, 1440, 2160],
        help="Resolusi maksimum video (contoh: 720 untuk 720p)",
    )
    parser.add_argument(
        "--start",
        type=int,
        metavar="N",
        help="Mulai dari video ke-N dalam playlist (1-based)",
    )
    parser.add_argument(
        "--end",
        type=int,
        metavar="N",
        help="Berhenti di video ke-N dalam playlist (1-based)",
    )
    parser.add_argument(
        "--no-skip",
        action="store_true",
        help="Re-download file yang sudah ada",
    )
    parser.add_argument(
        "--thumbnail",
        action="store_true",
        help="Simpan thumbnail sebagai file gambar",
    )
    parser.add_argument(
        "--no-metadata",
        action="store_true",
        help="Jangan embed metadata ke file",
    )
    parser.add_argument(
        "--fragments",
        type=int,
        default=4,
        help="Jumlah fragment paralel saat download (default: 4)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    download_playlist(
        url=args.url,
        output_dir=args.output,
        audio_only=args.audio_only,
        quality=args.quality,
        start_index=args.start,
        end_index=args.end,
        skip_existing=not args.no_skip,
        write_thumbnail=args.thumbnail,
        write_metadata=not args.no_metadata,
        concurrent_fragments=args.fragments,
    )


if __name__ == "__main__":
    main()
