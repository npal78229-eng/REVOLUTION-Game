"""
PROJECT REVOLUTION — Set Material Slots on Kabir v06 Skeletal Meshes
Ensures each SkeletalMesh has the corresponding M_Kabir_v06_* material assigned to its material slots.
"""

import unreal

def log(msg):
    unreal.log_warning(f"[SET_MATERIALS] {msg}")

def assign_materials_to_skm(skm_path):
    editor_asset_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    skm = unreal.load_asset(skm_path)
    if not skm:
        log(f"Failed to load {skm_path}")
        return False
        
    mats_dict = {
        "skin": unreal.load_asset("/Game/Characters/Kabir_v06/Materials/M_Kabir_v06_Skin"),
        "eye": unreal.load_asset("/Game/Characters/Kabir_v06/Materials/M_Kabir_v06_Eye"),
        "hair": unreal.load_asset("/Game/Characters/Kabir_v06/Materials/M_Kabir_v06_Hair"),
        "khadi_cream": unreal.load_asset("/Game/Characters/Kabir_v06/Materials/M_Kabir_v06_Khadi_Cream"),
        "khadi_pajama": unreal.load_asset("/Game/Characters/Kabir_v06/Materials/M_Kabir_v06_Khadi_Pajama"),
        "angavastram": unreal.load_asset("/Game/Characters/Kabir_v06/Materials/M_Kabir_v06_Angavastram"),
        "leather": unreal.load_asset("/Game/Characters/Kabir_v06/Materials/M_Kabir_v06_Leather"),
        "brass": unreal.load_asset("/Game/Characters/Kabir_v06/Materials/M_Kabir_v06_Brass"),
    }
    
    mesh_mats = skm.get_editor_property("materials")
    log(f"Assigning materials for {skm.get_name()} ({len(mesh_mats)} slots)")
    
    for i, slot in enumerate(mesh_mats):
        sname = str(slot.material_slot_name).lower()
        target_mat = None
        
        if "skin" in sname:
            target_mat = mats_dict["skin"]
        elif "eye" in sname:
            target_mat = mats_dict["eye"]
        elif "hair" in sname:
            target_mat = mats_dict["hair"]
        elif "angavastram" in sname:
            target_mat = mats_dict["angavastram"]
        elif "leather" in sname or "jutti" in sname or "satchel" in sname:
            target_mat = mats_dict["leather"]
        elif "brass" in sname:
            target_mat = mats_dict["brass"]
        elif "cream" in sname or "kurta" in sname:
            target_mat = mats_dict["khadi_cream"]
        elif "pajama" in sname or "dhoti" in sname or "salwar" in sname:
            target_mat = mats_dict["khadi_pajama"]
        else:
            target_mat = mats_dict["khadi_cream"]
            
        if target_mat:
            skm.set_material(i, target_mat)
            log(f"  Slot [{i}] '{slot.material_slot_name}' -> {target_mat.get_name()}")
            
    editor_asset_sub.save_loaded_asset(skm)
    return True

def main():
    stages = [
        "/Game/Characters/Kabir_v06/SKM_Kabir_v06_Child_12",
        "/Game/Characters/Kabir_v06/SKM_Kabir_v06_Teen_16",
        "/Game/Characters/Kabir_v06/SKM_Kabir_v06_Adult_25"
    ]
    for s in stages:
        assign_materials_to_skm(s)

if __name__ == "__main__":
    main()
