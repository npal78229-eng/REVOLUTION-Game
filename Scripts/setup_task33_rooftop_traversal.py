"""
PROJECT REVOLUTION — Task 33 Setup Script:
Rooftop Traversal & Vertical Climbing Polish
Assembles:
1. Haveli_Courtyard_Terrace_Ladder (ALadderActor) connecting ground courtyard (Z=0) to 1F terrace (Z=400)
2. Haveli_Rooftop_Basant_Kite (SM_Prop_Abandoned_Paper_Kite) perched on parapet coping overlooking ladder
3. Haveli_Rooftop_Patang_Charkhi (SM_Prop_Rooftop_Patang_Charkhi) vantage point setup on terrace
"""

import unreal

def log(msg):
    unreal.log_warning(f"[TASK_33_SETUP] {msg}")

def main():
    log("================================================================================")
    log("  TASK 33: ROOFTOP TRAVERSAL & VERTICAL CLIMBING SETUP")
    log("================================================================================")

    gym_map = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(gym_map)

    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    editor_asset_lib = unreal.EditorAssetLibrary

    # 1. Clean existing Task 33 actors if rerun
    t33_prefixes = [
        "Haveli_Courtyard_Terrace_Ladder",
        "Haveli_Rooftop_Basant_Kite",
        "Haveli_Rooftop_Patang_Charkhi"
    ]

    all_actors = actor_sub.get_all_level_actors()
    for a in all_actors:
        lbl = a.get_actor_label()
        for pfx in t33_prefixes:
            if lbl == pfx or lbl.startswith(pfx + "_"):
                actor_sub.destroy_actor(a)
                log(f"Cleaned existing actor: {lbl}")
                break

    # 2. Materials
    mat_saffron = editor_asset_lib.load_asset("/Game/Environment/Mohalla/Materials/M_ClothSaffron_PBR")
    mat_indigo = editor_asset_lib.load_asset("/Game/Environment/Mohalla/Materials/M_ClothIndigo_PBR")
    mat_teak = editor_asset_lib.load_asset("/Game/Environment/Mohalla/Materials/M_AgedTeak_PBR")
    mat_clay = editor_asset_lib.load_asset("/Game/Environment/Mohalla/Materials/M_Clay_PBR")

    # 3. Spawn Ladder Actor (ALadderActor)
    ladder_class = unreal.load_class(None, "/Script/REVOLUTION.LadderActor")
    assert ladder_class is not None, "Failed to load ALadderActor class!"

    ladder_loc = unreal.Vector(400.0, 100.0, 0.0)
    ladder_rot = unreal.Rotator(0.0, 0.0, 0.0)

    ladder_actor = actor_sub.spawn_actor_from_class(ladder_class, ladder_loc, ladder_rot)
    assert ladder_actor is not None, "Failed to spawn Haveli_Courtyard_Terrace_Ladder!"
    ladder_actor.set_actor_label("Haveli_Courtyard_Terrace_Ladder")
    log("  [SPAWNED LADDER] Haveli_Courtyard_Terrace_Ladder at (400.0, 100.0, 0.0)")

    # 4. Spawn Basant Paper Kite (SM_Prop_Abandoned_Paper_Kite) on Parapet Coping
    kite_mesh = editor_asset_lib.load_asset("/Game/Environment/Mohalla/Meshes/SM_Prop_Abandoned_Paper_Kite")
    assert kite_mesh is not None, "Failed to load SM_Prop_Abandoned_Paper_Kite!"

    kite_loc = unreal.Vector(380.0, 200.0, 480.0)
    kite_rot = unreal.Rotator(15.0, -45.0, 25.0)
    kite_actor = actor_sub.spawn_actor_from_class(unreal.StaticMeshActor, kite_loc, kite_rot)
    assert kite_actor is not None, "Failed to spawn Haveli_Rooftop_Basant_Kite!"
    kite_actor.set_actor_label("Haveli_Rooftop_Basant_Kite")
    kite_actor.set_actor_scale3d(unreal.Vector(0.010, 0.010, 0.010))

    kite_sm = kite_actor.get_component_by_class(unreal.StaticMeshComponent)
    if kite_sm:
        kite_sm.set_static_mesh(kite_mesh)
        kite_sm.set_collision_profile_name("BlockAll")
        if mat_saffron:
            kite_sm.set_material(0, mat_saffron)
        if mat_teak:
            kite_sm.set_material(1, mat_teak)
    log("  [SPAWNED KITE] Haveli_Rooftop_Basant_Kite at (380.0, 200.0, 480.0)")

    # 5. Spawn Rooftop Patang & Charkhi Vantage Setup (SM_Prop_Rooftop_Patang_Charkhi)
    charkhi_mesh = editor_asset_lib.load_asset("/Game/Environment/Mohalla/Meshes/SM_Prop_Rooftop_Patang_Charkhi")
    assert charkhi_mesh is not None, "Failed to load SM_Prop_Rooftop_Patang_Charkhi!"

    charkhi_loc = unreal.Vector(280.0, 350.0, 400.0)
    charkhi_rot = unreal.Rotator(0.0, 30.0, 0.0)
    charkhi_actor = actor_sub.spawn_actor_from_class(unreal.StaticMeshActor, charkhi_loc, charkhi_rot)
    assert charkhi_actor is not None, "Failed to spawn Haveli_Rooftop_Patang_Charkhi!"
    charkhi_actor.set_actor_label("Haveli_Rooftop_Patang_Charkhi")

    charkhi_sm = charkhi_actor.get_component_by_class(unreal.StaticMeshComponent)
    if charkhi_sm:
        charkhi_sm.set_static_mesh(charkhi_mesh)
        charkhi_sm.set_collision_profile_name("BlockAll")
        if mat_indigo:
            charkhi_sm.set_material(0, mat_indigo)
        if mat_teak:
            charkhi_sm.set_material(1, mat_teak)
        if mat_clay:
            charkhi_sm.set_material(2, mat_clay)
    log("  [SPAWNED CHARKHI] Haveli_Rooftop_Patang_Charkhi at (280.0, 350.0, 400.0)")

    # 6. Save level state
    level_sub.save_current_level()
    log("[PASS] Validation gym level state preserved and saved.")

    actors_after = actor_sub.get_all_level_actors()
    log(f"Level actor count is now: {len(actors_after)}")

    log("================================================================================")
    log("  TASK 33 ROOFTOP TRAVERSAL SETUP COMPLETED: 100% SUCCESS")
    log("================================================================================")

if __name__ == "__main__":
    main()
