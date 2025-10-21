#!/usr/bin/env python3
import json
from typing import Dict, Any

def validate_manifest(m: Dict[str, Any]) -> bool:
    required = ["version", "id", "total_size", "chunks", "integrity"]
    for k in required:
        if k not in m:
            raise ValueError(f"manifest missing field: {k}")
    if not isinstance(m["chunks"], list) or not m["chunks"]:
        raise ValueError("manifest has no chunks")
    return True

def save_manifest(path: str, m: Dict[str, Any]) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(m, f, indent=2)

def load_manifest(path: str) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

