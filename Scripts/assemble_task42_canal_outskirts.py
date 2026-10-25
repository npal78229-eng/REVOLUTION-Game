import unreal

def assemble_task42_canal_outskirts():
    unreal.log_warning("=== REVOLUTION: Assembling Task 42 Act IV Canal Outskirts Scene ===")
    
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)
    
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    
    # 1. Load Meshes & Materials
    mesh_cart = unreal.load_asset("/Game/Environment/Mohalla/Meshes/SM_Prop_Wheat_Sheaves_Cart")
    mesh_lantern = unreal.load_asset("/Game/Environment/Mohalla/Meshes/SM_Prop_HurricaneLantern")
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

    # Helper for AmbientSound / AudioComponent
    def spawn_or_update_audio(label, sound_path, loc, volume=1.0):
        sound_asset = unreal.load_asset(sound_path)
        if label in existing_actors:
            act = existing_actors[label]
            act.set_actor_location(loc, False, True)
            unreal.log_warning(f"Updated audio actor: {label}")
        else:
            act = actor_sub.spawn_actor_from_class(unreal.AmbientSound, loc, unreal.Rotator(0,0,0))
            act.set_actor_label(label)
            existing_actors[label] = act
            unreal.log_warning(f"Spawned ambient sound actor: {label}")
            
        audio_comp = act.get_component_by_class(unreal.AudioComponent)
        if audio_comp and sound_asset:
            audio_comp.set_editor_property("sound", sound_asset)
            audio_comp.set_editor_property("volume_multiplier", volume)
            audio_comp.set_editor_property("auto_activate", True)
        return act

    # 2. Agricultural Harvest Bullock Cart beside Canal Bed
    spawn_or_update_mesh(
        "Prop_Wheat_Harvest_BullockCart_Canal",
        mesh_cart,
        unreal.Vector(-1080.0, 2120.0, 0.0),
        unreal.Rotator(0.0, 35.0, 0.0),
        unreal.Vector(1.0, 1.0, 1.0)
    )

    # 3. Canal Sluice Catwalk Hurricane Lantern & Light
    spawn_or_update_mesh(
        "Prop_Canal_Sluice_Catwalk_Lantern",
        mesh_lantern,
        unreal.Vector(-950.0, 2200.0, 85.0),
        unreal.Rotator(0.0, 0.0, 0.0),
        unreal.Vector(0.9, 0.9, 0.9),
        mat_brass
    )
    spawn_or_update_point_light(
        "Light_Canal_Sluice_Catwalk",
        unreal.Vector(-950.0, 2200.0, 115.0),
        unreal.Color(255, 185, 100, 255),
        1300.0,
        380.0
    )

    # 4. Persian Wheel (Rahat) Flume Light
    spawn_or_update_point_light(
        "Light_Rahat_Timber_Flume",
        unreal.Vector(-1150.0, 2050.0, 95.0),
        unreal.Color(255, 180, 95, 255),
        1200.0,
        360.0
    )

    # 5. Continuous 3D Spatialized Atmospheric Audio
    spawn_or_update_audio(
        "Audio_Canal_Water_Flow",
        "/Game/Audio/SFX/SFX_Canal_Water_Flow_Gentle",
        unreal.Vector(-950.0, 2200.0, 30.0),
        1.15
    )
    spawn_or_update_audio(
        "Audio_Persian_Wheel_Creak",
        "/Game/Audio/SFX/SFX_Persian_Wheel_Rahat_Creak",
        unreal.Vector(-1150.0, 2050.0, 60.0),
        1.25
    )

    # 6. Save Level Package
    level_sub.save_current_level()
    unreal.log_warning("=== Task 42 Act IV Canal Scene Assembly Completed and Level Saved Successfully! ===")

if __name__ == "__main__":
    assemble_task42_canal_outskirts()
