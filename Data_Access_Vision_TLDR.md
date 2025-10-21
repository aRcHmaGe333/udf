**What We’re Building (Plain English)**
- Store data once as chunks, reuse everywhere by reference. Move only what changed. Cache hot data near where it’s used.
- Keep this as a low-level, efficiency-first track. Governance/access is a separate, optional track that can be layered on when/where needed.

**Tracks (Kept Separate, Can Be Combined)**
- Universal Data Fabric (core): content-addressed chunks, manifests, delta sync, caching, erasure coding, versioning, safe GC.
- Governed Access (optional): pre-agreed rules, auto-approvals, masking/audit. Helps safety and speed but is not required for the core fabric to work.

**Core Mechanics (Storage + Transfer)**
- Content-addressed chunks: split files/tables into chunks (e.g., 4–8MB). Each chunk gets a hash (its fingerprint). Same content = same hash.
- Single storage per unique chunk: if a chunk exists anywhere in the fabric, don’t re-store it; just reference it in a manifest.
- Manifests: lightweight lists of chunk hashes that define a file/table/version.
- Delta sync: updates send only changed chunks; unchanged hashes are reused.
- Caching: keep frequently read chunks on nearby nodes; evict by size/TTL.
- Erasure coding: redundancy with less overhead than full copies.
- Versioning: immutable manifests per version (append-only); easy rollback.
- Safe GC: reference counts + retention windows to avoid accidental loss.

**Why (and When) Rights/Policies Matter**
- Writes need protection: with many writers, rights prevent accidental overwrite and coordinate who can publish new manifests.
- Immutability by design: content hashes + append-only manifests make “the precious chunk” hard to corrupt; writes create new versions.
- Blast-radius control: rights stop one bad actor/process from breaking 10 systems.
- Reads don’t require heavy policy: for non-sensitive data in a trusted domain, open read is fine. Add policy only where regulation/risk requires it.

**How a Remote Reference Works (NY server → Istanbul PC)**
1) The Istanbul PC needs file F. It fetches the manifest (list of chunk hashes) via a gateway/locator.
2) For each needed chunk hash, the locator returns the nearest replicas (NY, London, Frankfurt, etc.) and a signed HTTPS URL.
3) The PC downloads missing chunks from the nearest healthy location (e.g., Frankfurt), validates hashes, and caches them locally.
4) Future reads are served from the local cache; only new/changed chunks cross the WAN.
5) Transport is standard HTTPS/gRPC with range requests—NAT/firewall friendly. If no replica is nearby, it falls back to NY.

**Stakeholders (Not Just Analysts)**
- App/Service teams: stable, cached reads; fewer bespoke pipelines.
- ML/DS: versioned training data; only re-fetch deltas; reproducibility.
- Backup/DR: dedupe + erasure coding reduce space and speed restores.
- Operations/SRE: predictable failover domains; integrity checks.
- Security/Gov (optional): fewer uncontrolled copies; audit when needed.

**Feasibility Today**
- All pieces exist: content-addressed stores, dedupe, delta sync, caches, lakehouse table formats. No breakthrough required.
- Novelty is in the combo: a global, policy-aware content fabric with manifests + nearest-replica routing and optional governance.

**Tiny Pilot (10 Weeks)**
- Weeks 0–2: Pick 2–3 datasets. Produce manifests, versioning, and docs. Turn on local cache.
- Weeks 2–6: Enable chunking+dedupe+delta on the biggest asset; stand up a simple locator service; add erasure coding in one region.
- Weeks 6–10: Add nearest-replica routing and WAN-optimized fetch; track cache hit rate and dedupe ratio.
- Metrics: storage saved (dedupe%), transfer saved (delta%), median fetch time, cache hit%, integrity failures (should be 0).

**Open Questions**
- Chunk size defaults and when to adapt (small-write workloads).
- Trust boundary: per team/region/org for dedupe? Cross-tenant later?
- Gateway shape: S3-compatible API, FUSE/NFS driver, or both?
- Table integration: Parquet/Iceberg/Delta manifests mapped to chunk manifests.

**Non-Goals (for Now)**
- Cross-tenant convergent encryption (security tradeoffs). Start within a trusted boundary.
- Sub-millisecond, cross-planet writes. Prioritize read optimization and delta updates first.

**Simple Glossary**
- Chunk: a piece of a file/table.
- Hash: fingerprint of a chunk/content.
- Manifest: list of chunk hashes that define a version.
- Delta: only the changed chunks.
- Cache: keep hot chunks nearby.
- Erasure coding: space-efficient redundancy.
