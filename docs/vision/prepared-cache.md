# Prepared Cache Vision

Core idea
- The cache is not only storage; it is readiness.
- It only needs to know it will need a chunk, not keep the chunk in RAM.
- When the time comes, it quickly swaps an identifier (hash) for bytes, so access feels local even when RAM stayed free.

What "prepared" means in UDF terms
- A manifest or query reveals the future working set (or likely subset).
- The system pre-resolves those chunk hashes to the best sources and access paths.
- The cache holds intent, location, and retrieval plans, not the full data.

Identifier-to-bytes swap
- A chunk hash is the stable identity.
- The prepared cache stores: best replica, authorization token, short path to fetch, and a disk slot if needed.
- On access, it performs a fast resolve + fetch + verify, then returns bytes as if already resident.

Not the same as prefetch
- Prefetch moves bytes early. Prepared cache moves resolution early and can keep bytes absent.

How it fits the current UDF stack
- Chunks + hashes: identity and verification remain the same.
- Manifests: supply the "will need" signal (entire file/table or upcoming segments).
- Locator: provides nearest healthy replicas and short-lived URLs.
- Cache: keeps hot chunks and can now also keep "prepared" metadata for imminent chunks.
- Compute cache: a "prepared" action can pre-resolve results by task key and keep the manifest ready.

Preparedness signals (inputs)
- Sequential reads (streaming, media, large scans).
- Pipeline hints (next stage manifests, query plans, batch windows).
- Recent locality (same user, same dataset, same location).
- Explicit client hints: "prepare these hashes, do not load yet."

Certainty classes (how strong is "will need")
- Structural certainties: manifests, query plans, declared pipelines.
- Constrained certainties: near-future windows (streaming, timelines, batch steps).
- Speculative guesses: popularity or heuristic hints.

Invariant
- Prepared cache acts on certainties when available, on bounded inevitabilities when constrained, and only speculates when cheap.

Benefits
- RAM stays available for active work, not speculative chunks.
- Cold data still feels warm because the path to it is pre-built.
- Network and disk IO become scheduled and predictable, reducing stalls.
- The system can scale with less memory pressure across devices.

Design implications
- Cache entries can be "intent-only" (metadata without bytes) or "materialized".
- Prefetch budgets should prioritize intent-first and materialize only on strong signals.
- Eviction can drop bytes while keeping intent for rapid rehydration.
- Observability should measure "prepared hit" vs "materialized hit".

State machine (minimal)
- Intent: ID plus resolve plan, no bytes.
- Resolved: ID plus current path/token/slot, still no bytes.
- Materialized: bytes present and verified.

Limits and guardrails
- Preparedness reduces latency; it does not eliminate it.
- Incorrect predictions must be cheap (metadata-only is the default).
- Hash verification remains mandatory on every materialization.
- TTLs prevent stale tokens and out-of-date paths.

Why this matters for UDF
- It extends UDF beyond caching as a storage technique into caching as a philosophy of readiness.
- It preserves the promise of "near-RAM" speed without hoarding RAM.
- It aligns with UDF's content-addressed identity and locator-driven retrieval.

Core spine (five sentences)
- Prepared cache is a readiness layer where identifiers stand in for bytes until the last responsible moment.
- It pre-computes the fastest verified path from ID to bytes (source, auth, route, verification plan, placement target).
- On access, the ID-to-bytes resolution is engineered to feel like a cache hit when prediction is correct and to be cheap when wrong.
- The objective is not to use less RAM, but to increase delivered performance per unit of RAM, IO, network, and energy.
- Caching becomes resource allocation under forecast, not a storage trick.
