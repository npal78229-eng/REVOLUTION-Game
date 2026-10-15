import unreal

def test_assign():
    bp_path = "/Game/Characters/Kabir/BP_Kabir"
    bp = unreal.load_asset(bp_path)
    mesh = unreal.load_asset("/Game/Characters/Kabir_AAA/SK_Kabir_Protagonist_AAA")
    unreal.log_warning(f"BP: {bp.get_name()}, Hero Mesh: {mesh.get_name()}")
    # Let's inspect the blueprint's component templates
    sub = unreal.get_editor_subsystem(unreal.SubobjectDataSubsystem)
    handles = sub.k2_gather_subobject_data_for_blueprint(bp)
    for h in handles:
        data = sub.k2_find_subobject_data_from_handle(h)
        name = sub.get_variable_name(data)
        unreal.log_warning(f"  Component handle: {name}")

if __name__ == "__main__":
    test_assign()
