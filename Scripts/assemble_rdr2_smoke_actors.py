import unreal

def setup_smoke_in_level():
    unreal.log_warning("=== Assembling RDR2-Inspired Smoke Actors into L_Validation_Gym ===")
    
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)
    
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    all_actors = actor_sub.get_all_level_actors()
    
    # Check if smoke actors already exist
    existing_chulha = [a for a in all_actors if "Chulha_Fireplace" in a.get_actor_label()]
    if existing_chulha:
        unreal.log_warning("Chulha_Fireplace already exists in level. Updating...")
        for a in existing_chulha:
            actor_sub.destroy_actor(a)
            
    existing_chimney = [a for a in all_actors if "Haveli_Chimney" in a.get_actor_label()]
    if existing_chimney:
        unreal.log_warning("Haveli_Chimney already exists in level. Updating...")
        for a in existing_chimney:
            actor_sub.destroy_actor(a)

    # 1. Spawn Courtyard Chulha / Hearth (near the kitchen/alcove at X=200, Y=650, Z=50)
    chulha_loc = unreal.Vector(180.0, 620.0, 50.0)
    chulha_actor = actor_sub.spawn_actor_from_class(unreal.StaticMeshActor, chulha_loc)
    if chulha_actor:
        chulha_actor.set_actor_label("BP_Chulha_Fireplace_RDR2")
        # Load a nice prop or cylinder/cube mesh for the clay chulha
        cube_mesh = unreal.load_asset("/Engine/BasicShapes/Cylinder.Cylinder")
        if cube_mesh:
            chulha_actor.static_mesh_component.set_static_mesh(cube_mesh)
            chulha_actor.static_mesh_component.set_world_scale3d(unreal.Vector(0.8, 0.8, 0.35))
            # Assign khadi/clay/leather material or default
            clay_mat = unreal.load_asset("/Game/Characters/Kabir_v05/M_Kabir_Leather_PBR")
            if clay_mat:
                chulha_actor.static_mesh_component.set_material(0, clay_mat)
        
        # Add Point Light for warm flame bounce (RDR2 ptxu_Light equivalent)
        light_actor = actor_sub.spawn_actor_from_class(unreal.PointLight, unreal.Vector(180.0, 620.0, 95.0))
        if light_actor:
            light_actor.set_actor_label("Light_Chulha_Flame_Bounce")
            comp = light_actor.point_light_component
            comp.set_intensity(2800.0)
            comp.set_attenuation_radius(450.0)
            comp.set_light_color(unreal.LinearColor(1.0, 0.42, 0.10, 1.0))
            comp.set_cast_shadows(True)
            unreal.log_warning("Spawned Light_Chulha_Flame_Bounce successfully!")
            
        # Spawn StaticMesh plane/billow card for continuous smoke plume
        smoke_card = actor_sub.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(180.0, 620.0, 160.0))
        if smoke_card:
            smoke_card.set_actor_label("Smoke_Plume_Chulha")
            plane_mesh = unreal.load_asset("/Engine/BasicShapes/Plane.Plane")
            smoke_mat = unreal.load_asset("/Game/VFX/Smoke/Materials/MI_Smoke_Chulha_Campfire")
            if plane_mesh:
                smoke_card.static_mesh_component.set_static_mesh(plane_mesh)
                smoke_card.static_mesh_component.set_world_scale3d(unreal.Vector(1.4, 1.4, 2.2))
                smoke_card.set_actor_rotation(unreal.Rotator(90.0, 0.0, 45.0), True)
                smoke_card.static_mesh_component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
            if smoke_mat:
                smoke_card.static_mesh_component.set_material(0, smoke_mat)
            unreal.log_warning("Spawned Smoke_Plume_Chulha with MI_Smoke_Chulha_Campfire!")

    # 2. Spawn Rooftop Chimney Plume (on 1F terrace at X=50, Y=1450, Z=420)
    chimney_loc = unreal.Vector(60.0, 1420.0, 420.0)
    chimney_actor = actor_sub.spawn_actor_from_class(unreal.StaticMeshActor, chimney_loc)
    if chimney_actor:
        chimney_actor.set_actor_label("BP_Haveli_Rooftop_Chimney_RDR2")
        cyl_mesh = unreal.load_asset("/Engine/BasicShapes/Cylinder.Cylinder")
        if cyl_mesh:
            chimney_actor.static_mesh_component.set_static_mesh(cyl_mesh)
            chimney_actor.static_mesh_component.set_world_scale3d(unreal.Vector(0.5, 0.5, 1.2))
            brick_mat = unreal.load_asset("/Game/Characters/Kabir_v05/M_Kabir_Khadi_PBR")
            if brick_mat:
                chimney_actor.static_mesh_component.set_material(0, brick_mat)
                
        # Chimney smoke plume card (tall billowing column)
        chimney_smoke = actor_sub.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(60.0, 1420.0, 560.0))
        if chimney_smoke:
            chimney_smoke.set_actor_label("Smoke_Plume_Rooftop_Chimney")
            plane_mesh = unreal.load_asset("/Engine/BasicShapes/Plane.Plane")
            smoke_mat = unreal.load_asset("/Game/VFX/Smoke/Materials/MI_Smoke_Haveli_Chimney")
            if plane_mesh:
                chimney_smoke.static_mesh_component.set_static_mesh(plane_mesh)
                chimney_smoke.static_mesh_component.set_world_scale3d(unreal.Vector(2.0, 2.0, 3.5))
                chimney_smoke.set_actor_rotation(unreal.Rotator(90.0, 0.0, 30.0), True)
                chimney_smoke.static_mesh_component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
            if smoke_mat:
                chimney_smoke.static_mesh_component.set_material(0, smoke_mat)
            unreal.log_warning("Spawned Smoke_Plume_Rooftop_Chimney with MI_Smoke_Haveli_Chimney!")

    level_sub.save_current_level()
    unreal.log_warning("L_Validation_Gym successfully saved with RDR2 smoke actors!")

if __name__ == "__main__":
    setup_smoke_in_level()
