# API Reference (Reference Implementation)

Base URL
- `http://<host>:<port>`

Endpoints
- `PUT /chunks/<hash>` — store a chunk (raw bytes)
- `GET /chunks/<hash>` — retrieve a chunk (raw bytes)
- `PUT /manifests/<id>` — store a content map (JSON; called "manifest" in API)
- `GET /manifests/<id>` — retrieve a content map (JSON)
- `GET /locate/<hash>` — return candidate URLs for a chunk (JSON: {candidates:[{url, latency_ms?}]})
- `GET /results/<task_key>` — return cached result mapping (JSON: {manifest, receipt?})
- `PUT /results/<task_key>` — record result mapping (JSON: {manifest, receipt?})
- `PUT /operators/<operator_id>` — store operator spec (JSON)
- `GET /operators/<operator_id>` — retrieve operator spec (JSON)
- `GET /health` — health probe

Notes
- Content maps were previously called "manifests"; the API path remains `/manifests` for compatibility.
- The locator returns the server itself unless `ref/nodes.json` is provided; then it returns multiple candidates sorted by region hint.

