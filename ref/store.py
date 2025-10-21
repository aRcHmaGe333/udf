#!/usr/bin/env python3
import os, json
from typing import Optional, Dict, Any


class Store:
    def __init__(self, root: str):
        self.root = root
        self.chunks = os.path.join(root, 'chunks')
        self.manifests = os.path.join(root, 'manifests')
        self.results_index = os.path.join(root, 'results.json')
        self.operators = os.path.join(root, 'operators')
        os.makedirs(self.chunks, exist_ok=True)
        os.makedirs(self.manifests, exist_ok=True)
        os.makedirs(self.operators, exist_ok=True)

    def chunk_path(self, h: str) -> str:
        safe = h.replace(':', '_')
        return os.path.join(self.chunks, safe)

    def has_chunk(self, h: str) -> bool:
        return os.path.exists(self.chunk_path(h))

    def put_chunk(self, h: str, data: bytes) -> None:
        p = self.chunk_path(h)
        if not os.path.exists(p):
            with open(p, 'wb') as f:
                f.write(data)

    def get_chunk(self, h: str) -> Optional[bytes]:
        p = self.chunk_path(h)
        if not os.path.exists(p):
            return None
        with open(p, 'rb') as f:
            return f.read()

    def manifest_path(self, mid: str) -> str:
        safe = mid.replace(':', '_')
        return os.path.join(self.manifests, safe + '.json')

    def put_manifest(self, mid: str, manifest: Dict[str, Any]) -> None:
        with open(self.manifest_path(mid), 'w', encoding='utf-8') as f:
            json.dump(manifest, f)

    def get_manifest(self, mid: str) -> Optional[Dict[str, Any]]:
        p = self.manifest_path(mid)
        if not os.path.exists(p):
            return None
        with open(p, 'r', encoding='utf-8') as f:
            return json.load(f)

    # Results index: task_key -> {manifest, receipt?}
    def get_result(self, key: str) -> Optional[Dict[str, Any]]:
        if not os.path.exists(self.results_index):
            return None
        try:
            with open(self.results_index, 'r', encoding='utf-8') as f:
                m = json.load(f)
        except Exception:
            return None
        val = m.get(key)
        if isinstance(val, dict):
            return val
        if val is None:
            return None
        return {"manifest": val}

    def put_result(self, key: str, manifest_id: str, receipt: Optional[Dict[str, Any]] = None) -> None:
        m = {}
        if os.path.exists(self.results_index):
            try:
                with open(self.results_index, 'r', encoding='utf-8') as f:
                    m = json.load(f)
            except Exception:
                m = {}
        entry: Dict[str, Any] = {"manifest": manifest_id}
        if receipt:
            entry["receipt"] = receipt
        m[key] = entry
        with open(self.results_index, 'w', encoding='utf-8') as f:
            json.dump(m, f)

    # Operators: store simple operator specs by id
    def operator_path(self, oid: str) -> str:
        safe = oid.replace(':', '_')
        return os.path.join(self.operators, safe + '.json')

    def put_operator(self, oid: str, spec: Dict[str, Any]) -> None:
        with open(self.operator_path(oid), 'w', encoding='utf-8') as f:
            json.dump(spec, f)

    def get_operator(self, oid: str) -> Optional[Dict[str, Any]]:
        p = self.operator_path(oid)
        if not os.path.exists(p):
            return None
        with open(p, 'r', encoding='utf-8') as f:
            return json.load(f)

