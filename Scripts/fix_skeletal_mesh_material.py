import unreal

def fix_materials():
    materials_to_fix = [
        "/Game/Environment/Mohalla/Materials/M_ClothIndigo_PBR",
        "/Game/Environment/Mohalla/Materials/M_ClothSaffron_PBR",
        "/Game/Environment/Mohalla/Materials/M_ClothTurban_PBR",
        "/Game/Characters/Mannequins/Materials/M_Manny_Simple",
        "/Game/Characters/Kabir_v05/M_Kabir_Khadi_PBR",
        "/Game/Characters/Kabir_v05/M_Kabir_Skin_PBR",
        "/Game/Characters/Kabir_v05/M_Kabir_Leather_PBR",
        "/Game/Characters/Kabir_v05/M_Kabir_Eye_PBR",
        "/Game/Characters/Kabir_v05/M_Hair"
    ]

    for path in materials_to_fix:
        if unreal.EditorAssetLibrary.does_asset_exist(path):
            asset = unreal.EditorAssetLibrary.load_asset(path)
            if isinstance(asset, unreal.Material):
                curr = asset.get_editor_property("used_with_skeletal_mesh")
                unreal.log_warning(f"Material {path}: used_with_skeletal_mesh = {curr}")
                if not curr:
                    asset.set_editor_property("used_with_skeletal_mesh", True)
                    unreal.MaterialEditingLibrary.recompile_material(asset)
                    unreal.EditorAssetLibrary.save_loaded_asset(asset)
                    unreal.log_warning(f"  [FIXED] Set used_with_skeletal_mesh = True and saved {path}")
            elif isinstance(asset, unreal.MaterialInstanceConstant):
                parent = asset.get_editor_property("parent")
                if parent and isinstance(parent, unreal.Material):
                    curr = parent.get_editor_property("used_with_skeletal_mesh")
                    unreal.log_warning(f"MaterialInstance {path} parent {parent.get_name()}: used_with_skeletal_mesh = {curr}")
                    if not curr:
                        parent.set_editor_property("used_with_skeletal_mesh", True)
                        unreal.MaterialEditingLibrary.recompile_material(parent)
                        unreal.EditorAssetLibrary.save_loaded_asset(parent)
                        unreal.log_warning(f"  [FIXED] Set used_with_skeletal_mesh = True on parent {parent.get_name()}")

if __name__ == "__main__":
    fix_materials()
