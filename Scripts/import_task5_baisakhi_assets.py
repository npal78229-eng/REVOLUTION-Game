"""
PROJECT REVOLUTION — Ingest Task 5 Baisakhi Assets into Unreal Engine
Loads FBX exports from Art/Exports and imports into /Game/Environment/Mohalla/Meshes/
Assigns period PBR materials and configures complex collision.
"""

import os
import unreal

def log(msg):
    unreal.log_warning(f"[REVOLUTION_TASK5_IMPORT] {msg}")

def run_import():
    log("Ingesting Task 5 Baisakhi FBX Meshes into Unreal Engine...")

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    exports_dir = "C:/Users/npal7/PROJECT/REVOLUTION/Art/Exports"
    destination_path = "/Game/Environment/Mohalla/Meshes"

    task5_fbx_files = [
        "SM_Munadi_Proclamation_Drum.fbx",
        "SM_Baisakhi_Garland_Archway.fbx",
        "SM_Jallianwala_Narrow_Gateway.fbx",
        "SM_Prop_Wheat_Sheaves_Cart.fbx",
        "SM_Baisakhi_Mela_Sweet_Stall.fbx"
    ]

    imported_meshes = []

    for fbx_name in task5_fbx_files:
        asset_name = os.path.splitext(fbx_name)[0]
        fbx_path = os.path.join(exports_dir, fbx_name).replace("\\", "/")
        if not os.path.exists(fbx_path):
            log(f"Warning: FBX not found: {fbx_path}")
            continue

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
        log(f"Successfully imported: {asset_name}")

        mesh_asset = unreal.load_asset(f"{destination_path}/{asset_name}")
        if mesh_asset:
            imported_meshes.append((asset_name, mesh_asset))

    # Load authentic PBR materials
    mat_brick = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_LahoriBrick_PBR")
    mat_teak = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_AgedTeak_PBR")
    mat_iron = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_WroughtIron_PBR")
    mat_clay = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_Clay_PBR")
    mat_saffron = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_ClothSaffron_PBR")
    mat_cotton = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_ClothUndyedCotton_PBR")
    mat_foliage = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_Foliage_PBR")

    if not mat_brick: mat_brick = mat_clay
    if not mat_teak: mat_teak = mat_brick
    if not mat_iron: mat_iron = mat_brick
    if not mat_saffron: mat_saffron = mat_clay
    if not mat_cotton: mat_cotton = mat_clay
    if not mat_foliage: mat_foliage = mat_clay

    material_bindings = {
        "SM_Munadi_Proclamation_Drum": [mat_iron, mat_teak, mat_cotton, mat_cotton],
        "SM_Baisakhi_Garland_Archway": [mat_teak, mat_saffron, mat_foliage, mat_brick],
        "SM_Jallianwala_Narrow_Gateway": [mat_brick, mat_iron, mat_teak],
        "SM_Prop_Wheat_Sheaves_Cart": [mat_teak, mat_iron, mat_saffron],
        "SM_Baisakhi_Mela_Sweet_Stall": [mat_teak, mat_saffron, mat_clay, mat_saffron]
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

    log("Successfully completed Task 5 Baisakhi assets import and configuration!")

if __name__ == "__main__":
    run_import()
