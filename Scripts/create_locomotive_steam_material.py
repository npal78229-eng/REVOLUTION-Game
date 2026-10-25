import unreal

def create_locomotive_steam_material():
    master_mat = unreal.load_asset("/Game/VFX/Smoke/Materials/M_RDR2_Pyroclastic_Smoke")
    if not master_mat:
        unreal.log_error("Could not load M_RDR2_Pyroclastic_Smoke!")
        return False
        
    mat_path = "/Game/VFX/Smoke/Materials"
    inst_name = "MI_Smoke_Locomotive_Steam"
    inst_full = f"{mat_path}/{inst_name}"
    
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = unreal.MaterialInstanceConstantFactoryNew()
    
    inst = unreal.EditorAssetLibrary.load_asset(inst_full)
    if not inst:
        inst = asset_tools.create_asset(inst_name, mat_path, unreal.MaterialInstanceConstant, factory)
        
    if inst:
        inst.set_editor_property("parent", master_mat)
        unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(
            inst, "SmokeBaseColor", unreal.LinearColor(0.85, 0.88, 0.92, 1.0)
        )
        unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(
            inst, "SilverRimColor", unreal.LinearColor(1.0, 1.0, 1.0, 1.0)
        )
        unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(
            inst, "CurlDistortionStrength", 0.15
        )
        unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(
            inst, "SilverRimExponent", 1.6
        )
        unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(
            inst, "DepthFadeDistance", 60.0
        )
        unreal.MaterialEditingLibrary.update_material_instance(inst)
        unreal.EditorAssetLibrary.save_loaded_asset(inst)
        unreal.log_warning(f"Created & configured {inst_name} successfully!")
        return True
    return False

if __name__ == "__main__":
    create_locomotive_steam_material()
