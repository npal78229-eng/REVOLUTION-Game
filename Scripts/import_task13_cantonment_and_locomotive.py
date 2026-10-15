"""
PROJECT REVOLUTION — Task 13 Ingestion Script
Imports:
1. SM_Locomotive_Engine_PunjabMail.fbx
2. SM_Civil_Lines_Clubhouse_Bungalow.fbx
3. SM_Cantonment_Guardhouse_Picket.fbx
4. SM_Prop_Cantonment_Archive_Cabinet.fbx
5. SFX_Telegraph_Chirp_Ticker.wav
6. SFX_Locomotive_Steam_Hiss.wav
"""

import os
import unreal

def log(msg):
    unreal.log_warning(f"[TASK13_IMPORTER] {msg}")

def run_import():
    log("Starting Task 13 Asset Ingestion into Unreal Engine 5.5...")

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    mesh_dest = "/Game/Environment/Mohalla/Meshes"
    audio_dest = "/Game/Audio/SFX"

    # 1. Ingest 4 Static Meshes
    mesh_files = [
        "SM_Locomotive_Engine_PunjabMail.fbx",
        "SM_Civil_Lines_Clubhouse_Bungalow.fbx",
        "SM_Cantonment_Guardhouse_Picket.fbx",
        "SM_Prop_Cantonment_Archive_Cabinet.fbx"
    ]

    mesh_src_dir = "C:/Users/npal7/PROJECT/PROJECT"
    tasks = []

    for mf in mesh_files:
        src = os.path.join(mesh_src_dir, mf)
        if not os.path.exists(src):
            src = os.path.join("C:/Users/npal7/PROJECT/REVOLUTION/Art/Exports", mf)

        asset_name = os.path.splitext(mf)[0]
        task = unreal.AssetImportTask()
        task.filename = src
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

        static_data = unreal.FbxStaticMeshImportData()
        static_data.combine_meshes = True
        static_data.generate_lightmap_u_vs = True
        options.static_mesh_import_data = static_data

        task.options = options
        tasks.append(task)

    # 2. Ingest Audio
    audio_files = [
        "SFX_Telegraph_Chirp_Ticker.wav",
        "SFX_Locomotive_Steam_Hiss.wav"
    ]
    audio_src_dir = "C:/Users/npal7/PROJECT/REVOLUTION/Project/Content/Audio/SFX"

    for af in audio_files:
        src = os.path.join(audio_src_dir, af)
        if os.path.exists(src):
            asset_name = os.path.splitext(af)[0]
            task = unreal.AssetImportTask()
            task.filename = src
            task.destination_path = audio_dest
            task.destination_name = asset_name
            task.replace_existing = True
            task.automated = True
            task.save = True
            tasks.append(task)

    asset_tools.import_asset_tasks(tasks)

    # 3. Post-process static meshes: set complex collision as simple
    editor_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    for mf in mesh_files:
        asset_name = os.path.splitext(mf)[0]
        mesh_path = f"{mesh_dest}/{asset_name}"
        mesh_obj = unreal.load_asset(mesh_path)
        if mesh_obj:
            mesh_obj.set_editor_property("body_setup", mesh_obj.get_editor_property("body_setup"))
            body_setup = mesh_obj.get_editor_property("body_setup")
            if body_setup:
                body_setup.set_editor_property("collision_trace_flag", unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE)
            editor_sub.save_loaded_asset(mesh_obj)
            log(f"Configured CTF_USE_COMPLEX_AS_SIMPLE for {asset_name}")

    log("Task 13 Asset Ingestion completed successfully!")
    return True

if __name__ == "__main__":
    run_import()
