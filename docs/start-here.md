# Start Here (General Audience)

- Problem: The same data gets copied over and over across devices, apps, and servers. That wastes space, bandwidth, and time.
- Idea: Split files/tables into chunks, give each chunk a fingerprint (hash), store unique chunks once, and let everything else reference them. When something changes, move only the changed chunks.
- Result: Less storage, less network transfer, faster access. Popular chunks are cached nearby.

What you’ll get here:
- Easy overview: `docs/overview.md`
- Quick value examples: `docs/value-examples.md`
- Skip the deep stuff unless you’re building — it’s there when you’re ready: `docs/architecture.md`

Optional topics (read only if relevant):
- Security/governance (for sensitive data): `docs/security-and-governance.md`
- Pilot plan & roadmap (for teams/orgs): `docs/pilot-plan.md`, `docs/roadmap.md`

Questions? See `docs/faq.md`.

