"""
PROJECT REVOLUTION — Storytelling Realism Assets Generator
Toolchain: Blender 5.2 LTS Headless Pipeline
Generates 5 period-authentic storytelling 3D models:
1. SM_Prop_School_Takhti_Slate (Traditional Punjabi wooden student writing board with reed pen)
2. SM_Prop_Bazaar_Cart_Thela (Authentic Indian wooden bazaar handcart with spoke wheels & cargo)
3. SM_Prop_Courtyard_Chulha_Stove (Earthen double-burner mud hearth with clay handi & brass lota)
4. SM_Prop_Pigeon_Coop_KabootarKhana (Rooftop wooden pigeon loft with slatted mesh & seed dishes)
5. SM_Prop_Pamphlet_Stack_Rowlatt (Clandestine anti-Rowlatt Hartal leaflets on rag paper)
"""

import bpy
import bmesh
import math
import os
from mathutils import Vector, Matrix

PROJECT_ROOT = r"C:\Users\npal7\PROJECT\REVOLUTION"
ART_DIR = os.path.join(PROJECT_ROOT, "Art")
BLENDER_DIR = os.path.join(ART_DIR, "Blender")
EXPORTS_DIR = os.path.join(ART_DIR, "Exports")

os.makedirs(BLENDER_DIR, exist_ok=True)
os.makedirs(EXPORTS_DIR, exist_ok=True)

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

def mat_aged_teak():
    return get_pbr_material("M_AgedTeak_PBR", (0.34, 0.22, 0.14, 1.0), roughness=0.78, metallic=0.0)

def mat_wrought_iron():
    return get_pbr_material("M_WroughtIron_PBR", (0.12, 0.12, 0.13, 1.0), roughness=0.62, metallic=0.88)

def mat_clay():
    return get_pbr_material("M_Clay_PBR", (0.62, 0.34, 0.22, 1.0), roughness=0.86, metallic=0.0)

def mat_lahori_brick():
    return get_pbr_material("M_LahoriBrick_PBR", (0.58, 0.22, 0.14, 1.0), roughness=0.85, metallic=0.0)

def mat_brass():
    return get_pbr_material("M_Brass_PBR", (0.78, 0.62, 0.24, 1.0), roughness=0.35, metallic=0.85)

def mat_jute():
    return get_pbr_material("M_Jute_PBR", (0.48, 0.40, 0.28, 1.0), roughness=0.92, metallic=0.0)

def mat_paper():
    return get_pbr_material("M_Paper_PBR", (0.86, 0.82, 0.72, 1.0), roughness=0.90, metallic=0.0)


# =========================================================================
# 1. TRADITIONAL WOODEN SCHOOL TAKHTI (SLATE) & REED PEN (QALAM)
# =========================================================================
def build_school_takhti(name="SM_Prop_School_Takhti_Slate"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Main rectangular wooden board (38cm tall x 24cm wide x 1.8cm thick)
    board = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.24, 0.38, 0.018, 1.0)))
    for v in board['verts']:
        v.co.z += 0.19

    # Triangular handle top with carved thumb grip hole
    handle = bmesh.ops.create_cone(bm, segments=8, radius1=0.06, radius2=0.02, depth=0.10)
    for v in handle['verts']:
        v.co.z += 0.43

    # String loop through handle top
    cord = bmesh.ops.create_cone(bm, segments=8, radius1=0.004, radius2=0.004, depth=0.08)
    for v in cord['verts']:
        v.co.z += 0.49

    # Reed Pen (Qalam) tied with hemp twine (18cm long bamboo reed with beveled nib)
    pen = bmesh.ops.create_cone(bm, segments=8, radius1=0.006, radius2=0.002, depth=0.18)
    for v in pen['verts']:
        v.co.x += 0.14
        v.co.y += 0.02
        v.co.z += 0.16

    # Earthen inkpot (Dawaat) sitting on slate edge
    inkpot = bmesh.ops.create_cone(bm, segments=12, radius1=0.035, radius2=0.025, depth=0.06)
    for v in inkpot['verts']:
        v.co.x += -0.14
        v.co.y += 0.02
        v.co.z += 0.06

    bm.to_mesh(mesh)
    bm.free()

    obj.data.materials.append(mat_aged_teak())
    obj.data.materials.append(mat_clay())
    return obj


# =========================================================================
# 2. BAZAAR WOODEN VENDOR HANDCART (THELA) WITH SPOKE WHEELS & CARGO
# =========================================================================
def build_bazaar_cart(name="SM_Prop_Bazaar_Cart_Thela"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Heavy wooden chassis bed (1.70m long x 1.05m wide x 0.10m thick)
    chassis = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((1.05, 1.70, 0.08, 1.0)))
    for v in chassis['verts']:
        v.co.z += 0.62

    # Side retaining planks (12cm high)
    for sx in [-0.51, 0.51]:
        plank = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.04, 1.70, 0.14, 1.0)))
        for v in plank['verts']:
            v.co.x += sx
            v.co.z += 0.70

    for sy in [-0.83, 0.83]:
        end_plank = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((1.05, 0.04, 0.14, 1.0)))
        for v in end_plank['verts']:
            v.co.y += sy
            v.co.z += 0.70

    # Axle beam (Solid iron bar)
    axle = bmesh.ops.create_cone(bm, segments=10, radius1=0.04, radius2=0.04, depth=1.30)
    for v in axle['verts']:
        old_x, old_z = v.co.x, v.co.z
        v.co.x = old_z
        v.co.z = -old_x
        v.co.z += 0.38

    # Wheels (2 heavy iron-rimmed wooden wheels, diameter 76cm)
    for wx in [-0.62, 0.62]:
        # Rim
        rim = bmesh.ops.create_cone(bm, segments=16, radius1=0.38, radius2=0.38, depth=0.06)
        for v in rim['verts']:
            old_x, old_z = v.co.x, v.co.z
            v.co.x = old_z
            v.co.z = -old_x
            v.co.x += wx
            v.co.z += 0.38

        # Center Hub
        hub = bmesh.ops.create_cone(bm, segments=12, radius1=0.10, radius2=0.10, depth=0.12)
        for v in hub['verts']:
            old_x, old_z = v.co.x, v.co.z
            v.co.x = old_z
            v.co.z = -old_x
            v.co.x += wx
            v.co.z += 0.38

        # 6 Wooden spokes per wheel
        for ang in range(0, 360, 60):
            rad = math.radians(ang)
            spoke = bmesh.ops.create_cone(bm, segments=6, radius1=0.02, radius2=0.02, depth=0.32)
            for v in spoke['verts']:
                y_rot = v.co.y * math.cos(rad) - v.co.z * math.sin(rad)
                z_rot = v.co.y * math.sin(rad) + v.co.z * math.cos(rad)
                v.co.y = y_rot
                v.co.z = z_rot + 0.38
                v.co.x += wx

    # Supporting ground legs (front & rear rests)
    for leg_y in [-0.70, 0.70]:
        leg = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.08, 0.08, 0.58, 1.0)))
        for v in leg['verts']:
            v.co.y += leg_y
            v.co.z += 0.29

    # Cargo on Cart: 3 stacked Burlap Jute sacks
    for jx, jy, jz in [(-0.25, -0.20, 0.74), (0.25, -0.20, 0.74), (0.0, 0.30, 0.78)]:
        sack = bmesh.ops.create_cone(bm, segments=12, radius1=0.24, radius2=0.20, depth=0.65)
        for v in sack['verts']:
            old_y, old_z = v.co.y, v.co.z
            v.co.y = old_z
            v.co.z = -old_y
            v.co.x += jx
            v.co.y += jy
            v.co.z += jz

    # Cargo on Cart: 2 Terracotta water pots (Matkas)
    for mx, my in [(-0.30, 0.55), (0.30, 0.55)]:
        pot = bmesh.ops.create_cone(bm, segments=12, radius1=0.18, radius2=0.08, depth=0.32)
        for v in pot['verts']:
            v.co.x += mx
            v.co.y += my
            v.co.z += 0.82

    bm.to_mesh(mesh)
    bm.free()

    obj.data.materials.append(mat_aged_teak())
    obj.data.materials.append(mat_wrought_iron())
    obj.data.materials.append(mat_jute())
    obj.data.materials.append(mat_clay())
    return obj


# =========================================================================
# 3. COURTYARD EARTHEN CLAY CHULHA STOVE WITH COOKING HANDI & BRASS LOTA
# =========================================================================
def build_courtyard_chulha(name="SM_Prop_Courtyard_Chulha_Stove"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Curved double-burner clay mud base (75cm wide x 48cm deep x 26cm tall)
    base = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.75, 0.48, 0.24, 1.0)))
    for v in base['verts']:
        v.co.z += 0.12

    # Two circular recessed burner hollows
    for cx in [-0.20, 0.20]:
        hollow = bmesh.ops.create_cone(bm, segments=12, radius1=0.14, radius2=0.14, depth=0.12)
        for v in hollow['verts']:
            v.co.x += cx
            v.co.y += -0.04
            v.co.z += 0.22

    # Cast-Iron cooking tripods / grates on burners
    for cx in [-0.20, 0.20]:
        grate = bmesh.ops.create_cone(bm, segments=8, radius1=0.15, radius2=0.15, depth=0.02)
        for v in grate['verts']:
            v.co.x += cx
            v.co.y += -0.04
            v.co.z += 0.25

    # Terracotta cooking pot (Handi) on left burner
    handi = bmesh.ops.create_cone(bm, segments=14, radius1=0.16, radius2=0.10, depth=0.22)
    for v in handi['verts']:
        v.co.x += -0.20
        v.co.y += -0.04
        v.co.z += 0.36

    handi_lid = bmesh.ops.create_cone(bm, segments=12, radius1=0.11, radius2=0.03, depth=0.05)
    for v in handi_lid['verts']:
        v.co.x += -0.20
        v.co.y += -0.04
        v.co.z += 0.48

    # Hammered brass water pitcher (Lota) sitting beside stove
    lota = bmesh.ops.create_cone(bm, segments=12, radius1=0.10, radius2=0.05, depth=0.18)
    for v in lota['verts']:
        v.co.x += 0.48
        v.co.y += 0.05
        v.co.z += 0.09

    # Firewood bundle and dried cow-dung fuel cakes (Uplay)
    for fx, fz in [(-0.46, 0.05), (-0.46, 0.11)]:
        log_mesh = bmesh.ops.create_cone(bm, segments=8, radius1=0.03, radius2=0.03, depth=0.35)
        for v in log_mesh['verts']:
            v.co.x += fx
            v.co.z += fz

    bm.to_mesh(mesh)
    bm.free()

    obj.data.materials.append(mat_clay())
    obj.data.materials.append(mat_brass())
    obj.data.materials.append(mat_wrought_iron())
    obj.data.materials.append(mat_aged_teak())
    return obj


# =========================================================================
# 4. ROOFTOP TIMBER PIGEON COOP (KABOOTAR-KHANA)
# =========================================================================
def build_pigeon_coop(name="SM_Prop_Pigeon_Coop_KabootarKhana"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Slatted wooden box enclosure (1.10m long x 0.55m deep x 0.85m tall)
    box = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((1.10, 0.55, 0.80, 1.0)))
    for v in box['verts']:
        v.co.z += 0.40

    # Overhanging pitched cedar roof
    roof_left = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((1.20, 0.35, 0.03, 1.0)))
    for v in roof_left['verts']:
        v.co.y += -0.15
        v.co.z += 0.86

    roof_right = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((1.20, 0.35, 0.03, 1.0)))
    for v in roof_right['verts']:
        v.co.y += 0.15
        v.co.z += 0.86

    # Slatted roost perches extending forward
    for px in [-0.35, 0.0, 0.35]:
        perch = bmesh.ops.create_cone(bm, segments=6, radius1=0.015, radius2=0.015, depth=0.22)
        for v in perch['verts']:
            old_y, old_z = v.co.y, v.co.z
            v.co.y = old_z
            v.co.z = -old_y
            v.co.x += px
            v.co.y += -0.36
            v.co.z += 0.45

    # Terracotta grain/water dish on coop floor
    dish = bmesh.ops.create_cone(bm, segments=12, radius1=0.10, radius2=0.06, depth=0.04)
    for v in dish['verts']:
        v.co.x += 0.25
        v.co.y += -0.32
        v.co.z += 0.02

    bm.to_mesh(mesh)
    bm.free()

    obj.data.materials.append(mat_aged_teak())
    obj.data.materials.append(mat_wrought_iron())
    obj.data.materials.append(mat_clay())
    return obj


# =========================================================================
# 5. CLANDESTINE ANTI-ROWLATT LEAFLETS STACK & SCATTER
# =========================================================================
def build_pamphlet_stack(name="SM_Prop_Pamphlet_Stack_Rowlatt"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Main stack of freshly pressed strike bulletins (28cm x 22cm x 7cm)
    stack = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.28, 0.22, 0.07, 1.0)))
    for v in stack['verts']:
        v.co.z += 0.035

    # Heavy river stone paperweight keeping pamphlets from blowing away
    stone = bmesh.ops.create_cone(bm, segments=10, radius1=0.05, radius2=0.03, depth=0.04)
    for v in stone['verts']:
        v.co.z += 0.09

    # Two loose windblown leaflets fluttering beside the stack
    leaf1 = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.26, 0.20, 0.003, 1.0)))
    for v in leaf1['verts']:
        # Rotate slightly
        old_x, old_y = v.co.x, v.co.y
        v.co.x = old_x * 0.94 - old_y * 0.34 + 0.24
        v.co.y = old_x * 0.34 + old_y * 0.94 - 0.05
        v.co.z += 0.005

    leaf2 = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.26, 0.20, 0.003, 1.0)))
    for v in leaf2['verts']:
        old_x, old_y = v.co.x, v.co.y
        v.co.x = old_x * 0.86 + old_y * 0.50 - 0.22
        v.co.y = -old_x * 0.50 + old_y * 0.86 - 0.06
        v.co.z += 0.006

    bm.to_mesh(mesh)
    bm.free()

    obj.data.materials.append(mat_paper())
    obj.data.materials.append(mat_wrought_iron())
    return obj


# =========================================================================
# EXPORT ALL 5 ASSETS AS FBX
# =========================================================================
def run_generation():
    print("[BLENDER] Generating 5 Historical Story Realism Assets...")

    generators = [
        (build_school_takhti, "SM_Prop_School_Takhti_Slate"),
        (build_bazaar_cart, "SM_Prop_Bazaar_Cart_Thela"),
        (build_courtyard_chulha, "SM_Prop_Courtyard_Chulha_Stove"),
        (build_pigeon_coop, "SM_Prop_Pigeon_Coop_KabootarKhana"),
        (build_pamphlet_stack, "SM_Prop_Pamphlet_Stack_Rowlatt")
    ]

    for gen_func, asset_name in generators:
        reset_scene()
        obj = gen_func(asset_name)

        bpy.ops.object.select_all(action='SELECT')
        bpy.context.view_layer.objects.active = obj

        fbx_path = os.path.join(EXPORTS_DIR, f"{asset_name}.fbx")
        bpy.ops.export_scene.fbx(
            filepath=fbx_path,
            use_selection=True,
            global_scale=1.0,
            apply_unit_scale=True,
            apply_scale_options='FBX_SCALE_NONE',
            axis_forward='-Z',
            axis_up='Y'
        )
        print(f"[BLENDER] Exported FBX: {fbx_path}")

    print("[BLENDER] All 5 story realism assets generated successfully!")

if __name__ == "__main__":
    run_generation()
