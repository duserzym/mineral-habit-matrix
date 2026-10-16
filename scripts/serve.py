"""Local preview: serves site/ at / and models/ at /models, like the deployed Pages site.

    python scripts/serve.py [port]
"""

import functools
import http.server
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        p = path.split("?", 1)[0].split("#", 1)[0]
        if p.startswith("/models/"):
            return str(ROOT / p.lstrip("/"))
        return str(ROOT / "site" / p.lstrip("/")) if p != "/" else str(ROOT / "site" / "index.html")


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    http.server.ThreadingHTTPServer(("127.0.0.1", port), functools.partial(Handler)).serve_forever()
