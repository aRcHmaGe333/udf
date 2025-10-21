# Table Integration (Parquet/Iceberg/Delta)

Approach:
- Treat Parquet files as sequences of chunks; store once by hash.
- Table manifests (Iceberg/Delta) reference parquet files; extend to reference chunk manifests directly.
- Time travel: old manifests retained; GC honors table retention policies.

Benefits:
- Dedup across tables/partitions when content repeats.
- Delta updates move only changed parquet chunks.

