"""
PROJECT REVOLUTION — Level Assembler for Schoolmate Kartar & Colonial Constable
Loads L_Validation_Gym and places:
1. Kartar Singh (Schoolmate & Friend, Age 12) near Sacred Peepal Tree at (450, 1380, 88)
2. Constable Gurdial Singh (Punjab Imperial Police) patrolling Grand Bazaar at (0, 1600, 88)
"""

import unreal

def log(msg):
    unreal.log_warning(f"[REVOLUTION_NPC_ASSEMBLER] {msg}")

def run_assemble():
    log("Starting Schoolmate Kartar & Colonial Constable Assembly...")

    level_editor_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    editor_actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    level_path = "/Game/Maps/L_Validation_Gym"
    level_editor_sub.load_level(level_path)

    # Clean existing instances if already present to avoid duplication
    existing_actors = editor_actor_sub.get_all_level_actors()
    labels_to_clean = [
        "NPC_KartarSingh_Friend",
        "NPC_Constable_Gurdial"
    ]
    for a in existing_actors:
        lbl = a.get_actor_label()
        if lbl in labels_to_clean:
            editor_actor_sub.destroy_actor(a)
            log(f"Cleaned existing actor: {lbl}")

    # 1. Spawn Kartar Singh (SchoolFriendKartar)
    civ_class = unreal.load_class(None, "/Script/REVOLUTION.CivilianNPCActor")
    if civ_class:
        occ_enum = getattr(unreal, "CivilianOccupation", None)
        kartar_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            civ_class,
            unreal.Vector(450.0, 1380.0, 88.0),
            unreal.Rotator(0.0, -90.0, 0.0)
        )
        if kartar_actor:
            kartar_actor.set_actor_label("NPC_KartarSingh_Friend")
            if occ_enum and hasattr(occ_enum, "SCHOOL_FRIEND_KARTAR"):
                val = getattr(occ_enum, "SCHOOL_FRIEND_KARTAR")
                kartar_actor.set_editor_property("occupation", val)
                kartar_actor.configure_occupation(val)
            log("Spawned NPC_KartarSingh_Friend (Schoolmate & Friend) at (450, 1380, 88)")
    else:
        log("Error: Failed to load CivilianNPCActor class")

    # 2. Spawn Colonial Police Constable in Grand Bazaar
    patrol_class = unreal.load_class(None, "/Script/REVOLUTION.CurfewPatrolAI")
    if patrol_class:
        constable_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            patrol_class,
            unreal.Vector(0.0, 1600.0, 88.0),
            unreal.Rotator(0.0, 90.0, 0.0)
        )
        if constable_actor:
            constable_actor.set_actor_label("NPC_Constable_Gurdial")
            constable_actor.set_editor_property("watchman_title", unreal.Text("Constable Gurdial Singh (Punjab Imperial Police)"))
            
            # Configure Bazaar patrol waypoints
            waypoints = [
                unreal.Vector(0.0, 1600.0, 88.0),
                unreal.Vector(0.0, 1820.0, 88.0),
                unreal.Vector(0.0, 2040.0, 88.0)
            ]
            constable_actor.set_editor_property("patrol_waypoints", waypoints)
            constable_actor.set_editor_property("patrol_walk_speed", 130.0)
            constable_actor.set_editor_property("waypoint_wait_duration", 4.0)
            log("Spawned NPC_Constable_Gurdial (Bazaar Constable) at (0, 1600, 88) with 3 waypoints")
    else:
        log("Error: Failed to load CurfewPatrolAI class")

    # Save level and dirty packages
    level_editor_sub.save_current_level()
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(False, True)
    unreal.EditorAssetLibrary.save_directory("/Game", only_if_is_dirty=True, recursive=True)
    log("=== Schoolmate & Constable Assembly Complete & Saved Successfully ===")

if __name__ == "__main__":
    run_assemble()
