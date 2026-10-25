import unreal

def assemble_task40_firing_line():
    unreal.log_warning("=== REVOLUTION: Assembling Task 40 Firing Line & Jallianwala Climax Scene ===")
    
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)
    
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    editor_asset_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    
    # 1. Load Meshes & Materials
    mesh_armored_car = unreal.load_asset("/Game/Environment/Mohalla/Meshes/SM_British_Armored_Car_Obstacle")
    mesh_bullet_wall = unreal.load_asset("/Game/Environment/Mohalla/Meshes/SM_Prop_Bullet_Pocked_Brick_Slab")
    mesh_scatter = unreal.load_asset("/Game/Environment/Mohalla/Meshes/SM_Prop_Fallen_Turban_Shoes_Scatter")
    mesh_cylinder = unreal.load_asset("/Engine/BasicShapes/Cylinder")
    
    mat_muzzle_smoke = unreal.load_asset("/Game/VFX/Smoke/Materials/MI_Smoke_Gunpowder_Muzzle")
    mat_khadi = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_ClothUndyedCotton_PBR")
    
    # Existing actors map
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

    # 2. Blocked British Armored Cars outside Narrow Alley Entrance
    spawn_or_update_mesh(
        "British_Armored_Car_Obstacle_North",
        mesh_armored_car,
        unreal.Vector(900.0, 2170.0, 0.0),
        unreal.Rotator(0.0, 0.0, 0.0),
        unreal.Vector(1.0, 1.0, 1.0)
    )
    
    spawn_or_update_mesh(
        "British_Armored_Car_Obstacle_South",
        mesh_armored_car,
        unreal.Vector(820.0, 2140.0, 0.0),
        unreal.Rotator(0.0, 15.0, 0.0),
        unreal.Vector(1.0, 1.0, 1.0)
    )

    # 3. British Military Firing Pickets on Raised Tactical Bank (SM_Jallianwala_Raised_Bank at 900, 2600, 0)
    # The raised bank top is at Z = 120
    curfew_class = unreal.load_class(None, "/Script/REVOLUTION.CurfewPatrolAI")
    
    riflemen_coords = [
        ("Picket_Rifleman_Alpha", unreal.Vector(840.0, 2620.0, 120.0)),
        ("Picket_Rifleman_Bravo", unreal.Vector(880.0, 2620.0, 120.0)),
        ("Picket_Rifleman_Charlie", unreal.Vector(920.0, 2620.0, 120.0)),
        ("Picket_Rifleman_Delta", unreal.Vector(960.0, 2620.0, 120.0)),
        ("Officer_GeneralDyer_Command", unreal.Vector(900.0, 2580.0, 120.0))
    ]
    
    for lbl, loc in riflemen_coords:
        if lbl in existing_actors:
            act = existing_actors[lbl]
            act.set_actor_location(loc, False, True)
            act.set_actor_rotation(unreal.Rotator(0.0, 90.0, 0.0), True)
            unreal.log_warning(f"Updated rifleman picket: {lbl}")
        else:
            if curfew_class:
                act = actor_sub.spawn_actor_from_class(curfew_class, loc, unreal.Rotator(0.0, 90.0, 0.0))
                act.set_actor_label(lbl)
                existing_actors[lbl] = act
                unreal.log_warning(f"Spawned rifleman picket AI: {lbl}")
            else:
                unreal.log_error(f"Failed to find CurfewPatrolAI class for {lbl}")

    # 4. Volumetric Gunsmoke Muzzle Plumes (RDR2 Inspired) across the Firing Line
    smoke_coords = [
        ("Gunsmoke_Plume_RaisedBank_01", unreal.Vector(860.0, 2650.0, 165.0), unreal.Vector(1.6, 1.6, 2.4)),
        ("Gunsmoke_Plume_RaisedBank_02", unreal.Vector(900.0, 2650.0, 165.0), unreal.Vector(1.8, 1.8, 2.6)),
        ("Gunsmoke_Plume_RaisedBank_03", unreal.Vector(940.0, 2650.0, 165.0), unreal.Vector(1.6, 1.6, 2.4))
    ]
    for lbl, loc, scl in smoke_coords:
        spawn_or_update_mesh(
            lbl,
            mesh_cylinder,
            loc,
            unreal.Rotator(0.0, 0.0, 0.0),
            scl,
            mat_muzzle_smoke
        )

    # 5. Bullet-Pocked Memorial Wall Slabs along garden perimeters
    spawn_or_update_mesh(
        "Jallianwala_Bullet_Pocked_Wall_East_02",
        mesh_bullet_wall,
        unreal.Vector(1740.0, 2900.0, 0.0),
        unreal.Rotator(0.0, -90.0, 0.0),
        unreal.Vector(1.0, 1.0, 1.0)
    )
    spawn_or_update_mesh(
        "Jallianwala_Bullet_Pocked_Wall_North",
        mesh_bullet_wall,
        unreal.Vector(1280.0, 3440.0, 0.0),
        unreal.Rotator(0.0, 0.0, 0.0),
        unreal.Vector(1.0, 1.0, 1.0)
    )

    # 6. Additional Panic Debris Scatter
    spawn_or_update_mesh(
        "Prop_Fallen_Turban_Scatter_WellApproach",
        mesh_scatter,
        unreal.Vector(1260.0, 2900.0, 0.0),
        unreal.Rotator(0.0, 45.0, 0.0),
        unreal.Vector(1.0, 1.0, 1.0)
    )
    spawn_or_update_mesh(
        "Prop_Fallen_Turban_Scatter_BreachApproach",
        mesh_scatter,
        unreal.Vector(780.0, 3300.0, 0.0),
        unreal.Rotator(0.0, -30.0, 0.0),
        unreal.Vector(1.0, 1.0, 1.0)
    )

    # 7. Save Level Package
    level_sub.save_current_level()
    unreal.log_warning("=== Task 40 Scene Assembly Completed and Level Saved Successfully! ===")

if __name__ == "__main__":
    assemble_task40_firing_line()
