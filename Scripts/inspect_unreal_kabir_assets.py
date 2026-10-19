"""
PROJECT REVOLUTION — Inspect Existing Kabir Assets, IK Rigs, Retargeters, and Animations in UE5.5
"""

import unreal

def log(msg):
    unreal.log_warning(f"[KABIR_AUDIT] {msg}")

def main():
    log("=== INSPECTING KABIR & ANIMATION ASSETS IN UNREAL ===")
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    
    # 1. Check Kabir Assets
    kabir_assets = asset_registry.get_assets_by_path("/Game/Characters", recursive=True)
    log(f"Found {len(kabir_assets)} assets under /Game/Characters:")
    for a in kabir_assets:
        log(f"  [{a.asset_class_path.asset_name}] {a.package_name}")
        
    # 2. Check IK Rig & Retargeter Assets
    ik_assets = asset_registry.get_assets_by_class("IKRigDefinition")
    log(f"Found {len(ik_assets)} IK Rig definitions:")
    for a in ik_assets:
        log(f"  IK Rig: {a.package_name}")
        
    retarget_assets = asset_registry.get_assets_by_class("IKRetargeter")
    log(f"Found {len(retarget_assets)} IK Retargeters:")
    for a in retarget_assets:
        log(f"  Retargeter: {a.package_name}")
        
    # 3. Check Mannequin Animations
    anim_assets = asset_registry.get_assets_by_path("/Game/Characters/Mannequins/Animations", recursive=True)
    log(f"Found {len(anim_assets)} assets under /Game/Characters/Mannequins/Animations:")
    for a in anim_assets[:15]:
        log(f"  Anim: {a.package_name} ({a.asset_class_path.asset_name})")
        
    # 4. Check BP_Kabir or Hero Blueprint
    bp_assets = [a for a in kabir_assets if "Blueprint" in str(a.asset_class_path.asset_name)]
    log(f"Character Blueprints: {[str(a.package_name) for a in bp_assets]}")

if __name__ == "__main__":
    main()
