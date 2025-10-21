#!/usr/bin/env python3
import argparse, os, sys, json, hashlib, urllib.request, logging
from ref.chunker import chunk_iter, manifest_for_file
from ref.cache import get_chunk_from_cache, put_chunk_to_cache

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


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
    try:
        m = manifest_for_file(args.path, name=os.path.basename(args.path))
    except Exception as e:
        logging.error(f"Failed to create manifest for {args.path}: {e}")
        raise RuntimeError(f"Manifest creation failed: {e}")
    # push chunks
    seen = set()
    for c in chunk_iter(args.path):
        h = c['hash']
        if h in seen:
            continue
        seen.add(h)
        url = f"{args.server}/chunks/{h}"
        try:
            status, _ = http_put(url, c['bytes'])
            if status not in (200,201):
                logging.error(f"Failed to PUT chunk {h}: HTTP {status}")
                raise RuntimeError(f"Chunk upload failed for {h}")
        except Exception as e:
            logging.error(f"Error uploading chunk {h}: {e}")
            raise
    # push manifest
    mid = m['id']
    try:
        status, _ = http_put(f"{args.server}/manifests/{mid}", json.dumps(m).encode('utf-8'), 'application/json')
        if status not in (200,201):
            logging.error(f"Failed to PUT manifest {mid}: HTTP {status}")
            raise RuntimeError(f"Manifest upload failed for {mid}")
    except Exception as e:
        logging.error(f"Error uploading manifest {mid}: {e}")
        raise
    print(mid)

def cmd_fetch(args):
    try:
        status, body = http_get(f"{args.server}/manifests/{args.manifest}")
        if status != 200:
            logging.error(f"Manifest not found: {args.manifest} (HTTP {status})")
            raise RuntimeError(f"Manifest fetch failed: {args.manifest}")
        m = json.loads(body.decode('utf-8'))
    except Exception as e:
        logging.error(f"Error fetching manifest {args.manifest}: {e}")
        raise
    out = open(args.out, 'wb') if args.out else sys.stdout.buffer
    try:
        for c in sorted(m['chunks'], key=lambda x: x['order']):
            h = c['hash']
            # locate
            try:
                status, body = http_get(f"{args.server}/locate/{h}")
                if status != 200:
                    logging.error(f"Locate failed for {h} (HTTP {status})")
                    raise RuntimeError(f"Locate failed for {h}")
                loc = json.loads(body.decode('utf-8'))
                url = loc['candidates'][0]['url']
            except Exception as e:
                logging.error(f"Error locating chunk {h}: {e}")
                raise
            # try cache first
            chunk_bytes = get_chunk_from_cache(h)
            if chunk_bytes is None:
                try:
                    status, chunk_bytes = http_get(url)
                    if status != 200:
                        logging.error(f"Chunk fetch failed {h} (HTTP {status})")
                        raise RuntimeError(f"Chunk fetch failed for {h}")
                    put_chunk_to_cache(h, chunk_bytes)
                except Exception as e:
                    logging.error(f"Error fetching chunk {h}: {e}")
                    raise
            # verify hash
            hh = 'sha256:' + hashlib.sha256(chunk_bytes).hexdigest()
            if hh != h:
                logging.error(f"Integrity mismatch for {h}")
                raise RuntimeError(f"Integrity check failed for {h}")
            out.write(chunk_bytes)
    except Exception:
        if args.out:
            out.close()
        raise
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
