import unreal

def assign_materials():
    mesh_path = "/Game/Characters/Kabir_AAA/SK_Kabir_Protagonist_AAA"
    mesh = unreal.load_asset(mesh_path)
    if not mesh:
        unreal.log_error(f"Failed to load {mesh_path}")
        return False

    mat_mapping = {
        0: "/Game/Characters/Kabir_v04_RigB/Kabir_Skin",
        1: "/Game/Environment/Mohalla/Materials/M_AgedTeak_PBR",
        2: "/Game/Characters/Kabir_v04_RigB/Kabir_Sclera",
        3: "/Game/Characters/Kabir_v04_RigB/Kabir_Iris",
        4: "/Game/Characters/Kabir_v04_RigB/Kabir_Hair_001",
        5: "/Game/Environment/Mohalla/Materials/M_AgedTeak_PBR",
        6: "/Game/Characters/Kabir_v04_RigB/Kabir_Kurta_Undyed_001",
        7: "/Game/Characters/Kabir_v04_RigB/Kabir_Shorts_Cotton",
        8: "/Game/Environment/Mohalla/Materials/M_ClothSaffron_PBR",
        9: "/Game/Environment/Mohalla/Materials/M_WroughtIron_PBR"
    }

    materials = mesh.get_editor_property("materials")
    for idx, mat_path in mat_mapping.items():
        if idx < len(materials):
            mat_asset = unreal.load_asset(mat_path)
            if mat_asset:
                materials[idx].set_editor_property("material_interface", mat_asset)
                slot_name = materials[idx].get_editor_property("material_slot_name")
                unreal.log_warning(f"Assigned {mat_path} to slot {idx} ({slot_name})")
            else:
                unreal.log_error(f"Could not load material {mat_path}")

    mesh.set_editor_property("materials", materials)
    unreal.EditorAssetSubsystem().save_loaded_asset(mesh)
    unreal.log_warning("Successfully updated and saved SK_Kabir_Protagonist_AAA materials!")
    return True

if __name__ == "__main__":
    assign_materials()
