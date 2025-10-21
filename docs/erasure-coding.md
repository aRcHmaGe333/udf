# Erasure Coding (Draft)

Why: Provide redundancy with lower overhead than full replication.

Example profile:
- 6+3 (k=6 data, m=3 parity) tolerates 3 failures; overhead ~50% vs 200% for 3x replication.

Guidelines:
- Apply within a failure domain (rack/zone) to limit blast radius.
- Keep at least one full copy for hot metadata/manifests when small.
- Rebuild priority for hot chunks.

