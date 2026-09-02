#!/usr/bin/env python3
"""
Extract Riventide's story graph out of the Python game into plain JSON.

The scene data in game/world/world.py is already uniform dicts, so this
imports World and dumps it rather than re-authoring 3,900 lines by hand.
Same for the race/class tables and the modifier registry. Run it again
after any story edit in world.py to regenerate the JSON the browser
build reads.

    python tools/extract_story.py           # -> web-js/story.json

Asset paths are rewritten onto the transcoded web tree that
tools/build_web_assets.py already produces (web/assets, .jpg/.png/.ogg),
so the browser build streams the same files the pygbag build bundled.
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ["RIVENTIDE_WEB"] = "1"  # select the web asset tree in assets_config

from game.world.world import World                      # noqa: E402
from game.characters.character_races import RACES        # noqa: E402
from game.characters.character_classes import CLASSES    # noqa: E402
from game.utils.game_state import GameState              # noqa: E402
from game.assets_config import graphics_path             # noqa: E402

WEB_ASSETS = ROOT / "web" / "assets"


def _resolve_background(name):
    """Map a location's "background" key onto a real file under web/assets.

    GraphicsManager keys these as "background_<name>" and stores desktop
    .png paths; the web tree carries .jpg for opaque images and .png for
    the few with alpha. Probe for whatever actually exists and return a
    path relative to the game root, or None so the page can fall back to
    a solid colour rather than a broken image.
    """
    if not name:
        return None
    for ext in (".jpg", ".png"):
        rel = f"graphics/backgrounds/{name}{ext}"
        if (WEB_ASSETS / rel).exists():
            return f"assets/{rel}"
    return None


def _resolve_audio(name, kind):
    if not name:
        return None
    rel = f"audio/{kind}/{name}.ogg"
    return f"assets/{rel}" if (WEB_ASSETS / rel).exists() else None


def main():
    world = World()

    locations = {}
    for region_id, region in world.regions.items():
        for loc_id, loc in (region.get("locations") or {}).items():
            out = {
                "id": loc_id,
                "region": region_id,
                "name": loc.get("name"),
                "description": loc.get("description"),
                "dialogue": loc.get("dialogue") or [],
                "choices": loc.get("choices") or [],
                "background": _resolve_background(loc.get("background")),
                "backgroundKey": loc.get("background"),
            }
            # Optional keys, only emitted when the location actually has them.
            if loc.get("modifiers"):
                out["modifierText"] = loc["modifiers"]
            if loc.get("music"):
                out["music"] = _resolve_audio(loc["music"], "music")
            locations[loc_id] = out

    # Region-level default music, used when a location declares none.
    region_music = {}
    for region_id in world.regions:
        region_music[region_id] = _resolve_audio(region_id, "music")

    data = {
        "start": world.get_starting_location()["id"]
        if world.get_starting_location() else "eldoria_introduction",
        "locations": locations,
        "regions": {rid: {"id": rid, "name": r.get("name"), "music": region_music.get(rid)}
                    for rid, r in world.regions.items()},
        "races": RACES,
        "classes": CLASSES,
        "modifiers": sorted(GameState().player_modifiers.keys()),
    }

    out_dir = ROOT / "web-js"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "story.json"
    out_path.write_text(json.dumps(data, indent=1, ensure_ascii=False))

    missing_bg = sorted({l["backgroundKey"] for l in locations.values()
                         if l["backgroundKey"] and not l["background"]})
    print(f"wrote {out_path.relative_to(ROOT)}")
    print(f"  locations   {len(locations)}")
    print(f"  choices     {sum(len(l['choices']) for l in locations.values())}")
    print(f"  races       {len(RACES)}   classes {len(CLASSES)}")
    print(f"  modifiers   {len(data['modifiers'])}")
    print(f"  size        {out_path.stat().st_size/1024:.0f} KB")
    if missing_bg:
        print(f"  MISSING backgrounds ({len(missing_bg)}): {', '.join(missing_bg)}")


if __name__ == "__main__":
    main()
