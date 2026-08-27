"""
web_main.py - Browser (pygbag) entrypoint for Riventide.

This is a SEPARATE entrypoint from main.py. main.py (argparse, colorama,
pyfiglet, sync GameEngine.start()) remains the desktop entrypoint and is
untouched by this file. web_main.py exists only to be built with pygbag,
e.g.:

    python -m pygbag --app_name Riventide web_main.py

(pygbag defaults to looking for main.py in the app folder - pointing it at
this file, or having the web build step copy/rename this into the web
build folder as main.py, is up to whatever sets up the pygbag build
directory. Nothing about that packaging is decided here.)

Why this file needs to exist at all, rather than just running main.py:

1. Blocking input(). main.py's text_only path (and GameEngine._text_game_loop)
   pull in game.ui.menu, game.ui.game_text, game.ui.character_creation, and
   game.utils.input_handler - between them, 14 blocking input() calls and 3
   os.system('clear') calls. There is no stdin in a browser tab; hitting any
   of those hangs or crashes the page. This file hard-forces
   text_only=False and never imports any of those modules, directly or
   transitively, so that call chain can never be reached.

2. Async main loop. Browsers (via pygbag/emscripten) require the game loop
   to periodically yield control with `await asyncio.sleep(0)` so the
   browser's own event loop can run - otherwise the tab appears frozen and
   audio/input never get serviced. GameEngine gained an async twin of the
   graphical loop for exactly this (_graphical_game_loop_async /
   start_async in game/engine.py); this file drives that async path via
   asyncio.run(main()) instead of the desktop's synchronous engine.start().

3. Autoplay policy. Browsers refuse to play any audio until the page has
   seen a user gesture (click, keypress, or touch). GameEngine.start_async()
   plays intro music as its very first act, so calling it immediately on
   page load would silently fail to produce sound. This file shows a
   "click or press any key to begin" splash screen first and only calls
   engine.start_async() once a gesture has been observed.
"""

import asyncio
import os

# Must be set before importing anything under game.* - game.ui.graphics_manager
# and game.audio.audio_manager both read game.assets_config's IS_WEB switch
# at import/class-definition time to select the web asset tree (web/assets/,
# .webp/.ogg) instead of the desktop one (assets/, .png/.wav).
os.environ["RIVENTIDE_WEB"] = "1"

import pygame

from game.engine import GameEngine

# Window size for the web build. Kept in one place so step 3 (asset/path
# work) can tweak it without touching the gating/loop logic below.
WEB_WIDTH = 800
WEB_HEIGHT = 600


async def _wait_for_user_gesture(engine: GameEngine):
    """Show a splash screen and block (async) until the player clicks,
    presses a key, or taps, so the caller can start audio afterward
    without tripping the browser's autoplay restrictions.

    Uses the engine's already-initialized pygame display (GraphicsManager's
    __init__ already called pygame.init()/display.set_mode() by the time
    the caller gets here) - no separate display setup needed.
    """
    screen = engine.graphics.screen
    width, height = engine.width, engine.height
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                engine.running = False
                return
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.FINGERDOWN):
                return

        screen.fill((0, 0, 50))  # Dark blue, matches the in-game menu background

        title_surface = engine.graphics.render_text("RIVENTIDE", 64, (255, 255, 100))
        if title_surface:
            screen.blit(
                title_surface,
                (width // 2 - title_surface.get_width() // 2, height // 2 - 80),
            )

        prompt_surface = engine.graphics.render_text(
            "Click or press any key to begin", 28, (220, 220, 255)
        )
        if prompt_surface:
            screen.blit(
                prompt_surface,
                (width // 2 - prompt_surface.get_width() // 2, height // 2 + 20),
            )

        pygame.display.flip()

        clock.tick(30)
        # Required so pygbag's emscripten runtime can keep servicing the
        # page (input, audio, rendering) while we wait for the gesture.
        await asyncio.sleep(0)


async def main():
    # Hard-force graphical mode. Do NOT trust GameEngine's own fallback
    # behavior here: if AudioManager/GraphicsManager raise during __init__,
    # GameEngine silently flips itself into text_only=True, which is a
    # dead end in a browser (no stdin for the input() calls that path
    # needs). Detect that fallback and fail loudly instead of limping
    # into a hung page.
    engine = GameEngine(width=WEB_WIDTH, height=WEB_HEIGHT, text_only=False)

    if engine.text_only:
        raise RuntimeError(
            "GameEngine fell back to text_only mode - audio/graphics failed "
            "to initialize in the browser. Refusing to start the blocking "
            "text-mode loop, which cannot run in a browser tab."
        )

    await _wait_for_user_gesture(engine)

    if not engine.running:
        # QUIT was posted while we were on the splash screen (unusual in a
        # browser tab, but handle it rather than starting audio anyway).
        return

    # This plays intro music as its first act, which is why it must run
    # only after _wait_for_user_gesture has observed a real user gesture.
    await engine.start_async()


if __name__ == "__main__":
    asyncio.run(main())
