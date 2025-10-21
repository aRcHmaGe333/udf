# Universal Data Fabric (working title)

Store data once as chunks; reference it everywhere. Move only what changed. Cache hot data near where it’s used. Governance is optional and layered.

- Start here (general audience): `docs/start-here.md`
- Plain-English overview: `docs/overview.md`
- What to read next (map): `docs/layers.md`
- Value with small demos: `docs/value-examples.md`
- Pillars overview: `docs/pillars/README.md`
- Data pillar: `docs/pillars/data/architecture.md`, `docs/pillars/data/manifest-spec.md`, `docs/pillars/data/locator-design.md`, `docs/pillars/data/cache-design.md`
- Compute pillar: `docs/pillars/compute/compute-cache.md`, `docs/pillars/compute/determinism-contract.md`
- Devices pillar: `docs/pillars/devices/operators.md`, `docs/pillars/devices/operator-provenance.md`
- Hardware plan and sizing: `docs/hardware-plan.md`
- Impact model (savings math): `docs/impact-model.md`
- Stack options: `docs/stack-options.md`
- Reference implementation (minimal Python): `docs/reference-impl.md`, `ref/`
- Quickstart: `docs/QUICKSTART.md`
- API Reference: `docs/api-reference.md`
- Ethics & access controls: `docs/ethics-and-access.md`
- Value by stakeholder: `docs/stakeholder-value.md`
- Optional governance & security: `docs/security-and-governance.md`
- Pilot plan & roadmap: `docs/pilot-plan.md`, `docs/roadmap.md`
- Contributing & stewardship: `CONTRIBUTING.md`, `docs/stewardship.md`
- Founder vision (adapted) and origins: `docs/vision/founder-vision.md`, `docs/vision/origins-notes.md`

## Why this exists
Most systems copy the same bytes many times. We split data into chunks, store unique chunks once, and let others reference them. Updates ship only changed chunks. Popular chunks are cached nearby. Result: less storage, less transfer, faster access.

## Who this is for
- General public: see `docs/start-here.md` and the value examples.
- Builders/engineers: explore `docs/architecture.md` and specs.
- Organizations: see the pilot plan, roadmap, and optional governance.

## Quick demo
- Small Python examples live in `examples/` to illustrate deduplication, delta sync, and caching benefits on tiny files.

## Status
Public, read‑first. Design docs and examples are WIP; reference implementations to follow. Contributions are paused while we finalize direction. See License/Contributing below.

## License & Permissions
- License: All Rights Reserved (see `LICENSE.txt`).
- You may view and link to this repository.
- Copying, modification, or redistribution requires written permission.

## Contributing (Paused)
- We are not accepting pull requests yet. Use the Feedback issue template to share use cases, questions, or corrections.
- Why contributions will matter later: reference client/server, connectors, workload validations, and benchmarks that prove value across contexts.
