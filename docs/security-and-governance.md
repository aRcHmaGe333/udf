# Security & Governance (Optional Layer)

Use only where needed. The core fabric works without this for non-sensitive data in trusted domains.

Why add it:
- Prevent accidental overwrites (write auth)
- Limit blast radius of bad writes
- Comply with regulations (masking, audit)

Lightweight defaults:
- Immutability by default; new writes create new versions
- Write permissions per dataset
- Basic audit log of publishes and reads

Advanced (opt-in):
- Purpose-bound access with expirations
- Dynamic masking/tokenization for sensitive fields
- Clean-room joins without sharing raw data

