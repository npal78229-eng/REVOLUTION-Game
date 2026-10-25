"""
PROJECT REVOLUTION — Kabir v06 Heritage Character Pipeline
Ingestion of Protagonist Kabir v06 Skeletal Meshes (Child 12, Teen 16, Adult 25)
and PBR Master Heritage Materials into /Game/Characters/Kabir_v06/
"""

import os
import sys
import unreal

def log(msg):
    unreal.log_warning(f"[KABIR_v06_IMPORTER] {msg}")

def create_or_update_material(mat_dir, mat_name, base_color_rgba, roughness_val, metallic_val=0.0):
    editor_asset_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    
    mat_path = f"{mat_dir}/{mat_name}"
    mat = unreal.load_asset(mat_path)
    if not mat:
        mat = asset_tools.create_asset(mat_name, mat_dir, unreal.Material, unreal.MaterialFactoryNew())
        log(f"Created Material Asset: {mat_path}")
        
    if not mat:
        log(f"ERROR: Could not create/load material: {mat_path}")
        return None
        
    try:
        mat.set_editor_property("used_with_skeletal_mesh", True)
    except Exception as e:
        log(f"Warning setting used_with_skeletal_mesh on {mat_name}: {e}")
        
    # Clear existing expressions and wire PBR properties
    try:
        # Base Color
        bc_node = unreal.MaterialEditingLibrary.create_material_expression(mat, unreal.MaterialExpressionConstant4Vector, -400, -200)
        bc_node.constant = unreal.LinearColor(base_color_rgba[0], base_color_rgba[1], base_color_rgba[2], base_color_rgba[3])
        unreal.MaterialEditingLibrary.connect_material_property(bc_node, "RGBA", unreal.MaterialProperty.MP_BASE_COLOR)
        
        # Roughness
        r_node = unreal.MaterialEditingLibrary.create_material_expression(mat, unreal.MaterialExpressionConstant, -400, 0)
        r_node.r = roughness_val
        unreal.MaterialEditingLibrary.connect_material_property(r_node, "", unreal.MaterialProperty.MP_ROUGHNESS)
        
        # Metallic
        if metallic_val > 0.0:
            m_node = unreal.MaterialEditingLibrary.create_material_expression(mat, unreal.MaterialExpressionConstant, -400, 150)
            m_node.r = metallic_val
            unreal.MaterialEditingLibrary.connect_material_property(m_node, "", unreal.MaterialProperty.MP_METALLIC)
            
        unreal.MaterialEditingLibrary.recompile_material(mat)
        editor_asset_sub.save_loaded_asset(mat)
        log(f"Configured and compiled PBR Material: {mat_name} (Color={base_color_rgba[:3]}, Roughness={roughness_val})")
    except Exception as e:
        log(f"Exception during material node wiring for {mat_name}: {e}")
        
    return mat

def build_materials():
    log("=== 1. BUILDING AUTHENTIC HERITAGE PBR MATERIALS ===")
    mat_dir = "/Game/Characters/Kabir_v06/Materials"
    editor_asset_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    if not editor_asset_sub.does_directory_exist(mat_dir):
        editor_asset_sub.make_directory(mat_dir)
        log(f"Created materials directory: {mat_dir}")
        
    materials_config = {
        # Authentic North Indian warm golden-bronze undertone
        "M_Kabir_v06_Skin": ((0.36, 0.20, 0.12, 1.0), 0.48, 0.0),
        # Deep obsidian/dark brown iris
        "M_Kabir_v06_Eye": ((0.08, 0.04, 0.02, 1.0), 0.10, 0.0),
        # Natural espresso hair
        "M_Kabir_v06_Hair": ((0.03, 0.02, 0.015, 1.0), 0.65, 0.0),
        # Unbleached handloom ecru/cream khadi kurta
        "M_Kabir_v06_Khadi_Cream": ((0.82, 0.77, 0.69, 1.0), 0.88, 0.0),
        # Pale warm wheat / oatmeal cotton pajama / dhoti
        "M_Kabir_v06_Khadi_Pajama": ((0.74, 0.68, 0.60, 1.0), 0.85, 0.0),
        # Muted saffron border shoulder cloth
        "M_Kabir_v06_Angavastram": ((0.70, 0.38, 0.20, 1.0), 0.86, 0.0),
        # Aged handcrafted saddle leather
        "M_Kabir_v06_Leather": ((0.15, 0.08, 0.04, 1.0), 0.42, 0.0),
        # Vintage satchel buckle brass
        "M_Kabir_v06_Brass": ((0.75, 0.58, 0.25, 1.0), 0.30, 0.90)
    }
    
    loaded_materials = {}
    for mat_name, (rgba, rough, metal) in materials_config.items():
        mat = create_or_update_material(mat_dir, mat_name, rgba, rough, metal)
        if mat:
            loaded_materials[mat_name] = mat
            
    return loaded_materials

def import_skeletal_mesh(fbx_path, asset_name, dest_path, loaded_materials):
    log(f"=== Importing Skeletal Mesh: {asset_name} from {fbx_path} ===")
    editor_asset_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    if not editor_asset_sub.does_directory_exist(dest_path):
        editor_asset_sub.make_directory(dest_path)
        
    task = unreal.AssetImportTask()
    task.filename = fbx_path
    task.destination_path = dest_path
    task.destination_name = asset_name
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
    
    mesh_path = f"{dest_path}/{asset_name}"
    skm = unreal.load_asset(mesh_path)
    if not skm:
        log(f"ERROR: Failed to import or load {mesh_path}")
        return None
        
    log(f"SUCCESS: Imported {asset_name}")
    skeleton = skm.get_editor_property("skeleton")
    log(f"  Skeleton: {skeleton.get_path_name() if skeleton else 'None'}")
    
    # Assign materials
    mesh_mats = skm.get_editor_property("materials")
    log(f"  Material Slot Count: {len(mesh_mats)}")
    
    for i, slot in enumerate(mesh_mats):
        slot_name = str(slot.material_slot_name)
        log(f"    Slot [{i}]: '{slot_name}'")
        
        assigned = False
        for mat_key, mat_obj in loaded_materials.items():
            if mat_key in slot_name or slot_name in mat_key:
                mesh_mats[i].material_interface = mat_obj
                assigned = True
                log(f"      Matched and assigned -> {mat_key}")
                break
                
        # Default fallback if name matching didn't match slot name
        if not assigned:
            # Check slot name hints
            lower_name = slot_name.lower()
            if "skin" in lower_name or "body" in lower_name:
                mesh_mats[i].material_interface = loaded_materials.get("M_Kabir_v06_Skin")
            elif "eye" in lower_name:
                mesh_mats[i].material_interface = loaded_materials.get("M_Kabir_v06_Eye")
            elif "hair" in lower_name:
                mesh_mats[i].material_interface = loaded_materials.get("M_Kabir_v06_Hair")
            elif "kurta" in lower_name or "cloth" in lower_name:
                mesh_mats[i].material_interface = loaded_materials.get("M_Kabir_v06_Khadi_Cream")
            elif "pajama" in lower_name or "dhoti" in lower_name or "salwar" in lower_name:
                mesh_mats[i].material_interface = loaded_materials.get("M_Kabir_v06_Khadi_Pajama")
            elif "anga" in lower_name or "chadar" in lower_name or "shawl" in lower_name:
                mesh_mats[i].material_interface = loaded_materials.get("M_Kabir_v06_Angavastram")
            elif "leather" in lower_name or "jitti" in lower_name or "jutti" in lower_name or "satchel" in lower_name:
                mesh_mats[i].material_interface = loaded_materials.get("M_Kabir_v06_Leather")
            elif "brass" in lower_name or "metal" in lower_name:
                mesh_mats[i].material_interface = loaded_materials.get("M_Kabir_v06_Brass")
            else:
                mesh_mats[i].material_interface = loaded_materials.get("M_Kabir_v06_Khadi_Cream")
            log(f"      Fallback assigned -> {mesh_mats[i].material_interface.get_name() if mesh_mats[i].material_interface else 'None'}")
            
    skm.set_editor_property("materials", mesh_mats)
    editor_asset_sub.save_loaded_asset(skm)
    log(f"Materials successfully assigned and saved on {asset_name}.")
    return skm

def main():
    log("================================================================================")
    log("  PROJECT REVOLUTION — INGESTION PIPELINE: KABIR v06 (ALL 3 LIFE STAGES)")
    log("================================================================================")
    
    base_art = "C:/Users/npal7/PROJECT/REVOLUTION/Art/Character/Kabir_v06/FBX"
    dest_path = "/Game/Characters/Kabir_v06"
    
    loaded_materials = build_materials()
    if not loaded_materials:
        log("ERROR: No materials built. Aborting.")
        sys.exit(1)
        
    stages = [
        ("SKM_Kabir_v06_Child_12.fbx", "SKM_Kabir_v06_Child_12"),
        ("SKM_Kabir_v06_Teen_16.fbx",  "SKM_Kabir_v06_Teen_16"),
        ("SKM_Kabir_v06_Adult_25.fbx", "SKM_Kabir_v06_Adult_25")
    ]
    
    imported_count = 0
    for fbx_file, asset_name in stages:
        fbx_path = os.path.join(base_art, fbx_file).replace("\\", "/")
        if not os.path.exists(fbx_path):
            log(f"ERROR: FBX file does not exist: {fbx_path}")
            continue
            
        skm = import_skeletal_mesh(fbx_path, asset_name, dest_path, loaded_materials)
        if skm:
            imported_count += 1
            
    log(f"Summary: Successfully imported and configured {imported_count}/{len(stages)} Skeletal Meshes.")
    if imported_count == len(stages):
        log("SUCCESS: All 3 Kabir v06 life stage assets ingested and verified!")
        sys.exit(0)
    else:
        log("FAILURE: Ingestion incomplete.")
        sys.exit(1)

if __name__ == "__main__":
    main()
