"""
PROJECT REVOLUTION — Headless Ingestion of Protagonist Kabir AAA Hero Skeletal Mesh
Imports SK_Kabir_Protagonist_AAA.fbx into /Game/Characters/Kabir_AAA/
"""

import os
import unreal

def log(msg):
    unreal.log_warning(f"[KABIR_HERO_IMPORTER] {msg}")

def run_import():
    log("Beginning ingestion of AAA Protagonist Hero Character (Kabir)...")

    fbx_candidates = [
        "C:/Users/npal7/PROJECT/PROJECT/SK_Kabir_Protagonist_AAA.fbx",
        "C:/Users/npal7/PROJECT/REVOLUTION/Art/PROJECT/SK_Kabir_Protagonist_AAA.fbx"
    ]
    fbx_path = None
    for cand in fbx_candidates:
        if os.path.exists(cand):
            fbx_path = cand
            break

    if not fbx_path:
        log("ERROR: Could not locate SK_Kabir_Protagonist_AAA.fbx")
        return False

    log(f"Found hero character FBX: {fbx_path} ({os.path.getsize(fbx_path)} bytes)")

    dest_path = "/Game/Characters/Kabir_AAA"
    editor_asset_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    if not editor_asset_sub.does_directory_exist(dest_path):
        editor_asset_sub.make_directory(dest_path)
        log(f"Created destination package directory: {dest_path}")

    task = unreal.AssetImportTask()
    task.filename = fbx_path
    task.destination_path = dest_path
    task.destination_name = "SK_Kabir_Protagonist_AAA"
    task.replace_existing = True
    task.automated = True
    task.save = True

    options = unreal.FbxImportUI()
    options.import_mesh = True
    options.import_as_skeletal = True
    options.import_materials = False
    options.import_textures = False
    options.import_animations = False
    options.create_physics_asset = True

    skel_data = unreal.FbxSkeletalMeshImportData()
    skel_data.import_mesh_lo_ds = False
    options.skeletal_mesh_import_data = skel_data

    task.options = options

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    asset_tools.import_asset_tasks([task])

    imported_mesh = unreal.load_asset(f"{dest_path}/SK_Kabir_Protagonist_AAA")
    if imported_mesh:
        log(f"SUCCESS: SK_Kabir_Protagonist_AAA imported successfully as SkeletalMesh: {imported_mesh.get_name()}")
        return True
    else:
        log("WARNING: Asset import task completed, but mesh not loaded at expected path. Checking directory...")
        return False

if __name__ == "__main__":
    run_import()
