#!/usr/bin/env python3
"""
Script untuk copy folder LAGU_MOBIL ke flashdisk F:
"""

import os
import shutil
from pathlib import Path

def copy_to_flashdisk():
    """Copy LAGU_MOBIL ke F: flashdisk"""
    
    source_folder = r"E:\lagu\LAGU_MOBIL"
    dest_folder = r"F:\LAGU_MOBIL"
    
    if not os.path.isdir(source_folder):
        print(f"❌ Folder source tidak ditemukan: {source_folder}")
        return
    
    # Check flashdisk
    if not os.path.exists(r"F:"):
        print(f"❌ Flashdisk F: tidak terdapat!")
        return
    
    print(f"🚗 COPY LAGU KE FLASHDISK F:")
    print(f"{'='*80}")
    print(f"Source: {source_folder}")
    print(f"Dest:   {dest_folder}\n")
    
    # Count files
    mp3_count = 0
    for filename in os.listdir(source_folder):
        if filename.endswith('.mp3'):
            mp3_count += 1
    
    print(f"📊 Total MP3: {mp3_count} lagu\n")
    
    # Check if dest folder exists
    if os.path.exists(dest_folder):
        print(f"⚠️  Folder sudah ada di F:\LAGU_MOBIL")
        response = input("Overwrite? (yes/no): ").strip().lower()
        if response != 'yes':
            print("⏭️  Pembatalan.")
            return
        shutil.rmtree(dest_folder)
        print("🗑️  Folder lama dihapus\n")
    
    # Copy folder
    print(f"📁 Copying folder...\n")
    
    try:
        shutil.copytree(source_folder, dest_folder)
        
        # Verify
        copied_count = 0
        for filename in os.listdir(dest_folder):
            if filename.endswith('.mp3'):
                copied_count += 1
        
        print(f"{'='*80}")
        print(f"✅ SELESAI!")
        print(f"✅ {copied_count} lagu berhasil dicopy ke flashdisk")
        print(f"📁 Folder: F:\\LAGU_MOBIL")
        print(f"{'='*80}")
        print(f"\n🚗 SIAP UNTUK MOBIL!")
        print(f"   • Colok flashdisk F: ke head unit mobil")
        print(f"   • Folder LAGU_MOBIL akan terdeteksi otomatis")
        print(f"   • 103 lagu terurut 001-103")
        
    except Exception as e:
        print(f"❌ Error saat copy: {e}")

if __name__ == '__main__':
    copy_to_flashdisk()
