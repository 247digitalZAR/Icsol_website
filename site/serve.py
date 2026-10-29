#!/usr/bin/env python3
"""Serve the generated ICS static site locally, including its production 404 page."""
from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class ICSStaticHandler(SimpleHTTPRequestHandler):
    def send_error(self, code, message=None, explain=None):
        if code == 404:
            page = Path(self.directory) / "404.html"
            if page.exists():
                data = page.read_bytes()
                self.send_response(404)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                self.wfile.write(data)
                return
        super().send_error(code, message, explain)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=3000)
    parser.add_argument("--directory", default="public")
    arguments = parser.parse_args()
    directory = Path(arguments.directory).resolve()
    handler = partial(ICSStaticHandler, directory=str(directory))
    server = ThreadingHTTPServer(("127.0.0.1", arguments.port), handler)
    print(f"Serving {directory} at http://127.0.0.1:{arguments.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
