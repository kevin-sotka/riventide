# Riventide, browser build (vanilla JS)

The web version of Riventide. One self-contained `index.html`, a generated
`story.json`, and the images and audio streamed on demand. No dependencies,
no build toolchain, no runtime to download.

This replaces the pygbag build in `../docs`. The desktop pygame game
(`../main.py`) is untouched and remains the canonical version to edit.

## Why this exists

The pygbag build shipped a 32MB archive containing CPython, pygame-ce and
every asset, and the player stared at a loading screen for a minute before
anything happened. It also broke outright when an upstream CSS assumption
in pygbag's own template changed (see the note in `../tools/build_web.sh`).

Riventide is text, a background image, music, and numbered choices. None of
that needs a Python runtime compiled to WebAssembly. This version loads in
about two seconds, works on a phone, and cannot break because someone else
moved a file on a CDN.

| | pygbag (`../docs`) | this |
|---|---|---|
| First paint | ~60-90s | ~2s |
| Downloaded before play | ~32MB | ~220KB |
| Assets | all bundled up front | streamed per scene |
| Mobile | poor | first-class |
| Upstream deps | pygbag + its CDN | none |

## How it works

`story.json` is **generated, never hand-edited**. The story lives in
`../game/world/world.py` as plain dicts, so `../tools/extract_story.py`
imports `World` and dumps it rather than duplicating 3,900 lines of prose.
Edit the story in `world.py` as always, then re-run the build.

The runtime rules mirror the Python engine:

- `{player_name}` is substituted throughout.
- A choice with `modifier_required` is hidden until the player holds that flag
  (`game/engine.py::available_choices`).
- Taking a choice with `modifier` sets that flag.
- A location's `modifiers` map appends extra description paragraphs once the
  matching flag is held.
- Race and class become `race_<x>` / `class_<y>` flags at creation, exactly as
  `CharacterCreationScreen._handle_review()` does.

Progress saves to `localStorage` after every scene, so Continue on the title
screen resumes where the player left off.

## Build

```bash
bash ../tools/build_webjs.sh
```

Extracts the story, then assembles `dist/` (HTML + JSON + a copy of
`../web/assets`). Requires `../web/assets` to exist; produce it once with
`python ../tools/build_web_assets.py`.

## Run locally

```bash
python3 -m http.server 8200 --directory .
```

`assets` here is a symlink to `../web/assets` for development. `dist/` gets a
real copy.

## Publish

`dist/` is a complete static site. To serve it from GitHub Pages in place of
the pygbag build:

```bash
rm -rf ../docs && cp -R dist ../docs
```

Pages is configured to serve `/docs` on `main`. Note that `../web/` is
gitignored today, so publishing this way commits roughly 32MB of loose asset
files that were previously only present inside the pygbag archive.

## Verified

- 113 locations, 227 choices, zero broken destinations, zero unknown flags.
- Every gate is satisfiable; an ending is reachable from all 102 rooms that
  are reachable from the start.
- Shortest complete run is 20 choices, passing three real gates
  (`humming_crystal`, `invasion_knowledge`, `complete_knowledge`).
- 8 locations are orphans with no inbound choice. They are orphans in
  `world.py` too, not a porting artifact: `drakkar_capital`, `drakkar_mines`,
  `drakkar_border`, `magic_tavern`, `ambush_negotiation_fail`,
  `continue_journey_path`, `crystal_disruption_attempt`, `rune_defense_attempt`.

## Known gaps

- No combat. Two choices in `world.py` carry `trigger_combat`; here they show
  a brief flourish and move on, which is what the pygame build effectively
  does with them today.
- Quests, shops, inns and NPCs exist as data on three locations but were never
  wired up in the pygame engine either, so nothing reads them.
