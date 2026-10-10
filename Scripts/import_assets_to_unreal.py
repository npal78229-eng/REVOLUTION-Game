"""
PROJECT REVOLUTION — UNREAL ENGINE HEADLESS ASSET INGESTION & LEVEL BUILDER
Imports modular 3D FBX assets, configures collisions, materials, and assembles L_Validation_Gym.
"""

import os
import unreal

def log(msg):
    unreal.log(f"[REVOLUTION] {msg}")

def run_ingestion():
    log("Starting Asset Ingestion Pipeline...")
    
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    editor_asset_subsystem = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    
    # 1. Directory Structure
    content_dirs = [
        "/Game/Environment/Mohalla/Meshes",
        "/Game/Environment/Mohalla/Materials",
        "/Game/Environment/Mohalla/Textures",
        "/Game/Maps",
        "/Game/Characters/Kabir"
    ]
    for d in content_dirs:
        if not editor_asset_subsystem.does_directory_exist(d):
            editor_asset_subsystem.make_directory(d)
            log(f"Created directory: {d}")

    # 2. FBX Files to Import
    exports_dir = "C:/Users/npal7/PROJECT/REVOLUTION/Art/Exports"
    destination_path = "/Game/Environment/Mohalla/Meshes"
    
    fbx_files = [f for f in os.listdir(exports_dir) if f.lower().endswith(".fbx")]
    log(f"Found {len(fbx_files)} FBX assets to import from {exports_dir}")

    for fbx_file in fbx_files:
        asset_name = os.path.splitext(fbx_file)[0]
        fbx_path = os.path.join(exports_dir, fbx_file).replace("\\", "/")
        
        task = unreal.AssetImportTask()
        task.filename = fbx_path
        task.destination_path = destination_path
        task.destination_name = asset_name
        task.replace_existing = True
        task.automated = True
        task.save = True
        
        options = unreal.FbxImportUI()
        options.import_mesh = True
        options.import_as_skeletal = False
        options.import_materials = False
        options.import_textures = False
        options.import_animations = False
        
        mesh_data = unreal.FbxStaticMeshImportData()
        mesh_data.combine_meshes = True
        mesh_data.auto_generate_collision = True
        mesh_data.generate_lightmap_u_vs = True
        options.static_mesh_import_data = mesh_data
        
        task.options = options
        asset_tools.import_asset_tasks([task])
        log(f"Imported StaticMesh: {asset_name} -> {destination_path}/{asset_name}")

    # 3. Create Basic PBR Materials
    mat_factory = unreal.MaterialFactoryNew()
    materials_path = "/Game/Environment/Mohalla/Materials"
    
    mat_configs = [
        ("M_LahoriBrick_PBR", unreal.LinearColor(0.55, 0.22, 0.15, 1.0), 0.85, 0.0),
        ("M_AgedTeak_PBR", unreal.LinearColor(0.25, 0.16, 0.09, 1.0), 0.65, 0.0),
        ("M_WroughtIron_PBR", unreal.LinearColor(0.12, 0.12, 0.13, 1.0), 0.40, 0.85),
        ("M_Clay_PBR", unreal.LinearColor(0.60, 0.35, 0.20, 1.0), 0.90, 0.0)
    ]
    
    for mat_name, base_color, roughness, metallic in mat_configs:
        mat_asset_path = f"{materials_path}/{mat_name}"
        if not editor_asset_subsystem.does_asset_exist(mat_asset_path):
            mat_asset = asset_tools.create_asset(mat_name, materials_path, unreal.Material, mat_factory)
            log(f"Created Material Asset: {mat_asset_path}")

    # 4. Create or Open L_Validation_Gym Level
    level_path = "/Game/Maps/L_Validation_Gym"
    world_subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    level_editor_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    
    # Create new level or load existing
    if not editor_asset_subsystem.does_asset_exist(level_path):
        level_editor_subsystem.new_level(level_path)
        log(f"Created new map: {level_path}")
    else:
        level_editor_subsystem.load_level(level_path)
        log(f"Loaded existing map: {level_path}")

    current_world = level_editor_subsystem.get_current_level().get_world()
    
    # 5. Spawn Atmosphere & Golden Hour Lighting (3200K Warm Punjab 1919)
    # Directional Light (Sun)
    sun_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.DirectionalLight,
        unreal.Vector(0, 0, 500),
        unreal.Rotator(-28.0, 45.0, 0.0) # Pitch 28 deg golden hour angle
    )
    if sun_actor:
        sun_comp = sun_actor.get_component_by_class(unreal.DirectionalLightComponent)
        if sun_comp:
            sun_comp.set_intensity(75000.0)
            sun_comp.set_use_temperature(True)
            sun_comp.set_temperature(3200.0) # Warm late afternoon Kelvin
            sun_comp.set_light_color(unreal.LinearColor(1.0, 0.88, 0.72, 1.0))
            sun_comp.set_atmosphere_sun_light(True)
        sun_actor.set_actor_label("DirectionalLight_Sun")
        log("Spawned DirectionalLight (Golden Hour 3200K)")

    # SkyAtmosphere
    sky_atmo = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.SkyAtmosphere,
        unreal.Vector(0, 0, 0),
        unreal.Rotator(0, 0, 0)
    )
    if sky_atmo:
        sky_atmo.set_actor_label("SkyAtmosphere")

    # SkyLight
    skylight_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.SkyLight,
        unreal.Vector(0, 0, 400),
        unreal.Rotator(0, 0, 0)
    )
    if skylight_actor:
        skylight_comp = skylight_actor.get_component_by_class(unreal.SkyLightComponent)
        if skylight_comp:
            skylight_comp.set_real_time_capture(True)
        skylight_actor.set_actor_label("SkyLight_RealTime")

    # Exponential Height Fog (Volumetric Fog)
    fog_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.ExponentialHeightFog,
        unreal.Vector(0, 0, 0),
        unreal.Rotator(0, 0, 0)
    )
    if fog_actor:
        fog_comp = fog_actor.get_component_by_class(unreal.ExponentialHeightFogComponent)
        if fog_comp:
            fog_comp.set_volumetric_fog(True)
            fog_comp.set_volumetric_fog_extinction_scale(0.04)
        fog_actor.set_actor_label("ExponentialHeightFog_Volumetric")

    # Post Process Volume (Software Lumen & TSR)
    ppv_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.PostProcessVolume,
        unreal.Vector(0, 0, 0),
        unreal.Rotator(0, 0, 0)
    )
    if ppv_actor:
        ppv_comp = ppv_actor.get_component_by_class(unreal.PostProcessComponent)
        if ppv_comp:
            ppv_comp.b_unbound = True
        ppv_actor.set_actor_label("PostProcessVolume_Global")

    # 6. Spawn Assembled Prototype Scene Mesh
    prototype_mesh_path = "/Game/Environment/Mohalla/Meshes/Courtyard_Rooftop_Gym_Prototype"
    prototype_mesh = unreal.load_asset(prototype_mesh_path)
    if prototype_mesh:
        mesh_actor = unreal.EditorLevelLibrary.spawn_actor_from_object(
            prototype_mesh,
            unreal.Vector(0.0, 0.0, 0.0),
            unreal.Rotator(0.0, 0.0, 0.0)
        )
        if mesh_actor:
            mesh_actor.set_actor_label("SM_Courtyard_Rooftop_Gym_Prototype")
            log(f"Spawned Prototype Gym Mesh at (0, 0, 0)")
    else:
        log("Warning: Courtyard_Rooftop_Gym_Prototype mesh could not be loaded directly.")

    # 7. Spawn PlayerStart in Courtyard
    player_start = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.PlayerStart,
        unreal.Vector(0.0, 0.0, 10.0),
        unreal.Rotator(0.0, 90.0, 0.0)
    )
    if player_start:
        player_start.set_actor_label("PlayerStart_Courtyard")
        log("Spawned PlayerStart in Courtyard ground at (0, 0, 10)")

    # Save Current Level and all dirty packages
    level_editor_subsystem.save_current_level()
    unreal.EditorAssetLibrary.save_directory("/Game", only_if_is_dirty=True, recursive=True)
    log("Saved L_Validation_Gym and all imported assets successfully!")
    log("Asset Ingestion Pipeline Finished.")

if __name__ == "__main__":
    run_ingestion()
