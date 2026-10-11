"""
PROJECT REVOLUTION — Ingest Historical Foliage and NPC Prop FBX Meshes into Unreal Engine
"""

import os
import unreal

def log(msg):
    unreal.log(f"[REVOLUTION_FOLIAGE_IMPORT] {msg}")

def run_import():
    log("Ingesting historical foliage and NPC prop assets...")

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    exports_dir = "C:/Users/npal7/PROJECT/REVOLUTION/Art/Exports"
    destination_path = "/Game/Environment/Mohalla/Meshes"

    new_fbx_files = [
        "SM_Foliage_PeepalTree_Shrine.fbx",
        "SM_Prop_Tulsi_Pedestal.fbx",
        "SM_Prop_Bhishti_Mashk.fbx",
        "SM_Prop_ClothRolls_Manchester.fbx"
    ]

    for fbx_name in new_fbx_files:
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

    # Assign Materials
    mat_bark = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_Bark_PBR")
    mat_foliage = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_Foliage_PBR")
    mat_brick = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_LahoriBrick_PBR")
    mat_clay = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_Clay_PBR")
    mat_iron = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_WroughtIron_PBR")
    mat_indigo = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_ClothIndigo_PBR")
    mat_saffron = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_ClothSaffron_PBR")

    mesh_mat_map = {
        "SM_Foliage_PeepalTree_Shrine": [mat_bark, mat_foliage, mat_brick, mat_clay],
        "SM_Prop_Tulsi_Pedestal": [mat_brick, mat_foliage, mat_clay],
        "SM_Prop_Bhishti_Mashk": [mat_clay, mat_iron],
        "SM_Prop_ClothRolls_Manchester": [mat_indigo, mat_saffron]
    }

    for mesh_name, mats in mesh_mat_map.items():
        m_path = f"/Game/Environment/Mohalla/Meshes/{mesh_name}"
        mesh_obj = unreal.load_asset(m_path)
        if mesh_obj:
            bs = mesh_obj.get_editor_property("body_setup")
            if bs:
                bs.set_editor_property("collision_trace_flag", unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE)
            for idx, m in enumerate(mats):
                if m and idx < mesh_obj.get_num_sections(0):
                    mesh_obj.set_material(idx, m)
            unreal.EditorAssetLibrary.save_loaded_asset(mesh_obj)
            log(f"Configured materials & collision for {mesh_name}")

    unreal.EditorAssetLibrary.save_directory("/Game/Environment/Mohalla/Meshes", only_if_is_dirty=True, recursive=True)
    log("=== Foliage and NPC Props Ingestion Complete ===")

if __name__ == "__main__":
    run_import()
