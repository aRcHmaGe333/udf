# Impact Model (Back-of-the-Envelope)

Inputs (example org)
- Total data under management: 1 PB
- Average dedupe across datasets: 45%
- Daily change rate (delta): 2%
- Cache hit rate on hot workloads: 70%
- Baseline 3× replication vs 6+3 erasure coding

Storage impact
- Baseline replicated: 1 PB × 3 = 3 PB stored
- With dedupe (unique bytes): 1 PB × (1 − 0.45) = 0.55 PB
- With 6+3 overhead (~1.5×): 0.55 PB × 1.5 ≈ 0.825 PB
- Net storage reduction vs baseline: ~72.5%

Network impact (daily updates)
- Baseline full re-ingest: 1 PB × 2% = 20 TB/day across WAN
- Delta sync (send only changed chunks): ~20 TB/day
- With edge cache (70% hits on reads): WAN read traffic reduced by 70% vs miss-only baseline

Latency/user impact
- Cold read: Nearest-replica fetch + verification; often within regional RTT
- Warm read: Served from local cache → seconds to milliseconds depending on size

Cost proxy (illustrative)
- Storage $/TB-month: compare (3 PB) vs (0.825 PB)
- Egress $/TB: multiply by avoided WAN reads (70% of repeated reads)

Notes
- Change the inputs to fit your workloads and re-run these simple calcs.
- Chunk size selection affects dedupe and delta precision; tune per dataset type.

