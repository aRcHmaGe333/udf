# Determinism Contract (Outcome Reuse)

A result is reusable if the action is deterministic under a defined envelope.

Include in the task key:
- Action identity: tool name + version (e.g., `gzip@1`).
- Parameters: only those that change outputs (e.g., `mtime=0`).
- Inputs: content map (index) IDs of inputs.
- Environment: minimal fingerprint (OS family, runtime version).

Sources of non-determinism to control or include:
- Timestamps, locales, RNG seeds, thread scheduling, timezones.

Task key = hash(action, params, inputs, env). Same key → same result content map.

