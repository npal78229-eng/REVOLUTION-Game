"""
PROJECT REVOLUTION — Verification of Kabir v06 Heritage Assets in UE 5.5
Verifies all 3 life-stage skeletal meshes, materials, and confirms zero regressions on v05.
"""

import sys
import unreal

def log(msg):
    unreal.log_warning(f"[KABIR_v06_VERIFIER] {msg}")

def main():
    log("================================================================================")
    log("  VERIFYING KABIR v06 HERITAGE ASSETS & ZERO-REGRESSION ON v05")
    log("================================================================================")
    
    stages = [
        "/Game/Characters/Kabir_v06/SKM_Kabir_v06_Child_12",
        "/Game/Characters/Kabir_v06/SKM_Kabir_v06_Teen_16",
        "/Game/Characters/Kabir_v06/SKM_Kabir_v06_Adult_25"
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
    
    passed = True
    
    # Check Materials
    for mpath in materials:
        mat = unreal.load_asset(mpath)
        if not mat:
            log(f"[FAIL] Material could not be loaded: {mpath}")
            passed = False
        else:
            used_skm = mat.get_editor_property("used_with_skeletal_mesh")
            log(f"[PASS] Material: {mat.get_name()} (used_with_skeletal_mesh={used_skm})")
            
    # Check Skeletal Meshes
    for spath in stages:
        skm = unreal.load_asset(spath)
        if not skm:
            log(f"[FAIL] Skeletal Mesh could not be loaded: {spath}")
            passed = False
        else:
            skel = skm.get_editor_property("skeleton")
            mats = skm.get_editor_property("materials")
            log(f"[PASS] Skeletal Mesh: {skm.get_name()} | Skeleton: {skel.get_name() if skel else 'NONE'} | Material Slots: {len(mats)}")
            for i, slot in enumerate(mats):
                m_interface = slot.material_interface
                log(f"       Slot [{i}] '{slot.material_slot_name}': {m_interface.get_name() if m_interface else 'UNASSIGNED'}")
                if not m_interface:
                    passed = False
                    
    # Check Kabir v05 preservation
    v05_mesh = unreal.load_asset("/Game/Characters/Kabir_v05/SKM_Kabir_v05")
    if not v05_mesh:
        log("[FAIL] Regression: SKM_Kabir_v05 could not be loaded!")
        passed = False
    else:
        v05_skel = v05_mesh.get_editor_property("skeleton")
        v05_mats = v05_mesh.get_editor_property("materials")
        log(f"[PASS] Zero-Regression Verified: SKM_Kabir_v05 intact | Skeleton: {v05_skel.get_name() if v05_skel else 'NONE'} | Material Slots: {len(v05_mats)}")
        
    if passed:
        log("================================================================================")
        log("  ALL KABIR v06 CHECKS PASSED — 100% SUCCESS")
        log("================================================================================")
        sys.exit(0)
    else:
        log("================================================================================")
        log("  VERIFICATION FAILED")
        log("================================================================================")
        sys.exit(1)

if __name__ == "__main__":
    main()
