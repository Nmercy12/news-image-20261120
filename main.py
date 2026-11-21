#!/usr/bin/env python3
import os
import sys
import hashlib

def main():
    # Resolve entry.png relative to main.py's own directory, with CWD fallback
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src_image_path = os.path.join(script_dir, "entry.png")
    if not os.path.exists(src_image_path):
        src_image_path = "entry.png"

    if not os.path.exists(src_image_path):
        print(f"Error: Source image {src_image_path} not found.", file=sys.stderr)
        sys.exit(1)

    # Get output directory from MAKEFUN_OUTPUT_DIR environment variable or default /output
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)

    dest_image_path = os.path.join(output_dir, "entry.png")

    # Read image bytes and copy exactly
    with open(src_image_path, "rb") as f:
        image_bytes = f.read()

    with open(dest_image_path, "wb") as f:
        f.write(image_bytes)

    # Verify the output exists and matches the source size
    if not os.path.exists(dest_image_path) or os.path.getsize(dest_image_path) != len(image_bytes):
        print(f"Error: Output {dest_image_path} missing or size mismatch.", file=sys.stderr)
        sys.exit(1)

    # Calculate SHA-256
    sha256_hash = hashlib.sha256(image_bytes).hexdigest()

    print(f"Output path: {dest_image_path}")
    print(f"SHA-256: {sha256_hash}")

if __name__ == "__main__":
    main()
