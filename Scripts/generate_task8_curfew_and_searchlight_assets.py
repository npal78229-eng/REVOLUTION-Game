"""
PROJECT REVOLUTION — Task 8: Act III — The Fateful Dusk & The Amritsar Curfew
Blender 5.2 LTS Headless Asset Generator: Searchlight, Curfew Notice, Stretcher & Sentry Bunker
Generates 4 authentic historical and gameplay environment assets:
1. SM_Prop_Searchlight_Tripod_Imperial: Carbon-arc searchlight on timber tripod with gimbal yoke
2. SM_Prop_Curfew_Notice_Martial_Law: Timber easel with pasted Dyer martial law curfew decree
3. SM_Prop_Makeshift_Stretcher_Charpai: Bamboo pole & moonj rope emergency survivor stretcher
4. SM_Checkpoint_Sandbag_Sentry_Bunker: Curved sandbag revetment bunker with timber shoring & roof
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

def mat_cloth_white():
    return get_pbr_material("M_ClothUndyedCotton_PBR", (0.88, 0.85, 0.78, 1.0), roughness=0.88, metallic=0.0)

def mat_dirt():
    return get_pbr_material("M_DirtRoad_PBR", (0.52, 0.42, 0.30, 1.0), roughness=0.95, metallic=0.0)


# =========================================================================
# 1. IMPERIAL CARBON-ARC SEARCHLIGHT (SM_Prop_Searchlight_Tripod_Imperial)
# =========================================================================
def build_searchlight_tripod(name="SM_Prop_Searchlight_Tripod_Imperial"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # A. Timber Tripod Base (3 turned legs angled at 120 deg apart)
    tripod_radius = 0.65
    leg_len = 1.45
    leg_angle_tilt = math.radians(24.0)

    for i in range(3):
        yaw = math.radians(i * 120.0)
        # Leg transform: positioned at center head Z=1.35m, rotated outward
        leg_mat = Matrix.Rotation(yaw, 3, 'Z').to_4x4() @ \
                  Matrix.Translation(Vector((0.0, 0.0, 1.35))) @ \
                  Matrix.Rotation(leg_angle_tilt, 3, 'Y').to_4x4() @ \
                  Matrix.Translation(Vector((0.0, 0.0, -leg_len / 2.0)))
        # Wooden leg
        bmesh.ops.create_cube(bm, size=1.0, matrix=leg_mat @
                              Matrix.Scale(0.08, 4, Vector((1,0,0))) @
                              Matrix.Scale(0.08, 4, Vector((0,1,0))) @
                              Matrix.Scale(leg_len, 4, Vector((0,0,1))))
        # Iron ground spike shoe
        bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.05, radius2=0.01, depth=0.12,
                              matrix=leg_mat @ Matrix.Translation(Vector((0.0, 0.0, -leg_len/2.0))))

    # B. Central Azimuth Hub & Swivel Collar (Z = 1.30 to 1.50m)
    bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=0.18, radius2=0.16, depth=0.20,
                          matrix=Matrix.Translation(Vector((0.0, 0.0, 1.40))))

    # C. Elevation Yoke Fork (U-arm holding searchlight drum)
    # Horizontal crossbar
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 1.52))) @
                          Matrix.Scale(0.72, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.12, 4, Vector((0,1,0))) @
                          Matrix.Scale(0.08, 4, Vector((0,0,1))))
    # Left vertical arm
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((-0.34, 0.0, 1.78))) @
                          Matrix.Scale(0.08, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.10, 4, Vector((0,1,0))) @
                          Matrix.Scale(0.48, 4, Vector((0,0,1))))
    # Right vertical arm
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.34, 0.0, 1.78))) @
                          Matrix.Scale(0.08, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.10, 4, Vector((0,1,0))) @
                          Matrix.Scale(0.48, 4, Vector((0,0,1))))

    # Elevation lock wheels on sides
    for side_x in [-0.40, 0.40]:
        bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.10, radius2=0.10, depth=0.04,
                              matrix=Matrix.Translation(Vector((side_x, 0.0, 1.85))) @
                              Matrix.Rotation(math.radians(90), 3, 'Y').to_4x4())

    # D. Searchlight Cylindrical Barrel Drum (Center at Z = 1.85m, pointing forward +Y)
    drum_mat = Matrix.Translation(Vector((0.0, 0.0, 1.85))) @ \
               Matrix.Rotation(math.radians(90), 3, 'X').to_4x4()
    # Main drum housing (radius 0.28m, depth 0.65m)
    bmesh.ops.create_cone(bm, cap_ends=True, segments=20, radius1=0.28, radius2=0.28, depth=0.65,
                          matrix=drum_mat)

    # Front glass lens & protective retaining ring (Y = +0.33m)
    bmesh.ops.create_cone(bm, cap_ends=True, segments=20, radius1=0.30, radius2=0.30, depth=0.06,
                          matrix=Matrix.Translation(Vector((0.0, 0.33, 1.85))) @
                          Matrix.Rotation(math.radians(90), 3, 'X').to_4x4())

    # Rear ventilation dome & carbon-rod chimney (Y = -0.35m)
    bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=0.22, radius2=0.14, depth=0.18,
                          matrix=Matrix.Translation(Vector((0.0, -0.40, 1.85))) @
                          Matrix.Rotation(math.radians(90), 3, 'X').to_4x4())
    # Top exhaust vent hood
    bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=0.08, radius2=0.06, depth=0.14,
                          matrix=Matrix.Translation(Vector((0.0, -0.15, 2.20))))

    bm.to_mesh(mesh)
    bm.free()

    # Materials: Iron, Teak wood, White glass/reflector
    mat_ir = mat_wrought_iron()
    mat_t = mat_aged_teak()
    mat_w = mat_cloth_white()
    for m in [mat_ir, mat_t, mat_w]:
        obj.data.materials.append(m)

    return obj


# =========================================================================
# 2. MARTIAL LAW CURFEW NOTICE (SM_Prop_Curfew_Notice_Martial_Law)
# =========================================================================
def build_curfew_notice_board(name="SM_Prop_Curfew_Notice_Martial_Law"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Dimensions: 1.2m width x 0.85m depth x 1.85m height
    # A. Timber A-Frame Struts (2 Front slanted legs, 1 rear prop)
    front_tilt = math.radians(10.0)
    for fx in [-0.48, 0.48]:
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((fx, 0.05, 0.90))) @
                              Matrix.Rotation(front_tilt, 3, 'X').to_4x4() @
                              Matrix.Scale(0.08, 4, Vector((1,0,0))) @
                              Matrix.Scale(0.08, 4, Vector((0,1,0))) @
                              Matrix.Scale(1.85, 4, Vector((0,0,1))))

    # Rear support prop leg (slanted backwards along -Y)
    rear_tilt = math.radians(-26.0)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, -0.32, 0.85))) @
                          Matrix.Rotation(rear_tilt, 3, 'X').to_4x4() @
                          Matrix.Scale(0.08, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.08, 4, Vector((0,1,0))) @
                          Matrix.Scale(1.80, 4, Vector((0,0,1))))

    # Horizontal bottom brace
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.03, 0.35))) @
                          Matrix.Scale(1.05, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.06, 4, Vector((0,1,0))) @
                          Matrix.Scale(0.08, 4, Vector((0,0,1))))

    # B. Wooden Notice Backboard (1.1m wide x 1.25m high x 0.06m thick, tilted 10 deg)
    board_mat = Matrix.Translation(Vector((0.0, 0.08, 1.20))) @ \
                Matrix.Rotation(front_tilt, 3, 'X').to_4x4()
    bmesh.ops.create_cube(bm, size=1.0, matrix=board_mat @
                          Matrix.Scale(1.10, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.06, 4, Vector((0,1,0))) @
                          Matrix.Scale(1.25, 4, Vector((0,0,1))))

    # Board top moulding cornice
    bmesh.ops.create_cube(bm, size=1.0, matrix=board_mat @ Matrix.Translation(Vector((0.0, 0.02, 0.65))) @
                          Matrix.Scale(1.18, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.10, 4, Vector((0,1,0))) @
                          Matrix.Scale(0.08, 4, Vector((0,0,1))))

    # C. Plastered Curfew Decree Parchment (Pasted on front face)
    # Sheet 1: Main Dyer Proclamation decree (0.85m x 1.0m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=board_mat @ Matrix.Translation(Vector((0.0, 0.035, 0.0))) @
                          Matrix.Scale(0.85, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.01, 4, Vector((0,1,0))) @
                          Matrix.Scale(1.00, 4, Vector((0,0,1))))

    # Red Imperial Wax Excise Seal at bottom of notice
    bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.06, radius2=0.06, depth=0.02,
                          matrix=board_mat @ Matrix.Translation(Vector((0.28, 0.045, -0.38))) @
                          Matrix.Rotation(math.radians(90), 3, 'X').to_4x4())

    bm.to_mesh(mesh)
    bm.free()

    # Materials: Teak, Paper, Wax (Brick red)
    mat_t = mat_aged_teak()
    mat_w = mat_cloth_white()
    mat_b = mat_lahori_brick()
    for m in [mat_t, mat_w, mat_b]:
        obj.data.materials.append(m)

    return obj


# =========================================================================
# 3. MAKESHIFT CASUALTY STRETCHER (SM_Prop_Makeshift_Stretcher_Charpai)
# =========================================================================
def build_casualty_stretcher(name="SM_Prop_Makeshift_Stretcher_Charpai"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Dimensions: Length = 2.4m, Width = 0.68m, Height = 0.22m
    # A. Two Bamboo Carrying Poles (along X axis from -1.2m to +1.2m)
    for py in [-0.28, 0.28]:
        bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.035, radius2=0.032, depth=2.40,
                              matrix=Matrix.Translation(Vector((0.0, py, 0.14))) @
                              Matrix.Rotation(math.radians(90), 3, 'Y').to_4x4())
        # Carved hand grips at both ends
        for hx in [-1.15, 1.15]:
            bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.04, radius2=0.04, depth=0.14,
                                  matrix=Matrix.Translation(Vector((hx, py, 0.14))) @
                                  Matrix.Rotation(math.radians(90), 3, 'Y').to_4x4())

    # B. Four Turned Standoff Leg Feet (under poles at X = ±0.75m)
    for lx in [-0.75, 0.75]:
        for ly in [-0.28, 0.28]:
            bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((lx, ly, 0.07))) @
                                  Matrix.Scale(0.06, 4, Vector((1,0,0))) @
                                  Matrix.Scale(0.06, 4, Vector((0,1,0))) @
                                  Matrix.Scale(0.14, 4, Vector((0,0,1))))

    # C. Woven Moonj Rope Webbing / Canvas Bed (X = -0.75 to +0.75m, Y = -0.26 to +0.26m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 0.13))) @
                          Matrix.Scale(1.50, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.52, 4, Vector((0,1,0))) @
                          Matrix.Scale(0.03, 4, Vector((0,0,1))))

    # D. Folded Khadi Medical Bolster / Pillow (at head end X = -0.55m)
    bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.10, radius2=0.10, depth=0.48,
                          matrix=Matrix.Translation(Vector((-0.55, 0.0, 0.18))) @
                          Matrix.Rotation(math.radians(90), 3, 'X').to_4x4())

    # Folded cotton bandage cloths
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.45, 0.0, 0.16))) @
                          Matrix.Scale(0.35, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.28, 4, Vector((0,1,0))) @
                          Matrix.Scale(0.06, 4, Vector((0,0,1))))

    bm.to_mesh(mesh)
    bm.free()

    # Materials: Teak (Bamboo poles), Dirt (Woven moonj bed), Cloth (Bandages)
    mat_t = mat_aged_teak()
    mat_d = mat_dirt()
    mat_w = mat_cloth_white()
    for m in [mat_t, mat_d, mat_w]:
        obj.data.materials.append(m)

    return obj


# =========================================================================
# 4. SANDBAG SENTRY BUNKER REVETMENT (SM_Checkpoint_Sandbag_Sentry_Bunker)
# =========================================================================
def build_sandbag_sentry_bunker(name="SM_Checkpoint_Sandbag_Sentry_Bunker"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Dimensions: 4.2m width x 2.4m depth x 2.1m height
    # A. Foundation Base Plinth (Z = 0.0 to 0.15m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 0.075))) @
                          Matrix.Scale(4.4, 4, Vector((1,0,0))) @
                          Matrix.Scale(2.6, 4, Vector((0,1,0))) @
                          Matrix.Scale(0.15, 4, Vector((0,0,1))))

    # B. Stacked Sandbag Courses (Curved crescent front revetment)
    # 5 vertical layers of burlap sandbags (layer height ~0.24m)
    for layer in range(5):
        lz = 0.15 + layer * 0.24 + 0.12
        # Front crescent bags
        num_bags = 8
        for b in range(num_bags):
            # Curved arc along front wall (X = -1.8 to +1.8m, Y = -0.8 to -0.3m)
            frac = (b / (num_bags - 1.0)) * 2.0 - 1.0  # -1.0 to 1.0
            bx = frac * 1.80
            by = -0.85 + (1.0 - frac * frac) * 0.35
            # Staggered jitter
            jitter = (0.05 if layer % 2 == 1 else -0.05)
            bx += jitter

            # Individual sandbag (0.46m x 0.30m x 0.22m with rounded corners)
            bag_mat = Matrix.Translation(Vector((bx, by, lz))) @ \
                      Matrix.Rotation(math.radians(-frac * 25.0), 3, 'Z').to_4x4()
            bmesh.ops.create_cube(bm, size=1.0, matrix=bag_mat @
                                  Matrix.Scale(0.46, 4, Vector((1,0,0))) @
                                  Matrix.Scale(0.30, 4, Vector((0,1,0))) @
                                  Matrix.Scale(0.22, 4, Vector((0,0,1))))

        # Left wing sandbag wall (Y = -0.8 to +0.8m at X = -1.85m)
        for b_side in range(3):
            sy = -0.50 + b_side * 0.45
            bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((-1.85, sy, lz))) @
                                  Matrix.Scale(0.30, 4, Vector((1,0,0))) @
                                  Matrix.Scale(0.44, 4, Vector((0,1,0))) @
                                  Matrix.Scale(0.22, 4, Vector((0,0,1))))

        # Right wing sandbag wall (Y = -0.8 to +0.8m at X = +1.85m)
        for b_side in range(3):
            sy = -0.50 + b_side * 0.45
            bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((1.85, sy, lz))) @
                                  Matrix.Scale(0.30, 4, Vector((1,0,0))) @
                                  Matrix.Scale(0.44, 4, Vector((0,1,0))) @
                                  Matrix.Scale(0.22, 4, Vector((0,0,1))))

    # C. Timber Shoring Posts & Roof Canopy (Rear bunker Z = 1.35 to 2.15m)
    # 4 Heavy Corner Teak Posts
    post_coords = [(-1.75, 0.65), (1.75, 0.65), (-1.75, -0.35), (1.75, -0.35)]
    for px, py in post_coords:
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((px, py, 1.10))) @
                              Matrix.Scale(0.14, 4, Vector((1,0,0))) @
                              Matrix.Scale(0.14, 4, Vector((0,1,0))) @
                              Matrix.Scale(2.10, 4, Vector((0,0,1))))

    # Overhead Teak Tie-Beams (Z = 2.05m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.15, 2.05))) @
                          Matrix.Scale(3.80, 4, Vector((1,0,0))) @
                          Matrix.Scale(1.30, 4, Vector((0,1,0))) @
                          Matrix.Scale(0.12, 4, Vector((0,0,1))))

    # Corrugated Tin Shield Roof Canopy (Z = 2.12m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.15, 2.14))) @
                          Matrix.Scale(4.10, 4, Vector((1,0,0))) @
                          Matrix.Scale(1.50, 4, Vector((0,1,0))) @
                          Matrix.Scale(0.04, 4, Vector((0,0,1))))

    # Inner trench duckboard walkway (teak duckboard planks at Z = 0.18m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.10, 0.20))) @
                          Matrix.Scale(3.20, 4, Vector((1,0,0))) @
                          Matrix.Scale(0.90, 4, Vector((0,1,0))) @
                          Matrix.Scale(0.05, 4, Vector((0,0,1))))

    bm.to_mesh(mesh)
    bm.free()

    # Materials: Dirt (Sandbags), Teak (Shoring & posts), Iron (Tin roof)
    mat_d = mat_dirt()
    mat_t = mat_aged_teak()
    mat_ir = mat_wrought_iron()
    for m in [mat_d, mat_t, mat_ir]:
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
    print("================ TASK 8: CURFEW & SEARCHLIGHT ASSET GENERATOR ================")

    assets = [
        (build_searchlight_tripod, "SM_Prop_Searchlight_Tripod_Imperial"),
        (build_curfew_notice_board, "SM_Prop_Curfew_Notice_Martial_Law"),
        (build_casualty_stretcher, "SM_Prop_Makeshift_Stretcher_Charpai"),
        (build_sandbag_sentry_bunker, "SM_Checkpoint_Sandbag_Sentry_Bunker"),
    ]

    for builder, name in assets:
        export_asset(builder, name)

    print("================ ALL 4 TASK 8 ASSETS GENERATED & EXPORTED TO DUAL TARGETS ================")

if __name__ == "__main__":
    main()
