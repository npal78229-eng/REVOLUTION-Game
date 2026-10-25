import unreal

def inspect():
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)
    
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = actor_sub.get_all_level_actors()
    
    gurdial = next((a for a in actors if a.get_actor_label() == "NPC_Constable_Gurdial"), None)
    if gurdial:
        wps = gurdial.get_editor_property("patrol_waypoints")
        unreal.log_warning(f"Gurdial loc={gurdial.get_actor_location()}")
        for i, wp in enumerate(wps):
            unreal.log_warning(f"  WP[{i}]: {wp}")
            
    canopy = next((a for a in actors if a.get_actor_label() == "Bazaar_Canopy_Khadi_SouthEast"), None)
    if canopy:
        comp = canopy.get_component_by_class(unreal.StaticMeshComponent)
        sm = comp.get_editor_property("static_mesh")
        unreal.log_warning(f"Canopy actor: loc={canopy.get_actor_location()}, rot={canopy.get_actor_rotation()}, scale={canopy.get_actor_scale3d()}")
        unreal.log_warning(f"Canopy collision profile: {comp.get_collision_profile_name()}")
        unreal.log_warning(f"Canopy bounds: {canopy.get_actor_bounds(False)}")
        unreal.log_warning(f"Static mesh: {sm.get_path_name() if sm else 'None'}")

if __name__ == "__main__":
    inspect()
