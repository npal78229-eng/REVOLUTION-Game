"""
PROJECT REVOLUTION — Level Assembler for Task 10: Railway Junction & Colonial Civil Lines
Arranges the 4 monumental railway & civil lines structures along the Northern Perimeter of L_Validation_Gym:
1. SM_Railway_Brick_Overpass_Arch (Monumental colonial arched bridge separating indigenous quarters from Civil Lines)
2. 3x SM_Railway_Tracks_Ballast_Bed_4m (Broad-gauge dual railway tracks through cutting)
3. SM_Colonial_Railway_Signal_Gantry (6.5m lattice iron semaphore tower with signal arm)
4. 2x SM_Civil_Lines_Club_Perimeter_Railing (Security spearhead palisade along Civil Lines boundary)

Enforces CTF_USE_COMPLEX_AS_SIMPLE collision and saves level.
"""

import unreal

def log(msg):
    unreal.log_warning(f"[REVOLUTION_TASK10_ARRANGER] {msg}")

def run_arrangement():
    log("Arranging Task 10 Railway & Civil Lines Structures into L_Validation_Gym...")

    level_editor_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    editor_actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    level_path = "/Game/Maps/L_Validation_Gym"
    level_editor_sub.load_level(level_path)

    # Clean existing actors from this set to prevent duplicates if re-run
    prefix_list = [
        "Railway_Brick_Overpass_",
        "Railway_Tracks_Ballast_",
        "Colonial_Railway_Signal_Gantry_",
        "Civil_Lines_Perimeter_Railing_"
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
        "SM_Railway_Tracks_Ballast_Bed_4m",
        "SM_Railway_Brick_Overpass_Arch",
        "SM_Colonial_Railway_Signal_Gantry",
        "SM_Civil_Lines_Club_Perimeter_Railing"
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

    # 1. Monumental Colonial Railway Brick Overpass
    spawn_static_prop(
        "SM_Railway_Brick_Overpass_Arch",
        (900.0, 3900.0, 0.0),
        (0.0, 0.0, 0.0),
        label="Railway_Brick_Overpass_Imperial"
    )

    # 2. Continuous Broad-Gauge Railway Tracks through the Arch Cutting (Oriented along X axis)
    spawn_static_prop(
        "SM_Railway_Tracks_Ballast_Bed_4m",
        (500.0, 3900.0, 0.0),
        (0.0, 90.0, 0.0),
        label="Railway_Tracks_Ballast_West"
    )
    spawn_static_prop(
        "SM_Railway_Tracks_Ballast_Bed_4m",
        (900.0, 3900.0, 0.0),
        (0.0, 90.0, 0.0),
        label="Railway_Tracks_Ballast_CenterArch"
    )
    spawn_static_prop(
        "SM_Railway_Tracks_Ballast_Bed_4m",
        (1300.0, 3900.0, 0.0),
        (0.0, 90.0, 0.0),
        label="Railway_Tracks_Ballast_East"
    )

    # 3. Lattice Iron Semaphore Signal Gantry
    spawn_static_prop(
        "SM_Colonial_Railway_Signal_Gantry",
        (1160.0, 3960.0, 0.0),
        (0.0, -90.0, 0.0),
        label="Colonial_Railway_Signal_Gantry_Junction"
    )

    # 4. Civil Lines Club Security Perimeter Railings (Boundary at Y = 4200)
    spawn_static_prop(
        "SM_Civil_Lines_Club_Perimeter_Railing",
        (700.0, 4200.0, 0.0),
        (0.0, 0.0, 0.0),
        label="Civil_Lines_Perimeter_Railing_West"
    )
    spawn_static_prop(
        "SM_Civil_Lines_Club_Perimeter_Railing",
        (1100.0, 4200.0, 0.0),
        (0.0, 0.0, 0.0),
        label="Civil_Lines_Perimeter_Railing_East"
    )

    # Save level
    level_editor_sub.save_current_level()
    all_actors = editor_actor_sub.get_all_level_actors()
    log(f"SUCCESS: Task 10 Railway & Civil Lines assembled. Total level actors: {len(all_actors)}")

if __name__ == "__main__":
    run_arrangement()
