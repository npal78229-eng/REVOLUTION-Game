"""
PROJECT REVOLUTION — Ingest Task 9 Canal & Outskirts Assets & Audio into Unreal Engine
Loads FBX exports from Art/Exports and imports into /Game/Environment/Mohalla/Meshes/
Loads WAV audio from Art/Audio and imports into /Game/Audio/SFX/
Assigns period PBR materials and configures CTF_USE_COMPLEX_AS_SIMPLE collision.
"""

import os
import unreal

def log(msg):
    unreal.log_warning(f"[REVOLUTION_TASK9_IMPORT] {msg}")

def run_import():
    log("Ingesting Task 9 Canal, Persian Wheel, Bhatta Assets & Audio into Unreal Engine...")

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    exports_dir = "C:/Users/npal7/PROJECT/REVOLUTION/Art/Exports"
    audio_dir = "C:/Users/npal7/PROJECT/REVOLUTION/Art/Audio"
    mesh_dest = "/Game/Environment/Mohalla/Meshes"
    audio_dest = "/Game/Audio/SFX"

    # 1. Ingest Audio
    audio_files = [
        "SFX_Canal_Water_Flow_Gentle.wav",
        "SFX_Persian_Wheel_Rahat_Creak.wav"
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
    task9_fbx_files = [
        "SM_Canal_Distributary_Aqueduct_Stone.fbx",
        "SM_Persian_Wheel_Rahat_Timber.fbx",
        "SM_Brick_Kiln_Chimney_Bhatta.fbx",
        "SM_Prop_Clandestine_Safehouse_Crate_Cache.fbx"
    ]

    imported_meshes = []

    for fbx_name in task9_fbx_files:
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

    # 3. Configure Materials & Collision for imported meshes
    material_map = {
        "M_LahoriBrick_PBR": "/Game/Environment/Mohalla/Materials/M_LahoriBrick_PBR",
        "M_AgedTeak_PBR": "/Game/Environment/Mohalla/Materials/M_AgedTeak_PBR",
        "M_WroughtIron_PBR": "/Game/Environment/Mohalla/Materials/M_WroughtIron_PBR",
        "M_ClothUndyedCotton_PBR": "/Game/Environment/Mohalla/Materials/M_ClothUndyedCotton_PBR",
        "M_DirtRoad_PBR": "/Game/Environment/Mohalla/Materials/M_DirtRoad_PBR",
        "M_Clay_PBR": "/Game/Environment/Mohalla/Materials/M_Clay_PBR"
    }
    loaded_materials = {}
    for mat_name, mat_path in material_map.items():
        mat_obj = unreal.load_asset(mat_path)
        if mat_obj:
            loaded_materials[mat_name] = mat_obj

    # Material assignments per mesh
    mesh_material_assignments = {
        "SM_Canal_Distributary_Aqueduct_Stone": [
            "M_LahoriBrick_PBR",
            "M_WroughtIron_PBR",
            "M_AgedTeak_PBR"
        ],
        "SM_Persian_Wheel_Rahat_Timber": [
            "M_AgedTeak_PBR",
            "M_Clay_PBR",
            "M_WroughtIron_PBR"
        ],
        "SM_Brick_Kiln_Chimney_Bhatta": [
            "M_LahoriBrick_PBR",
            "M_DirtRoad_PBR",
            "M_Clay_PBR"
        ],
        "SM_Prop_Clandestine_Safehouse_Crate_Cache": [
            "M_AgedTeak_PBR",
            "M_WroughtIron_PBR",
            "M_ClothUndyedCotton_PBR"
        ]
    }

    for asset_name, mesh_asset in imported_meshes:
        if asset_name in mesh_material_assignments:
            slot_names = mesh_material_assignments[asset_name]
            for slot_idx, mat_name in enumerate(slot_names):
                if mat_name in loaded_materials:
                    mesh_asset.set_material(slot_idx, loaded_materials[mat_name])
                    log(f"Assigned material {mat_name} to {asset_name} slot {slot_idx}")

        # Collision settings: Complex as simple for realistic parkour vaulting & physical navigation
        body_setup = mesh_asset.get_editor_property("body_setup")
        if body_setup:
            body_setup.set_editor_property("collision_trace_flag", unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE)
        unreal.EditorAssetLibrary.save_loaded_asset(mesh_asset)

    log("Successfully completed Task 9 assets and audio ingestion into Unreal Engine!")

if __name__ == "__main__":
    run_import()
