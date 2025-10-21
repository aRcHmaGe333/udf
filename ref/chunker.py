#!/usr/bin/env python3
import hashlib
from typing import Iterator, Dict, Any, Optional

DEFAULT_CHUNK_SIZE = 4 * 1024 * 1024  # 4MB

#!/usr/bin/env python3
import hashlib
from typing import Iterator, Dict, Any, Optional

DEFAULT_CHUNK_SIZE = 4 * 1024 * 1024  # 4MB

# Buzhash table for rolling hash
BUZHASH_TABLE = [
    0x458be752, 0xc1079ccd, 0xf245b4bf, 0x5a5113ba, 0x2e4bf22f, 0x90252118, 0xb8ad6b88, 0x6f3ef0c6,
    0x36f332b9, 0x4c6684e4, 0xf31a5d8b, 0x99c9b271, 0x48dd1f9d, 0x19ad2dd1, 0x79a7a518, 0x015ab8b5,
    0xce59bbf6, 0x37d2e9a0, 0x11942ce9, 0x8863d908, 0xd091b65c, 0xfed353c6, 0x9d6c7d6b, 0x7f6d9b03,
    0x800a57af, 0x8ddabec7, 0x9fe8f7f1, 0x5b5afc9f, 0xba45a35a, 0x71bd8e4d, 0xd7e9c0bd, 0x0a5d8a9c,
    0x7b4b96b8, 0x5b3c3d1c, 0x7e7bcc86, 0x8e8b6207, 0xdeafac29, 0x5c6a624b, 0xe5ae6e7c, 0x6c1efad1,
    0xc5ab1bb8, 0x77a51725, 0x4b25b7b8, 0xd391e8c7, 0x0cd3aad0, 0xd829b8e1, 0x52d7a7ac, 0x8c861b95,
    0x2a8909a6, 0x1c3e2f27, 0x8b6b6e3b, 0x4e6cd938, 0x3f7ba8d9, 0x57b0e5dc, 0xb1a5c4ae, 0x3eab3e8c,
    0x1e7a49c3, 0x647db6b6, 0x3ae5d395, 0x8f5ba3d1, 0x8d8c9e9d, 0x8c6a1a6b, 0x7c5b3a99, 0x4a5e4664,
    0xb6b6e363, 0x2f4e8b9d, 0x9d1a7a28, 0x53b8d4e1, 0x4f5a2f3b, 0x9db0d7e3, 0x8b4c4e7b, 0x2e6b05ad,
    0x5c9f02d8, 0x4a930f89, 0x8d4c1970, 0x8f2bbbc5, 0x1e52d29c, 0x2af6d5cc, 0x8d6d2ddc, 0x0ef7f5f0,
    0x5b8b8f8e, 0x6a7a7b5c, 0x2d8b8f8f, 0x8e7a7b5d, 0x5c9f02d9, 0x4a930f8a, 0x8d4c1971, 0x8f2bbbc6,
    0x1e52d29d, 0x2af6d5cd, 0x8d6d2ddd, 0x0ef7f5f1, 0x5b8b8f8f, 0x6a7a7b5d, 0x2d8b8f90, 0x8e7a7b5e,
    0x5c9f02da, 0x4a930f8b, 0x8d4c1972, 0x8f2bbbc7, 0x1e52d29e, 0x2af6d5ce, 0x8d6d2dde, 0x0ef7f5f2,
    0x5b8b8f90, 0x6a7a7b5e, 0x2d8b8f91, 0x8e7a7b5f, 0x5c9f02db, 0x4a930f8c, 0x8d4c1973, 0x8f2bbbc8,
    0x1e52d29f, 0x2af6d5cf, 0x8d6d2ddf, 0x0ef7f5f3, 0x5b8b8f91, 0x6a7a7b5f, 0x2d8b8f92, 0x8e7a7b60,
    0x5c9f02dc, 0x4a930f8d, 0x8d4c1974, 0x8f2bbbc9, 0x1e52d2a0, 0x2af6d5d0, 0x8d6d2de0, 0x0ef7f5f4,
    0x5b8b8f92, 0x6a7a7b60, 0x2d8b8f93, 0x8e7a7b61, 0x5c9f02dd, 0x4a930f8e, 0x8d4c1975, 0x8f2bbbca,
    0x1e52d2a1, 0x2af6d5d1, 0x8d6d2de1, 0x0ef7f5f5, 0x5b8b8f93, 0x6a7a7b61, 0x2d8b8f94, 0x8e7a7b62,
    0x5c9f02de, 0x4a930f8f, 0x8d4c1976, 0x8f2bbbcb, 0x1e52d2a2, 0x2af6d5d2, 0x8d6d2de2, 0x0ef7f5f6,
    0x5b8b8f94, 0x6a7a7b62, 0x2d8b8f95, 0x8e7a7b63, 0x5c9f02df, 0x4a930f90, 0x8d4c1977, 0x8f2bbbcc,
    0x1e52d2a3, 0x2af6d5d3, 0x8d6d2de3, 0x0ef7f5f7, 0x5b8b8f95, 0x6a7a7b63, 0x2d8b8f96, 0x8e7a7b64,
    0x5c9f02e0, 0x4a930f91, 0x8d4c1978, 0x8f2bbbcd, 0x1e52d2a4, 0x2af6d5d4, 0x8d6d2de4, 0x0ef7f5f8,
    0x5b8b8f96, 0x6a7a7b64, 0x2d8b8f97, 0x8e7a7b65, 0x5c9f02e1, 0x4a930f92, 0x8d4c1979, 0x8f2bbbce,
    0x1e52d2a5, 0x2af6d5d5, 0x8d6d2de5, 0x0ef7f5f9, 0x5b8b8f97, 0x6a7a7b65, 0x2d8b8f98, 0x8e7a7b66,
    0x5c9f02e2, 0x4a930f93, 0x8d4c197a, 0x8f2bbbcf, 0x1e52d2a6, 0x2af6d5d6, 0x8d6d2de6, 0x0ef7f5fa,
    0x5b8b8f98, 0x6a7a7b66, 0x2d8b8f99, 0x8e7a7b67, 0x5c9f02e3, 0x4a930f94, 0x8d4c197b, 0x8f2bbbd0,
    0x1e52d2a7, 0x2af6d5d7, 0x8d6d2de7, 0x0ef7f5fb, 0x5b8b8f99, 0x6a7a7b67, 0x2d8b8f9a, 0x8e7a7b68,
    0x5c9f02e4, 0x4a930f95, 0x8d4c197c, 0x8f2bbbd1, 0x1e52d2a8, 0x2af6d5d8, 0x8d6d2de8, 0x0ef7f5fc,
    0x5b8b8f9a, 0x6a7a7b68, 0x2d8b8f9b, 0x8e7a7b69, 0x5c9f02e5, 0x4a930f96, 0x8d4c197d, 0x8f2bbbd2,
    0x1e52d2a9, 0x2af6d5d9, 0x8d6d2de9, 0x0ef7f5fd, 0x5b8b8f9b, 0x6a7a7b69, 0x2d8b8f9c, 0x8e7a7b6a,
    0x5c9f02e6, 0x4a930f97, 0x8d4c197e, 0x8f2bbbd3, 0x1e52d2aa, 0x2af6d5da, 0x8d6d2dea, 0x0ef7f5fe,
    0x5b8b8f9c, 0x6a7a7b6a, 0x2d8b8f9d, 0x8e7a7b6b, 0x5c9f02e7, 0x4a930f98, 0x8d4c197f, 0x8f2bbbd4,
    0x1e52d2ab, 0x2af6d5db, 0x8d6d2deb, 0x0ef7f5ff, 0x5b8b8f9d, 0x6a7a7b6b, 0x2d8b8f9e, 0x8e7a7b6c,
]

def buzhash(data: bytes, window_size: int = 64) -> int:
    if len(data) < window_size:
        return 0
    h = 0
    for i in range(window_size):
        h ^= BUZHASH_TABLE[data[i]]
    return h

def rolling_hash(data: bytes, window_size: int = 64) -> int:
    return buzhash(data, window_size)

def chunk_iter(path: str, chunk_size: int = DEFAULT_CHUNK_SIZE, use_cdc: bool = False) -> Iterator[Dict[str, Any]]:
    with open(path, 'rb') as f:
        i = 0
        buffer = b''
        while True:
            b = f.read(4096)  # Read in chunks
            if not b:
                if buffer:
                    h = hashlib.sha256(buffer).hexdigest()
                    yield {"hash": f"sha256:{h}", "size": len(buffer), "order": i, "bytes": buffer}
                break
            buffer += b
            if use_cdc:
                # Simple CDC: split when rolling hash % 1024 == 0 or buffer too large
                if len(buffer) >= chunk_size or (len(buffer) >= 64 and rolling_hash(buffer[-64:]) % 1024 == 0):
                    h = hashlib.sha256(buffer).hexdigest()
                    yield {"hash": f"sha256:{h}", "size": len(buffer), "order": i, "bytes": buffer}
                    buffer = b''
                    i += 1
            else:
                # Fixed size
                while len(buffer) >= chunk_size:
                    chunk = buffer[:chunk_size]
                    h = hashlib.sha256(chunk).hexdigest()
                    yield {"hash": f"sha256:{h}", "size": len(chunk), "order": i, "bytes": chunk}
                    buffer = buffer[chunk_size:]
                    i += 1
        if buffer and not use_cdc:
            h = hashlib.sha256(buffer).hexdigest()
            yield {"hash": f"sha256:{h}", "size": len(buffer), "order": i, "bytes": buffer}

def manifest_for_file(path: str, chunk_size: int = DEFAULT_CHUNK_SIZE, name: Optional[str] = None, media_type: str = "application/octet-stream", use_cdc: bool = False) -> Dict[str, Any]:
    chunks = []
    total = 0
    for c in chunk_iter(path, chunk_size, use_cdc):
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

