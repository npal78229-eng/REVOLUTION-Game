"""
PROJECT REVOLUTION — Ingest Story Realism FBX Meshes into Unreal Engine
Loads FBX exports from Art/Exports and imports into /Game/Environment/Mohalla/Meshes/
Assigns period PBR materials and configures collision.
"""

import os
import unreal

def log(msg):
    unreal.log_warning(f"[REVOLUTION_STORY_IMPORT] {msg}")

def run_import():
    log("Ingesting 5 Story Realism FBX Meshes into Unreal Engine...")

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    exports_dir = "C:/Users/npal7/PROJECT/REVOLUTION/Art/Exports"
    destination_path = "/Game/Environment/Mohalla/Meshes"

    new_fbx_files = [
        "SM_Prop_School_Takhti_Slate.fbx",
        "SM_Prop_Bazaar_Cart_Thela.fbx",
        "SM_Prop_Courtyard_Chulha_Stove.fbx",
        "SM_Prop_Pigeon_Coop_KabootarKhana.fbx",
        "SM_Prop_Pamphlet_Stack_Rowlatt.fbx"
    ]

    imported_meshes = []

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

        mesh_asset = unreal.load_asset(f"{destination_path}/{asset_name}")
        if mesh_asset:
            imported_meshes.append((asset_name, mesh_asset))

    # Load authentic PBR materials
    mat_teak = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_AgedTeak_PBR")
    mat_clay = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_Clay_PBR")
    mat_iron = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_WroughtIron_PBR")
    mat_brick = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_LahoriBrick_PBR")
    mat_cloth = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_ClothIndigo_PBR")

    # Fallback to brick or clay if any material isn't present
    if not mat_teak: mat_teak = mat_brick
    if not mat_clay: mat_clay = mat_brick
    if not mat_iron: mat_iron = mat_brick

    material_bindings = {
        "SM_Prop_School_Takhti_Slate": [mat_teak, mat_clay],
        "SM_Prop_Bazaar_Cart_Thela": [mat_teak, mat_iron, mat_teak, mat_clay],
        "SM_Prop_Courtyard_Chulha_Stove": [mat_clay, mat_teak, mat_iron, mat_teak],
        "SM_Prop_Pigeon_Coop_KabootarKhana": [mat_teak, mat_iron, mat_clay],
        "SM_Prop_Pamphlet_Stack_Rowlatt": [mat_clay, mat_iron]
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

    log("=== Ingestion of Story Realism Assets Complete ===")

if __name__ == "__main__":
    run_import()
