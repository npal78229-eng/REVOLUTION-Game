"""
PROJECT REVOLUTION — Level Assembler for Task 9: Outskirts & The Upper Bari Doab Canal
Loads L_Validation_Gym and arranges the Task 9 assets in the Western Outskirts (Zone F):
1. SM_Canal_Distributary_Aqueduct_Stone (Stone culvert & sluice regulator spanning irrigation channel)
2. SM_Persian_Wheel_Rahat_Timber (Traditional Punjabi Persian wheel well mechanism with buckets)
3. SM_Brick_Kiln_Chimney_Bhatta (Conical brick kiln chimney & brick drying trench)
4. SM_Prop_Clandestine_Safehouse_Crate_Cache (Disguised supply cache with bicycle & cargo crates)
"""

import unreal

def log(msg):
    unreal.log_warning(f"[REVOLUTION_TASK9_ARRANGER] {msg}")

def run_arrangement():
    log("Arranging Task 9 Canal & Outskirts Structures in L_Validation_Gym...")

    level_editor_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    editor_actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    level_path = "/Game/Maps/L_Validation_Gym"
    level_editor_sub.load_level(level_path)

    # Clean existing actors from this set to prevent duplicates if re-run
    prefix_list = [
        "Canal_Distributary_Aqueduct_",
        "Rural_Persian_Wheel_Rahat_",
        "Industrial_Brick_Kiln_Bhatta_",
        "Story_Clandestine_Safehouse_Supply_Cache"
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
        "SM_Canal_Distributary_Aqueduct_Stone",
        "SM_Persian_Wheel_Rahat_Timber",
        "SM_Brick_Kiln_Chimney_Bhatta",
        "SM_Prop_Clandestine_Safehouse_Crate_Cache"
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
    # 1. CANAL DISTRIBUTARY AQUEDUCT & SLUICE (Zone F Western Channel)
    # =========================================================================
    spawn_static_prop(
        "SM_Canal_Distributary_Aqueduct_Stone",
        (-950.0, 2200.0, 0.0),
        (0.0, 90.0, 0.0),
        label="Canal_Distributary_Aqueduct_Sluice"
    )

    # =========================================================================
    # 2. PUNJABI PERSIAN WHEEL RAHAT (Canal feeder well)
    # =========================================================================
    spawn_static_prop(
        "SM_Persian_Wheel_Rahat_Timber",
        (-1150.0, 2050.0, 0.0),
        (0.0, -15.0, 0.0),
        label="Rural_Persian_Wheel_Rahat_Canal"
    )

    # =========================================================================
    # 3. TRADITIONAL BRICK KILN BHATTA (Outskirt industrial horizon & hideout)
    # =========================================================================
    spawn_static_prop(
        "SM_Brick_Kiln_Chimney_Bhatta",
        (-1250.0, 2650.0, 0.0),
        (0.0, 45.0, 0.0),
        label="Industrial_Brick_Kiln_Bhatta_Chimney"
    )

    # =========================================================================
    # 4. CLANDESTINE SAFEHOUSE SUPPLY CACHE (Behind the brick kiln trench)
    # =========================================================================
    spawn_static_prop(
        "SM_Prop_Clandestine_Safehouse_Crate_Cache",
        (-1180.0, 2520.0, 0.0),
        (0.0, 20.0, 0.0),
        label="Story_Clandestine_Safehouse_Supply_Cache"
    )

    # Save Level
    level_editor_sub.save_current_level()
    log("Successfully saved L_Validation_Gym with Task 9 Canal & Outskirts Structures!")

if __name__ == "__main__":
    run_arrangement()
