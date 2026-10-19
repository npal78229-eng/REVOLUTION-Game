"""
PROJECT REVOLUTION — Ingestion of Protagonist Kabir v05 Skeletal Mesh & PBR Textures
Imports SKM_Kabir_v05.fbx and 11 PBR texture maps into /Game/Characters/Kabir_v05/
"""

import os
import unreal

def log(msg):
    unreal.log_warning(f"[KABIR_v05_IMPORTER] {msg}")

def import_textures():
    tex_dir = "C:/Users/npal7/PROJECT/REVOLUTION/Art/Character/Kabir_v05/Textures"
    dest_path = "/Game/Characters/Kabir_v05/Textures"
    
    editor_asset_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    if not editor_asset_sub.does_directory_exist(dest_path):
        editor_asset_sub.make_directory(dest_path)
        log(f"Created directory: {dest_path}")
        
    tasks = []
    files = [f for f in os.listdir(tex_dir) if f.endswith(".png")]
    for f in files:
        fpath = os.path.join(tex_dir, f).replace("\\", "/")
        tname = os.path.splitext(f)[0]
        
        task = unreal.AssetImportTask()
        task.filename = fpath
        task.destination_path = dest_path
        task.destination_name = tname
        task.replace_existing = True
        task.automated = True
        task.save = True
        tasks.append(task)
        
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    asset_tools.import_asset_tasks(tasks)
    log(f"Imported {len(tasks)} textures.")
    
    # Configure compression settings
    for f in files:
        tname = os.path.splitext(f)[0]
        tex_asset = unreal.load_asset(f"{dest_path}/{tname}")
        if tex_asset:
            if "_N" in tname:
                tex_asset.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_NORMALMAP)
                try:
                    tex_asset.set_editor_property("srgb", False)
                except Exception:
                    pass
            elif "_ORM" in tname:
                tex_asset.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_MASKS)
                try:
                    tex_asset.set_editor_property("srgb", False)
                except Exception:
                    pass
            editor_asset_sub.save_loaded_asset(tex_asset)
            log(f"  Configured texture: {tname}")

def import_skeletal_mesh():
    fbx_path = "C:/Users/npal7/PROJECT/REVOLUTION/Art/Character/Kabir_v05/SKM_Kabir_v05.fbx"
    dest_path = "/Game/Characters/Kabir_v05"
    
    editor_asset_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    if not editor_asset_sub.does_directory_exist(dest_path):
        editor_asset_sub.make_directory(dest_path)
        
    task = unreal.AssetImportTask()
    task.filename = fbx_path
    task.destination_path = dest_path
    task.destination_name = "SKM_Kabir_v05"
    task.replace_existing = True
    task.automated = True
    task.save = True
    
    options = unreal.FbxImportUI()
    options.import_mesh = True
    options.import_as_skeletal = True
    options.import_materials = True
    options.import_textures = False
    options.import_animations = False
    options.create_physics_asset = True
    
    skel_data = unreal.FbxSkeletalMeshImportData()
    skel_data.import_mesh_lo_ds = False
    options.skeletal_mesh_import_data = skel_data
    
    task.options = options
    
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    asset_tools.import_asset_tasks([task])
    
    skm = unreal.load_asset(f"{dest_path}/SKM_Kabir_v05")
    if skm:
        log(f"SUCCESS: Loaded SKM_Kabir_v05: {skm.get_name()}")
        skeleton = skm.get_editor_property("skeleton")
        log(f"  Skeleton: {skeleton.get_path_name() if skeleton else 'None'}")
        return True
    else:
        log("ERROR: Failed to load SKM_Kabir_v05 after import.")
        return False

def main():
    log("=== STARTING KABIR v05 INGESTION INTO UNREAL ENGINE 5.5 ===")
    import_textures()
    success = import_skeletal_mesh()
    if success:
        log("=== KABIR v05 INGESTION COMPLETED SUCCESSFULLY ===")
    else:
        log("=== KABIR v05 INGESTION FAILED ===")

if __name__ == "__main__":
    main()
