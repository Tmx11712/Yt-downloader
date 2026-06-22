#!/usr/bin/env python3
"""
Script untuk menemukan lagu yang terduplikat dalam folder downloads
"""

import os
from collections import defaultdict
from pathlib import Path

def extract_song_name(filename):
    """
    Ekstrak nama lagu dari nama file dengan menghapus nomor urut di depan
    """
    # Hapus ekstensi
    name = Path(filename).stem
    
    # Hapus nomor urut di depan (001 - , 002 - , dst)
    parts = name.split(' - ', 1)
    if len(parts) > 1 and parts[0].strip().isdigit():
        return parts[1].strip().lower()
    return name.lower()

def find_duplicates(folder_path):
    """
    Cari semua lagu yang terduplikat dalam folder
    """
    if not os.path.isdir(folder_path):
        print(f"❌ Folder tidak ditemukan: {folder_path}")
        return
    
    # Mapping dari song_name ke list of files
    songs = defaultdict(list)
    
    # Scan folder
    for filename in os.listdir(folder_path):
        if filename.startswith('.'):
            continue
        
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
            song_name = extract_song_name(filename)
            songs[song_name].append(filename)
    
    # Tampilkan duplicates
    duplicates = {k: v for k, v in songs.items() if len(v) > 1}
    
    if not duplicates:
        print(f"✅ Tidak ada lagu yang terduplikat di {folder_path}")
        return
    
    print(f"\n📋 LAPORAN DUPLIKAT - {folder_path}")
    print(f"{'='*80}")
    print(f"Total lagu unik: {len(songs)}")
    print(f"Total duplikat: {len(duplicates)}")
    print(f"{'='*80}\n")
    
    # Sorting untuk daftar yang lebih rapi
    sorted_dups = sorted(duplicates.items(), key=lambda x: x[0])
    
    total_duplicate_files = 0
    for i, (song_name, files) in enumerate(sorted_dups, 1):
        print(f"{i}. [{len(files)} file] {song_name}")
        for j, filename in enumerate(files, 1):
            filepath = os.path.join(folder_path, filename)
            file_size = os.path.getsize(filepath) / (1024 * 1024)  # MB
            print(f"   [{j}] {filename} ({file_size:.2f} MB)")
        print()
        total_duplicate_files += len(files) - 1  # -1 karena 1 file yang original
    
    print(f"{'='*80}")
    print(f"✓ Total file yang bisa dihapus: {total_duplicate_files} file")
    print(f"✓ Perkiraan storage yang bisa dihemat: Lihat total ukuran di atas")
    print(f"{'='*80}\n")

if __name__ == '__main__':
    print("🔍 Analisis Lagu Terduplikat\n")
    
    # Scan folder downloads_mix
    find_duplicates("e:\\lagu\\downloads_mix")
    
    # Scan folder LAgu BAtak
    find_duplicates("e:\\lagu\\LAgu BAtak")
    
    # Optional: Scan cross-folder duplicates
    print("\n" + "="*80)
    print("🔍 Cek Duplikat ANTAR FOLDER (downloads_mix vs LAgu BAtak)")
    print("="*80 + "\n")
    
    folder1 = "e:\\lagu\\downloads_mix"
    folder2 = "e:\\lagu\\LAgu BAtak"
    
    songs1 = {}
    songs2 = {}
    
    # Scan folder 1
    for filename in os.listdir(folder1):
        if filename.startswith('.'):
            continue
        filepath = os.path.join(folder1, filename)
        if os.path.isfile(filepath):
            song_name = extract_song_name(filename)
            songs1[song_name] = filename
    
    # Scan folder 2
    for filename in os.listdir(folder2):
        if filename.startswith('.'):
            continue
        filepath = os.path.join(folder2, filename)
        if os.path.isfile(filepath):
            song_name = extract_song_name(filename)
            songs2[song_name] = filename
    
    # Cari cross-folder duplicates
    cross_dups = {}
    for song in songs1:
        if song in songs2:
            cross_dups[song] = (songs1[song], songs2[song])
    
    if cross_dups:
        print(f"⚠️  Ditemukan {len(cross_dups)} lagu yang ada di kedua folder:\n")
        for i, (song_name, (file1, file2)) in enumerate(sorted(cross_dups.items()), 1):
            print(f"{i}. {song_name}")
            print(f"   downloads_mix: {file1}")
            print(f"   LAgu BAtak:    {file2}\n")
    else:
        print("✅ Tidak ada duplikat antar folder")
