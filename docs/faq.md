# FAQ

Q: Why not just compress?
A: Compression helps once per copy. Dedup stores identical chunks once across many files/systems; delta sync avoids re-sending unchanged chunks.

Q: Do I need governance?
A: Not for non-sensitive data in a trusted domain. Add lightweight write permissions and audit to reduce blast radius; add more only if required.

Q: How do remote references work?
A: A manifest lists chunk hashes; a locator returns nearest replicas and signed URLs; client fetches, verifies hashes, and caches.

Q: What about tiny updates?
A: Delta sync moves only changed chunks; small edits transfer a small fraction of bytes.

Q: Is this feasible today?
A: Yes. All building blocks exist; the value is combining them cleanly.

Q: Isn’t this already optimized by CDNs and updaters?
A: CDNs bring data closer but still ship whole files per URL. Many updaters still deliver full binaries. UDF uses content hashes so identical chunks across versions/apps share caches, and updates fetch only changed chunks.

Q: What saves the most — chunking, caching, or coding tricks?
A: Chunking+dedup is the primary lever (often 30–70% storage saved). Delta-on-chunks cuts WAN for small edits by 80–99%. Caching multiplies wins because popular chunks come from nearby edges/LAN.

Q: How can you serve chunks “closer to the PC”?
A: Edge/LAN caches store chunks by hash; a locator picks the nearest healthy source (Anycast/GeoDNS/CDN or self‑hosted edges). Clients verify hashes and cache locally.

Q: Why mention “analysts” — who benefits, really?
A: Many roles do. App/Service teams get stable reads; ML/DS get reproducible, delta‑friendly data; Backup/DR gets space savings; Security/Gov gains fewer stray copies and auditability.

Q: Why do rights/policies matter if the goal is efficiency?
A: Rights prevent accidental overwrites and limit blast radius. Reads can be open for non‑sensitive data; add policy only where required. Immutability + manifests already protect integrity.

Q: Are compute-cache and operator/IR reuse part of UDF?
A: Yes. UDF has three co‑equal pillars: Data (store once, move less), Compute (reuse outcomes via task keys), and Devices (reuse modifiers via operator manifests). All share content addressing and manifests.

Q: Can access be effectively denied when needed?
A: Yes with encryption and tokens. Strongest: client‑side envelope encryption per chunk with key control (revocation via key rotation). Operational: token‑gated endpoints with short TTL.
