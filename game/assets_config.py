"""
game/assets_config.py

Single switch point for the pygame (desktop) -> pygbag (web) asset path
rewiring. Selects a base directory + file extension for graphics and audio
based on the RIVENTIDE_WEB environment variable, so the loaders in
game/ui/graphics_manager.py and game/audio/audio_manager.py never hardcode
web-specific paths themselves.

Desktop behavior (RIVENTIDE_WEB unset or not "1") is completely unchanged:
graphics stay under assets/graphics/**/*.png and audio under
assets/audio/{music,sfx}/**/*.wav, exactly as before this module existed.

Set RIVENTIDE_WEB=1 (web_main.py does this at process start, before any
game.* module is imported) to switch to the transcoded web asset tree
produced by tools/build_web_assets.py: web/assets/graphics/**/*.webp and
web/assets/audio/{music,sfx}/**/*.ogg.
"""

import os

IS_WEB = os.environ.get("RIVENTIDE_WEB") == "1"

# Base directories (no trailing slash), relative to the repo root.
GRAPHICS_BASE = "web/assets/graphics" if IS_WEB else "assets/graphics"
AUDIO_BASE = "web/assets/audio" if IS_WEB else "assets/audio"

# Extensions used under each base directory.
GRAPHICS_EXT = ".webp" if IS_WEB else ".png"
AUDIO_EXT = ".ogg" if IS_WEB else ".wav"

_DESKTOP_GRAPHICS_PREFIX = "assets/graphics/"


def graphics_path(desktop_relative_path: str) -> str:
    """Rewrite a desktop-style "assets/graphics/.../name.png" path onto the
    active graphics base dir + extension.

    Video files (.mp4) are intentionally left untouched: build_web_assets.py
    does not transcode video, and GraphicsManager._load_video_background()
    never actually opens this path (it only prints it and falls back to a
    placeholder), so there's nothing to rewrite safely to and no behavior
    to preserve either way.
    """
    rel = desktop_relative_path
    if rel.startswith(_DESKTOP_GRAPHICS_PREFIX):
        rel = rel[len(_DESKTOP_GRAPHICS_PREFIX):]

    root, ext = os.path.splitext(rel)
    if ext.lower() == ".mp4":
        return desktop_relative_path

    return f"{GRAPHICS_BASE}/{root}{GRAPHICS_EXT}"
