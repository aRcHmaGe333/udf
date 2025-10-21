#!/usr/bin/env python3
import os, hashlib
from typing import Optional
from collections import OrderedDict

DEFAULT_CACHE_DIR = os.path.join(os.path.expanduser('~'), '.udf_cache')
DEFAULT_CACHE_SIZE = 100  # max entries

class LRUCache:
    def __init__(self, max_size: int = DEFAULT_CACHE_SIZE):
        self.cache = OrderedDict()
        self.max_size = max_size

    def get(self, key: str) -> Optional[bytes]:
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return None

    def put(self, key: str, value: bytes) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)

_lru_cache = LRUCache()

def cache_dir(path: Optional[str] = None) -> str:
    d = path or os.environ.get('UDF_CACHE_DIR') or DEFAULT_CACHE_DIR
    os.makedirs(d, exist_ok=True)
    return d

def key_for_hash(h: str) -> str:
    # h is like sha256:abcd...
    return h.replace(':','_')

def get_chunk_from_cache(h: str, cache_path: Optional[str] = None) -> Optional[bytes]:
    # First check LRU
    data = _lru_cache.get(h)
    if data:
        return data
    # Then disk
    d = cache_dir(cache_path)
    p = os.path.join(d, key_for_hash(h))
    if os.path.exists(p):
        data = open(p,'rb').read()
        _lru_cache.put(h, data)  # add to LRU
        return data
    return None

def put_chunk_to_cache(h: str, data: bytes, cache_path: Optional[str] = None) -> None:
    # Add to LRU
    _lru_cache.put(h, data)
    # Write to disk
    d = cache_dir(cache_path)
    p = os.path.join(d, key_for_hash(h))
    with open(p,'wb') as f:
        f.write(data)

