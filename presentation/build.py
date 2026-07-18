#!/usr/bin/env python3
"""Assemble the single-file GodotCon26 deck.

Reads deck-src.html and resolves:
  <!-- @file:relpath -->   raw file contents inlined (reveal css/js)
  <!-- @panel:name -->     generated editor panel from generated/<name>.html
  __DATA:relpath__         base64 data URI (fonts, images, video)

Writes ../cooties-godotcon26.html
"""

import base64
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE.parent / "cooties-godotcon26.html"

MIME = {
    ".woff2": "font/woff2",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".mp4": "video/mp4",
    ".svg": "image/svg+xml",
}


def data_uri(rel: str) -> str:
    p: Path = HERE / rel
    mime: str = MIME[p.suffix]
    return "data:%s;base64,%s" % (mime, base64.b64encode(p.read_bytes()).decode())


def main() -> None:
    src: str = (HERE / "deck-src.html").read_text()

    src = re.sub(
        r"<!-- @file:(\S+) -->",
        lambda m: (HERE / m.group(1)).read_text(),
        src,
    )
    src = re.sub(
        r"<!-- @panel:(\w+) -->",
        lambda m: (HERE / "generated" / (m.group(1) + ".html")).read_text(),
        src,
    )
    src = re.sub(r"__DATA:(\S+?)__", lambda m: data_uri(m.group(1)), src)
    src = re.sub(r"//# sourceMappingURL=\S+", "", src)

    leftovers: list[str] = re.findall(r"<!-- @\w+:\S+ -->|__DATA:\S+?__", src)
    if leftovers:
        sys.exit("unresolved directives: %s" % leftovers)

    OUT.write_text(src)
    print("wrote %s (%.1f MB)" % (OUT, OUT.stat().st_size / 1e6))


if __name__ == "__main__":
    main()
