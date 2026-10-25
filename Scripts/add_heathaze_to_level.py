import unreal

def add_heathaze_to_level():
    unreal.log_warning("=== Adding RDR2 Heat Haze Shimmer to L_Validation_Gym ===")
    
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)
    
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = actor_sub.get_all_level_actors()
    
    # Remove existing heat haze card if any
    for a in actors:
        if a.get_actor_label() == "HeatHaze_Chulha":
            actor_sub.destroy_actor(a)
            break
            
    # Spawn Heat Haze Plane at Chulha base (Z=100)
    haze_actor = actor_sub.spawn_actor_from_class(
        unreal.StaticMeshActor,
        unreal.Vector(180.0, 620.0, 100.0)
    )
    if haze_actor:
        haze_actor.set_actor_label("HeatHaze_Chulha")
        plane_mesh = unreal.load_asset("/Engine/BasicShapes/Plane.Plane")
        haze_mat = unreal.load_asset("/Game/VFX/Smoke/Materials/M_RDR2_HeatHaze")
        if plane_mesh:
            haze_actor.static_mesh_component.set_static_mesh(plane_mesh)
            haze_actor.static_mesh_component.set_world_scale3d(unreal.Vector(0.7, 0.7, 1.0))
            haze_actor.set_actor_rotation(unreal.Rotator(90.0, 0.0, 45.0), True)
            haze_actor.static_mesh_component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
        if haze_mat:
            haze_actor.static_mesh_component.set_material(0, haze_mat)
        unreal.log_warning("Spawned HeatHaze_Chulha with M_RDR2_HeatHaze successfully!")
        
    level_sub.save_current_level()
    unreal.log_warning("L_Validation_Gym saved with HeatHaze_Chulha!")

if __name__ == "__main__":
    add_heathaze_to_level()
