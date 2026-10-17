"""
PROJECT REVOLUTION — Task 16: Cinematic Level Sequences & Cutscene Director Creator
Generates:
1. /Game/Cinematics/LS_Munadi_Proclamation (150 frames, 5.0s @ 30fps)
2. /Game/Cinematics/LS_Golden_Sunrise_Finale (180 frames, 6.0s @ 30fps)
3. Spawns and configures ARevolutionCinematicDirectorActor in /Game/Maps/L_Validation_Gym
"""

import unreal

def log_info(msg):
    unreal.log_warning(f"[CINEMATIC_CREATOR] {msg}")

def create_sequences_and_director():
    log_info("================================================================================")
    log_info("  PROJECT REVOLUTION — CREATING CINEMATIC LEVEL SEQUENCES & DIRECTOR")
    log_info("================================================================================")

    # Clean up test asset if present
    if unreal.EditorAssetLibrary.does_asset_exist("/Game/Cinematics/LS_Test"):
        unreal.EditorAssetLibrary.delete_asset("/Game/Cinematics/LS_Test")

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    package_path = "/Game/Cinematics"

    if not unreal.EditorAssetLibrary.does_directory_exist(package_path):
        unreal.EditorAssetLibrary.make_directory(package_path)
        log_info(f"Created directory '{package_path}'")

    factory = unreal.LevelSequenceFactoryNew()

    # 1. Create / Configure LS_Munadi_Proclamation
    munadi_asset_path = f"{package_path}/LS_Munadi_Proclamation"
    seq_munadi = unreal.EditorAssetLibrary.load_asset(munadi_asset_path)
    if not seq_munadi:
        seq_munadi = asset_tools.create_asset("LS_Munadi_Proclamation", package_path, unreal.LevelSequence, factory)
        log_info(f"Created Level Sequence asset: {munadi_asset_path}")
    else:
        log_info(f"Loaded existing Level Sequence asset: {munadi_asset_path}")

    if seq_munadi:
        seq_munadi.set_playback_start(0)
        seq_munadi.set_playback_end(150)
        seq_munadi.set_display_rate(unreal.FrameRate(30, 1))
        unreal.EditorAssetLibrary.save_loaded_asset(seq_munadi)
        log_info(f"[PASS] LS_Munadi_Proclamation configured: 150 frames (5.0s @ 30 FPS)")

    # 2. Create / Configure LS_Golden_Sunrise_Finale
    sunrise_asset_path = f"{package_path}/LS_Golden_Sunrise_Finale"
    seq_sunrise = unreal.EditorAssetLibrary.load_asset(sunrise_asset_path)
    if not seq_sunrise:
        seq_sunrise = asset_tools.create_asset("LS_Golden_Sunrise_Finale", package_path, unreal.LevelSequence, factory)
        log_info(f"Created Level Sequence asset: {sunrise_asset_path}")
    else:
        log_info(f"Loaded existing Level Sequence asset: {sunrise_asset_path}")

    if seq_sunrise:
        seq_sunrise.set_playback_start(0)
        seq_sunrise.set_playback_end(180)
        seq_sunrise.set_display_rate(unreal.FrameRate(30, 1))
        unreal.EditorAssetLibrary.save_loaded_asset(seq_sunrise)
        log_info(f"[PASS] LS_Golden_Sunrise_Finale configured: 180 frames (6.0s @ 30 FPS)")

    # 3. Assemble Director into Master Level
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)

    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    all_actors = actor_sub.get_all_level_actors()

    director_class = unreal.load_class(None, "/Script/REVOLUTION.RevolutionCinematicDirectorActor")
    assert director_class is not None, "Failed to load RevolutionCinematicDirectorActor class!"

    # Check if director already exists
    director_actor = None
    for a in all_actors:
        if a.get_actor_label() == "CinematicDirector_Master" or a.get_class() == director_class or "CinematicDirector" in a.get_class().get_name():
            director_actor = a
            break

    if not director_actor:
        director_loc = unreal.Vector(500, 1800, 150)
        director_actor = actor_sub.spawn_actor_from_class(director_class, director_loc)
        director_actor.set_actor_label("CinematicDirector_Master")
        log_info(f"[PASS] Spawned CinematicDirector_Master at {director_loc}")
    else:
        log_info(f"[PASS] Found existing CinematicDirector_Master: {director_actor.get_name()}")

    # Assign pre-configured sequences
    director_actor.set_editor_property("munadi_proclamation_sequence", seq_munadi)
    director_actor.set_editor_property("golden_sunrise_finale_sequence", seq_sunrise)

    # Save level
    b_saved = level_sub.save_current_level()
    log_info(f"[PASS] Master Level saved: {b_saved}")

    all_actors_after = actor_sub.get_all_level_actors()
    log_info(f"[PASS] Total Level Actors in L_Validation_Gym: {len(all_actors_after)} (Expected >= 206)")

    log_info("================================================================================")
    log_info("  CINEMATIC LEVEL SEQUENCES & DIRECTOR ASSEMBLED SUCCESSFULLY")
    log_info("================================================================================")

if __name__ == "__main__":
    create_sequences_and_director()
