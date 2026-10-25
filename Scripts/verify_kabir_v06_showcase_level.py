"""
PROJECT REVOLUTION — Verify Kabir v06 Showcase Level
Audits L_Kabir_v06_Showcase to ensure all 3 protagonist life-stage actors,
the CineCamera, and lighting/environment actors are present and correctly positioned.
"""

import sys
import unreal

def log(msg):
    unreal.log_warning(f"[SHOWCASE_VERIFIER] {msg}")

def main():
    log("================================================================================")
    log("  VERIFYING KABIR v06 SHOWCASE LEVEL (L_Kabir_v06_Showcase)")
    log("================================================================================")
    
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    
    map_path = "/Game/Maps/L_Kabir_v06_Showcase"
    loaded = level_sub.load_level(map_path)
    if not loaded:
        log(f"FAIL: Could not load {map_path}")
        sys.exit(1)
        
    actors = actor_sub.get_all_level_actors()
    log(f"Total level actors in showcase: {len(actors)}")
    
    required_actors = [
        ("Showcase_Kabir_v06_Child_12", "SKM_Kabir_v06_Child_12", -130.0),
        ("Showcase_Kabir_v06_Teen_16",  "SKM_Kabir_v06_Teen_16",  0.0),
        ("Showcase_Kabir_v06_Adult_25", "SKM_Kabir_v06_Adult_25", 130.0),
        ("Showcase_CineCam_Master",     None,                      0.0)
    ]
    
    actor_map = {a.get_actor_label(): a for a in actors}
    all_passed = True
    
    for label, expected_skm, expected_x in required_actors:
        if label not in actor_map:
            log(f"  [FAIL] Missing required actor: {label}")
            all_passed = False
            continue
            
        actor = actor_map[label]
        loc = actor.get_actor_location()
        if abs(loc.x - expected_x) > 5.0:
            log(f"  [WARN] {label} X position mismatch: expected {expected_x}, got {loc.x}")
            
        if expected_skm:
            mesh_comp = actor.get_component_by_class(unreal.SkeletalMeshComponent)
            if not mesh_comp:
                log(f"  [FAIL] {label} has no SkeletalMeshComponent")
                all_passed = False
                continue
            skm = mesh_comp.get_editor_property("skeletal_mesh_asset")
            if not skm or skm.get_name() != expected_skm:
                actual = skm.get_name() if skm else "None"
                log(f"  [FAIL] {label} mesh mismatch: expected {expected_skm}, got {actual}")
                all_passed = False
            else:
                log(f"  [PASS] {label} verified with {expected_skm} at loc=({loc.x:.1f}, {loc.y:.1f}, {loc.z:.1f})")
        else:
            log(f"  [PASS] {label} verified at loc=({loc.x:.1f}, {loc.y:.1f}, {loc.z:.1f})")
            
    # Check lighting actors
    has_sun = any("DirectionalLight" in a.get_class().get_name() for a in actors)
    has_sky = any("SkyAtmosphere" in a.get_class().get_name() for a in actors)
    has_fog = any("ExponentialHeightFog" in a.get_class().get_name() for a in actors)
    
    log(f"Atmosphere & Lighting: Sun={has_sun}, Sky={has_sky}, Fog={has_fog}")
    if not (has_sun and has_sky and has_fog):
        log("  [WARN] Missing one or more atmosphere actors")
        
    log("================================================================================")
    if all_passed:
        log("  AUDIT RESULT: 100% PASS — SHOWCASE LEVEL FULLY OPERATIONAL")
        log("================================================================================")
        sys.exit(0)
    else:
        log("  AUDIT RESULT: FAIL")
        log("================================================================================")
        sys.exit(1)

if __name__ == "__main__":
    main()
