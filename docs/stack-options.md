# Stack Options (Implementation Choices)

Open-source building blocks
- Storage: SeaweedFS, MinIO (erasure coding), Ceph
- CAS/Dedup ideas: restic/borg internals, IPFS concepts
- Table: Apache Parquet + Iceberg/Delta/Hudi
- Query: Trino/Presto, DuckDB for local
- Cache: Alluxio, Nginx+FS cache, custom NVMe cache
- Orchestration: Kubernetes (optional), Nomad, or simple VMs
- Observability: Prometheus/Grafana, OpenTelemetry

Languages
- Reference client/server: Go or Rust (hashing performance, concurrency)
- Demos and tooling: Python

Gateways
- S3-compatible API for object pull/push
- FUSE/NFS for POSIX-like mounting

Security
- mTLS between nodes, OIDC for users; optional masking/tokenization layer

