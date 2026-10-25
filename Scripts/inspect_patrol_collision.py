import unreal

def inspect():
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)
    
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = actor_sub.get_all_level_actors()
    
    constable = None
    target_sma = None
    for a in actors:
        lbl = a.get_actor_label()
        if lbl == "NPC_Constable_Gurdial" or "CurfewPatrol" in a.get_name():
            constable = a
        if a.get_name() == "StaticMeshActor_128" or lbl == "StaticMeshActor_128":
            target_sma = a
            
    if constable:
        loc = constable.get_actor_location()
        wps = constable.get_editor_property("patrol_waypoints")
        unreal.log_warning(f"Constable found: {constable.get_name()} ({constable.get_actor_label()}) at {loc}")
        unreal.log_warning(f"Waypoints ({len(wps)}):")
        for i, wp in enumerate(wps):
            unreal.log_warning(f"  WP[{i}]: {wp}")
    else:
        unreal.log_warning("Constable NOT found!")
        
    for a in actors:
        loc = a.get_actor_location()
        # Look for actors near 107.46, 1750.62, 125.0
        if abs(loc.x - 107.46) < 150.0 and abs(loc.y - 1750.62) < 150.0:
            comp = a.get_component_by_class(unreal.StaticMeshComponent)
            sm = comp.get_editor_property("static_mesh") if comp else None
            sm_name = sm.get_name() if sm else "None"
            col_prof = comp.get_collision_profile_name() if comp else "None"
            unreal.log_warning(f"Nearby Actor: {a.get_name()} (label: {a.get_actor_label()}), Class={a.get_class().get_name()} at {loc}, Mesh={sm_name}, Collision={col_prof}")

if __name__ == "__main__":
    inspect()
