# Cache Design (Draft)

Goal: Serve repeat reads locally to cut WAN transfer and latency.

Basics:
- Write policy: read-through for fetch; optional write-through on publish.
- Eviction: size-based LRU with TTL hints.
- Validation: always verify chunk hash on load.

Tuning:
- Chunk size trade-offs: 4–8MB common; smaller for random access workloads.
- Pre-fetch: predictive for sequential reads; disable for sparse access.

Interfaces:
- Local FS (FUSE/NFS) or S3-compatible gateway.

