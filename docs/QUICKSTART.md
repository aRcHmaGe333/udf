# Quickstart

This walks you through running the minimal reference implementation and trying the demos.

Requirements
- Python 3.9+
- No external dependencies

1) Start the UDF server
- `python ref/server.py --root .udf_store --port 8080`

Optional: multi-node locator demo
- Create `ref/nodes.json` with peer servers (can list the same server for demo):
```
[
  {"url": "http://127.0.0.1:8080", "region": "local"},
  {"url": "http://127.0.0.1:8081", "region": "local"}
]
```
- Then start a second server on 8081: `python ref/server.py --root .udf_store2 --port 8081`

2) Push and fetch a file
- Push: `python ref/client.py push examples/data/sample1.txt --server http://localhost:8080`
- Copy the printed manifest ID
- Fetch: `python ref/client.py fetch <manifest_id> --server http://localhost:8080 -o out.txt`

3) Deterministic compute cache demo (gzip)
- `python ref/compute_cache.py gzip examples/data/sample1.txt --server http://localhost:8080 -o sample1.txt.gz`
- Run it again; it should hit the cached result

4) Operator demo (FIR)
- Create coeffs.txt with a few numbers (e.g., `0.5 0.5`)
- Create series.txt with numbers (e.g., `1 2 3 4`)
- `python ref/operator_apply.py --server http://localhost:8080 --coeffs coeffs.txt --input series.txt --out out.txt`

Notes
- Client has a simple local chunk cache at `~/.udf_cache`.
- Server exposes simple HTTP endpoints documented in `docs/api-reference.md`.

