"""
PROJECT REVOLUTION — Level Assembler for Task 8: Act III — The Amritsar Curfew & Searchlights
Loads L_Validation_Gym and arranges the Task 8 assets:
1. SM_Checkpoint_Sandbag_Sentry_Bunker (Sandbag sentry bunker with timber shoring & roof)
2. 2x SM_Prop_Searchlight_Tripod_Imperial (Searchlights sweeping checkpost and rooftops)
3. SM_Prop_Curfew_Notice_Martial_Law (Martial law curfew notice easel at Chowk)
4. SM_Prop_Makeshift_Stretcher_Charpai (Makeshift casualty stretcher in secluded alley)
"""

import unreal

def log(msg):
    unreal.log_warning(f"[REVOLUTION_TASK8_ARRANGER] {msg}")

def run_arrangement():
    log("Arranging Task 8 Curfew & Searchlight Structures in L_Validation_Gym...")

    level_editor_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    editor_actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    level_path = "/Game/Maps/L_Validation_Gym"
    level_editor_sub.load_level(level_path)

    # Clean existing actors from this set to prevent duplicates if re-run
    prefix_list = [
        "Checkpoint_Sandbag_Sentry_Bunker_",
        "Story_Searchlight_Tripod_",
        "Story_Curfew_Notice_Martial_Law_",
        "Story_Makeshift_Stretcher_"
    ]
    for a in editor_actor_sub.get_all_level_actors():
        lbl = a.get_actor_label()
        for prefix in prefix_list:
            if lbl.startswith(prefix):
                editor_actor_sub.destroy_actor(a)
                log(f"Cleaned existing actor: {lbl}")
                break

    # Cache Mesh Assets
    mesh_keys = [
        "SM_Checkpoint_Sandbag_Sentry_Bunker",
        "SM_Prop_Searchlight_Tripod_Imperial",
        "SM_Prop_Curfew_Notice_Martial_Law",
        "SM_Prop_Makeshift_Stretcher_Charpai"
    ]
    mesh_cache = {}
    for mk in mesh_keys:
        m_obj = unreal.load_asset(f"/Game/Environment/Mohalla/Meshes/{mk}")
        if m_obj:
            mesh_cache[mk] = m_obj
            log(f"Cached mesh: {mk}")
        else:
            log(f"Warning: Failed to load mesh {mk}")

    def spawn_static_prop(mesh_key, loc, rot=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0), label=None):
        if mesh_key not in mesh_cache:
            log(f"Error: {mesh_key} not in cache")
            return None
        m_obj = mesh_cache[mesh_key]

        actor = unreal.EditorLevelLibrary.spawn_actor_from_object(
            m_obj,
            unreal.Vector(loc[0], loc[1], loc[2]),
            unreal.Rotator(rot[0], rot[1], rot[2])
        )
        if actor:
            actor.set_actor_scale3d(unreal.Vector(scale[0], scale[1], scale[2]))
            if label:
                actor.set_actor_label(label)
            sm_comp = actor.get_component_by_class(unreal.StaticMeshComponent)
            if sm_comp:
                sm_comp.set_collision_profile_name("BlockAll")
                sm_comp.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)
                sm_comp.set_mobility(unreal.ComponentMobility.STATIC)
            log(f"Spawned {label} at {loc}")
        return actor

    # =========================================================================
    # 1. SANDBAG SENTRY BUNKER (Fortified North checkpost boundary)
    # =========================================================================
    spawn_static_prop(
        "SM_Checkpoint_Sandbag_Sentry_Bunker",
        (0.0, 2260.0, 0.0),
        (0.0, 0.0, 0.0),
        label="Checkpoint_Sandbag_Sentry_Bunker_North"
    )

    # =========================================================================
    # 2. IMPERIAL CARBON-ARC SEARCHLIGHTS (Rooftop & Checkpost)
    # =========================================================================
    # Searchlight 1: Rooftop terrace overlooking Grand Bazaar chowk
    spawn_static_prop(
        "SM_Prop_Searchlight_Tripod_Imperial",
        (-180.0, 1850.0, 400.0),
        (0.0, 30.0, 0.0),
        label="Story_Searchlight_Tripod_Rooftop"
    )

    # Searchlight 2: At North checkpoint bunker perimeter
    spawn_static_prop(
        "SM_Prop_Searchlight_Tripod_Imperial",
        (120.0, 2260.0, 0.0),
        (0.0, -45.0, 0.0),
        label="Story_Searchlight_Tripod_Checkpost"
    )

    # =========================================================================
    # 3. MARTIAL LAW CURFEW NOTICE (Grand Bazaar central chowk)
    # =========================================================================
    spawn_static_prop(
        "SM_Prop_Curfew_Notice_Martial_Law",
        (-80.0, 1850.0, 0.0),
        (0.0, 45.0, 0.0),
        label="Story_Curfew_Notice_Martial_Law_Chowk"
    )

    # =========================================================================
    # 4. EMERGENCY MAKESHIFT STRETCHER (Secluded Deorhi alleyway)
    # =========================================================================
    spawn_static_prop(
        "SM_Prop_Makeshift_Stretcher_Charpai",
        (-120.0, 950.0, 0.0),
        (0.0, 25.0, 0.0),
        label="Story_Makeshift_Stretcher_Alley"
    )

    # Save Level
    level_editor_sub.save_current_level()
    log("Successfully saved L_Validation_Gym with Task 8 Curfew & Searchlight Structures!")

if __name__ == "__main__":
    run_arrangement()
