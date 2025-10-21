# Locator Design (Draft)

Purpose: Given a chunk hash, return the nearest healthy replicas and short-lived signed URLs for retrieval.

Inputs:
- Chunk hash (e.g., sha256:...)
- Client hint (region/city/IP ASN) or auth principal

Outputs:
- Ordered list of candidate locations with latency/cost hints
- Signed URLs (HTTPS) or credentials for fetch

Responsibilities:
- Health/latency awareness
- Policy filtering (optional): respect trust boundaries
- Caching: responses are cacheable for a short TTL

Implementation options:
- Simple: hash ring / DHT mapping to store nodes
- Advanced: geo-aware routing + CDN edge

