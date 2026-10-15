"""
PROJECT REVOLUTION — Ingest Task 7 Stampede Debris, Wall Breach & Audio into Unreal Engine
Loads FBX exports from Art/Exports and imports into /Game/Environment/Mohalla/Meshes/
Loads WAV audio from Art/Audio and imports into /Game/Audio/SFX/
Assigns period PBR materials and configures CTF_USE_COMPLEX_AS_SIMPLE collision.
"""

import os
import unreal

def log(msg):
    unreal.log_warning(f"[REVOLUTION_TASK7_IMPORT] {msg}")

def run_import():
    log("Ingesting Task 7 Stampede Debris, Wall Breach Assets & Audio into Unreal Engine...")

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    exports_dir = "C:/Users/npal7/PROJECT/REVOLUTION/Art/Exports"
    audio_dir = "C:/Users/npal7/PROJECT/REVOLUTION/Art/Audio"
    mesh_dest = "/Game/Environment/Mohalla/Meshes"
    audio_dest = "/Game/Audio/SFX"

    # 1. Ingest Audio
    audio_files = [
        "SFX_Bugle_Call_Charge.wav",
        "SFX_Crowd_Panic_Scream.wav"
    ]
    audio_tasks = []
    for af in audio_files:
        wav_path = os.path.join(audio_dir, af).replace("\\", "/")
        if os.path.exists(wav_path):
            asset_name = os.path.splitext(af)[0]
            task = unreal.AssetImportTask()
            task.filename = wav_path
            task.destination_path = audio_dest
            task.destination_name = asset_name
            task.replace_existing = True
            task.automated = True
            task.save = True
            audio_tasks.append(task)
    if audio_tasks:
        asset_tools.import_asset_tasks(audio_tasks)
        log(f"Successfully imported {len(audio_tasks)} audio assets into {audio_dest}")

    # 2. Ingest 3D Meshes
    task7_fbx_files = [
        "SM_Prop_Fallen_Turban_Shoes_Scatter.fbx",
        "SM_Jallianwala_Crumbling_Wall_Breach.fbx",
        "SM_Prop_Bullet_Pocked_Brick_Slab.fbx",
        "SM_Prop_Makeshift_Timber_Ladder.fbx"
    ]

    imported_meshes = []

    for fbx_name in task7_fbx_files:
        asset_name = os.path.splitext(fbx_name)[0]
        fbx_path = os.path.join(exports_dir, fbx_name).replace("\\", "/")
        if not os.path.exists(fbx_path):
            log(f"Warning: FBX not found: {fbx_path}")
            continue

        task = unreal.AssetImportTask()
        task.filename = fbx_path
        task.destination_path = mesh_dest
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
        log(f"Successfully imported mesh: {asset_name}")

        mesh_asset = unreal.load_asset(f"{mesh_dest}/{asset_name}")
        if mesh_asset:
            imported_meshes.append((asset_name, mesh_asset))

    # Load authentic PBR materials
    mat_brick = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_LahoriBrick_PBR")
    mat_teak = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_AgedTeak_PBR")
    mat_iron = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_WroughtIron_PBR")
    mat_clay = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_Clay_PBR")
    mat_dirt = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_DirtRoad_PBR")
    mat_saffron = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_ClothSaffron_PBR")
    mat_cotton = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_ClothUndyedCotton_PBR")

    if not mat_brick: mat_brick = mat_clay
    if not mat_teak: mat_teak = mat_brick
    if not mat_iron: mat_iron = mat_brick
    if not mat_dirt: mat_dirt = mat_clay
    if not mat_saffron: mat_saffron = mat_clay
    if not mat_cotton: mat_cotton = mat_clay

    material_bindings = {
        "SM_Prop_Fallen_Turban_Shoes_Scatter": [mat_saffron, mat_teak, mat_clay, mat_iron, mat_cotton],
        "SM_Jallianwala_Crumbling_Wall_Breach": [mat_brick, mat_dirt, mat_teak],
        "SM_Prop_Bullet_Pocked_Brick_Slab": [mat_brick, mat_cotton],
        "SM_Prop_Makeshift_Timber_Ladder": [mat_teak, mat_cotton]
    }

    for name, mesh_obj in imported_meshes:
        if name in material_bindings:
            bindings = material_bindings[name]
            for slot_idx, mat in enumerate(bindings):
                if mat:
                    mesh_obj.set_material(slot_idx, mat)
                    log(f"Assigned material {mat.get_name()} to {name} slot {slot_idx}")

        # Set Complex Collision As Simple
        body_setup = mesh_obj.get_editor_property("body_setup")
        if body_setup:
            body_setup.set_editor_property("collision_trace_flag", unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE)

        unreal.EditorAssetLibrary.save_loaded_asset(mesh_obj)

    log("Successfully completed Task 7 assets and audio ingestion into Unreal Engine!")

if __name__ == "__main__":
    run_import()
