#!/usr/bin/env python3
import os
import shutil
import hashlib

def main():
    # Resolve entry.png relative to main.py's directory with CWD fallback
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(script_dir, "entry.png")
    if not os.path.exists(src_path):
        src_path = "entry.png"

    # Read output directory from environment variable or default to /output
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)

    dest_path = os.path.join(out_dir, "entry.png")

    # Copy image bytes exactly
    shutil.copyfile(src_path, dest_path)

    # Check that output file exists and its size equals source file size
    if not os.path.exists(dest_path) or os.path.getsize(dest_path) != os.path.getsize(src_path):
        import sys
        print(f"Error: Output file {dest_path} is missing or size mismatch.", file=sys.stderr)
        sys.exit(1)

    # Compute SHA-256 of the copied file
    sha256_hash = hashlib.sha256()
    with open(dest_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    file_sha256 = sha256_hash.hexdigest()

    print(f"Output image: {dest_path}")
    print(f"SHA-256: {file_sha256}")

if __name__ == "__main__":
    main()
