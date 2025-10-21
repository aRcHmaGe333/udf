#!/usr/bin/env python3
import argparse, json, os
from ref.operators import operator_id, apply_fir
from ref.client import http_put, http_get
from ref.chunker import manifest_for_file

def read_numbers(path):
    # Reads whitespace or comma-separated floats
    txt = open(path, 'r', encoding='utf-8').read()
    txt = txt.replace(',', ' ')
    vals = [float(x) for x in txt.split() if x.strip()]
    return vals

def write_numbers(path, vals):
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(str(v) for v in vals))

def push_file(server, path):
    from ref.chunker import chunk_iter
    m = manifest_for_file(path, name=os.path.basename(path), media_type='text/plain')
    seen = set()
    for c in chunk_iter(path):
        h = c['hash']
        if h in seen: continue
        seen.add(h)
        http_put(f"{server}/chunks/{h}", c['bytes'])
    http_put(f"{server}/manifests/{m['id']}", json.dumps(m).encode('utf-8'), 'application/json')
    return m['id']

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--server', required=True)
    ap.add_argument('--coeffs', required=True, help='Path to FIR coeffs JSON or text numbers')
    ap.add_argument('--input', required=True, help='Path to input numeric series')
    ap.add_argument('--out', required=True)
    args = ap.parse_args()

    # Load coeffs
    coeffs_path = args.coeffs
    if coeffs_path.lower().endswith('.json'):
        spec = json.load(open(coeffs_path, 'r', encoding='utf-8'))
        coeffs = spec.get('coeffs', [])
        op_spec = {"type": "fir", "coeffs": coeffs}
    else:
        coeffs = read_numbers(coeffs_path)
        op_spec = {"type": "fir", "coeffs": coeffs}
    oid = operator_id(op_spec)

    # Push operator spec to server
    http_put(f"{args.server}/operators/{oid}", json.dumps(op_spec).encode('utf-8'), 'application/json')

    # Push input file and get manifest
    in_mid = push_file(args.server, args.input)

    # Build task key
    import hashlib
    payload = json.dumps({"op": oid, "input": in_mid}, sort_keys=True).encode('utf-8')
    tkey = 'sha256:' + hashlib.sha256(payload).hexdigest()

    # Lookup cached result
    status, body = http_get(f"{args.server}/results/{tkey}")
    if status == 200:
        mapping = json.loads(body.decode('utf-8'))
        out_mid = mapping['manifest']
        # Fetch chunks and reconstruct
        status, mbody = http_get(f"{args.server}/manifests/{out_mid}")
        if status == 200:
            m = json.loads(mbody.decode('utf-8'))
            with open(args.out, 'wb') as f:
                for c in sorted(m['chunks'], key=lambda x: x['order']):
                    _, cbytes = http_get(f"{args.server}/chunks/{c['hash']}")
                    f.write(cbytes)
            print(out_mid)
            return

    # Compute and store result
    vals = read_numbers(args.input)
    out_vals = apply_fir(vals, coeffs)
    write_numbers(args.out, out_vals)
    out_mid = push_file(args.server, args.out)
    http_put(f"{args.server}/results/{tkey}", json.dumps({"manifest": out_mid}).encode('utf-8'), 'application/json')
    print(out_mid)

if __name__ == '__main__':
    main()

