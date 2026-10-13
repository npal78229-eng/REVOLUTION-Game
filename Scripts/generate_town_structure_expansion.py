"""
PROJECT REVOLUTION — Town Structure Expansion Generator
Toolchain: Blender 5.2 LTS Headless Pipeline
Generates 5 authentic monumental architectural & narrative structures for 1919 Punjab:
1. SM_Wall_Town_Faseel_Rampart (Heavy 6m Lahori brick defensive perimeter wall with walkway & kanguras)
2. SM_Checkpoint_Picket_Sandbag_Barrier (British military sandbag revetment, wooden blockade & curfew sign)
3. SM_Haveli_Facade_3Story_Jharokha (Monumental 12m 3-story haveli facade with projecting teak jharokha)
4. SM_Prop_Litho_Press_Flatbed (Authentic cast-iron flatbed stone lithographic hand press & flywheel)
5. SM_Mohalla_Pyaoo_Water_Shelter (Covered roadside drinking water kiosk with timber pillars & matkas)
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

def mat_lahori_brick():
    return get_pbr_material("M_LahoriBrick_PBR", (0.58, 0.22, 0.14, 1.0), roughness=0.85, metallic=0.0)

def mat_aged_teak():
    return get_pbr_material("M_AgedTeak_PBR", (0.34, 0.22, 0.14, 1.0), roughness=0.78, metallic=0.0)

def mat_wrought_iron():
    return get_pbr_material("M_WroughtIron_PBR", (0.12, 0.12, 0.13, 1.0), roughness=0.62, metallic=0.88)

def mat_clay():
    return get_pbr_material("M_Clay_PBR", (0.62, 0.34, 0.22, 1.0), roughness=0.86, metallic=0.0)

def mat_brass():
    return get_pbr_material("M_Brass_PBR", (0.78, 0.62, 0.24, 1.0), roughness=0.35, metallic=0.85)

def mat_cloth_indigo():
    return get_pbr_material("M_ClothIndigo_PBR", (0.16, 0.24, 0.44, 1.0), roughness=0.92, metallic=0.0)

def mat_jute():
    return get_pbr_material("M_Jute_PBR", (0.48, 0.40, 0.28, 1.0), roughness=0.92, metallic=0.0)

def mat_limestone():
    return get_pbr_material("M_Limestone_PBR", (0.72, 0.68, 0.60, 1.0), roughness=0.75, metallic=0.0)

def create_cylinder_mesh(bm, radius, depth, segments=12, matrix=None):
    res = bmesh.ops.create_cone(bm, cap_ends=True, segments=segments, radius1=radius, radius2=radius, depth=depth)
    if matrix is not None:
        bmesh.ops.transform(bm, verts=res['verts'], matrix=matrix)
    return res


# =========================================================================
# 1. LAHORI BRICK DEFENSIVE TOWN PERIMETER RAMPART (SM_Wall_Town_Faseel_Rampart)
# =========================================================================
def build_town_faseel_rampart(name="SM_Wall_Town_Faseel_Rampart"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Dimensions: 6.0m width (along X), 1.2m depth (along Y), 6.0m height (along Z)
    # Plinth Base (Z = 0 to 0.6m, width = 6.0m, depth = 1.6m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 0.30))) @ Matrix.Diagonal((6.0, 1.6, 0.60, 1.0)))

    # Main Wall Body (Z = 0.6 to 4.8m, depth = 1.2m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 2.70))) @ Matrix.Diagonal((6.0, 1.2, 4.20, 1.0)))

    # Flanking Pilasters / Buttresses on exterior face (Y = -0.65m)
    for x_pos in [-2.6, 0.0, 2.6]:
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((x_pos, -0.68, 2.40))) @ Matrix.Diagonal((0.70, 0.25, 4.60, 1.0)))

    # Sentry Walkway on interior face (Y = +0.2m, Z = 4.8m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.35, 4.70))) @ Matrix.Diagonal((6.0, 0.60, 0.20, 1.0)))

    # Battlement Parapet with Kanguras (Z = 4.8 to 6.0m)
    # Continuous low front parapet
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, -0.45, 5.25))) @ Matrix.Diagonal((6.0, 0.30, 0.90, 1.0)))

    # 6 stepped Kangura battlements along the top
    for i in range(6):
        kx = -2.5 + i * 1.0
        # Lower kangura block
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((kx, -0.45, 5.80))) @ Matrix.Diagonal((0.55, 0.32, 0.40, 1.0)))
        # Upper pointed cap
        bmesh.ops.create_cone(bm, cap_ends=True, segments=4, radius1=0.22, radius2=0.0, depth=0.35, matrix=Matrix.Translation(Vector((kx, -0.45, 6.15))))

    # Wrought-iron S-anchor plates on exterior facade
    for x_pos in [-2.0, 2.0]:
        for z_pos in [1.8, 3.8]:
            create_cylinder_mesh(bm, radius=0.12, depth=0.06, segments=8, matrix=Matrix.Translation(Vector((x_pos, -0.62, z_pos))) @ Matrix.Rotation(math.radians(90.0), 4, 'X'))

    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(mat_lahori_brick())
    mesh.materials.append(mat_wrought_iron())

    return obj


# =========================================================================
# 2. BRITISH CHECKPOINT PICKET & BARRICADE (SM_Checkpoint_Picket_Sandbag_Barrier)
# =========================================================================
def build_checkpoint_picket_barrier(name="SM_Checkpoint_Picket_Sandbag_Barrier"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Sandbag Revetment (Length = 3.6m, depth = 0.8m, height = 1.1m)
    for row in range(4):
        z_layer = 0.12 + row * 0.26
        num_bags = 8 if row % 2 == 0 else 7
        offset = 0.0 if row % 2 == 0 else 0.22
        for b in range(num_bags):
            bx = -1.6 + offset + b * 0.46
            rot_z = math.radians((b % 3 - 1) * 3.5)
            bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((bx, 0.0, z_layer))) @ Matrix.Rotation(rot_z, 4, 'Z') @ Matrix.Diagonal((0.48, 0.34, 0.24, 1.0)))

    # Timber X-frame road blockade (Cheval de frise saw-horses) on side (X = 1.0 to 2.8)
    for x_center in [1.4, 2.4]:
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((x_center, -0.6, 0.60))) @ Matrix.Rotation(math.radians(45.0), 4, 'Y') @ Matrix.Diagonal((0.14, 0.14, 1.40, 1.0)))
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((x_center, -0.6, 0.60))) @ Matrix.Rotation(math.radians(-45.0), 4, 'Y') @ Matrix.Diagonal((0.14, 0.14, 1.40, 1.0)))

    # Horizontal connecting log beam
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((1.9, -0.6, 0.65))) @ Matrix.Diagonal((1.40, 0.16, 0.16, 1.0)))

    # Iron Signpost with Section 144 Notice Board (X = -1.2, Y = -0.4, Z = 0 to 2.2m)
    create_cylinder_mesh(bm, radius=0.04, depth=2.20, segments=10, matrix=Matrix.Translation(Vector((-1.2, -0.4, 1.10))))
    # Sign board plate (0.8m x 0.6m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((-1.2, -0.4, 1.80))) @ Matrix.Diagonal((0.80, 0.04, 0.60, 1.0)))
    # Royal crown finial on top of post
    bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.08, radius2=0.0, depth=0.15, matrix=Matrix.Translation(Vector((-1.2, -0.4, 2.25))))

    # Kerosene Warning Lantern hung from arm bracket
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((-0.95, -0.4, 1.70))) @ Matrix.Diagonal((0.50, 0.03, 0.03, 1.0)))
    create_cylinder_mesh(bm, radius=0.09, depth=0.28, segments=8, matrix=Matrix.Translation(Vector((-0.72, -0.4, 1.52))))

    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(mat_jute())
    mesh.materials.append(mat_aged_teak())
    mesh.materials.append(mat_wrought_iron())

    return obj


# =========================================================================
# 3. MONUMENTAL 3-STORY HAVELI FACADE WITH TEAK JHAROKHA (SM_Haveli_Facade_3Story_Jharokha)
# =========================================================================
def build_haveli_facade_3story(name="SM_Haveli_Facade_3Story_Jharokha"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Scale: 8.0m wide (X), 0.8m deep (Y), 12.0m tall (Z)
    # Ground Floor Base Wall (Z = 0 to 4.0m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 2.0))) @ Matrix.Diagonal((8.0, 0.80, 4.0, 1.0)))

    # Ground Floor Arched Portal Recess (X = 0, Y = -0.2, Z = 0 to 2.8m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, -0.25, 1.30))) @ Matrix.Diagonal((2.20, 0.40, 2.60, 1.0)))
    # Teak Takhta Shutters inside portal
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, -0.15, 1.20))) @ Matrix.Diagonal((1.90, 0.10, 2.40, 1.0)))

    # Floor 1 Horizontal Cornice Belt (Z = 4.0m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, -0.45, 4.0))) @ Matrix.Diagonal((8.20, 0.30, 0.25, 1.0)))

    # Floor 1 Main Wall (Z = 4.0 to 8.0m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 6.0))) @ Matrix.Diagonal((8.0, 0.80, 4.0, 1.0)))

    # Central Projecting Carved Teak Jharokha Balcony (Z = 4.3 to 7.2m, X = 0, projecting to Y = -1.2)
    # 4 Ornate Todis (Carved Corbel Brackets)
    for bx in [-0.9, -0.3, 0.3, 0.9]:
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((bx, -0.65, 4.50))) @ Matrix.Rotation(math.radians(-30.0), 4, 'X') @ Matrix.Diagonal((0.16, 0.45, 0.70, 1.0)))

    # Jharokha Base Floor Platform
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, -0.90, 4.85))) @ Matrix.Diagonal((2.40, 1.00, 0.20, 1.0)))

    # Jharokha Screen Walls (Perforated Jaali lattice)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, -1.35, 5.45))) @ Matrix.Diagonal((2.30, 0.10, 1.00, 1.0)))
    for sx in [-1.15, 1.15]:
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((sx, -0.90, 5.45))) @ Matrix.Diagonal((0.10, 0.90, 1.00, 1.0)))

    # Jharokha Slender Timber Pillars (4 posts)
    for px in [-1.1, 1.1]:
        for py in [-0.5, -1.3]:
            create_cylinder_mesh(bm, radius=0.06, depth=1.60, segments=8, matrix=Matrix.Translation(Vector((px, py, 6.20))))

    # Jharokha Eave Canopy (Chhajja) & Ribbed Domelet
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, -0.90, 7.05))) @ Matrix.Diagonal((2.60, 1.20, 0.12, 1.0)))
    create_cylinder_mesh(bm, radius=0.90, depth=0.35, segments=12, matrix=Matrix.Translation(Vector((0.0, -0.90, 7.30))))

    # Floor 2 Horizontal Cornice Belt (Z = 8.0m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, -0.45, 8.0))) @ Matrix.Diagonal((8.20, 0.30, 0.25, 1.0)))

    # Floor 2 Main Wall (Z = 8.0 to 12.0m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 10.0))) @ Matrix.Diagonal((8.0, 0.80, 4.0, 1.0)))

    # Floor 2 Twin Arched Takhta Windows (X = -2.2 and +2.2, Z = 9.6m)
    for wx in [-2.2, 2.2]:
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((wx, -0.42, 9.60))) @ Matrix.Diagonal((1.30, 0.15, 1.80, 1.0)))
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((wx, -0.38, 9.60))) @ Matrix.Diagonal((1.10, 0.08, 1.60, 1.0)))
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((wx, -0.55, 10.60))) @ Matrix.Diagonal((1.50, 0.35, 0.10, 1.0)))

    # Roof Parapet & Decorative Cornice (Z = 12.0m to 13.1m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, -0.48, 12.05))) @ Matrix.Diagonal((8.30, 0.35, 0.30, 1.0)))
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, -0.35, 12.70))) @ Matrix.Diagonal((8.0, 0.30, 1.10, 1.0)))

    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(mat_lahori_brick())
    mesh.materials.append(mat_aged_teak())

    return obj


# =========================================================================
# 4. FLATBED LITHOGRAPHIC STONE PRINTING PRESS (SM_Prop_Litho_Press_Flatbed)
# =========================================================================
def build_litho_press_flatbed(name="SM_Prop_Litho_Press_Flatbed"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Dimensions: 2.2m length (along X), 1.3m depth (along Y), 1.25m height (along Z)
    # Heavy Cast-Iron Table Legs (4 corner legs)
    for lx in [-0.95, 0.95]:
        for ly in [-0.50, 0.50]:
            create_cylinder_mesh(bm, radius=0.07, depth=0.82, segments=10, matrix=Matrix.Translation(Vector((lx, ly, 0.41))))

    # Cast-Iron Bed Table Frame & Cross-braces
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 0.82))) @ Matrix.Diagonal((2.10, 1.20, 0.14, 1.0)))
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 0.28))) @ Matrix.Diagonal((1.90, 1.00, 0.08, 1.0)))

    # Sliding Press Bed Rails (along X)
    for ry in [-0.35, 0.35]:
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, ry, 0.92))) @ Matrix.Diagonal((2.00, 0.12, 0.08, 1.0)))

    # Bavarian Limestone Printing Slab (Stone Litho Block) in center
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((-0.10, 0.0, 0.98))) @ Matrix.Diagonal((0.95, 0.65, 0.10, 1.0)))

    # Upper Scraper / Pressure Bar Assembly (Z = 1.05 to 1.35m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((-0.10, 0.0, 1.22))) @ Matrix.Diagonal((0.22, 1.10, 0.28, 1.0)))
    # Steel pressure screw handle
    create_cylinder_mesh(bm, radius=0.03, depth=0.30, segments=8, matrix=Matrix.Translation(Vector((-0.10, 0.0, 1.45))))
    create_cylinder_mesh(bm, radius=0.02, depth=0.45, segments=8, matrix=Matrix.Translation(Vector((-0.10, 0.0, 1.58))) @ Matrix.Rotation(math.radians(90.0), 4, 'X'))

    # Large Geared Cast-Iron Flywheel on Side (X = +1.10m, Y = 0.0)
    create_cylinder_mesh(bm, radius=0.48, depth=0.06, segments=24, matrix=Matrix.Translation(Vector((1.12, 0.0, 0.88))) @ Matrix.Rotation(math.radians(90.0), 4, 'Y'))
    # 4 Spokes
    for sp in range(4):
        rot = math.radians(sp * 45.0)
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((1.12, 0.0, 0.88))) @ Matrix.Rotation(rot, 4, 'X') @ Matrix.Diagonal((0.04, 0.90, 0.05, 1.0)))
    # Turned Hardwood Turning Handle
    create_cylinder_mesh(bm, radius=0.03, depth=0.18, segments=8, matrix=Matrix.Translation(Vector((1.22, 0.36, 0.88))) @ Matrix.Rotation(math.radians(90.0), 4, 'Y'))

    # Inking Roller (Naward) on side shelf
    create_cylinder_mesh(bm, radius=0.05, depth=0.55, segments=12, matrix=Matrix.Translation(Vector((0.65, -0.40, 0.95))) @ Matrix.Rotation(math.radians(90.0), 4, 'Y'))
    # Terracotta Ink Pot
    create_cylinder_mesh(bm, radius=0.09, depth=0.16, segments=10, matrix=Matrix.Translation(Vector((0.65, 0.40, 0.96))))

    # Stacks of Printed Pamphlets on feed table
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((-0.72, 0.0, 0.94))) @ Matrix.Diagonal((0.44, 0.32, 0.12, 1.0)))

    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(mat_wrought_iron())
    mesh.materials.append(mat_limestone())
    mesh.materials.append(mat_aged_teak())
    mesh.materials.append(mat_clay())

    return obj


# =========================================================================
# 5. ROADSIDE DRINKING WATER CHHABEEL / PYAOO (SM_Mohalla_Pyaoo_Water_Shelter)
# =========================================================================
def build_mohalla_pyaoo_shelter(name="SM_Mohalla_Pyaoo_Water_Shelter"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Scale: 2.8m length (along X), 2.0m depth (along Y), 2.7m height (along Z)
    # Raised Stone Plinth Chabutra (Z = 0 to 0.40m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 0.20))) @ Matrix.Diagonal((2.80, 2.00, 0.40, 1.0)))

    # 4 Turned Timber Pillars
    for px in [-1.20, 1.20]:
        for py in [-0.80, 0.80]:
            create_cylinder_mesh(bm, radius=0.07, depth=1.80, segments=10, matrix=Matrix.Translation(Vector((px, py, 1.30))))
            # Pillar carved bracket capital
            bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((px, py, 2.24))) @ Matrix.Diagonal((0.26, 0.26, 0.12, 1.0)))

    # Timber Roof Tie Beams
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, -0.80, 2.30))) @ Matrix.Diagonal((2.70, 0.14, 0.14, 1.0)))
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.80, 2.30))) @ Matrix.Diagonal((2.70, 0.14, 0.14, 1.0)))
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((-1.20, 0.0, 2.30))) @ Matrix.Diagonal((0.14, 1.70, 0.14, 1.0)))
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((1.20, 0.0, 2.30))) @ Matrix.Diagonal((0.14, 1.70, 0.14, 1.0)))

    # Sloped Terracotta Tile Roof with Overhanging Chhajjas (Z = 2.35 to 2.80m)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 2.55))) @ Matrix.Diagonal((3.10, 2.30, 0.15, 1.0)))
    # Roof Ridge Hip
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 2.70))) @ Matrix.Diagonal((2.80, 0.25, 0.18, 1.0)))

    # Matka Stand Bench (Raised shelf along rear wall)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.40, 0.70))) @ Matrix.Diagonal((2.20, 0.55, 0.20, 1.0)))

    # 3 Large Terracotta Water Matkas / Gharas
    for i, mx in enumerate([-0.65, 0.0, 0.65]):
        # Hemp coiled ring (binnu)
        create_cylinder_mesh(bm, radius=0.20, depth=0.08, segments=12, matrix=Matrix.Translation(Vector((mx, 0.40, 0.84))))
        # Bulbous belly
        create_cylinder_mesh(bm, radius=0.24, depth=0.32, segments=14, matrix=Matrix.Translation(Vector((mx, 0.40, 1.04))))
        # Narrow neck & flared lip
        create_cylinder_mesh(bm, radius=0.12, depth=0.12, segments=12, matrix=Matrix.Translation(Vector((mx, 0.40, 1.24))))
        create_cylinder_mesh(bm, radius=0.16, depth=0.04, segments=12, matrix=Matrix.Translation(Vector((mx, 0.40, 1.30))))

    # Brass Drinking Lotas with chained tether
    for lx in [-0.30, 0.30]:
        create_cylinder_mesh(bm, radius=0.08, depth=0.14, segments=10, matrix=Matrix.Translation(Vector((lx, -0.20, 0.47))))

    # Front low stone sitting thara
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, -0.65, 0.45))) @ Matrix.Diagonal((2.00, 0.40, 0.12, 1.0)))

    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(mat_aged_teak())
    mesh.materials.append(mat_clay())
    mesh.materials.append(mat_brass())
    mesh.materials.append(mat_lahori_brick())

    return obj


# =========================================================================
# EXPORT PIPELINE
# =========================================================================
def export_asset_fbx(asset_name, fbx_filename):
    reset_scene()
    
    if asset_name == "SM_Wall_Town_Faseel_Rampart":
        target = build_town_faseel_rampart(asset_name)
    elif asset_name == "SM_Checkpoint_Picket_Sandbag_Barrier":
        target = build_checkpoint_picket_barrier(asset_name)
    elif asset_name == "SM_Haveli_Facade_3Story_Jharokha":
        target = build_haveli_facade_3story(asset_name)
    elif asset_name == "SM_Prop_Litho_Press_Flatbed":
        target = build_litho_press_flatbed(asset_name)
    elif asset_name == "SM_Mohalla_Pyaoo_Water_Shelter":
        target = build_mohalla_pyaoo_shelter(asset_name)
    else:
        raise ValueError(f"Unknown asset: {asset_name}")

    bpy.ops.object.select_all(action='DESELECT')
    target.select_set(True)
    bpy.context.view_layer.objects.active = target

    out_fbx = os.path.join(EXPORTS_DIR, fbx_filename)
    bpy.ops.export_scene.fbx(
        filepath=out_fbx,
        use_selection=True,
        global_scale=100.0,
        axis_forward='-Z',
        axis_up='Y',
        apply_unit_scale=True,
        bake_space_transform=True,
        mesh_smooth_type='FACE'
    )
    print(f"[EXPORT] Successfully saved: {out_fbx}")

def main():
    print("================ PROJECT REVOLUTION: TOWN STRUCTURE EXPANSION GENERATOR ================")
    
    assets = [
        ("SM_Wall_Town_Faseel_Rampart", "SM_Wall_Town_Faseel_Rampart.fbx"),
        ("SM_Checkpoint_Picket_Sandbag_Barrier", "SM_Checkpoint_Picket_Sandbag_Barrier.fbx"),
        ("SM_Haveli_Facade_3Story_Jharokha", "SM_Haveli_Facade_3Story_Jharokha.fbx"),
        ("SM_Prop_Litho_Press_Flatbed", "SM_Prop_Litho_Press_Flatbed.fbx"),
        ("SM_Mohalla_Pyaoo_Water_Shelter", "SM_Mohalla_Pyaoo_Water_Shelter.fbx"),
    ]

    for asset_name, fbx_name in assets:
        export_asset_fbx(asset_name, fbx_name)

    print("================ ALL TOWN STRUCTURE EXPANSION ASSETS EXPORTED SUCCESSFULLY ================")

if __name__ == "__main__":
    main()
