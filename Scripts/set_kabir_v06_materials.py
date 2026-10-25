"""
PROJECT REVOLUTION — Set Material Slots on Kabir v06 Skeletal Meshes
Uses unreal.SkeletalMaterial constructors to cleanly assign PBR materials to slots.
"""

import unreal

def log(msg):
    unreal.log_warning(f"[SET_MATERIALS] {msg}")

def main():
    editor_asset_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    
    mats_dict = {
        "skin": unreal.load_asset("/Game/Characters/Kabir_v06/Materials/M_Kabir_v06_Skin"),
        "eye": unreal.load_asset("/Game/Characters/Kabir_v06/Materials/M_Kabir_v06_Eye"),
        "hair": unreal.load_asset("/Game/Characters/Kabir_v06/Materials/M_Kabir_v06_Hair"),
        "cream": unreal.load_asset("/Game/Characters/Kabir_v06/Materials/M_Kabir_v06_Khadi_Cream"),
        "pajama": unreal.load_asset("/Game/Characters/Kabir_v06/Materials/M_Kabir_v06_Khadi_Pajama"),
        "angavastram": unreal.load_asset("/Game/Characters/Kabir_v06/Materials/M_Kabir_v06_Angavastram"),
        "leather": unreal.load_asset("/Game/Characters/Kabir_v06/Materials/M_Kabir_v06_Leather"),
        "brass": unreal.load_asset("/Game/Characters/Kabir_v06/Materials/M_Kabir_v06_Brass"),
    }
    
    for k, v in mats_dict.items():
        if not v:
            log(f"ERROR: Could not load material for key {k}")
            return
            
    stages = ["SKM_Kabir_v06_Child_12", "SKM_Kabir_v06_Teen_16", "SKM_Kabir_v06_Adult_25"]
    for s in stages:
        skm = unreal.load_asset(f"/Game/Characters/Kabir_v06/{s}")
        if not skm:
            log(f"ERROR: Could not load {s}")
            continue
            
        mesh_mats = skm.get_editor_property("materials")
        new_mats = []
        log(f"Processing {s} ({len(mesh_mats)} slots):")
        
        for i, slot in enumerate(mesh_mats):
            sname = str(slot.material_slot_name).lower()
            target = mats_dict["cream"]
            
            if "skin" in sname:
                target = mats_dict["skin"]
            elif "eye" in sname:
                target = mats_dict["eye"]
            elif "hair" in sname:
                target = mats_dict["hair"]
            elif "angavastram" in sname:
                target = mats_dict["angavastram"]
            elif "leather" in sname:
                target = mats_dict["leather"]
            elif "brass" in sname:
                target = mats_dict["brass"]
            elif "pajama" in sname or "dhoti" in sname:
                target = mats_dict["pajama"]
                
            new_slot = unreal.SkeletalMaterial(material_interface=target, material_slot_name=slot.material_slot_name)
            new_mats.append(new_slot)
            log(f"  Slot [{i}] '{slot.material_slot_name}' -> {target.get_name()}")
            
        skm.set_editor_property("materials", new_mats)
        editor_asset_sub.save_loaded_asset(skm)
        log(f"Saved {s} with updated materials.")
        
    log("All Kabir v06 materials assigned successfully.")

if __name__ == "__main__":
    main()
