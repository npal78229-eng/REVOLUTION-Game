import unreal

mesh = unreal.EditorAssetLibrary.load_asset("/Game/Environment/Mohalla/Meshes/SM_Checkpoint_Picket_Sandbag_Barrier")
if mesh:
    bounds = mesh.get_bounds()
    unreal.log_warning(f"Bounds: Origin={bounds.origin}, Extent={bounds.box_extent}")
    # Check if there is import data
    asset_import_data = mesh.get_editor_property("asset_import_data")
    if asset_import_data:
        unreal.log_warning(f"AssetImportData: {type(asset_import_data)}")
        if isinstance(asset_import_data, unreal.FbxStaticMeshImportData):
            unreal.log_warning(f"  ImportScale: {asset_import_data.get_editor_property('import_uniform_scale')}")
            unreal.log_warning(f"  ImportTranslation: {asset_import_data.get_editor_property('import_translation')}")
