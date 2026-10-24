import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

HOST = "0.0.0.0"
PORT = int(os.getenv("PORT", "8080"))
FAULT_FILE = Path(os.getenv("FAULT_FILE", "/tmp/pitstop-unhealthy"))


def is_healthy(fault_file=FAULT_FILE):
    return not fault_file.exists()


class PitStopHandler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/":
            return self.send_json(200, {
                "service": "pitstop-telemetry",
                "status": "running",
                "purpose": "local reliability lab",
            })

        if path == "/health":
            healthy = is_healthy()
            return self.send_json(200 if healthy else 503, {
                "status": "healthy" if healthy else "unhealthy",
            })

        return self.send_json(404, {"error": "not found"})

    def do_POST(self):
        path = urlparse(self.path).path


        if path == "/fault/on":
            FAULT_FILE.touch()
            return self.send_json(200, {
                "fault_injected": True,
                "message": "Health endpoint will return HTTP 503",
            })

        if path == "/fault/off":
            FAULT_FILE.unlink(missing_ok=True)
            return self.send_json(200, {
                "fault_injected": False,
                "message": "Health endpoint restored",
            })
              

        return self.send_json(404, {"error": "not found"})

    def log_message(self, fmt, *args):
        print(f"[pitstop] {self.address_string()} - {fmt % args}", flush=True)


if __name__ == "__main__":
    print(f"PitStop listening on {HOST}:{PORT}", flush=True)
    ThreadingHTTPServer((HOST, PORT), PitStopHandler).serve_forever()