import unreal
import json
import os

def verify_rdr2_smoke():
    unreal.log_warning("=== REVOLUTION: Verifying RDR2 Smoke System Integration ===")
    
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)
    
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = actor_sub.get_all_level_actors()
    
    results = {
        "milestone": "RDR2_SMOKE_INTEGRATION",
        "status": "IN_PROGRESS",
        "verified_actors": {},
        "materials": {},
        "textures": {}
    }
    
    # 1. Verify Textures
    tex_puff = unreal.load_asset("/Game/VFX/Smoke/Textures/T_Smoke_Pyroclastic_Puff")
    tex_flow = unreal.load_asset("/Game/VFX/Smoke/Textures/T_Smoke_CurlNoise_Flow")
    results["textures"]["T_Smoke_Pyroclastic_Puff"] = tex_puff is not None
    results["textures"]["T_Smoke_CurlNoise_Flow"] = tex_flow is not None
    
    # 2. Verify Materials
    mat_master = unreal.load_asset("/Game/VFX/Smoke/Materials/M_RDR2_Pyroclastic_Smoke")
    mat_chulha = unreal.load_asset("/Game/VFX/Smoke/Materials/MI_Smoke_Chulha_Campfire")
    mat_chimney = unreal.load_asset("/Game/VFX/Smoke/Materials/MI_Smoke_Haveli_Chimney")
    mat_muzzle = unreal.load_asset("/Game/VFX/Smoke/Materials/MI_Smoke_Gunpowder_Muzzle")
    mat_steam = unreal.load_asset("/Game/VFX/Smoke/Materials/MI_Smoke_Locomotive_Steam")
    mat_haze = unreal.load_asset("/Game/VFX/Smoke/Materials/M_RDR2_HeatHaze")
    
    results["materials"]["M_RDR2_Pyroclastic_Smoke"] = mat_master is not None
    results["materials"]["MI_Smoke_Chulha_Campfire"] = mat_chulha is not None
    results["materials"]["MI_Smoke_Haveli_Chimney"] = mat_chimney is not None
    results["materials"]["MI_Smoke_Gunpowder_Muzzle"] = mat_muzzle is not None
    results["materials"]["MI_Smoke_Locomotive_Steam"] = mat_steam is not None
    results["materials"]["M_RDR2_HeatHaze"] = mat_haze is not None
    
    # 3. Verify Placed Actors in L_Validation_Gym
    labels_to_find = [
        "BP_Chulha_Fireplace_RDR2",
        "Light_Chulha_Flame_Bounce",
        "Smoke_Plume_Chulha",
        "HeatHaze_Chulha",
        "BP_Haveli_Rooftop_Chimney_RDR2",
        "Smoke_Plume_Rooftop_Chimney",
        "Locomotive_Steam_Pressure_Relief_Valve"
    ]
    
    found_count = 0
    for label in labels_to_find:
        match = [a for a in actors if a.get_actor_label() == label]
        if match:
            act = match[0]
            loc = act.get_actor_location()
            results["verified_actors"][label] = {
                "found": True,
                "location": f"X={loc.x:.1f}, Y={loc.y:.1f}, Z={loc.z:.1f}"
            }
            found_count += 1
            unreal.log_warning(f"Verified Actor: {label} at {results['verified_actors'][label]['location']}")
        else:
            results["verified_actors"][label] = {"found": False}
            unreal.log_error(f"Missing Actor: {label}")

    all_textures_ok = all(results["textures"].values())
    all_materials_ok = all(results["materials"].values())
    all_actors_ok = found_count == len(labels_to_find)
    
    if all_textures_ok and all_materials_ok and all_actors_ok:
        results["status"] = "PASS"
        unreal.log_warning("=== RDR2 SMOKE SYSTEM INTEGRATION VERIFIED: PASS ===")
    else:
        results["status"] = "FAIL"
        unreal.log_error("=== RDR2 SMOKE SYSTEM INTEGRATION VERIFIED: FAIL ===")

    # Trigger Inspection Screenshot request
    screenshot_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Tests\Screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshot_dir, "RDR2_01_Courtyard_Smoke_Chulha.png")
    
    # Save verification JSON
    json_path = r"C:\Users\npal7\PROJECT\REVOLUTION\Tests\RDR2_SMOKE_VERIFICATION.json"
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)
    unreal.log_warning(f"Saved verification metrics to {json_path}")

if __name__ == "__main__":
    verify_rdr2_smoke()
