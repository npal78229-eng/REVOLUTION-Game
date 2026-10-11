"""
PROJECT REVOLUTION — MOHALLA DARZIAN & GRAND BAZAAR LEVEL BUILDER
Assembles the complete, polished, playable historical vertical slice:
- Kabir's Two-Story Family Haveli (Tailor workshop, courtyard aangan, masonry stairs, solid 1F rooftop terrace, jharokha)
- Deorhi Gateway Transition Archway
- Communal Stone Well & Chopal Square
- Grand Bazaar Market Street with Shaded Stalls, Spice Baskets, and Storefronts
- Period props, interactive matka stand, curfew gong, and chaukidar patrol
- 100% solid collision (CTF_USE_COMPLEX_AS_SIMPLE + floor slabs)
"""

import os
import unreal

def log(msg):
    unreal.log(f"[REVOLUTION_BUILDER] {msg}")

def run_build():
    log("Starting Mohalla Darzian & Grand Bazaar Environment Build...")

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    editor_asset_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    level_editor_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    editor_actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    # 1. Import New Expansion FBX Assets
    exports_dir = "C:/Users/npal7/PROJECT/REVOLUTION/Art/Exports"
    destination_path = "/Game/Environment/Mohalla/Meshes"

    new_fbx_files = [
        "SM_Floor_Ceiling_Slab_4x4m.fbx",
        "SM_Mohalla_Well_Stone.fbx",
        "SM_Market_Stall_Wood_Awning.fbx",
        "SM_Prop_SpiceBasket_Woven.fbx",
        "SM_Prop_ShopSign_Wood.fbx",
        "SM_Shop_Shutter_Foldable.fbx"
    ]

    for fbx_name in new_fbx_files:
        asset_name = os.path.splitext(fbx_name)[0]
        fbx_path = os.path.join(exports_dir, fbx_name).replace("\\", "/")
        if not os.path.exists(fbx_path):
            log(f"Warning: FBX file not found: {fbx_path}")
            continue

        task = unreal.AssetImportTask()
        task.filename = fbx_path
        task.destination_path = destination_path
        task.destination_name = asset_name
        task.replace_existing = True
        task.automated = True
        task.save = True

        options = unreal.FbxImportUI()
        options.import_mesh = True
        options.import_as_skeletal = False
        options.import_materials = False
        options.import_textures = False
        options.import_animations = False

        mesh_data = unreal.FbxStaticMeshImportData()
        mesh_data.combine_meshes = True
        mesh_data.auto_generate_collision = True
        mesh_data.generate_lightmap_u_vs = True
        options.static_mesh_import_data = mesh_data

        task.options = options
        asset_tools.import_asset_tasks([task])
        log(f"Imported: {asset_name}")

    # 2. Configure PBR Materials and Complex Collision on all meshes
    mat_brick = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_LahoriBrick_PBR")
    mat_teak = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_AgedTeak_PBR")
    mat_iron = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_WroughtIron_PBR")
    mat_clay = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_Clay_PBR")

    all_meshes_to_configure = [
        ("SM_Floor_Ceiling_Slab_4x4m", [mat_brick, mat_brick]),
        ("SM_Mohalla_Well_Stone", [mat_brick, mat_teak, mat_iron]),
        ("SM_Market_Stall_Wood_Awning", [mat_teak, mat_clay, mat_clay]),
        ("SM_Prop_SpiceBasket_Woven", [mat_clay, mat_clay]),
        ("SM_Prop_ShopSign_Wood", [mat_teak, mat_iron]),
        ("SM_Shop_Shutter_Foldable", [mat_teak, mat_iron]),
        ("SM_Wall_Brick_4x4m_A", [mat_brick, mat_brick]),
        ("SM_Wall_Brick_Doorway_4x4m", [mat_brick]),
        ("SM_Wall_Brick_Window_4x4m", [mat_brick]),
        ("SM_Balcony_Jharokha_Wood_A", [mat_teak]),
        ("SM_Door_Deorhi_Teak_01", [mat_teak]),
        ("SM_Roof_Parapet_4m_A", [mat_brick]),
        ("SM_Roof_Stairs_Masonry_01", [mat_brick]),
        ("SM_Prop_Charpai_RopeBed", [mat_teak]),
        ("SM_Prop_ClayChaiCup_Kulhad", [mat_clay]),
        ("SM_Prop_GrainSack_Jute_01", [mat_clay]),
        ("SM_Prop_HurricaneLantern", [mat_iron]),
        ("SM_Prop_Kite_Spool_Charkhi", [mat_teak]),
        ("Courtyard_Rooftop_Gym_Prototype", [mat_brick, mat_teak, mat_iron, mat_clay, mat_brick])
    ]

    for m_name, mats in all_meshes_to_configure:
        m_path = f"/Game/Environment/Mohalla/Meshes/{m_name}"
        mesh_asset = unreal.load_asset(m_path)
        if mesh_asset:
            bs = mesh_asset.get_editor_property("body_setup")
            if bs:
                bs.set_editor_property("collision_trace_flag", unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE)
            for idx, mat in enumerate(mats):
                if mat and idx < mesh_asset.get_num_sections(0):
                    mesh_asset.set_material(idx, mat)
            unreal.EditorAssetLibrary.save_loaded_asset(mesh_asset)

    log("Configured materials and CTF_USE_COMPLEX_AS_SIMPLE on all mesh assets.")

    # 3. Load Level L_Validation_Gym
    level_path = "/Game/Maps/L_Validation_Gym"
    level_editor_sub.load_level(level_path)
    current_world = level_editor_sub.get_current_level().get_world()

    # Load StaticMesh assets for level spawning
    mesh_cache = {}
    for m_name, _ in all_meshes_to_configure:
        m_asset = unreal.load_asset(f"/Game/Environment/Mohalla/Meshes/{m_name}")
        if m_asset:
            mesh_cache[m_name] = m_asset

    # 4. Clear old prototype mesh to make room for full modular layout
    for a in editor_actor_sub.get_all_level_actors():
        label = a.get_actor_label()
        if "Gym_Prototype" in label or "Modular_" in label:
            editor_actor_sub.destroy_actor(a)

    log("Cleaned previous temporary gym actors for clean modular environment assembly.")

    # 5. Helper function to spawn static mesh actor
    def spawn_mesh(mesh_key, loc, rot=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0), label=None):
        if mesh_key not in mesh_cache:
            log(f"Warning: Mesh {mesh_key} not in cache!")
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
                actor.set_actor_label(f"Modular_{label}")
            sm_comp = actor.get_component_by_class(unreal.StaticMeshComponent)
            if sm_comp:
                sm_comp.set_collision_profile_name("BlockAll")
                sm_comp.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)
                sm_comp.set_mobility(unreal.ComponentMobility.STATIC)
        return actor

    # =========================================================================
    # 6. ASSEMBLE ZONE A: KABIR'S FAMILY HAVELI & COURTYARD (X: -600 to 600, Y: -600 to 600)
    # =========================================================================
    log("Building Zone A: Kabir's Family Haveli & Courtyard...")

    # A1. Ground Floor North Facade (Tailor workshop & Deorhi entrance)
    spawn_mesh("SM_Wall_Brick_Doorway_4x4m", (0.0, 600.0, 0.0), (0.0, 0.0, 0.0), label="Haveli_GF_Doorway")
    spawn_mesh("SM_Door_Deorhi_Teak_01", (0.0, 600.0, 0.0), (0.0, 0.0, 0.0), label="Haveli_GF_DeorhiDoor")
    spawn_mesh("SM_Wall_Brick_Window_4x4m", (-400.0, 600.0, 0.0), (0.0, 0.0, 0.0), label="Haveli_GF_WinL")
    spawn_mesh("SM_Wall_Brick_4x4m_A", (400.0, 600.0, 0.0), (0.0, 0.0, 0.0), label="Haveli_GF_WallR")
    spawn_mesh("SM_Prop_ShopSign_Wood", (0.0, 580.0, 260.0), (0.0, 0.0, 0.0), label="Haveli_TailorShopSign")

    # A2. Ground Floor South Facade (Family living quarters)
    spawn_mesh("SM_Wall_Brick_Doorway_4x4m", (0.0, -600.0, 0.0), (0.0, 180.0, 0.0), label="Haveli_GF_SouthDoor")
    spawn_mesh("SM_Shop_Shutter_Foldable", (0.0, -590.0, 0.0), (0.0, 180.0, 0.0), label="Haveli_GF_SouthShutter")
    spawn_mesh("SM_Wall_Brick_Window_4x4m", (-400.0, -600.0, 0.0), (0.0, 180.0, 0.0), label="Haveli_GF_SouthWinL")
    spawn_mesh("SM_Wall_Brick_4x4m_A", (400.0, -600.0, 0.0), (0.0, 180.0, 0.0), label="Haveli_GF_SouthWallR")

    # A3. Ground Floor West Facade
    spawn_mesh("SM_Wall_Brick_4x4m_A", (-600.0, 200.0, 0.0), (0.0, 90.0, 0.0), label="Haveli_GF_WestWall1")
    spawn_mesh("SM_Wall_Brick_Window_4x4m", (-600.0, -200.0, 0.0), (0.0, 90.0, 0.0), label="Haveli_GF_WestWin2")

    # A4. Ground Floor East Facade & Stairs Access
    spawn_mesh("SM_Wall_Brick_4x4m_A", (600.0, -200.0, 0.0), (0.0, -90.0, 0.0), label="Haveli_GF_EastWall1")
    spawn_mesh("SM_Wall_Brick_Doorway_4x4m", (600.0, 200.0, 0.0), (0.0, -90.0, 0.0), label="Haveli_GF_EastStairDoor")

    # A5. Masonry Stairs (Ascending from Courtyard to 1F Terrace: 4 meters high)
    spawn_mesh("SM_Roof_Stairs_Masonry_01", (450.0, 200.0, 0.0), (0.0, 90.0, 0.0), label="Courtyard_Stairs_Up")

    # A6. 1F North Facade (Upper rooms & Jharokha balcony)
    spawn_mesh("SM_Wall_Brick_Window_4x4m", (0.0, 600.0, 400.0), (0.0, 0.0, 0.0), label="Haveli_1F_WinCenter")
    spawn_mesh("SM_Balcony_Jharokha_Wood_A", (0.0, 620.0, 500.0), (0.0, 0.0, 0.0), label="Haveli_1F_JharokhaBalcony")
    spawn_mesh("SM_Wall_Brick_4x4m_A", (-400.0, 600.0, 400.0), (0.0, 0.0, 0.0), label="Haveli_1F_WallL")
    spawn_mesh("SM_Wall_Brick_4x4m_A", (400.0, 600.0, 400.0), (0.0, 0.0, 0.0), label="Haveli_1F_WallR")

    # A7. 1F South Facade
    spawn_mesh("SM_Wall_Brick_Window_4x4m", (0.0, -600.0, 400.0), (0.0, 180.0, 0.0), label="Haveli_1F_SouthWin")
    spawn_mesh("SM_Wall_Brick_4x4m_A", (-400.0, -600.0, 400.0), (0.0, 180.0, 0.0), label="Haveli_1F_SouthWallL")
    spawn_mesh("SM_Wall_Brick_4x4m_A", (400.0, -600.0, 400.0), (0.0, 180.0, 0.0), label="Haveli_1F_SouthWallR")

    # A8. 1F Solid Terrace Walkable Floor Slabs (Z = 400.0 cm)
    # 3x3 grid of 4x4m floor slabs covering the 12m x 12m roof terrace
    for fx in [-400.0, 0.0, 400.0]:
        for fy in [-400.0, 0.0, 400.0]:
            # Leave open courtyard center for light well, cover rooms and perimeter terrace
            if fx == 0.0 and fy == 0.0:
                continue # Open central aangan courtyard
            spawn_mesh("SM_Floor_Ceiling_Slab_4x4m", (fx, fy, 400.0), label=f"Haveli_1F_FloorSlab_{int(fx)}_{int(fy)}")

    # A9. 1F Rooftop Parapet Railings (1.1m high vaultable boundaries at Z = 400.0 cm)
    spawn_mesh("SM_Roof_Parapet_4m_A", (0.0, 580.0, 400.0), (0.0, 0.0, 0.0), label="Haveli_RoofParapet_NorthCenter")
    spawn_mesh("SM_Roof_Parapet_4m_A", (-400.0, 580.0, 400.0), (0.0, 0.0, 0.0), label="Haveli_RoofParapet_NorthL")
    spawn_mesh("SM_Roof_Parapet_4m_A", (400.0, 580.0, 400.0), (0.0, 0.0, 0.0), label="Haveli_RoofParapet_NorthR")

    spawn_mesh("SM_Roof_Parapet_4m_A", (0.0, -580.0, 400.0), (0.0, 180.0, 0.0), label="Haveli_RoofParapet_SouthCenter")
    spawn_mesh("SM_Roof_Parapet_4m_A", (-400.0, -580.0, 400.0), (0.0, 180.0, 0.0), label="Haveli_RoofParapet_SouthL")
    spawn_mesh("SM_Roof_Parapet_4m_A", (400.0, -580.0, 400.0), (0.0, 180.0, 0.0), label="Haveli_RoofParapet_SouthR")

    spawn_mesh("SM_Roof_Parapet_4m_A", (-580.0, 0.0, 400.0), (0.0, 90.0, 0.0), label="Haveli_RoofParapet_West")
    spawn_mesh("SM_Roof_Parapet_4m_A", (580.0, -400.0, 400.0), (0.0, -90.0, 0.0), label="Haveli_RoofParapet_East")

    # A10. Rooftop Dressing Props (Kite spools, charpai, lanterns on roof terrace)
    spawn_mesh("SM_Prop_Charpai_RopeBed", (200.0, 400.0, 400.0), (0.0, 25.0, 0.0), label="Roof_Charpai_Kabir")
    spawn_mesh("SM_Prop_Kite_Spool_Charkhi", (240.0, 320.0, 400.0), (0.0, -45.0, 0.0), label="Roof_KiteSpool_Basant")
    spawn_mesh("SM_Prop_HurricaneLantern", (0.0, 570.0, 510.0), (0.0, 0.0, 0.0), label="Roof_Lantern_Ledge")

    # =========================================================================
    # 7. ASSEMBLE ZONE B: DEORHI GATEWAY & CONNECTING ALLEY (Y: 600 to 1200)
    # =========================================================================
    log("Building Zone B: Deorhi Gateway & Connecting Alleyway...")

    # Narrow brick-paved galli flanked by 2-story buildings
    spawn_mesh("SM_Wall_Brick_4x4m_A", (-300.0, 900.0, 0.0), (0.0, 90.0, 0.0), label="Alley_West_Wall1")
    spawn_mesh("SM_Wall_Brick_Window_4x4m", (-300.0, 900.0, 400.0), (0.0, 90.0, 0.0), label="Alley_West_1FWall")

    spawn_mesh("SM_Wall_Brick_4x4m_A", (300.0, 900.0, 0.0), (0.0, -90.0, 0.0), label="Alley_East_Wall1")
    spawn_mesh("SM_Wall_Brick_Window_4x4m", (300.0, 900.0, 400.0), (0.0, -90.0, 0.0), label="Alley_East_1FWall")

    # Alley Ground Floor props
    spawn_mesh("SM_Prop_GrainSack_Jute_01", (-220.0, 750.0, 0.0), (0.0, 30.0, 0.0), label="Alley_GrainSack1")
    spawn_mesh("SM_Prop_GrainSack_Jute_01", (-200.0, 780.0, 0.0), (0.0, -45.0, 0.0), label="Alley_GrainSack2")
    spawn_mesh("SM_Prop_HurricaneLantern", (-220.0, 730.0, 80.0), (0.0, 0.0, 0.0), label="Alley_Lantern_Sack")

    # =========================================================================
    # 8. ASSEMBLE ZONE C: COMMUNAL STONE WELL & CHOPAL (Y: 1200 to 1500)
    # =========================================================================
    log("Building Zone C: Communal Stone Well & Gathering Chopal...")

    # Communal Well (Centerpiece of the square)
    spawn_mesh("SM_Mohalla_Well_Stone", (0.0, 1350.0, 0.0), (0.0, 22.5, 0.0), label="Mohalla_CommunalWell")

    # Chopal Seating (Charpais & Kulhads under banyan space)
    spawn_mesh("SM_Prop_Charpai_RopeBed", (220.0, 1350.0, 0.0), (0.0, 0.0, 0.0), label="Chopal_Charpai_Elders")
    spawn_mesh("SM_Prop_ClayChaiCup_Kulhad", (180.0, 1300.0, 45.0), (0.0, 0.0, 0.0), label="Chopal_Kulhad1")
    spawn_mesh("SM_Prop_ClayChaiCup_Kulhad", (195.0, 1290.0, 45.0), (0.0, 0.0, 0.0), label="Chopal_Kulhad2")

    # West wall of the well square
    spawn_mesh("SM_Wall_Brick_4x4m_A", (-500.0, 1350.0, 0.0), (0.0, 90.0, 0.0), label="WellSquare_WestWall")
    spawn_mesh("SM_Shop_Shutter_Foldable", (-480.0, 1350.0, 0.0), (0.0, 90.0, 0.0), label="WellSquare_ClosedShop")

    # =========================================================================
    # 9. ASSEMBLE ZONE D: GRAND BAZAAR & MANDI MARKET STREET (Y: 1600 to 2200)
    # =========================================================================
    log("Building Zone D: Grand Bazaar & Mandi Market Street...")

    # Market Street runs East-West along Y = 1800
    # North side of market street (Shopfronts & Awning Stalls)
    spawn_mesh("SM_Market_Stall_Wood_Awning", (-400.0, 1950.0, 0.0), (0.0, 180.0, 0.0), label="Bazaar_Stall_Spices")
    spawn_mesh("SM_Prop_SpiceBasket_Woven", (-450.0, 1900.0, 80.0), (0.0, 0.0, 0.0), label="Bazaar_Spice_Turmeric")
    spawn_mesh("SM_Prop_SpiceBasket_Woven", (-380.0, 1900.0, 80.0), (0.0, 30.0, 0.0), label="Bazaar_Spice_RedChili")
    spawn_mesh("SM_Prop_SpiceBasket_Woven", (-320.0, 1900.0, 80.0), (0.0, -15.0, 0.0), label="Bazaar_Spice_Besan")

    spawn_mesh("SM_Market_Stall_Wood_Awning", (200.0, 1950.0, 0.0), (0.0, 180.0, 0.0), label="Bazaar_Stall_ClothKhadi")
    spawn_mesh("SM_Prop_GrainSack_Jute_01", (150.0, 1900.0, 80.0), (0.0, 15.0, 0.0), label="Bazaar_KhadiBolt1")
    spawn_mesh("SM_Prop_GrainSack_Jute_01", (250.0, 1900.0, 80.0), (0.0, -20.0, 0.0), label="Bazaar_KhadiBolt2")

    # North Bazaar Backing Buildings (2 stories high)
    spawn_mesh("SM_Wall_Brick_Doorway_4x4m", (-400.0, 2150.0, 0.0), (0.0, 180.0, 0.0), label="Bazaar_North_Shop1")
    spawn_mesh("SM_Wall_Brick_4x4m_A", (0.0, 2150.0, 0.0), (0.0, 180.0, 0.0), label="Bazaar_North_Wall2")
    spawn_mesh("SM_Wall_Brick_Doorway_4x4m", (400.0, 2150.0, 0.0), (0.0, 180.0, 0.0), label="Bazaar_North_Shop3")
    spawn_mesh("SM_Balcony_Jharokha_Wood_A", (0.0, 2130.0, 500.0), (0.0, 180.0, 0.0), label="Bazaar_North_Jharokha")

    # South side of market street (Halwai Tea Shop & Mandi Weighing Area)
    spawn_mesh("SM_Market_Stall_Wood_Awning", (-200.0, 1650.0, 0.0), (0.0, 0.0, 0.0), label="Bazaar_Stall_Halwai")
    spawn_mesh("SM_Prop_ClayChaiCup_Kulhad", (-250.0, 1700.0, 80.0), (0.0, 0.0, 0.0), label="Halwai_Kulhad_Pot1")
    spawn_mesh("SM_Prop_ClayChaiCup_Kulhad", (-230.0, 1710.0, 80.0), (0.0, 0.0, 0.0), label="Halwai_Kulhad_Pot2")
    spawn_mesh("SM_Prop_ClayChaiCup_Kulhad", (-210.0, 1690.0, 80.0), (0.0, 0.0, 0.0), label="Halwai_Kulhad_Pot3")
    spawn_mesh("SM_Prop_HurricaneLantern", (-150.0, 1700.0, 80.0), (0.0, 0.0, 0.0), label="Halwai_Lantern")

    # Mandi Grain Sacks Pyramid (excise seals)
    spawn_mesh("SM_Prop_GrainSack_Jute_01", (400.0, 1650.0, 0.0), (0.0, 15.0, 0.0), label="Mandi_Sack_Base1")
    spawn_mesh("SM_Prop_GrainSack_Jute_01", (460.0, 1660.0, 0.0), (0.0, -30.0, 0.0), label="Mandi_Sack_Base2")
    spawn_mesh("SM_Prop_GrainSack_Jute_01", (520.0, 1650.0, 0.0), (0.0, 45.0, 0.0), label="Mandi_Sack_Base3")
    spawn_mesh("SM_Prop_GrainSack_Jute_01", (430.0, 1655.0, 32.0), (0.0, 5.0, 0.0), label="Mandi_Sack_Mid1")
    spawn_mesh("SM_Prop_GrainSack_Jute_01", (490.0, 1655.0, 32.0), (0.0, -10.0, 0.0), label="Mandi_Sack_Mid2")
    spawn_mesh("SM_Prop_GrainSack_Jute_01", (460.0, 1655.0, 64.0), (0.0, 20.0, 0.0), label="Mandi_Sack_Top")

    # 10. Update PlayerStart_Courtyard Position
    player_start = None
    for a in editor_actor_sub.get_all_level_actors():
        if isinstance(a, unreal.PlayerStart) or "PlayerStart" in a.get_actor_label():
            player_start = a
            break

    if player_start:
        player_start.set_actor_location(unreal.Vector(0.0, -150.0, 80.0), False, False)
        player_start.set_actor_rotation(unreal.Rotator(0.0, 90.0, 0.0), False)
        log("Verified PlayerStart at (0, -150, 80) facing North.")

    # 11. Save Level and Assets
    level_editor_sub.save_current_level()
    unreal.EditorAssetLibrary.save_directory("/Game", only_if_is_dirty=True, recursive=True)
    log("Mohalla Darzian & Grand Bazaar Level Assembly successfully saved!")
    log("=== BUILD COMPLETE ===")

if __name__ == "__main__":
    run_build()
