"""
PROJECT REVOLUTION — Level Assembler for Task 7: Stampede Debris & Escape Traversal
Loads L_Validation_Gym and arranges the Task 7 assets:
1. SM_Jallianwala_Crumbling_Wall_Breach (Historic crumbling 1.8m low wall section with rubble ramp for vaulting)
2. SM_Prop_Bullet_Pocked_Brick_Slab (Historic memorial brick slab with bullet impacts & white marking frames)
3. SM_Prop_Makeshift_Timber_Ladder (Escape ladder leaned against north enclosure wall)
4. 3x SM_Prop_Fallen_Turban_Shoes_Scatter (Stampede debris along panic escape routes)
"""

import unreal

def log(msg):
    unreal.log_warning(f"[REVOLUTION_TASK7_ARRANGER] {msg}")

def run_arrangement():
    log("Arranging Task 7 Stampede Debris & Wall Breach in L_Validation_Gym...")

    level_editor_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    editor_actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    level_path = "/Game/Maps/L_Validation_Gym"
    level_editor_sub.load_level(level_path)

    # Clean existing actors from this set to prevent duplicates if re-run
    prefix_list = [
        "Jallianwala_Crumbling_Wall_Breach_",
        "Jallianwala_Bullet_Pocked_Wall_",
        "Jallianwala_Makeshift_Ladder_",
        "Story_Panic_Debris_Scatter_"
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
        "SM_Jallianwala_Crumbling_Wall_Breach",
        "SM_Prop_Bullet_Pocked_Brick_Slab",
        "SM_Prop_Makeshift_Timber_Ladder",
        "SM_Prop_Fallen_Turban_Shoes_Scatter"
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
    # 1. CRUMBLING WALL BREACH (North-West garden boundary escape route)
    # =========================================================================
    # Positioned at (650, 3350, 0) aligned North-South with Y axis
    spawn_static_prop(
        "SM_Jallianwala_Crumbling_Wall_Breach",
        (650.0, 3350.0, 0.0),
        (0.0, 90.0, 0.0),
        label="Jallianwala_Crumbling_Wall_Breach_West"
    )

    # =========================================================================
    # 2. BULLET-POCKED MEMORIAL WALL SLAB (East enclosure wall facing firing line)
    # =========================================================================
    spawn_static_prop(
        "SM_Prop_Bullet_Pocked_Brick_Slab",
        (1740.0, 3100.0, 0.0),
        (0.0, 90.0, 0.0),
        label="Jallianwala_Bullet_Pocked_Wall_East"
    )

    # =========================================================================
    # 3. MAKESHIFT TIMBER ESCAPE LADDER (Leaned against North wall)
    # =========================================================================
    spawn_static_prop(
        "SM_Prop_Makeshift_Timber_Ladder",
        (1350.0, 3420.0, 0.0),
        (0.0, 0.0, 0.0),
        label="Jallianwala_Makeshift_Ladder_North"
    )

    # =========================================================================
    # 4. PANIC DEBRIS SCATTER (3 distinct locations along the stampede route)
    # =========================================================================
    # Scatter 1: Near assembly dais
    spawn_static_prop(
        "SM_Prop_Fallen_Turban_Shoes_Scatter",
        (1380.0, 3020.0, 0.0),
        (0.0, 35.0, 0.0),
        label="Story_Panic_Debris_Scatter_Dais"
    )

    # Scatter 2: Near Martyrs' Well
    spawn_static_prop(
        "SM_Prop_Fallen_Turban_Shoes_Scatter",
        (1180.0, 2880.0, 0.0),
        (0.0, -45.0, 0.0),
        label="Story_Panic_Debris_Scatter_Well"
    )

    # Scatter 3: In front of the crumbling wall breach escape route
    spawn_static_prop(
        "SM_Prop_Fallen_Turban_Shoes_Scatter",
        (750.0, 3250.0, 0.0),
        (0.0, 110.0, 0.0),
        label="Story_Panic_Debris_Scatter_Breach"
    )

    # Save Level
    level_editor_sub.save_current_level()
    log("Successfully saved L_Validation_Gym with Task 7 Stampede Debris & Wall Breach Structures!")

if __name__ == "__main__":
    run_arrangement()
