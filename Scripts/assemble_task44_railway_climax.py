import unreal

def assemble_task44_railway_climax():
    unreal.log_warning("=== REVOLUTION: Assembling Task 44 Act V North Western Railway Climax Scene ===")
    
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)
    
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    
    # Load Meshes & Materials
    mesh_cylinder = unreal.load_asset("/Engine/BasicShapes/Cylinder")
    mat_chimney_smoke = unreal.load_asset("/Game/VFX/Smoke/Materials/MI_Smoke_Haveli_Chimney")
    mesh_brass = unreal.load_asset("/Game/Environment/Mohalla/Meshes/SM_Prop_BrassUrli")
    mat_brass = unreal.load_asset("/Game/Environment/Mohalla/Materials/MI_HammeredBrass_Photogrammetry")
    
    existing_actors = {a.get_actor_label(): a for a in actor_sub.get_all_level_actors()}
    
    # Helper for StaticMeshActor
    def spawn_or_update_mesh(label, mesh, loc, rot=unreal.Rotator(0,0,0), scale=unreal.Vector(1,1,1), mat=None):
        if label in existing_actors:
            act = existing_actors[label]
            act.set_actor_location(loc, False, True)
            act.set_actor_rotation(rot, True)
            act.set_actor_scale3d(scale)
            unreal.log_warning(f"Updated existing mesh actor: {label}")
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

    # Helper for SpotLight
    def spawn_or_update_spot_light(label, loc, rot, color, intensity, radius, inner_angle, outer_angle, scattering=1.0):
        if label in existing_actors:
            act = existing_actors[label]
            act.set_actor_location(loc, False, True)
            act.set_actor_rotation(rot, True)
            unreal.log_warning(f"Updated spot light: {label}")
        else:
            act = actor_sub.spawn_actor_from_class(unreal.SpotLight, loc, rot)
            act.set_actor_label(label)
            existing_actors[label] = act
            unreal.log_warning(f"Spawned spot light: {label}")
            
        light_comp = act.get_component_by_class(unreal.SpotLightComponent)
        if light_comp:
            light_comp.set_editor_property("light_color", color)
            light_comp.set_editor_property("intensity", intensity)
            light_comp.set_editor_property("attenuation_radius", radius)
            light_comp.set_editor_property("inner_cone_angle", inner_angle)
            light_comp.set_editor_property("outer_cone_angle", outer_angle)
            light_comp.set_editor_property("volumetric_scattering_intensity", scattering)
            light_comp.set_editor_property("cast_shadows", True)
        return act

    # 1. RDR2-Inspired Locomotive Smokestack Smoke Plume
    # Anchored at top of locomotive smokebox (X=1000, Y=4120, Z=360)
    spawn_or_update_mesh(
        "Smoke_Plume_Locomotive_PunjabMail",
        mesh_cylinder,
        unreal.Vector(1000.0, 4120.0, 360.0),
        unreal.Rotator(0.0, 0.0, 0.0),
        unreal.Vector(1.8, 1.8, 3.2),
        mat_chimney_smoke
    )

    # 2. Locomotive Boiler High-Powered Headlamp Beam
    # Pierces the cutting fog along track direction (Rotator -5, 90, 0)
    spawn_or_update_spot_light(
        "Light_Locomotive_Headlamp_Beam",
        unreal.Vector(1000.0, 4180.0, 160.0),
        unreal.Rotator(-5.0, 90.0, 0.0),
        unreal.Color(255, 230, 180, 255),
        14000.0,
        2500.0,
        20.0,
        38.0,
        2.5
    )

    # 3. Semaphore Signal Gantry High-Level Signal Lanterns at (1160, 3960, 650)
    spawn_or_update_point_light(
        "Light_Railway_Signal_Amber",
        unreal.Vector(1160.0, 3960.0, 650.0),
        unreal.Color(255, 160, 20, 255),
        1800.0,
        600.0
    )
    spawn_or_update_point_light(
        "Light_Railway_Signal_Green",
        unreal.Vector(1160.0, 3960.0, 580.0),
        unreal.Color(40, 255, 120, 255),
        1200.0,
        450.0
    )

    # 4. Signal Gantry Maintenance Access Ladder Actor (ALadderActor)
    ladder_class = unreal.load_class(None, "/Script/REVOLUTION.LadderActor")
    ladder_label = "Ladder_Signal_Gantry_Climb"
    if ladder_label in existing_actors:
        act = existing_actors[ladder_label]
        act.set_actor_location(unreal.Vector(1175.0, 3960.0, 0.0), False, True)
        act.set_actor_rotation(unreal.Rotator(0.0, 90.0, 0.0), True)
        unreal.log_warning(f"Updated {ladder_label}")
    else:
        if ladder_class:
            act = actor_sub.spawn_actor_from_class(ladder_class, unreal.Vector(1175.0, 3960.0, 0.0), unreal.Rotator(0.0, 90.0, 0.0))
            act.set_actor_label(ladder_label)
            try:
                act.set_editor_property("ClimbDuration", 2.2)
            except:
                pass
            existing_actors[ladder_label] = act
            unreal.log_warning(f"Spawned {ladder_label}")

    # 5. Cantonment Gate Sentry Watchman (ACurfewPatrolAI)
    curfew_class = unreal.load_class(None, "/Script/REVOLUTION.CurfewPatrolAI")
    sentry_label = "NPC_Cantonment_Sentry_NorthGate"
    if sentry_label in existing_actors:
        act = existing_actors[sentry_label]
        act.set_actor_location(unreal.Vector(650.0, 4200.0, 10.0), False, True)
        act.set_actor_rotation(unreal.Rotator(0.0, -90.0, 0.0), True)
        unreal.log_warning(f"Updated {sentry_label}")
    else:
        if curfew_class:
            act = actor_sub.spawn_actor_from_class(curfew_class, unreal.Vector(650.0, 4200.0, 10.0), unreal.Rotator(0.0, -90.0, 0.0))
            act.set_actor_label(sentry_label)
            existing_actors[sentry_label] = act
            unreal.log_warning(f"Spawned {sentry_label}")

    # Cantonment Sentry Gate Lantern
    spawn_or_update_point_light(
        "Light_Cantonment_NorthGate_Sentry",
        unreal.Vector(650.0, 4220.0, 180.0),
        unreal.Color(255, 200, 120, 255),
        1800.0,
        500.0
    )

    # 6. Cantonment Administrative Veranda Dressing & Task Light
    spawn_or_update_mesh(
        "Prop_Cantonment_Telegraph_Station",
        mesh_brass,
        unreal.Vector(835.0, 4515.0, 95.0),
        unreal.Rotator(0.0, 45.0, 0.0),
        unreal.Vector(0.7, 0.7, 0.7),
        mat_brass
    )
    spawn_or_update_point_light(
        "Light_Cantonment_Archive_Veranda",
        unreal.Vector(820.0, 4520.0, 160.0),
        unreal.Color(255, 210, 130, 255),
        1500.0,
        450.0
    )

    # 7. Save Level Package
    level_sub.save_current_level()
    unreal.log_warning("=== Task 44 Act V Railway Climax Scene Assembled and Level Saved Successfully! ===")

if __name__ == "__main__":
    assemble_task44_railway_climax()
