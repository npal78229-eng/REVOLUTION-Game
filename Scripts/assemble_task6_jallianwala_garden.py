"""
PROJECT REVOLUTION — Level Assembler for Task 6: The Enclosed Garden of Jallianwala Bagh
Loads L_Validation_Gym and arranges the Task 6 Jallianwala Bagh structures:
1. SM_British_Armored_Car_Obstacle (Austin armored car stopped outside narrow entrance)
2. SM_Jallianwala_Raised_Bank (Tactical 1.2m elevated earthen terrace mound inside gate)
3. SM_Jallianwala_Shahidi_Kua_Well (Historic Martyrs' Well with octagonal plinth & canopy)
4. SM_Jallianwala_Baisakhi_Pandal (Assembly dais platform with shamiana canopy & podium)
5. 4x SM_Jallianwala_Enclosure_Wall (4.5m tall blind Lahori brick haveli walls sealing the garden)
"""

import unreal

def log(msg):
    unreal.log_warning(f"[REVOLUTION_TASK6_ARRANGER] {msg}")

def run_arrangement():
    log("Arranging Task 6 Jallianwala Bagh Garden Structures in L_Validation_Gym...")

    level_editor_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    editor_actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    level_path = "/Game/Maps/L_Validation_Gym"
    level_editor_sub.load_level(level_path)

    # Clean existing actors from this set to prevent duplicates if re-run
    prefix_list = [
        "British_Armored_Car_Obstacle_",
        "Jallianwala_Raised_Bank_",
        "Jallianwala_Shahidi_Kua_",
        "Jallianwala_Baisakhi_Pandal_",
        "Jallianwala_Enclosure_Wall_"
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
        "SM_British_Armored_Car_Obstacle",
        "SM_Jallianwala_Raised_Bank",
        "SM_Jallianwala_Shahidi_Kua_Well",
        "SM_Jallianwala_Baisakhi_Pandal",
        "SM_Jallianwala_Enclosure_Wall"
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
    # 1. BRITISH ARMORED CAR OBSTACLE (Stopped in street outside narrow gate)
    # =========================================================================
    spawn_static_prop(
        "SM_British_Armored_Car_Obstacle",
        (900.0, 2020.0, 0.0),
        (0.0, 0.0, 0.0),
        label="British_Armored_Car_Obstacle_Gate"
    )

    # =========================================================================
    # 2. TACTICAL RAISED BANK (Inside gate entrance overlooking garden)
    # =========================================================================
    spawn_static_prop(
        "SM_Jallianwala_Raised_Bank",
        (900.0, 2600.0, 0.0),
        (0.0, 0.0, 0.0),
        label="Jallianwala_Raised_Bank_Tactical"
    )

    # =========================================================================
    # 3. SHAHIDI KUA — THE MARTYRS' WELL (Center-West ground of garden)
    # =========================================================================
    spawn_static_prop(
        "SM_Jallianwala_Shahidi_Kua_Well",
        (1200.0, 2950.0, 0.0),
        (0.0, 22.5, 0.0),
        label="Jallianwala_Shahidi_Kua_MemorialWell"
    )

    # =========================================================================
    # 4. BAISAKHI PANDAL ASSEMBLY DAIS (Northeast ground facing rally crowd)
    # =========================================================================
    spawn_static_prop(
        "SM_Jallianwala_Baisakhi_Pandal",
        (1450.0, 3100.0, 0.0),
        (0.0, -135.0, 0.0),
        label="Jallianwala_Baisakhi_Pandal_Dais"
    )

    # =========================================================================
    # 5. ENCLOSURE WALLS (4.5m blind brick haveli walls sealing garden)
    # =========================================================================
    # North Enclosure Wall
    spawn_static_prop(
        "SM_Jallianwala_Enclosure_Wall",
        (1200.0, 3450.0, 0.0),
        (0.0, 0.0, 0.0),
        label="Jallianwala_Enclosure_Wall_North"
    )

    # East Enclosure Wall
    spawn_static_prop(
        "SM_Jallianwala_Enclosure_Wall",
        (1750.0, 2950.0, 0.0),
        (0.0, 90.0, 0.0),
        label="Jallianwala_Enclosure_Wall_East"
    )

    # West Enclosure Wall
    spawn_static_prop(
        "SM_Jallianwala_Enclosure_Wall",
        (650.0, 2950.0, 0.0),
        (0.0, 90.0, 0.0),
        label="Jallianwala_Enclosure_Wall_West"
    )

    # South-East Enclosure Wall
    spawn_static_prop(
        "SM_Jallianwala_Enclosure_Wall",
        (1400.0, 2550.0, 0.0),
        (0.0, 0.0, 0.0),
        label="Jallianwala_Enclosure_Wall_SouthEast"
    )

    # Save Level
    level_editor_sub.save_current_level()
    log("Successfully saved L_Validation_Gym with Task 6 Jallianwala Bagh Garden Structures!")

if __name__ == "__main__":
    run_arrangement()
