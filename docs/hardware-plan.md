# Hardware Plan & Deployment Tiers (Draft)

Goal: keep this idea-first and map it to pragmatic hardware you can buy today. Sizes are indicative and assume efficient implementation; adjust by workload.

Key components
- Edge cache node: Serves repeat reads locally. Needs fast NVMe and modest CPU.
- Storage node (chunk store): Persists unique chunks with erasure coding. Needs disk capacity, some NVMe for metadata/journal, and CPU for hashing.
- Manifest service: Light metadata + API. Low CPU/RAM; HA pair or small cluster.
- Locator service: Latency/health-aware routing. Low CPU/RAM; HA pair or small cluster.

Sizing knobs
- Chunk size: 4–8 MB typical. Smaller chunks improve deltas for random edits but increase index overhead.
- Hashing throughput: Modern CPUs with SHA extensions can exceed 10–20 Gbit/s per socket; GPUs rarely needed.
- Cache size: Aim for 1–3× working set to reach >70% hit rates on reuse-heavy workloads.
- Erasure coding: 6+3 (~50% overhead) vs 3× replication (200%). Choose by durability SLOs.

Reference tiers (per site)
- Small (single team / lab)
  - 1× edge cache node: 8 cores, 32 GB RAM, 2 TB NVMe
  - 2× storage nodes: 8 cores, 64 GB RAM, 8× 8 TB HDD + 1 TB NVMe cache (ZNS optional)
  - Shared control (VMs/containers) for manifest + locator, or managed cloud services
- Medium (department)
  - 2–3× edge cache nodes: 16 cores, 64 GB RAM, 4–8 TB NVMe each
  - 4–6× storage nodes: 16 cores, 128 GB RAM, 12× 16 TB HDD + 2 TB NVMe per node
  - 3-node control plane for manifest + locator (HA)
- Large (org/site)
  - 4–8× edge cache nodes with 25/40/100 GbE, 8–16 TB NVMe each
  - 8–20× storage nodes, 24× 18–22 TB HDD, 2–4 TB NVMe, dual 25–100 GbE
  - Dedicated control plane (3–5 nodes), separate observability cluster

Network
- NICs: 10 GbE baseline; 25–100 GbE where WAN ingress/egress or intra-cluster traffic is high.
- WAN: HTTPS with range requests; consider private backbones or cloud interconnect for cross-region.

Security
- At-rest encryption with hardware AES; consider convergent encryption only within trusted boundary if cross-tenant dedupe is needed (tradeoffs apply).
- TLS with modern ciphers; mutual TLS for node-to-node traffic.

Notes
- Start small: one storage pair + one cache node proves value.
- Prioritize NVMe for cache/journal; use HDD for capacity in chunk store.
- Hash offload (Intel SHA, ARMv8 SHA) preferred; GPU offload generally unnecessary.

