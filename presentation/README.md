# GodotCon26 deck build pipeline

The deliverable is `../cooties-godotcon26.html`: a single self-contained file
(reveal.js, JetBrains Mono, and all images inlined). Copy it anywhere and
double-click; it needs no network. Optionally place a `cooties_clips.mp4` next
to it for the "What is Cooties?" slide.

## Editing

- Slide content and styling live in `deck-src.html`
- Code panels are generated from the cooties repo by `gdhl.py`:
  - The `MANIFEST` at the top maps snippet names to file + line ranges
    (a list of ranges renders an elided `# ...` gap between segments)
  - `python gdhl.py extract` refreshes `snippets/` (frozen verbatim copies)
  - `python gdhl.py render` regenerates `generated/*.html` editor panels
- `python build.py` assembles everything into `../cooties-godotcon26.html`

Full rebuild: `python gdhl.py extract && python gdhl.py render && python build.py`

## Live reload

`python presentation/dev.py` serves http://localhost:8137/cooties-godotcon26.html,
watches the presentation sources, rebuilds on save (including gdhl re-render when
the highlighter or snippets change), and auto-refreshes the browser. The reload
poll only activates over http, the built file stays fully offline from file://.

## Slide authoring notes

- `<!-- @panel:name -->` inside a `.ed-wrap` div inlines an editor panel
- Popup notes: `<div class="note fragment" data-line="63" data-hl="63-69">`,
  anchored and collision-resolved by JS; `data-hl` highlights those lines
  while the note is visible. Add class `alt` for a yellow border.
- `.reminder` divs are the quiet corner self-reminders
- Section tab strip follows each `<section data-section="...">`
- `?frag=N` in the URL steps N fragments after load (used for screenshots)

## Presenting

Arrows advance, ESC gives the overview grid, F is fullscreen.
PDF backup: open with `?print-pdf` appended in Chrome, then print to PDF.

## Outstanding placeholders

- Inspector screenshot on THE SYNC CONFIG slide
- Jitter before/after GIF on THE JITTER PROBLEM slide
- 2024 Steam game title on the whoami slide
