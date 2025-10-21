#!/usr/bin/env python3
import argparse, os, sys, json, hashlib, urllib.request
from ref.chunker import chunk_iter, manifest_for_file


def http_put(url, data: bytes, content_type='application/octet-stream'):
    req = urllib.request.Request(url, data=data, method='PUT')
    req.add_header('Content-Type', content_type)
    with urllib.request.urlopen(req) as resp:
        return resp.status, resp.read()

def http_get(url):
    with urllib.request.urlopen(url) as resp:
        return resp.status, resp.read()

def cmd_make_manifest(args):
    m = manifest_for_file(args.path, name=os.path.basename(args.path))
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as f:
            json.dump(m, f, indent=2)
    print(m['id'])

def cmd_push(args):
    m = manifest_for_file(args.path, name=os.path.basename(args.path))
    # push chunks
    seen = set()
    for c in chunk_iter(args.path):
        h = c['hash']
        if h in seen:
            continue
        seen.add(h)
        url = f"{args.server}/chunks/{h}"
        status, _ = http_put(url, c['bytes'])
        if status not in (200,201):
            print(f"Failed to PUT chunk {h}: {status}", file=sys.stderr)
            sys.exit(1)
    # push manifest
    mid = m['id']
    status, _ = http_put(f"{args.server}/manifests/{mid}", json.dumps(m).encode('utf-8'), 'application/json')
    if status not in (200,201):
        print(f"Failed to PUT manifest {mid}: {status}", file=sys.stderr)
        sys.exit(1)
    print(mid)

def cmd_fetch(args):
    status, body = http_get(f"{args.server}/manifests/{args.manifest}")
    if status != 200:
        print(f"Manifest not found: {args.manifest}", file=sys.stderr)
        sys.exit(1)
    m = json.loads(body.decode('utf-8'))
    out = open(args.out, 'wb') if args.out else sys.stdout.buffer
    for c in sorted(m['chunks'], key=lambda x: x['order']):
        h = c['hash']
        # locate
        status, body = http_get(f"{args.server}/locate/{h}")
        if status != 200:
            print(f"Locate failed for {h}", file=sys.stderr); sys.exit(1)
        loc = json.loads(body.decode('utf-8'))
        url = loc['candidates'][0]['url']
        status, chunk_bytes = http_get(url)
        if status != 200:
            print(f"Chunk fetch failed {h}", file=sys.stderr); sys.exit(1)
        # verify hash
        hh = 'sha256:' + hashlib.sha256(chunk_bytes).hexdigest()
        if hh != h:
            print(f"Integrity mismatch for {h}", file=sys.stderr); sys.exit(1)
        out.write(chunk_bytes)
    if args.out:
        out.close()

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)

    ap_m = sub.add_parser('make-manifest', help='Create manifest for a file')
    ap_m.add_argument('path')
    ap_m.add_argument('-o','--out')
    ap_m.set_defaults(func=cmd_make_manifest)

    ap_p = sub.add_parser('push', help='Chunk+push a file to server')
    ap_p.add_argument('path')
    ap_p.add_argument('--server', required=True)
    ap_p.set_defaults(func=cmd_push)

    ap_f = sub.add_parser('fetch', help='Fetch by manifest id and reconstruct')
    ap_f.add_argument('manifest')
    ap_f.add_argument('--server', required=True)
    ap_f.add_argument('-o','--out', required=True)
    ap_f.set_defaults(func=cmd_fetch)

    args = ap.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()

