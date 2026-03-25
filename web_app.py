#!/usr/bin/env python3
"""DreamForge 本地 Web 服务。"""

from __future__ import annotations

import argparse
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from dreamforge import DreamForge, serialize_idea

WEB_DIR = Path(__file__).parent / "web"


class DreamForgeHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)

        if parsed.path == "/api/idea":
            self._handle_api_idea(parsed.query)
            return

        if parsed.path in {"/", "/index.html"}:
            self._serve_file(WEB_DIR / "index.html", content_type="text/html; charset=utf-8")
            return

        self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def _handle_api_idea(self, query: str) -> None:
        params = parse_qs(query)
        seed_value = params.get("seed", [None])[0]
        seed = int(seed_value) if seed_value is not None else None

        idea = DreamForge(seed=seed).generate()
        body = json.dumps(serialize_idea(idea), ensure_ascii=False).encode("utf-8")

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_file(self, file_path: Path, *, content_type: str) -> None:
        if not file_path.exists():
            self.send_error(HTTPStatus.NOT_FOUND, "Missing file")
            return

        body = file_path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="运行 DreamForge Web 可视化服务")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    server = ThreadingHTTPServer((args.host, args.port), DreamForgeHandler)
    print(f"DreamForge Web running at http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
