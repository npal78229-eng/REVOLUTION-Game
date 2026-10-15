"""
PROJECT REVOLUTION — Task 5: The Road to Jallianwala Bagh (Baisakhi Gathering & Proclamation)
Toolchain: Blender 5.2 LTS Headless Pipeline
Generates 5 authentic monumental and period assets for April 13, 1919:
1. SM_Munadi_Proclamation_Drum (Nagara drum on tripod with beaters & British proclamation parchment)
2. SM_Baisakhi_Garland_Archway (Festive arched portal with marigold garlands & mango leaf toran)
3. SM_Jallianwala_Narrow_Gateway (Historic 2.2m claustrophobic corridor gateway into Jallianwala Bagh)
4. SM_Prop_Wheat_Sheaves_Cart (Punjabi bullock harvest cart with spoked wheels & golden wheat sheaves)
5. SM_Baisakhi_Mela_Sweet_Stall (Festive halwai market platform with jalebi platters, brass samovar & bunting)
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

def mat_brass():
    return get_pbr_material("M_Brass_PBR", (0.80, 0.64, 0.22, 1.0), roughness=0.32, metallic=0.85)

def mat_clay():
    return get_pbr_material("M_Clay_PBR", (0.62, 0.34, 0.22, 1.0), roughness=0.86, metallic=0.0)

def mat_leather_drum():
    return get_pbr_material("M_LeatherDrum_PBR", (0.72, 0.65, 0.50, 1.0), roughness=0.70, metallic=0.0)

def mat_marigold_orange():
    return get_pbr_material("M_Marigold_Orange_PBR", (0.95, 0.45, 0.05, 1.0), roughness=0.80, metallic=0.0)

def mat_mango_leaf_green():
    return get_pbr_material("M_MangoLeaf_Green_PBR", (0.18, 0.45, 0.12, 1.0), roughness=0.65, metallic=0.0)

def mat_wheat_golden():
    return get_pbr_material("M_Wheat_Golden_PBR", (0.88, 0.72, 0.30, 1.0), roughness=0.85, metallic=0.0)

def mat_parchment_scroll():
    return get_pbr_material("M_Parchment_Scroll_PBR", (0.85, 0.80, 0.68, 1.0), roughness=0.88, metallic=0.0)


# =========================================================================
# 1. MUNADI PROCLAMATION DRUM (SM_Munadi_Proclamation_Drum)
# =========================================================================
def build_munadi_proclamation_drum(name="SM_Munadi_Proclamation_Drum"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Tripod Stand (Teak wood legs meeting under the drum at Z = 0.75m)
    leg_radius = 0.04
    leg_height = 0.85
    spread = 0.38
    for i in range(3):
        angle = i * (2.0 * math.pi / 3.0)
        lx = math.cos(angle) * spread
        ly = math.sin(angle) * spread
        # Base to apex
        v_base = Vector((lx, ly, 0.0))
        v_apex = Vector((lx * 0.3, ly * 0.3, leg_height))
        diff = v_apex - v_base
        length = diff.length
        center = (v_base + v_apex) / 2.0
        # Cylinder aligned to leg direction
        rot = Vector((0, 0, 1)).rotation_difference(diff).to_matrix().to_4x4()
        bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=leg_radius, radius2=leg_radius, depth=length,
                              matrix=Matrix.Translation(center) @ rot)

    # Tripod Ring Brace (Iron hoop connecting legs at Z = 0.35m)
    bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=0.28, radius2=0.28, depth=0.03,
                          matrix=Matrix.Translation(Vector((0.0, 0.0, 0.35))))

    # Copper/Brass Kettle Drum Body (Nagara)
    # Drum bowl (Z = 0.75 to 1.15m, radius 0.42m at top, 0.22m at bottom)
    bmesh.ops.create_cone(bm, cap_ends=True, segments=20, radius1=0.42, radius2=0.22, depth=0.38,
                          matrix=Matrix.Translation(Vector((0.0, 0.0, 0.94))))

    # Drum Rim Ring (Z = 1.13m, outer radius 0.44m)
    bmesh.ops.create_cone(bm, cap_ends=True, segments=20, radius1=0.45, radius2=0.45, depth=0.05,
                          matrix=Matrix.Translation(Vector((0.0, 0.0, 1.13))))

    # Drumhead Skin (Flat circular membrane slightly recessed at Z = 1.15m)
    bmesh.ops.create_cone(bm, cap_ends=True, segments=20, radius1=0.42, radius2=0.42, depth=0.01,
                          matrix=Matrix.Translation(Vector((0.0, 0.0, 1.15))))

    # Tension Rawhide Ropes / Lacing Pegs (around perimeter)
    for i in range(12):
        angle = i * (2.0 * math.pi / 12.0)
        rx = math.cos(angle) * 0.44
        ry = math.sin(angle) * 0.44
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((rx, ry, 1.02))) @ Matrix.Diagonal((0.03, 0.03, 0.16, 1.0)))

    # Twin Wooden Curved Drum Beaters (Danka) resting on drum
    # Beater 1
    bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.02, radius2=0.015, depth=0.45,
                          matrix=Matrix.Translation(Vector((-0.10, 0.05, 1.19))) @ Matrix.Rotation(math.radians(25), 4, 'Z') @ Matrix.Rotation(math.radians(85), 4, 'X'))
    # Knob 1
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((-0.26, -0.04, 1.20))) @ Matrix.Diagonal((0.05, 0.05, 0.05, 1.0)))
    # Beater 2
    bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.02, radius2=0.015, depth=0.45,
                          matrix=Matrix.Translation(Vector((0.10, -0.05, 1.19))) @ Matrix.Rotation(math.radians(-30), 4, 'Z') @ Matrix.Rotation(math.radians(85), 4, 'X'))
    # Knob 2
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.26, 0.04, 1.20))) @ Matrix.Diagonal((0.05, 0.05, 0.05, 1.0)))

    # Proclamation Parchment Scroll (attached to tripod leg)
    # Scroll sheet hanging down (Z = 0.30 to 0.65m, width = 0.30m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.28, 0.0, 0.48))) @ Matrix.Diagonal((0.02, 0.32, 0.36, 1.0)))
    # Pinned seal at top
    bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.03, radius2=0.03, depth=0.02,
                          matrix=Matrix.Translation(Vector((0.29, 0.0, 0.64))) @ Matrix.Rotation(math.radians(90), 4, 'Y'))

    bm.to_mesh(mesh)
    bm.free()

    obj.data.materials.append(mat_brass())
    obj.data.materials.append(mat_aged_teak())
    obj.data.materials.append(mat_leather_drum())
    obj.data.materials.append(mat_parchment_scroll())

    return obj


# =========================================================================
# 2. BAISAKHI GARLAND ARCHWAY (SM_Baisakhi_Garland_Archway)
# =========================================================================
def build_baisakhi_garland_archway(name="SM_Baisakhi_Garland_Archway"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Grand Festive Gateway: 4.2m width across roadway, 0.8m depth, 4.4m height
    # Twin Timber Carved Posts (X = -1.9m and +1.9m)
    for px in [-1.9, 1.9]:
        # Stone Plinth Base
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((px, 0.0, 0.25))) @ Matrix.Diagonal((0.60, 0.60, 0.50, 1.0)))
        # Main Wooden Pillar
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((px, 0.0, 2.10))) @ Matrix.Diagonal((0.40, 0.40, 3.20, 1.0)))
        # Carved Capital Bracket
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((px, 0.0, 3.75))) @ Matrix.Diagonal((0.65, 0.65, 0.30, 1.0)))

    # Main Overhead Lintel Beam (Z = 3.9m, length = 4.6m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 4.0))) @ Matrix.Diagonal((4.60, 0.50, 0.35, 1.0)))

    # Decorative Cusped Wooden Arch Facade under lintel
    # Corbel brackets flanking arch
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((-1.5, 0.0, 3.65))) @ Matrix.Diagonal((0.50, 0.45, 0.35, 1.0)))
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((1.5, 0.0, 3.65))) @ Matrix.Diagonal((0.50, 0.45, 0.35, 1.0)))

    # Marigold Garlands (Genda Phool): Dense drooping loops across the arch
    # Main Central Droop (parabolic arc of marigold blooms)
    for step in range(21):
        t = -1.7 + (3.4 * (step / 20.0))
        # Parabolic sag: lowest in center
        z_droop = 3.85 - (0.55 * (1.0 - (t / 1.7) ** 2))
        y_offset = -0.28
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((t, y_offset, z_droop))) @ Matrix.Diagonal((0.14, 0.14, 0.14, 1.0)))

    # Second Lower Garland Droop
    for step in range(17):
        t = -1.4 + (2.8 * (step / 16.0))
        z_droop = 3.60 - (0.45 * (1.0 - (t / 1.4) ** 2))
        y_offset = -0.26
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((t, y_offset, z_droop))) @ Matrix.Diagonal((0.12, 0.12, 0.12, 1.0)))

    # Vertical Hanging Marigold Strands on both pillars
    for px in [-1.88, 1.88]:
        for y_side in [-0.22, 0.22]:
            for z_step in range(15):
                z_pos = 1.0 + (z_step * 0.18)
                bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((px, y_side, z_pos))) @ Matrix.Diagonal((0.10, 0.10, 0.10, 1.0)))

    # Mango Leaf Toran (Festoons under the main lintel)
    for step in range(25):
        t = -1.8 + (3.6 * (step / 24.0))
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((t, -0.25, 3.80))) @ Matrix.Diagonal((0.10, 0.04, 0.18, 1.0)))

    # Overhead Festive Bunting & Khadi Canopy Banner (Z = 4.25m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 4.30))) @ Matrix.Diagonal((4.20, 0.30, 0.25, 1.0)))

    bm.to_mesh(mesh)
    bm.free()

    obj.data.materials.append(mat_aged_teak())
    obj.data.materials.append(mat_marigold_orange())
    obj.data.materials.append(mat_mango_leaf_green())
    obj.data.materials.append(mat_lahori_brick())

    return obj


# =========================================================================
# 3. JALLIANWALA BAGH NARROW GATEWAY (SM_Jallianwala_Narrow_Gateway)
# =========================================================================
def build_jallianwala_narrow_gateway(name="SM_Jallianwala_Narrow_Gateway"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Historic Dimensions:
    # 2.2m clear passage width (X = -1.1 to +1.1m)
    # 6.0m corridor depth along Y (Y = -3.0 to +3.0m)
    # 5.0m wall height along Z
    wall_thickness = 1.2
    corridor_length = 6.0
    wall_height = 5.0
    clear_width = 2.2

    # Left Flanking Haveli Wall (X = -1.1 to -2.3m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((-(clear_width / 2.0 + wall_thickness / 2.0), 0.0, wall_height / 2.0)))
                          @ Matrix.Diagonal((wall_thickness, corridor_length, wall_height, 1.0)))

    # Right Flanking Haveli Wall (X = +1.1 to +2.3m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector(((clear_width / 2.0 + wall_thickness / 2.0), 0.0, wall_height / 2.0)))
                          @ Matrix.Diagonal((wall_thickness, corridor_length, wall_height, 1.0)))

    # Entrance Overhead Corbelled Arch & Brick Lintel (Front at Y = -2.7m, Z = 3.5 to 5.0m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, -2.7, 4.25)))
                          @ Matrix.Diagonal((clear_width, 0.60, 1.50, 1.0)))

    # Exit Overhead Arch (Rear at Y = +2.7m, Z = 3.5 to 5.0m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 2.7, 4.25)))
                          @ Matrix.Diagonal((clear_width, 0.60, 1.50, 1.0)))

    # Walkable Corridor Paved Brick Floor Slab (Z = 0.0 to 0.15m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 0.08)))
                          @ Matrix.Diagonal((clear_width, corridor_length, 0.15, 1.0)))

    # Historic Iron Wicket Gate / Security Grille framing entrance (recessed at Y = -2.4m)
    # Iron Posts
    for gx in [-1.05, 1.05]:
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((gx, -2.4, 1.70)))
                              @ Matrix.Diagonal((0.08, 0.08, 3.40, 1.0)))
    # Iron Horizontal Railings
    for gz in [0.4, 1.2, 2.0, 2.8, 3.4]:
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, -2.4, gz)))
                              @ Matrix.Diagonal((2.10, 0.04, 0.04, 1.0)))
    # Iron Vertical Bars
    for b_idx in range(9):
        bx = -0.90 + (b_idx * 0.225)
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((bx, -2.4, 1.70)))
                              @ Matrix.Diagonal((0.03, 0.03, 3.30, 1.0)))

    # Projected Roof Parapet / Kanguras along top edge of corridor walls (Z = 5.0 to 5.4m)
    for side_x in [-(clear_width / 2.0 + wall_thickness / 2.0), (clear_width / 2.0 + wall_thickness / 2.0)]:
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((side_x, 0.0, 5.20)))
                              @ Matrix.Diagonal((wall_thickness + 0.2, corridor_length, 0.40, 1.0)))

    bm.to_mesh(mesh)
    bm.free()

    obj.data.materials.append(mat_lahori_brick())
    obj.data.materials.append(mat_wrought_iron())
    obj.data.materials.append(mat_aged_teak())

    return obj


# =========================================================================
# 4. WHEAT SHEAVES HARVEST CART (SM_Prop_Wheat_Sheaves_Cart)
# =========================================================================
def build_wheat_sheaves_cart(name="SM_Prop_Wheat_Sheaves_Cart"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Heavy Punjabi Bullock Cart (Bail Gadi):
    # Length 3.2m along Y, Width 1.6m along X, Height ~1.8m to top of wheat pile
    # Main Heavy Axle Beam (Z = 0.65m, length = 1.9m along X)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 0.65)))
                          @ Matrix.Diagonal((1.90, 0.16, 0.16, 1.0)))

    # Twin Large Spoked Wooden Wheels (X = -0.92m and +0.92m, radius = 0.65m)
    wheel_radius = 0.65
    for wx in [-0.92, 0.92]:
        # Outer Iron Rim
        bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=wheel_radius, radius2=wheel_radius, depth=0.08,
                              matrix=Matrix.Translation(Vector((wx, 0.0, 0.65))) @ Matrix.Rotation(math.radians(90), 4, 'Y'))
        # Wheel Hub
        bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.14, radius2=0.14, depth=0.22,
                              matrix=Matrix.Translation(Vector((wx, 0.0, 0.65))) @ Matrix.Rotation(math.radians(90), 4, 'Y'))
        # 12 Spokes
        for s in range(12):
            s_angle = s * (2.0 * math.pi / 12.0)
            sz = math.sin(s_angle) * (wheel_radius * 0.5)
            sy = math.cos(s_angle) * (wheel_radius * 0.5)
            bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((wx, sy, 0.65 + sz)))
                                  @ Matrix.Rotation(s_angle, 4, 'X') @ Matrix.Diagonal((0.04, 0.05, wheel_radius, 1.0)))

    # Timber Chassis Frame (Bed Z = 0.76m, length = 2.8m, width = 1.4m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.1, 0.76)))
                          @ Matrix.Diagonal((1.40, 2.60, 0.08, 1.0)))

    # Slatted Side Rails
    for rx in [-0.68, 0.68]:
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((rx, 0.1, 1.0)))
                              @ Matrix.Diagonal((0.06, 2.60, 0.40, 1.0)))
    # Rear Gate
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, -1.2, 1.0)))
                          @ Matrix.Diagonal((1.36, 0.06, 0.40, 1.0)))

    # Draught Poles / Yoke Beams extending forward (Y = 1.4 to 3.0m)
    for yx in [-0.35, 0.35]:
        bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.06, radius2=0.04, depth=1.8,
                              matrix=Matrix.Translation(Vector((yx, 2.1, 0.50))) @ Matrix.Rotation(math.radians(-10), 4, 'X'))
    # Cross Yoke Beam (Y = 2.9m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 2.9, 0.35)))
                          @ Matrix.Diagonal((1.50, 0.12, 0.10, 1.0)))

    # Golden Baisakhi Wheat Sheaves (High piled bundle volumes)
    # Lower layer bundles
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.1, 1.15)))
                          @ Matrix.Diagonal((1.30, 2.40, 0.45, 1.0)))
    # Upper heaped sheaf mound
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 1.45)))
                          @ Matrix.Diagonal((1.10, 1.80, 0.40, 1.0)))
    # Individual Wheat Sheaf Heads projecting at rear and sides
    for sheaf_idx in range(6):
        sy = -0.9 + (sheaf_idx * 0.35)
        bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.18, radius2=0.08, depth=0.6,
                              matrix=Matrix.Translation(Vector((-0.65, sy, 1.25))) @ Matrix.Rotation(math.radians(35), 4, 'Y'))
        bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.18, radius2=0.08, depth=0.6,
                              matrix=Matrix.Translation(Vector((0.65, sy, 1.25))) @ Matrix.Rotation(math.radians(-35), 4, 'Y'))

    # Tether Ropes binding sheaves (iron/hemp straps)
    for rope_y in [-0.5, 0.1, 0.7]:
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, rope_y, 1.48)))
                              @ Matrix.Diagonal((1.18, 0.05, 0.50, 1.0)))

    bm.to_mesh(mesh)
    bm.free()

    obj.data.materials.append(mat_aged_teak())
    obj.data.materials.append(mat_wrought_iron())
    obj.data.materials.append(mat_wheat_golden())

    return obj


# =========================================================================
# 5. BAISAKHI MELA SWEET STALL (SM_Baisakhi_Mela_Sweet_Stall)
# =========================================================================
def build_baisakhi_mela_sweet_stall(name="SM_Baisakhi_Mela_Sweet_Stall"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Timber Takhtposh Platform (2.2m width, 1.4m depth, 0.55m height)
    # Legs
    for lx in [-1.0, 1.0]:
        for ly in [-0.6, 0.6]:
            bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((lx, ly, 0.25)))
                                  @ Matrix.Diagonal((0.12, 0.12, 0.50, 1.0)))
    # Tabletop
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 0.53)))
                          @ Matrix.Diagonal((2.20, 1.40, 0.06, 1.0)))

    # Large Hammered Brass Platters (Thalis) laden with Jalebis
    # Platter 1 (Left)
    bmesh.ops.create_cone(bm, cap_ends=True, segments=20, radius1=0.35, radius2=0.32, depth=0.04,
                          matrix=Matrix.Translation(Vector((-0.55, 0.10, 0.58))))
    # Golden Jalebi pile 1
    bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=0.30, radius2=0.20, depth=0.10,
                          matrix=Matrix.Translation(Vector((-0.55, 0.10, 0.63))))

    # Platter 2 (Right)
    bmesh.ops.create_cone(bm, cap_ends=True, segments=20, radius1=0.35, radius2=0.32, depth=0.04,
                          matrix=Matrix.Translation(Vector((0.55, 0.10, 0.58))))
    # Golden Laddu pile 2
    bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=0.30, radius2=0.20, depth=0.10,
                          matrix=Matrix.Translation(Vector((0.55, 0.10, 0.63))))

    # Brass Chai Samovar / Large Kettle (Center Rear)
    bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=0.18, radius2=0.16, depth=0.45,
                          matrix=Matrix.Translation(Vector((0.0, 0.35, 0.80))))
    # Samovar Lid & Spigot
    bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.12, radius2=0.04, depth=0.12,
                          matrix=Matrix.Translation(Vector((0.0, 0.35, 1.08))))

    # Clay Kulhads (stacked along table front)
    for kx in [-0.25, -0.10, 0.05, 0.20]:
        bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=0.045, radius2=0.03, depth=0.08,
                              matrix=Matrix.Translation(Vector((kx, -0.45, 0.60))))

    # Festive Bamboo Canopy Frame with Triangular Bunting Flags
    for bx in [-1.05, 1.05]:
        bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.035, radius2=0.03, depth=2.4,
                              matrix=Matrix.Translation(Vector((bx, -0.65, 1.20))))
    # Cross pole
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, -0.65, 2.35)))
                          @ Matrix.Diagonal((2.20, 0.05, 0.05, 1.0)))

    # Triangular Paper/Cloth Flags suspended from pole
    for f in range(9):
        fx = -0.9 + (f * 0.22)
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((fx, -0.65, 2.22)))
                              @ Matrix.Diagonal((0.15, 0.02, 0.22, 1.0)))

    bm.to_mesh(mesh)
    bm.free()

    obj.data.materials.append(mat_aged_teak())
    obj.data.materials.append(mat_brass())
    obj.data.materials.append(mat_clay())
    obj.data.materials.append(mat_marigold_orange())

    return obj


# =========================================================================
# EXPORT PIPELINE & DUAL-FOLDER SYNC
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
    print("================ TASK 5: BAISAKHI GATHERING & PROCLAMATION ASSET GENERATOR ================")

    assets = [
        (build_munadi_proclamation_drum, "SM_Munadi_Proclamation_Drum"),
        (build_baisakhi_garland_archway, "SM_Baisakhi_Garland_Archway"),
        (build_jallianwala_narrow_gateway, "SM_Jallianwala_Narrow_Gateway"),
        (build_wheat_sheaves_cart, "SM_Prop_Wheat_Sheaves_Cart"),
        (build_baisakhi_mela_sweet_stall, "SM_Baisakhi_Mela_Sweet_Stall"),
    ]

    for builder, name in assets:
        export_asset(builder, name)

    print("================ ALL 5 BAISAKHI ASSETS GENERATED & EXPORTED TO DUAL TARGETS ================")

if __name__ == "__main__":
    main()
