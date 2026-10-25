"""
PROJECT REVOLUTION — Ingestion of Kabir v06 Animation Suite into Unreal Engine 5.5
Imports all 16 FBX animations into /Game/Characters/Kabir_v06/Animations/
bound to the shared Kabir v06 Skeleton.
"""

import os
import sys
import unreal

def log(msg):
    unreal.log_warning(f"[KABIR_v06_ANIM_IMPORTER] {msg}")

def main():
    log("================================================================================")
    log("  PROJECT REVOLUTION — IMPORTING KABIR v06 ANIMATIONS TO UE 5.5")
    log("================================================================================")
    
    anim_dir = "C:/Users/npal7/PROJECT/REVOLUTION/Art/Character/Kabir_v06/Animations"
    dest_path = "/Game/Characters/Kabir_v06/Animations"
    skel_path = "/Game/Characters/Kabir_v06/SKM_Kabir_v06_Child_12_Skeleton"
    
    editor_asset_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    if not editor_asset_sub.does_directory_exist(dest_path):
        editor_asset_sub.make_directory(dest_path)
        log(f"Created animations directory: {dest_path}")
        
    skeleton = unreal.load_asset(skel_path)
    if not skeleton:
        log(f"ERROR: Could not load skeleton: {skel_path}")
        sys.exit(1)
        
    fbx_files = [f for f in os.listdir(anim_dir) if f.endswith(".fbx")]
    log(f"Found {len(fbx_files)} animation FBX files to import.")
    
    tasks = []
    for f in fbx_files:
        anim_name = os.path.splitext(f)[0]
        fbx_path = os.path.join(anim_dir, f).replace("\\", "/")
        
        task = unreal.AssetImportTask()
        task.filename = fbx_path
        task.destination_path = dest_path
        task.destination_name = anim_name
        task.replace_existing = True
        task.automated = True
        task.save = True
        
        options = unreal.FbxImportUI()
        options.automated_import_should_detect_type = False
        options.mesh_type_to_import = unreal.FBXImportType.FBXIT_ANIMATION
        options.import_mesh = False
        options.import_as_skeletal = True
        options.import_animations = True
        options.skeleton = skeleton
        
        task.options = options
        tasks.append(task)
        
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    asset_tools.import_asset_tasks(tasks)
    
    # Verify imported anim sequences
    success_count = 0
    for f in fbx_files:
        anim_name = os.path.splitext(f)[0]
        anim_asset = unreal.load_asset(f"{dest_path}/{anim_name}")
        if anim_asset:
            num_frames = anim_asset.get_editor_property("number_of_sampled_keys")
            play_length = anim_asset.get_editor_property("sequence_length")
            log(f"  [PASS] {anim_name:<30} (Frames: {num_frames}, Duration: {play_length:.2f}s)")
            success_count += 1
        else:
            log(f"  [FAIL] Failed to load {anim_name}")
            
    log(f"Summary: Successfully imported {success_count}/{len(fbx_files)} animation sequences.")
    if success_count == len(fbx_files):
        log("ALL ANIMATIONS INGESTED AND VERIFIED SUCCESSFULLY!")
        sys.exit(0)
    else:
        log("Ingestion incomplete.")
        sys.exit(1)

if __name__ == "__main__":
    main()
