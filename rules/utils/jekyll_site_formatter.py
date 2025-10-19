#!/usr/bin/env python3
import argparse
import os
import shutil
from pathlib import Path

def safe_copy(src, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    dst_path = os.path.join(dst_dir, os.path.basename(src))
    shutil.copy(src, dst_path)
    print(f"Copied {src} -> {dst_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--index", required=True)
    parser.add_argument("--section", action="append", default=[])
    parser.add_argument("--data", action="append", default=[])
    parser.add_argument("--output_dir", required=True)
    args = parser.parse_args()

    print(f"\n📘 Building doc site: {args.title}")
    print(f"Index: {args.index}")
    print(f"Sections: {len(args.section)}")
    print(f"Data files: {len(args.data)}")
    print(f"Output dir: {args.output_dir}\n")

    os.makedirs(args.output_dir, exist_ok=True)

    # Copy index
    safe_copy(args.index, args.output_dir)

    # Copy sections (Markdown files)
    for sec in args.section:
        safe_copy(sec, args.output_dir)

    # Copy associated data (images, etc.)
    data_dir = os.path.join(args.output_dir, "assets")
    for data_file in args.data:
        safe_copy(data_file, data_dir)

    print("\n✅ Documentation site files prepared successfully.")

if __name__ == "__main__":
    main()
