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

# Yield Model (Plain-English)

Goal: make each unit of RAM, SSD, and network deliver more real work by adding "prepared" readiness, not just storing more bytes.

Core idea
- Keep only the truly hot working set in RAM.
- Track the near-future set as intent-only entries (hash + source + path), ready to materialize on demand.
- Use the locator to pre-resolve "where" so the fetch path is short when needed.
- Materialize only when the workload signal crosses a confidence threshold.

What success looks like
- Fewer stalls without bloating RAM.
- Lower tail latency on repeated or predictable access patterns.
- More predictable IO because fetches are planned, not reactive.
- Clear ROI math that picks the best mix of RAM, SSD, and network.

Decision loop (plain terms)
- Predict the next window of chunks or results.
- Pre-resolve location and access, store intent-only metadata.
- Materialize only when a request is imminent.
- Measure hits, misses, and cost; update thresholds.

# Yield Model (Math Sketch)

Define a simple model to compare resource mixes.

Variables
- W: hot working set bytes (must be in RAM)
- P: prepared set bytes (intent-only metadata size)
- S: storage fetch throughput (bytes/s)
- R: RAM bandwidth (bytes/s)
- L: median fetch latency (s)
- Hm: materialized cache hit rate
- Hp: prepared-hit rate (intent exists, data not yet materialized)
- M: miss rate (no intent, cold path)
- Cram, Cssd, Cnet: cost per unit of RAM, SSD, network

Latency model (per access)
- T_hit = size / R
- T_prep = L + size / S
- T_miss = L + size / S + lookup_overhead
- Expected latency: T = Hm*T_hit + Hp*T_prep + M*T_miss

Worked example (small numbers)
- size = 256 KB, R = 20 GB/s, S = 2 GB/s, L = 3 ms, lookup_overhead = 1 ms
- Hm = 0.60, Hp = 0.25, M = 0.15
- T_hit = 0.000013 s, T_prep = 0.003125 s, T_miss = 0.004125 s
- Expected T = 0.60*0.000013 + 0.25*0.003125 + 0.15*0.004125
  = ~0.00140 s (1.40 ms)

Cost proxy (per period)
- Cost = Cram*W + Cssd*SSD_capacity + Cnet*WAN_bytes
- SSD_capacity includes materialized cache + a small budget for prepared metadata.

Yield metric (illustrative)
- Yield = (baseline_latency - T) / Cost
- Goal: maximize Yield subject to SLOs (e.g., P99 latency).

# Prototype / Simulator Outline

Inputs
- Workload trace or synthetic pattern (sequential, random, bursty)
- Chunk size, manifest size, access window
- Resource caps (RAM, SSD, network)
- Predictor quality (precision/recall for "will need")

Loop
- Build manifests and chunk IDs for each workload step.
- Predict near-future chunk set and store intent-only entries.
- Resolve locator targets and access paths.
- Materialize on threshold or access request.
- Track hit rates, latency, IO, and energy proxies.

Outputs
- Prepared-hit rate vs materialized-hit rate
- Latency distribution (P50/P95/P99)
- IO costs (bytes moved, SSD reads, WAN reads)
- Sensitivity curves: how results change with more RAM, SSD, or better prediction

Prototype milestones
- Phase 1: spreadsheet or Python sim for a single workload trace.
- Phase 2: add a simple locator latency model and TTL expiry.
- Phase 3: integrate with UDF reference implementation for real traces.
- Starter script: `scripts/udf_yield_sim.py`

# Wear and Yield Policy (Draft)

Goal: keep readiness cheap while moving write-heavy churn off fragile local SSDs.

Action by certainty
- Structural certainties: always pre-resolve; prefetch only if reuse is guaranteed.
- Constrained certainties: pre-resolve; prefetch within tight budgets.
- Speculative guesses: metadata-only, strict caps, fast eviction.

Where costs should land
- Local SSD: reads and short-lived hot materializations only.
- Shared edge/cloud tiers: write-heavy churn, logs, and repeated materialization.
- RAM: hot working set and short-lived readiness maps.

Wear-aware knobs
- Batch metadata writes; avoid random tiny updates.
- Use hysteresis to prevent hydrate/evict oscillation.
- Separate "prepared" metadata storage from bulk bytes.
