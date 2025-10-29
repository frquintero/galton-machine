"""
Standard-library HTTP server powering the Galton Board web interface.

This module exposes a lightweight JSON API plus a static single-page
application built on top of the existing `galton_sim` package. It
avoids external dependencies by relying exclusively on Python's built-in
`http.server` implementation.
"""
from __future__ import annotations

import json
import logging
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from galton_sim.models import SimulationParameters
from galton_sim.rendering.ascii import render_ascii
from galton_sim.simulation import simulate_galton

DEFAULT_NUM_BALLS = 1000
DEFAULT_NUM_LEVELS = 10
DEFAULT_P_RIGHT = 0.5

_TEMPLATE_PATH = Path(__file__).resolve().parent / "templates" / "index.html"
INDEX_HTML = _TEMPLATE_PATH.read_text(encoding="utf-8")

__all__ = ["run", "build_simulation_payload"]


def _parse_seed(raw_value: Any) -> Optional[int]:
    """Normalize a seed value coming from JSON payloads."""
    if raw_value is None:
        return None
    if isinstance(raw_value, str):
        stripped = raw_value.strip()
        if stripped == "":
            return None
        try:
            return int(stripped)
        except ValueError as exc:
            raise ValueError("seed must be an integer") from exc
    if isinstance(raw_value, (int, float)):
        if isinstance(raw_value, float):
            if not raw_value.is_integer():
                raise ValueError("seed must be an integer")
            raw_value = int(raw_value)
        return int(raw_value)
    raise ValueError("seed must be an integer")


def _ensure_float(raw_value: Any, *, field: str) -> float:
    """Coerce value to float, raising ValueError with friendly message."""
    try:
        return float(raw_value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be a float, got {raw_value!r}") from exc


def _ensure_int(raw_value: Any, *, field: str) -> int:
    """Coerce value to int, raising ValueError with friendly message."""
    if isinstance(raw_value, bool):  # bool is subclass of int; reject explicitly
        raise ValueError(f"{field} must be an integer, got {raw_value!r}")

    if isinstance(raw_value, float):
        if not raw_value.is_integer():
            raise ValueError(f"{field} must be an integer, got {raw_value!r}")
        raw_value = int(raw_value)

    try:
        return int(raw_value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be an integer, got {raw_value!r}") from exc


def _build_parameters(payload: Dict[str, Any]) -> SimulationParameters:
    """Construct `SimulationParameters` from inbound payload dictionary."""
    num_balls = payload.get("num_balls", DEFAULT_NUM_BALLS)
    num_levels = payload.get("num_levels", DEFAULT_NUM_LEVELS)
    p_right = payload.get("p_right", DEFAULT_P_RIGHT)
    seed = payload.get("seed")

    params = SimulationParameters(
        num_balls=_ensure_int(num_balls, field="num_balls"),
        num_levels=_ensure_int(num_levels, field="num_levels"),
        p_right=_ensure_float(p_right, field="p_right"),
        seed=_parse_seed(seed),
    )
    return params


def build_simulation_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Run simulation using payload dict and return serialized response."""
    params = _build_parameters(payload)
    results = simulate_galton(params)
    ascii_histogram = render_ascii(results.counts)

    return {
        "success": True,
        "data": {
            "counts": results.counts,
            "mean": results.mean,
            "variance": results.variance,
            "proportions": results.proportions,
            "ascii": ascii_histogram,
            "parameters": {
                "num_balls": params.num_balls,
                "num_levels": params.num_levels,
                "p_right": params.p_right,
                "seed": params.seed,
            },
        },
        "error": None,
    }


class GaltonRequestHandler(BaseHTTPRequestHandler):
    """HTTP handler serving the web UI and JSON API."""

    server_version = "GaltonWebApp/1.0"
    sys_version = ""

    def do_GET(self) -> None:  # noqa: N802 (BaseHTTPRequestHandler naming)
        """Serve the single-page frontend or API responses."""
        path, _query = self._split_path()

        if path in ("/", "/index.html"):
            self._send_response(
                HTTPStatus.OK,
                INDEX_HTML.encode("utf-8"),
                "text/html; charset=utf-8",
            )
            return

        if path == "/api/health":
            self._send_json(HTTPStatus.OK, {"status": "healthy"})
            return

        if path == "/favicon.ico":
            self.send_response(HTTPStatus.NO_CONTENT)
            self.end_headers()
            return

        self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not Found"})

    def do_OPTIONS(self) -> None:  # noqa: N802
        """Handle CORS pre-flight requests (simple permissive policy)."""
        self.send_response(HTTPStatus.NO_CONTENT)
        self._set_common_headers()
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self) -> None:  # noqa: N802
        """Handle API POST requests."""
        path, _query = self._split_path()

        if path != "/api/simulate":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not Found"})
            return

        try:
            payload = self._read_json_body()
        except ValueError as exc:
            self._send_json(HTTPStatus.BAD_REQUEST, {"success": False, "data": None, "error": str(exc)})
            return

        try:
            response_payload = build_simulation_payload(payload)
        except ValueError as exc:
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                {"success": False, "data": None, "error": str(exc)},
            )
            return
        except Exception as exc:  # noqa: BLE001
            logging.exception("Unexpected error handling simulation request")
            self._send_json(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"success": False, "data": None, "error": f"Unexpected error: {exc}"},
            )
            return

        self._send_json(HTTPStatus.OK, response_payload)

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------
    def _read_json_body(self) -> Dict[str, Any]:
        """Parse JSON body from request."""
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise ValueError("Invalid Content-Length header") from exc

        if content_length == 0:
            return {}

        body = self.rfile.read(content_length)
        try:
            return json.loads(body.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError("Request body must be valid JSON") from exc

    def _split_path(self) -> Tuple[str, Optional[str]]:
        """Return tuple of (path, query) without performing full parsing."""
        raw_path = self.path
        if "?" in raw_path:
            path, query = raw_path.split("?", 1)
            return path, query
        return raw_path, None

    def _set_common_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Access-Control-Allow-Origin", "*")

    def _send_response(self, status: HTTPStatus, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self._set_common_headers()
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: HTTPStatus, payload: Dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self._send_response(status, body, "application/json; charset=utf-8")

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        """Reduce logging noise; rely on standard logging module instead."""
        logging.info("%s - - %s", self.client_address[0], format % args)


def run(host: str = "127.0.0.1", port: int = 5000) -> None:
    """Start the HTTP server and block until interrupted."""
    server_address = (host, port)
    with ThreadingHTTPServer(server_address, GaltonRequestHandler) as httpd:
        print("\n🎰 Galton Board Web App")
        print("=" * 40)
        print(f"Listening on http://{host}:{port}")
        print("Press Ctrl+C to stop")
        print("=" * 40 + "\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down web server...")
        finally:
            httpd.server_close()


if __name__ == "__main__":
    run()
