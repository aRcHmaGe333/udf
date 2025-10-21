# UDF Pillars

UDF has three co-equal pillars that share the same primitives (content addressing + content maps/indexes):

- UDF-Data: Store once as chunks, move only changes, serve from the nearest healthy source, and cache hot bytes.
  - Start: `docs/pillars/data/architecture.md`
  - Specs: `docs/pillars/data/manifest-spec.md`, `docs/pillars/data/locator-design.md`, `docs/pillars/data/cache-design.md`, `docs/pillars/data/erasure-coding.md`, `docs/pillars/data/table-integration.md`

- UDF-Compute: Reuse outcomes of deterministic actions via task keys (action + params + input + env → result content map).
  - Start: `docs/pillars/compute/compute-cache.md`
  - Determinism: `docs/pillars/compute/determinism-contract.md`

- UDF-Devices: Capture reusable modifiers (operators like IR/FIR/IIR/LUT/models) and apply deterministically.
  - Start: `docs/pillars/devices/operators.md`
  - Provenance: `docs/pillars/devices/operator-provenance.md`

