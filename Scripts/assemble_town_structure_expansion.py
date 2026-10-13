"""
PROJECT REVOLUTION — Level Assembler for Town Structure Expansion
Loads L_Validation_Gym and arranges the 5 new monumental structures:
1. 6x SM_Wall_Town_Faseel_Rampart (Perimeter defensive rampart walls with battlements & walkways)
2. 1x SM_Checkpoint_Picket_Sandbag_Barrier (British sandbag revetment, wooden blockade & curfew sign)
3. 4x SM_Haveli_Facade_3Story_Jharokha (12m monumental 3-story haveli facades with teak balconies)
4. 1x SM_Prop_Litho_Press_Flatbed (Authentic cast-iron flatbed stone lithographic hand press & stash)
5. 1x SM_Mohalla_Pyaoo_Water_Shelter (Roadside drinking water shelter with timber pillars & matkas)
"""

import unreal

def log(msg):
    unreal.log_warning(f"[REVOLUTION_EXPANSION_ARRANGER] {msg}")

def run_arrangement():
    log("Arranging Town Structure Expansion in L_Validation_Gym...")

    level_editor_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    editor_actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    level_path = "/Game/Maps/L_Validation_Gym"
    level_editor_sub.load_level(level_path)

    # Clean existing actors from this set to prevent duplicates if re-run
    prefix_list = [
        "Town_Faseel_",
        "Checkpoint_Picket_Barrier_",
        "Haveli_Facade_3Story_",
        "Story_Litho_Press_Flatbed_",
        "Mohalla_Pyaoo_Water_Shelter_",
        "SupplyStash_Litho_Press"
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
        "SM_Wall_Town_Faseel_Rampart",
        "SM_Checkpoint_Picket_Sandbag_Barrier",
        "SM_Haveli_Facade_3Story_Jharokha",
        "SM_Prop_Litho_Press_Flatbed",
        "SM_Mohalla_Pyaoo_Water_Shelter"
    ]
    mesh_cache = {}
    for mk in mesh_keys:
        m_obj = unreal.load_asset(f"/Game/Environment/Mohalla/Meshes/{mk}")
        if m_obj:
            mesh_cache[mk] = m_obj
            log(f"Cached mesh: {mk}")
        else:
            log(f"Warning: Failed to load mesh {mk}")

    def spawn_expansion_prop(mesh_key, loc, rot=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0), label=None):
        if mesh_key not in mesh_cache:
            log(f"Error: {mesh_key} not in cache")
            return None
        m_obj = mesh_cache[mesh_key]

        # Use spawn_actor_from_class with StaticMeshActor to be 100% commandlet-safe
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.StaticMeshActor,
            unreal.Vector(loc[0], loc[1], loc[2]),
            unreal.Rotator(rot[0], rot[1], rot[2])
        )
        if actor:
            actor.set_actor_scale3d(unreal.Vector(scale[0], scale[1], scale[2]))
            if label:
                actor.set_actor_label(label)
            sm_comp = actor.get_component_by_class(unreal.StaticMeshComponent)
            if sm_comp:
                sm_comp.set_static_mesh(m_obj)
                sm_comp.set_collision_profile_name("BlockAll")
                sm_comp.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)
                sm_comp.set_mobility(unreal.ComponentMobility.STATIC)
            log(f"Spawned {label} at {loc}")
        return actor

    # =========================================================================
    # 1. PERIMETER DEFENSIVE TOWN RAMPART WALLS (Faseel)
    # =========================================================================
    # North Gate Flanking Ramparts (sealing northern boundary around checkpoint)
    spawn_expansion_prop("SM_Wall_Town_Faseel_Rampart", (-600.0, 2250.0, 0.0), (0.0, 0.0, 0.0), label="Town_Faseel_NorthWall_West")
    spawn_expansion_prop("SM_Wall_Town_Faseel_Rampart", (600.0, 2250.0, 0.0), (0.0, 0.0, 0.0), label="Town_Faseel_NorthWall_East")

    # East Enclosure Ramparts (behind Vernacular Middle School)
    spawn_expansion_prop("SM_Wall_Town_Faseel_Rampart", (1750.0, 1350.0, 0.0), (0.0, 90.0, 0.0), label="Town_Faseel_EastWall_School")
    spawn_expansion_prop("SM_Wall_Town_Faseel_Rampart", (1750.0, 1950.0, 0.0), (0.0, 90.0, 0.0), label="Town_Faseel_EastWall_North")

    # West Enclosure Ramparts (western boundary of Well Square & Deorhi)
    spawn_expansion_prop("SM_Wall_Town_Faseel_Rampart", (-650.0, 1350.0, 0.0), (0.0, -90.0, 0.0), label="Town_Faseel_WestWall_Well")
    spawn_expansion_prop("SM_Wall_Town_Faseel_Rampart", (-650.0, 750.0, 0.0), (0.0, -90.0, 0.0), label="Town_Faseel_WestWall_Deorhi")

    # =========================================================================
    # 2. BRITISH CHECKPOINT PICKET & BARRICADE (North Exit of Grand Bazaar)
    # =========================================================================
    spawn_expansion_prop("SM_Checkpoint_Picket_Sandbag_Barrier", (0.0, 2120.0, 0.0), (0.0, 0.0, 0.0), label="Checkpoint_Picket_Barrier_NorthGate")

    # =========================================================================
    # 3. MONUMENTAL 3-STORY HAVELI URBAN FACADES (12m Street Enclosure)
    # =========================================================================
    # Flanking Grand Bazaar
    spawn_expansion_prop("SM_Haveli_Facade_3Story_Jharokha", (-550.0, 1800.0, 0.0), (0.0, 90.0, 0.0), label="Haveli_Facade_3Story_BazaarWest")
    spawn_expansion_prop("SM_Haveli_Facade_3Story_Jharokha", (550.0, 1800.0, 0.0), (0.0, -90.0, 0.0), label="Haveli_Facade_3Story_BazaarEast")

    # Flanking Well Square
    spawn_expansion_prop("SM_Haveli_Facade_3Story_Jharokha", (-350.0, 1050.0, 0.0), (0.0, 45.0, 0.0), label="Haveli_Facade_3Story_WellSouth")

    # Kabir's Haveli South Rear Elevation
    spawn_expansion_prop("SM_Haveli_Facade_3Story_Jharokha", (0.0, -450.0, 0.0), (0.0, 0.0, 0.0), label="Haveli_Facade_3Story_HaveliRear")

    # =========================================================================
    # 4. FLATBED LITHOGRAPHIC PRINTING PRESS (Secret Haveli Cellar Workshop)
    # =========================================================================
    spawn_expansion_prop("SM_Prop_Litho_Press_Flatbed", (320.0, 280.0, 0.0), (0.0, -45.0, 0.0), label="Story_Litho_Press_Flatbed_Vault")

    # Ensure a Pamphlet Supply Stash Actor is positioned at the litho press
    supply_stash_cls = unreal.load_class(None, "/Script/REVOLUTION.SupplyStashActor")
    if supply_stash_cls:
        stash_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            supply_stash_cls,
            unreal.Vector(320.0, 280.0, 90.0),
            unreal.Rotator(0.0, 0.0, 0.0)
        )
        if stash_actor:
            stash_actor.set_actor_label("SupplyStash_Litho_Press")
            stash_actor.set_editor_property("stash_type", unreal.SupplyStashType.PAMPHLETS)
            stash_actor.set_editor_property("replenish_amount", 5)
            stash_actor.set_editor_property("stash_title", unreal.Text("Litho Press Pamphlet Cache"))
            log("Spawned SupplyStash_Litho_Press at (320, 280, 90)")

    # =========================================================================
    # 5. ROADSIDE DRINKING WATER CHHABEEL / PYAOO (Well Square / Chowk Gateway)
    # =========================================================================
    spawn_expansion_prop("SM_Mohalla_Pyaoo_Water_Shelter", (-220.0, 1420.0, 0.0), (0.0, 45.0, 0.0), label="Mohalla_Pyaoo_Water_Shelter_Chowk")

    # Save Level
    level_editor_sub.save_current_level()
    log("Successfully saved L_Validation_Gym with Town Structure Expansion!")

if __name__ == "__main__":
    run_arrangement()
