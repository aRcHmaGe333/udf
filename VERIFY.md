# VERIFY.md — How to Verify an APC Claim

This document explains how anyone — the Author, a court, a competitor, a journalist, a machine — can independently verify that this Work existed in its exact form at the claimed date.

No special software is required beyond OpenSSL, which ships with virtually every operating system.

---

## What You're Verifying

An APC-licensed project contains a `.timestamps/` folder with proof files. Each proof file corresponds to a **Git tree hash** — a cryptographic fingerprint of the entire repository contents at a given commit.

The tree hash (not the commit hash) is used because it represents the actual file contents, stripped of manipulable metadata like author dates and commit messages. You cannot backdate a tree hash.

---

## Step-by-Step Verification

### 1. Recompute the Tree Hash

Clone or download the repository at the commit you want to verify. Then:

```bash
git rev-parse HEAD^{tree}
```

This gives you the tree hash. It should match the filename prefix in `.timestamps/`.

### 2. Verify the RFC 3161 Timestamp

Download the FreeTSA certificates (one-time):

```bash
wget https://freetsa.org/files/tsa.crt
wget https://freetsa.org/files/cacert.pem
```

Verify the timestamp token against the tree hash data:

```bash
echo -n "[TREE_HASH]" > /tmp/tree_hash.txt
openssl ts -verify \
  -in .timestamps/[TREE_HASH].tsr \
  -data /tmp/tree_hash.txt \
  -CAfile cacert.pem \
  -untrusted tsa.crt
```

If the output says `Verification: OK`, the proof is valid. The tree hash text file — and therefore the repository state represented by that tree hash — existed at the time stated in the token, as certified by an independent Time Stamping Authority.

### 3. (Optional) Verify OpenTimestamps Proof

If a `.ots` file is present:

```bash
pip install opentimestamps-client
ots verify .timestamps/[TREE_HASH].ots
```

This checks the proof against the Bitcoin blockchain. It provides a second, decentralized confirmation independent of any single TSA.

---

## What This Proves

| Question | Answer |
|---|---|
| Did these exact files exist at the claimed date? | Yes — the tree hash is bound to the timestamp by the TSA's cryptographic signature. |
| Could the files have been altered after timestamping? | No — any change to any file produces a different tree hash, which will not match the token. |
| Could the timestamp have been backdated? | No — the TSA's signature uses a verified UTC clock. Forging it would require compromising the TSA's private key. |
| Does verification require trusting the Author? | No — it requires trusting the math (SHA-512) and the TSA (an independent third party). Both are independently auditable. |
| Does verification require trusting GitHub? | No — the tree hash is computed from file contents, not from GitHub's metadata. You can verify it locally on a downloaded copy. |

---

## Merkle Root Verification (For Bundle Submissions)

If the Work was submitted through a bundling service (Stamped, ProofForge, or similar), the timestamped value may be a **Merkle root** rather than a Git tree hash.

A Merkle root is computed by:

1. Hashing each file individually (SHA-512).
2. Pairing hashes and hashing the pairs.
3. Repeating until a single root hash remains.

To verify:

```bash
# Recompute individual file hashes
sha512sum file1.md file2.py file3.png

# Compare against the manifest included in the bundle
# Then verify that the Merkle root in the manifest matches the timestamped hash
```

The Merkle root proves that **all files as a collection** existed at the timestamped moment. Changing, adding, or removing any file breaks the root.

---

## Automated Timestamping (GitHub Actions)

To automatically timestamp every push to `main`, add this file to your repository:

### `.github/workflows/timestamp.yml`

```yaml
name: APC Cryptographic Timestamp

on:
  push:
    branches: [main, master]

jobs:
  timestamp:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Generate tree hash and timestamp
        run: |
          TREE_HASH=$(git rev-parse HEAD^{tree})
          echo "Tree hash: $TREE_HASH"

          mkdir -p .timestamps

          # RFC 3161 timestamp via FreeTSA
          echo -n "$TREE_HASH" > /tmp/tree_hash.txt
          openssl ts -query -data /tmp/tree_hash.txt -no_nonce -sha512 -cert -out /tmp/request.tsq
          curl -s -H "Content-Type: application/timestamp-query" \
               --data-binary '@/tmp/request.tsq' \
               https://freetsa.org/tsr \
               -o .timestamps/${TREE_HASH}.tsr

          # Verify immediately
          wget -q https://freetsa.org/files/tsa.crt
          wget -q https://freetsa.org/files/cacert.pem
          openssl ts -verify \
            -in .timestamps/${TREE_HASH}.tsr \
            -queryfile /tmp/request.tsq \
            -CAfile cacert.pem \
            -untrusted tsa.crt

          echo "Timestamp verified for tree: $TREE_HASH"

      - name: Commit timestamp proof
        run: |
          git config user.name "APC Timestamp Bot"
          git config user.email "apc-bot@users.noreply.github.com"
          git add .timestamps/
          git diff --cached --quiet || git commit -m "[APC] Cryptographic timestamp proof added"
          git push
```

This creates a closed loop: every push generates a timestamped proof that is itself stored in the repository, forming a permanent, self-referencing chain of evidence.

---

## Summary

Verification requires no accounts, no fees, no permissions, and no trust in the Author or in any platform. It requires only:

- The files.
- The timestamp token.
- OpenSSL.
- Approximately 10 seconds.

That is what proof looks like when it is not behind a paywall.
