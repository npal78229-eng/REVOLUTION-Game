"""
PROJECT REVOLUTION — Level Assembler for Task 14: Locomotive Steam Valve & Picket Station
Places the interactive ALocomotiveSteamValveActor onto the boiler of SM_Locomotive_Engine_PunjabMail
in L_Validation_Gym.umap.
"""

import unreal

def log(msg):
    unreal.log_warning(f"[REVOLUTION_TASK14_ARRANGER] {msg}")

def run_arrangement():
    log("Arranging Task 14 Locomotive Steam Pressure Relief Valve into L_Validation_Gym...")

    level_editor_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    editor_actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    level_path = "/Game/Maps/L_Validation_Gym"
    level_editor_sub.load_level(level_path)

    # Clean existing actor if re-run
    for a in editor_actor_sub.get_all_level_actors():
        if a.get_actor_label() == "Locomotive_Steam_Pressure_Relief_Valve":
            editor_actor_sub.destroy_actor(a)
            log("Cleaned existing Locomotive_Steam_Pressure_Relief_Valve")
            break

    valve_class = unreal.load_class(None, "/Script/REVOLUTION.LocomotiveSteamValveActor")
    if not valve_class:
        log("ERROR: Could not load ALocomotiveSteamValveActor class!")
        return False

    valve_actor = editor_actor_sub.spawn_actor_from_class(
        valve_class,
        unreal.Vector(1000.0, 3880.0, 90.0),
        unreal.Rotator(0.0, 0.0, 0.0)
    )

    if valve_actor:
        valve_actor.set_actor_label("Locomotive_Steam_Pressure_Relief_Valve")
        log("Successfully spawned Locomotive_Steam_Pressure_Relief_Valve at (1000, 3880, 90)")

    # Save level
    level_editor_sub.save_current_level()
    all_actors = editor_actor_sub.get_all_level_actors()
    log(f"SUCCESS: Task 14 Steam Valve assembled. Total level actors: {len(all_actors)}")
    return True

if __name__ == "__main__":
    run_arrangement()
