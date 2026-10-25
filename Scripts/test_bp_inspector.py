"""
Test script to inspect Blueprint generated class and CDO
"""
import unreal

bp_path = "/Game/Characters/Kabir_v06/BP_Kabir_v06_Adult_25"
bp = unreal.load_asset(bp_path)
unreal.log_warning(f"Loaded BP: {bp}")
if bp:
    # Check generated class
    gen_cls = bp.generated_class() if hasattr(bp, 'generated_class') else None
    unreal.log_warning(f"bp.generated_class(): {gen_cls}")
    
    # Check load_class
    cls2 = unreal.load_class(None, f"{bp_path}.BP_Kabir_v06_Adult_25_C")
    unreal.log_warning(f"load_class: {cls2}")
    
    target_cls = gen_cls or cls2
    if target_cls:
        cdo = unreal.get_default_object(target_cls)
        unreal.log_warning(f"CDO: {cdo}")
        mesh = cdo.get_editor_property("mesh") if hasattr(cdo, 'get_editor_property') else None
        unreal.log_warning(f"Mesh property: {mesh}")
        if mesh:
            skm = mesh.get_editor_property("skeletal_mesh_asset")
            unreal.log_warning(f"Current Skeletal Mesh on CDO: {skm}")
