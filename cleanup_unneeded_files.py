#!/usr/bin/env python3
"""Cleanup file sementara dan sampah di folder musik."""

import argparse
import os
import shutil
from pathlib import Path

JUNK_EXTENSIONS = {
    ".part",
    ".crdownload",
    ".tmp",
    ".temp",
    ".temp.mp3",
    ".log",
    ".url",
    ".lnk",
}

JUNK_FILENAMES = {
    "desktop.ini",
    "thumbs.db",
    ".ds_store",
    ".localized",
}

EXCLUDE_FOLDERS = {
    "_duplicates_backup",
    "_duplicates_backup_F",
    "_WebM Videos",
    "_MP3 Audio",
}


def is_junk_file(path: Path) -> bool:
    if not path.is_file():
        return False

    lower_name = path.name.lower()
    if lower_name in JUNK_FILENAMES:
        return True

    for ext in JUNK_EXTENSIONS:
        if lower_name.endswith(ext):
            return True

    return False


def find_junk_files(folder: Path, recursive: bool = True):
    junk_files = []
    for root, dirs, files in os.walk(folder):
        rel_root = Path(root).relative_to(folder)
        if any(part in EXCLUDE_FOLDERS for part in rel_root.parts):
            dirs.clear()
            continue

        for filename in files:
            filepath = Path(root) / filename
            if is_junk_file(filepath):
                junk_files.append(filepath)

        if not recursive:
            break
    return junk_files


def cleanup_junk_files(folder: Path, backup: bool = True, recursive: bool = True):
    junk_files = find_junk_files(folder, recursive=recursive)
    if not junk_files:
        print(f"✅ Tidak ditemukan file sementara/junk di {folder}")
        return 0

    backup_folder = folder / "_unneeded_backup"
    if backup:
        backup_folder.mkdir(exist_ok=True)
        print(f"📁 Backup akan dibuat di: {backup_folder}\n")

    total_bytes = 0
    for filepath in junk_files:
        try:
            size = filepath.stat().st_size
            total_bytes += size
            if backup:
                destination = backup_folder / filepath.name
                destination = destination.with_name(_unique_name(destination))
                shutil.move(str(filepath), str(destination))
                print(f"✓ Dipindahkan ke backup: {filepath}")
            else:
                filepath.unlink()
                print(f"✓ Dihapus: {filepath}")
        except Exception as exc:
            print(f"❌ Gagal memproses {filepath}: {exc}")

    print(f"\n📊 Total file: {len(junk_files)}")
    print(f"  • Total ukuran: {total_bytes / (1024 * 1024):.2f} MB")
    return len(junk_files)


def _unique_name(path: Path) -> str:
    if not path.exists():
        return path.name

    stem = path.stem
    suffix = path.suffix
    counter = 1
    while True:
        candidate = path.with_name(f"{stem}_{counter}{suffix}")
        if not candidate.exists():
            return candidate.name
        counter += 1


def parse_args():
    parser = argparse.ArgumentParser(description="Cleanup file sementara/junk di folder lagu")
    parser.add_argument("folder", help="Folder target untuk pembersihan")
    parser.add_argument("--no-backup", action="store_true", help="Hapus file secara permanen tanpa backup")
    parser.add_argument("--no-recursive", action="store_true", help="Hanya scan folder target, tidak rekursif")
    parser.add_argument("--yes", action="store_true", help="Langsung hapus tanpa konfirmasi")
    return parser.parse_args()


def main():
    args = parse_args()
    folder = Path(args.folder)

    if not folder.is_dir():
        print(f"❌ Folder tidak ditemukan: {folder}")
        return

    print(f"🔎 Mencari file sementara/junk di: {folder}")
    junk_files = find_junk_files(folder, recursive=not args.no_recursive)

    if not junk_files:
        print("✅ Tidak ada file sementara/junk yang ditemukan.")
        return

    print(f"\n📋 Daftar file yang tidak diperlukan ({len(junk_files)}):")
    for filepath in junk_files:
        print(f"  - {filepath}")

    if not args.yes:
        confirm = input("Hapus/move file-file tersebut? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("⏭️  Dibatalkan. Tidak ada file yang dihapus.")
            return

    deleted = cleanup_junk_files(
        folder,
        backup=not args.no_backup,
        recursive=not args.no_recursive,
    )

    if deleted:
        print(f"✅ Selesai: {deleted} file sementara/junk sudah diproses.")


if __name__ == "__main__":
    main()
