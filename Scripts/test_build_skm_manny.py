import unreal

unreal.log_warning("Testing loading SKM_Manny...")
mesh = unreal.EditorAssetLibrary.load_asset("/Game/Characters/Mannequins/Meshes/SKM_Manny")
if mesh:
    unreal.log_warning(f"Loaded SKM_Manny successfully: {mesh.get_name()}")
    sub = unreal.get_editor_subsystem(unreal.SkeletalMeshEditorSubsystem)
    num_lods = sub.get_lod_count(mesh) if sub else "N/A"
    unreal.log_warning(f"SKM_Manny Num LODs: {num_lods}")
else:
    unreal.log_warning("SKM_Manny not found or failed to load!")

