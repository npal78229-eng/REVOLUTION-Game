"""
PROJECT REVOLUTION — Storytelling Realism Assets Pack 2 Generator
Toolchain: Blender 5.2 LTS Headless Pipeline
Generates 5 period-authentic historical 3D models for April 1919 Punjab:
1. SM_Prop_Imperial_Postbox_GR (Colonial British cast-iron pillar letter box with collection plate)
2. SM_Prop_Bazaar_Tarazu_Scale (Mandi merchant balance scale with brass pans & iron weights)
3. SM_Prop_Rooftop_Patang_Charkhi (Basant fighter kites with glass manja thread on wooden spool)
4. SM_Prop_Haveli_Grain_Sandook (Traditional Punjabi carved timber dowry & grain chest)
5. SM_Prop_School_Wall_Map_Easel (Classroom timber easel with 1919 Punjab map & pointer stick)
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

def mat_pillar_red():
    # Imperial postal red lacquer over cast iron
    return get_pbr_material("M_ImperialRed_PBR", (0.68, 0.12, 0.10, 1.0), roughness=0.45, metallic=0.25)


# =========================================================================
# 1. COLONIAL BRITISH IMPERIAL PILLAR POSTBOX (GEORGE V ROYAL CYPHER)
# =========================================================================
def build_imperial_postbox(name="SM_Prop_Imperial_Postbox_GR"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Octagonal stepped cast-iron base ring (60cm wide, 12cm tall)
    base = bmesh.ops.create_cone(bm, segments=8, radius1=0.30, radius2=0.27, depth=0.12)
    for v in base['verts']:
        v.co.z += 0.06

    # Main cylindrical postbox column (46cm diameter, 110cm tall)
    body = bmesh.ops.create_cone(bm, segments=16, radius1=0.23, radius2=0.23, depth=1.10)
    for v in body['verts']:
        v.co.z += 0.12 + 0.55

    # Molded collar trim below dome
    collar = bmesh.ops.create_cone(bm, segments=16, radius1=0.26, radius2=0.25, depth=0.06)
    for v in collar['verts']:
        v.co.z += 1.22 + 0.03

    # Domed fluted top cap
    cap = bmesh.ops.create_cone(bm, segments=16, radius1=0.25, radius2=0.06, depth=0.18)
    for v in cap['verts']:
        v.co.z += 1.28 + 0.09

    # Finial acorn knob at top
    finial = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.05)
    for v in finial['verts']:
        v.co.z += 1.46 + 0.04

    # Letter posting aperture hood (jutting outward on front face +Y)
    hood = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.26, 0.08, 0.07, 1.0)))
    for v in hood['verts']:
        v.co.y += 0.22
        v.co.z += 1.08

    # Letter drop slit cutout inside hood
    slit = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.18, 0.02, 0.02, 1.0)))
    for v in slit['verts']:
        v.co.y += 0.23
        v.co.z += 1.07

    # Brass collection times plate & George V Royal Cypher plate (front lower)
    plate = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.20, 0.015, 0.28, 1.0)))
    for v in plate['verts']:
        v.co.y += 0.235
        v.co.z += 0.72

    # Hinged collection door seam surround
    door = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.24, 0.01, 0.52, 1.0)))
    for v in door['verts']:
        v.co.y += 0.228
        v.co.z += 0.62

    # Boycott notice pasted on the side of the postbox (-X flank)
    pamphlet = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.008, 0.16, 0.24, 1.0)))
    for v in pamphlet['verts']:
        v.co.x -= 0.235
        v.co.y += 0.02
        v.co.z += 0.82

    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(mat_pillar_red())
    mesh.materials.append(mat_wrought_iron())
    mesh.materials.append(mat_brass())
    mesh.materials.append(mat_paper())

    return obj


# =========================================================================
# 2. BAZAAR MANDI BALANCE SCALE (TARAZU) WITH WEIGHTS
# =========================================================================
def build_bazaar_tarazu_scale(name="SM_Prop_Bazaar_Tarazu_Scale"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Wooden merchant display tray base (60cm x 35cm x 4cm)
    base = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.60, 0.35, 0.04, 1.0)))
    for v in base['verts']:
        v.co.z += 0.02

    # Upright timber tripod / support post (65cm tall x 4cm x 4cm)
    post = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.04, 0.04, 0.65, 1.0)))
    for v in post['verts']:
        v.co.z += 0.04 + 0.325

    # Top suspension arm / fulcrum hook
    hook = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.05, 0.08, 0.04, 1.0)))
    for v in hook['verts']:
        v.co.z += 0.69

    # Central iron balance beam (52cm long horizontal crossbar with center ring)
    beam = bmesh.ops.create_cone(bm, segments=8, radius1=0.008, radius2=0.008, depth=0.52)
    for v in beam['verts']:
        # rotate along X axis to make it horizontal along X
        vx = v.co.x
        vy = v.co.y
        vz = v.co.z
        v.co.x = vz
        v.co.y = vy
        v.co.z = vx + 0.62

    # Center pointer needle (vertical indicator 12cm tall)
    needle = bmesh.ops.create_cone(bm, segments=6, radius1=0.004, radius2=0.001, depth=0.12)
    for v in needle['verts']:
        v.co.z += 0.68

    # Left & Right suspension cords / chains and brass pans
    for side, offset_x in [(-1, -0.24), (1, 0.24)]:
        # 3 angled support chains from beam end down to pan
        for chain_angle in [0.0, 2.094, 4.188]:
            cx = math.cos(chain_angle) * 0.09
            cy = math.sin(chain_angle) * 0.09
            chain = bmesh.ops.create_cone(bm, segments=4, radius1=0.002, radius2=0.002, depth=0.34)
            for v in chain['verts']:
                v.co.x += offset_x + (cx * 0.5)
                v.co.y += cy * 0.5
                v.co.z += 0.44

        # Concave brass weighing pan (20cm diameter)
        pan = bmesh.ops.create_cone(bm, segments=16, radius1=0.10, radius2=0.08, depth=0.02)
        for v in pan['verts']:
            v.co.x += offset_x
            v.co.z += 0.27

    # Cast-iron counterweights (Baat) sitting in a row on the wooden base: 1kg, 500g, 200g, 100g, 50g
    weights = [
        (0.038, 0.045, 0.00),    # 1 kg
        (0.030, 0.038, 0.08),    # 500 g
        (0.024, 0.030, 0.15),    # 200 g
        (0.018, 0.024, 0.20),    # 100 g
        (0.014, 0.018, 0.24),    # 50 g
    ]
    for radius, height, pos_x in weights:
        wt = bmesh.ops.create_cone(bm, segments=8, radius1=radius, radius2=radius*0.85, depth=height)
        for v in wt['verts']:
            v.co.x += pos_x - 0.12
            v.co.y -= 0.10
            v.co.z += 0.04 + (height * 0.5)
        # Ring knob on top of weight
        knob = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=radius*0.35)
        for v in knob['verts']:
            v.co.x += pos_x - 0.12
            v.co.y -= 0.10
            v.co.z += 0.04 + height + (radius * 0.3)

    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(mat_aged_teak())
    mesh.materials.append(mat_wrought_iron())
    mesh.materials.append(mat_brass())

    return obj


# =========================================================================
# 3. ROOFTOP BASANT FIGHTER KITES (PATANG) & SPOOL (CHARKHI)
# =========================================================================
def build_rooftop_patang_charkhi(name="SM_Prop_Rooftop_Patang_Charkhi"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # KITE 1: Resting on rooftop floor, tilted slightly (44cm diamond sail)
    # Diamond sail created from four triangular vertices
    kite1_rot = 0.25 # slight tilt
    kite1_pts = [
        (0.0, 0.22, 0.02),    # Top point
        (0.20, 0.0, 0.02),    # Right corner
        (0.0, -0.22, 0.02),   # Bottom tail point
        (-0.20, 0.0, 0.02),   # Left corner
    ]
    k_verts = [bm.verts.new(p) for p in kite1_pts]
    bm.faces.new(k_verts)

    # Bamboo spine spar (straight vertical stick)
    spine = bmesh.ops.create_cone(bm, segments=4, radius1=0.003, radius2=0.003, depth=0.44)
    for v in spine['verts']:
        v.co.z += 0.022

    # Bamboo curved bow spar (curved cross spar)
    bow = bmesh.ops.create_cone(bm, segments=4, radius1=0.0025, radius2=0.0025, depth=0.42)
    for v in bow['verts']:
        vx = v.co.x
        v.co.x = v.co.z
        v.co.z = 0.024
        # arc curvature
        v.co.y += (1.0 - (abs(v.co.x) / 0.22)) * 0.05

    # Triangular paper tail tassel at bottom
    tail_pts = [
        (-0.04, -0.22, 0.02),
        (0.04, -0.22, 0.02),
        (0.0, -0.29, 0.02)
    ]
    t_verts = [bm.verts.new(tp) for tp in tail_pts]
    bm.faces.new(t_verts)

    # KITE 2: Second kite stacked offset underneath
    kite2_pts = [
        (0.08, 0.20, 0.008),
        (0.27, -0.02, 0.008),
        (0.08, -0.24, 0.008),
        (-0.11, -0.02, 0.008),
    ]
    k2_verts = [bm.verts.new(p) for p in kite2_pts]
    bm.faces.new(k2_verts)

    # TRADITIONAL PUNJABI HARDWOOD CHARKHI (KITE LINE SPOOL)
    # Central axle spindle (32cm long hardwood cylinder with end handles)
    charkhi_center_x = 0.32
    charkhi_center_y = 0.10
    spindle = bmesh.ops.create_cone(bm, segments=8, radius1=0.014, radius2=0.014, depth=0.32)
    for v in spindle['verts']:
        vx = v.co.x
        v.co.x = v.co.z + charkhi_center_x
        v.co.y += charkhi_center_y
        v.co.z = 0.09

    # Two 6-spoke wooden end-wheels (18cm diameter)
    for end_x in [charkhi_center_x - 0.09, charkhi_center_x + 0.09]:
        wheel_rim = bmesh.ops.create_cone(bm, segments=12, radius1=0.09, radius2=0.09, depth=0.012)
        for v in wheel_rim['verts']:
            vy = v.co.y
            vz = v.co.z
            v.co.x += end_x
            v.co.y = vy + charkhi_center_y
            v.co.z = vz + 0.09

    # Spool wound with bright glass-coated manja line (cylinder between wheels)
    manja = bmesh.ops.create_cone(bm, segments=12, radius1=0.065, radius2=0.065, depth=0.16)
    for v in manja['verts']:
        v.co.x = v.co.z + charkhi_center_x
        v.co.y += charkhi_center_y
        v.co.z = 0.09

    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(mat_paper())
    mesh.materials.append(mat_aged_teak())
    mesh.materials.append(mat_brass())

    return obj


# =========================================================================
# 4. TRADITIONAL PUNJABI CARVED TIMBER GRAIN & DOWRY CHEST (SANDOOK)
# =========================================================================
def build_haveli_grain_sandook(name="SM_Prop_Haveli_Grain_Sandook"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Main solid hardwood chest body (110cm wide x 58cm deep x 62cm tall)
    body = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((1.10, 0.58, 0.58, 1.0)))
    for v in body['verts']:
        v.co.z += 0.16 + 0.29

    # 4 Carved corner legs / stilt posts elevating chest off damp floor (12cm x 12cm x 16cm)
    for lx in [-0.50, 0.50]:
        for ly in [-0.24, 0.24]:
            leg = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.12, 0.12, 0.16, 1.0)))
            for v in leg['verts']:
                v.co.x += lx
                v.co.y += ly
                v.co.z += 0.08
            # Carved foot detail
            foot = bmesh.ops.create_cone(bm, segments=8, radius1=0.06, radius2=0.04, depth=0.05)
            for v in foot['verts']:
                v.co.x += lx
                v.co.y += ly
                v.co.z += 0.025

    # Hinged top lid with overhang rim (114cm x 62cm x 6cm)
    lid = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((1.14, 0.62, 0.06, 1.0)))
    for v in lid['verts']:
        v.co.z += 0.74 + 0.03

    # Wrought iron decorative corner reinforcing brackets (8 brackets on corners)
    for bx in [-0.55, 0.55]:
        for bz in [0.20, 0.68]:
            bracket = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.04, 0.10, 0.10, 1.0)))
            for v in bracket['verts']:
                v.co.x += bx
                v.co.y += 0.27
                v.co.z += bz

    # Front brass hasp latch and padlock (Kundi & Tala)
    hasp = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.08, 0.025, 0.16, 1.0)))
    for v in hasp['verts']:
        v.co.y += 0.295
        v.co.z += 0.66

    lock = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.06, 0.02, 0.08, 1.0)))
    for v in lock['verts']:
        v.co.y += 0.305
        v.co.z += 0.58

    # Side heavy wrought-iron drop handles
    for sx in [-0.555, 0.555]:
        handle = bmesh.ops.create_cone(bm, segments=6, radius1=0.01, radius2=0.01, depth=0.18)
        for v in handle['verts']:
            v.co.x += sx
            v.co.z += 0.46

    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(mat_aged_teak())
    mesh.materials.append(mat_wrought_iron())
    mesh.materials.append(mat_brass())

    return obj


# =========================================================================
# 5. CLASSROOM PUNJAB 1919 MAP EASEL & POINTER STICK
# =========================================================================
def build_school_map_easel(name="SM_Prop_School_Wall_Map_Easel"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Three-legged wooden classroom easel (155cm tall)
    # Front-left and front-right legs (angled outward and back)
    for leg_sign in [-1, 1]:
        fleg = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.04, 0.04, 1.55, 1.0)))
        for v in fleg['verts']:
            v.co.x += leg_sign * 0.28
            v.co.y += 0.08
            v.co.z += 0.775

    # Back support leg (angled backward)
    bleg = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.04, 0.04, 1.52, 1.0)))
    for v in bleg['verts']:
        v.co.y -= 0.38
        v.co.z += 0.76

    # Horizontal wooden support shelf (crossbar at 75cm height)
    shelf = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.85, 0.08, 0.04, 1.0)))
    for v in shelf['verts']:
        v.co.y += 0.10
        v.co.z += 0.75

    # Upper horizontal stabilizer bar
    upper_bar = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.55, 0.04, 0.03, 1.0)))
    for v in upper_bar['verts']:
        v.co.y += 0.08
        v.co.z += 1.35

    # Framed historical map board (82cm wide x 62cm tall x 3cm thick)
    map_board = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.82, 0.03, 0.62, 1.0)))
    for v in map_board['verts']:
        v.co.y += 0.11
        v.co.z += 1.08

    # Teacher's wooden pointer stick (Chhari) leaning against front leg
    stick = bmesh.ops.create_cone(bm, segments=6, radius1=0.008, radius2=0.003, depth=0.88)
    for v in stick['verts']:
        v.co.x += 0.32
        v.co.y += 0.14
        v.co.z += 0.44

    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(mat_aged_teak())
    mesh.materials.append(mat_paper())
    mesh.materials.append(mat_brass())

    return obj


# =========================================================================
# EXPORT PIPELINE
# =========================================================================
def export_asset_fbx(asset_name, fbx_filename):
    reset_scene()
    
    # Re-build target mesh in clean scene
    name = asset_name
    if name == "SM_Prop_Imperial_Postbox_GR":
        target = build_imperial_postbox(name)
    elif name == "SM_Prop_Bazaar_Tarazu_Scale":
        target = build_bazaar_tarazu_scale(name)
    elif name == "SM_Prop_Rooftop_Patang_Charkhi":
        target = build_rooftop_patang_charkhi(name)
    elif name == "SM_Prop_Haveli_Grain_Sandook":
        target = build_haveli_grain_sandook(name)
    elif name == "SM_Prop_School_Wall_Map_Easel":
        target = build_school_map_easel(name)
    else:
        raise ValueError(f"Unknown asset: {name}")

    bpy.ops.object.select_all(action='DESELECT')
    target.select_set(True)
    bpy.context.view_layer.objects.active = target

    out_fbx = os.path.join(EXPORTS_DIR, fbx_filename)
    bpy.ops.export_scene.fbx(
        filepath=out_fbx,
        use_selection=True,
        global_scale=100.0,  # Blender meters to Unreal centimeters (1m = 100cm)
        axis_forward='-Z',
        axis_up='Y',
        apply_unit_scale=True,
        bake_space_transform=True,
        mesh_smooth_type='FACE'
    )
    print(f"[EXPORT] Successfully saved: {out_fbx}")

def main():
    print("================ PROJECT REVOLUTION: BLENDER ASSET PACK 2 GENERATOR ================")
    
    assets = [
        ("SM_Prop_Imperial_Postbox_GR", "SM_Prop_Imperial_Postbox_GR.fbx"),
        ("SM_Prop_Bazaar_Tarazu_Scale", "SM_Prop_Bazaar_Tarazu_Scale.fbx"),
        ("SM_Prop_Rooftop_Patang_Charkhi", "SM_Prop_Rooftop_Patang_Charkhi.fbx"),
        ("SM_Prop_Haveli_Grain_Sandook", "SM_Prop_Haveli_Grain_Sandook.fbx"),
        ("SM_Prop_School_Wall_Map_Easel", "SM_Prop_School_Wall_Map_Easel.fbx"),
    ]

    for asset_name, fbx_name in assets:
        export_asset_fbx(asset_name, fbx_name)

    print("================ ALL PACK 2 ASSETS GENERATED & EXPORTED SUCCESSFULLY ================")

if __name__ == "__main__":
    main()
