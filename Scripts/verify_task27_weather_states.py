"""
PROJECT REVOLUTION — Task 27 QA Verification Suite: Dynamic Time-of-Day Weather States
Validates:
1. Both Weather SoundWave Assets exist in /Game/Audio/Weather/ and /Game/Audio/SFX/:
   - SFX_Weather_DustStorm_Wind_Loop (SC_Ambience_Mohalla, Looping=True)
   - SFX_Weather_GoldenHaze_Breeze (SC_Ambience_Mohalla, Looping=True)
2. C++ Class & UFUNCTION Reflection:
   - ARevolutionAtmosphereController exposes:
     - get_current_weather_state
     - get_weather_visibility_multiplier
     - is_weather_sound_masked
     - set_weather_state
     - trigger_dust_storm
3. Weather State Dynamic Modulation & Volumetric Fog:
   - ClearSky: 1.0x visibility multiplier, unmasked sound
   - DustStormAndhi: 0.65x visibility multiplier (35% sentry sight reduction), sound masked
   - GoldenHaze: Soft morning river mist and peaceful breeze
4. Master Level Scene Integration:
   - /Game/Maps/L_Validation_Gym loaded cleanly with 209 level actors
   - AtmosphereController verified and tested through all weather transitions
"""

import sys
import unreal

def log_qa(msg):
    unreal.log_warning(f"[WEATHER_QA] {msg}")

def run_task27_verification():
    log_qa("================================================================================")
    log_qa("  PROJECT REVOLUTION — TASK 27 DYNAMIC WEATHER STATES QA SUITE")
    log_qa("================================================================================")

    editor_asset_lib = unreal.EditorAssetLibrary

    # 1. Verify Audio Assets & Routing
    sc_ambience = editor_asset_lib.load_asset("/Game/Audio/SoundClasses/SC_Ambience_Mohalla")
    assert sc_ambience is not None, "SC_Ambience_Mohalla missing!"
    log_qa("[PASS] SC_Ambience_Mohalla SoundClass verified.")

    expected_weather_assets = [
        "SFX_Weather_DustStorm_Wind_Loop",
        "SFX_Weather_GoldenHaze_Breeze"
    ]

    for wname in expected_weather_assets:
        for folder in ["/Game/Audio/Weather", "/Game/Audio/SFX"]:
            wpath = f"{folder}/{wname}"
            sw = editor_asset_lib.load_asset(wpath)
            assert sw is not None, f"Missing weather SoundWave: {wpath}!"
            assert sw.get_class().get_name() == "SoundWave", f"Asset {wpath} is not a SoundWave!"

            sc = sw.get_editor_property("sound_class_object")
            assert sc is not None and sc.get_name() == "SC_Ambience_Mohalla", \
                f"Asset {wpath} has invalid SoundClass: {sc}!"

            b_loop = sw.get_editor_property("looping")
            assert b_loop == True, f"Asset {wpath} is not marked looping!"
            log_qa(f"  [VERIFIED SOUNDWAVE] {wpath} (SC_Ambience_Mohalla, Looping=True)")

    log_qa("[PASS] All weather audio assets verified and routed.")

    # 2. Verify Master Level & Atmosphere Controller
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    level_sub.load_level(level_path)
    all_actors = actor_sub.get_all_level_actors()
    log_qa(f"Total Level Actors in Scene: {len(all_actors)}")
    assert len(all_actors) >= 209, f"Actor count below 209 threshold: {len(all_actors)}"

    atmo_actor = None
    for a in all_actors:
        if "AtmosphereController" in a.get_class().get_name():
            atmo_actor = a
            break

    assert atmo_actor is not None, "AtmosphereController missing from gym!"
    log_qa(f"[PASS] Atmosphere Controller found in gym: {atmo_actor.get_name()}")

    # 3. Verify C++ Weather Methods & Reflection
    required_methods = [
        "get_current_weather_state",
        "get_weather_visibility_multiplier",
        "is_weather_sound_masked",
        "set_weather_state",
        "trigger_dust_storm"
    ]

    for m in required_methods:
        assert hasattr(atmo_actor, m), f"AtmosphereController missing UFUNCTION '{m}'!"
        log_qa(f"  [UFUNCTION VERIFIED] {m}")

    # 4. Test Weather State Transitions & Gameplay Multipliers
    log_qa("--- Testing Weather State Transitions & Sentry Perception Modifiers ---")

    weather_enum = getattr(unreal, "HistoricalWeatherState", None)
    assert weather_enum is not None, "unreal.HistoricalWeatherState enum missing from reflection!"

    # Test 4.1: ClearSky
    atmo_actor.set_weather_state(weather_enum.CLEAR_SKY, 0.0)
    w_state = atmo_actor.get_current_weather_state()
    v_mult = atmo_actor.get_weather_visibility_multiplier()
    b_mask = atmo_actor.is_weather_sound_masked()
    log_qa(f"  ClearSky State: Weather={w_state.name}, VisMultiplier={v_mult:.2f}, SoundMasked={b_mask}")
    assert abs(v_mult - 1.0) < 0.001, f"Expected 1.0 vis multiplier for ClearSky, got {v_mult}!"
    assert b_mask == False, f"Expected sound masking False for ClearSky, got {b_mask}!"

    # Test 4.2: DustStormAndhi
    atmo_actor.set_weather_state(weather_enum.DUST_STORM_ANDHI, 0.0)
    w_state = atmo_actor.get_current_weather_state()
    v_mult = atmo_actor.get_weather_visibility_multiplier()
    b_mask = atmo_actor.is_weather_sound_masked()
    log_qa(f"  DustStormAndhi State: Weather={w_state.name}, VisMultiplier={v_mult:.2f}, SoundMasked={b_mask}")
    assert abs(v_mult - 0.65) < 0.001, f"Expected 0.65 vis multiplier for DustStorm, got {v_mult}!"
    assert b_mask == True, f"Expected sound masking True for DustStorm, got {b_mask}!"

    # Test 4.3: TriggerDustStorm method
    atmo_actor.trigger_dust_storm(10.0)
    assert atmo_actor.get_current_weather_state() == weather_enum.DUST_STORM_ANDHI, "TriggerDustStorm failed to set DustStormAndhi!"
    log_qa("[PASS] TriggerDustStorm(10.0) successfully executed.")

    # Test 4.4: Restore GoldenHaze
    atmo_actor.set_weather_state(weather_enum.GOLDEN_HAZE, 0.0)
    w_state = atmo_actor.get_current_weather_state()
    v_mult = atmo_actor.get_weather_visibility_multiplier()
    b_mask = atmo_actor.is_weather_sound_masked()
    log_qa(f"  GoldenHaze State: Weather={w_state.name}, VisMultiplier={v_mult:.2f}, SoundMasked={b_mask}")
    assert abs(v_mult - 1.0) < 0.001, f"Expected 1.0 vis multiplier for GoldenHaze, got {v_mult}!"
    assert b_mask == False, f"Expected sound masking False for GoldenHaze, got {b_mask}!"

    # 5. Verify Volumetric Fog Properties on HeightFogActor in gym
    fog_actor = next((a for a in all_actors if "ExponentialHeightFog" in a.get_class().get_name()), None)
    assert fog_actor is not None, "Level missing ExponentialHeightFog actor!"
    fog_comp = fog_actor.get_component_by_class(unreal.ExponentialHeightFogComponent)
    assert fog_comp is not None, "HeightFogComponent missing from fog actor!"
    b_vol_fog = fog_comp.get_editor_property("enable_volumetric_fog")
    log_qa(f"[PASS] HeightFogComponent verified with VolumetricFog={b_vol_fog}")

    log_qa("================================================================================")
    log_qa("  TASK 27 DYNAMIC WEATHER STATES RESULT: 100% PASS (0 ERRORS)")
    log_qa("================================================================================")
    return True

if __name__ == "__main__":
    success = run_task27_verification()
    if not success:
        sys.exit(1)
    sys.exit(0)
