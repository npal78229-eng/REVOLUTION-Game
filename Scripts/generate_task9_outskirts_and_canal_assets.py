"""
PROJECT REVOLUTION — Task 9: Outskirts & The Upper Bari Doab Canal
Blender 5.2 LTS Headless Asset Generator: Aqueduct, Persian Wheel, Brick Kiln & Supply Cache
Generates 4 authentic historical and gameplay environment assets:
1. SM_Canal_Distributary_Aqueduct_Stone: Masonry canal culvert with sluice gate regulator & gantry
2. SM_Persian_Wheel_Rahat_Timber: Traditional Punjabi Persian wheel (Rahat) with buckets & draft beam
3. SM_Brick_Kiln_Chimney_Bhatta: Traditional Bull's trench brick kiln (Bhatta) chimney & brick hacks
4. SM_Prop_Clandestine_Safehouse_Crate_Cache: Disguised resistance supply cache with bicycle & crates
"""

import bpy
import bmesh
import math
import os
import random
import shutil
from mathutils import Vector, Matrix

PROJECT_ROOT = r"C:\Users\npal7\PROJECT\REVOLUTION"
ART_DIR = os.path.join(PROJECT_ROOT, "Art")
BLENDER_DIR = os.path.join(ART_DIR, "Blender")
EXPORTS_DIR = os.path.join(ART_DIR, "Exports")
ART_PROJECT_DIR = os.path.join(ART_DIR, "PROJECT")
USER_PROJECT_DIR = r"C:\Users\npal7\PROJECT\PROJECT"

for d in [BLENDER_DIR, EXPORTS_DIR, ART_PROJECT_DIR, USER_PROJECT_DIR]:
    os.makedirs(d, exist_ok=True)

def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def add_cylinder(bm, radius, depth, segments=16, matrix=Matrix()):
    bmesh.ops.create_cone(bm, cap_ends=True, segments=segments, radius1=radius, radius2=radius, depth=depth, matrix=matrix)

def get_pbr_material(name, base_color=(0.5, 0.5, 0.5, 1.0), roughness=0.7, metallic=0.0):
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

def mat_lahori_brick():
    return get_pbr_material("M_LahoriBrick_PBR", (0.58, 0.22, 0.14, 1.0), roughness=0.85, metallic=0.0)

def mat_aged_teak():
    return get_pbr_material("M_AgedTeak_PBR", (0.34, 0.22, 0.14, 1.0), roughness=0.78, metallic=0.0)

def mat_wrought_iron():
    return get_pbr_material("M_WroughtIron_PBR", (0.12, 0.12, 0.13, 1.0), roughness=0.62, metallic=0.88)

def mat_cloth_white():
    return get_pbr_material("M_ClothUndyedCotton_PBR", (0.88, 0.85, 0.78, 1.0), roughness=0.88, metallic=0.0)

def mat_dirt():
    return get_pbr_material("M_DirtRoad_PBR", (0.52, 0.42, 0.30, 1.0), roughness=0.95, metallic=0.0)

def mat_clay():
    return get_pbr_material("M_Clay_PBR", (0.64, 0.44, 0.30, 1.0), roughness=0.82, metallic=0.0)


# =========================================================================
# 1. CANAL DISTRIBUTARY AQUEDUCT & SLUICE (SM_Canal_Distributary_Aqueduct_Stone)
# =========================================================================
def build_canal_distributary_aqueduct(name="SM_Canal_Distributary_Aqueduct_Stone"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Material slots: 0: Brick, 1: Iron, 2: Teak
    mat_brick = mat_lahori_brick()
    mat_iron = mat_wrought_iron()
    mat_teak = mat_aged_teak()
    obj.data.materials.append(mat_brick)
    obj.data.materials.append(mat_iron)
    obj.data.materials.append(mat_teak)

    # A. Stone invert bed (Channel bottom: 2.0m wide between X = -1.0 and +1.0, 6.0m long Y = -3.0 to +3.0)
    bmesh.ops.create_cube(bm, size=1.0, matrix=
        Matrix.Translation(Vector((0.0, 0.0, 0.125))) @
        Matrix.Scale(2.0, 4, Vector((1,0,0))) @
        Matrix.Scale(6.0, 4, Vector((0,1,0))) @
        Matrix.Scale(0.25, 4, Vector((0,0,1))))

    # B. Left & Right Masonry Revetment Walls (0.8m thick, 2.2m high)
    for sign in [-1.0, 1.0]:
        wall_x = sign * 1.40  # Centers at -1.4m and +1.4m (inner face at +/-1.0m, outer face at +/-1.8m)
        # Main brick wall
        bmesh.ops.create_cube(bm, size=1.0, matrix=
            Matrix.Translation(Vector((wall_x, 0.0, 1.10))) @
            Matrix.Scale(0.80, 4, Vector((1,0,0))) @
            Matrix.Scale(6.00, 4, Vector((0,1,0))) @
            Matrix.Scale(2.20, 4, Vector((0,0,1))))

        # Stepped stone coping on top (Z = 2.20 to 2.35m, 0.9m wide with overhang)
        bmesh.ops.create_cube(bm, size=1.0, matrix=
            Matrix.Translation(Vector((wall_x, 0.0, 2.275))) @
            Matrix.Scale(0.92, 4, Vector((1,0,0))) @
            Matrix.Scale(6.08, 4, Vector((0,1,0))) @
            Matrix.Scale(0.15, 4, Vector((0,0,1))))

        # 45-degree Upstream flared training wing wall (at Y = -3.0m)
        wing_mat = Matrix.Translation(Vector((wall_x, -3.0, 1.10))) @ \
                   Matrix.Rotation(math.radians(-sign * 35.0), 3, 'Z').to_4x4() @ \
                   Matrix.Translation(Vector((0.0, -0.9, 0.0))) @ \
                   Matrix.Scale(0.70, 4, Vector((1,0,0))) @ \
                   Matrix.Scale(1.80, 4, Vector((0,1,0))) @ \
                   Matrix.Scale(2.20, 4, Vector((0,0,1)))
        bmesh.ops.create_cube(bm, size=1.0, matrix=wing_mat)

    # Assign Brick material to current faces
    bm.faces.ensure_lookup_table()
    for f in bm.faces:
        f.material_index = 0

    iron_faces_start = len(bm.faces)

    # C. Sluice Gate Mechanism (Located at Y = 0.0m)
    # Iron Guide Channels on inner wall faces (X = -1.0m and +1.0m)
    for sign in [-1.0, 1.0]:
        bmesh.ops.create_cube(bm, size=1.0, matrix=
            Matrix.Translation(Vector((sign * 0.97, 0.0, 1.25))) @
            Matrix.Scale(0.08, 4, Vector((1,0,0))) @
            Matrix.Scale(0.16, 4, Vector((0,1,0))) @
            Matrix.Scale(2.30, 4, Vector((0,0,1))))

    # Sluice Gate Sheet Plate (2.0m wide, 1.35m high, slightly lifted to Z = 0.35m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=
        Matrix.Translation(Vector((0.0, 0.0, 1.025))) @
        Matrix.Scale(1.98, 4, Vector((1,0,0))) @
        Matrix.Scale(0.06, 4, Vector((0,1,0))) @
        Matrix.Scale(1.35, 4, Vector((0,0,1))))

    # Horizontal reinforcing ribs on the gate plate
    for rib_z in [0.55, 0.95, 1.35, 1.65]:
        bmesh.ops.create_cube(bm, size=1.0, matrix=
            Matrix.Translation(Vector((0.0, 0.0, rib_z))) @
            Matrix.Scale(1.96, 4, Vector((1,0,0))) @
            Matrix.Scale(0.10, 4, Vector((0,1,0))) @
            Matrix.Scale(0.05, 4, Vector((0,0,1))))

    # Twin vertical gear rack stems (at X = -0.55m and +0.55m, rising to Z = 2.85m)
    for sign in [-1.0, 1.0]:
        bmesh.ops.create_cube(bm, size=1.0, matrix=
            Matrix.Translation(Vector((sign * 0.55, 0.0, 2.05))) @
            Matrix.Scale(0.07, 4, Vector((1,0,0))) @
            Matrix.Scale(0.07, 4, Vector((0,1,0))) @
            Matrix.Scale(1.70, 4, Vector((0,0,1))))

    # Twin Cast-Iron Handwheels (mounted on operating stands at Z = 2.45m)
    for sign in [-1.0, 1.0]:
        wheel_mat = Matrix.Translation(Vector((sign * 0.55, 0.0, 2.45))) @ \
                    Matrix.Rotation(math.radians(90.0), 3, 'X').to_4x4()
        # Wheel rim
        bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=0.25, radius2=0.25, depth=0.04,
                              matrix=wheel_mat)
        # Hub
        bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.07, radius2=0.07, depth=0.08,
                              matrix=wheel_mat)
        # Crank handle
        add_cylinder(bm, radius=0.02, depth=0.14, segments=8,
                     matrix=Matrix.Translation(Vector((sign * 0.55, -0.08, 2.65))))

    # Pipe safety handrail across catwalk (Z = 2.35m to 3.25m, at Y = 0.55m)
    add_cylinder(bm, radius=0.025, depth=3.60, segments=8,
                 matrix=Matrix.Translation(Vector((0.0, 0.55, 3.20))) @
                 Matrix.Rotation(math.radians(90.0), 3, 'Y').to_4x4())
    # Upright stanchions
    for st_x in [-1.4, -0.6, 0.6, 1.4]:
        add_cylinder(bm, radius=0.025, depth=0.90, segments=8,
                     matrix=Matrix.Translation(Vector((st_x, 0.55, 2.75))))

    # Assign Iron material to iron faces
    bm.faces.ensure_lookup_table()
    for idx in range(iron_faces_start, len(bm.faces)):
        bm.faces[idx].material_index = 1

    teak_faces_start = len(bm.faces)

    # D. Teak Overhead Gantry Beam & Inspection Catwalk
    # Heavy lintel crossbeam (0.24m x 0.24m x 2.8m long spanning revetments at Y = 0.0, Z = 2.32m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=
        Matrix.Translation(Vector((0.0, 0.0, 2.32))) @
        Matrix.Scale(2.80, 4, Vector((1,0,0))) @
        Matrix.Scale(0.24, 4, Vector((0,1,0))) @
        Matrix.Scale(0.24, 4, Vector((0,0,1))))

    # Catwalk timber planks (spanning between revetments at Y = 0.35m, Z = 2.24m)
    for plank_i in range(5):
        py = 0.15 + plank_i * 0.12
        bmesh.ops.create_cube(bm, size=1.0, matrix=
            Matrix.Translation(Vector((0.0, py, 2.24))) @
            Matrix.Scale(2.02, 4, Vector((1,0,0))) @
            Matrix.Scale(0.10, 4, Vector((0,1,0))) @
            Matrix.Scale(0.04, 4, Vector((0,0,1))))

    # Assign Teak material to wood faces
    bm.faces.ensure_lookup_table()
    for idx in range(teak_faces_start, len(bm.faces)):
        bm.faces[idx].material_index = 2

    bm.to_mesh(mesh)
    bm.free()

    # UV Unwrap
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.02)
    bpy.ops.object.mode_set(mode='OBJECT')

    return obj


# =========================================================================
# 2. PUNJABI PERSIAN WHEEL RAHAT (SM_Persian_Wheel_Rahat_Timber)
# =========================================================================
def build_persian_wheel_rahat(name="SM_Persian_Wheel_Rahat_Timber"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Material slots: 0: Teak, 1: Clay, 2: Iron
    mat_teak = mat_aged_teak()
    mat_clay_mat = mat_clay()
    mat_iron = mat_wrought_iron()
    obj.data.materials.append(mat_teak)
    obj.data.materials.append(mat_clay_mat)
    obj.data.materials.append(mat_iron)

    # A. Vertical Water Wheel Frame (Radius 1.5m, center axle at X=0, Y=0, Z=1.60m)
    # Heavy Central Teak Hub
    hub_mat = Matrix.Translation(Vector((0.0, 0.0, 1.60))) @ \
              Matrix.Rotation(math.radians(90.0), 3, 'Y').to_4x4()
    add_cylinder(bm, radius=0.22, depth=0.45, segments=16, matrix=hub_mat)

    # 8 Radial Spokes connecting hub to rim
    for i in range(8):
        angle = math.radians(i * 45.0)
        spoke_rot = Matrix.Translation(Vector((0.0, 0.0, 1.60))) @ \
                    Matrix.Rotation(angle, 3, 'X').to_4x4() @ \
                    Matrix.Translation(Vector((0.0, 0.70, 0.0)))
        bmesh.ops.create_cube(bm, size=1.0, matrix=spoke_rot @
                              Matrix.Scale(0.10, 4, Vector((1,0,0))) @
                              Matrix.Scale(1.30, 4, Vector((0,1,0))) @
                              Matrix.Scale(0.08, 4, Vector((0,0,1))))

    # Double Wooden Rim Rings (Outer rim R=1.50m, inner rim R=1.35m)
    num_rim_segs = 24
    for s in range(num_rim_segs):
        a1 = math.radians(s * (360.0 / num_rim_segs))
        a2 = math.radians((s + 1) * (360.0 / num_rim_segs))
        mid_a = (a1 + a2) / 2.0
        seg_len = 2.0 * math.pi * 1.45 / num_rim_segs
        
        # Dual rims (X = -0.16m and +0.16m)
        for rx in [-0.16, 0.16]:
            seg_mat = Matrix.Translation(Vector((rx, 0.0, 1.60))) @ \
                      Matrix.Rotation(mid_a, 3, 'X').to_4x4() @ \
                      Matrix.Translation(Vector((0.0, 1.45, 0.0))) @ \
                      Matrix.Rotation(math.radians(90.0), 3, 'Z').to_4x4()
            bmesh.ops.create_cube(bm, size=1.0, matrix=seg_mat @
                                  Matrix.Scale(0.08, 4, Vector((1,0,0))) @
                                  Matrix.Scale(seg_len * 1.05, 4, Vector((0,1,0))) @
                                  Matrix.Scale(0.12, 4, Vector((0,0,1))))

    # Cross-rungs between rims
    for r in range(16):
        ra = math.radians(r * (360.0 / 16.0))
        rung_mat = Matrix.Translation(Vector((0.0, 0.0, 1.60))) @ \
                   Matrix.Rotation(ra, 3, 'X').to_4x4() @ \
                   Matrix.Translation(Vector((0.0, 1.45, 0.0))) @ \
                   Matrix.Rotation(math.radians(90.0), 3, 'Y').to_4x4()
        add_cylinder(bm, radius=0.035, depth=0.36, segments=8, matrix=rung_mat)

    # B. Supporting A-frame Timber Trestle Piers (supporting horizontal axle)
    for px in [-0.45, 0.45]:
        # Left leg
        bmesh.ops.create_cube(bm, size=1.0, matrix=
            Matrix.Translation(Vector((px, -0.40, 0.80))) @
            Matrix.Rotation(math.radians(-14.0), 3, 'X').to_4x4() @
            Matrix.Scale(0.14, 4, Vector((1,0,0))) @
            Matrix.Scale(0.14, 4, Vector((0,1,0))) @
            Matrix.Scale(1.70, 4, Vector((0,0,1))))
        # Right leg
        bmesh.ops.create_cube(bm, size=1.0, matrix=
            Matrix.Translation(Vector((px, 0.40, 0.80))) @
            Matrix.Rotation(math.radians(14.0), 3, 'X').to_4x4() @
            Matrix.Scale(0.14, 4, Vector((1,0,0))) @
            Matrix.Scale(0.14, 4, Vector((0,1,0))) @
            Matrix.Scale(1.70, 4, Vector((0,0,1))))
        # Top bearing cap
        bmesh.ops.create_cube(bm, size=1.0, matrix=
            Matrix.Translation(Vector((px, 0.0, 1.58))) @
            Matrix.Scale(0.18, 4, Vector((1,0,0))) @
            Matrix.Scale(0.35, 4, Vector((0,1,0))) @
            Matrix.Scale(0.12, 4, Vector((0,0,1))))

    # C. Horizontal Spur Gear Transmission & Bullock Draught Yoke
    # Vertical shaft upright at X = 1.45m, Y = 0.0m (Z = 0.0 to 2.2m)
    add_cylinder(bm, radius=0.12, depth=2.20, segments=12,
                 matrix=Matrix.Translation(Vector((1.45, 0.0, 1.10))))

    # Horizontal spur gear wheel (R = 0.85m at Z = 1.25m)
    add_cylinder(bm, radius=0.85, depth=0.12, segments=24,
                 matrix=Matrix.Translation(Vector((1.45, 0.0, 1.25))))
    # 16 Wooden gear pegs along perimeter
    for tooth in range(16):
        ta = math.radians(tooth * (360.0 / 16.0))
        t_pos = Vector((1.45 + 0.82 * math.cos(ta), 0.82 * math.sin(ta), 1.25))
        add_cylinder(bm, radius=0.035, depth=0.16, segments=8,
                     matrix=Matrix.Translation(t_pos))

    # Long curved bullock draught beam extending from top of vertical shaft out 3.2m
    bmesh.ops.create_cube(bm, size=1.0, matrix=
        Matrix.Translation(Vector((1.45, 1.60, 2.15))) @
        Matrix.Scale(0.14, 4, Vector((1,0,0))) @
        Matrix.Scale(3.20, 4, Vector((0,1,0))) @
        Matrix.Scale(0.12, 4, Vector((0,0,1))))
    # Bullock yoke crossbar at the tip (Y = 3.15m)
    add_cylinder(bm, radius=0.05, depth=1.10, segments=8,
                 matrix=Matrix.Translation(Vector((1.45, 3.15, 2.10))) @
                 Matrix.Rotation(math.radians(90.0), 3, 'X').to_4x4())

    # D. Discharge Water Sluice Trough (under wheel at Z = 0.50m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=
        Matrix.Translation(Vector((0.0, -1.10, 0.50))) @
        Matrix.Scale(0.48, 4, Vector((1,0,0))) @
        Matrix.Scale(2.20, 4, Vector((0,1,0))) @
        Matrix.Scale(0.25, 4, Vector((0,0,1))))

    # Assign Teak material to initial wood faces
    bm.faces.ensure_lookup_table()
    for f in bm.faces:
        f.material_index = 0

    clay_faces_start = len(bm.faces)

    # E. Turned Terracotta Water Pots (Tind / Koozeh) mounted around wheel
    for p in range(8):
        pa = math.radians(p * 45.0)
        # Position pot at outer rim radius 1.50m
        pot_center = Vector((0.0, 1.55 * math.sin(pa), 1.60 + 1.55 * math.cos(pa)))
        pot_mat = Matrix.Translation(pot_center) @ \
                  Matrix.Rotation(pa, 3, 'X').to_4x4()
        # Earthenware bulbous body
        bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.10, radius2=0.07, depth=0.22,
                              matrix=pot_mat)
        # Flared rim
        add_cylinder(bm, radius=0.08, depth=0.04, segments=12,
                     matrix=pot_mat @ Matrix.Translation(Vector((0.0, 0.0, 0.12))))

    bm.faces.ensure_lookup_table()
    for idx in range(clay_faces_start, len(bm.faces)):
        bm.faces[idx].material_index = 1

    iron_faces_start = len(bm.faces)

    # F. Iron components: Axle shafts, bucket chain loops & band clamps
    # Horizontal center axle pin (through hub and trestles)
    add_cylinder(bm, radius=0.04, depth=1.40, segments=10,
                 matrix=Matrix.Translation(Vector((0.0, 0.0, 1.60))) @
                 Matrix.Rotation(math.radians(90.0), 3, 'Y').to_4x4())
    # Chain loop ropes hung around rim
    for sign in [-0.14, 0.14]:
        bmesh.ops.create_cone(bm, cap_ends=False, segments=24, radius1=1.52, radius2=1.52, depth=0.03,
                              matrix=Matrix.Translation(Vector((sign, 0.0, 1.60))) @
                              Matrix.Rotation(math.radians(90.0), 3, 'Y').to_4x4())

    bm.faces.ensure_lookup_table()
    for idx in range(iron_faces_start, len(bm.faces)):
        bm.faces[idx].material_index = 2

    bm.to_mesh(mesh)
    bm.free()

    # UV Unwrap
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.02)
    bpy.ops.object.mode_set(mode='OBJECT')

    return obj


# =========================================================================
# 3. TRADITIONAL BRICK KILN BHATTA (SM_Brick_Kiln_Chimney_Bhatta)
# =========================================================================
def build_brick_kiln_bhatta(name="SM_Brick_Kiln_Chimney_Bhatta"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Material slots: 0: Brick, 1: Dirt, 2: Clay (green bricks)
    mat_brick = mat_lahori_brick()
    mat_dirt_mat = mat_dirt()
    mat_clay_mat = mat_clay()
    obj.data.materials.append(mat_brick)
    obj.data.materials.append(mat_dirt_mat)
    obj.data.materials.append(mat_clay_mat)

    # A. Conical Brick Chimney (Base Z=0, Height=7.5m)
    # Heavy octagonal masonry plinth (Z = 0.0 to 0.70m, 2.5m diameter)
    add_cylinder(bm, radius=1.25, depth=0.70, segments=8,
                 matrix=Matrix.Translation(Vector((0.0, 0.0, 0.35))))

    # Main tapering conical shaft (Z = 0.70m to 7.20m, base radius 1.10m tapering to 0.60m)
    cone_height = 6.50
    bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=1.10, radius2=0.60, depth=cone_height,
                          matrix=Matrix.Translation(Vector((0.0, 0.0, 0.70 + cone_height/2.0))))

    # Stepped Corbelled Crown Rim (Z = 7.20m to 7.60m)
    # Layer 1
    add_cylinder(bm, radius=0.68, depth=0.12, segments=24,
                 matrix=Matrix.Translation(Vector((0.0, 0.0, 7.26))))
    # Layer 2 (flared cornice)
    add_cylinder(bm, radius=0.76, depth=0.14, segments=24,
                 matrix=Matrix.Translation(Vector((0.0, 0.0, 7.39))))
    # Layer 3 (top rim)
    add_cylinder(bm, radius=0.72, depth=0.10, segments=24,
                 matrix=Matrix.Translation(Vector((0.0, 0.0, 7.51))))

    # Arched flue intake portal at base (+Y side: 0.8m wide, 1.1m high)
    bmesh.ops.create_cube(bm, size=1.0, matrix=
        Matrix.Translation(Vector((0.0, 1.15, 0.65))) @
        Matrix.Scale(0.85, 4, Vector((1,0,0))) @
        Matrix.Scale(0.35, 4, Vector((0,1,0))) @
        Matrix.Scale(1.10, 4, Vector((0,0,1))))

    # Stack of fired red bricks (Ready for distribution: 1.6m x 1.1m x 1.2m at X = -1.8m, Y = 1.8m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=
        Matrix.Translation(Vector((-1.80, 1.80, 0.60))) @
        Matrix.Scale(1.60, 4, Vector((1,0,0))) @
        Matrix.Scale(1.10, 4, Vector((0,1,0))) @
        Matrix.Scale(1.20, 4, Vector((0,0,1))))

    # Assign Brick material to chimney & fired brick stack
    bm.faces.ensure_lookup_table()
    for f in bm.faces:
        f.material_index = 0

    dirt_faces_start = len(bm.faces)

    # B. Firing Trench Excavation Bed & Ash Floor (4.5m x 2.6m at Y = 2.0 to 6.5m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=
        Matrix.Translation(Vector((0.60, 3.80, 0.08))) @
        Matrix.Scale(2.80, 4, Vector((1,0,0))) @
        Matrix.Scale(4.60, 4, Vector((0,1,0))) @
        Matrix.Scale(0.16, 4, Vector((0,0,1))))
    # Earthen bund berm along the edge
    bmesh.ops.create_cube(bm, size=1.0, matrix=
        Matrix.Translation(Vector((2.10, 3.80, 0.30))) @
        Matrix.Scale(0.50, 4, Vector((1,0,0))) @
        Matrix.Scale(4.60, 4, Vector((0,1,0))) @
        Matrix.Scale(0.50, 4, Vector((0,0,1))))

    bm.faces.ensure_lookup_table()
    for idx in range(dirt_faces_start, len(bm.faces)):
        bm.faces[idx].material_index = 1

    clay_faces_start = len(bm.faces)

    # C. Stack of Unfired Green Sun-Dried Bricks (Lattice drying pattern: 1.5m x 1.0m x 0.9m at X = 0.8m, Y = 3.6m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=
        Matrix.Translation(Vector((0.80, 3.60, 0.55))) @
        Matrix.Scale(1.50, 4, Vector((1,0,0))) @
        Matrix.Scale(1.00, 4, Vector((0,1,0))) @
        Matrix.Scale(0.90, 4, Vector((0,0,1))))

    # Second small stack of green clay bricks
    bmesh.ops.create_cube(bm, size=1.0, matrix=
        Matrix.Translation(Vector((0.70, 5.20, 0.40))) @
        Matrix.Scale(1.20, 4, Vector((1,0,0))) @
        Matrix.Scale(0.80, 4, Vector((0,1,0))) @
        Matrix.Scale(0.65, 4, Vector((0,0,1))))

    bm.faces.ensure_lookup_table()
    for idx in range(clay_faces_start, len(bm.faces)):
        bm.faces[idx].material_index = 2

    bm.to_mesh(mesh)
    bm.free()

    # UV Unwrap
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.02)
    bpy.ops.object.mode_set(mode='OBJECT')

    return obj


# =========================================================================
# 4. CLANDESTINE SAFEHOUSE SUPPLY CACHE (SM_Prop_Clandestine_Safehouse_Crate_Cache)
# =========================================================================
def build_clandestine_safehouse_cache(name="SM_Prop_Clandestine_Safehouse_Crate_Cache"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Material slots: 0: Teak, 1: Iron, 2: Cotton/Burlap
    mat_teak = mat_aged_teak()
    mat_iron = mat_wrought_iron()
    mat_cloth = mat_cloth_white()
    obj.data.materials.append(mat_teak)
    obj.data.materials.append(mat_iron)
    obj.data.materials.append(mat_cloth)

    # A. Stenciled Shipping Crates
    # Crate 1 (Bottom Left: 1.1m x 0.65m x 0.55m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=
        Matrix.Translation(Vector((-0.30, 0.0, 0.275))) @
        Matrix.Scale(1.10, 4, Vector((1,0,0))) @
        Matrix.Scale(0.65, 4, Vector((0,1,0))) @
        Matrix.Scale(0.55, 4, Vector((0,0,1))))

    # Crate 2 (Bottom Right: 0.95m x 0.60m x 0.50m, rotated 8 deg)
    c2_rot = Matrix.Translation(Vector((0.65, -0.05, 0.25))) @ \
             Matrix.Rotation(math.radians(8.0), 3, 'Z').to_4x4()
    bmesh.ops.create_cube(bm, size=1.0, matrix=c2_rot @
                          Matrix.Scale(0.95, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.60, 4, Vector((0,1,0))) @
                          Matrix.Scale(0.50, 4, Vector((0,0,1))))

    # Crate 3 (Top Crate: 0.85m x 0.50m x 0.42m stacked on Crate 1)
    bmesh.ops.create_cube(bm, size=1.0, matrix=
        Matrix.Translation(Vector((-0.20, 0.05, 0.76))) @
        Matrix.Scale(0.85, 4, Vector((1,0,0))) @
        Matrix.Scale(0.50, 4, Vector((0,1,0))) @
        Matrix.Scale(0.42, 4, Vector((0,0,1))))

    # Assign Teak material
    bm.faces.ensure_lookup_table()
    for f in bm.faces:
        f.material_index = 0

    iron_faces_start = len(bm.faces)

    # B. Metal Cans & Courier Roadster Bicycle Frame
    # 2 Cylindrical printing ink drums (X = 0.75m, Y = 0.45m)
    for ink_x in [0.65, 0.95]:
        add_cylinder(bm, radius=0.13, depth=0.42, segments=12,
                     matrix=Matrix.Translation(Vector((ink_x, 0.45, 0.21))))
        # Lid handle
        bmesh.ops.create_cube(bm, size=1.0, matrix=
            Matrix.Translation(Vector((ink_x, 0.45, 0.435))) @
            Matrix.Scale(0.08, 4, Vector((1,0,0))) @
            Matrix.Scale(0.02, 4, Vector((0,1,0))) @
            Matrix.Scale(0.03, 4, Vector((0,0,1))))

    # Rectangular kerosene tin (X = -0.75m, Y = 0.25m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=
        Matrix.Translation(Vector((-0.75, 0.25, 0.18))) @
        Matrix.Scale(0.24, 4, Vector((1,0,0))) @
        Matrix.Scale(0.24, 4, Vector((0,1,0))) @
        Matrix.Scale(0.36, 4, Vector((0,0,1))))

    # Vintage Roadster Bicycle Frame (Diamond frame leaned at X = 1.15m, Y = -0.15m, tilted at 18 deg)
    bike_mat = Matrix.Translation(Vector((1.18, -0.15, 0.45))) @ \
               Matrix.Rotation(math.radians(-18.0), 3, 'Y').to_4x4() @ \
               Matrix.Rotation(math.radians(12.0), 3, 'Z').to_4x4()

    # Wheels (Front & Rear, 28-inch radius 0.35m)
    for wx in [-0.55, 0.55]:
        add_cylinder(bm, radius=0.35, depth=0.035, segments=16,
                     matrix=bike_mat @ Matrix.Translation(Vector((wx, 0.0, -0.10))) @
                     Matrix.Rotation(math.radians(90.0), 3, 'Y').to_4x4())
    # Frame tubes (Crossbar, downtube, seat tube)
    add_cylinder(bm, radius=0.02, depth=0.65, segments=8,
                 matrix=bike_mat @ Matrix.Translation(Vector((0.0, 0.0, 0.18))) @
                 Matrix.Rotation(math.radians(90.0), 3, 'Y').to_4x4())
    add_cylinder(bm, radius=0.02, depth=0.58, segments=8,
                 matrix=bike_mat @ Matrix.Translation(Vector((-0.18, 0.0, 0.05))) @
                 Matrix.Rotation(math.radians(52.0), 3, 'Y').to_4x4())
    # Handlebars
    add_cylinder(bm, radius=0.018, depth=0.48, segments=8,
                 matrix=bike_mat @ Matrix.Translation(Vector((0.35, 0.0, 0.38))) @
                 Matrix.Rotation(math.radians(90.0), 3, 'X').to_4x4())

    bm.faces.ensure_lookup_table()
    for idx in range(iron_faces_start, len(bm.faces)):
        bm.faces[idx].material_index = 1

    cloth_faces_start = len(bm.faces)

    # C. Weathered Burlap Tarpaulin Sheet draped over top and side of crates
    tarp_mat = Matrix.Translation(Vector((-0.25, 0.0, 0.88))) @ \
               Matrix.Rotation(math.radians(-12.0), 3, 'Y').to_4x4()
    bmesh.ops.create_cube(bm, size=1.0, matrix=tarp_mat @
                          Matrix.Scale(1.15, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.75, 4, Vector((0,1,0))) @
                          Matrix.Scale(0.06, 4, Vector((0,0,1))))
    # Drooping fold flap on back edge
    bmesh.ops.create_cube(bm, size=1.0, matrix=
        Matrix.Translation(Vector((-0.25, -0.36, 0.55))) @
        Matrix.Rotation(math.radians(25.0), 3, 'X').to_4x4() @
        Matrix.Scale(1.10, 4, Vector((1,0,0))) @
        Matrix.Scale(0.05, 4, Vector((0,1,0))) @
        Matrix.Scale(0.65, 4, Vector((0,0,1))))

    bm.faces.ensure_lookup_table()
    for idx in range(cloth_faces_start, len(bm.faces)):
        bm.faces[idx].material_index = 2

    bm.to_mesh(mesh)
    bm.free()

    # UV Unwrap
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.02)
    bpy.ops.object.mode_set(mode='OBJECT')

    return obj


# =========================================================================
# EXPORT PIPELINE
# =========================================================================
def export_asset(builder_func, asset_name):
    print(f"\n--- Building & Exporting: {asset_name} ---")
    reset_scene()

    target = builder_func(asset_name)

    bpy.ops.object.select_all(action='DESELECT')
    target.select_set(True)
    bpy.context.view_layer.objects.active = target

    # 1. Save .blend source file
    blend_path = os.path.join(BLENDER_DIR, f"{asset_name}.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"[SAVE] Blend file: {blend_path}")

    # Copy blend file to dual project targets
    shutil.copy2(blend_path, os.path.join(ART_PROJECT_DIR, f"{asset_name}.blend"))
    shutil.copy2(blend_path, os.path.join(USER_PROJECT_DIR, f"{asset_name}.blend"))

    # 2. Export FBX
    fbx_name = f"{asset_name}.fbx"
    fbx_export_path = os.path.join(EXPORTS_DIR, fbx_name)

    bpy.ops.export_scene.fbx(
        filepath=fbx_export_path,
        use_selection=True,
        global_scale=100.0,
        axis_forward='-Z',
        axis_up='Y',
        apply_unit_scale=True,
        bake_space_transform=True,
        mesh_smooth_type='FACE'
    )
    print(f"[EXPORT] FBX: {fbx_export_path}")

    # Copy FBX to dual project targets
    shutil.copy2(fbx_export_path, os.path.join(ART_PROJECT_DIR, fbx_name))
    shutil.copy2(fbx_export_path, os.path.join(USER_PROJECT_DIR, fbx_name))

def main():
    print("================ TASK 9: CANAL & OUTSKIRTS ASSET GENERATOR ================")

    assets = [
        (build_canal_distributary_aqueduct, "SM_Canal_Distributary_Aqueduct_Stone"),
        (build_persian_wheel_rahat, "SM_Persian_Wheel_Rahat_Timber"),
        (build_brick_kiln_bhatta, "SM_Brick_Kiln_Chimney_Bhatta"),
        (build_clandestine_safehouse_cache, "SM_Prop_Clandestine_Safehouse_Crate_Cache"),
    ]

    for builder, name in assets:
        export_asset(builder, name)

    print("================ ALL 4 TASK 9 ASSETS GENERATED & EXPORTED TO DUAL TARGETS ================")

if __name__ == "__main__":
    main()
