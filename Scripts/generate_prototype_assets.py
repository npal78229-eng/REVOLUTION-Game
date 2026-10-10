"""
PROJECT REVOLUTION — 3D Asset Generator & Environment Prototype Builder
Toolchain: Blender 5.2.1 LTS Headless Pipeline
Generates KIT_PUNJABI_MOHALLA modular architecture, authentic period props,
and the assembled 100m x 100m Courtyard & Rooftop Gym Scene.
"""

import bpy
import bmesh
import math
import os
from mathutils import Vector, Matrix

# Base Paths
PROJECT_ROOT = r"C:\Users\npal7\PROJECT\REVOLUTION"
ART_DIR = os.path.join(PROJECT_ROOT, "Art")
BLENDER_DIR = os.path.join(ART_DIR, "Blender")
EXPORTS_DIR = os.path.join(ART_DIR, "Exports")

os.makedirs(BLENDER_DIR, exist_ok=True)
os.makedirs(EXPORTS_DIR, exist_ok=True)

def reset_scene():
    """Wipes current scene clean."""
    bpy.ops.wm.read_factory_settings(use_empty=True)

def get_pbr_material(name, base_color=(0.5, 0.5, 0.5, 1.0), roughness=0.7, metallic=0.0):
    """Retrieves or creates a standardized PBR Principled BSDF material in the active scene."""
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        bsdf = nodes.get("Principled BSDF")
        if bsdf:
            if "Base Color" in bsdf.inputs:
                bsdf.inputs["Base Color"].default_value = base_color
            if "Roughness" in bsdf.inputs:
                bsdf.inputs["Roughness"].default_value = roughness
            if "Metallic" in bsdf.inputs:
                bsdf.inputs["Metallic"].default_value = metallic
    return mat

def mat_brick():
    return get_pbr_material("M_LahoriBrick_PBR", (0.58, 0.22, 0.14, 1.0), roughness=0.85, metallic=0.0)

def mat_teak():
    return get_pbr_material("M_AgedTeak_PBR", (0.24, 0.14, 0.08, 1.0), roughness=0.55, metallic=0.0)

def mat_plaster():
    return get_pbr_material("M_LimePlaster_PBR", (0.82, 0.78, 0.70, 1.0), roughness=0.90, metallic=0.0)

def mat_iron():
    return get_pbr_material("M_WroughtIron_PBR", (0.12, 0.12, 0.13, 1.0), roughness=0.65, metallic=0.85)

def mat_jute():
    return get_pbr_material("M_JuteRope_PBR", (0.65, 0.52, 0.35, 1.0), roughness=0.92, metallic=0.0)

def mat_clay():
    return get_pbr_material("M_Terracotta_PBR", (0.68, 0.36, 0.20, 1.0), roughness=0.88, metallic=0.0)

def mat_brass():
    return get_pbr_material("M_AgedBrass_PBR", (0.75, 0.60, 0.25, 1.0), roughness=0.40, metallic=0.90)

# --- 1. MODULAR ARCHITECTURE MESH BUILDERS ---

def build_wall_solid(name="SM_Wall_Brick_4x4m_A"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((4.0, 0.4, 4.0, 1.0)))
    for v in bm.verts:
        v.co.z += 2.0

    cornice = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((4.1, 0.5, 0.2, 1.0)))
    for v in cornice['verts']:
        v.co.z += 3.9

    bm.to_mesh(mesh)
    bm.free()
    
    mesh.materials.append(mat_brick())
    mesh.materials.append(mat_plaster())
    return obj

def build_wall_doorway(name="SM_Wall_Brick_Doorway_4x4m"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()
    lp = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((1.1, 0.4, 4.0, 1.0)))
    for v in lp['verts']:
        v.co.x -= 1.45
        v.co.z += 2.0

    rp = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((1.1, 0.4, 4.0, 1.0)))
    for v in rp['verts']:
        v.co.x += 1.45
        v.co.z += 2.0

    top = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((4.0, 0.4, 1.2, 1.0)))
    for v in top['verts']:
        v.co.z += 3.4

    frame = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((2.0, 0.45, 0.15, 1.0)))
    for v in frame['verts']:
        v.co.z += 2.8

    bm.to_mesh(mesh)
    bm.free()
    mesh.materials.append(mat_brick())
    return obj

def build_wall_window(name="SM_Wall_Brick_Window_4x4m"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()
    bot = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((4.0, 0.4, 1.0, 1.0)))
    for v in bot['verts']:
        v.co.z += 0.5

    lp = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((1.3, 0.4, 2.0, 1.0)))
    for v in lp['verts']:
        v.co.x -= 1.35
        v.co.z += 2.0

    rp = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((1.3, 0.4, 2.0, 1.0)))
    for v in rp['verts']:
        v.co.x += 1.35
        v.co.z += 2.0

    top = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((4.0, 0.4, 1.0, 1.0)))
    for v in top['verts']:
        v.co.z += 3.5

    sill = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((1.6, 0.5, 0.1, 1.0)))
    for v in sill['verts']:
        v.co.z += 1.05

    bm.to_mesh(mesh)
    bm.free()
    mesh.materials.append(mat_brick())
    return obj

def build_jharokha_balcony(name="SM_Balcony_Jharokha_Wood_A"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()
    base = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((2.0, 1.0, 0.15, 1.0)))
    for v in base['verts']:
        v.co.y += 0.5
        v.co.z += 0.075

    for cx in [-0.7, 0.0, 0.7]:
        bracket = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.15, 0.8, 0.4, 1.0)))
        for v in bracket['verts']:
            v.co.x += cx
            v.co.y += 0.4
            v.co.z -= 0.2

    fr = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((2.0, 0.08, 0.9, 1.0)))
    for v in fr['verts']:
        v.co.y += 0.96
        v.co.z += 0.6

    for sx in [-0.96, 0.96]:
        sr = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.08, 1.0, 0.9, 1.0)))
        for v in sr['verts']:
            v.co.x += sx
            v.co.y += 0.5
            v.co.z += 0.6

    canopy = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((2.2, 1.2, 0.1, 1.0)))
    for v in canopy['verts']:
        v.co.y += 0.6
        v.co.z += 1.8

    bm.to_mesh(mesh)
    bm.free()
    mesh.materials.append(mat_teak())
    return obj

def build_deorhi_door(name="SM_Door_Deorhi_Teak_01"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()
    dl = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.88, 0.08, 2.7, 1.0)))
    for v in dl['verts']:
        v.co.x -= 0.45
        v.co.z += 1.35

    dr = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.88, 0.08, 2.7, 1.0)))
    for v in dr['verts']:
        v.co.x += 0.45
        v.co.z += 1.35

    for bz in [0.4, 1.0, 1.7, 2.3]:
        batten = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((1.8, 0.12, 0.14, 1.0)))
        for v in batten['verts']:
            v.co.z += bz

    latch = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.4, 0.16, 0.08, 1.0)))
    for v in latch['verts']:
        v.co.z += 1.35

    for sx in [-0.6, -0.3, 0.3, 0.6]:
        for sz in [0.7, 1.35, 2.0]:
            stud = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.06, 0.15, 0.06, 1.0)))
            for v in stud['verts']:
                v.co.x += sx
                v.co.z += sz

    bm.to_mesh(mesh)
    bm.free()
    mesh.materials.append(mat_teak())
    mesh.materials.append(mat_iron())
    mesh.materials.append(mat_brass())
    return obj

def build_roof_parapet(name="SM_Roof_Parapet_4m_A"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()
    pw = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((4.0, 0.3, 1.0, 1.0)))
    for v in pw['verts']:
        v.co.z += 0.5

    coping = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((4.05, 0.35, 0.1, 1.0)))
    for v in coping['verts']:
        v.co.z += 1.05

    bm.to_mesh(mesh)
    bm.free()
    mesh.materials.append(mat_brick())
    return obj

def build_masonry_stairs(name="SM_Roof_Stairs_Masonry_01"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()
    num_steps = 16
    step_height = 4.0 / num_steps
    step_depth = 3.6 / num_steps
    step_width = 1.2

    for i in range(num_steps):
        sz = (i + 1) * step_height
        sy = (i + 0.5) * step_depth
        step = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((step_width, step_depth, sz, 1.0)))
        for v in step['verts']:
            v.co.y += sy
            v.co.z += sz / 2.0

    bm.to_mesh(mesh)
    bm.free()
    mesh.materials.append(mat_brick())
    return obj

# --- 2. AUTHENTIC PERIOD PROP BUILDERS ---

def build_prop_charpai(name="SM_Prop_Charpai_RopeBed"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()
    for lx in [-0.9, 0.9]:
        for ly in [-0.42, 0.42]:
            leg = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.1, 0.1, 0.55, 1.0)))
            for v in leg['verts']:
                v.co.x += lx
                v.co.y += ly
                v.co.z += 0.275

    for ly in [-0.42, 0.42]:
        rail = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((1.8, 0.08, 0.08, 1.0)))
        for v in rail['verts']:
            v.co.y += ly
            v.co.z += 0.51

    for lx in [-0.9, 0.9]:
        srail = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.08, 0.84, 0.08, 1.0)))
        for v in srail['verts']:
            v.co.x += lx
            v.co.z += 0.51

    web = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((1.72, 0.76, 0.04, 1.0)))
    for v in web['verts']:
        v.co.z += 0.50

    bm.to_mesh(mesh)
    bm.free()
    mesh.materials.append(mat_teak())
    mesh.materials.append(mat_jute())
    return obj

def build_prop_lantern(name="SM_Prop_HurricaneLantern"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()
    base = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.16, 0.16, 0.08, 1.0)))
    for v in base['verts']:
        v.co.z += 0.04

    glass = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.10, 0.10, 0.20, 1.0)))
    for v in glass['verts']:
        v.co.z += 0.18

    for wx in [-0.08, 0.08]:
        guard = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.015, 0.015, 0.24, 1.0)))
        for v in guard['verts']:
            v.co.x += wx
            v.co.z += 0.18

    cap = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.12, 0.12, 0.06, 1.0)))
    for v in cap['verts']:
        v.co.z += 0.31

    handle = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.14, 0.01, 0.12, 1.0)))
    for v in handle['verts']:
        v.co.z += 0.40

    bm.to_mesh(mesh)
    bm.free()
    mesh.materials.append(mat_iron())
    return obj

def build_prop_grainsack(name="SM_Prop_GrainSack_Jute_01"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()
    sack = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.85, 0.55, 0.32, 1.0)))
    for v in sack['verts']:
        v.co.z += 0.16
        v.co.z -= 0.04 * (v.co.x * v.co.x)

    bm.to_mesh(mesh)
    bm.free()
    mesh.materials.append(mat_jute())
    return obj

def build_prop_kulhad(name="SM_Prop_ClayChaiCup_Kulhad"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()
    cup = bmesh.ops.create_cone(bm, segments=12, cap_ends=True, radius1=0.04, radius2=0.025, depth=0.10)
    for v in cup['verts']:
        v.co.z += 0.05

    bm.to_mesh(mesh)
    bm.free()
    mesh.materials.append(mat_clay())
    return obj

def build_prop_kite_spool(name="SM_Prop_Kite_Spool_Charkhi"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.03, 0.03, 0.34, 1.0)))
    for ez in [-0.12, 0.12]:
        plate = bmesh.ops.create_cone(bm, segments=6, cap_ends=True, radius1=0.08, radius2=0.08, depth=0.02)
        for v in plate['verts']:
            v.co.z += ez

    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.09, 0.09, 0.20, 1.0)))

    bm.to_mesh(mesh)
    bm.free()
    mesh.materials.append(mat_teak())
    return obj

# --- 3. EXPORT ALL MODULAR PIECES TO INDIVIDUAL FBX ---

def export_all_modular_pieces():
    reset_scene()
    print("--- BUILDING KIT_PUNJABI_MOHALLA ---")

    builders = [
        ("SM_Wall_Brick_4x4m_A", build_wall_solid),
        ("SM_Wall_Brick_Doorway_4x4m", build_wall_doorway),
        ("SM_Wall_Brick_Window_4x4m", build_wall_window),
        ("SM_Balcony_Jharokha_Wood_A", build_jharokha_balcony),
        ("SM_Door_Deorhi_Teak_01", build_deorhi_door),
        ("SM_Roof_Parapet_4m_A", build_roof_parapet),
        ("SM_Roof_Stairs_Masonry_01", build_masonry_stairs),
        ("SM_Prop_Charpai_RopeBed", build_prop_charpai),
        ("SM_Prop_HurricaneLantern", build_prop_lantern),
        ("SM_Prop_GrainSack_Jute_01", build_prop_grainsack),
        ("SM_Prop_ClayChaiCup_Kulhad", build_prop_kulhad),
        ("SM_Prop_Kite_Spool_Charkhi", build_prop_kite_spool)
    ]

    created_objects = []
    for name, builder_fn in builders:
        obj = builder_fn(name)
        created_objects.append(obj)

    master_blend_path = os.path.join(BLENDER_DIR, "KIT_Punjabi_Mohalla.blend")
    bpy.ops.wm.save_as_mainfile(filepath=master_blend_path)
    print(f"SAVED: Master Kit Library -> {master_blend_path}")

    for obj in created_objects:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        fbx_path = os.path.join(EXPORTS_DIR, f"{obj.name}.fbx")
        bpy.ops.export_scene.fbx(
            filepath=fbx_path,
            use_selection=True,
            global_scale=1.0,
            axis_forward='-Z',
            axis_up='Y',
            apply_unit_scale=True,
            apply_scale_options='FBX_SCALE_ALL',
            bake_space_transform=True,
            object_types={'MESH'}
        )
        print(f"EXPORTED: {obj.name}.fbx -> {fbx_path}")

# --- 4. BUILD THE COMPLETE ASSEMBLED ENVIRONMENT PROTOTYPE SCENE ---

def build_assembled_courtyard_scene():
    reset_scene()
    print("--- ASSEMBLING COURTYARD & ROOFTOP GYM SCENE ---")

    # 1. Ground Plane
    ground_mesh = bpy.data.meshes.new("SM_Ground_Courtyard_Paved")
    ground_obj = bpy.data.objects.new("SM_Ground_Courtyard_Paved", ground_mesh)
    bpy.context.scene.collection.objects.link(ground_obj)
    bm_g = bmesh.new()
    bmesh.ops.create_grid(bm_g, x_segments=10, y_segments=10, size=50.0)
    bm_g.to_mesh(ground_mesh)
    bm_g.free()
    ground_mesh.materials.append(mat_brick())

    def place_instance(mesh_obj, loc, rot_z_deg=0.0, name_prefix="Inst"):
        new_obj = bpy.data.objects.new(f"{name_prefix}_{mesh_obj.name}", mesh_obj.data)
        new_obj.location = Vector(loc)
        new_obj.rotation_euler.z = math.radians(rot_z_deg)
        bpy.context.scene.collection.objects.link(new_obj)
        return new_obj

    wall_solid = build_wall_solid("Temp_Wall")
    wall_door = build_wall_doorway("Temp_DoorWall")
    wall_win = build_wall_window("Temp_WinWall")
    jharokha = build_jharokha_balcony("Temp_Jharokha")
    door_gate = build_deorhi_door("Temp_Gate")
    parapet = build_roof_parapet("Temp_Parapet")
    stairs = build_masonry_stairs("Temp_Stairs")
    charpai = build_prop_charpai("Temp_Charpai")
    lantern = build_prop_lantern("Temp_Lantern")
    grainsack = build_prop_grainsack("Temp_Sack")
    kulhad = build_prop_kulhad("Temp_Kulhad")
    charkhi = build_prop_kite_spool("Temp_Charkhi")

    # Kabir's Two-Story Family House
    place_instance(wall_door, (0.0, 6.0, 0.0), 0.0, "KabirHouse_GF_Door")
    place_instance(door_gate, (0.0, 6.0, 0.0), 0.0, "KabirHouse_GF_Gate")
    place_instance(wall_win, (-4.0, 6.0, 0.0), 0.0, "KabirHouse_GF_WinL")
    place_instance(wall_solid, (4.0, 6.0, 0.0), 0.0, "KabirHouse_GF_WallR")
    
    place_instance(wall_win, (0.0, 6.0, 4.0), 0.0, "KabirHouse_1F_Win")
    place_instance(jharokha, (0.0, 6.2, 5.0), 0.0, "KabirHouse_1F_Jharokha")
    place_instance(wall_solid, (-4.0, 6.0, 4.0), 0.0, "KabirHouse_1F_WallL")
    place_instance(wall_solid, (4.0, 6.0, 4.0), 0.0, "KabirHouse_1F_WallR")

    # Rooftop 1
    place_instance(parapet, (0.0, 5.8, 8.0), 0.0, "Roof1_Parapet_Front")
    place_instance(parapet, (-4.0, 5.8, 8.0), 0.0, "Roof1_Parapet_FrontL")
    place_instance(parapet, (4.0, 5.8, 8.0), 0.0, "Roof1_Parapet_FrontR")

    # Stairs
    place_instance(stairs, (6.0, 2.0, 0.0), 90.0, "Courtyard_Stairs_Up")

    # Neighbor House
    place_instance(wall_solid, (-6.0, 2.0, 0.0), 90.0, "WestHouse_GF_Wall1")
    place_instance(wall_win, (-6.0, -2.0, 0.0), 90.0, "WestHouse_GF_Win2")
    place_instance(wall_solid, (-6.0, 2.0, 4.0), 90.0, "WestHouse_1F_Wall1")
    place_instance(jharokha, (-6.2, -2.0, 5.0), 90.0, "WestHouse_1F_Jharokha")
    place_instance(parapet, (-5.8, 2.0, 8.0), 90.0, "Roof2_Parapet_West")
    place_instance(parapet, (-5.8, -2.0, 8.0), 90.0, "Roof2_Parapet_WestS")

    # Alleyway
    place_instance(wall_solid, (-3.0, -8.0, 0.0), 90.0, "Alley_Wall_West")
    place_instance(wall_solid, (3.0, -8.0, 0.0), -90.0, "Alley_Wall_East")
    place_instance(wall_door, (3.0, -12.0, 0.0), -90.0, "Alley_Door_East")

    # Dressing Props
    place_instance(charpai, (1.5, 3.5, 8.0), 15.0, "Roof_Charpai")
    place_instance(charkhi, (1.8, 2.8, 8.55), 45.0, "Roof_KiteSpool")
    place_instance(lantern, (0.0, 5.7, 9.1), 0.0, "Roof_Lantern_Ledge")

    place_instance(grainsack, (-2.5, 4.5, 0.0), 25.0, "Courtyard_Sack1")
    place_instance(grainsack, (-2.1, 4.8, 0.0), -40.0, "Courtyard_Sack2")
    place_instance(grainsack, (-2.3, 4.6, 0.32), 10.0, "Courtyard_Sack3_Stacked")
    place_instance(kulhad, (1.2, 5.8, 0.8), 0.0, "Courtyard_ChaiCup1")
    place_instance(kulhad, (1.35, 5.75, 0.8), 0.0, "Courtyard_ChaiCup2")
    place_instance(lantern, (-1.5, 5.8, 1.2), 0.0, "Courtyard_Lantern_Doorway")

    templates = [wall_solid, wall_door, wall_win, jharokha, door_gate, parapet, stairs, charpai, lantern, grainsack, kulhad, charkhi]
    for t in templates:
        bpy.data.objects.remove(t, do_unlink=True)

    # Lighting
    sun_data = bpy.data.lights.new(name="Sun_GoldenHour_Punjab", type='SUN')
    sun_data.energy = 4.5
    sun_data.color = (1.0, 0.82, 0.62)
    sun_obj = bpy.data.objects.new("Sun_GoldenHour_Punjab", sun_data)
    sun_obj.rotation_euler = (math.radians(65.0), math.radians(15.0), math.radians(-35.0))
    bpy.context.scene.collection.objects.link(sun_obj)

    # Camera
    cam_data = bpy.data.cameras.new("Cam_Cinematic_Kabir_EyeLevel")
    cam_data.lens = 50.0
    cam_data.dof.use_dof = True
    cam_data.dof.focus_distance = 6.5
    cam_data.dof.aperture_fstop = 2.8
    cam_obj = bpy.data.objects.new("Cam_Cinematic_Kabir_EyeLevel", cam_data)
    cam_obj.location = Vector((0.0, -3.5, 1.4))
    cam_obj.rotation_euler = (math.radians(82.0), 0.0, 0.0)
    bpy.context.scene.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj

    scene_blend_path = os.path.join(BLENDER_DIR, "Courtyard_Rooftop_Gym_Scene.blend")
    bpy.ops.wm.save_as_mainfile(filepath=scene_blend_path)
    print(f"SAVED: Assembled Scene -> {scene_blend_path}")

    scene_fbx_path = os.path.join(EXPORTS_DIR, "Courtyard_Rooftop_Gym_Prototype.fbx")
    bpy.ops.export_scene.fbx(
        filepath=scene_fbx_path,
        global_scale=1.0,
        axis_forward='-Z',
        axis_up='Y',
        apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_ALL',
        bake_space_transform=True,
        object_types={'MESH'}
    )
    print(f"EXPORTED: Assembled Prototype FBX -> {scene_fbx_path}")

if __name__ == "__main__":
    export_all_modular_pieces()
    build_assembled_courtyard_scene()
    print("==================================================")
    print("  STAGE 6 PROTOTYPE GENERATION COMPLETE")
    print("==================================================")
