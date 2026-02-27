from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json
from urllib.parse import urlparse, parse_qs

from audit_logger import LOG_PATH

MANIFEST_PATH = Path.home() / "tucker_console" / "godfirst_manifest.yaml"

class G1PHandler(BaseHTTPRequestHandler):
    def _send_json(self, obj, code=200):
        data = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/g1p/manifest":
            if MANIFEST_PATH.exists():
                self.send_response(200)
                self.send_header("Content-Type", "text/yaml")
                self.end_headers()
                self.wfile.write(MANIFEST_PATH.read_bytes())
            else:
                self._send_json({"error": "manifest_not_found"}, 404)

        elif parsed.path == "/g1p/audit":
            qs = parse_qs(parsed.query)
            user_id = qs.get("user_id", ["anonymous"])[0]
            entries = []

            if LOG_PATH.exists():
                with LOG_PATH.open() as f:
                    for line in f:
                        try:
                            obj = json.loads(line)
                            if obj.get("user_id") == user_id:
                                entries.append(obj)
                        except:
                            pass

            self._send_json({"user_id": user_id, "entries": entries})

        elif parsed.path == "/g1p/policies":
            self._send_json({
                "protocol": "GodFirst-LLM-ML",
                "version": "1.0.0",
                "principles": [
                    "protect_children",
                    "no_deception",
                    "respect_faith",
                    "transparency",
                    "right_to_exit",
                ],
            })

        else:
            self._send_json({"error": "not_found"}, 404)

def run_server(port=8081):
    server = HTTPServer(("0.0.0.0", port), G1PHandler)
    print(f"G1P API listening on http://localhost:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
