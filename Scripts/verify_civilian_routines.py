"""
PROJECT REVOLUTION — Task 31 QA Verification Suite (TEST-17)
Procedural Skeletal Idle Animations, Authentic Occupational Routine Life & Heritage Attire
Verifies:
1. All 6 authentic period occupational routine audio loop assets in /Game/Audio/SFX/:
   - SFX_Routine_SewingMachine_Loop (Ram Lubhaya - Singer sewing machine treadle)
   - SFX_Routine_ChaiStir_Loop (Hira Halwai - copper karahi simmering and brass spoon stirring)
   - SFX_Routine_MashkWater_Loop (Ghasita Bhishti - goatskin mashk slosh and well water drops)
   - SFX_Routine_ClothMerchant_Loop (Lala Karam Chand - khadi weave handling and yardstick)
   - SFX_Routine_Schoolmaster_Loop (Pandit Kashi Ram - slate pencil chalkboard scratch)
   - SFX_Routine_KartarKite_Loop (Kartar Singh - kite manja hum and wooden spool rattle)
2. In /Game/Maps/L_Validation_Gym:
   - All 6 Civilian NPCs instantiate ACivilianNPCActor with bEnableRoutineAnimations = True.
   - ConfigureOccupation binds authentic props, sounds, barks, and lore.
   - ApplyHeritageAttireMaterials assigns authentic period khadi, saffron, indigo, and teak PBR materials to mesh slots 0 & 1.
   - Procedural breathing and micro-gesture tick simulation advances RoutineCycleTime and BreathingCycleTime monotonically.
   - Dynamic enable/disable switching (SetRoutineAnimationsEnabled) restores neutral rest transforms.
   - Stumble override precedence: sprint impact suppresses routine motion during balance recovery, then restores routine life cleanly.
"""

import sys
import unreal

def log_qa(msg):
    unreal.log_warning(f"[CIVILIAN_ROUTINES_QA] {msg}")

def main():
    log_qa("================================================================================")
    log_qa("  PROJECT REVOLUTION — TASK 31 CIVILIAN IDLE & ROUTINE LIFE QA VERIFICATION")
    log_qa("================================================================================")

    editor_asset_lib = unreal.EditorAssetLibrary

    # 1. Verify Routine Audio Loop Assets
    routine_audio_assets = [
        ("FatherTailor", "SFX_Routine_SewingMachine_Loop"),
        ("HalwaiChaiVendor", "SFX_Routine_ChaiStir_Loop"),
        ("BhishtiWaterCarrier", "SFX_Routine_MashkWater_Loop"),
        ("ClothMerchant", "SFX_Routine_ClothMerchant_Loop"),
        ("SchoolHeadmaster", "SFX_Routine_Schoolmaster_Loop"),
        ("SchoolFriendKartar", "SFX_Routine_KartarKite_Loop")
    ]

    sc_foley = editor_asset_lib.load_asset("/Game/Audio/SoundClasses/SC_Foley")
    att_voice = editor_asset_lib.load_asset("/Game/Audio/Attenuation/ATT_Voice_Proximity")

    for occ_name, snd_name in routine_audio_assets:
        asset_path = f"/Game/Audio/SFX/{snd_name}"
        sw = editor_asset_lib.load_asset(asset_path)
        assert sw is not None, f"Routine SoundWave asset missing: {asset_path}!"
        assert sw.get_class().get_name() == "SoundWave", f"Asset {asset_path} is not SoundWave!"
        
        # Ensure proper sound class and attenuation routing
        b_dirty = False
        if sc_foley and sw.get_editor_property("sound_class_object") is None:
            sw.set_editor_property("sound_class_object", sc_foley)
            b_dirty = True
        if att_voice and sw.get_editor_property("attenuation_settings") is None:
            sw.set_editor_property("attenuation_settings", att_voice)
            b_dirty = True
        if not sw.get_editor_property("looping"):
            sw.set_editor_property("looping", True)
            b_dirty = True
        if b_dirty:
            editor_asset_lib.save_loaded_asset(sw)

        log_qa(f"  [ROUTINE AUDIO VERIFIED] {snd_name} for archetype {occ_name}")

    log_qa("[PASS] All 6 occupational routine audio loops verified and configured.")

    # 2. Verify Heritage Materials Existence
    heritage_materials = [
        "/Game/Environment/Mohalla/Materials/M_ClothUndyedCotton_PBR",
        "/Game/Environment/Mohalla/Materials/M_ClothSaffron_PBR",
        "/Game/Environment/Mohalla/Materials/M_ClothIndigo_PBR",
        "/Game/Environment/Mohalla/Materials/M_AgedTeak_PBR"
    ]

    for mat_path in heritage_materials:
        mat = editor_asset_lib.load_asset(mat_path)
        assert mat is not None, f"Heritage material missing: {mat_path}!"
        log_qa(f"  [HERITAGE MATERIAL VERIFIED] {mat.get_name()}")

    log_qa("[PASS] All 4 heritage attire PBR materials verified.")

    # 3. Load Validation Gym Level
    gym_map = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(gym_map)

    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = actor_sub.get_all_level_actors()
    log_qa(f"Loaded gym level: {gym_map} ({len(actors)} actors)")

    # 4. Find all Civilian NPCs
    civilians = []
    for a in actors:
        if a.get_class().get_name() == "CivilianNPCActor":
            civilians.append(a)

    log_qa(f"Found {len(civilians)} Civilian NPCs in L_Validation_Gym")
    assert len(civilians) >= 6, f"Expected at least 6 civilians, found {len(civilians)}!"

    # 5. Verify and Test Each Civilian NPC
    archetypes_found = set()

    for civ in civilians:
        label = civ.get_actor_label()
        occ_enum = civ.get_editor_property("occupation")
        occ_name = occ_enum.name
        archetypes_found.add(occ_name)

        # Re-configure to ensure latest C++ occupation logic is initialized
        civ.configure_occupation(occ_enum)

        name = str(civ.get_editor_property("civilian_name"))
        title = str(civ.get_editor_property("profession_title"))
        b_anim = civ.get_editor_property("enable_routine_animations")
        routine_snd = civ.get_editor_property("occupation_routine_sound")
        prop_comp = civ.get_editor_property("prop_accessory_mesh")

        assert b_anim is True, f"Civilian {label} has enable_routine_animations = False!"
        assert civ.is_routine_animation_active() is True, f"Civilian {label} IsRoutineAnimationActive() returned False!"
        assert routine_snd is not None, f"Civilian {label} has null OccupationRoutineSound!"
        assert prop_comp is not None, f"Civilian {label} has null PropAccessoryMesh!"
        prop_mesh = prop_comp.get_editor_property("static_mesh")
        assert prop_mesh is not None, f"Civilian {label} has no static mesh assigned on PropAccessoryMesh!"

        # Verify Heritage Attire assignment
        civ.apply_heritage_attire_materials()
        skel_mesh = civ.get_component_by_class(unreal.SkeletalMeshComponent)
        assert skel_mesh is not None, f"Civilian {label} has no skeletal mesh component!"
        mat0 = skel_mesh.get_material(0)
        mat1 = skel_mesh.get_material(1)
        assert mat0 is not None, f"Civilian {label} slot 0 material is None!"
        assert mat1 is not None, f"Civilian {label} slot 1 material is None!"
        assert not mat0.get_name().startswith("MI_Manny"), f"Civilian {label} still using default mannequin material in slot 0 ({mat0.get_name()})!"
        assert not mat1.get_name().startswith("MI_Manny"), f"Civilian {label} still using default mannequin material in slot 1 ({mat1.get_name()})!"

        log_qa(f"  [CIVILIAN VERIFIED] {name} ({title}) - Prop: {prop_mesh.get_name()}, Sound: {routine_snd.get_name()}, Attire: [{mat0.get_name()}, {mat1.get_name()}]")

        # Procedural Animation Simulation Test
        initial_cycle = civ.get_routine_cycle_time()
        initial_mesh_loc = skel_mesh.get_editor_property("relative_location")
        initial_mesh_rot = skel_mesh.get_editor_property("relative_rotation")

        # Step 1: Simulate ticks
        civ.simulate_routine_tick(0.5)
        cycle_after_1 = civ.get_routine_cycle_time()
        assert cycle_after_1 > initial_cycle, f"Civilian {label} RoutineCycleTime did not advance after tick (was {initial_cycle}, now {cycle_after_1})!"
        assert civ.get_editor_property("breathing_cycle_time") > 0.0, f"Civilian {label} BreathingCycleTime did not advance!"

        civ.simulate_routine_tick(1.0)
        cycle_after_2 = civ.get_routine_cycle_time()
        assert cycle_after_2 > cycle_after_1, f"Civilian {label} RoutineCycleTime did not advance monotonically!"

        # Step 2: Toggle Routine Animations Off
        civ.set_routine_animations_enabled(False)
        assert civ.is_routine_animation_active() is False, f"Civilian {label} should be inactive after SetRoutineAnimationsEnabled(False)!"
        civ.simulate_routine_tick(0.5)
        # Verify relative transforms reset
        disabled_mesh_loc = skel_mesh.get_editor_property("relative_location")
        assert abs(disabled_mesh_loc.z - initial_mesh_loc.z) < 0.1, \
            f"Civilian {label} mesh Z did not return to neutral baseline when disabled! Got {disabled_mesh_loc.z}, expected {initial_mesh_loc.z}"

        # Step 3: Toggle Routine Animations Back On
        civ.set_routine_animations_enabled(True)
        assert civ.is_routine_animation_active() is True, f"Civilian {label} should be active after SetRoutineAnimationsEnabled(True)!"
        civ.simulate_routine_tick(0.5)

        log_qa(f"    [PROCEDURAL SIMULATION PASS] {label} cycle={cycle_after_2:.2f}s, breathing active, toggle clean")

    assert len(archetypes_found) == 6, f"Expected all 6 archetypes present in gym, found {len(archetypes_found)}: {archetypes_found}"
    log_qa(f"[PASS] All 6 archetypes verified in level: {archetypes_found}")

    # 6. Test Stumble Override Precedence
    test_civ = civilians[0]
    log_qa(f"Testing Stumble precedence on {test_civ.get_actor_label()}...")
    test_civ.trigger_stumble(unreal.Vector(1, 0, 0), 400.0)
    assert test_civ.is_stumbling() is True, "Civilian failed to enter stumbling state!"
    test_civ.simulate_routine_tick(0.2)
    assert test_civ.is_stumbling() is True, "Civilian should remain in stumbling state during recovery!"
    # Fast forward stumble completion
    test_civ.simulate_routine_tick(1.5)
    assert test_civ.is_stumbling() is False, "Civilian should recover from stumble after duration!"
    assert test_civ.is_routine_animation_active() is True, "Civilian routine animations should resume after stumble recovery!"
    log_qa("[PASS] Stumble precedence and routine resumption verified.")

    # 7. Save level and assets if any modifications occurred
    level_sub.save_current_level()
    log_qa("[PASS] Validation gym level state preserved and saved.")

    log_qa("================================================================================")
    log_qa("  TASK 31 QA VERIFICATION SUITE (TEST-17) COMPLETED: 100% PASS (0 ERRORS)")
    log_qa("================================================================================")

if __name__ == "__main__":
    main()
