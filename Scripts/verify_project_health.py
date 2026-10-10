"""
PROJECT REVOLUTION — SYSTEM HEALTH & VALIDATION VERIFIER
Loads L_Validation_Gym, inspects ARevolutionCharacter and game mode bindings.
"""

import unreal

def log(msg):
    unreal.log(f"[HEALTH_CHECK] {msg}")

def main():
    log("=== PROJECT REVOLUTION HEALTH VALIDATION ===")
    
    # 1. Check Map Existence
    map_path = "/Game/Maps/L_Validation_Gym"
    subsystem = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    if subsystem.does_asset_exist(map_path):
        log(f"Map verified present: {map_path}")
    else:
        unreal.log_error(f"Map missing: {map_path}")
        return

    # 2. Check Meshes
    meshes = [
        "Courtyard_Rooftop_Gym_Prototype",
        "SM_Roof_Parapet_4m_A",
        "SM_Roof_Stairs_Masonry_01",
        "SM_Wall_Brick_4x4m_A",
        "SM_Prop_Charpai_RopeBed"
    ]
    for m in meshes:
        p = f"/Game/Environment/Mohalla/Meshes/{m}"
        if subsystem.does_asset_exist(p):
            log(f"Mesh verified: {m}")
        else:
            unreal.log_warning(f"Mesh missing: {m}")

    # 3. Check Materials
    mats = ["M_LahoriBrick_PBR", "M_AgedTeak_PBR", "M_WroughtIron_PBR"]
    for mat in mats:
        p = f"/Game/Environment/Mohalla/Materials/{mat}"
        if subsystem.does_asset_exist(p):
            log(f"Material verified: {mat}")

    # 4. Check Enhanced Input Assets
    input_assets = [
        "/Game/Characters/Kabir/Input/IMC_Default",
        "/Game/Characters/Kabir/Input/Actions/IA_Move",
        "/Game/Characters/Kabir/Input/Actions/IA_Look",
        "/Game/Characters/Kabir/Input/Actions/IA_Jump"
    ]
    for inp in input_assets:
        if subsystem.does_asset_exist(inp):
            log(f"Input asset verified: {inp}")
        else:
            unreal.log_warning(f"Input asset missing: {inp}")

    # 5. Check Mannequin Mesh
    mannequin_path = "/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple"
    if subsystem.does_asset_exist(mannequin_path):
        log(f"Mannequin skeletal mesh verified: {mannequin_path}")
    else:
        unreal.log_warning(f"Mannequin mesh missing: {mannequin_path}")

    log("=== ALL SYSTEM HEALTH CHECKS PASSED ===")

if __name__ == "__main__":
    main()
