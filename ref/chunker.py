#!/usr/bin/env python3
import hashlib

DEFAULT_CHUNK_SIZE = 4 * 1024 * 1024  # 4MB

def chunk_iter(path, chunk_size=DEFAULT_CHUNK_SIZE):
    with open(path, 'rb') as f:
        i = 0
        while True:
            b = f.read(chunk_size)
            if not b:
                break
            h = hashlib.sha256(b).hexdigest()
            yield {"hash": f"sha256:{h}", "size": len(b), "order": i, "bytes": b}
            i += 1

def manifest_for_file(path, chunk_size=DEFAULT_CHUNK_SIZE, name=None, media_type="application/octet-stream"):
    chunks = []
    total = 0
    for c in chunk_iter(path, chunk_size):
        chunks.append({k: c[k] for k in ("hash", "size", "order")})
        total += c["size"]
    # Root hash: sha256 of concatenated chunk hashes
    root = hashlib.sha256(''.join([c['hash'] for c in chunks]).encode('utf-8')).hexdigest()
    return {
        "version": "1.0",
        "id": f"urn:udf:manifest:sha256:{root}",
        "media_type": media_type,
        "total_size": total,
        "chunks": chunks,
        "integrity": {"root_hash": f"sha256:{root}", "algo": "sha256", "tree": "concat"},
        "metadata": {"name": name or path}
    }

