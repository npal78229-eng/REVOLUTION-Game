import unreal

def log(msg):
    unreal.log_warning(f"[SCHOOL_ASSEMBLER] {msg}")

log("Starting District C (School) & Family Workshop Assembly...")

# 1. Configure collision and materials on existing meshes
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
        log(f"Configured CTF_USE_COMPLEX_AS_SIMPLE and materials on {m_name}")

# 2. Load Level
level_path = "/Game/Maps/L_Validation_Gym"
level_editor_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
level_editor_sub.load_level(level_path)

editor_actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

# 3. Clean any existing School_ or Workshop_ actors
for a in editor_actor_sub.get_all_level_actors():
    label = a.get_actor_label()
    if label.startswith("School_") or label.startswith("Workshop_") or "SewingMachine" in label:
        editor_actor_sub.destroy_actor(a)

mesh_cache = {}
mesh_names = [
    "SM_School_Desk_Bench_Wood", "SM_School_Blackboard_Easel", "SM_School_Bell_Tower_Iron",
    "SM_Prop_SewingMachine_Singer", "SM_Wall_Brick_4x4m_A", "SM_Wall_Brick_Doorway_4x4m",
    "SM_Wall_Brick_Window_4x4m", "SM_Floor_Ceiling_Slab_4x4m", "SM_Roof_Parapet_4m_A",
    "SM_Prop_Charpai_RopeBed", "SM_Prop_HurricaneLantern", "SM_Prop_ClayChaiCup_Kulhad",
    "SM_Prop_ShopSign_Wood"
]
for mn in mesh_names:
    m = unreal.load_asset(f"/Game/Environment/Mohalla/Meshes/{mn}")
    if m:
        mesh_cache[mn] = m

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
            actor.set_actor_label(label)
        sm_comp = actor.get_component_by_class(unreal.StaticMeshComponent)
        if sm_comp:
            sm_comp.set_collision_profile_name("BlockAll")
            sm_comp.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)
            sm_comp.set_mobility(unreal.ComponentMobility.STATIC)
    return actor

log("Spawning District C: Vernacular Middle School...")
# C1. Gateway from Well Square
spawn_mesh("SM_Wall_Brick_Doorway_4x4m", (800.0, 1350.0, 0.0), (0.0, 90.0, 0.0), label="School_Gateway_Arch")
spawn_mesh("SM_Prop_ShopSign_Wood", (800.0, 1330.0, 260.0), (0.0, 90.0, 0.0), label="School_Signboard")

# C2. School Central Bell Tower
spawn_mesh("SM_School_Bell_Tower_Iron", (1350.0, 1350.0, 0.0), (0.0, 0.0, 0.0), label="School_Bell_Tower")

# C3. Classroom 4B Main Compound (X: 750 to 1950, Y: 1650 to 2050)
spawn_mesh("SM_Wall_Brick_Doorway_4x4m", (1350.0, 1650.0, 0.0), (0.0, 180.0, 0.0), label="School_Classroom_Door")
spawn_mesh("SM_Wall_Brick_Window_4x4m", (950.0, 1650.0, 0.0), (0.0, 180.0, 0.0), label="School_Classroom_WinL")
spawn_mesh("SM_Wall_Brick_Window_4x4m", (1750.0, 1650.0, 0.0), (0.0, 180.0, 0.0), label="School_Classroom_WinR")

spawn_mesh("SM_Wall_Brick_4x4m_A", (1350.0, 2050.0, 0.0), (0.0, 0.0, 0.0), label="School_Classroom_RearMid")
spawn_mesh("SM_Wall_Brick_Window_4x4m", (950.0, 2050.0, 0.0), (0.0, 0.0, 0.0), label="School_Classroom_RearWinL")
spawn_mesh("SM_Wall_Brick_Window_4x4m", (1750.0, 2050.0, 0.0), (0.0, 0.0, 0.0), label="School_Classroom_RearWinR")

spawn_mesh("SM_Wall_Brick_4x4m_A", (750.0, 1850.0, 0.0), (0.0, 90.0, 0.0), label="School_Classroom_SideWest")
spawn_mesh("SM_Wall_Brick_4x4m_A", (1950.0, 1850.0, 0.0), (0.0, -90.0, 0.0), label="School_Classroom_SideEast")

# Roof Slabs at Z = 400
spawn_mesh("SM_Floor_Ceiling_Slab_4x4m", (950.0, 1850.0, 400.0), label="School_Roof_SlabL")
spawn_mesh("SM_Floor_Ceiling_Slab_4x4m", (1350.0, 1850.0, 400.0), label="School_Roof_SlabMid")
spawn_mesh("SM_Floor_Ceiling_Slab_4x4m", (1750.0, 1850.0, 400.0), label="School_Roof_SlabR")

# Classroom Interior Furniture
spawn_mesh("SM_School_Blackboard_Easel", (1350.0, 1980.0, 0.0), (0.0, 180.0, 0.0), label="School_Blackboard")
spawn_mesh("SM_School_Desk_Bench_Wood", (1150.0, 1850.0, 0.0), (0.0, 0.0, 0.0), label="School_Desk_Row1_L")
spawn_mesh("SM_School_Desk_Bench_Wood", (1550.0, 1850.0, 0.0), (0.0, 0.0, 0.0), label="School_Desk_Row1_R")
spawn_mesh("SM_School_Desk_Bench_Wood", (1150.0, 1730.0, 0.0), (0.0, 0.0, 0.0), label="School_Desk_Row2_L")
spawn_mesh("SM_School_Desk_Bench_Wood", (1550.0, 1730.0, 0.0), (0.0, 0.0, 0.0), label="School_Desk_Row2_R")
spawn_mesh("SM_Prop_HurricaneLantern", (1550.0, 1980.0, 80.0), (0.0, 0.0, 0.0), label="School_Teacher_Lantern")

log("Spawning Family Tailor Workshop in Zone A Courtyard...")
spawn_mesh("SM_Prop_SewingMachine_Singer", (200.0, 520.0, 0.0), (0.0, -90.0, 0.0), label="Workshop_SewingMachine_Singer")
spawn_mesh("SM_Prop_Charpai_RopeBed", (350.0, 480.0, 0.0), (0.0, 15.0, 0.0), label="Workshop_Charpai_TailorRest")
spawn_mesh("SM_Prop_ClayChaiCup_Kulhad", (200.0, 500.0, 75.0), (0.0, 0.0, 0.0), label="Workshop_ChaiKulhad_Father")

# 4. Save Level
unreal.EditorLevelLibrary.save_current_level()
log("District C & Family Workshop successfully assembled and saved to L_Validation_Gym!")
