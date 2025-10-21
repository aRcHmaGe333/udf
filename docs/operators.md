# Operator Manifests (Modifiers like Impulse Responses)

Idea
- Remember the altering factor, not just a single outcome. If you know the modifier (e.g., the combined effect of a room + speakers + amp), you can apply it to many inputs without the hardware.

Two classes
- Linear Time-Invariant (LTI) operators: impulse responses, FIR/IIR filters, convolution kernels. Reusable across inputs of the same domain.
- Nonlinear / context-dependent operators: compressors, saturators, learned effects; require parameter capture or a learned model.

Operator manifest
- `id`: `urn:udf:operator:sha256:<hash>` over a canonical JSON spec
- `type`: `fir`, `iir`, `lut`, `ml-model`
- `params`: coefficients, sample rate, units, bounds
- `provenance`: how it was measured/derived (devices, environment, date)
- Optional `applicability`: constraints (e.g., sample rate 48kHz, level ranges)

Flow
- To apply: compute `task_key = hash(operator_id, input_manifest, params, env)`
- Check `GET /results/<task_key>`; reuse output if present. Otherwise apply operator, store result, and record mapping.

Limits
- LTI assumptions must hold for pure impulse-response reuse. Nonlinear chains require parameterization or a model.
- Determinism: fix randomness and timestamps for stable keys.

Next
- Add receipts (who/when/tool) to results
- Add operator registry fields for validation and versioning
- Example: sample FIR operator applied to toy data sequence

