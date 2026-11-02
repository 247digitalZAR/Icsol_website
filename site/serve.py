#!/usr/bin/env python3
"""Serve the ICS static site with hostname-aware robots metadata and real 404s."""
from __future__ import annotations

import argparse
import mimetypes
import re
from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

CANONICAL_HOSTS = {"icsol.co.za", "www.icsol.co.za"}
ROBOTS_META = re.compile(r"\s*<meta\s+name=[\"']robots[\"']\s+content=[\"'][^\"']*[\"']\s*/?>", re.IGNORECASE)


class ICSStaticHandler(SimpleHTTPRequestHandler):
    """Serve pre-rendered files while varying robots directives by the requested hostname."""

    def log_message(self, format: str, *args: object) -> None:
        print(f"{self.address_string()} - {format % args}")

    def do_GET(self) -> None:
        self._serve(include_body=True)

    def do_HEAD(self) -> None:
        self._serve(include_body=False)

    def _requested_host(self) -> str:
        forwarded = self.headers.get("X-Forwarded-Host", "")
        host = (forwarded or self.headers.get("Host", "")).split(",", maxsplit=1)[0].strip().lower()
        return host.split(":", maxsplit=1)[0]

    def _robots_directive(self, status: int) -> str | None:
        if status == HTTPStatus.NOT_FOUND:
            return "noindex" if self._requested_host() in CANONICAL_HOSTS else "noindex, nofollow"
        if self._requested_host() not in CANONICAL_HOSTS:
            return "noindex, nofollow"
        return None

    def _html_with_robots(self, content: bytes, status: int) -> bytes:
        page = content.decode("utf-8")
        page = ROBOTS_META.sub("", page)
        directive = self._robots_directive(status)
        if directive:
            page = page.replace("</head>", f'  <meta name="robots" content="{directive}">\n</head>', 1)
        return page.encode("utf-8")

    def _send(self, status: int, content_type: str, content: bytes, include_body: bool) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-cache" if content_type.startswith("text/html") else "public, max-age=7776000")
        self.end_headers()
        if include_body:
            self.wfile.write(content)

    def _serve_robots(self, include_body: bool) -> None:
        if self._requested_host() in CANONICAL_HOSTS:
            content = b"User-agent: *\nAllow: /\nSitemap: https://icsol.co.za/sitemap.xml\n"
        else:
            content = b"User-agent: *\nDisallow: /\n"
        self._send(HTTPStatus.OK, "text/plain; charset=utf-8", content, include_body)

    def _serve(self, include_body: bool) -> None:
        request_path = urlsplit(self.path).path
        if request_path == "/_app/health":
            self._send(HTTPStatus.NO_CONTENT, "text/plain; charset=utf-8", b"", include_body)
            return
        if request_path == "/robots.txt":
            self._serve_robots(include_body)
            return

        target = Path(self.translate_path(request_path))
        if target.is_dir():
            if not request_path.endswith("/"):
                self.send_response(HTTPStatus.MOVED_PERMANENTLY)
                self.send_header("Location", f"{request_path}/")
                self.end_headers()
                return
            target /= "index.html"

        if not target.is_file():
            not_found = Path(self.directory) / "404.html"
            content = self._html_with_robots(not_found.read_bytes(), HTTPStatus.NOT_FOUND)
            self._send(HTTPStatus.NOT_FOUND, "text/html; charset=utf-8", content, include_body)
            return

        content_type = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
        content = target.read_bytes()
        if content_type == "text/html":
            content = self._html_with_robots(content, HTTPStatus.OK)
            content_type = "text/html; charset=utf-8"
        self._send(HTTPStatus.OK, content_type, content, include_body)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=3000)
    parser.add_argument("--directory", default="public")
    arguments = parser.parse_args()
    directory = Path(arguments.directory).resolve()
    handler = partial(ICSStaticHandler, directory=str(directory))
    server = ThreadingHTTPServer(("0.0.0.0", arguments.port), handler)
    print(f"Serving {directory} at http://0.0.0.0:{arguments.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
