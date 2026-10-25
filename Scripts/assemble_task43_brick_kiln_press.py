import unreal

def assemble_task43_brick_kiln_press():
    unreal.log_warning("=== REVOLUTION: Assembling Task 43 Act IV Bhatta Brick Kiln Climax Scene ===")
    
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)
    
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    
    # 1. Load Meshes & Materials
    mesh_kiln = unreal.load_asset("/Game/Environment/Mohalla/Meshes/SM_Brick_Kiln_Chimney_Bhatta")
    mesh_cache = unreal.load_asset("/Game/Environment/Mohalla/Meshes/SM_Prop_Clandestine_Safehouse_Crate_Cache")
    mesh_cylinder = unreal.load_asset("/Engine/BasicShapes/Cylinder")
    mesh_lantern = unreal.load_asset("/Game/Environment/Mohalla/Meshes/SM_Prop_HurricaneLantern")
    mesh_cloth_rolls = unreal.load_asset("/Game/Environment/Mohalla/Meshes/SM_Prop_ClothRolls_Manchester")
    
    mat_chimney_smoke = unreal.load_asset("/Game/VFX/Smoke/Materials/MI_Smoke_Haveli_Chimney")
    mat_khadi = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_ClothUndyedCotton_PBR")
    mat_brass = unreal.load_asset("/Game/Environment/Mohalla/Materials/MI_HammeredBrass_Photogrammetry")
    
    existing_actors = {a.get_actor_label(): a for a in actor_sub.get_all_level_actors()}
    
    # Helper for StaticMeshActor
    def spawn_or_update_mesh(label, mesh, loc, rot=unreal.Rotator(0,0,0), scale=unreal.Vector(1,1,1), mat=None):
        if label in existing_actors:
            act = existing_actors[label]
            act.set_actor_location(loc, False, True)
            act.set_actor_rotation(rot, True)
            act.set_actor_scale3d(scale)
            unreal.log_warning(f"Updated existing actor: {label}")
        else:
            act = actor_sub.spawn_actor_from_class(unreal.StaticMeshActor, loc, rot)
            act.set_actor_label(label)
            act.set_actor_scale3d(scale)
            existing_actors[label] = act
            unreal.log_warning(f"Spawned new mesh actor: {label}")
            
        sm_comp = act.get_component_by_class(unreal.StaticMeshComponent)
        if sm_comp and mesh:
            sm_comp.set_static_mesh(mesh)
            if mat:
                sm_comp.set_material(0, mat)
        return act

    # Helper for PointLight
    def spawn_or_update_point_light(label, loc, color, intensity, radius):
        if label in existing_actors:
            act = existing_actors[label]
            act.set_actor_location(loc, False, True)
            unreal.log_warning(f"Updated point light: {label}")
        else:
            act = actor_sub.spawn_actor_from_class(unreal.PointLight, loc, unreal.Rotator(0,0,0))
            act.set_actor_label(label)
            existing_actors[label] = act
            unreal.log_warning(f"Spawned point light: {label}")
            
        light_comp = act.get_component_by_class(unreal.PointLightComponent)
        if light_comp:
            light_comp.set_editor_property("light_color", color)
            light_comp.set_editor_property("intensity", intensity)
            light_comp.set_editor_property("attenuation_radius", radius)
            light_comp.set_editor_property("cast_shadows", True)
        return act

    # 2. Bull's Trench Brick Kiln Conical Chimney at (-1250, 2650, 0)
    spawn_or_update_mesh(
        "Industrial_Brick_Kiln_Bhatta_Chimney",
        mesh_kiln,
        unreal.Vector(-1250.0, 2650.0, 0.0),
        unreal.Rotator(0.0, 0.0, 0.0),
        unreal.Vector(1.0, 1.0, 1.0)
    )

    # 3. RDR2-Inspired Brick Kiln Industrial Smoke Plume at top of chimney (Z = 750)
    spawn_or_update_mesh(
        "Smoke_Plume_Bhatta_Kiln",
        mesh_cylinder,
        unreal.Vector(-1250.0, 2650.0, 780.0),
        unreal.Rotator(0.0, 0.0, 0.0),
        unreal.Vector(2.5, 2.5, 4.0),
        mat_chimney_smoke
    )

    # 4. Kiln Subterranean Flue Ember Fire Bounce Light
    spawn_or_update_point_light(
        "Light_Bhatta_Kiln_Flue_Glow",
        unreal.Vector(-1250.0, 2650.0, 45.0),
        unreal.Color(255, 120, 25, 255),  # Deep glowing coal ember orange
        2200.0,
        480.0
    )

    # 5. Underground Lithographic Printing Press & Clandestine Cache at (-1180, 2520, 0)
    spawn_or_update_mesh(
        "Story_Clandestine_Safehouse_Supply_Cache",
        mesh_cache,
        unreal.Vector(-1180.0, 2520.0, 0.0),
        unreal.Rotator(0.0, -15.0, 0.0),
        unreal.Vector(1.0, 1.0, 1.0)
    )

    # Freshly Printed Strike Handbill Bundles on crate
    spawn_or_update_mesh(
        "Prop_Safehouse_Handbill_Bundles",
        mesh_cloth_rolls,
        unreal.Vector(-1175.0, 2515.0, 35.0),
        unreal.Rotator(0.0, 20.0, 0.0),
        unreal.Vector(0.75, 0.75, 0.75),
        mat_khadi
    )

    # Safehouse Work Lantern on printing crate
    spawn_or_update_mesh(
        "Prop_Safehouse_Printing_Lantern",
        mesh_lantern,
        unreal.Vector(-1160.0, 2530.0, 20.0),
        unreal.Rotator(0.0, 0.0, 0.0),
        unreal.Vector(0.9, 0.9, 0.9),
        mat_brass
    )

    # Warm task lighting over the printing press
    spawn_or_update_point_light(
        "Light_Safehouse_Printing_Lantern",
        unreal.Vector(-1160.0, 2530.0, 60.0),
        unreal.Color(255, 195, 110, 255),
        1350.0,
        380.0
    )

    # 6. Resistance Courier Contact NPC
    civilian_class = unreal.load_class(None, "/Script/REVOLUTION.CivilianNPCActor")
    contact_label = "NPC_Resistance_Courier_Liaison"
    if contact_label in existing_actors:
        act = existing_actors[contact_label]
        act.set_actor_location(unreal.Vector(-1200.0, 2540.0, 88.0), False, True)
        act.set_actor_rotation(unreal.Rotator(0.0, 45.0, 0.0), True)
        unreal.log_warning(f"Updated {contact_label}")
    else:
        if civilian_class:
            act = actor_sub.spawn_actor_from_class(civilian_class, unreal.Vector(-1200.0, 2540.0, 88.0), unreal.Rotator(0.0, 45.0, 0.0))
            act.set_actor_label(contact_label)
            existing_actors[contact_label] = act
            unreal.log_warning(f"Spawned {contact_label}")

    # 7. Save Level Package
    level_sub.save_current_level()
    unreal.log_warning("=== Task 43 Act IV Brick Kiln Climax Assembly Completed and Level Saved Successfully! ===")

if __name__ == "__main__":
    assemble_task43_brick_kiln_press()
