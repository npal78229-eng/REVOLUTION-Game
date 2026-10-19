"""
PROJECT REVOLUTION — Task 26 QA Verification Suite: Multi-Dialect Punjabi Voice Recording Expansion
Validates:
1. All 8 authentic Punjabi vendor & crowd walla SoundWaves exist in /Game/Audio/Voice/
   - Majhi (4 tracks): Sabzi-Walla, Patrika Hawker, Chana Vendor, Elder Matron
   - Doabi (4 tracks): Kulfi-Walla, Kumhar Potter, Mandi Arhtiya, Mazdoor Porter
2. SoundClass & Attenuation Architecture:
   - 100% routed to SC_Voice_Punjabi and ATT_Voice_Proximity
3. C++ Class & UFUNCTION Reflection:
   - ARevolutionBazaarWallaActor loads and exposes play_walla_call, set_curfew_silenced, is_curfew_silenced
4. Master Level Integration:
   - /Game/Maps/L_Validation_Gym loaded cleanly with >= 209 actors
   - All 4 Bazaar Walla actors verified with valid voice and attenuation assignments
   - Curfew silencing logic verified
"""

import sys
import unreal

def log_qa(msg):
    unreal.log_warning(f"[WALLA_QA] {msg}")

def run_task26_verification():
    log_qa("================================================================================")
    log_qa("  PROJECT REVOLUTION — TASK 26 MULTI-DIALECT VOICE QA VERIFICATION")
    log_qa("================================================================================")

    editor_asset_lib = unreal.EditorAssetLibrary

    # 1. Verify Core Audio Architecture (SoundClass & Attenuation)
    sc_voice = editor_asset_lib.load_asset("/Game/Audio/SoundClasses/SC_Voice_Punjabi")
    assert sc_voice is not None, "SC_Voice_Punjabi missing!"
    att_voice = editor_asset_lib.load_asset("/Game/Audio/Attenuation/ATT_Voice_Proximity")
    assert att_voice is not None, "ATT_Voice_Proximity missing!"
    log_qa("[PASS] Core Voice SoundClass and Attenuation loaded successfully.")

    # 2. Verify all 8 multi-dialect SoundWave assets
    expected_walla_assets = [
        "SFX_Voice_Majhi_SabziWalla_Bark",
        "SFX_Voice_Majhi_PatrikaHawker_Bark",
        "SFX_Voice_Majhi_ChanaVendor_Bark",
        "SFX_Voice_Majhi_ElderMatron_Bark",
        "SFX_Voice_Doabi_KulfiWalla_Bark",
        "SFX_Voice_Doabi_KumharPotter_Bark",
        "SFX_Voice_Doabi_MandiArhtiya_Bark",
        "SFX_Voice_Doabi_MazdoorPorter_Bark"
    ]

    for vname in expected_walla_assets:
        vpath = f"/Game/Audio/Voice/{vname}"
        sw = editor_asset_lib.load_asset(vpath)
        assert sw is not None, f"Walla voice asset missing: {vpath}!"
        assert sw.get_class().get_name() == "SoundWave", f"Asset {vpath} is not a SoundWave!"

        assigned_sc = sw.get_editor_property("sound_class_object")
        assert assigned_sc is not None and assigned_sc.get_name() == "SC_Voice_Punjabi", \
            f"Asset {vname} has invalid SoundClass: {assigned_sc}!"

        assigned_att = sw.get_editor_property("attenuation_settings")
        assert assigned_att is not None and assigned_att.get_name() == "ATT_Voice_Proximity", \
            f"Asset {vname} has invalid Attenuation: {assigned_att}!"

        log_qa(f"  [VERIFIED SOUNDWAVE] {vname} (SC_Voice_Punjabi, ATT_Voice_Proximity)")

    log_qa(f"[PASS] All {len(expected_walla_assets)} multi-dialect voice SoundWaves verified.")

    # 3. Verify C++ Class & UFUNCTION Reflection
    walla_class = unreal.load_class(None, "/Script/REVOLUTION.RevolutionBazaarWallaActor")
    assert walla_class is not None, "Failed to load ARevolutionBazaarWallaActor class!"
    log_qa("[PASS] ARevolutionBazaarWallaActor class loaded successfully.")

    # 4. Verify Master Level Scene Integration
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    level_sub.load_level(level_path)
    all_actors = actor_sub.get_all_level_actors()
    log_qa(f"Total Level Actors in Scene: {len(all_actors)}")
    assert len(all_actors) >= 209, f"Actor count below expected 209: {len(all_actors)}"

    expected_actors = [
        "BazaarWalla_Majhi_Sabzi",
        "BazaarWalla_Doabi_Kulfi",
        "BazaarWalla_Majhi_Hawker",
        "BazaarWalla_Doabi_Mazdoor"
    ]

    found_actors = {}
    for a in all_actors:
        label = a.get_actor_label()
        if label in expected_actors:
            found_actors[label] = a

    assert len(found_actors) == 4, f"Expected 4 Bazaar Walla actors, found {len(found_actors)}: {list(found_actors.keys())}"

    for label, actor in found_actors.items():
        sound = actor.get_editor_property("primary_walla_sound")
        att = actor.get_editor_property("voice_attenuation")
        assert sound is not None, f"Actor '{label}' has null primary_walla_sound!"
        assert att is not None, f"Actor '{label}' has null voice_attenuation!"

        # Verify UFUNCTION reflection
        assert hasattr(actor, "play_walla_call"), f"Actor '{label}' missing play_walla_call method!"
        assert hasattr(actor, "set_curfew_silenced"), f"Actor '{label}' missing set_curfew_silenced method!"
        assert hasattr(actor, "is_curfew_silenced"), f"Actor '{label}' missing is_curfew_silenced method!"

        # Test curfew silencing behavior
        actor.set_curfew_silenced(True)
        assert actor.is_curfew_silenced() == True, f"Actor '{label}' failed to set curfew silenced!"
        actor.set_curfew_silenced(False)
        assert actor.is_curfew_silenced() == False, f"Actor '{label}' failed to clear curfew silenced!"

        # Test call invocation
        actor.play_walla_call()
        log_qa(f"  [VERIFIED ACTOR] {label}: sound={sound.get_name()}, att={att.get_name()}, functions verified.")

    log_qa("================================================================================")
    log_qa("  TASK 26 MULTI-DIALECT VOICE RESULT: 100% PASS (0 ERRORS)")
    log_qa("================================================================================")
    return True

if __name__ == "__main__":
    success = run_task26_verification()
    if not success:
        sys.exit(1)
    sys.exit(0)
