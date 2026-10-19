"""
Update BP_Kabir_v05 to use SKM_Kabir_v05
"""
import unreal

def log(msg):
    unreal.log_warning(f"[BP_UPDATE] {msg}")

def main():
    skm = unreal.load_asset("/Game/Characters/Kabir_v05/SKM_Kabir_v05")
    bp = unreal.load_asset("/Game/Characters/Kabir/BP_Kabir_v05")
    if not skm or not bp:
        log("Failed to load SKM or BP")
        return
        
    gen_class = unreal.load_object(None, "/Game/Characters/Kabir/BP_Kabir_v05_C")
    if gen_class:
        cdo = unreal.get_default_object(gen_class)
        mesh_comp = cdo.get_editor_property("mesh")
        if mesh_comp:
            mesh_comp.set_skeletal_mesh_asset(skm)
            log(f"Assigned {skm.get_name()} to {mesh_comp.get_name()}")
            
    editor_asset_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    editor_asset_sub.save_loaded_asset(bp)
    log("Saved BP_Kabir_v05.")

if __name__ == "__main__":
    main()
