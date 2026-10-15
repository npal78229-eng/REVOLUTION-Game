import unreal

def inspect_kabir():
    mesh = unreal.load_asset("/Game/Characters/Kabir_AAA/SK_Kabir_Protagonist_AAA")
    if not mesh:
        unreal.log_error("Could not load SK_Kabir_Protagonist_AAA")
        return

    unreal.log_warning(f"SK_Kabir_Protagonist_AAA loaded: {mesh.get_name()}")
    materials = mesh.get_editor_property("materials")
    unreal.log_warning(f"Material slots count: {len(materials)}")
    for i, mat in enumerate(materials):
        slot_name = mat.get_editor_property("material_slot_name")
        curr_mat = mat.get_editor_property("material_interface")
        mat_name = curr_mat.get_name() if curr_mat else "None"
        unreal.log_warning(f"  Slot {i}: '{slot_name}' -> {mat_name}")

    skeleton = mesh.get_editor_property("skeleton")
    unreal.log_warning(f"Skeleton: {skeleton.get_name() if skeleton else 'None'}")

if __name__ == "__main__":
    inspect_kabir()
