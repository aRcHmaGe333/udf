# Plain-English Overview

- Store once, reference everywhere: split data into chunks; same bytes share the same hash; store unique chunks once.
- Move only what changed: updates send only changed chunks (delta sync).
- Keep hot data close: cache frequently used chunks near users/compute.
- Make mistakes survivable: manifests are append-only; old versions remain; safe garbage collection prevents loss.
- Governance is optional: non-sensitive data in a trusted domain can be wide-open for reads; add policy where needed.

Core pieces:
- Chunks and hashes (content-addressed storage)
- Manifests (a version = ordered chunk hashes)
- Locator (find nearest replica of a hash)
- Cache (store hot chunks locally)
- Erasure coding (redundancy without 3x replication)

Next: See examples of space/network savings in `docs/value-examples.md`.

