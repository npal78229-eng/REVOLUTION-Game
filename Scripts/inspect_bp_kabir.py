import unreal

def inspect_bp_kabir():
    bp_path = "/Game/Characters/Kabir/BP_Kabir"
    bp = unreal.load_asset(bp_path)
    if not bp:
        unreal.log_error(f"Could not load {bp_path}")
        return

    unreal.log_warning(f"Loaded {bp.get_name()}, Class: {bp.get_class().get_name()}")
    gen_class = bp.generated_class()
    if gen_class:
        unreal.log_warning(f"Generated class: {gen_class.get_name()}")
        cdo = unreal.get_default_object(gen_class)
        if cdo:
            mesh = cdo.get_editor_property("mesh")
            if mesh:
                sk_mesh = mesh.get_editor_property("skeletal_mesh_asset")
                unreal.log_warning(f"CDO SkeletalMesh: {sk_mesh.get_name() if sk_mesh else 'None'}")
                anim_class = mesh.get_editor_property("anim_class")
                unreal.log_warning(f"CDO AnimClass: {anim_class.get_name() if anim_class else 'None'}")

if __name__ == "__main__":
    inspect_bp_kabir()
