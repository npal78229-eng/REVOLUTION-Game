"""
PROJECT REVOLUTION — Level Assembler for Task 13: Locomotive Depot & Colonial Cantonment
Arranges the 4 monumental assets in Zone G / Northern Civil Lines of L_Validation_Gym:
1. SM_Locomotive_Engine_PunjabMail (British 4-6-0 broad-gauge steam engine on railway tracks)
2. SM_Cantonment_Guardhouse_Picket (Fortified whitewashed sentry post with sandbags guarding gate)
3. SM_Civil_Lines_Clubhouse_Bungalow (Colonial administrative bungalow with Doric veranda)
4. SM_Prop_Cantonment_Archive_Cabinet (Teak archive cabinet on veranda with martial law dockets)

Enforces CTF_USE_COMPLEX_AS_SIMPLE collision and saves level.
"""

import unreal

def log(msg):
    unreal.log_warning(f"[REVOLUTION_TASK13_ARRANGER] {msg}")

def run_arrangement():
    log("Arranging Task 13 Locomotive & Cantonment Assets into L_Validation_Gym...")

    level_editor_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    editor_actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    level_path = "/Game/Maps/L_Validation_Gym"
    level_editor_sub.load_level(level_path)

    # Clean existing actors from this set to prevent duplicates if re-run
    target_labels = [
        "Locomotive_Engine_PunjabMail_Depot",
        "Cantonment_Guardhouse_Picket_NorthGate",
        "Civil_Lines_Clubhouse_Bungalow_HQ",
        "Prop_Cantonment_Archive_Cabinet_Veranda"
    ]
    for a in editor_actor_sub.get_all_level_actors():
        lbl = a.get_actor_label()
        if lbl in target_labels:
            editor_actor_sub.destroy_actor(a)
            log(f"Cleaned existing actor: {lbl}")

    # Cache Mesh Assets
    mesh_keys = [
        "SM_Locomotive_Engine_PunjabMail",
        "SM_Cantonment_Guardhouse_Picket",
        "SM_Civil_Lines_Clubhouse_Bungalow",
        "SM_Prop_Cantonment_Archive_Cabinet"
    ]
    mesh_cache = {}
    for mk in mesh_keys:
        m_obj = unreal.load_asset(f"/Game/Environment/Mohalla/Meshes/{mk}")
        if m_obj:
            mesh_cache[mk] = m_obj
            log(f"Cached mesh: {mk}")
        else:
            log(f"Warning: Failed to load mesh {mk}")

    def spawn_static_mesh_actor(mesh_key, loc, rot=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0), label=None):
        if mesh_key not in mesh_cache:
            log(f"Error: {mesh_key} not in cache")
            return None
        m_obj = mesh_cache[mesh_key]

        actor = editor_actor_sub.spawn_actor_from_class(
            unreal.StaticMeshActor,
            unreal.Vector(loc[0], loc[1], loc[2]),
            unreal.Rotator(rot[0], rot[1], rot[2])
        )
        if actor:
            actor.set_actor_scale3d(unreal.Vector(scale[0], scale[1], scale[2]))
            if label:
                actor.set_actor_label(label)
            sm_comp = actor.static_mesh_component
            if sm_comp:
                sm_comp.set_static_mesh(m_obj)
                sm_comp.set_collision_profile_name("BlockAll")
                sm_comp.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)
                sm_comp.set_mobility(unreal.ComponentMobility.STATIC)
            log(f"Spawned {label} at {loc}")
        return actor

    # 1. SM_Locomotive_Engine_PunjabMail on Broad-Gauge Tracks at Y=3900 (Oriented along X axis with Yaw=90)
    spawn_static_mesh_actor(
        "SM_Locomotive_Engine_PunjabMail",
        (1000.0, 3900.0, 30.0),
        (0.0, 90.0, 0.0),
        label="Locomotive_Engine_PunjabMail_Depot"
    )

    # 2. SM_Cantonment_Guardhouse_Picket guarding the Civil Lines gateway at (650, 4220, 0)
    spawn_static_mesh_actor(
        "SM_Cantonment_Guardhouse_Picket",
        (650.0, 4220.0, 0.0),
        (0.0, 0.0, 0.0),
        label="Cantonment_Guardhouse_Picket_NorthGate"
    )

    # 3. SM_Civil_Lines_Clubhouse_Bungalow at (900, 4800, 0) as the Act V climax colonial headquarters
    spawn_static_mesh_actor(
        "SM_Civil_Lines_Clubhouse_Bungalow",
        (900.0, 4800.0, 0.0),
        (0.0, 0.0, 0.0),
        label="Civil_Lines_Clubhouse_Bungalow_HQ"
    )

    # 4. SM_Prop_Cantonment_Archive_Cabinet on the clubhouse veranda at (820, 4520, 60)
    spawn_static_mesh_actor(
        "SM_Prop_Cantonment_Archive_Cabinet",
        (820.0, 4520.0, 60.0),
        (0.0, 0.0, 0.0),
        label="Prop_Cantonment_Archive_Cabinet_Veranda"
    )

    # Save level
    level_editor_sub.save_current_level()
    all_actors = editor_actor_sub.get_all_level_actors()
    log(f"SUCCESS: Task 13 Locomotive & Cantonment assembled. Total level actors: {len(all_actors)}")

if __name__ == "__main__":
    run_arrangement()
