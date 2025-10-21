#!/usr/bin/env python3
import argparse, os, json, logging
from http.server import HTTPServer
from ref.store import Store
from ref.handlers import Handler


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.udf_store')
    ap.add_argument('--host', default='127.0.0.1')
    ap.add_argument('--port', type=int, default=8080)
    ap.add_argument('--nodes', default='ref/nodes.json', help='optional peer nodes JSON')
    ap.add_argument('--region', default='local', help='server region hint')
    args = ap.parse_args()

    store = Store(args.root)
    httpd = HTTPServer((args.host, args.port), Handler)
    httpd.store = store
    httpd.host = args.host
    httpd.port = args.port
    httpd.region = args.region
    # Load nodes if present
    nodes_path = args.nodes
    if nodes_path and os.path.exists(nodes_path):
        try:
            httpd.nodes = json.load(open(nodes_path, 'r', encoding='utf-8'))
        except Exception:
            httpd.nodes = []
    else:
        httpd.nodes = []
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s %(message)s')
    logging.info(f"UDF server at http://{args.host}:{args.port} root={args.root} region={args.region} peers={len(httpd.nodes)}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
