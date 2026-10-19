"""
PROJECT REVOLUTION — Inspect Material Slots & Bone Hierarchy on SKM_Kabir_v05
"""

import unreal

def log(msg):
    unreal.log_warning(f"[KABIR_AUDIT] {msg}")

def main():
    skm = unreal.load_asset("/Game/Characters/Kabir_v05/SKM_Kabir_v05")
    if not skm:
        log("ERROR: Could not load /Game/Characters/Kabir_v05/SKM_Kabir_v05")
        return
        
    log(f"Inspecting Skeletal Mesh: {skm.get_name()}")
    materials = skm.get_editor_property("materials")
    log(f"Total Material Slots: {len(materials)}")
    for i, m in enumerate(materials):
        slot_name = m.material_slot_name
        mat_int = m.material_interface
        log(f"  Slot [{i}]: {slot_name} -> {mat_int.get_name() if mat_int else 'None'}")
        
    skeleton = skm.get_editor_property("skeleton")
    log(f"Skeleton: {skeleton.get_name() if skeleton else 'None'}")
    
    # Check morph targets
    morph_targets = skm.get_editor_property("morph_targets")
    log(f"Morph Targets count: {len(morph_targets)}")
    for mt in morph_targets:
        log(f"  Morph Target: {mt.get_name()}")

if __name__ == "__main__":
    main()
