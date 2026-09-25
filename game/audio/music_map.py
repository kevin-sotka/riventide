"""Which music track plays where, for both the desktop and browser builds.

This is the single source of truth for Riventide's music. The desktop engine
(game/engine.py) and AudioManager.play_music_for_location() read it directly.
tools/extract_story.py copies it into web-js/story.json, refuses to build if
any location is missing from LOCATION_MUSIC, if any track named here has no
.ogg under assets/audio/music, or if any .ogg on disk is never used, and
writes web-js/MUSIC_MAP.md from it.

Rules this table follows:
  * main_theme belongs to the title screen only.
  * intro_music covers character creation and the opening in Eldoria, and
    gives way to royal_court when the herald brings you to the court.
  * No "in between" screen falls back to a generic track. A transition
    screen plays the music of the scene it leads into (eldoria_gate plays
    whisperwood, not main_theme), so the change happens once, at the
    transition, rather than dipping out for one screen and back.
  * A location keeps playing the current track when the next one is the
    same file; the player never restarts a track it is already playing.

Locations built on the fly (the engine's "Unknown Location" placeholder, for
one) are not in the table; track_for_location() returns None for them and the
current track keeps playing.
"""

# Screens that are not story locations.
SCREEN_MUSIC = {
    "title":  "main_theme",    # title screen, before and between runs
    "create": "intro_music",   # character creation
    "fin":    None,            # "The Tale Ends" card: the ending's track keeps playing
}

# Every location in game/world/world.py, in rough story order.
LOCATION_MUSIC = {
    # --- Eldoria -------------------------------------------------------------
    "eldoria_introduction":        "intro_music",
    "royal_court":                 "royal_court",
    "royal_court_segue_artifact":  "royal_court",
    "royal_court_segue_rune":      "royal_court",
    "royal_court_segue_alchemist": "royal_court",
    "eldoria_gate":                "whisperwood",   # the walk out to Whisperwood

    # --- Whisperwood ---------------------------------------------------------
    "whisperwood_start":           "whisperwood",
    "mushroom_path":               "whisperwood",
    "flee_ambush_attempt":         "whisperwood",
    "continue_journey_path":       "whisperwood",
    "ambush_victory":              "whisperwood",
    "alien_tech_discovery":        "alien_tech",
    "device_activation":           "alien_tech",
    "tech_fragment_path":          "alien_tech",
    "device_destruction_path":     "alien_tech",
    "synthetic_clearing":          "synthetic",
    "bioengineered_creatures":     "synthetic",     # mushrooms with metal implants
    "faerie_vision":               "faerie_realm",
    "tech_ambush_risk":            "combat",
    "tech_soldiers_parley":        "combat",
    "ambush_negotiation_fail":     "combat",
    "crystal_disruption_attempt":  "combat",
    "rune_defense_attempt":        "combat",
    "combat_tech_soldiers_weakened": "combat",
    "combat_tech_soldiers":        "death_music",
    "continue_to_faerie":          "faerie",

    # --- Faerie realm --------------------------------------------------------
    "faerie_border":               "faerie_realm",
    "faerie_realm_entrance":       "faerie_realm",
    "faerie_scouts":               "faerie_scouts",
    "faerie_escort":               "faerie_scouts",
    "faerie_invasion_reaction":    "faerie_scouts",
    "faerie_tech_reaction":        "faerie",
    "faerie_city_approach":        "faerie",
    "faerie_realm_entry":          "faerie",
    "faerie_rescue":               "faerie",
    "faerie_defense_preparations": "faerie",
    "faerie_alliance":             "faerie",
    "faerie_war_council":          "faerie",
    "test_of_loyalty":             "crystal_grove",
    "drone_aftermath":             "crystal_grove",
    "crystal_interface":           "knowledge_interface",
    "knowledge_repository":        "knowledge_interface",
    "overloaded_connection":       "knowledge_interface",
    "safe_disconnect":             "knowledge_interface",
    "faerie_favor":                "knowledge_interface",
    "grackle_ship_mission":        "faerie_scouts",  # planning with Sylvara's scouts
    "mission_preparation":         "faerie_scouts",
    "outpost_destruction":         "synthetic",      # Grackle-corrupted outpost

    # --- Crash site ----------------------------------------------------------
    "crash_site_retrieval":        "crash_site",
    "heartstone_retrieval":        "crash_site",
    "heartstone_secured":          "crash_site",
    "crash_site_collapse":         "crash_site",

    # --- Grackles ------------------------------------------------------------
    "grackle_encounter":           "grackle_encounter",
    "grackle_deception":           "grackle_encounter",
    "forest_escape":               "grackle_encounter",
    "grackle_alliance_offer":      "grackle_encounter",
    "sneak_aboard":                "grackle_encounter",
    "grackle_infiltrator":         "grackle_encounter",
    "grackle_sabotage":            "alien_tech",     # the ship's power core
    "grackle_tracking":            "grackle_scout",  # hunted by the scout ship
    "sensor_probe":                "grackle_scout",
    "scout_ship_battle":           "combat",
    "map_escape":                  "combat",
    "data_core_escape":            "alien_tech",
    "larger_vessel_threat":        "death_music",
    "larger_grackle_force":        "death_music",
    "void_transport":              "faerie_realm",
    "grackle_incursion":           "synthetic",
    "warship_focus":               "synthetic",
    "spire_shielded":              "synthetic",
    "vision_of_tanis":             "alien_tech",
    "void_exile":                  "tragic",
    "tanis_portal":                "faerie_realm",   # aboard the faerie warship

    # --- Vanlander Prison ----------------------------------------------------
    "captured_by_grackles":        "captured_by_grackles",
    "vanlander_prison_capture":    "vanlander_prison",
    "vent_escape":                 "vanlander_prison",
    "panel_escape":                "vanlander_prison",
    "delayed_escape":              "vanlander_prison",
    "hidden_exit":                 "vanlander_prison",
    "alternate_route":             "vanlander_prison",
    "maintenance_shaft":           "vanlander_prison",
    "outer_pursuit":               "vanlander_prison",
    "safe_exit":                   "vanlander_prison",
    "power_core":                  "alien_tech",
    "alarm_escape":                "combat",
    "lockdown":                    "combat",
    "injured_retreat":             "combat",
    "shuttle_chase":               "combat",
    "recapture":                   "defeat",

    # --- The void and the asteroid -------------------------------------------
    "void_survival":               "tragic",
    "safe_haven_search":           "tragic",
    "cave_shelter":                "tragic",
    "crash_landing":               "crash_site",
    "recovered_ally":              "crash_site",
    "crystal_signal":              "faerie",         # the faerie beacon
    "miracle_ship":                "faerie_realm",   # hidden faerie ship

    # --- Shadowlands and Malgrim ---------------------------------------------
    "shadowlands_approach":        "shadowlands",
    "malgrim_fortress_infiltration": "shadowlands",
    "malgrim_audience":            "boss_battle",
    "malgrim_fortress_gate":       "boss_battle",    # the dawn assault
    "malgrim_throne_room":         "boss_battle",
    "malgrim_showdown":            "boss_battle",
    "final_showdown":              "boss_battle",

    # --- Endings -------------------------------------------------------------
    "ending_heros_victory":        "victory",
    "ending_pyrrhic_victory":      "tragic",
    "ending_double_agent":         "shadowlands",
    "ending_forgotten_prisoner":   "defeat",
    "story_end":                   "tavern",         # the WanderLost Tavern reveal
    "magic_tavern":                "tavern",
    "title_screen":                "main_theme",     # "Another Tale Awaits"

    # --- Drakkar (not reachable from the current story) ----------------------
    "drakkar_capital":             "royal_court",
    "drakkar_mines":               "royal_court",
    "drakkar_border":              "royal_court",
}


def track_for_location(location_id):
    """The track for a location, or None to keep whatever is playing."""
    return LOCATION_MUSIC.get(location_id)
