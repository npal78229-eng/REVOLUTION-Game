"""
PROJECT REVOLUTION — Kabir v06 Playable Blueprint Creation
Creates 3 playable character blueprints in /Game/Characters/Kabir_v06/:
- BP_Kabir_v06_Child_12
- BP_Kabir_v06_Teen_16
- BP_Kabir_v06_Adult_25
Configured with the respective SKM meshes, authentic materials, and Enhanced Input.
"""

import sys
import unreal

def log(msg):
    unreal.log_warning(f"[BP_KABIR_v06] {msg}")

def main():
    log("================================================================================")
    log("  CREATING PLAYABLE BLUEPRINTS FOR KABIR v06 (CHILD, TEEN, ADULT)")
    log("================================================================================")
    
    editor_asset_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    source_bp = "/Game/Characters/Kabir/BP_Kabir_v05"
    dest_dir = "/Game/Characters/Kabir_v06"
    
    stages = [
        ("BP_Kabir_v06_Child_12", "/Game/Characters/Kabir_v06/SKM_Kabir_v06_Child_12", -60.0, 1.42/1.76),
        ("BP_Kabir_v06_Teen_16",  "/Game/Characters/Kabir_v06/SKM_Kabir_v06_Teen_16",  -70.0, 1.68/1.76),
        ("BP_Kabir_v06_Adult_25", "/Game/Characters/Kabir_v06/SKM_Kabir_v06_Adult_25", -76.0, 1.0)
    ]
    
    created_count = 0
    for bp_name, skm_path, mesh_z, scale in stages:
        dest_bp_path = f"{dest_dir}/{bp_name}"
        
        # Duplicate from base BP to inherit all Enhanced Input, Foley, and Camera setup
        if not editor_asset_sub.does_asset_exist(dest_bp_path):
            duplicated = editor_asset_sub.duplicate_asset(source_bp, dest_bp_path)
            if not duplicated:
                log(f"Failed to duplicate {source_bp} -> {dest_bp_path}")
                continue
            log(f"Created Character Blueprint: {dest_bp_path}")
        else:
            log(f"Character Blueprint already exists: {dest_bp_path}")
            
        bp_asset = unreal.load_asset(dest_bp_path)
        skm_asset = unreal.load_asset(skm_path)
        
        if bp_asset and skm_asset:
            gen_class = unreal.load_object(None, f"{dest_bp_path}_C")
            if gen_class:
                cdo = unreal.get_default_object(gen_class)
                mesh_comp = cdo.get_editor_property("mesh")
                if mesh_comp:
                    mesh_comp.set_skeletal_mesh_asset(skm_asset)
                    mesh_comp.set_editor_property("relative_location", unreal.Vector(0.0, 0.0, mesh_z))
                    mesh_comp.set_editor_property("relative_rotation", unreal.Rotator(0.0, -90.0, 0.0))
                    mesh_comp.set_editor_property("relative_scale3d", unreal.Vector(1.0, 1.0, 1.0))
                    log(f"  Assigned {skm_asset.get_name()} to {bp_name} (Z={mesh_z})")
                    
            editor_asset_sub.save_loaded_asset(bp_asset)
            created_count += 1
            
    log(f"Summary: Successfully configured {created_count}/{len(stages)} Playable Blueprints.")
    if created_count == len(stages):
        log("SUCCESS: All 3 Kabir v06 Character Blueprints operational!")
        sys.exit(0)
    else:
        log("Incomplete blueprint setup.")
        sys.exit(1)

if __name__ == "__main__":
    main()
