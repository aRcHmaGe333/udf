# Value Examples (Small Scale, Measured)

These demos use tiny files to show the math. See `examples/` for scripts.

## 1) Deduplication (store once)
- Setup: Three 10 MB files share ~60% identical content across them.
- Without dedupe: 30 MB stored.
- With dedupe: ~12 MB unique chunks stored + small manifests.
- Savings: ~60% space reduction; future copies reference existing chunks.

Try it: `python examples/dedupe_demo.py examples/data/*.txt`
Outputs unique-bytes stored vs total-bytes and dedupe ratio.

## 2) Delta Sync (move only changes)
- Setup: Edit ~1% of a 50 MB file (e.g., fix metadata, small patch).
- Full re-upload: 50 MB across the network.
- Delta upload: ~0.5 MB (only changed chunks).
- Savings: ~99% transfer reduction on small edits.

Try it: `python examples/delta_demo.py examples/data/sample1.txt examples/data/sample1_edited.txt`

## 3) Caching (keep hot data near use)
- Setup: Workload reuses 80% of chunks across runs.
- Without cache: 100% fetched over WAN.
- With cache: ~80% served locally; WAN transfer ~20% of baseline.

Try it: `python examples/cache_sim.py`

## 4) Erasure Coding vs Replication
- 3x replication: 3 TB to protect 1 TB (200% overhead).
- 6+3 erasure coding: ~1.5 TB to protect 1 TB (~50% overhead) with similar fault tolerance.

Note: Numbers vary with chunk size, workload mix, and fault-tolerance targets, but the direction holds across scales.

