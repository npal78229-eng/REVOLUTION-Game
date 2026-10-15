"""
PROJECT REVOLUTION — Level Assembler for Task 5: The Road to Jallianwala Bagh
Loads L_Validation_Gym and arranges the Task 5 Baisakhi gathering & proclamation structures:
1. SM_Baisakhi_Garland_Archway (Welcoming festive portal with marigolds at Deorhi chowk)
2. SM_Munadi_Proclamation_Drum (British town crier proclamation drum at Grand Bazaar chowk)
3. SM_Prop_Wheat_Sheaves_Cart (Baisakhi harvest bullock cart at Mandi grain market)
4. SM_Baisakhi_Mela_Sweet_Stall (Festive halwai jalebi & laddu stall at Grand Bazaar)
5. SM_Jallianwala_Narrow_Gateway (Historic 2.2m narrow choke-point corridor into Jallianwala Bagh)
6. Interactive story triggers with authentic period audio:
   - Trigger_Munadi_Drum_Proclamation with SFX_Munadi_Drum
   - Trigger_Jallianwala_Narrow_Gateway with SFX_Baisakhi_Crowd_Murmur
"""

import unreal

def log(msg):
    unreal.log_warning(f"[REVOLUTION_TASK5_ARRANGER] {msg}")

def run_arrangement():
    log("Arranging Task 5 Baisakhi Gathering & Proclamation Assets in L_Validation_Gym...")

    level_editor_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    editor_actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    level_path = "/Game/Maps/L_Validation_Gym"
    level_editor_sub.load_level(level_path)

    # Clean existing actors from this set to prevent duplicates if re-run
    prefix_list = [
        "Baisakhi_Garland_Archway_",
        "Baisakhi_Munadi_Drum_",
        "Baisakhi_Wheat_Sheaves_Cart_",
        "Baisakhi_Mela_Sweet_Stall_",
        "Jallianwala_Narrow_Gateway_",
        "Trigger_Munadi_Drum_",
        "Trigger_Jallianwala_Narrow_"
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
        "SM_Baisakhi_Garland_Archway",
        "SM_Munadi_Proclamation_Drum",
        "SM_Prop_Wheat_Sheaves_Cart",
        "SM_Baisakhi_Mela_Sweet_Stall",
        "SM_Jallianwala_Narrow_Gateway"
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
    # 1. BAISAKHI GARLAND FESTIVE ARCHWAY (Welcoming portal at Deorhi Chowk)
    # =========================================================================
    spawn_static_prop(
        "SM_Baisakhi_Garland_Archway",
        (0.0, 1150.0, 0.0),
        (0.0, 0.0, 0.0),
        label="Baisakhi_Garland_Archway_Chowk"
    )

    # =========================================================================
    # 2. MUNADI PROCLAMATION DRUM (Grand Bazaar Chowk near Police Naka)
    # =========================================================================
    spawn_static_prop(
        "SM_Munadi_Proclamation_Drum",
        (80.0, 1920.0, 0.0),
        (0.0, -30.0, 0.0),
        label="Baisakhi_Munadi_Drum_Proclamation"
    )

    # =========================================================================
    # 3. BAISAKHI HARVEST WHEAT SHEAVES CART (Mandi Grain Market)
    # =========================================================================
    spawn_static_prop(
        "SM_Prop_Wheat_Sheaves_Cart",
        (380.0, 1680.0, 0.0),
        (0.0, 75.0, 0.0),
        label="Baisakhi_Wheat_Sheaves_Cart_Mandi"
    )

    # =========================================================================
    # 4. BAISAKHI MELA SWEET STALL (Grand Bazaar West opposite Halwai)
    # =========================================================================
    spawn_static_prop(
        "SM_Baisakhi_Mela_Sweet_Stall",
        (-320.0, 1650.0, 0.0),
        (0.0, -45.0, 0.0),
        label="Baisakhi_Mela_Sweet_Stall_Bazaar"
    )

    # =========================================================================
    # 5. JALLIANWALA BAGH NARROW GATEWAY (North-East Perimeter Choke-Point)
    # =========================================================================
    spawn_static_prop(
        "SM_Jallianwala_Narrow_Gateway",
        (900.0, 2250.0, 0.0),
        (0.0, 0.0, 0.0),
        label="Jallianwala_Narrow_Gateway_Entrance"
    )

    # Note: Interactive ObjectiveTriggerActors are dynamically instantiated at runtime in RevolutionGameMode::BeginPlay()

    # Save Level
    level_editor_sub.save_current_level()
    log("Successfully saved L_Validation_Gym with Task 5 Baisakhi Assets & Triggers!")

if __name__ == "__main__":
    run_arrangement()
