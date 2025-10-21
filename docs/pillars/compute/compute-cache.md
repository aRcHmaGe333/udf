# Compute Cache (Action → Outcome)

Overview
- Skip repeated work: same action+params+inputs+env → same result content map (index).
- On hit: return the prior result content map and fetch chunks as usual.
- On miss: compute deterministically, publish content map, and record the task key.

Reference
- See `docs/reference-impl.md` and `ref/compute_cache.py` for a minimal demo.
- Higher-level concepts: `docs/pillars/compute/determinism-contract.md`.

