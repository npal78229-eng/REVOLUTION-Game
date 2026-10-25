import unreal

unreal.log_warning("Testing loading SKM_Quinn...")
mesh = unreal.EditorAssetLibrary.load_asset("/Game/Characters/Mannequins/Meshes/SKM_Quinn")
if mesh:
    unreal.log_warning(f"Loaded SKM_Quinn successfully: {mesh.get_name()}")
    num_lods = unreal.SkeletalMeshEditorSubsystem().get_lod_count(mesh) if hasattr(unreal, 'SkeletalMeshEditorSubsystem') else "N/A"
    unreal.log_warning(f"SKM_Quinn Num LODs: {num_lods}")
else:
    unreal.log_warning("SKM_Quinn not found or failed to load!")

