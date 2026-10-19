"""
PROJECT REVOLUTION — Task 32 Setup Script:
Haveli Ground Floor Domestic Dressing & Village Exploration Boundaries
"""

import unreal

def log(msg):
    unreal.log_warning(f"[TASK_32_SETUP] {msg}")

def main():
    log("================================================================================")
    log("  TASK 32: FURNISH HAVELI GROUND FLOOR & ESTABLISH CLOSED BOUNDARIES")
    log("================================================================================")

    gym_map = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(gym_map)

    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    editor_asset_lib = unreal.EditorAssetLibrary

    # 1. Clean any previous Task 32 generated actors if rerun
    t32_prefixes = [
        "Haveli_GF_Charpai_Veranda",
        "Haveli_GF_Brass_Lota_Hearth",
        "Haveli_GF_Chai_Kulhads_Stove",
        "Haveli_GF_GrainSack_Jute_01",
        "Haveli_GF_GrainSack_Jute_02",
        "Haveli_GF_SpiceBasket_Woven",
        "Haveli_GF_Takhta_Shutter_TailorShop",
        "Haveli_GF_ClothRolls_Workbench",
        "Haveli_GF_HurricaneLantern_Niche",
        "Boundary_Wall_South_HaveliCenter",
        "Boundary_Wall_West_DeorhiGap",
        "Boundary_Wall_East_MohallaAlley",
        "Boundary_Barrier_NorthGate_West",
        "Boundary_Barrier_NorthGate_East",
        "Boundary_Wall_North_CantonmentSeal"
    ]

    all_actors = actor_sub.get_all_level_actors()
    for a in all_actors:
        lbl = a.get_actor_label()
        for pfx in t32_prefixes:
            if lbl == pfx or lbl.startswith(pfx + "_"):
                actor_sub.destroy_actor(a)
                log(f"Cleaned existing actor: {lbl}")
                break

    # 2. Cache Materials
    mat_jute = editor_asset_lib.load_asset("/Game/Environment/Mohalla/Materials/MI_WovenJute_Photogrammetry")
    mat_brass = editor_asset_lib.load_asset("/Game/Environment/Mohalla/Materials/MI_HammeredBrass_Photogrammetry")
    mat_clay = editor_asset_lib.load_asset("/Game/Environment/Mohalla/Materials/M_Clay_PBR")
    mat_teak = editor_asset_lib.load_asset("/Game/Environment/Mohalla/Materials/M_AgedTeak_PBR")
    mat_cotton = editor_asset_lib.load_asset("/Game/Environment/Mohalla/Materials/M_ClothUndyedCotton_PBR")
    mat_brick = editor_asset_lib.load_asset("/Game/Environment/Mohalla/Materials/M_LahoriBrick_PBR")
    mat_heritage = editor_asset_lib.load_asset("/Game/Environment/Mohalla/Materials/M_Master_Heritage_PBR")

    # 3. Item Manifest
    manifest = [
        # --- HAVELI GROUND FLOOR DOMESTIC DRESSING ---
        {
            "label": "Haveli_GF_Charpai_Veranda",
            "mesh": "/Game/Environment/Mohalla/Meshes/SM_Prop_Charpai_RopeBed",
            "loc": (280.0, 380.0, 0.0),
            "rot": (0.0, 0.0, 15.0),
            "scale": (1.0, 1.0, 1.0),
            "material": mat_jute,
            "category": "Haveli Domestic"
        },
        {
            "label": "Haveli_GF_Brass_Lota_Hearth",
            "mesh": "/Game/Environment/Mohalla/Meshes/SM_Prop_Overturned_Brass_Lota",
            "loc": (95.0, -55.0, 0.0),
            "rot": (0.0, 0.0, -30.0),
            "scale": (1.2, 1.2, 1.2),
            "material": mat_brass,
            "category": "Haveli Domestic"
        },
        {
            "label": "Haveli_GF_Chai_Kulhads_Stove",
            "mesh": "/Game/Environment/Mohalla/Meshes/SM_Prop_ClayChaiCup_Kulhad",
            "loc": (80.0, -95.0, 8.0),
            "rot": (0.0, 0.0, 10.0),
            "scale": (1.3, 1.3, 1.3),
            "material": mat_clay,
            "category": "Haveli Domestic"
        },
        {
            "label": "Haveli_GF_GrainSack_Jute_01",
            "mesh": "/Game/Environment/Mohalla/Meshes/SM_Prop_GrainSack_Jute_01",
            "loc": (170.0, -140.0, 0.0),
            "rot": (0.0, 0.0, 25.0),
            "scale": (1.1, 1.1, 1.1),
            "material": mat_jute,
            "category": "Haveli Domestic"
        },
        {
            "label": "Haveli_GF_GrainSack_Jute_02",
            "mesh": "/Game/Environment/Mohalla/Meshes/SM_Prop_GrainSack_Jute_01",
            "loc": (195.0, -105.0, 0.0),
            "rot": (0.0, 0.0, -45.0),
            "scale": (1.0, 1.0, 1.0),
            "material": mat_jute,
            "category": "Haveli Domestic"
        },
        {
            "label": "Haveli_GF_SpiceBasket_Woven",
            "mesh": "/Game/Environment/Mohalla/Meshes/SM_Prop_SpiceBasket_Woven",
            "loc": (35.0, -125.0, 0.0),
            "rot": (0.0, 0.0, 0.0),
            "scale": (1.0, 1.0, 1.0),
            "material": mat_jute,
            "category": "Haveli Domestic"
        },
        {
            "label": "Haveli_GF_Takhta_Shutter_TailorShop",
            "mesh": "/Game/Environment/Mohalla/Meshes/SM_Shop_Shutter_Foldable",
            "loc": (380.0, 580.0, 0.0),
            "rot": (0.0, 0.0, 90.0),
            "scale": (1.0, 1.0, 1.0),
            "material": mat_teak,
            "category": "Haveli Domestic"
        },
        {
            "label": "Haveli_GF_ClothRolls_Workbench",
            "mesh": "/Game/Environment/Mohalla/Meshes/SM_Prop_ClothRolls_Manchester",
            "loc": (500.0, 440.0, 0.0),
            "rot": (0.0, 0.0, 45.0),
            "scale": (0.85, 0.85, 0.85),
            "material": mat_cotton,
            "category": "Haveli Domestic"
        },
        {
            "label": "Haveli_GF_HurricaneLantern_Niche",
            "mesh": "/Game/Environment/Mohalla/Meshes/SM_Prop_HurricaneLantern",
            "loc": (140.0, -135.0, 50.0),
            "rot": (0.0, 0.0, 0.0),
            "scale": (1.0, 1.0, 1.0),
            "material": mat_brass,
            "category": "Haveli Domestic"
        },

        # --- VILLAGE EXPLORATION PERIMETER BOUNDARIES ---
        {
            "label": "Boundary_Wall_South_HaveliCenter",
            "mesh": "/Game/Environment/Mohalla/Meshes/SM_Wall_Brick_4x4m_A",
            "loc": (0.0, -600.0, 0.0),
            "rot": (0.0, 0.0, 0.0),
            "scale": (1.0, 1.0, 1.0),
            "material": mat_brick,
            "category": "Exploration Boundary"
        },
        {
            "label": "Boundary_Wall_West_DeorhiGap",
            "mesh": "/Game/Environment/Mohalla/Meshes/SM_Wall_Town_Faseel_Rampart",
            "loc": (-650.0, 350.0, 0.0),
            "rot": (0.0, 0.0, 90.0),
            "scale": (1.0, 1.0, 1.0),
            "material": mat_brick,
            "category": "Exploration Boundary"
        },
        {
            "label": "Boundary_Wall_East_MohallaAlley",
            "mesh": "/Game/Environment/Mohalla/Meshes/SM_Wall_Town_Faseel_Rampart",
            "loc": (650.0, 850.0, 0.0),
            "rot": (0.0, 0.0, 90.0),
            "scale": (1.0, 1.0, 1.0),
            "material": mat_brick,
            "category": "Exploration Boundary"
        },
        {
            "label": "Boundary_Barrier_NorthGate_West",
            "mesh": "/Game/Environment/Mohalla/Meshes/SM_Checkpoint_Picket_Sandbag_Barrier",
            "loc": (-180.0, 2150.0, 0.0),
            "rot": (0.0, 0.0, 15.0),
            "scale": (1.0, 1.0, 1.0),
            "material": mat_heritage,
            "category": "Exploration Boundary"
        },
        {
            "label": "Boundary_Barrier_NorthGate_East",
            "mesh": "/Game/Environment/Mohalla/Meshes/SM_Checkpoint_Picket_Sandbag_Barrier",
            "loc": (180.0, 2150.0, 0.0),
            "rot": (0.0, 0.0, -15.0),
            "scale": (1.0, 1.0, 1.0),
            "material": mat_heritage,
            "category": "Exploration Boundary"
        },
        {
            "label": "Boundary_Wall_North_CantonmentSeal",
            "mesh": "/Game/Environment/Mohalla/Meshes/SM_Wall_Brick_4x4m_A",
            "loc": (0.0, 2250.0, 0.0),
            "rot": (0.0, 0.0, 0.0),
            "scale": (1.0, 1.0, 1.5),
            "material": mat_brick,
            "category": "Exploration Boundary"
        }
    ]

    spawned_count = 0
    for item in manifest:
        mesh_obj = editor_asset_lib.load_asset(item["mesh"])
        assert mesh_obj is not None, f"Mesh asset missing: {item['mesh']}!"
        
        actor = actor_sub.spawn_actor_from_class(
            unreal.StaticMeshActor,
            unreal.Vector(item["loc"][0], item["loc"][1], item["loc"][2]),
            unreal.Rotator(item["rot"][0], item["rot"][1], item["rot"][2])
        )
        assert actor is not None, f"Failed to spawn actor: {item['label']}!"
        
        actor.set_actor_label(item["label"])
        actor.set_actor_scale3d(unreal.Vector(item["scale"][0], item["scale"][1], item["scale"][2]))

        sm_comp = actor.get_component_by_class(unreal.StaticMeshComponent)
        if sm_comp:
            sm_comp.set_static_mesh(mesh_obj)
            sm_comp.set_collision_profile_name("BlockAll")
            if item["material"]:
                sm_comp.set_material(0, item["material"])

        spawned_count += 1
        log(f"  [SPAWNED {item['category']}] {item['label']} at {item['loc']}")

    log(f"[PASS] Successfully spawned and dressed {spawned_count} Haveli props and boundary elements.")

    # 4. Save Level State
    level_sub.save_current_level()
    log("[PASS] Validation gym level state preserved and saved.")

    log("================================================================================")
    log("  TASK 32 HAVELI & BOUNDARIES SETUP COMPLETED: 100% SUCCESS")
    log("================================================================================")

if __name__ == "__main__":
    main()
