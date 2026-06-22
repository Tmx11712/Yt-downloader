#!/usr/bin/env python3
"""
Script untuk menganalisis duplikat di F: (WebM vs MP3)
"""

import os
from pathlib import Path
from collections import defaultdict

def extract_song_name(filename):
    """Ekstrak nama lagu dari filename"""
    name = Path(filename).stem
    # Hapus nomor di awal
    parts = name.split(' - ', 1)
    if len(parts) > 1 and parts[0].strip().isdigit():
        return parts[1].strip().lower()
    return name.lower()

def analyze_f_drive():
    """Analisis folder F:\LAgu BAtak dan F:\LAGU DJ"""
    
    batak_folder = r"F:\LAgu BAtak"
    dj_folder = r"F:\LAGU DJ"
    
    # Map lagu dari masing-masing folder
    batak_songs = {}  # {song_name: filename}
    dj_songs = {}      # {song_name: filename}
    
    print("🔍 ANALISIS DUPLIKAT F: FLASHDISK")
    print("=" * 80)
    
    # Scan folder LAgu BAtak
    if os.path.isdir(batak_folder):
        print(f"\n📂 Scanning: {batak_folder}")
        for filename in os.listdir(batak_folder):
            if filename.endswith('.webm'):
                song_name = extract_song_name(filename)
                batak_songs[song_name] = filename
        print(f"   ✓ Found {len(batak_songs)} WebM files")
    
    # Scan folder LAGU DJ
    if os.path.isdir(dj_folder):
        print(f"\n📂 Scanning: {dj_folder}")
        for filename in os.listdir(dj_folder):
            if filename.endswith('.mp3'):
                song_name = extract_song_name(filename)
                dj_songs[song_name] = filename
        print(f"   ✓ Found {len(dj_songs)} MP3 files")
    
    # Cari duplikat antar folder (WebM vs MP3)
    print(f"\n{'=' * 80}")
    print("🔎 DUPLIKAT ANTAR FOLDER (WebM vs MP3)")
    print(f"{'=' * 80}")
    
    duplicates = {}
    for song_name in batak_songs:
        if song_name in dj_songs:
            duplicates[song_name] = {
                'webm': batak_songs[song_name],
                'mp3': dj_songs[song_name]
            }
    
    if duplicates:
        print(f"\n⚠️  Ditemukan {len(duplicates)} lagu DUPLIKAT (format berbeda):\n")
        for idx, (song_name, files) in enumerate(sorted(duplicates.items()), 1):
            print(f"{idx:3}. {song_name}")
            print(f"    WebM: {files['webm']}")
            print(f"    MP3:  {files['mp3']}\n")
    else:
        print("\n✅ Tidak ada duplikat antar folder")
    
    # Statistik
    print(f"\n{'=' * 80}")
    print("📊 STATISTIK:")
    print(f"  • File di LAgu BAtak (WebM): {len(batak_songs)}")
    print(f"  • File di LAGU DJ (MP3): {len(dj_songs)}")
    print(f"  • Duplikat (sama-sama ada): {len(duplicates)}")
    print(f"  • Unik di LAgu BAtak: {len(batak_songs) - len(duplicates)}")
    print(f"  • Unik di LAGU DJ: {len(dj_songs) - len(duplicates)}")
    print(f"{'=' * 80}")
    
    # Cek duplikat dalam folder LAGU DJ
    print(f"\n{'=' * 80}")
    print("🔎 DUPLIKAT DALAM FOLDER: F:\\LAGU DJ")
    print(f"{'=' * 80}")
    
    dj_songs_full = {}
    if os.path.isdir(dj_folder):
        for filename in os.listdir(dj_folder):
            if filename.endswith('.mp3'):
                filepath = os.path.join(dj_folder, filename)
                if os.path.isfile(filepath):
                    song_name = extract_song_name(filename)
                    if song_name not in dj_songs_full:
                        dj_songs_full[song_name] = []
                    dj_songs_full[song_name].append((filename, filepath))
    
    # Cari duplikat dalam LAGU DJ
    dj_duplicates = {k: v for k, v in dj_songs_full.items() if len(v) > 1}
    
    if dj_duplicates:
        print(f"\n⚠️  Ditemukan {len(dj_duplicates)} lagu DUPLIKAT dalam folder LAGU DJ:\n")
        for idx, (song_name, files) in enumerate(sorted(dj_duplicates.items()), 1):
            print(f"{idx}. {song_name}")
            for filename, filepath in files:
                size = os.path.getsize(filepath) / (1024 * 1024)
                print(f"   - {filename} ({size:.2f} MB)")
            print()
    else:
        print("\n✅ Tidak ada duplikat dalam folder LAGU DJ")

if __name__ == '__main__':
    analyze_f_drive()
