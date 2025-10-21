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

