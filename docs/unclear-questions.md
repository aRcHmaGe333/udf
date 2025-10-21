# Open Questions & Next Clarifications

- Content-defined chunking (CDC) vs fixed-size chunks for mixed workloads?
- Manifest format: JSON vs binary; Merkle tree structure for partial verification?
- Locator data source: DHT vs centralized index; integrating with existing CDNs?
- Trust boundary: organization-wide dedupe vs per-domain; convergent encryption posture?
- Table integration: direct chunk manifests vs file-level manifests for Parquet?
- Cache eviction: simple LRU vs cost-aware (latency/egress) policies?
- GC semantics: retention holds, legal hold integration, safe deletion proofs?
- Observability: metrics and tracing requirements per component; SLOs?
- Hardware constraints: minimal NVMe per TB to sustain target throughput?

