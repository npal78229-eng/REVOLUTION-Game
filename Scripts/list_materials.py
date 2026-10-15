import unreal

def inspect_materials():
    asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
    filter = unreal.ARFilter(
        class_names=["Material", "MaterialInstanceConstant"],
        package_paths=["/Game"],
        recursive_paths=True
    )
    assets = asset_reg.get_assets(filter)
    unreal.log_warning(f"Found {len(assets)} materials in /Game:")
    for a in assets[:20]:
        unreal.log_warning(f"  {a.package_name} ({a.asset_class_path.asset_name})")

if __name__ == "__main__":
    inspect_materials()
