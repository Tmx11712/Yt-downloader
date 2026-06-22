#!/usr/bin/env python3
"""
Script untuk organize lagu MP3 clean untuk mobil
Format: Nomor urut rapi (001-103) untuk kompatibilitas head unit
"""

import os
import shutil
from pathlib import Path

def organize_for_car():
    """Organize lagu untuk mobil"""
    
    source_folder = r"E:\lagu\downloads_mix"
    output_folder = r"E:\lagu\LAGU_MOBIL"
    
    if not os.path.isdir(source_folder):
        print(f"❌ Folder source tidak ditemukan: {source_folder}")
        return
    
    # Create output folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"📁 Folder dibuat: {output_folder}\n")
    
    # Collect all MP3 files
    mp3_files = []
    for filename in sorted(os.listdir(source_folder)):
        filepath = os.path.join(source_folder, filename)
        if os.path.isfile(filepath) and filename.endswith('.mp3'):
            mp3_files.append((filename, filepath))
    
    if not mp3_files:
        print(f"❌ Tidak ada MP3 file di {source_folder}")
        return
    
    print(f"🎵 ORGANIZE LAGU UNTUK MOBIL")
    print(f"{'='*80}")
    print(f"Total MP3 ditemukan: {len(mp3_files)}\n")
    
    # Copy dan rename dengan nomor urut rapi
    print(f"📋 DAFTAR LAGU YANG AKAN DICOPY:")
    print(f"{'='*80}\n")
    
    for idx, (old_name, filepath) in enumerate(mp3_files, 1):
        # Ambil hanya nama lagu (tanpa nomor awal)
        parts = old_name.split(' - ', 1)
        if len(parts) > 1 and parts[0].strip().isdigit():
            song_name = parts[1]
        else:
            song_name = old_name
        
        # Nomor urut baru dengan format 001, 002, dst
        new_number = f"{idx:03d}"
        new_name = f"{new_number} - {song_name}"
        new_filepath = os.path.join(output_folder, new_name)
        
        print(f"{idx:3}. {new_name}")
    
    print(f"\n{'='*80}")
    print(f"📊 RINGKASAN:")
    print(f"  • Total lagu: {len(mp3_files)}")
    print(f"  • Folder tujuan: {output_folder}")
    print(f"  • Format: 001, 002, 003... (kompatibel head unit mobil)")
    print(f"{'='*80}\n")
    
    # Confirm copy
    response = input("Copy lagu ke folder LAGU_MOBIL? (yes/no): ").strip().lower()
    
    if response == 'yes':
        copied = 0
        for idx, (old_name, filepath) in enumerate(mp3_files, 1):
            try:
                parts = old_name.split(' - ', 1)
                if len(parts) > 1 and parts[0].strip().isdigit():
                    song_name = parts[1]
                else:
                    song_name = old_name
                
                new_number = f"{idx:03d}"
                new_name = f"{new_number} - {song_name}"
                new_filepath = os.path.join(output_folder, new_name)
                
                shutil.copy2(filepath, new_filepath)
                print(f"✓ {idx:3}. {new_name}")
                copied += 1
            except Exception as e:
                print(f"❌ Error dengan {old_name}: {e}")
        
        print(f"\n{'='*80}")
        print(f"✅ SELESAI!")
        print(f"✅ {copied} lagu berhasil dicopy")
        print(f"📁 Folder: {output_folder}")
        print(f"🚗 Siap dipindahkan ke USB/SD card untuk mobil!")
        print(f"{'='*80}")
        
        # Info tambahan
        print(f"\n💡 TIPS MOBIL:")
        print(f"  1. Copy folder LAGU_MOBIL ke USB flashdisk")
        print(f"  2. Colok USB ke head unit mobil")
        print(f"  3. Head unit akan scan otomatis nomor urut 001-103")
        print(f"  4. Semua lagu akan terurut rapi di playlist")
        
    else:
        print("⏭️  Pembatalan. Tidak ada file yang dicopy.")

if __name__ == '__main__':
    organize_for_car()
