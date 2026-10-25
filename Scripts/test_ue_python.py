import unreal

def main():
    unreal.log_warning("=== UE5 Python Test Script Executing ===")
    version = unreal.SystemLibrary.get_engine_version()
    unreal.log_warning(f"Engine Version: {version}")
    
    # Test asset tools
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    unreal.log_warning(f"AssetTools available: {asset_tools is not None}")

if __name__ == "__main__":
    main()
