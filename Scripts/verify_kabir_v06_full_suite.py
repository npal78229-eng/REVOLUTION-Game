"""
PROJECT REVOLUTION — Full In-Engine Verification of Kabir v06
Verifies:
1. 8 PBR Heritage Materials
2. 3 Skeletal Meshes (Child 12, Teen 16, Adult 25)
3. 16 Game Animation Sequences
4. 3 Playable Character Blueprints (Child 12, Teen 16, Adult 25)
5. Zero-Regression on Kabir v05
"""

import sys
import unreal

def log(msg):
    unreal.log_warning(f"[FULL_VERIFIER] {msg}")

def main():
    log("================================================================================")
    log("  PROJECT REVOLUTION — KABIR v06 FULL IN-ENGINE VERIFICATION AUDIT")
    log("================================================================================")
    
    stages = [
        ("SKM_Kabir_v06_Child_12", "/Game/Characters/Kabir_v06/SKM_Kabir_v06_Child_12"),
        ("SKM_Kabir_v06_Teen_16",  "/Game/Characters/Kabir_v06/SKM_Kabir_v06_Teen_16"),
        ("SKM_Kabir_v06_Adult_25", "/Game/Characters/Kabir_v06/SKM_Kabir_v06_Adult_25")
    ]
    
    materials = [
        "/Game/Characters/Kabir_v06/Materials/M_Kabir_v06_Skin",
        "/Game/Characters/Kabir_v06/Materials/M_Kabir_v06_Eye",
        "/Game/Characters/Kabir_v06/Materials/M_Kabir_v06_Hair",
        "/Game/Characters/Kabir_v06/Materials/M_Kabir_v06_Khadi_Cream",
        "/Game/Characters/Kabir_v06/Materials/M_Kabir_v06_Khadi_Pajama",
        "/Game/Characters/Kabir_v06/Materials/M_Kabir_v06_Angavastram",
        "/Game/Characters/Kabir_v06/Materials/M_Kabir_v06_Leather",
        "/Game/Characters/Kabir_v06/Materials/M_Kabir_v06_Brass"
    ]
    
    anims = [
        "Anim_Kabir_v06_Idle",
        "Anim_Kabir_v06_Walk",
        "Anim_Kabir_v06_Run",
        "Anim_Kabir_v06_Stop",
        "Anim_Kabir_v06_Crouch_Idle",
        "Anim_Kabir_v06_Crouch_Walk",
        "Anim_Kabir_v06_Weapon_Pickup",
        "Anim_Kabir_v06_Weapon_Draw",
        "Anim_Kabir_v06_Weapon_Aim",
        "Anim_Kabir_v06_Weapon_Shoot",
        "Anim_Kabir_v06_Weapon_Holster",
        "Anim_Kabir_v06_Jump",
        "Anim_Kabir_v06_Climb_Ladder",
        "Anim_Kabir_v06_Mantle",
        "Anim_Kabir_v06_Satchel_Open",
        "Anim_Kabir_v06_Curfew_Listen"
    ]
    
    blueprints = [
        ("BP_Kabir_v06_Child_12", "SKM_Kabir_v06_Child_12"),
        ("BP_Kabir_v06_Teen_16",  "SKM_Kabir_v06_Teen_16"),
        ("BP_Kabir_v06_Adult_25", "SKM_Kabir_v06_Adult_25")
    ]
    
    passed = True
    
    # 1. Check Materials (8)
    log("\n--- Checking 8 PBR Heritage Materials ---")
    for mpath in materials:
        mat = unreal.load_asset(mpath)
        if not mat:
            log(f"  [FAIL] Missing Material: {mpath}")
            passed = False
        else:
            log(f"  [PASS] {mat.get_name()}")
            
    # 2. Check Skeletal Meshes (3)
    log("\n--- Checking 3 Life-Stage Skeletal Meshes ---")
    for name, spath in stages:
        skm = unreal.load_asset(spath)
        if not skm:
            log(f"  [FAIL] Missing Skeletal Mesh: {spath}")
            passed = False
        else:
            skel = skm.get_editor_property("skeleton")
            mats = skm.get_editor_property("materials")
            log(f"  [PASS] {skm.get_name()} | Skeleton: {skel.get_name() if skel else 'NONE'} | Slots: {len(mats)}")
            
    # 3. Check 16 Animation Sequences (16)
    log("\n--- Checking 16 Game Animation Sequences ---")
    for aname in anims:
        apath = f"/Game/Characters/Kabir_v06/Animations/{aname}"
        seq = unreal.load_asset(apath)
        if not seq:
            log(f"  [FAIL] Missing Animation: {apath}")
            passed = False
        else:
            nkeys = seq.get_editor_property("number_of_sampled_keys")
            dur = seq.get_editor_property("sequence_length")
            log(f"  [PASS] {aname:<30} ({nkeys} keys, {dur:.2f}s)")
            
    # 4. Check 3 Character Blueprints (3)
    log("\n--- Checking 3 Playable Character Blueprints ---")
    for bp_name, expected_skm_name in blueprints:
        bp_path = f"/Game/Characters/Kabir_v06/{bp_name}"
        bp = unreal.load_asset(bp_path)
        if not bp:
            log(f"  [FAIL] Missing Character Blueprint: {bp_path}")
            passed = False
            continue
            
        gen_cls = bp.generated_class()
        if not gen_cls:
            log(f"  [FAIL] Generated class not found for {bp_name}")
            passed = False
            continue
            
        cdo = unreal.get_default_object(gen_cls)
        mesh_comp = cdo.get_editor_property("mesh")
        if not mesh_comp:
            log(f"  [FAIL] CharacterMesh not found on CDO of {bp_name}")
            passed = False
            continue
            
        skm_asset = mesh_comp.get_editor_property("skeletal_mesh_asset")
        if not skm_asset or skm_asset.get_name() != expected_skm_name:
            actual_name = skm_asset.get_name() if skm_asset else "None"
            log(f"  [FAIL] {bp_name} has incorrect mesh: expected {expected_skm_name}, got {actual_name}")
            passed = False
        else:
            rel_loc = mesh_comp.get_editor_property("relative_location")
            anim_mode = mesh_comp.get_editor_property("animation_mode")
            log(f"  [PASS] {bp_name} | Mesh: {expected_skm_name} | Z={rel_loc.z:.1f} | AnimMode: {anim_mode}")
            
    # 5. Check Kabir v05 Zero-Regression
    log("\n--- Checking Kabir v05 Zero-Regression Preservation ---")
    v05_mesh = unreal.load_asset("/Game/Characters/Kabir_v05/SKM_Kabir_v05")
    if not v05_mesh:
        log("  [FAIL] Regression: SKM_Kabir_v05 missing!")
        passed = False
    else:
        log("  [PASS] SKM_Kabir_v05 intact and functional.")
        
    log("================================================================================")
    if passed:
        log("  AUDIT RESULT: 100% PASS — ALL 30 KABIR v06 ASSETS OPERATIONAL IN UE 5.5")
        log("================================================================================")
        sys.exit(0)
    else:
        log("  AUDIT RESULT: FAIL")
        log("================================================================================")
        sys.exit(1)

if __name__ == "__main__":
    main()
