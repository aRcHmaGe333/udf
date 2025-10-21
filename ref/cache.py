#!/usr/bin/env python3
import os, hashlib

DEFAULT_CACHE_DIR = os.path.join(os.path.expanduser('~'), '.udf_cache')

def cache_dir(path=None):
    d = path or os.environ.get('UDF_CACHE_DIR') or DEFAULT_CACHE_DIR
    os.makedirs(d, exist_ok=True)
    return d

def key_for_hash(h: str) -> str:
    # h is like sha256:abcd...
    return h.replace(':','_')

def get_chunk_from_cache(h: str, cache_path=None):
    d = cache_dir(cache_path)
    p = os.path.join(d, key_for_hash(h))
    if os.path.exists(p):
        return open(p,'rb').read()
    return None

def put_chunk_to_cache(h: str, data: bytes, cache_path=None):
    d = cache_dir(cache_path)
    p = os.path.join(d, key_for_hash(h))
    # simple write-through; no eviction policy in prototype
    with open(p,'wb') as f:
        f.write(data)

