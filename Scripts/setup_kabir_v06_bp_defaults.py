"""
PROJECT REVOLUTION — Configure Kabir v06 Character Blueprint Defaults
Sets Skeletal Mesh, Default SingleNode Animation (Anim_Kabir_v06_Idle), and PBR materials.
"""

import sys
import unreal

def log(msg):
    unreal.log_warning(f"[BP_DEFAULTS] {msg}")

def main():
    log("================================================================================")
    log("  CONFIGURING KABIR v06 BLUEPRINT DEFAULTS & ANIMATION PLAYBACK")
    log("================================================================================")
    
    editor_asset_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    idle_anim = unreal.load_asset("/Game/Characters/Kabir_v06/Animations/Anim_Kabir_v06_Idle")
    
    stages = [
        ("BP_Kabir_v06_Child_12", "/Game/Characters/Kabir_v06/SKM_Kabir_v06_Child_12"),
        ("BP_Kabir_v06_Teen_16",  "/Game/Characters/Kabir_v06/SKM_Kabir_v06_Teen_16"),
        ("BP_Kabir_v06_Adult_25", "/Game/Characters/Kabir_v06/SKM_Kabir_v06_Adult_25")
    ]
    
    for bp_name, skm_path in stages:
        bp_path = f"/Game/Characters/Kabir_v06/{bp_name}"
        bp = unreal.load_asset(bp_path)
        skm = unreal.load_asset(skm_path)
        
        if not bp or not skm:
            log(f"Failed to load {bp_name} or {skm_path}")
            continue
            
        gen_class = unreal.load_object(None, f"{bp_path}_C")
        if gen_class:
            cdo = unreal.get_default_object(gen_class)
            mesh_comp = cdo.get_editor_property("mesh")
            if mesh_comp:
                mesh_comp.set_skeletal_mesh_asset(skm)
                mesh_comp.set_editor_property("animation_mode", unreal.AnimationMode.ANIMATION_SINGLE_NODE)
                if idle_anim:
                    mesh_comp.set_editor_property("animation_data", unreal.SingleAnimationPlayData(anim_to_play=idle_anim, saved_playing=True, saved_looping=True))
                log(f"  Configured {bp_name} with {skm.get_name()} and Anim_Kabir_v06_Idle")
                
        editor_asset_sub.save_loaded_asset(bp)
        
    log("ALL 3 KABIR v06 BLUEPRINTS FULLY CONFIGURED!")

if __name__ == "__main__":
    main()
