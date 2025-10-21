# Ethics, Access, and Denial Effectiveness

Intent
- UDF is a general-purpose fabric for reuse (bytes, outcomes, modifiers). With reuse comes power dynamics: who can access, and can access be effectively denied when needed?

Design posture
- Separation of concerns: keep UDF-Core usable without policy for non-sensitive data. Add protection where required.
- “Effective denial” means: without the right keys/tokens, content is unreadable or endpoints refuse service.

Mechanisms (from strongest → operational)
- Cryptographic control (strongest):
  - Client-side envelope encryption per chunk (keys in KMS). Without keys, bytes are useless even if fetched.
  - Key rotation for revocation; cryptographic erasure for deletes.
- Token-gated endpoints (operational):
  - Signed tokens required for `GET/PUT` to chunks/manifests/results.
  - Short TTL; purpose-bound claims; server-side allowlists.
- Topology control:
  - Keep sensitive datasets inside trust boundaries (region/org) with no external replicas.
  - Air-gap or private links for sensitive flows.
- Audit & deterrence:
  - Immutable logs and watermarking to discourage misuse.

Trade-offs
- Strong crypto limits global dedupe across tenants (unless convergent encryption with known risks). Prefer per-boundary dedupe.
- Tokens can be leaked; pair with least privilege, short TTL, and rotation.

Recommended defaults
- Non-sensitive: open reads inside trust boundary, token-gated writes.
- Sensitive: envelope encryption per chunk; token-gated endpoints; audit.

Denial effectiveness scorecard (guidance)
- Open reads, no crypto: weak denial; rely on network controls.
- Tokens only: medium denial; operationally strong with rotation.
- Envelope encryption + tokens: strong denial; revocation via key rotation.

Next steps
- Reference: add optional token checks in the demo server.
- Reference: add client-side encryption demo (envelope) and key stub.

