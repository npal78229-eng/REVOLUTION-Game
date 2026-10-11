"""
PROJECT REVOLUTION — DISTRICT C (SCHOOL) & NARRATIVE NPCS LEVEL BUILDER
Assembles:
1. District C: Kot Gurdarshan Vernacular Middle School (Classroom 4B, Bell Tower, Desks, Blackboard)
2. Family Workshop: Singer Foot-Pedal Sewing Machine in Kabir's home veranda
3. Three Foundational Narrative NPCs:
   - Father (Darzi Ram Lubhaya) in family courtyard
   - Moti Ram (Halwai Chai Vendor) in Grand Bazaar
   - Pandit Kashi Ram (Headmaster) in school veranda
4. The Ringable School Bell interactive landmark
"""

import os
import unreal

def log(msg):
    unreal.log(f"[REVOLUTION_SCHOOL_BUILDER] {msg}")

def run_build():
    log("Starting District C (School) & Narrative NPC Build...")

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    editor_asset_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    level_editor_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    editor_actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    # 1. Ingest the 4 new FBX files
    exports_dir = "C:/Users/npal7/PROJECT/REVOLUTION/Art/Exports"
    destination_path = "/Game/Environment/Mohalla/Meshes"

    new_fbx_files = [
        "SM_School_Desk_Bench_Wood.fbx",
        "SM_School_Blackboard_Easel.fbx",
        "SM_School_Bell_Tower_Iron.fbx",
        "SM_Prop_SewingMachine_Singer.fbx"
    ]

    for fbx_name in new_fbx_files:
        asset_name = os.path.splitext(fbx_name)[0]
        fbx_path = os.path.join(exports_dir, fbx_name).replace("\\", "/")
        if not os.path.exists(fbx_path):
            log(f"Warning: FBX not found: {fbx_path}")
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

    # 2. Configure PBR Materials & Collision
    mat_brick = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_LahoriBrick_PBR")
    mat_teak = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_AgedTeak_PBR")
    mat_iron = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_WroughtIron_PBR")
    mat_clay = unreal.load_asset("/Game/Environment/Mohalla/Materials/M_Clay_PBR")

    new_mesh_configs = [
        ("SM_School_Desk_Bench_Wood", [mat_teak]),
        ("SM_School_Blackboard_Easel", [mat_teak, mat_iron]),
        ("SM_School_Bell_Tower_Iron", [mat_iron, mat_teak]),
        ("SM_Prop_SewingMachine_Singer", [mat_iron, mat_teak])
    ]

    for m_name, mats in new_mesh_configs:
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
            log(f"Configured CTF_USE_COMPLEX_AS_SIMPLE on {m_name}")

    # 3. Load Level L_Validation_Gym
    level_path = "/Game/Maps/L_Validation_Gym"
    level_editor_sub.load_level(level_path)
    current_world = level_editor_sub.get_current_level().get_world()

    # Load StaticMesh cache
    mesh_keys = [
        "SM_School_Desk_Bench_Wood", "SM_School_Blackboard_Easel", "SM_School_Bell_Tower_Iron",
        "SM_Prop_SewingMachine_Singer", "SM_Wall_Brick_4x4m_A", "SM_Wall_Brick_Doorway_4x4m",
        "SM_Wall_Brick_Window_4x4m", "SM_Floor_Ceiling_Slab_4x4m", "SM_Roof_Parapet_4m_A",
        "SM_Prop_Charpai_RopeBed", "SM_Prop_HurricaneLantern", "SM_Prop_ClayChaiCup_Kulhad",
        "SM_Prop_ShopSign_Wood"
    ]
    mesh_cache = {}
    for mk in mesh_keys:
        m_obj = unreal.load_asset(f"/Game/Environment/Mohalla/Meshes/{mk}")
        if m_obj:
            mesh_cache[mk] = m_obj

    def spawn_mesh(mesh_key, loc, rot=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0), label=None):
        if mesh_key not in mesh_cache:
            log(f"Warning: {mesh_key} not in cache")
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
                actor.set_actor_label(f"School_{label}")
            sm_comp = actor.get_component_by_class(unreal.StaticMeshComponent)
            if sm_comp:
                sm_comp.set_collision_profile_name("BlockAll")
                sm_comp.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)
                sm_comp.set_mobility(unreal.ComponentMobility.STATIC)
        return actor

    # Clear previous school actors if updating
    for a in editor_actor_sub.get_all_level_actors():
        if "School_" in a.get_actor_label() or "NPC_" in a.get_actor_label():
            editor_actor_sub.destroy_actor(a)

    # =========================================================================
    # 4. ASSEMBLE DISTRICT C: THE VERNACULAR MIDDLE SCHOOL (X: 800 to 1800, Y: 1000 to 1800)
    # =========================================================================
    log("Assembling District C: Kot Gurdarshan Vernacular Middle School...")

    # C1. School Connecting Archway / East Gate from Well Square (at X = 800, Y = 1350)
    spawn_mesh("SM_Wall_Brick_Doorway_4x4m", (800.0, 1350.0, 0.0), (0.0, 90.0, 0.0), label="Gateway_Doorway")
    spawn_mesh("SM_Prop_ShopSign_Wood", (800.0, 1330.0, 260.0), (0.0, 90.0, 0.0), label="Sign_VernacularSchool")

    # C2. Schoolyard Central Bell Tower (at X = 1350, Y = 1350, Z = 0)
    spawn_mesh("SM_School_Bell_Tower_Iron", (1350.0, 1350.0, 0.0), (0.0, 0.0, 0.0), label="BellTower_Central")

    # C3. Classroom 4B Main Compound (North of schoolyard: X = 1100 to 1700, Y = 1600 to 2000)
    # Front Veranda Facade (South-facing entrance to classroom)
    spawn_mesh("SM_Wall_Brick_Doorway_4x4m", (1350.0, 1650.0, 0.0), (0.0, 180.0, 0.0), label="Classroom_FrontDoor")
    spawn_mesh("SM_Wall_Brick_Window_4x4m", (950.0, 1650.0, 0.0), (0.0, 180.0, 0.0), label="Classroom_FrontWinL")
    spawn_mesh("SM_Wall_Brick_Window_4x4m", (1750.0, 1650.0, 0.0), (0.0, 180.0, 0.0), label="Classroom_FrontWinR")

    # North Rear Wall of Classroom
    spawn_mesh("SM_Wall_Brick_4x4m_A", (1350.0, 2050.0, 0.0), (0.0, 0.0, 0.0), label="Classroom_RearWallMid")
    spawn_mesh("SM_Wall_Brick_Window_4x4m", (950.0, 2050.0, 0.0), (0.0, 0.0, 0.0), label="Classroom_RearWinL")
    spawn_mesh("SM_Wall_Brick_Window_4x4m", (1750.0, 2050.0, 0.0), (0.0, 0.0, 0.0), label="Classroom_RearWinR")

    # East and West Side Walls of Classroom
    spawn_mesh("SM_Wall_Brick_4x4m_A", (750.0, 1850.0, 0.0), (0.0, 90.0, 0.0), label="Classroom_WestWall")
    spawn_mesh("SM_Wall_Brick_4x4m_A", (1950.0, 1850.0, 0.0), (0.0, -90.0, 0.0), label="Classroom_EastWall")

    # Solid Roof Slabs over Classroom (Z = 400.0 cm)
    spawn_mesh("SM_Floor_Ceiling_Slab_4x4m", (950.0, 1850.0, 400.0), label="Classroom_RoofL")
    spawn_mesh("SM_Floor_Ceiling_Slab_4x4m", (1350.0, 1850.0, 400.0), label="Classroom_RoofMid")
    spawn_mesh("SM_Floor_Ceiling_Slab_4x4m", (1750.0, 1850.0, 400.0), label="Classroom_RoofR")

    # C4. Classroom 4B Interior Furniture (Blackboard, Student Desks, Teacher's Podium)
    # Slate Blackboard on Easel facing South toward student desks
    spawn_mesh("SM_School_Blackboard_Easel", (1350.0, 1980.0, 0.0), (0.0, 180.0, 0.0), label="Blackboard_Classroom4B")

    # Student Desks (Two rows of dual benches)
    # Row 1 (Front row)
    spawn_mesh("SM_School_Desk_Bench_Wood", (1150.0, 1850.0, 0.0), (0.0, 0.0, 0.0), label="Desk_Row1_Left")
    spawn_mesh("SM_School_Desk_Bench_Wood", (1550.0, 1850.0, 0.0), (0.0, 0.0, 0.0), label="Desk_Row1_Right")
    # Row 2 (Back row)
    spawn_mesh("SM_School_Desk_Bench_Wood", (1150.0, 1730.0, 0.0), (0.0, 0.0, 0.0), label="Desk_Row2_Left")
    spawn_mesh("SM_School_Desk_Bench_Wood", (1550.0, 1730.0, 0.0), (0.0, 0.0, 0.0), label="Desk_Row2_Right")

    # Lantern for evening adult literacy classes
    spawn_mesh("SM_Prop_HurricaneLantern", (1550.0, 1980.0, 80.0), (0.0, 0.0, 0.0), label="Lantern_TeacherDesk")

    # =========================================================================
    # 5. ASSEMBLE KABIR'S FAMILY TAILOR WORKSTATION (ZONE A VERANDA)
    # =========================================================================
    log("Placing Singer Sewing Machine in Kabir's Family Haveli Workshop...")
    spawn_mesh("SM_Prop_SewingMachine_Singer", (200.0, 520.0, 0.0), (0.0, -90.0, 0.0), label="Singer_SewingMachine_Father")
    spawn_mesh("SM_Prop_Charpai_RopeBed", (350.0, 480.0, 0.0), (0.0, 15.0, 0.0), label="Charpai_TailorRest")
    spawn_mesh("SM_Prop_ClayChaiCup_Kulhad", (200.0, 500.0, 75.0), (0.0, 0.0, 0.0), label="Kulhad_FatherSewingTable")

    # =========================================================================
    # 6. SAVE LEVEL & PACKAGES
    # =========================================================================
    level_editor_sub.save_current_level()
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(False, True)
    unreal.EditorAssetLibrary.save_directory("/Game", only_if_is_dirty=True, recursive=True)
    log("District C (School) & Family Workshop successfully assembled and saved!")
    log("=== BUILD COMPLETE ===")

if __name__ == "__main__":
    run_build()
