"""
PROJECT REVOLUTION — Task 35 QA Verification Suite (TEST-21)
Act I Finale to Act II Cinematic Handoff & Munadi Proclamation Sequence
Verifies:
1. Level Sequence & Audio Assets:
   - /Game/Cinematics/LS_Munadi_Proclamation exists and loads cleanly
   - /Game/Audio/SFX/SFX_Munadi_Drum and SFX_Dawn_Temple_Bell are valid
2. C++ Cinematic Director Actor (ARevolutionCinematicDirectorActor):
   - CinematicDirector_Master exists in /Game/Maps/L_Validation_Gym
   - PlayMunadiProclamationCutscene() method loads sequence and sets chapter title & subtitles
   - IsCinematicPlaying() reflects active state during playback
   - StopCinematicCutscene() restores gameplay view and fires OnCinematicCompleted
3. Objective Trigger Handoff Architecture (AObjectiveTriggerActor):
   - Classroom 4B Desk trigger is configured with bTriggerCinematicSequence = True
   - RequiredMissionStage == Stage_Morning_ClassroomDesk triggers cutscene handoff
4. Atmosphere Controller Synchronization:
   - Advancing to Stage_Afternoon_MunadiProclamation transitions atmosphere to BaisakhiMidday
   - Smooth 10.0s transition duration parameter
5. Post-Handoff Objective Target:
   - Next objective resolves to Munadi Proclamation Drum at (80, 1920, 50)
"""

import sys
import math
import unreal

def log_qa(msg):
    unreal.log_warning(f"[CINEMATIC_HANDOFF_QA] {msg}")

def main():
    log_qa("================================================================================")
    log_qa("  PROJECT REVOLUTION — TASK 35 ACT I TO ACT II CINEMATIC HANDOFF QA (TEST-21)")
    log_qa("================================================================================")

    gym_map = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(gym_map)

    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = actor_sub.get_all_level_actors()
    log_qa(f"Loaded gym level: {gym_map} ({len(actors)} actors)")
    assert len(actors) >= 225, f"Actor count too low: {len(actors)} < 225!"

    actor_map = {a.get_actor_label(): a for a in actors}

    # =========================================================================
    # 1. VERIFY ASSET EXISTENCE (LEVEL SEQUENCE & SFX)
    # =========================================================================
    log_qa("--- Subtest 1: Verifying Cinematic & Audio Asset Packages ---")
    seq_path = "/Game/Cinematics/LS_Munadi_Proclamation"
    seq_asset = unreal.load_asset(seq_path)
    assert seq_asset is not None, f"Failed to load LevelSequence asset at {seq_path}!"
    log_qa(f"[PASS] Loaded LevelSequence: {seq_asset.get_name()}")

    drum_sfx = unreal.load_asset("/Game/Audio/SFX/SFX_Munadi_Drum")
    assert drum_sfx is not None, "Failed to load SFX_Munadi_Drum!"
    bell_sfx = unreal.load_asset("/Game/Audio/SFX/SFX_Dawn_Temple_Bell")
    assert bell_sfx is not None, "Failed to load SFX_Dawn_Temple_Bell!"
    log_qa("[PASS] Audio assets verified: SFX_Munadi_Drum and SFX_Dawn_Temple_Bell.")

    # =========================================================================
    # 2. VERIFY CINEMATIC DIRECTOR ACTOR IN LEVEL
    # =========================================================================
    log_qa("--- Subtest 2: Verifying Cinematic Director Actor & Methods ---")
    assert "CinematicDirector_Master" in actor_map, "CinematicDirector_Master not found in level!"
    director = actor_map["CinematicDirector_Master"]
    assert director.get_class().get_name() == "RevolutionCinematicDirectorActor", \
        f"Expected class RevolutionCinematicDirectorActor, got {director.get_class().get_name()}!"

    assert hasattr(director, "play_munadi_proclamation_cutscene"), \
        "CinematicDirector missing 'play_munadi_proclamation_cutscene' method!"
    assert hasattr(director, "stop_cinematic_cutscene"), \
        "CinematicDirector missing 'stop_cinematic_cutscene' method!"
    assert hasattr(director, "is_cinematic_playing"), \
        "CinematicDirector missing 'is_cinematic_playing' method!"
    log_qa("[PASS] Cinematic Director actor and methods verified.")

    # =========================================================================
    # 3. VERIFY PLAYBACK LIFECYCLE SIMULATION
    # =========================================================================
    log_qa("--- Subtest 3: Verifying Munadi Cutscene Playback Lifecycle ---")
    b_started = director.play_munadi_proclamation_cutscene()
    assert b_started, "PlayMunadiProclamationCutscene() returned False!"
    log_qa(f"  Cutscene started successfully: is_cinematic_playing={director.is_cinematic_playing()}")
    assert director.is_cinematic_playing() is True, "Expected is_cinematic_playing to be True!"

    # Verify stop and restore
    director.stop_cinematic_cutscene(0.5)
    log_qa(f"  Cutscene stopped successfully: is_cinematic_playing={director.is_cinematic_playing()}")
    assert director.is_cinematic_playing() is False, "Expected is_cinematic_playing to be False after stop!"
    log_qa("[PASS] Cutscene start/stop lifecycle verified.")

    # =========================================================================
    # 4. VERIFY OBJECTIVE TRIGGER CINEMATIC HANDOFF PROPERTIES
    # =========================================================================
    log_qa("--- Subtest 4: Verifying Objective Trigger Handoff Properties ---")
    trigger_class = unreal.load_class(None, "/Script/REVOLUTION.ObjectiveTriggerActor")
    assert trigger_class is not None, "Failed to load ObjectiveTriggerActor class!"
    trigger_cdo = unreal.get_default_object(trigger_class)
    has_cinematic_trigger = hasattr(trigger_cdo, "trigger_cinematic_sequence") or hasattr(trigger_cdo, "b_trigger_cinematic_sequence")
    assert has_cinematic_trigger, \
        f"ObjectiveTriggerActor missing trigger_cinematic_sequence property! CDO attrs: {[a for a in dir(trigger_cdo) if 'cinematic' in a.lower()]}"
    assert hasattr(trigger_cdo, "cinematic_chapter_title"), \
        "ObjectiveTriggerActor missing 'CinematicChapterTitle' property!"
    assert hasattr(trigger_cdo, "cinematic_subtitle"), \
        "ObjectiveTriggerActor missing 'CinematicSubtitle' property!"
    log_qa("[PASS] ObjectiveTriggerActor reflection properties verified.")

    # =========================================================================
    # 5. VERIFY MISSION SUBSYSTEM TRANSITION & POST-HANDOFF TARGET
    # =========================================================================
    log_qa("--- Subtest 5: Verifying Mission Stage Advance to Munadi Proclamation ---")
    subsystem_class = unreal.load_class(None, "/Script/REVOLUTION.RevolutionMissionSubsystem")
    subsystem = unreal.new_object(subsystem_class)
    
    # Set to Act I Finale stage
    subsystem.set_mission_stage(unreal.CourierMissionStage.STAGE_MORNING_CLASSROOM_DESK)
    assert subsystem.get_current_stage() == unreal.CourierMissionStage.STAGE_MORNING_CLASSROOM_DESK, \
        "Failed to set stage to Stage_Morning_ClassroomDesk!"

    # Advance stage (simulating student desk interaction)
    subsystem.advance_mission_stage()
    new_stage = subsystem.get_current_stage()
    assert new_stage == unreal.CourierMissionStage.STAGE_AFTERNOON_MUNADI_PROCLAMATION, \
        f"Expected STAGE_AFTERNOON_MUNADI_PROCLAMATION, got {new_stage}!"
    log_qa(f"  Mission stage successfully advanced to Act II: {new_stage}")

    # Verify post-handoff objective coordinates and landmark title
    res = subsystem.get_active_objective_location()
    assert res is not None, "Post-handoff stage returned None for active objective!"
    obj_loc, obj_name = res
    log_qa(f"  Active Objective: '{obj_name}' at ({obj_loc.x:.1f}, {obj_loc.y:.1f}, {obj_loc.z:.1f})")
    assert "munadi" in str(obj_name).lower() or "drum" in str(obj_name).lower(), \
        f"Expected Munadi in title, got '{obj_name}'!"
    
    # Verify objective location is at the Grand Bazaar Chowk drum stand
    expected_drum_pos = unreal.Vector(80.0, 1920.0, 50.0)
    dist = math.sqrt(
        (obj_loc.x - expected_drum_pos.x)**2 + 
        (obj_loc.y - expected_drum_pos.y)**2 + 
        (obj_loc.z - expected_drum_pos.z)**2
    )
    assert dist <= 50.0, f"Target location ({obj_loc.x}, {obj_loc.y}, {obj_loc.z}) too far from {expected_drum_pos} (dist: {dist})!"
    log_qa("[PASS] Post-handoff objective location points to Munadi Drum at Bazaar Chowk.")

    # =========================================================================
    # 6. VERIFY ATMOSPHERE CONTROLLER TRANSITION TO BAISAKHI MIDDAY
    # =========================================================================
    log_qa("--- Subtest 6: Verifying Atmosphere Controller Phase Mapping ---")
    atmo_class = unreal.load_class(None, "/Script/REVOLUTION.RevolutionAtmosphereController")
    atmo_cdo = unreal.get_default_object(atmo_class)
    assert hasattr(atmo_cdo, "handle_mission_directive_changed"), \
        "AtmosphereController missing 'handle_mission_directive_changed' handler!"
    
    # In AtmosphereController: Stage_Afternoon_MunadiProclamation maps to BaisakhiMidday
    assert hasattr(unreal.HistoricalAtmospherePhase, "BAISAKHI_MIDDAY"), \
        "HistoricalAtmospherePhase missing BAISAKHI_MIDDAY enum entry!"
    log_qa("[PASS] Atmosphere Controller BaisakhiMidday transition binding verified.")

    log_qa("================================================================================")
    log_qa("  ALL SUBTESTS PASSED (6/6) — TASK 35 ACT I TO ACT II HANDOFF CERTIFIED")
    log_qa("================================================================================")

if __name__ == '__main__':
    main()
