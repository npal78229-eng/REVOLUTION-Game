"""
PROJECT REVOLUTION — Task 7: The Fateful Afternoon of April 13, 1919
Blender 5.2 LTS Headless Asset Generator: Stampede Debris & Escape Traversal
Generates 4 authentic historical and gameplay traversal assets:
1. SM_Prop_Fallen_Turban_Shoes_Scatter: Discarded pagris, Punjabi juttis, cane umbrellas, and pottery
2. SM_Jallianwala_Crumbling_Wall_Breach: Damaged 1.8m low wall section with climbable rubble ramp for vaulting
3. SM_Prop_Bullet_Pocked_Brick_Slab: Historic memorial brick wall slab with bullet impacts & white marker frames
4. SM_Prop_Makeshift_Timber_Ladder: Bamboo/sal wood escape ladder leaned against wall with hemp lashings
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

def mat_clay():
    return get_pbr_material("M_Clay_PBR", (0.64, 0.35, 0.22, 1.0), roughness=0.92, metallic=0.0)

def mat_cloth_saffron():
    return get_pbr_material("M_ClothSaffron_PBR", (0.92, 0.48, 0.12, 1.0), roughness=0.85, metallic=0.0)

def mat_cloth_white():
    return get_pbr_material("M_ClothUndyedCotton_PBR", (0.88, 0.85, 0.78, 1.0), roughness=0.88, metallic=0.0)

def mat_dirt():
    return get_pbr_material("M_DirtRoad_PBR", (0.52, 0.42, 0.30, 1.0), roughness=0.95, metallic=0.0)


# =========================================================================
# 1. FALLEN TURBAN & JUTTI SHOE SCATTER (SM_Prop_Fallen_Turban_Shoes_Scatter)
# =========================================================================
def build_stampede_debris_scatter(name="SM_Prop_Fallen_Turban_Shoes_Scatter"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Ground contact disc base (Z = 0.0 to 0.02m)
    bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=1.4, radius2=1.4, depth=0.02,
                          matrix=Matrix.Translation(Vector((0.0, 0.0, 0.01))))

    # A. Discarded Pagris (Saffron & White turban cloth coils on ground)
    # Saffron Turban roll 1
    turban1_center = Vector((-0.45, 0.35, 0.10))
    for ring in range(3):
        r = 0.28 - ring * 0.07
        h = 0.08 + ring * 0.04
        bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=r, radius2=r*0.9, depth=h,
                              matrix=Matrix.Translation(turban1_center + Vector((0.0, 0.0, ring * 0.03))))
    # Trailing cloth sash 1
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((-0.15, 0.55, 0.03))) @
                          Matrix.Rotation(math.radians(28), 3, 'Z').to_4x4() @
                          Matrix.Scale(0.55, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.18, 4, Vector((0,1,0))) @
                          Matrix.Scale(0.03, 4, Vector((0,0,1))))

    # White Turban roll 2
    turban2_center = Vector((0.55, -0.40, 0.08))
    for ring in range(3):
        r = 0.24 - ring * 0.06
        h = 0.07 + ring * 0.03
        bmesh.ops.create_cone(bm, cap_ends=True, segments=14, radius1=r, radius2=r*0.85, depth=h,
                              matrix=Matrix.Translation(turban2_center + Vector((0.0, 0.0, ring * 0.025))))
    # Trailing cloth sash 2
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.80, -0.25, 0.025))) @
                          Matrix.Rotation(math.radians(-42), 3, 'Z').to_4x4() @
                          Matrix.Scale(0.60, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.16, 4, Vector((0,1,0))) @
                          Matrix.Scale(0.025, 4, Vector((0,0,1))))

    # B. Scattered Punjabi Juttis (Leather shoes with curled upturned toes)
    juttis = [
        # (X, Y, Z, Yaw, Pitch)
        (-0.65, -0.25, 0.04, 35.0, 0.0),    # Left jutti 1
        (-0.48, -0.38, 0.04, 60.0, 0.0),    # Right jutti 1
        (0.20, 0.60, 0.04, -85.0, 10.0),    # Overturned jutti 2
        (0.05, 0.72, 0.04, -110.0, 0.0),    # Left jutti 2
        (0.75, 0.20, 0.04, 150.0, 0.0),     # Lost jutti 3
        (-0.15, -0.65, 0.04, -20.0, 15.0),  # Tipped jutti 4
    ]
    for jx, jy, jz, jyaw, jpitch in juttis:
        j_mat = Matrix.Translation(Vector((jx, jy, jz))) @ \
                Matrix.Rotation(math.radians(jyaw), 3, 'Z').to_4x4() @ \
                Matrix.Rotation(math.radians(jpitch), 3, 'X').to_4x4()
        # Sole & vamp
        bmesh.ops.create_cube(bm, size=1.0, matrix=j_mat @
                              Matrix.Scale(0.26, 4, Vector((1,0,0))) @
                              Matrix.Scale(0.10, 4, Vector((0,1,0))) @
                              Matrix.Scale(0.04, 4, Vector((0,0,1))))
        # Curled toe tip (characteristic Punjabi jutti nok)
        bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.04, radius2=0.01, depth=0.07,
                              matrix=j_mat @ Matrix.Translation(Vector((0.14, 0.0, 0.02))) @
                              Matrix.Rotation(math.radians(45), 3, 'Y').to_4x4())

    # C. Dropped Cane Umbrella / Walking Cane
    umbrella_mat = Matrix.Translation(Vector((-0.10, -0.10, 0.05))) @ \
                   Matrix.Rotation(math.radians(52), 3, 'Z').to_4x4()
    # Shaft (0.95m long)
    bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.016, radius2=0.014, depth=0.95,
                          matrix=umbrella_mat @ Matrix.Rotation(math.radians(90), 3, 'Y').to_4x4())
    # Curved cane hook handle
    bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.02, radius2=0.02, depth=0.14,
                          matrix=umbrella_mat @ Matrix.Translation(Vector((-0.48, 0.05, 0.0))) @
                          Matrix.Rotation(math.radians(90), 3, 'X').to_4x4())
    # Folded black fabric rib ribs
    bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.05, radius2=0.02, depth=0.55,
                          matrix=umbrella_mat @ Matrix.Translation(Vector((0.15, 0.0, 0.0))) @
                          Matrix.Rotation(math.radians(90), 3, 'Y').to_4x4())

    # D. Broken Terracotta Matka / Lota
    # Tipped brass lota
    bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.09, radius2=0.07, depth=0.16,
                          matrix=Matrix.Translation(Vector((0.35, 0.15, 0.07))) @
                          Matrix.Rotation(math.radians(75), 3, 'X').to_4x4())
    # Broken terracotta shards
    shard_coords = [(0.15, -0.20), (0.28, -0.12), (0.05, -0.32), (-0.30, 0.10)]
    for sx, sy in shard_coords:
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((sx, sy, 0.02))) @
                              Matrix.Rotation(math.radians(random.uniform(0, 180)), 3, 'Z').to_4x4() @
                              Matrix.Scale(0.12, 4, Vector((1,0,0))) @
                              Matrix.Scale(0.09, 4, Vector((0,1,0))) @
                              Matrix.Scale(0.02, 4, Vector((0,0,1))))

    bm.to_mesh(mesh)
    bm.free()

    # Material slots
    mat_saff = mat_cloth_saffron()
    mat_w = mat_cloth_white()
    mat_t = mat_aged_teak()
    mat_c = mat_clay()
    mat_ir = mat_wrought_iron()
    for m in [mat_saff, mat_t, mat_c, mat_ir, mat_w]:
        obj.data.materials.append(m)

    return obj


# =========================================================================
# 2. CRUMBLING WALL BREACH (SM_Jallianwala_Crumbling_Wall_Breach)
# =========================================================================
def build_crumbling_wall_breach(name="SM_Jallianwala_Crumbling_Wall_Breach"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Dimensions: Total Width = 4.4m, Depth = 1.2m, Height = 1.75m at breach, 3.6m at side piers

    # A. Foundation Base Plinth (X = -2.2 to +2.2m, Y = -0.6 to +0.6m, Z = 0.0 to 0.35m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 0.175))) @
                          Matrix.Scale(4.4, 4, Vector((1,0,0))) @
                          Matrix.Scale(1.2, 4, Vector((0,1,0))) @
                          Matrix.Scale(0.35, 4, Vector((0,0,1))))

    # B. Left Intact Wall Pier (X = -2.2 to -1.3m, Z = 0.35 to 3.6m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((-1.75, 0.0, 1.975))) @
                          Matrix.Scale(0.9, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.85, 4, Vector((0,1,0))) @
                          Matrix.Scale(3.25, 4, Vector((0,0,1))))
    # Left Wall Coping Stone (Z = 3.6 to 3.8m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((-1.75, 0.0, 3.70))) @
                          Matrix.Scale(1.05, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.95, 4, Vector((0,1,0))) @
                          Matrix.Scale(0.20, 4, Vector((0,0,1))))

    # C. Right Intact Wall Pier (X = +1.3 to +2.2m, Z = 0.35 to 3.6m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((1.75, 0.0, 1.975))) @
                          Matrix.Scale(0.9, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.85, 4, Vector((0,1,0))) @
                          Matrix.Scale(3.25, 4, Vector((0,0,1))))
    # Right Wall Coping Stone (Z = 3.6 to 3.8m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((1.75, 0.0, 3.70))) @
                          Matrix.Scale(1.05, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.95, 4, Vector((0,1,0))) @
                          Matrix.Scale(0.20, 4, Vector((0,0,1))))

    # D. Stepped Jagged Wall Transitions (X = -1.3 to -0.8m, and X = +0.8 to +1.3m)
    # Left stepped intermediate brickwork (Z = 0.35 to 2.45m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((-1.05, 0.0, 1.40))) @
                          Matrix.Scale(0.50, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.80, 4, Vector((0,1,0))) @
                          Matrix.Scale(2.10, 4, Vector((0,0,1))))
    # Right stepped intermediate brickwork (Z = 0.35 to 2.30m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((1.05, 0.0, 1.325))) @
                          Matrix.Scale(0.50, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.80, 4, Vector((0,1,0))) @
                          Matrix.Scale(1.95, 4, Vector((0,0,1))))

    # E. Central Wall Breach Ledge (X = -0.8 to +0.8m, 1.6m wide, Z = 0.35 to 1.75m)
    # This is the exact vaultable boundary where Kabir leaps over
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 1.05))) @
                          Matrix.Scale(1.60, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.75, 4, Vector((0,1,0))) @
                          Matrix.Scale(1.40, 4, Vector((0,0,1))))

    # Breach rim coping ledge (cracked flat brickwork at Z = 1.70 to 1.78m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 1.75))) @
                          Matrix.Scale(1.65, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.80, 4, Vector((0,1,0))) @
                          Matrix.Scale(0.08, 4, Vector((0,0,1))))

    # F. Garden-Side Rubble Talus / Climbable Stepped Brick Ramp (Y = -0.4 to -1.3m)
    # Allows 12-year-old Kabir to step up from Z = 0.0 to 0.45m to 0.75m, making the 1.75m ledge
    # exactly 1.0m above his feet, enabling a seamless vault traversal!
    # Step 1: Base talus mound (Z = 0.0 to 0.40m, Y = -0.7 to -1.4m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, -0.95, 0.20))) @
                          Matrix.Scale(2.20, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.90, 4, Vector((0,1,0))) @
                          Matrix.Scale(0.40, 4, Vector((0,0,1))))

    # Step 2: Intermediate rubble terrace (Z = 0.40 to 0.78m, Y = -0.45 to -0.85m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, -0.65, 0.58))) @
                          Matrix.Scale(1.70, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.55, 4, Vector((0,1,0))) @
                          Matrix.Scale(0.38, 4, Vector((0,0,1))))

    # Scattered individual collapsed bricks on the talus
    rubble_bricks = [
        (-0.55, -1.05, 0.42, 22.0),
        (0.40, -1.15, 0.42, -35.0),
        (-0.20, -1.25, 0.32, 70.0),
        (0.65, -0.85, 0.65, -15.0),
        (-0.45, -0.70, 0.82, 45.0),
        (0.25, -0.60, 0.82, -50.0),
    ]
    for rx, ry, rz, ryaw in rubble_bricks:
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((rx, ry, rz))) @
                              Matrix.Rotation(math.radians(ryaw), 3, 'Z').to_4x4() @
                              Matrix.Scale(0.32, 4, Vector((1,0,0))) @
                              Matrix.Scale(0.18, 4, Vector((0,1,0))) @
                              Matrix.Scale(0.12, 4, Vector((0,0,1))))

    # G. Outer Alley Side: Lower rubble debris (Y = +0.5 to +1.0m, Z = 0.0 to 0.30m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.75, 0.15))) @
                          Matrix.Scale(1.80, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.60, 4, Vector((0,1,0))) @
                          Matrix.Scale(0.30, 4, Vector((0,0,1))))

    bm.to_mesh(mesh)
    bm.free()

    # Materials
    mat_b = mat_lahori_brick()
    mat_d = mat_dirt()
    mat_t = mat_aged_teak()
    for m in [mat_b, mat_d, mat_t]:
        obj.data.materials.append(m)

    return obj


# =========================================================================
# 3. BULLET-POCKED MEMORIAL BRICK SLAB (SM_Prop_Bullet_Pocked_Brick_Slab)
# =========================================================================
def build_bullet_pocked_wall_slab(name="SM_Prop_Bullet_Pocked_Brick_Slab"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Dimensions: 2.8m width x 0.5m depth x 3.2m height
    # Masonry Plinth base (Z = 0.0 to 0.3m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 0.15))) @
                          Matrix.Scale(2.9, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.55, 4, Vector((0,1,0))) @
                          Matrix.Scale(0.30, 4, Vector((0,0,1))))

    # Main Brick Wall Slab (Z = 0.3 to 3.0m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 1.65))) @
                          Matrix.Scale(2.8, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.48, 4, Vector((0,1,0))) @
                          Matrix.Scale(2.70, 4, Vector((0,0,1))))

    # Top Coping Cornice (Z = 3.0 to 3.2m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 3.10))) @
                          Matrix.Scale(2.95, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.58, 4, Vector((0,1,0))) @
                          Matrix.Scale(0.20, 4, Vector((0,0,1))))

    # Side Buttress Pilasters (Left & Right margins)
    for bx in [-1.30, 1.30]:
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((bx, -0.05, 1.65))) @
                              Matrix.Scale(0.25, 4, Vector((1,0,0))) @
                              Matrix.Scale(0.55, 4, Vector((0,1,0))) @
                              Matrix.Scale(2.70, 4, Vector((0,0,1))))

    # Historical Bullet Impact Clusters on Front Face (Y = -0.24m)
    # Impact cluster coordinates (X, Z) with crater chips and surrounding white memorial marking frames
    bullet_clusters = [
        # Cluster 1: Center-left chest height
        (-0.55, 1.65, 0.35, 0.30),
        # Cluster 2: Center-right standing height
        (0.45, 1.85, 0.40, 0.35),
        # Cluster 3: Lower ricochet marks
        (-0.25, 1.15, 0.30, 0.25),
        # Cluster 4: High ricochet marks near wall crest
        (0.20, 2.45, 0.32, 0.28),
    ]

    for cx, cz, fw, fh in bullet_clusters:
        # A. Painted white plaster marking frame (surrounding impact site)
        # Top frame border
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((cx, -0.25, cz + fh/2))) @
                              Matrix.Scale(fw, 4, Vector((1,0,0))) @
                              Matrix.Scale(0.015, 4, Vector((0,1,0))) @
                              Matrix.Scale(0.035, 4, Vector((0,0,1))))
        # Bottom frame border
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((cx, -0.25, cz - fh/2))) @
                              Matrix.Scale(fw, 4, Vector((1,0,0))) @
                              Matrix.Scale(0.015, 4, Vector((0,1,0))) @
                              Matrix.Scale(0.035, 4, Vector((0,0,1))))
        # Left frame border
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((cx - fw/2, -0.25, cz))) @
                              Matrix.Scale(0.035, 4, Vector((1,0,0))) @
                              Matrix.Scale(0.015, 4, Vector((0,1,0))) @
                              Matrix.Scale(fh, 4, Vector((0,0,1))))
        # Right frame border
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((cx + fw/2, -0.25, cz))) @
                              Matrix.Scale(0.035, 4, Vector((1,0,0))) @
                              Matrix.Scale(0.015, 4, Vector((0,1,0))) @
                              Matrix.Scale(fh, 4, Vector((0,0,1))))

        # B. Indented bullet impact craters (3 to 4 impacts inside each white marked frame)
        for offset_x, offset_z in [(-0.06, 0.04), (0.05, -0.05), (-0.02, -0.02), (0.07, 0.06)]:
            # Crater indentation
            bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.038, radius2=0.012, depth=0.06,
                                  matrix=Matrix.Translation(Vector((cx + offset_x, -0.23, cz + offset_z))) @
                                  Matrix.Rotation(math.radians(90), 3, 'X').to_4x4())

    bm.to_mesh(mesh)
    bm.free()

    # Materials
    mat_b = mat_lahori_brick()
    mat_w = mat_cloth_white()  # White plaster marking
    for m in [mat_b, mat_w]:
        obj.data.materials.append(m)

    return obj


# =========================================================================
# 4. MAKESHIFT TIMBER ESCAPE LADDER (SM_Prop_Makeshift_Timber_Ladder)
# =========================================================================
def build_makeshift_escape_ladder(name="SM_Prop_Makeshift_Timber_Ladder"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Length = 3.6m, Width = 0.58m
    # Tilted lean angle: 72 degrees against wall (lean offset along Y = 1.1m)
    lean_angle = math.radians(18.0)  # Tilted forward by 18 deg from vertical
    ladder_rot = Matrix.Rotation(lean_angle, 3, 'X').to_4x4()

    # Two heavy bamboo/sal timber stringers (side rails)
    for sx in [-0.26, 0.26]:
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.55, 1.70))) @
                              ladder_rot @
                              Matrix.Translation(Vector((sx, 0.0, 0.0))) @
                              Matrix.Scale(0.07, 4, Vector((1,0,0))) @
                              Matrix.Scale(0.09, 4, Vector((0,1,0))) @
                              Matrix.Scale(3.60, 4, Vector((0,0,1))))

    # 10 Cross rungs lashed to stringers at 0.32m intervals
    for rung_idx in range(10):
        rz = -1.45 + rung_idx * 0.32
        rung_mat = Matrix.Translation(Vector((0.0, 0.55, 1.70))) @ \
                   ladder_rot @ \
                   Matrix.Translation(Vector((0.0, 0.0, rz)))

        # Rung wood cylinder
        bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.03, radius2=0.028, depth=0.56,
                              matrix=rung_mat @ Matrix.Rotation(math.radians(90), 3, 'Y').to_4x4())

        # Hemp rope lashings at left and right joint
        for jx in [-0.26, 0.26]:
            bmesh.ops.create_cube(bm, size=1.0, matrix=rung_mat @ Matrix.Translation(Vector((jx, 0.0, 0.0))) @
                                  Matrix.Scale(0.09, 4, Vector((1,0,0))) @
                                  Matrix.Scale(0.11, 4, Vector((0,1,0))) @
                                  Matrix.Scale(0.06, 4, Vector((0,0,1))))

    bm.to_mesh(mesh)
    bm.free()

    # Materials
    mat_t = mat_aged_teak()
    mat_w = mat_cloth_white()  # Hemp rope
    for m in [mat_t, mat_w]:
        obj.data.materials.append(m)

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
    print("================ TASK 7: STAMPEDE DEBRIS & ESCAPE TRAVERSAL ASSET GENERATOR ================")

    assets = [
        (build_stampede_debris_scatter, "SM_Prop_Fallen_Turban_Shoes_Scatter"),
        (build_crumbling_wall_breach, "SM_Jallianwala_Crumbling_Wall_Breach"),
        (build_bullet_pocked_wall_slab, "SM_Prop_Bullet_Pocked_Brick_Slab"),
        (build_makeshift_escape_ladder, "SM_Prop_Makeshift_Timber_Ladder"),
    ]

    for builder, name in assets:
        export_asset(builder, name)

    print("================ ALL 4 TASK 7 ASSETS GENERATED & EXPORTED TO DUAL TARGETS ================")

if __name__ == "__main__":
    main()
