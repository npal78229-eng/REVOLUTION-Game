"""
PROJECT REVOLUTION — Create Kabir v06 Cinematic Showcase Level
Duplicates L_Validation_Gym to L_Kabir_v06_Showcase and stages all 3 Kabir v06 life-stage characters
in the authentic 1919 Amritsar courtyard under Lumen lighting with a CineCamera.
"""

import sys
import unreal

def log(msg):
    unreal.log_warning(f"[SHOWCASE_BUILDER] {msg}")

def main():
    log("================================================================================")
    log("  CREATING KABIR v06 CINEMATIC SHOWCASE LEVEL")
    log("================================================================================")
    
    editor_asset_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    
    source_map = "/Game/Maps/L_Validation_Gym"
    dest_map = "/Game/Maps/L_Kabir_v06_Showcase"
    
    if not editor_asset_sub.does_asset_exist(dest_map):
        duplicated = editor_asset_sub.duplicate_asset(source_map, dest_map)
        if not duplicated:
            log(f"Failed to duplicate {source_map} -> {dest_map}")
            sys.exit(1)
        log(f"Duplicated {source_map} to {dest_map}")
    else:
        log(f"Showcase map already exists: {dest_map}")
        
    loaded = level_sub.load_level(dest_map)
    if not loaded:
        log(f"Failed to load {dest_map}")
        sys.exit(1)
    log(f"Successfully loaded {dest_map}")
    
    # Clean up any previously spawned showcase actors if re-running
    existing_actors = actor_sub.get_all_level_actors()
    for a in existing_actors:
        label = a.get_actor_label()
        if "Showcase_Kabir" in label or "Showcase_CineCam" in label:
            actor_sub.destroy_actor(a)
            
    # Load Blueprints
    bp_child = unreal.load_asset("/Game/Characters/Kabir_v06/BP_Kabir_v06_Child_12")
    bp_teen  = unreal.load_asset("/Game/Characters/Kabir_v06/BP_Kabir_v06_Teen_16")
    bp_adult = unreal.load_asset("/Game/Characters/Kabir_v06/BP_Kabir_v06_Adult_25")
    
    characters = [
        ("Showcase_Kabir_v06_Child_12", bp_child, unreal.Vector(-130.0, 120.0, 0.0), unreal.Rotator(0.0, -90.0, 0.0)),
        ("Showcase_Kabir_v06_Teen_16",  bp_teen,  unreal.Vector(0.0, 120.0, 0.0),    unreal.Rotator(0.0, -90.0, 0.0)),
        ("Showcase_Kabir_v06_Adult_25", bp_adult, unreal.Vector(130.0, 120.0, 0.0),  unreal.Rotator(0.0, -90.0, 0.0))
    ]
    
    for label, bp_asset, loc, rot in characters:
        if not bp_asset:
            log(f"ERROR: Missing BP for {label}")
            continue
        gen_class = bp_asset.generated_class()
        actor = actor_sub.spawn_actor_from_class(gen_class, loc, rot)
        if actor:
            actor.set_actor_label(label)
            log(f"  Spawned {label} at {loc}")
        else:
            log(f"  Failed to spawn {label}")
            
    # Spawn CineCameraActor
    cam_class = unreal.load_class(None, "/Script/CinematicCamera.CineCameraActor")
    if cam_class:
        cam_loc = unreal.Vector(0.0, -180.0, 110.0)
        # Calculate pitch looking slightly down towards characters (chest level at Z=90, dist=300)
        cam_rot = unreal.Rotator(-4.0, 90.0, 0.0)
        cam = actor_sub.spawn_actor_from_class(cam_class, cam_loc, cam_rot)
        if cam:
            cam.set_actor_label("Showcase_CineCam_Master")
            log(f"  Spawned CineCameraActor at {cam_loc}")
            
    level_sub.save_current_level()
    log("================================================================================")
    log("  SUCCESS: KABIR v06 CINEMATIC SHOWCASE LEVEL SAVED (L_Kabir_v06_Showcase)")
    log("================================================================================")
    sys.exit(0)

if __name__ == "__main__":
    main()
