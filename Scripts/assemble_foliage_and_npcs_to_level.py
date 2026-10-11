"""
PROJECT REVOLUTION — Level Assembler for Foliage & Narrative Civilian NPCs
Loads L_Validation_Gym and places:
1. Sacred Peepal Tree with Chabutra Shrine in Zone C Well Square
2. Courtyard Tulsi Pedestal Shrine in Zone A Haveli Courtyard
3. Manchester & Swadeshi Cloth Rolls in Zone D Bazaar Stall
4. Bhishti Leather Mashk Water-Skin in Zone C Well
5. Five Civilian NPCs:
   - Ram Lubhaya (Father / Master Tailor)
   - Ghasita Bhishti (Water-Carrier)
   - Hira Halwai (Chai Stall Owner)
   - Lala Karam Chand (Cloth Merchant)
   - Pandit Kashi Ram (School Headmaster)
"""

import unreal

def log(msg):
    unreal.log(f"[REVOLUTION_LEVEL_ASSEMBLER] {msg}")

def run_assemble():
    log("Starting Foliage and NPC Level Assembly...")

    level_editor_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    editor_actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    level_path = "/Game/Maps/L_Validation_Gym"
    level_editor_sub.load_level(level_path)

    # Cache Meshes
    mesh_keys = [
        "SM_Foliage_PeepalTree_Shrine",
        "SM_Prop_Tulsi_Pedestal",
        "SM_Prop_Bhishti_Mashk",
        "SM_Prop_ClothRolls_Manchester"
    ]
    mesh_cache = {}
    for mk in mesh_keys:
        m_obj = unreal.load_asset(f"/Game/Environment/Mohalla/Meshes/{mk}")
        if m_obj:
            mesh_cache[mk] = m_obj
            log(f"Cached mesh: {mk}")
        else:
            log(f"Warning: Failed to load mesh {mk}")

    def spawn_static_mesh(mesh_key, loc, rot=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0), label=None):
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

    # Remove any previous instances of these specific actors to avoid duplicates
    existing_actors = editor_actor_sub.get_all_level_actors()
    labels_to_clean = [
        "Foliage_PeepalTree_Shrine",
        "Prop_Tulsi_Pedestal",
        "Prop_ClothRolls_Manchester",
        "Prop_Bhishti_Mashk",
        "NPC_RamLubhaya_Father",
        "NPC_GhasitaBhishti_Water",
        "NPC_HiraHalwai_Chai",
        "NPC_LalaKaramChand_Cloth",
        "NPC_PanditKashiRam_Headmaster"
    ]
    for a in existing_actors:
        lbl = a.get_actor_label()
        if lbl in labels_to_clean:
            editor_actor_sub.destroy_actor(a)
            log(f"Cleaned existing actor: {lbl}")

    # 1. Place Historical Foliage & Nature Assets
    spawn_static_mesh("SM_Foliage_PeepalTree_Shrine", (380.0, 1350.0, 0.0), (0.0, 45.0, 0.0), label="Foliage_PeepalTree_Shrine")
    spawn_static_mesh("SM_Prop_Tulsi_Pedestal", (120.0, 80.0, 0.0), (0.0, 0.0, 0.0), label="Prop_Tulsi_Pedestal")
    spawn_static_mesh("SM_Prop_ClothRolls_Manchester", (240.0, 1920.0, 80.0), (0.0, 0.0, 0.0), label="Prop_ClothRolls_Manchester")
    spawn_static_mesh("SM_Prop_Bhishti_Mashk", (-60.0, 1310.0, 40.0), (0.0, 45.0, 0.0), label="Prop_Bhishti_Mashk")

    # 2. Place 5 Civilian NPCs using C++ ACivilianNPCActor class
    civ_class = unreal.load_class(None, "/Script/REVOLUTION.CivilianNPCActor")
    if civ_class:
        occ_enum = getattr(unreal, "CivilianOccupation", None)
        log(f"CivilianOccupation enum available: {occ_enum is not None}")
        if occ_enum:
            log(f"Enum members: {[m for m in dir(occ_enum) if not m.startswith('__')]}")

        npc_defs = [
            ("FATHER_TAILOR", (200.0, 480.0, 88.0), (0.0, 90.0, 0.0), "NPC_RamLubhaya_Father"),
            ("BHISHTI_WATER_CARRIER", (-80.0, 1320.0, 88.0), (0.0, 45.0, 0.0), "NPC_GhasitaBhishti_Water"),
            ("HALWAI_CHAI_VENDOR", (-200.0, 1680.0, 88.0), (0.0, 90.0, 0.0), "NPC_HiraHalwai_Chai"),
            ("CLOTH_MERCHANT", (200.0, 1980.0, 88.0), (0.0, -90.0, 0.0), "NPC_LalaKaramChand_Cloth"),
            ("SCHOOL_HEADMASTER", (1350.0, 1420.0, 88.0), (0.0, -90.0, 0.0), "NPC_PanditKashiRam_Headmaster")
        ]

        for enum_attr, loc, rot, label in npc_defs:
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
                civ_class,
                unreal.Vector(loc[0], loc[1], loc[2]),
                unreal.Rotator(rot[0], rot[1], rot[2])
            )
            if actor:
                actor.set_actor_label(label)
                if occ_enum and hasattr(occ_enum, enum_attr):
                    val = getattr(occ_enum, enum_attr)
                    actor.set_editor_property("occupation", val)
                    actor.configure_occupation(val)
                log(f"Spawned {label} ({enum_attr}) at {loc}")
    else:
        log("Warning: Failed to load /Script/REVOLUTION.CivilianNPCActor class")

    # Save level and dirty packages
    level_editor_sub.save_current_level()
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(False, True)
    unreal.EditorAssetLibrary.save_directory("/Game", only_if_is_dirty=True, recursive=True)
    log("=== Level Assembly Complete & Saved Successfully ===")

if __name__ == "__main__":
    run_assemble()
