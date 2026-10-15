"""
PROJECT REVOLUTION — Task 6: The Enclosed Garden of Jallianwala Bagh
Toolchain: Blender 5.2 LTS Headless Pipeline
Generates 5 authentic monumental and historical assets for April 13, 1919:
1. SM_Jallianwala_Shahidi_Kua_Well (Historic Martyrs' Well with octagonal plinth, deep shaft & timber canopy)
2. SM_Jallianwala_Enclosure_Wall (4.5m tall blind Lahori brick haveli enclosure wall module)
3. SM_Jallianwala_Raised_Bank (Tactical elevated 1.2m earthen/brick mound where Dyer deployed riflemen)
4. SM_British_Armored_Car_Obstacle (1919 Austin armored vehicle stopped outside narrow gate)
5. SM_Jallianwala_Baisakhi_Pandal (Assembly dais platform with shamiana canopy, masnad bolsters & podium)
"""

import bpy
import bmesh
import math
import os
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

def mat_armored_steel():
    return get_pbr_material("M_ArmoredSteel_PBR", (0.28, 0.32, 0.24, 1.0), roughness=0.55, metallic=0.75)

def mat_dirt_earth():
    return get_pbr_material("M_DirtRoad_PBR", (0.52, 0.42, 0.30, 1.0), roughness=0.95, metallic=0.0)

def mat_cloth_khadi():
    return get_pbr_material("M_ClothUndyedCotton_PBR", (0.88, 0.85, 0.78, 1.0), roughness=0.88, metallic=0.0)

def mat_cloth_saffron():
    return get_pbr_material("M_ClothSaffron_PBR", (0.92, 0.48, 0.12, 1.0), roughness=0.85, metallic=0.0)


# =========================================================================
# 1. SHAHIDI KUA — THE MARTYRS' WELL (SM_Jallianwala_Shahidi_Kua_Well)
# =========================================================================
def build_shahidi_kua_well(name="SM_Jallianwala_Shahidi_Kua_Well"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Octagonal Masonry Plinth Base (Z = 0.0 to 0.6m, diameter ~3.8m)
    bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=1.9, radius2=1.9, depth=0.6,
                          matrix=Matrix.Translation(Vector((0.0, 0.0, 0.30))))

    # Stepped Stone Ring (Z = 0.6 to 0.9m, diameter ~3.4m)
    bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=1.7, radius2=1.7, depth=0.3,
                          matrix=Matrix.Translation(Vector((0.0, 0.0, 0.75))))

    # Circular Well Parapet Wall (Outer radius 1.35m, inner radius 1.05m, height Z = 0.9 to 1.9m)
    # Outer cylinder
    bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=1.35, radius2=1.35, depth=1.0,
                          matrix=Matrix.Translation(Vector((0.0, 0.0, 1.40))))

    # Shaft Void / Recessed Deep Floor (recessed black stone bottom at Z = 0.1m)
    bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=1.05, radius2=1.05, depth=0.2,
                          matrix=Matrix.Translation(Vector((0.0, 0.0, 0.10))))

    # 4 Heavy Timber Corner Posts for Protective Canopy (X = ±1.4m, Y = ±1.4m, Z = 0.6 to 3.6m)
    post_coords = [(-1.4, -1.4), (1.4, -1.4), (1.4, 1.4), (-1.4, 1.4)]
    for px, py in post_coords:
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((px, py, 2.1)))
                              @ Matrix.Diagonal((0.22, 0.22, 3.0, 1.0)))

    # Overhead Timber Lintel Tie Beams (Z = 3.5m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, -1.4, 3.55)))
                          @ Matrix.Diagonal((3.0, 0.20, 0.20, 1.0)))
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 1.4, 3.55)))
                          @ Matrix.Diagonal((3.0, 0.20, 0.20, 1.0)))
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((-1.4, 0.0, 3.55)))
                          @ Matrix.Diagonal((0.20, 3.0, 0.20, 1.0)))
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((1.4, 0.0, 3.55)))
                          @ Matrix.Diagonal((0.20, 3.0, 0.20, 1.0)))

    # Hipped Terracotta Roof Canopy (Z = 3.6 to 4.5m)
    # Lower eave cornice
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 3.75)))
                          @ Matrix.Diagonal((3.4, 3.4, 0.25, 1.0)))
    # Upper pyramid roof cap
    bmesh.ops.create_cone(bm, cap_ends=True, segments=4, radius1=2.3, radius2=0.2, depth=0.8,
                          matrix=Matrix.Translation(Vector((0.0, 0.0, 4.25))) @ Matrix.Rotation(math.radians(45), 4, 'Z'))

    # Central Iron Pulley Beam across the well opening (Z = 2.4m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 2.4)))
                          @ Matrix.Diagonal((0.10, 2.5, 0.12, 1.0)))
    # Iron Pulley Wheel
    bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=0.22, radius2=0.22, depth=0.06,
                          matrix=Matrix.Translation(Vector((0.0, 0.0, 2.2))) @ Matrix.Rotation(math.radians(90), 4, 'Y'))

    # Wrought Iron Perimeter Safety Grille around the parapet
    for gx in [-1.35, 1.35]:
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((gx, 0.0, 2.1)))
                              @ Matrix.Diagonal((0.05, 2.4, 0.40, 1.0)))

    bm.to_mesh(mesh)
    bm.free()

    obj.data.materials.append(mat_lahori_brick())
    obj.data.materials.append(mat_aged_teak())
    obj.data.materials.append(mat_wrought_iron())

    return obj


# =========================================================================
# 2. BLIND HAVELI ENCLOSURE WALL (SM_Jallianwala_Enclosure_Wall)
# =========================================================================
def build_jallianwala_enclosure_wall(name="SM_Jallianwala_Enclosure_Wall"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Dimensions: 8.0m length along X, 1.2m thickness along Y, 4.6m height along Z
    # Solid Masonry Plinth (Z = 0.0 to 0.6m, depth 1.4m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 0.30)))
                          @ Matrix.Diagonal((8.0, 1.4, 0.60, 1.0)))

    # Main Blind Brick Wall (Z = 0.6 to 4.2m, depth 1.2m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 2.40)))
                          @ Matrix.Diagonal((8.0, 1.2, 3.60, 1.0)))

    # Buttress Pilasters on interior face (Y = -0.65m) at X = -3.2m, 0.0m, +3.2m
    for bx in [-3.2, 0.0, 3.2]:
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((bx, -0.68, 2.10)))
                              @ Matrix.Diagonal((0.80, 0.25, 4.20, 1.0)))

    # Projecting Brick Coping & Cornice at Top (Z = 4.2 to 4.6m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 4.35)))
                          @ Matrix.Diagonal((8.0, 1.35, 0.30, 1.0)))
    # Stepped tile ridge cap
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 4.55)))
                          @ Matrix.Diagonal((8.0, 0.90, 0.15, 1.0)))

    # Decorative blind arched brick relief recesses on the wall face (shallow 4cm insets)
    for arc_x in [-2.0, 2.0]:
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((arc_x, -0.61, 2.50)))
                              @ Matrix.Diagonal((1.40, 0.04, 2.20, 1.0)))

    bm.to_mesh(mesh)
    bm.free()

    obj.data.materials.append(mat_lahori_brick())
    obj.data.materials.append(mat_aged_teak())

    return obj


# =========================================================================
# 3. TACTICAL RAISED BANK (SM_Jallianwala_Raised_Bank)
# =========================================================================
def build_jallianwala_raised_bank(name="SM_Jallianwala_Raised_Bank"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Elevated Earthen/Brick Mound: 6.0m length along X, 4.5m width along Y, 1.2m elevation at Z
    # Retaining Brick Front Wall (facing the garden at Y = +2.0m, Z = 0.0 to 1.2m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 2.15, 0.60)))
                          @ Matrix.Diagonal((6.0, 0.40, 1.20, 1.0)))

    # Main Walkable Upper Platform Slab (Z = 1.05 to 1.20m, width 6.0m, depth 3.5m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.30, 1.125)))
                          @ Matrix.Diagonal((6.0, 3.50, 0.15, 1.0)))

    # Sloped Earth Ramp on the rear side (Y = -2.0m to -0.5m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, -1.20, 0.55)))
                          @ Matrix.Rotation(math.radians(-16), 4, 'X') @ Matrix.Diagonal((6.0, 1.80, 0.20, 1.0)))

    # Solid Foundation Earth Core
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.20, 0.50)))
                          @ Matrix.Diagonal((5.80, 3.20, 1.00, 1.0)))

    # Low Step Blocks flanking the bank
    for sx in [-3.1, 3.1]:
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((sx, 0.5, 0.60)))
                              @ Matrix.Diagonal((0.40, 3.60, 1.20, 1.0)))

    bm.to_mesh(mesh)
    bm.free()

    obj.data.materials.append(mat_dirt_earth())
    obj.data.materials.append(mat_lahori_brick())

    return obj


# =========================================================================
# 4. BRITISH ARMORED CAR OBSTACLE (SM_British_Armored_Car_Obstacle)
# =========================================================================
def build_armored_car_obstacle(name="SM_British_Armored_Car_Obstacle"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # 1919 Austin Armored Car: Length 4.8m along Y, Width 2.1m along X, Height 2.4m along Z
    # Heavy Steel Chassis Frame (Z = 0.45 to 0.70m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 0.55)))
                          @ Matrix.Diagonal((1.60, 4.40, 0.20, 1.0)))

    # Lower Armored Hull (Z = 0.65 to 1.45m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, -0.2, 1.05)))
                          @ Matrix.Diagonal((1.90, 4.20, 0.80, 1.0)))

    # Sloped Engine Hood / Louvered Grille at Front (Y = 1.3 to 2.3m, Z = 0.75 to 1.35m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 1.75, 1.05)))
                          @ Matrix.Diagonal((1.40, 1.30, 0.60, 1.0)))
    # Front Heavy Iron Bumper (Y = 2.45m, Z = 0.55m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 2.45, 0.55)))
                          @ Matrix.Diagonal((1.95, 0.15, 0.15, 1.0)))

    # Armored Driver Cabin with Slotted Visor Louvers (Y = 0.4 to 1.2m, Z = 1.35 to 1.95m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.80, 1.65)))
                          @ Matrix.Diagonal((1.85, 0.90, 0.60, 1.0)))
    # Visor flaps
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 1.26, 1.68)))
                          @ Matrix.Diagonal((1.40, 0.05, 0.20, 1.0)))

    # Rear Troop / Ammunition Compartment (Y = -1.9 to 0.4m, Z = 1.25 to 1.90m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, -0.75, 1.55)))
                          @ Matrix.Diagonal((1.85, 2.30, 0.65, 1.0)))

    # Cylindrical Rotating Machine Gun Turret on Roof (Z = 1.90 to 2.45m, radius 0.65m)
    bmesh.ops.create_cone(bm, cap_ends=True, segments=18, radius1=0.65, radius2=0.65, depth=0.55,
                          matrix=Matrix.Translation(Vector((0.0, -0.35, 2.18))))
    # Turret Domed Cap
    bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=0.65, radius2=0.15, depth=0.20,
                          matrix=Matrix.Translation(Vector((0.0, -0.35, 2.55))))

    # Twin Vickers Machine Gun Barrels projecting forward from turret
    for gun_x in [-0.22, 0.22]:
        bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=0.045, radius2=0.035, depth=0.95,
                              matrix=Matrix.Translation(Vector((gun_x, 0.45, 2.22))) @ Matrix.Rotation(math.radians(-90), 4, 'X'))
        # Flash hider muzzle
        bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.055, radius2=0.055, depth=0.10,
                              matrix=Matrix.Translation(Vector((gun_x, 0.95, 2.22))) @ Matrix.Rotation(math.radians(-90), 4, 'X'))

    # 4 Heavy Steel Spoked Road Wheels with Solid Rubber Tires (radius 0.50m)
    wheel_coords = [(-1.05, 1.4), (1.05, 1.4), (-1.05, -1.3), (1.05, -1.3)]
    for wx, wy in wheel_coords:
        # Solid rubber tire
        bmesh.ops.create_cone(bm, cap_ends=True, segments=20, radius1=0.50, radius2=0.50, depth=0.22,
                              matrix=Matrix.Translation(Vector((wx, wy, 0.50))) @ Matrix.Rotation(math.radians(90), 4, 'Y'))
        # Steel hub
        bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.20, radius2=0.20, depth=0.28,
                              matrix=Matrix.Translation(Vector((wx, wy, 0.50))) @ Matrix.Rotation(math.radians(90), 4, 'Y'))
        # Armored mudguard arch above wheel
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((wx, wy, 1.10)))
                              @ Matrix.Diagonal((0.30, 1.25, 0.15, 1.0)))

    bm.to_mesh(mesh)
    bm.free()

    obj.data.materials.append(mat_armored_steel())
    obj.data.materials.append(mat_wrought_iron())

    return obj


# =========================================================================
# 5. BAISAKHI PANDAL ASSEMBLY PLATFORM (SM_Jallianwala_Baisakhi_Pandal)
# =========================================================================
def build_jallianwala_baisakhi_pandal(name="SM_Jallianwala_Baisakhi_Pandal"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Low Timber Takhtposh Dais Platform (4.0m width X, 3.0m depth Y, 0.40m height Z)
    # Timber platform deck
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 0.20)))
                          @ Matrix.Diagonal((4.0, 3.0, 0.40, 1.0)))

    # Woven White Khadi Sheet covering the platform
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 0.41)))
                          @ Matrix.Diagonal((3.90, 2.90, 0.04, 1.0)))

    # Persian Pattern Carpet Runner down the center (Y = -1.3 to +1.3m, width 1.2m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 0.43)))
                          @ Matrix.Diagonal((1.20, 2.80, 0.02, 1.0)))

    # Traditional Long Masnad Bolsters (Cylindrical cotton cushions, radius 0.18m, length 1.2m)
    # Rear Bolster 1
    bmesh.ops.create_cone(bm, cap_ends=True, segments=14, radius1=0.18, radius2=0.18, depth=1.3,
                          matrix=Matrix.Translation(Vector((-1.0, 0.8, 0.60))) @ Matrix.Rotation(math.radians(90), 4, 'Y'))
    # Rear Bolster 2
    bmesh.ops.create_cone(bm, cap_ends=True, segments=14, radius1=0.18, radius2=0.18, depth=1.3,
                          matrix=Matrix.Translation(Vector((1.0, 0.8, 0.60))) @ Matrix.Rotation(math.radians(90), 4, 'Y'))

    # Wooden Speech Podium / Lectern at Front (X = 0.0, Y = -1.1, Z = 0.4 to 1.4m)
    # Base
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, -1.1, 0.50)))
                          @ Matrix.Diagonal((0.60, 0.50, 0.15, 1.0)))
    # Pillar
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, -1.1, 0.90)))
                          @ Matrix.Diagonal((0.25, 0.25, 0.70, 1.0)))
    # Sloped Reading Desk
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, -1.1, 1.30)))
                          @ Matrix.Rotation(math.radians(20), 4, 'X') @ Matrix.Diagonal((0.70, 0.55, 0.06, 1.0)))

    # 4 Bamboo Corner Posts supporting Shamiana Canopy (X = ±1.9m, Y = ±1.4m, Z = 0.4 to 3.2m)
    canopy_posts = [(-1.9, -1.4), (1.9, -1.4), (1.9, 1.4), (-1.9, 1.4)]
    for bx, by in canopy_posts:
        bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.045, radius2=0.035, depth=2.8,
                              matrix=Matrix.Translation(Vector((bx, by, 1.8))))

    # Striped Shamiana Fabric Canopy Roof (Z = 3.2m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 3.25)))
                          @ Matrix.Diagonal((4.20, 3.20, 0.08, 1.0)))

    # Hanging Saffron Fabric Valance / Frills along Canopy Borders
    for vy in [-1.55, 1.55]:
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, vy, 3.10)))
                              @ Matrix.Diagonal((4.20, 0.04, 0.25, 1.0)))
    for vx in [-2.05, 2.05]:
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((vx, 0.0, 3.10)))
                              @ Matrix.Diagonal((0.04, 3.20, 0.25, 1.0)))

    bm.to_mesh(mesh)
    bm.free()

    obj.data.materials.append(mat_aged_teak())
    obj.data.materials.append(mat_cloth_khadi())
    obj.data.materials.append(mat_cloth_saffron())

    return obj


# =========================================================================
# EXPORT PIPELINE & DUAL-FOLDER PERSISTENCE
# =========================================================================
def export_asset(builder_func, asset_name):
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
    print("================ TASK 6: JALLIANWALA BAGH ENCLOSED GARDEN ASSET GENERATOR ================")

    assets = [
        (build_shahidi_kua_well, "SM_Jallianwala_Shahidi_Kua_Well"),
        (build_jallianwala_enclosure_wall, "SM_Jallianwala_Enclosure_Wall"),
        (build_jallianwala_raised_bank, "SM_Jallianwala_Raised_Bank"),
        (build_armored_car_obstacle, "SM_British_Armored_Car_Obstacle"),
        (build_jallianwala_baisakhi_pandal, "SM_Jallianwala_Baisakhi_Pandal"),
    ]

    for builder, name in assets:
        export_asset(builder, name)

    print("================ ALL 5 JALLIANWALA BAGH ASSETS GENERATED & EXPORTED TO DUAL TARGETS ================")

if __name__ == "__main__":
    main()
