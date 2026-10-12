"""
PROJECT REVOLUTION — Master Architectural Structures Generator
Toolchain: Blender 5.2 LTS Headless Pipeline
Generates 5 high-quality, authentic architectural environment structures for 1919 Punjab:
1. SM_Arch_Overhead_Kucha (Overhead flying multi-foil brick arch with timber tie-beam Teh-Bandi)
2. SM_Arch_Monumental_Chowk_Gate (Double-height monumental town gate with octagonal bastions)
3. SM_Street_Lamp_Post_Victorian (Cast-iron municipal lamppost with ladder crossbar & hexagonal lantern)
4. SM_Bazaar_Canopy_Khadi_Awning (Timber-frame draped khadi cloth bazaar street awning)
5. SM_Street_Drain_Stone_Gutter (Carved stone street gutter curb with flagstone crossings)
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


# =========================================================================
# 1. OVERHEAD FLYING KUCHA ARCHWAY WITH TIMBER TIE-BEAM (TEH-BANDI)
# =========================================================================
def build_overhead_kucha_arch(name="SM_Arch_Overhead_Kucha"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Spans a 6.0m street, 2.4m tall arch structure, 0.6m deep along Y
    # Left and Right Wall Abutments / Piers (X = -3.0 to -2.3, and X = 2.3 to 3.0)
    for sign in [-1, 1]:
        pier = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.70, 0.60, 2.40, 1.0)))
        for v in pier['verts']:
            v.co.x += sign * 2.65
            v.co.z += 1.20

        # Carved stone corbel / console brackets below beam
        corbel = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.35, 0.62, 0.35, 1.0)))
        for v in corbel['verts']:
            v.co.x += sign * 2.15
            v.co.z += 0.30

    # Multi-foil / cusped arch span across the street
    # Upper solid brick lintel / parapet band (spans from -3.0 to +3.0 at Z = 1.8 to 2.4)
    lintel = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((6.00, 0.55, 0.60, 1.0)))
    for v in lintel['verts']:
        v.co.z += 2.10

    # Projecting decorative terracotta tile cornice / eaves
    cornice = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((6.20, 0.70, 0.12, 1.0)))
    for v in cornice['verts']:
        v.co.z += 2.46

    # Cusped arch vault segments (approximated by 5 segmental arched brick voussoirs)
    arch_pts = [
        (-2.2, 0.50), (-1.6, 1.15), (-0.8, 1.55), (0.0, 1.70),
        (0.8, 1.55), (1.6, 1.15), (2.2, 0.50)
    ]
    for i in range(len(arch_pts) - 1):
        x1, z1 = arch_pts[i]
        x2, z2 = arch_pts[i+1]
        mid_x = (x1 + x2) * 0.5
        mid_z = (z1 + z2) * 0.5
        length = math.hypot(x2 - x1, z2 - z1)
        angle = math.atan2(z2 - z1, x2 - x1)
        
        seg = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((length, 0.56, 0.30, 1.0)))
        for v in seg['verts']:
            # rotate by angle
            vx = v.co.x * math.cos(angle) - v.co.z * math.sin(angle)
            vz = v.co.x * math.sin(angle) + v.co.z * math.cos(angle)
            v.co.x = vx + mid_x
            v.co.z = vz + mid_z

    # Heavy Shisham Hardwood Tie-Beam (Teh-Bandi) spanning horizontally at Z = 0.40m
    beam = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((5.40, 0.22, 0.24, 1.0)))
    for v in beam['verts']:
        v.co.z += 0.38

    # Wrought iron anchor plates and tie-rods at beam ends
    for sign in [-1, 1]:
        plate = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.08, 0.34, 0.34, 1.0)))
        for v in plate['verts']:
            v.co.x += sign * 2.70
            v.co.z += 0.38

    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(mat_lahori_brick())
    mesh.materials.append(mat_aged_teak())
    mesh.materials.append(mat_wrought_iron())

    return obj


# =========================================================================
# 2. MONUMENTAL TOWN CHOWK GATE (DARWAZA)
# =========================================================================
def build_monumental_chowk_gate(name="SM_Arch_Monumental_Chowk_Gate"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Total dimensions: 7.0m wide x 1.4m deep x 6.5m tall
    # Central arch opening: 4.2m wide x 4.6m tall
    # Left & Right Octagonal Guard Bastions / Pilasters (X = -3.0 and X = +3.0)
    for sign in [-1, 1]:
        bastion = bmesh.ops.create_cone(bm, segments=8, radius1=0.75, radius2=0.70, depth=6.20)
        for v in bastion['verts']:
            v.co.x += sign * 3.00
            v.co.z += 3.10

        # Domed cupola / chhatri cap on bastion top
        cap = bmesh.ops.create_cone(bm, segments=8, radius1=0.82, radius2=0.10, depth=0.80)
        for v in cap['verts']:
            v.co.x += sign * 3.00
            v.co.z += 6.20 + 0.40

    # Side Wall Massing flanking the portal
    for sign in [-1, 1]:
        side_wall = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((1.10, 1.20, 5.00, 1.0)))
        for v in side_wall['verts']:
            v.co.x += sign * 2.30
            v.co.z += 2.50

    # Arch Spandrels and Upper Story Mass (X = -2.4 to +2.4, Z = 4.0 to 6.2)
    upper_wall = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((5.20, 1.20, 1.80, 1.0)))
    for v in upper_wall['verts']:
        v.co.z += 5.10

    # Central Pointed Arch Portal Ring
    arch_pts = [
        (-2.1, 2.4), (-1.6, 3.6), (-0.9, 4.4), (0.0, 4.75),
        (0.9, 4.4), (1.6, 3.6), (2.1, 2.4)
    ]
    for i in range(len(arch_pts) - 1):
        x1, z1 = arch_pts[i]
        x2, z2 = arch_pts[i+1]
        mid_x = (x1 + x2) * 0.5
        mid_z = (z1 + z2) * 0.5
        length = math.hypot(x2 - x1, z2 - z1)
        angle = math.atan2(z2 - z1, x2 - x1)
        
        seg = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((length, 1.25, 0.45, 1.0)))
        for v in seg['verts']:
            vx = v.co.x * math.cos(angle) - v.co.z * math.sin(angle)
            vz = v.co.x * math.sin(angle) + v.co.z * math.cos(angle)
            v.co.x = vx + mid_x
            v.co.z = vz + mid_z

    # Kangura Battlements along gateway roofline (decorative notched merlons)
    for bx in [-2.0, -1.2, -0.4, 0.4, 1.2, 2.0]:
        merlon = bmesh.ops.create_cone(bm, segments=4, radius1=0.25, radius2=0.08, depth=0.45)
        for v in merlon['verts']:
            v.co.x += bx
            v.co.z += 6.00 + 0.225

    # Upper Jharokha inspection niche facing front (+Y)
    jharokha = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((1.20, 0.40, 1.10, 1.0)))
    for v in jharokha['verts']:
        v.co.y += 0.70
        v.co.z += 5.20

    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(mat_lahori_brick())
    mesh.materials.append(mat_aged_teak())
    mesh.materials.append(mat_wrought_iron())

    return obj


# =========================================================================
# 3. COLONIAL VICTORIAN CAST-IRON STREET LAMP POST
# =========================================================================
def build_street_lamp_post(name="SM_Street_Lamp_Post_Victorian"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Total height: 3.4m tall
    # Stepped octagonal cast-iron base plinth (50cm wide x 45cm tall)
    base1 = bmesh.ops.create_cone(bm, segments=8, radius1=0.25, radius2=0.22, depth=0.25)
    for v in base1['verts']:
        v.co.z += 0.125

    base2 = bmesh.ops.create_cone(bm, segments=8, radius1=0.22, radius2=0.14, depth=0.20)
    for v in base2['verts']:
        v.co.z += 0.25 + 0.10

    # Fluted tapered cast-iron column (12cm to 7cm diameter, 2.2m tall)
    col = bmesh.ops.create_cone(bm, segments=12, radius1=0.07, radius2=0.045, depth=2.20)
    for v in col['verts']:
        v.co.z += 0.45 + 1.10

    # Middle decorative collar ring
    ring = bmesh.ops.create_cone(bm, segments=12, radius1=0.09, radius2=0.09, depth=0.08)
    for v in ring['verts']:
        v.co.z += 1.65

    # Horizontal ladder-rest crossbar (60cm wide x 3cm diameter at Z = 2.45m)
    crossbar = bmesh.ops.create_cone(bm, segments=6, radius1=0.015, radius2=0.015, depth=0.60)
    for v in crossbar['verts']:
        # rotate along X axis
        vx = v.co.x
        v.co.x = v.co.z
        v.co.z = vx + 2.45

    # Ornate scroll brackets supporting lantern cradle
    for sign in [-1, 1]:
        bracket = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.15, 0.03, 0.22, 1.0)))
        for v in bracket['verts']:
            v.co.x += sign * 0.10
            v.co.z += 2.60

    # Lantern base collar
    l_base = bmesh.ops.create_cone(bm, segments=6, radius1=0.14, radius2=0.18, depth=0.08)
    for v in l_base['verts']:
        v.co.z += 2.70

    # Hexagonal flared glass/copper lantern cage (55cm tall x 36cm wide at top)
    cage = bmesh.ops.create_cone(bm, segments=6, radius1=0.18, radius2=0.12, depth=0.48)
    for v in cage['verts']:
        v.co.z += 2.74 + 0.24

    # Domed brass ventilator cap and smoke chimney
    dome = bmesh.ops.create_cone(bm, segments=6, radius1=0.14, radius2=0.03, depth=0.16)
    for v in dome['verts']:
        v.co.z += 3.22 + 0.08

    # Acorn finial knob at very top
    finial = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.03)
    for v in finial['verts']:
        v.co.z += 3.40

    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(mat_wrought_iron())
    mesh.materials.append(mat_brass())
    mesh.materials.append(mat_clay())

    return obj


# =========================================================================
# 4. BAZAAR KHADI AWNING & CANOPY FRAME
# =========================================================================
def build_bazaar_khadi_awning(name="SM_Bazaar_Canopy_Khadi_Awning"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # 4.4m wide along X, 2.8m deep along Y, 2.6m tall
    # 2 Front timber support posts (at Y = -1.4m, X = -2.1m and +2.1m)
    for sign in [-1, 1]:
        post = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.10, 0.10, 2.40, 1.0)))
        for v in post['verts']:
            v.co.x += sign * 2.10
            v.co.y -= 1.35
            v.co.z += 1.20

    # Front horizontal timber beam connecting posts
    front_beam = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((4.40, 0.12, 0.12, 1.0)))
    for v in front_beam['verts']:
        v.co.y -= 1.35
        v.co.z += 2.35

    # Back wall ledger beam (at Y = 1.35m, Z = 2.80m)
    back_beam = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((4.40, 0.12, 0.12, 1.0)))
    for v in back_beam['verts']:
        v.co.y += 1.35
        v.co.z += 2.80

    # 4 Sloped bamboo cross rafters spanning from back to front
    for rx in [-2.1, -0.7, 0.7, 2.1]:
        rafter = bmesh.ops.create_cone(bm, segments=6, radius1=0.035, radius2=0.035, depth=2.85)
        for v in rafter['verts']:
            vy = v.co.y
            vz = v.co.z
            v.co.x += rx
            v.co.y = vz
            # slope: 2.80 at Y = 1.35 down to 2.35 at Y = -1.35
            v.co.z = 2.575 + (vy * 0.16)

    # Draped Canvas / Khadi Fabric Sheet (with natural catenary sag in middle)
    # Formed by 4 longitudinal fabric panels
    fabric_grid_x = [-2.15, -1.07, 0.0, 1.07, 2.15]
    fabric_grid_y = [-1.45, -0.70, 0.0, 0.70, 1.40]

    # Create cloth surface
    cloth_verts = []
    for fy in fabric_grid_y:
        row = []
        for fx in fabric_grid_x:
            # Base slope from Y=-1.45 (Z=2.30) to Y=1.40 (Z=2.82)
            t = (fy + 1.45) / 2.85
            base_z = 2.30 + (t * 0.52)
            # Catenary dip in center (max 14cm sag)
            sag = math.sin((1.0 - abs(fx) / 2.15) * math.pi * 0.5) * math.sin(t * math.pi) * 0.12
            v = bm.verts.new((fx, fy, base_z - sag))
            row.append(v)
        cloth_verts.append(row)

    for r in range(len(cloth_verts) - 1):
        for c in range(len(cloth_verts[0]) - 1):
            v1 = cloth_verts[r][c]
            v2 = cloth_verts[r][c+1]
            v3 = cloth_verts[r+1][c+1]
            v4 = cloth_verts[r+1][c]
            bm.faces.new([v1, v2, v3, v4])

    # Hanging scalloped front valance (draping down from front beam at Y = -1.45)
    for vx in [-1.6, -0.8, 0.0, 0.8, 1.6]:
        fringe = bmesh.ops.create_cone(bm, segments=4, radius1=0.25, radius2=0.02, depth=0.28)
        for v in fringe['verts']:
            v.co.x += vx
            v.co.y -= 1.44
            v.co.z += 2.18

    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(mat_aged_teak())
    mesh.materials.append(mat_cloth_indigo())
    mesh.materials.append(mat_jute())

    return obj


# =========================================================================
# 5. STREET DRAINAGE GUTTER & STONE FLAGSTONES
# =========================================================================
def build_street_drain_stone_gutter(name="SM_Street_Drain_Stone_Gutter"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # 4.0m long module (along Y), 60cm wide (along X), 22cm tall
    # Raised street curb edge stone (20cm wide x 22cm tall along Y)
    curb = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.20, 4.00, 0.22, 1.0)))
    for v in curb['verts']:
        v.co.x -= 0.20
        v.co.z += 0.11

    # Recessed drain trough base slab (26cm wide x 6cm thick at Z = 0.03m)
    trough = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.26, 4.00, 0.06, 1.0)))
    for v in trough['verts']:
        v.co.x += 0.03
        v.co.z += 0.03

    # Building threshold footing stone (14cm wide x 18cm tall along Y)
    footing = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.14, 4.00, 0.18, 1.0)))
    for v in footing['verts']:
        v.co.x += 0.23
        v.co.z += 0.09

    # Two carved stone crossing bridge flagstones (Patra) spanning the drain
    for py in [-1.20, 1.20]:
        bridge = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.36, 0.55, 0.08, 1.0)))
        for v in bridge['verts']:
            v.co.x += 0.02
            v.co.y += py
            v.co.z += 0.18

    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(mat_lahori_brick())
    mesh.materials.append(mat_clay())

    return obj


# =========================================================================
# EXPORT PIPELINE
# =========================================================================
def export_asset_fbx(asset_name, fbx_filename):
    reset_scene()
    
    if asset_name == "SM_Arch_Overhead_Kucha":
        target = build_overhead_kucha_arch(asset_name)
    elif asset_name == "SM_Arch_Monumental_Chowk_Gate":
        target = build_monumental_chowk_gate(asset_name)
    elif asset_name == "SM_Street_Lamp_Post_Victorian":
        target = build_street_lamp_post(asset_name)
    elif asset_name == "SM_Bazaar_Canopy_Khadi_Awning":
        target = build_bazaar_khadi_awning(asset_name)
    elif asset_name == "SM_Street_Drain_Stone_Gutter":
        target = build_street_drain_stone_gutter(asset_name)
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
    print("================ PROJECT REVOLUTION: ARCHITECTURAL STRUCTURES GENERATOR ================")
    
    assets = [
        ("SM_Arch_Overhead_Kucha", "SM_Arch_Overhead_Kucha.fbx"),
        ("SM_Arch_Monumental_Chowk_Gate", "SM_Arch_Monumental_Chowk_Gate.fbx"),
        ("SM_Street_Lamp_Post_Victorian", "SM_Street_Lamp_Post_Victorian.fbx"),
        ("SM_Bazaar_Canopy_Khadi_Awning", "SM_Bazaar_Canopy_Khadi_Awning.fbx"),
        ("SM_Street_Drain_Stone_Gutter", "SM_Street_Drain_Stone_Gutter.fbx"),
    ]

    for asset_name, fbx_name in assets:
        export_asset_fbx(asset_name, fbx_name)

    print("================ ALL ARCHITECTURAL STRUCTURES EXPORTED SUCCESSFULLY ================")

if __name__ == "__main__":
    main()
