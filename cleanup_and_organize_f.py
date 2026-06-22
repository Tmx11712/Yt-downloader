#!/usr/bin/env python3
"""
Script untuk menghapus duplikat di F:\LAGU DJ dan reorganisasi folder lagu
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict

def extract_song_name(filename):
    """Ekstrak nama lagu tanpa nomor urut"""
    name = Path(filename).stem
    parts = name.split(' - ', 1)
    if len(parts) > 1 and parts[0].strip().isdigit():
        return parts[1].strip().lower()
    return name.lower()

def cleanup_f_lagu_dj():
    """Hapus duplikat di F:\LAGU DJ"""
    
    folder = r"F:\LAGU DJ"
    backup_folder = os.path.join(folder, "_duplicates_backup_F")
    
    if not os.path.isdir(folder):
        print(f"❌ Folder tidak ditemukan: {folder}")
        return
    
    # Create backup folder
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
        print(f"📁 Backup folder dibuat: {backup_folder}\n")
    
    # Mapping dari song_name ke list of files with numbers
    songs = defaultdict(list)
    
    # Scan folder
    for filename in os.listdir(folder):
        if filename.startswith('_'):
            continue
        
        filepath = os.path.join(folder, filename)
        if os.path.isfile(filepath) and filename.endswith('.mp3'):
            song_name = extract_song_name(filename)
            
            # Extract number from filename
            parts = filename.split(' - ', 1)
            try:
                number = int(parts[0].strip())
                songs[song_name].append((number, filename, filepath))
            except:
                songs[song_name].append((999999, filename, filepath))
    
    # Temukan dan hapus duplicates
    duplicates = {k: v for k, v in songs.items() if len(v) > 1}
    
    if not duplicates:
        print(f"✅ Tidak ada duplikat di {folder}")
        return
    
    print(f"🗑️  REMOVAL PLAN untuk {folder}")
    print(f"{'='*80}")
    
    total_size_freed = 0
    files_to_remove = []
    
    for song_name, file_list in sorted(duplicates.items()):
        # Sort by number to keep lowest numbers
        file_list_sorted = sorted(file_list, key=lambda x: x[0])
        
        # Keep first one, mark others for removal
        keep_file = file_list_sorted[0]
        remove_files = file_list_sorted[1:]
        
        print(f"\n📌 {song_name}")
        print(f"   KEEP: {keep_file[1]}")
        
        for num, filename, filepath in remove_files:
            file_size = os.path.getsize(filepath) / (1024 * 1024)
            print(f"   🗑️  REMOVE: {filename} ({file_size:.2f} MB)")
            total_size_freed += file_size
            files_to_remove.append((filename, filepath))
    
    print(f"\n{'='*80}")
    print(f"📊 RINGKASAN:")
    print(f"  • File yang akan dihapus: {len(files_to_remove)}")
    print(f"  • Storage yang dihemat: {total_size_freed:.2f} MB ({total_size_freed/1024:.2f} GB)")
    print(f"{'='*80}\n")
    
    # Confirm removal
    response = input("Hapus file-file duplikat? (yes/no): ").strip().lower()
    
    if response == 'yes':
        removed_count = 0
        for filename, filepath in files_to_remove:
            try:
                # Move to backup folder
                backup_path = os.path.join(backup_folder, filename)
                shutil.move(filepath, backup_path)
                print(f"✓ Dipindahkan ke backup: {filename}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Error dengan {filename}: {e}")
        
        print(f"\n{'='*80}")
        print(f"✅ Selesai! {removed_count} file berhasil dihapus/dipindahkan")
        print(f"✅ Storage dihemat: {total_size_freed/1024:.2f} GB")
        print(f"💾 File duplikat disimpan di: {backup_folder}")
        print(f"{'='*80}")
    else:
        print("⏭️  Pembatalan. Tidak ada file yang dihapus.")

def organize_music_folders():
    """Reorganisasi folder musik"""
    
    print(f"\n\n{'='*80}")
    print("📂 REORGANISASI FOLDER MUSIK")
    print(f"{'='*80}\n")
    
    folders_to_organize = [
        r"F:\LAGU DJ",
        r"F:\LAgu BAtak",
    ]
    
    for folder in folders_to_organize:
        if not os.path.isdir(folder):
            continue
        
        # Buat subfolder untuk format/kategori
        webm_folder = os.path.join(folder, "_WebM Videos")
        mp3_folder = os.path.join(folder, "_MP3 Audio")
        
        webm_count = 0
        mp3_count = 0
        
        # Count files
        for filename in os.listdir(folder):
            if filename.startswith('_'):
                continue
            if filename.endswith('.webm'):
                webm_count += 1
            elif filename.endswith('.mp3'):
                mp3_count += 1
        
        print(f"📍 {folder}")
        print(f"   WebM: {webm_count} file")
        print(f"   MP3: {mp3_count} file")
        print(f"   💡 Rekomendasi: Pisahkan format atau hapus duplikat antar format\n")

if __name__ == '__main__':
    print("🎵 PEMBERSIH & ORGANIZER FOLDER LAGU F:\n")
    
    # Bersihkan duplikat
    cleanup_f_lagu_dj()
    
    # Reorganisasi
    organize_music_folders()
