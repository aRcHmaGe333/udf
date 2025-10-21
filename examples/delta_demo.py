#!/usr/bin/env python3
import sys, hashlib

CHUNK_SIZE = 4 * 1024 * 1024

def iter_hashes(path):
    with open(path, 'rb') as f:
        while True:
            b = f.read(CHUNK_SIZE)
            if not b:
                break
            yield hashlib.sha256(b).hexdigest(), len(b)

def main(a, b):
    A = list(iter_hashes(a))
    B = list(iter_hashes(b))
    setA = {h for h,_ in A}
    setB = {h for h,_ in B}
    total = sum(sz for _,sz in B)
    changed_hashes = setB - setA
    # approximate changed bytes by chunk size count
    changed = len(changed_hashes) * CHUNK_SIZE
    print(f"Baseline bytes (new version): {total}")
    print(f"Changed chunks: {len(changed_hashes)}")
    print(f"Approx bytes to transfer (delta): {changed}")
    if total:
        print(f"Transfer ratio (delta/baseline): {changed/total:.2f}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: delta_demo.py <old_file> <new_file>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])

