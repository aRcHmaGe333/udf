# Operators (Reusable Modifiers)

Idea
- Remember the altering factor (e.g., impulse responses, FIR/IIR filters, LUTs, or learned effects) as an operator manifest and reapply deterministically.

Start here
- Background: `docs/operators.md`
- Provenance & constraints: `docs/pillars/devices/operator-provenance.md`

Application flow
- Build task key: hash(operator_id, input content map ID, params, env)
- Lookup result; reuse if present; else apply operator, publish result.

