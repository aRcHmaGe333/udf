#!/usr/bin/env python3
import sys, hashlib, os

CHUNK_SIZE = 4 * 1024 * 1024  # 4MB

def chunks(path, size=CHUNK_SIZE):
    with open(path, 'rb') as f:
        while True:
            b = f.read(size)
            if not b:
                break
            yield b

def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def main(paths):
    total = 0
    unique = set()
    for p in paths:
        if not os.path.isfile(p):
            continue
        for c in chunks(p):
            total += len(c)
            unique.add(sha256(c))
    unique_bytes = len(unique) * CHUNK_SIZE  # approximate upper bound
    # adjust last chunk sizes by reading sizes again
    # Better: track sizes; keep it simple for demo
    print(f"Files: {len(paths)}")
    print(f"Chunk size: {CHUNK_SIZE//(1024*1024)}MB")
    print(f"Total bytes (approx): {total}")
    print(f"Unique chunks: {len(unique)}")
    print(f"Approx unique bytes: {unique_bytes}")
    if total:
        print(f"Dedupe ratio (stored/total): {unique_bytes/total:.2f}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: dedupe_demo.py <files...>")
        sys.exit(1)
    main(sys.argv[1:])

