# UDF Reference Implementation (Minimal)

This is a tiny, no-deps Python prototype to exercise chunking, manifests, a local HTTP chunk store + manifest service, and a basic client.

- Server: `ref/server.py`
- Client CLI: `ref/client.py`
- Shared utils: `ref/chunker.py`, `ref/manifest.py`

Quick start
- Start server: `python ref/server.py --root .udf_store --port 8080`
- Push a file: `python ref/client.py push path/to/file.bin --server http://localhost:8080`
- Fetch it back: `python ref/client.py fetch <manifest_id> --server http://localhost:8080 -o out.bin`

Notes
- Fixed-size chunks (default 4MB)
- Hash algo: SHA-256
- Manifest ID = SHA-256 Merkle-like root over chunk hashes (concatenation for simplicity)

See `docs/reference-impl.md` for details and diagrams.

