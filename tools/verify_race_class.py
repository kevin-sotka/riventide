"""
Standalone verification for the race/class modifier feature.

Constructs a GameState directly (no pygame/display needed), simulates the
modifier-setting step that CharacterCreationScreen._handle_review() performs
for every race and every class, and asserts:

  1. The expected "race_<id>" / "class_<id>" modifier is registered in
     GameState.player_modifiers and gets set to True.
  2. No other race_* / class_* modifier gets set as a side effect.
  3. GameState.reset() clears all race_*/class_* modifiers, so a second
     playthrough with a different race/class doesn't inherit the first
     one's flags.

Run with:
    SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy .venv/bin/python tools/verify_race_class.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.utils.game_state import GameState
from game.characters.character_races import RACES
from game.characters.character_classes import CLASSES


def race_class_modifier_names():
    race_mods = [f"race_{name.lower()}" for name in RACES.keys()]
    class_mods = [f"class_{name.lower()}" for name in CLASSES.keys()]
    return race_mods, class_mods


def all_other_flags_false(game_state, exclude, universe):
    """Assert every modifier in `universe` except `exclude` is still False."""
    problems = []
    for name in universe:
        if name == exclude:
            continue
        if game_state.player_modifiers.get(name) is not False:
            problems.append(name)
    return problems


def main():
    race_mods, class_mods = race_class_modifier_names()
    all_race_class_mods = race_mods + class_mods

    failures = []

    print("Race identifiers found:", list(RACES.keys()))
    print("Class identifiers found:", list(CLASSES.keys()))
    print(f"Expected race modifiers: {race_mods}")
    print(f"Expected class modifiers: {class_mods}")
    print()

    # --- Test each race in isolation ---
    for race_name in RACES.keys():
        gs = GameState()
        modifier_name = f"race_{race_name.lower()}"

        # Sanity: modifier must be pre-declared or set_modifier silently no-ops
        assert modifier_name in gs.player_modifiers, (
            f"FAIL: '{modifier_name}' not declared in player_modifiers.__init__"
        )

        ok = gs.set_modifier(modifier_name)
        if not ok:
            failures.append(f"set_modifier('{modifier_name}') returned False")
            continue

        if gs.player_modifiers[modifier_name] is not True:
            failures.append(f"{modifier_name} was not set to True")

        stray = all_other_flags_false(gs, modifier_name, all_race_class_mods)
        if stray:
            failures.append(f"Setting {modifier_name} unexpectedly also set: {stray}")

        print(f"PASS: race '{race_name}' -> {modifier_name} = "
              f"{gs.player_modifiers[modifier_name]}")

    print()

    # --- Test each class in isolation ---
    for class_name in CLASSES.keys():
        gs = GameState()
        modifier_name = f"class_{class_name.lower()}"

        assert modifier_name in gs.player_modifiers, (
            f"FAIL: '{modifier_name}' not declared in player_modifiers.__init__"
        )

        ok = gs.set_modifier(modifier_name)
        if not ok:
            failures.append(f"set_modifier('{modifier_name}') returned False")
            continue

        if gs.player_modifiers[modifier_name] is not True:
            failures.append(f"{modifier_name} was not set to True")

        stray = all_other_flags_false(gs, modifier_name, all_race_class_mods)
        if stray:
            failures.append(f"Setting {modifier_name} unexpectedly also set: {stray}")

        print(f"PASS: class '{class_name}' -> {modifier_name} = "
              f"{gs.player_modifiers[modifier_name]}")

    print()

    # --- Test a combined race+class pick (mirrors what character creation does) ---
    gs = GameState()
    race_name = list(RACES.keys())[0]
    class_name = list(CLASSES.keys())[0]
    race_mod = f"race_{race_name.lower()}"
    class_mod = f"class_{class_name.lower()}"
    gs.set_modifier(race_mod)
    gs.set_modifier(class_mod)

    if not (gs.player_modifiers[race_mod] and gs.player_modifiers[class_mod]):
        failures.append("Combined race+class pick did not set both modifiers")
    else:
        print(f"PASS: combined pick ({race_name} + {class_name}) sets both "
              f"'{race_mod}' and '{class_mod}'")

    # --- Test reset() clears them, so a 2nd playthrough doesn't inherit flags ---
    gs.reset()
    leftover = [m for m in all_race_class_mods if gs.player_modifiers.get(m) is not False]
    if leftover:
        failures.append(f"reset() left stale race/class modifiers set: {leftover}")
    else:
        print("PASS: reset() clears all race_*/class_* modifiers "
              "(no bleed-through into a second playthrough)")

    # --- Test every race_*/class_* modifier is declared as False by default ---
    gs2 = GameState()
    not_false_by_default = [m for m in all_race_class_mods if gs2.player_modifiers.get(m) is not False]
    if not_false_by_default:
        failures.append(f"Fresh GameState has non-False race/class modifiers: {not_false_by_default}")
    else:
        print("PASS: fresh GameState.__init__ starts all race_*/class_* modifiers as False")

    print()
    if failures:
        print(f"RESULT: {len(failures)} FAILURE(S)")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print("RESULT: ALL CHECKS PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
