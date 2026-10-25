import unreal

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Maps/L_Validation_Gym")
actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

for a in actor_sub.get_all_level_actors():
    lbl = a.get_actor_label()
    if lbl in ["Boundary_Barrier_NorthGate_West", "Boundary_Barrier_NorthGate_East"]:
        old_scale = a.get_actor_scale3d()
        a.set_actor_scale3d(unreal.Vector(0.01, 0.01, 0.01))
        bounds = a.get_actor_bounds(False)
        unreal.log_warning(f"Updated {lbl}: Scale {old_scale} -> (0.01, 0.01, 0.01)")
        unreal.log_warning(f"  New Bounds: Origin={bounds[0]}, Extent={bounds[1]}")

unreal.EditorLoadingAndSavingUtils.save_dirty_packages(False, True)
unreal.EditorAssetLibrary.save_directory("/Game/Maps", only_if_is_dirty=False, recursive=True)
unreal.log_warning("L_Validation_Gym saved successfully with corrected barrier scales.")
