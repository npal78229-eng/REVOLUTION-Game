import unreal

def assemble_task41_desolate_night_clinic():
    unreal.log_warning("=== REVOLUTION: Assembling Task 41 Act III Desolate Night & Clandestine Clinic ===")
    
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)
    
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    
    # 1. Load Meshes & Materials
    mesh_stretcher = unreal.load_asset("/Game/Environment/Mohalla/Meshes/SM_Prop_Makeshift_Stretcher_Charpai")
    mesh_crate = unreal.load_asset("/Game/Environment/Mohalla/Meshes/SM_Prop_Clandestine_Safehouse_Crate_Cache")
    mesh_cloth_rolls = unreal.load_asset("/Game/Environment/Mohalla/Meshes/SM_Prop_ClothRolls_Manchester")
    mesh_lantern = unreal.load_asset("/Game/Environment/Mohalla/Meshes/SM_Prop_HurricaneLantern")
    
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

    # Helper for SpotLight
    def spawn_or_update_spot_light(label, loc, rot, color, intensity, radius, inner_angle, outer_angle, volumetric_intensity=3.0):
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
            light_comp.set_editor_property("volumetric_scattering_intensity", volumetric_intensity)
            light_comp.set_editor_property("cast_shadows", True)
        return act

    # 2. Clandestine Medical Safehouse Clinic at (-120, 950, 0)
    # Stretcher 1 already exists at Story_Makeshift_Stretcher_Alley
    # Add Stretcher 2:
    spawn_or_update_mesh(
        "Makeshift_Stretcher_Charpai_Clinic_02",
        mesh_stretcher,
        unreal.Vector(-160.0, 980.0, 0.0),
        unreal.Rotator(0.0, 25.0, 0.0),
        unreal.Vector(1.0, 1.0, 1.0)
    )
    
    # Supply Crate for First Aid medicines & antiseptics
    spawn_or_update_mesh(
        "Prop_Medical_Supply_Crate",
        mesh_crate,
        unreal.Vector(-140.0, 910.0, 0.0),
        unreal.Rotator(0.0, -10.0, 0.0),
        unreal.Vector(0.85, 0.85, 0.85)
    )
    
    # Clean Rolled Khadi Cloths for Bandages
    spawn_or_update_mesh(
        "Prop_Medical_ClothRolls_Bandages",
        mesh_cloth_rolls,
        unreal.Vector(-140.0, 910.0, 32.0),
        unreal.Rotator(0.0, 15.0, 0.0),
        unreal.Vector(0.8, 0.8, 0.8),
        mat_khadi
    )
    
    # Hurricane Lantern on clinic crate
    spawn_or_update_mesh(
        "Prop_Clinic_Hurricane_Lantern",
        mesh_lantern,
        unreal.Vector(-110.0, 970.0, 15.0),
        unreal.Rotator(0.0, 0.0, 0.0),
        unreal.Vector(0.9, 0.9, 0.9),
        mat_brass
    )
    
    # Soft warm amber lighting at the clinic
    spawn_or_update_point_light(
        "Light_Clinic_Warm_Flicker",
        unreal.Vector(-110.0, 970.0, 50.0),
        unreal.Color(255, 175, 90, 255),
        1400.0,
        420.0
    )
    
    # Volunteer Elder attending the clinic (Bhai Sant Singh / ProtestElder archetype)
    civilian_class = unreal.load_class(None, "/Script/REVOLUTION.CivilianNPCActor")
    elder_label = "NPC_Clinic_Volunteer_Elder"
    if elder_label in existing_actors:
        act = existing_actors[elder_label]
        act.set_actor_location(unreal.Vector(-180.0, 950.0, 88.0), False, True)
        act.set_actor_rotation(unreal.Rotator(0.0, 15.0, 0.0), True)
        unreal.log_warning(f"Updated {elder_label}")
    else:
        if civilian_class:
            act = actor_sub.spawn_actor_from_class(civilian_class, unreal.Vector(-180.0, 950.0, 88.0), unreal.Rotator(0.0, 15.0, 0.0))
            act.set_actor_label(elder_label)
            existing_actors[elder_label] = act
            # Configure as ProtestElder
            try:
                act.set_editor_property("Occupation", unreal.CivilianOccupation.PROTEST_ELDER)
            except:
                pass
            unreal.log_warning(f"Spawned {elder_label}")

    # 3. Imperial Searchlight Picket at (0, 2260, 0)
    # Searchlight Beam casting volumetric sweep down the Grand Bazaar corridor
    spawn_or_update_spot_light(
        "Light_Searchlight_CarbonArc_Beam",
        unreal.Vector(120.0, 2260.0, 180.0),
        unreal.Rotator(-15.0, -90.0, 0.0),  # Tilted down and facing South down the street
        unreal.Color(220, 235, 255, 255),  # Cool carbon-arc bluish white
        16000.0,
        1800.0,
        18.0,
        34.0,
        3.5
    )

    # Curfew Sentry Bunker Watchman
    curfew_class = unreal.load_class(None, "/Script/REVOLUTION.CurfewPatrolAI")
    sentry_label = "NPC_Curfew_Sentry_Bunker"
    if sentry_label in existing_actors:
        act = existing_actors[sentry_label]
        act.set_actor_location(unreal.Vector(30.0, 2220.0, 10.0), False, True)
        act.set_actor_rotation(unreal.Rotator(0.0, -90.0, 0.0), True)
        unreal.log_warning(f"Updated {sentry_label}")
    else:
        if curfew_class:
            act = actor_sub.spawn_actor_from_class(curfew_class, unreal.Vector(30.0, 2220.0, 10.0), unreal.Rotator(0.0, -90.0, 0.0))
            act.set_actor_label(sentry_label)
            existing_actors[sentry_label] = act
            unreal.log_warning(f"Spawned {sentry_label}")

    # 4. Curfew Notice Station at Chowk (-80, 1850, 0)
    spawn_or_update_point_light(
        "Light_Curfew_Notice_Niche",
        unreal.Vector(-80.0, 1850.0, 120.0),
        unreal.Color(255, 190, 110, 255),
        1100.0,
        320.0
    )

    # 5. Save Level Package
    level_sub.save_current_level()
    unreal.log_warning("=== Task 41 Act III Scene Assembly Completed and Level Saved Successfully! ===")

if __name__ == "__main__":
    assemble_task41_desolate_night_clinic()
