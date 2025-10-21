# Pilot Plan (10 Weeks)

- Weeks 0–2: Pick 2–3 datasets. Produce manifests, versions, docs. Turn on local cache.
- Weeks 2–6: Enable chunking+dedupe+delta on the largest asset; add a basic locator; use erasure coding in one region.
- Weeks 6–10: Nearest-replica routing + WAN-optimized fetch; measure.

Metrics:
- Dedupe% (unique-bytes / total-bytes)
- Delta savings% (transferred-bytes / baseline)
- Cache hit%
- Median fetch time
- Integrity failures (target 0)

