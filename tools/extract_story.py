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
from game.audio.audio_manager import AudioManager, MusicType  # noqa: E402
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


def _resolve_audio(name, kind="music"):
    if not name:
        return None
    rel = f"audio/{kind}/{name}.ogg"
    return f"assets/{rel}" if (WEB_ASSETS / rel).exists() else None


# Scene-specific overrides, copied from
# AudioManager.play_music_for_location_or_scene() step 1. They live in a local
# dict there rather than on the instance, so there is nothing to import.
SCENE_MUSIC = {
    "grackle_incursion": "synthetic",
    "vision_of_tanis": "alien_tech",
    "void_exile": "tragic",
    "spire_shielded": "synthetic",
    "warship_focus": "synthetic",
    "cave_shelter": "void_ambient",
    "injured_retreat": "prison_alarm",
    "crash_site_retrieval": "crash_site",
    "captured_by_grackles": "captured_by_grackles",
}


def _track_for_location(loc_id, audio):
    """Reproduce AudioManager.play_music_for_location_or_scene()'s choice.

    Same four tiers in the same order: a scene-specific override, then the
    region_music table (which is keyed by a mix of region names and location
    id prefixes, matched with startswith exactly as the engine does), then
    main_theme as the guaranteed fallback. Getting this wrong is why the
    first cut of this file emitted silence for most of the game: it assumed
    region id == filename, and there is no eldoria.ogg.

    Longest key first, so "whisperwood_start" wins over "whisperwood".
    """
    if loc_id in SCENE_MUSIC:
        return SCENE_MUSIC[loc_id]
    for key in sorted(audio.region_music, key=len, reverse=True):
        if loc_id.startswith(key):
            v = audio.region_music[key]
            return v.value if hasattr(v, "value") else v
    return MusicType.MAIN_THEME.value if hasattr(MusicType.MAIN_THEME, "value") \
        else MusicType.MAIN_THEME


def main():
    world = World()
    audio = AudioManager()

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
            # Every location gets a track. The engine always falls back to
            # main_theme, so silence is never the intended outcome; a location
            # whose chosen track has no .ogg on disk falls back here too.
            wanted = loc.get("music") or _track_for_location(loc_id, audio)
            out["music"] = _resolve_audio(wanted) or _resolve_audio("main_theme")
            out["musicKey"] = wanted
            if loc.get("modifiers"):
                out["modifierText"] = loc["modifiers"]
            locations[loc_id] = out

    # Region-level default, resolved through the same table rather than by
    # assuming the region id names a file.
    region_music = {}
    for region_id in world.regions:
        region_music[region_id] = (_resolve_audio(_track_for_location(region_id, audio))
                                   or _resolve_audio("main_theme"))

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
    silent = [k for k, l in locations.items() if not l["music"]]
    missing_track = sorted({l["musicKey"] for l in locations.values()
                            if l["musicKey"] and not _resolve_audio(l["musicKey"])})
    print(f"wrote {out_path.relative_to(ROOT)}")
    print(f"  locations   {len(locations)}")
    print(f"  choices     {sum(len(l['choices']) for l in locations.values())}")
    print(f"  races       {len(RACES)}   classes {len(CLASSES)}")
    print(f"  modifiers   {len(data['modifiers'])}")
    print(f"  size        {out_path.stat().st_size/1024:.0f} KB")
    tracks = sorted({l["music"] for l in locations.values() if l["music"]})
    print(f"  music       {len(tracks)} distinct tracks, {len(silent)} silent locations")
    if missing_bg:
        print(f"  MISSING backgrounds ({len(missing_bg)}): {', '.join(missing_bg)}")
    if missing_track:
        print(f"  no .ogg for track (fell back to main_theme): {', '.join(missing_track)}")


if __name__ == "__main__":
    main()
