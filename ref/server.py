#!/usr/bin/env python3
import argparse, os, json
from http.server import HTTPServer, BaseHTTPRequestHandler


class Store:
    def __init__(self, root):
        self.root = root
        self.chunks = os.path.join(root, 'chunks')
        self.manifests = os.path.join(root, 'manifests')
        self.results_index = os.path.join(root, 'results.json')
        self.operators = os.path.join(root, 'operators')
        os.makedirs(self.chunks, exist_ok=True)
        os.makedirs(self.manifests, exist_ok=True)
        os.makedirs(self.operators, exist_ok=True)

    def chunk_path(self, h):
        safe = h.replace(':', '_')
        return os.path.join(self.chunks, safe)

    def has_chunk(self, h):
        return os.path.exists(self.chunk_path(h))

    def put_chunk(self, h, data):
        p = self.chunk_path(h)
        if not os.path.exists(p):
            with open(p, 'wb') as f:
                f.write(data)

    def get_chunk(self, h):
        p = self.chunk_path(h)
        if not os.path.exists(p):
            return None
        with open(p, 'rb') as f:
            return f.read()

    def manifest_path(self, mid):
        safe = mid.replace(':', '_')
        return os.path.join(self.manifests, safe + '.json')

    def put_manifest(self, mid, manifest):
        with open(self.manifest_path(mid), 'w', encoding='utf-8') as f:
            json.dump(manifest, f)

    def get_manifest(self, mid):
        p = self.manifest_path(mid)
        if not os.path.exists(p):
            return None
        with open(p, 'r', encoding='utf-8') as f:
            return json.load(f)

    # Results index: task_key -> manifest id
    def get_result(self, key):
        if not os.path.exists(self.results_index):
            return None
        try:
            with open(self.results_index, 'r', encoding='utf-8') as f:
                m = json.load(f)
        except Exception:
            return None
        return m.get(key)

    def put_result(self, key, manifest_id, receipt=None):
        m = {}
        if os.path.exists(self.results_index):
            try:
                with open(self.results_index, 'r', encoding='utf-8') as f:
                    m = json.load(f)
            except Exception:
                m = {}
        entry = {"manifest": manifest_id}
        if receipt:
            entry["receipt"] = receipt
        m[key] = entry
        with open(self.results_index, 'w', encoding='utf-8') as f:
            json.dump(m, f)

    # Operators: store simple operator specs by id
    def operator_path(self, oid):
        safe = oid.replace(':', '_')
        return os.path.join(self.operators, safe + '.json')

    def put_operator(self, oid, spec):
        with open(self.operator_path(oid), 'w', encoding='utf-8') as f:
            json.dump(spec, f)

    def get_operator(self, oid):
        p = self.operator_path(oid)
        if not os.path.exists(p):
            return None
        with open(p, 'r', encoding='utf-8') as f:
            return json.load(f)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200); self.end_headers(); self.wfile.write(b'OK'); return
        if self.path.startswith('/chunks/'):
            h = self.path.split('/chunks/',1)[1]
            data = self.server.store.get_chunk(h)
            if data is None:
                self.send_error(404, 'chunk not found'); return
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        if self.path.startswith('/manifests/'):
            mid = self.path.split('/manifests/',1)[1]
            m = self.server.store.get_manifest(mid)
            if m is None:
                self.send_error(404, 'manifest not found'); return
            body = json.dumps(m).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path.startswith('/results/'):
            key = self.path.split('/results/',1)[1]
            entry = self.server.store.get_result(key)
            if not entry:
                self.send_error(404, 'result not found'); return
            payload = entry if isinstance(entry, dict) else {"manifest": entry}
            body = json.dumps(payload).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path.startswith('/operators/'):
            oid = self.path.split('/operators/',1)[1]
            spec = self.server.store.get_operator(oid)
            if spec is None:
                self.send_error(404, 'operator not found'); return
            body = json.dumps(spec).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path.startswith('/locate/'):
            h = self.path.split('/locate/',1)[1]
            # Stub locator: always returns self URL
            base = f"http://{self.server.host}:{self.server.port}"
            payload = {"hash": h, "candidates": [{"url": f"{base}/chunks/{h}", "latency_ms": 1}]}
            body = json.dumps(payload).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_error(404, 'unknown endpoint')

    def do_PUT(self):
        length = int(self.headers.get('Content-Length','0'))
        body = self.rfile.read(length) if length else b''
        if self.path.startswith('/chunks/'):
            h = self.path.split('/chunks/',1)[1]
            self.server.store.put_chunk(h, body)
            self.send_response(201); self.end_headers(); return
        if self.path.startswith('/manifests/'):
            mid = self.path.split('/manifests/',1)[1]
            try:
                m = json.loads(body.decode('utf-8'))
            except Exception:
                self.send_error(400, 'invalid json'); return
            self.server.store.put_manifest(mid, m)
            self.send_response(201); self.end_headers(); return
        if self.path.startswith('/results/'):
            key = self.path.split('/results/',1)[1]
            try:
                payload = json.loads(body.decode('utf-8'))
            except Exception:
                self.send_error(400, 'invalid json'); return
            mid = payload.get('manifest')
            if not mid:
                self.send_error(400, 'missing manifest'); return
            self.server.store.put_result(key, mid, payload.get('receipt'))
            self.send_response(201); self.end_headers(); return
        if self.path.startswith('/operators/'):
            oid = self.path.split('/operators/',1)[1]
            try:
                spec = json.loads(body.decode('utf-8'))
            except Exception:
                self.send_error(400, 'invalid json'); return
            self.server.store.put_operator(oid, spec)
            self.send_response(201); self.end_headers(); return
        self.send_error(404, 'unknown endpoint')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.udf_store')
    ap.add_argument('--host', default='127.0.0.1')
    ap.add_argument('--port', type=int, default=8080)
    args = ap.parse_args()

    store = Store(args.root)
    httpd = HTTPServer((args.host, args.port), Handler)
    httpd.store = store
    httpd.host = args.host
    httpd.port = args.port
    print(f"UDF server at http://{args.host}:{args.port} root={args.root}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
