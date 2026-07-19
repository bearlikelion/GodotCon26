#!/usr/bin/env python3
"""GDScript to gruvbox HTML highlighter for the GodotCon26 deck.

Modes:
  python gdhl.py extract   copy manifest line ranges verbatim from the cooties
                           repo into snippets/<name>.gd (frozen deck copies)
  python gdhl.py render    tokenize snippets/<name>.gd into generated/<name>.html
                           editor panels (gutter with true line numbers + code)

Token colors (gruvbox-dark):
  keyword red, annotation orange, type aqua, function blue, string green,
  number purple, comment gray italic, const/nodepath yellow
"""

import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
COOTIES = Path("/mnt/Storage/Godot/Source/cooties")
SNIPPETS = HERE / "snippets"
GENERATED = HERE / "generated"

# name: (source file, start line, end line, breadcrumb)
# start/end may instead be a list of (start, end) segments; gaps render as an
# elision row so wide but non-essential blocks stay out of the slide
MANIFEST = {
    "steaminit_full":           ("Singletons/SteamInit.gd",        1,  20, "SteamInit.gd > _ready"),
    "global_peer_connected":    ("Singletons/Global.gd",          28,  39, "Global.gd > _on_peer_connected"),
    "global_connected":         ("Singletons/Global.gd",          60,  77, "Global.gd > _on_connected_to_server"),
    "global_send_player":       ("Singletons/Global.gd",          80,  87, "Global.gd > send_player_to_server"),
    "global_add_local_player":  ("Singletons/Global.gd",         167, 189, "Global.gd > add_local_player"),
    "global_set_character":     ("Singletons/Global.gd",         102, 112, "Global.gd > set_player_character"),
    "menu_backend_enum":        ("Scenes/MainMenu/main_menu.gd", [(4, 4), (12, 12), (144, 145)], None, "main_menu.gd > MultiplayerBackend"),
    "menu_host_game":           ("Scenes/MainMenu/main_menu.gd", 144, 158, "main_menu.gd > _on_host_game_pressed"),
    "menu_connect":             ("Scenes/MainMenu/main_menu.gd", 161, 175, "main_menu.gd > _on_connect_pressed"),
    "menu_lobby_created":       ("Scenes/MainMenu/main_menu.gd",  62,  76, "main_menu.gd > _on_lobby_created"),
    "menu_lobby_joined":        ("Scenes/MainMenu/main_menu.gd", [(88, 89), (95, 106)], None, "main_menu.gd > _on_lobby_joined"),
    "menu_get_lobbies":         ("Scenes/MainMenu/main_menu.gd", 109, 113, "main_menu.gd > get_lobbies"),
    "menu_lobby_match_list":    ("Scenes/MainMenu/main_menu.gd",  46,  59, "main_menu.gd > _on_lobby_match_list"),
    "main_change_level":        ("Scenes/main.gd",                 1,  17, "main.gd > _on_change_level"),
    "spawner_ready":            ("Scenes/Game/player_spawner.gd", 10,  19, "player_spawner.gd > _ready"),
    "spawner_spawn_player":     ("Scenes/Game/player_spawner.gd", [(22, 28), (42, 43)], None, "player_spawner.gd > spawn_player"),
    "player_ready":             ("Scenes/Player/player.gd",       37,  48, "player.gd > _ready"),
    "player_physics":           ("Scenes/Player/player.gd",       51,  54, "player.gd > _physics_process"),
    "select_ready_rpcs":        ("Scenes/UI/character_select.gd", [(64, 72), (79, 82)], None, "character_select.gd > _set_ready"),
    "lobby_check_all_ready":    ("Scenes/Lobby/lobby.gd", [(72, 79), (86, 88), (91, 94)], None, "lobby.gd > check_all_ready"),
    "game_set_infected":        ("Scenes/Game/game.gd",          284, 296, "game.gd > _set_player_infected"),
}

# per-snippet (old, new) line rewrites for slide simplification; new "" deletes
REWRITE = {
    "menu_connect": [(", CONNECT_ONE_SHOT", "")],
}

KEYWORDS = (
    "func|var|const|if|elif|else|for|in|while|match|return|pass|break|continue|"
    "extends|class_name|signal|enum|static|await|and|or|not|is|as|void|"
    "preload|load|print|str|int|float|bool|self|true|false|null"
)

TOKEN_RE = re.compile(
    r"""(?P<comment>\#.*$)
      | (?P<string>"[^"\n]*"|'[^'\n]*')
      | (?P<annotation>@\w+)
      | (?P<nodepath>[$%][A-Za-z_][\w/]*)
      | (?P<number>\b\d[\d_]*(?:\.\d+)?\b)
      | (?P<keyword>\b(?:KEYWORDS)\b)
      | (?P<const>\b[A-Z][A-Z0-9_]{2,}\b)
      | (?P<type>\b[A-Z][A-Za-z0-9]*\b)
      | (?P<func>\b[a-z_][a-z0-9_]*(?=\())
    """.replace("KEYWORDS", KEYWORDS),
    re.VERBOSE | re.MULTILINE,
)


# Tokenize one line of GDScript into gruvbox span markup
def highlight_line(line: str) -> str:
    out: list[str] = []
    pos: int = 0
    for m in TOKEN_RE.finditer(line):
        out.append(html.escape(line[pos:m.start()]))
        kind: str = m.lastgroup or ""
        # print/str/int/float/bool double as calls, keep keyword color
        out.append('<span class="g-%s">%s</span>' % (kind, html.escape(m.group())))
        pos = m.end()
    out.append(html.escape(line[pos:]))
    return "".join(out)


# Copy manifest ranges verbatim out of the cooties repo
def extract() -> None:
    SNIPPETS.mkdir(exist_ok=True)
    meta: dict = {}
    for name, (rel, start, end, crumb) in MANIFEST.items():
        segments: list = start if isinstance(start, list) else [(start, end)]
        src: Path = COOTIES / rel
        lines: list[str] = src.read_text().splitlines()
        chunks: list[str] = ["\n".join(lines[a - 1:b]) for a, b in segments]
        (SNIPPETS / (name + ".gd")).write_text("\n# [...]\n".join(chunks) + "\n")
        meta[name] = {"file": rel, "tab": Path(rel).name, "segments": segments,
                      "end": segments[-1][1], "crumb": crumb}
    (SNIPPETS / "manifest.json").write_text(json.dumps(meta, indent=2) + "\n")
    print("extracted %d snippets" % len(meta))


# Render each frozen snippet into an editor-panel HTML fragment
def render() -> None:
    GENERATED.mkdir(exist_ok=True)
    meta: dict = json.loads((SNIPPETS / "manifest.json").read_text())
    source_cache: dict = {}
    for name, info in meta.items():
        rel: str = info["file"]
        if rel not in source_cache:
            source_cache[rel] = (COOTIES / rel).read_text().splitlines()
        lines: list[str] = source_cache[rel]
        rows: list[str] = []
        for si, (a, b) in enumerate(info["segments"]):
            if si > 0:
                rows.append(
                    '<div class="ed-line ed-gap"><span class="ed-num">&#8942;</span>'
                    '<span class="ed-code g-comment"># ...</span></div>'
                )
            for n in range(a, b + 1):
                line: str = lines[n - 1]
                for old, new in REWRITE.get(name, []):
                    line = line.replace(old, new)
                rows.append(
                    '<div class="ed-line" data-l="%d"><span class="ed-num">%d</span>'
                    '<span class="ed-code">%s</span></div>'
                    % (n, n, highlight_line(line) or "&nbsp;")
                )
        panel: str = (
            '<div class="editor" data-snippet="%s">\n'
            '<div class="ed-tabs"><span class="ed-tab active">%s<span class="ed-x">&times;</span></span></div>\n'
            '<div class="ed-crumb">%s</div>\n'
            '<div class="ed-body">\n%s\n</div>\n'
            '<div class="ed-status"><span>%s</span><span class="ed-status-r">%d:1 &nbsp; GDScript</span></div>\n'
            '</div>' % (name, info["tab"], html.escape(info["crumb"]), "\n".join(rows),
                        html.escape(info["file"]), info["end"])
        )
        (GENERATED / (name + ".html")).write_text(panel + "\n")
    print("rendered %d panels" % len(meta))


if __name__ == "__main__":
    mode: str = sys.argv[1] if len(sys.argv) > 1 else "render"
    if mode == "extract":
        extract()
    elif mode == "render":
        render()
    else:
        sys.exit("usage: gdhl.py extract|render")
