"""
Test setting CDO and compiling with unreal.BlueprintEditorLibrary.compile_blueprint
"""
import sys
import unreal

bp_path = "/Game/Characters/Kabir_v06/BP_Kabir_v06_Adult_25"
skm_path = "/Game/Characters/Kabir_v06/SKM_Kabir_v06_Adult_25"

bp = unreal.load_asset(bp_path)
skm = unreal.load_asset(skm_path)

gen_cls = bp.generated_class()
cdo = unreal.get_default_object(gen_cls)
mesh = cdo.get_editor_property("mesh")

# Configure mesh
mesh.set_skeletal_mesh_asset(skm)
mesh.set_editor_property("relative_location", unreal.Vector(0.0, 0.0, -76.0))
mesh.set_editor_property("relative_rotation", unreal.Rotator(0.0, -90.0, 0.0))

unreal.BlueprintEditorLibrary.compile_blueprint(bp)
sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
sub.save_loaded_asset(bp)

unreal.log_warning(f"SUCCESS: Adult_25 compiled with mesh {skm.get_name()}")
