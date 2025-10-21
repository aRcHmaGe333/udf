#!/usr/bin/env python3
import argparse, os, sys, json, hashlib, platform, gzip
from io import BytesIO
from ref.chunker import chunk_iter, manifest_for_file
from ref.client import http_put, http_get

def env_fingerprint():
    return {
        "python": platform.python_version(),
        "os": platform.system().lower(),
        "arch": platform.machine().lower(),
    }

def task_key(action:str, params:dict, input_manifest_id:str, env:dict):
    payload = {
        "action": action,
        "params": params,
        "input_manifest": input_manifest_id,
        "env": env,
    }
    data = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode('utf-8')
    return 'sha256:' + hashlib.sha256(data).hexdigest()

def gzip_deterministic(data: bytes, level:int=6):
    bio = BytesIO()
    # mtime=0 ensures deterministic gzip header
    with gzip.GzipFile(fileobj=bio, mode='wb', compresslevel=level, mtime=0) as gz:
        gz.write(data)
    return bio.getvalue()

def push_file(server, path):
    # push chunks and manifest for path; return manifest id
    m = manifest_for_file(path, name=os.path.basename(path))
    seen = set()
    for c in chunk_iter(path):
        h = c['hash']
        if h in seen:
            continue
        seen.add(h)
        status, _ = http_put(f"{server}/chunks/{h}", c['bytes'])
        if status not in (200,201):
            raise RuntimeError(f"chunk put failed: {h} {status}")
    status, _ = http_put(f"{server}/manifests/{m['id']}", json.dumps(m).encode('utf-8'), 'application/json')
    if status not in (200,201):
        raise RuntimeError(f"manifest put failed: {m['id']} {status}")
    return m['id']

def write_bytes(path, data: bytes):
    with open(path, 'wb') as f:
        f.write(data)

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)

    ap_gz = sub.add_parser('gzip', help='Deterministic gzip of a file with cache')
    ap_gz.add_argument('path')
    ap_gz.add_argument('--server', required=True)
    ap_gz.add_argument('-o','--out', required=True)
    ap_gz.add_argument('--level', type=int, default=6)

    args = ap.parse_args()

    if args.cmd == 'gzip':
        # 1) Ensure input manifest exists on server
        in_manifest = push_file(args.server, args.path)
        # 2) Build task key
        env = env_fingerprint()
        params = {"level": args.level, "mtime": 0}
        tkey = task_key("gzip@1", params, in_manifest, env)
        # 3) Lookup result
        status, body = http_get(f"{args.server}/results/{tkey}")
        if status == 200:
            mapping = json.loads(body.decode('utf-8'))
            out_manifest = mapping['manifest']
            # Reconstruct using client fetch path
            from ref.client import http_get as get
            status, mbody = get(f"{args.server}/manifests/{out_manifest}")
            if status != 200:
                print("Cached manifest missing; recomputing", file=sys.stderr)
            else:
                m = json.loads(mbody.decode('utf-8'))
                out = open(args.out, 'wb')
                for c in sorted(m['chunks'], key=lambda x: x['order']):
                    status, cbytes = get(f"{args.server}/chunks/{c['hash']}")
                    if status != 200:
                        print("Cached chunk missing; recomputing", file=sys.stderr); break
                    out.write(cbytes)
                else:
                    out.close(); print(out_manifest); return
        # 4) Compute deterministically
        with open(args.path, 'rb') as f:
            data = f.read()
        gz = gzip_deterministic(data, level=args.level)
        write_bytes(args.out, gz)
        # 5) Push output and record result
        out_manifest = push_file(args.server, args.out)
        import time, getpass
        receipt = {"who": getpass.getuser(), "when": int(time.time()), "tool": "compute_cache@gzip"}
        payload = json.dumps({"manifest": out_manifest, "receipt": receipt}).encode('utf-8')
        status, _ = http_put(f"{args.server}/results/{tkey}", payload, 'application/json')
        if status not in (200,201):
            print("Failed to record result", file=sys.stderr)
        print(out_manifest)

if __name__ == '__main__':
    main()
