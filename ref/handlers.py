#!/usr/bin/env python3
import json
from http.server import BaseHTTPRequestHandler


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, obj, code=200):
        body = json.dumps(obj).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

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
            self._send_json(m)
            return
        if self.path.startswith('/results/'):
            key = self.path.split('/results/',1)[1]
            entry = self.server.store.get_result(key)
            if not entry:
                self.send_error(404, 'result not found'); return
            self._send_json(entry)
            return
        if self.path.startswith('/operators/'):
            oid = self.path.split('/operators/',1)[1]
            spec = self.server.store.get_operator(oid)
            if spec is None:
                self.send_error(404, 'operator not found'); return
            self._send_json(spec)
            return
        if self.path.startswith('/locate/'):
            h = self.path.split('/locate/',1)[1]
            base = f"http://{self.server.host}:{self.server.port}"
            candidates = [{"url": f"{base}/chunks/{h}", "latency_ms": 1, "region": getattr(self.server, 'region', 'local')}]
            # Add peers from nodes config if present
            peers = getattr(self.server, 'nodes', []) or []
            for peer in peers:
                url = peer.get('url')
                if not url:
                    continue
                candidates.append({"url": f"{url}/chunks/{h}", "region": peer.get('region', 'unknown')})
            # Sort by region match with hint
            hint = self.headers.get('X-Region')
            if hint:
                candidates.sort(key=lambda c: 0 if c.get('region') == hint else 1)
            self._send_json({"hash": h, "candidates": candidates})
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

