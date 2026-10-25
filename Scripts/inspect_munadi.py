import unreal

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Maps/L_Validation_Gym")
actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = actor_sub.get_all_level_actors()

munadi = next((a for a in actors if a.get_name() == "CivilianNPCActor_6" or a.get_actor_label() == "NPC_Munadi_TownCrier"), None)
if munadi:
    loc = munadi.get_actor_location()
    rot = munadi.get_actor_rotation()
    scale = munadi.get_actor_scale3d()
    capsule = munadi.get_component_by_class(unreal.CapsuleComponent)
    r = capsule.get_scaled_capsule_radius() if capsule else "None"
    h = capsule.get_scaled_capsule_half_height() if capsule else "None"
    un_r = capsule.get_unscaled_capsule_radius() if capsule else "None"
    un_h = capsule.get_unscaled_capsule_half_height() if capsule else "None"
    col_prof = capsule.get_collision_profile_name() if capsule else "None"
    unreal.log_warning(f"NPC_Munadi_TownCrier: Loc={loc}, Rot={rot}, Scale={scale}, CapsuleProfile={col_prof}")
    unreal.log_warning(f"  Scaled Capsule: r={r}, h={h} | Unscaled Capsule: r={un_r}, h={un_h}")
    # Also check other Civilian NPCs
    for a in actors:
        if isinstance(a, unreal.CivilianNPCActor) or "CivilianNPC" in a.get_class().get_name():
            c = a.get_component_by_class(unreal.CapsuleComponent)
            cr = c.get_scaled_capsule_radius() if c else -1
            ch = c.get_scaled_capsule_half_height() if c else -1
            unreal.log_warning(f"  Civilian: '{a.get_actor_label()}' ({a.get_name()}) Loc={a.get_actor_location()} Scale={a.get_actor_scale3d()} Capsule: r={cr}, h={ch}")

