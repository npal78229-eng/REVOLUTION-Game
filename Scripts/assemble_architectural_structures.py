"""
PROJECT REVOLUTION — Level Assembler for Architectural Environment Structures
Loads L_Validation_Gym and arranges master architectural structures to establish
a complete, cohesive Punjabi walled-town streetscape:
1. 4x SM_Arch_Overhead_Kucha (Vaulted overhead arches across Deorhi & School paths)
2. 1x SM_Arch_Monumental_Chowk_Gate (Monumental 7m gateway into Grand Bazaar)
3. 6x SM_Street_Lamp_Post_Victorian (Period cast-iron streetlamps at junctions)
4. 4x SM_Bazaar_Canopy_Khadi_Awning (Draped khadi cloth market street tunnels)
5. 4x SM_Street_Drain_Stone_Gutter (Carved stone gutters & crossing flagstones)
"""

import unreal

def log(msg):
    unreal.log_warning(f"[REVOLUTION_ARCH_ARRANGER] {msg}")

def run_arrangement():
    log("Arranging architectural structures in L_Validation_Gym...")

    level_editor_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    editor_actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    level_path = "/Game/Maps/L_Validation_Gym"
    level_editor_sub.load_level(level_path)

    # Clean existing arch/structure actors if previously spawned to avoid duplicates
    arch_prefix_list = [
        "Arch_Overhead_Kucha_",
        "Arch_Monumental_Chowk_Gate",
        "Street_Lamp_Post_",
        "Bazaar_Canopy_Khadi_",
        "Street_Drain_Gutter_"
    ]
    for a in editor_actor_sub.get_all_level_actors():
        lbl = a.get_actor_label()
        for prefix in arch_prefix_list:
            if lbl.startswith(prefix):
                editor_actor_sub.destroy_actor(a)
                log(f"Cleaned existing actor: {lbl}")
                break

    # Cache Mesh Assets
    mesh_keys = [
        "SM_Arch_Overhead_Kucha",
        "SM_Arch_Monumental_Chowk_Gate",
        "SM_Street_Lamp_Post_Victorian",
        "SM_Bazaar_Canopy_Khadi_Awning",
        "SM_Street_Drain_Stone_Gutter"
    ]
    mesh_cache = {}
    for mk in mesh_keys:
        m_obj = unreal.load_asset(f"/Game/Environment/Mohalla/Meshes/{mk}")
        if m_obj:
            mesh_cache[mk] = m_obj
            log(f"Cached mesh: {mk}")
        else:
            log(f"Warning: Failed to load mesh {mk}")

    def spawn_arch_prop(mesh_key, loc, rot=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0), label=None):
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
    # 1. FLYING OVERHEAD KUCHA ARCHWAYS (Vaulting the narrow alleys)
    # =========================================================================
    # Arch 1: Haveli north courtyard exit into Deorhi Alley
    spawn_arch_prop("SM_Arch_Overhead_Kucha", (0.0, 600.0, 380.0), (0.0, 0.0, 0.0), label="Arch_Overhead_Kucha_HaveliExit")
    # Arch 2: Mid-Deorhi Alley vault
    spawn_arch_prop("SM_Arch_Overhead_Kucha", (0.0, 900.0, 380.0), (0.0, 0.0, 0.0), label="Arch_Overhead_Kucha_MidAlley")
    # Arch 3: Deorhi Alley into Well Square
    spawn_arch_prop("SM_Arch_Overhead_Kucha", (0.0, 1200.0, 380.0), (0.0, 0.0, 0.0), label="Arch_Overhead_Kucha_WellSquareEntry")
    # Arch 4: School Compound Entry Portal walkway
    spawn_arch_prop("SM_Arch_Overhead_Kucha", (800.0, 1350.0, 0.0), (0.0, 90.0, 0.0), label="Arch_Overhead_Kucha_SchoolEntry")

    # =========================================================================
    # 2. MONUMENTAL TOWN CHOWK GATE (Grand Bazaar Entrance Portal)
    # =========================================================================
    spawn_arch_prop("SM_Arch_Monumental_Chowk_Gate", (0.0, 1550.0, 0.0), (0.0, 0.0, 0.0), label="Arch_Monumental_Chowk_Gate")

    # =========================================================================
    # 3. COLONIAL VICTORIAN STREET LAMP POSTS (Illuminating key intersections)
    # =========================================================================
    spawn_arch_prop("SM_Street_Lamp_Post_Victorian", (180.0, 520.0, 0.0), (0.0, 45.0, 0.0), label="Street_Lamp_Post_HaveliCourtyard")
    spawn_arch_prop("SM_Street_Lamp_Post_Victorian", (-160.0, 1280.0, 0.0), (0.0, -30.0, 0.0), label="Street_Lamp_Post_WellSquareWest")
    spawn_arch_prop("SM_Street_Lamp_Post_Victorian", (240.0, 1420.0, 0.0), (0.0, 120.0, 0.0), label="Street_Lamp_Post_WellSquareEast")
    spawn_arch_prop("SM_Street_Lamp_Post_Victorian", (120.0, 1620.0, 0.0), (0.0, -45.0, 0.0), label="Street_Lamp_Post_BazaarChowk")
    spawn_arch_prop("SM_Street_Lamp_Post_Victorian", (-100.0, 2100.0, 0.0), (0.0, 60.0, 0.0), label="Street_Lamp_Post_BazaarCheckpoint")
    spawn_arch_prop("SM_Street_Lamp_Post_Victorian", (750.0, 1380.0, 0.0), (0.0, 90.0, 0.0), label="Street_Lamp_Post_SchoolGate")

    # =========================================================================
    # 4. BAZAAR KHADI AWNING CANOPIES (Creating covered market tunnels)
    # =========================================================================
    spawn_arch_prop("SM_Bazaar_Canopy_Khadi_Awning", (-200.0, 1950.0, 0.0), (0.0, 180.0, 0.0), label="Bazaar_Canopy_Khadi_NorthWest")
    spawn_arch_prop("SM_Bazaar_Canopy_Khadi_Awning", (200.0, 1950.0, 0.0), (0.0, 180.0, 0.0), label="Bazaar_Canopy_Khadi_NorthEast")
    spawn_arch_prop("SM_Bazaar_Canopy_Khadi_Awning", (-200.0, 1650.0, 0.0), (0.0, 0.0, 0.0), label="Bazaar_Canopy_Khadi_SouthWest")
    spawn_arch_prop("SM_Bazaar_Canopy_Khadi_Awning", (200.0, 1650.0, 0.0), (0.0, 0.0, 0.0), label="Bazaar_Canopy_Khadi_SouthEast")

    # =========================================================================
    # 5. STREET DRAINAGE GUTTERS & CROSSING FLAGSTONES
    # =========================================================================
    spawn_arch_prop("SM_Street_Drain_Stone_Gutter", (-220.0, 900.0, 0.0), (0.0, 0.0, 0.0), label="Street_Drain_Gutter_DeorhiWest")
    spawn_arch_prop("SM_Street_Drain_Stone_Gutter", (220.0, 900.0, 0.0), (0.0, 180.0, 0.0), label="Street_Drain_Gutter_DeorhiEast")
    spawn_arch_prop("SM_Street_Drain_Stone_Gutter", (0.0, 1920.0, 0.0), (0.0, 90.0, 0.0), label="Street_Drain_Gutter_BazaarNorth")
    spawn_arch_prop("SM_Street_Drain_Stone_Gutter", (0.0, 1680.0, 0.0), (0.0, -90.0, 0.0), label="Street_Drain_Gutter_BazaarSouth")

    # Save Level
    level_editor_sub.save_current_level()
    log("Saved L_Validation_Gym with Master Architectural Structures!")

if __name__ == "__main__":
    run_arrangement()
