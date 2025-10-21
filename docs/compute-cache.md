# Action → Outcome Cache (Deterministic Compute)

Plain English
- Don’t re-run expensive work when the inputs and the requested action are the same. Reuse the prior outcome.
- Key idea: hash the action + inputs + environment to get a task key; if we’ve done this before, return the stored output (by manifest) instead of recomputing.

When it works
- Deterministic actions (same inputs → same outputs): compression, transcoding with fixed params, sorting, feature engineering steps, aggregations.
- Not for non-deterministic actions unless you capture and fix all sources of randomness.

Task key (content-addressed compute)
- Components (normalized and hashed):
  - `action`: name + version (e.g., `gzip@1` or `sort@utf8-casefold@1`)
  - `params`: flags that change the result (e.g., mtime=0 for gzip determinism)
  - `input_manifest`: the manifest ID of input content
  - `env`: minimal fingerprint (e.g., `python-3.11`, OS family)

What is stored
- Result index: `task_key → output_manifest_id`
- Output content stored as chunks as usual; fetched by manifest like any other artifact.

Flow
```mermaid
sequenceDiagram
  participant C as Client
  participant S as UDF Server
  Note over C: Build task_key(action, params, input_manifest, env)
  C->>S: GET /results/<task_key>
  alt hit
    S-->>C: { manifest: <id> }
    C->>S: GET /manifests/<id> … GET /chunks/…
    C->>C: Verify, return output
  else miss
    C->>C: Run action locally (deterministic)
    C->>S: PUT /chunks/…; PUT /manifests/<out_id>
    C->>S: PUT /results/<task_key> { manifest: <out_id> }
  end
```

Integrity & trust
- Client verifies chunk hashes as usual.
- Determinism contracts should be documented per action (e.g., `gzip` with `mtime=0`).
- Optional receipts later: who computed it, when, tool version.

Limits & caveats
- Task key correctness relies on including every parameter that affects output.
- Non-determinism (timestamps, locale, RNG) must be fixed or nulled in params.

Next steps
- Add receipts and basic provenance to result entries.
- Add a shared cache directory to client for offline reuse.
- Multi-node demo: two servers, cross-lookup for results.

