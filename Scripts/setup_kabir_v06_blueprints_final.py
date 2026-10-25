"""
PROJECT REVOLUTION — Kabir v06 Character Blueprints Setup & Finalization
Sets SkeletalMesh, relative transform offsets, and idle animation playback for all 3 variants.
Compiles and serializes the blueprints to disk.
"""

import sys
import unreal

def log(msg):
    unreal.log_warning(f"[BP_SETUP_FINAL] {msg}")

def main():
    log("================================================================================")
    log("  CONFIGURING ALL 3 KABIR v06 CHARACTER BLUEPRINTS (CHILD, TEEN, ADULT)")
    log("================================================================================")
    
    stages = [
        ("BP_Kabir_v06_Child_12", "/Game/Characters/Kabir_v06/SKM_Kabir_v06_Child_12", -60.0),
        ("BP_Kabir_v06_Teen_16",  "/Game/Characters/Kabir_v06/SKM_Kabir_v06_Teen_16",  -70.0),
        ("BP_Kabir_v06_Adult_25", "/Game/Characters/Kabir_v06/SKM_Kabir_v06_Adult_25", -76.0)
    ]
    
    idle_anim = unreal.load_asset("/Game/Characters/Kabir_v06/Animations/Anim_Kabir_v06_Idle")
    if not idle_anim:
        log("ERROR: Could not load Anim_Kabir_v06_Idle!")
        sys.exit(1)
        
    editor_asset_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    
    success_count = 0
    for bp_name, skm_path, mesh_z in stages:
        bp_path = f"/Game/Characters/Kabir_v06/{bp_name}"
        bp = unreal.load_asset(bp_path)
        skm = unreal.load_asset(skm_path)
        
        if not bp:
            log(f"ERROR: Missing Blueprint {bp_path}")
            continue
        if not skm:
            log(f"ERROR: Missing SkeletalMesh {skm_path}")
            continue
            
        gen_cls = bp.generated_class()
        if not gen_cls:
            log(f"ERROR: Generated class not found for {bp_name}")
            continue
            
        cdo = unreal.get_default_object(gen_cls)
        mesh_comp = cdo.get_editor_property("mesh")
        if not mesh_comp:
            log(f"ERROR: CharacterMesh not found on CDO of {bp_name}")
            continue
            
        # Assign Mesh and Transforms
        mesh_comp.set_skeletal_mesh_asset(skm)
        mesh_comp.set_editor_property("relative_location", unreal.Vector(0.0, 0.0, mesh_z))
        mesh_comp.set_editor_property("relative_rotation", unreal.Rotator(0.0, -90.0, 0.0))
        mesh_comp.set_editor_property("relative_scale3d", unreal.Vector(1.0, 1.0, 1.0))
        
        # Configure Animation Playback
        mesh_comp.set_editor_property("animation_mode", unreal.AnimationMode.ANIMATION_SINGLE_NODE)
        mesh_comp.set_editor_property("animation_data", unreal.SingleAnimationPlayData(
            anim_to_play=idle_anim,
            saved_playing=True,
            saved_looping=True
        ))
        
        # Compile and save
        unreal.BlueprintEditorLibrary.compile_blueprint(bp)
        editor_asset_sub.save_loaded_asset(bp)
        
        log(f"  [SUCCESS] {bp_name} configured -> {skm.get_name()} (Z={mesh_z}) + Anim_Kabir_v06_Idle")
        success_count += 1
        
    log("================================================================================")
    if success_count == len(stages):
        log("  SUCCESS: ALL 3 KABIR v06 CHARACTER BLUEPRINTS FULLY CONFIGURED & SERIALIZED")
        log("================================================================================")
        sys.exit(0)
    else:
        log(f"  FAILED: Only {success_count}/{len(stages)} blueprints configured")
        log("================================================================================")
        sys.exit(1)

if __name__ == "__main__":
    main()
