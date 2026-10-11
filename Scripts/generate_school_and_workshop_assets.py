"""
PROJECT REVOLUTION — 3D Asset Generator for District C (School) & Family Workshop
Toolchain: Blender 5.2 LTS Headless Pipeline
Generates:
1. SM_School_Desk_Bench_Wood (Two-seater colonial school desk & bench)
2. SM_School_Blackboard_Easel (Slate chalkboard on wooden easel)
3. SM_School_Bell_Tower_Iron (Pyramidal iron school bell frame with bronze bell)
4. SM_Prop_SewingMachine_Singer (1910s cast-iron foot-pedal tailor sewing machine)
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

def mat_iron():
    return get_pbr_material("M_WroughtIron_PBR", (0.12, 0.12, 0.13, 1.0), roughness=0.65, metallic=0.85)

def mat_clay():
    return get_pbr_material("M_Terracotta_PBR", (0.68, 0.36, 0.20, 1.0), roughness=0.88, metallic=0.0)

# --- 1. COLONIAL SCHOOL DESK & BENCH ---
def build_school_desk(name="SM_School_Desk_Bench_Wood"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()

    # Desk Top (slanted writing surface: width 1.3m, depth 0.45m, height 0.72m)
    desk_top = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((1.3, 0.45, 0.05, 1.0)))
    for v in desk_top['verts']:
        v.co.y += 0.20
        v.co.z += 0.72

    # Desk Legs (4 timber posts)
    for lx in [-0.60, 0.60]:
        for ly in [0.05, 0.38]:
            leg = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.08, 0.08, 0.70, 1.0)))
            for v in leg['verts']:
                v.co.x += lx
                v.co.y += ly
                v.co.z += 0.35

    # Attached Bench (width 1.3m, depth 0.28m, height 0.42m)
    bench_top = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((1.3, 0.28, 0.04, 1.0)))
    for v in bench_top['verts']:
        v.co.y -= 0.25
        v.co.z += 0.42

    # Bench Legs
    for lx in [-0.60, 0.60]:
        for ly in [-0.35, -0.15]:
            leg = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.08, 0.08, 0.40, 1.0)))
            for v in leg['verts']:
                v.co.x += lx
                v.co.y += ly
                v.co.z += 0.20

    # Connecting Floor Runners
    for lx in [-0.60, 0.60]:
        runner = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.08, 0.85, 0.06, 1.0)))
        for v in runner['verts']:
            v.co.x += lx
            v.co.y += 0.02
            v.co.z += 0.03

    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(mat_teak())
    return obj

# --- 2. SLATE BLACKBOARD ON WOODEN EASEL ---
def build_blackboard(name="SM_School_Blackboard_Easel"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()

    # Easel Legs (A-frame: left post, right post, back strut)
    leg_l = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.08, 0.08, 1.9, 1.0)))
    for v in leg_l['verts']:
        v.co.x -= 0.75
        v.co.z += 0.95

    leg_r = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.08, 0.08, 1.9, 1.0)))
    for v in leg_r['verts']:
        v.co.x += 0.75
        v.co.z += 0.95

    # Slate Board Panel (width 1.5m, height 1.0m, thickness 0.04m, center Z = 1.25m)
    board = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((1.5, 0.04, 1.0, 1.0)))
    for v in board['verts']:
        v.co.z += 1.25

    # Wooden Chalk Tray (width 1.55m, depth 0.12m, height 0.04m at Z = 0.73m)
    tray = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((1.55, 0.12, 0.04, 1.0)))
    for v in tray['verts']:
        v.co.y += 0.04
        v.co.z += 0.73

    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(mat_teak())
    mesh.materials.append(mat_iron())
    return obj

# --- 3. WROUGHT-IRON SCHOOL BELL TOWER ---
def build_bell_tower(name="SM_School_Bell_Tower_Iron"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()

    # 4 Corner Iron Struts (angled upward: height 3.6m, footprint 1.2m tapering to 0.5m)
    footprint = 0.60
    top_taper = 0.25
    corners = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
    for cx, cy in corners:
        post = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.10, 0.10, 3.6, 1.0)))
        for v in post['verts']:
            t = (v.co.z + 0.5)  # 0 to 1
            v.co.x = cx * (footprint * (1.0 - t * 0.5))
            v.co.y = cy * (footprint * (1.0 - t * 0.5))
            v.co.z = v.co.z + 1.8

    # Horizontal Cross-bracing tiers at Z = 1.2m and Z = 2.4m
    for bz in [1.2, 2.4]:
        brace = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.9, 0.9, 0.06, 1.0)))
        for v in brace['verts']:
            v.co.z += bz

    # Top Canopy Cap & Bell Hanger Beam at Z = 3.4m
    cap = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.6, 0.6, 0.10, 1.0)))
    for v in cap['verts']:
        v.co.z += 3.45

    # Heavy Bronze Bell (tapered cone: radius 0.25m, depth 0.35m at Z = 3.0m)
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=16,
        radius1=0.25,
        radius2=0.08,
        depth=0.35,
        matrix=Matrix.Translation((0, 0, 3.0))
    )

    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(mat_iron())
    mesh.materials.append(mat_teak())
    return obj

# --- 4. SINGER FOOT-PEDAL SEWING MACHINE (Tailor Workshop) ---
def build_sewing_machine(name="SM_Prop_SewingMachine_Singer"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()

    # Wooden Table Top (width 0.95m, depth 0.48m, height 0.05m at Z = 0.72m)
    table = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.95, 0.48, 0.05, 1.0)))
    for v in table['verts']:
        v.co.z += 0.72

    # Cast Iron Side Legs (ornate scrolled iron trestle sides)
    for lx in [-0.40, 0.40]:
        leg = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.06, 0.42, 0.70, 1.0)))
        for v in leg['verts']:
            v.co.x += lx
            v.co.z += 0.35

    # Cast Iron Treadle Foot Pedal at Z = 0.12m
    pedal = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.35, 0.25, 0.04, 1.0)))
    for v in pedal['verts']:
        v.co.z += 0.12

    # Sewing Machine Body (Cast-iron black lacquered arm)
    # Bed plate on table
    bed = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.45, 0.20, 0.03, 1.0)))
    for v in bed['verts']:
        v.co.x -= 0.05
        v.co.z += 0.76

    # Upright Arm Post
    post = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.10, 0.12, 0.22, 1.0)))
    for v in post['verts']:
        v.co.x += 0.10
        v.co.z += 0.88

    # Horizontal Needle Arm
    arm = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.30, 0.10, 0.08, 1.0)))
    for v in arm['verts']:
        v.co.x -= 0.02
        v.co.z += 0.98

    # Balance Handwheel on right side
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=16,
        radius1=0.10,
        radius2=0.10,
        depth=0.03,
        matrix=Matrix.Rotation(math.radians(90.0), 4, 'Y') @ Matrix.Translation((0.17, 0, 0.88))
    )

    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(mat_iron())
    mesh.materials.append(mat_teak())
    return obj

def export_assets():
    reset_scene()
    print("=== GENERATING SCHOOL & WORKSHOP ASSETS ===")

    builders = [
        ("SM_School_Desk_Bench_Wood", build_school_desk),
        ("SM_School_Blackboard_Easel", build_blackboard),
        ("SM_School_Bell_Tower_Iron", build_bell_tower),
        ("SM_Prop_SewingMachine_Singer", build_sewing_machine),
    ]

    for name, builder_fn in builders:
        reset_scene()
        obj = builder_fn(name)
        fbx_path = os.path.join(EXPORTS_DIR, f"{name}.fbx")
        
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
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
        print(f"EXPORTED: {name}.fbx -> {fbx_path}")

    print("=== SCHOOL & WORKSHOP ASSET EXPORT COMPLETE ===")

if __name__ == "__main__":
    export_assets()
