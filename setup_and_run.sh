#!/usr/bin/env bash
# =============================================================
# Setup & jalankan YouTube Playlist Downloader
# Digunakan jika belum ada yt-dlp / ffmpeg terinstall
# =============================================================

set -euo pipefail

echo "=== YouTube Playlist Downloader Setup ==="

# --- 1. Cek Python ---
if ! command -v python3 &>/dev/null; then
    echo "[ERROR] Python 3 tidak ditemukan. Install dulu."
    exit 1
fi
PYTHON=$(command -v python3)
echo "[OK] Python: $($PYTHON --version)"

# --- 2. Install yt-dlp jika belum ada ---
if ! $PYTHON -c "import yt_dlp" 2>/dev/null; then
    echo "[INFO] Menginstall yt-dlp..."
    pip install --quiet --upgrade yt-dlp
    echo "[OK] yt-dlp terinstall."
else
    # Update ke versi terbaru (penting karena YouTube sering berubah)
    echo "[INFO] Update yt-dlp ke versi terbaru..."
    pip install --quiet --upgrade yt-dlp
    echo "[OK] yt-dlp: $(yt-dlp --version)"
fi

# --- 3. Cek ffmpeg (diperlukan untuk merge video+audio & konversi mp3) ---
if ! command -v ffmpeg &>/dev/null; then
    echo ""
    echo "[PERINGATAN] ffmpeg tidak ditemukan."
    echo "  - Tanpa ffmpeg: hanya bisa download format tunggal (biasanya kualitas lebih rendah)"
    echo "  - Untuk install ffmpeg:"
    echo "    Ubuntu/Debian : sudo apt install ffmpeg"
    echo "    macOS         : brew install ffmpeg"
    echo "    Windows       : https://ffmpeg.org/download.html"
    echo ""
else
    echo "[OK] ffmpeg: $(ffmpeg -version 2>&1 | head -1)"
fi

# --- 4. Jalankan downloader ---
echo ""
echo "=== Menjalankan Downloader ==="

# Ambil argumen dari command line, atau tanya interaktif
if [ "$#" -ge 1 ]; then
    $PYTHON yt_playlist_downloader.py "$@"
else
    # Mode interaktif sederhana
    echo ""
    read -rp "Masukkan URL playlist YouTube: " URL
    if [ -z "$URL" ]; then
        echo "[ERROR] URL tidak boleh kosong."
        exit 1
    fi

    echo ""
    echo "Mode download:"
    echo "  1) Video terbaik (default)"
    echo "  2) Video 1080p"
    echo "  3) Video 720p"
    echo "  4) Audio MP3 saja"
    read -rp "Pilih [1-4, default=1]: " MODE
    MODE=${MODE:-1}

    read -rp "Folder output [./downloads]: " OUTDIR
    OUTDIR=${OUTDIR:-./downloads}

    case "$MODE" in
        1) $PYTHON yt_playlist_downloader.py "$URL" --output "$OUTDIR" ;;
        2) $PYTHON yt_playlist_downloader.py "$URL" --output "$OUTDIR" --quality 1080 ;;
        3) $PYTHON yt_playlist_downloader.py "$URL" --output "$OUTDIR" --quality 720 ;;
        4) $PYTHON yt_playlist_downloader.py "$URL" --output "$OUTDIR" --audio-only ;;
        *) echo "[ERROR] Pilihan tidak valid."; exit 1 ;;
    esac
fi
