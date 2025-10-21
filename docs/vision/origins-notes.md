# Origins Notes (Optional)

This note captures the original framing, translated to UDF terms for consistency.

- Make data chunks available locally by default; reduce or avoid downloads where possible.
- Use a universal comparison (hashing) to detect identical chunks across file types.
- Avoid repeated storage across systems; reference one stored chunk wherever needed.
- Apply the same idea locally on a single PC to save space and time.

These ideas are now expressed through UDF’s chunking, manifests, delta sync, and caching.

