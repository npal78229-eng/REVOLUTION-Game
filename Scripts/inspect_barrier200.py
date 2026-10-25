import unreal

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Maps/L_Validation_Gym")
actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

for a in actor_sub.get_all_level_actors():
    if a.get_actor_label() == "Boundary_Barrier_NorthGate_West":
        unreal.log_warning(f"Label: {a.get_actor_label()} ({a.get_name()})")
        unreal.log_warning(f"  Location: {a.get_actor_location()}")
        unreal.log_warning(f"  Scale: {a.get_actor_scale3d()}")
        unreal.log_warning(f"  Rotation: {a.get_actor_rotation()}")
        smc = a.get_component_by_class(unreal.StaticMeshComponent)
        if smc:
            unreal.log_warning(f"  StaticMesh: {smc.get_editor_property('static_mesh')}")
            unreal.log_warning(f"  Bounds: {a.get_actor_bounds(False)}")
