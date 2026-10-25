import unreal

mesh = unreal.EditorAssetLibrary.load_asset("/Game/Environment/Mohalla/Meshes/SM_Checkpoint_Picket_Sandbag_Barrier")
if mesh:
    # Check source models and build settings
    src_models = mesh.get_editor_property("source_models")
    unreal.log_warning(f"Num source models: {len(src_models)}")
    for i, sm in enumerate(src_models):
        bs = sm.get_editor_property("build_settings")
        unreal.log_warning(f"  Model[{i}] build_scale: {bs.get_editor_property('build_scale')}")
