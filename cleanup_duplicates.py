#!/usr/bin/env python3
"""
Script untuk menghapus lagu terduplikat dengan opsi backup
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

def find_and_remove_duplicates(folder_path, keep_lowest_numbers=True, create_backup=True):
    """
    Temukan dan hapus duplikat dengan opsi backup
    """
    if not os.path.isdir(folder_path):
        print(f"❌ Folder tidak ditemukan: {folder_path}")
        return
    
    # Create backup folder
    backup_folder = os.path.join(folder_path, "_duplicates_backup")
    if create_backup and not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
        print(f"📁 Backup folder dibuat: {backup_folder}\n")
    
    # Mapping dari song_name ke list of files with numbers
    songs = defaultdict(list)
    
    # Scan folder
    for filename in os.listdir(folder_path):
        if filename.startswith('_'):
            continue
        if filename.startswith('.'):
            continue
        
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
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
        print(f"✅ Tidak ada duplikat di {folder_path}")
        return
    
    print(f"🗑️  REMOVAL PLAN untuk {folder_path}")
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
                if create_backup:
                    # Move to backup folder
                    backup_path = os.path.join(backup_folder, filename)
                    shutil.move(filepath, backup_path)
                    print(f"✓ Dipindahkan ke backup: {filename}")
                else:
                    # Delete permanently
                    os.remove(filepath)
                    print(f"✓ Dihapus: {filename}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Error dengan {filename}: {e}")
        
        print(f"\n{'='*80}")
        print(f"✅ Selesai! {removed_count} file berhasil dihapus/dipindahkan")
        print(f"✅ Storage dihemat: {total_size_freed/1024:.2f} GB")
        if create_backup:
            print(f"💾 File duplikat disimpan di: {backup_folder}")
        print(f"{'='*80}")
    else:
        print("⏭️  Pembatalan. Tidak ada file yang dihapus.")

if __name__ == '__main__':
    print("🔍 PEMBERSIH LAGU TERDUPLIKAT\n")
    
    folder = "e:\\lagu\\downloads_mix"
    find_and_remove_duplicates(folder, keep_lowest_numbers=True, create_backup=True)
