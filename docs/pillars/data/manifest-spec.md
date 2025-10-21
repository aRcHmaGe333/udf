# Content Map (Index) Specification (Draft)

(formerly referred to as a "manifest")

Format: JSON (human-readable), with room for a compact binary form later. Consider a Merkle tree to verify subranges.

Example:
```
{
  "version": "1.0",
  "id": "urn:udf:content-map:sha256:...", 
  "created_at": "2025-10-21T14:00:00Z",
  "media_type": "application/octet-stream",
  "total_size": 52428800,
  "chunks": [
    {"hash": "sha256:abc...", "size": 4194304, "order": 0},
    {"hash": "sha256:def...", "size": 4194304, "order": 1}
  ],
  "integrity": {"root_hash": "sha256:...", "algo": "sha256", "tree": "merkle|concat"},
  "metadata": {"name": "sample.bin", "tags": ["example"]}
}
```

Notes:
- Hash: SHA-256 of chunk bytes; identical bytes = identical hash. Optionally combine with CDC (content-defined chunking) for binary formats.
- Order: reconstructs original content; optional for unordered datasets.
- Root hash: hash of concatenated chunk hashes or a Merkle root; enables tamper detection and partial verification.
- Extensibility: support for Parquet/table content maps via references.
