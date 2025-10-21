# Glossary (Simple)

- Chunk: A piece of a file/table.
- Hash: Fingerprint of content; same bytes = same hash.
- Manifest: List of chunk hashes describing a version of data.
- Delta: Only the changed chunks between versions.
- Cache: Local store of hot chunks for fast reuse.
- Erasure coding: Space-efficient redundancy (e.g., 6+3).
- Locator: Service that finds the nearest replica for a given chunk.

