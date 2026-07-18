#!/usr/bin/env python3
"""Live-reload dev server for the deck. No dependencies.

    python presentation/dev.py

Serves the repo root at http://localhost:8137/cooties-godotcon26.html
Watches presentation/ sources; on change it reruns build.py (and gdhl.py when
the highlighter or snippets change) and the browser auto-reloads via the
/__version poll baked into the deck (active only when served over http).
"""

import http.server
import subprocess
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent
OUT = ROOT / "cooties-godotcon26.html"
PORT = 8137

WATCH = ["deck-src.html", "build.py", "gdhl.py", "godot_ascii.txt"]
WATCH_DIRS = ["img", "snippets", "generated", "vendor"]


def snapshot() -> dict:
    files: dict = {}
    for name in WATCH:
        p: Path = HERE / name
        if p.exists():
            files[str(p)] = p.stat().st_mtime
    for d in WATCH_DIRS:
        for p in (HERE / d).rglob("*"):
            if p.is_file():
                files[str(p)] = p.stat().st_mtime
    return files


def rebuild(changed: list) -> None:
    if any("gdhl.py" in c or "/snippets/" in c for c in changed):
        subprocess.run([sys.executable, HERE / "gdhl.py", "extract"], check=False)
        subprocess.run([sys.executable, HERE / "gdhl.py", "render"], check=False)
    subprocess.run([sys.executable, HERE / "build.py"], check=False)


def watcher() -> None:
    seen: dict = snapshot()
    while True:
        time.sleep(0.4)
        now: dict = snapshot()
        changed: list = [k for k in now if now[k] != seen.get(k)]
        changed += [k for k in seen if k not in now]
        if changed:
            print("changed:", ", ".join(Path(c).name for c in changed))
            rebuild(changed)
            seen = snapshot()


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kw):
        super().__init__(*args, directory=str(ROOT), **kw)

    def do_GET(self):
        if self.path == "/__version":
            body: bytes = str(OUT.stat().st_mtime if OUT.exists() else 0).encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def log_message(self, fmt, *args):
        if "/__version" not in (args[0] if args else ""):
            super().log_message(fmt, *args)


if __name__ == "__main__":
    threading.Thread(target=watcher, daemon=True).start()
    print("serving http://localhost:%d/cooties-godotcon26.html" % PORT)
    http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
