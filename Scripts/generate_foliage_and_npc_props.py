"""
PROJECT REVOLUTION — Historical Foliage & Civilian NPC Props Generator
Toolchain: Blender 5.2 LTS Headless Pipeline
Generates:
1. SM_Foliage_PeepalTree_Shrine (Ancient Sacred Peepal Tree with Brick Chabutra Shrine)
2. SM_Prop_Tulsi_Pedestal (Courtyard Holy Basil / Tulsi Chaura Brick Planter)
3. SM_Prop_Bhishti_Mashk (Traditional Punjabi Leather Goatskin Water Bag with Brass Spout)
4. SM_Prop_ClothRolls_Manchester (Bolts of Imported British Cotton & Swadeshi Khadi)
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

def mat_bark():
    return get_pbr_material("M_Bark_PBR", (0.28, 0.20, 0.14, 1.0), roughness=0.90, metallic=0.0)

def mat_foliage():
    return get_pbr_material("M_Foliage_PBR", (0.15, 0.38, 0.12, 1.0), roughness=0.60, metallic=0.0)

def mat_brick():
    return get_pbr_material("M_LahoriBrick_PBR", (0.58, 0.22, 0.14, 1.0), roughness=0.85, metallic=0.0)

def mat_clay():
    return get_pbr_material("M_Clay_PBR", (0.65, 0.35, 0.22, 1.0), roughness=0.85, metallic=0.0)

def mat_iron():
    return get_pbr_material("M_WroughtIron_PBR", (0.15, 0.15, 0.16, 1.0), roughness=0.65, metallic=0.85)

def mat_cloth_indigo():
    return get_pbr_material("M_ClothIndigo_PBR", (0.10, 0.18, 0.40, 1.0), roughness=0.85, metallic=0.0)

def mat_cloth_saffron():
    return get_pbr_material("M_ClothSaffron_PBR", (0.85, 0.45, 0.10, 1.0), roughness=0.85, metallic=0.0)


# =========================================================================
# 1. ANCIENT SACRED PEEPAL TREE WITH BRICK CHABUTRA SHRINE
# =========================================================================
def build_peepal_tree(name="SM_Foliage_PeepalTree_Shrine"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()

    # 1. Octagonal Lahori Brick Chabutra (Plinth) at Base
    # Diameter ~4.2m, height 0.65m
    num_sides = 12
    radius = 2.4
    height = 0.65
    
    verts_bottom = []
    verts_top = []
    for i in range(num_sides):
        ang = (2.0 * math.pi * i) / num_sides
        x = radius * math.cos(ang)
        y = radius * math.sin(ang)
        verts_bottom.append(bm.verts.new((x, y, 0.0)))
        verts_top.append(bm.verts.new((x * 0.95, y * 0.95, height)))

    # Step tier
    verts_step_bottom = []
    verts_step_top = []
    for i in range(num_sides):
        ang = (2.0 * math.pi * i) / num_sides
        x = (radius + 0.5) * math.cos(ang)
        y = (radius + 0.5) * math.sin(ang)
        verts_step_bottom.append(bm.verts.new((x, y, 0.0)))
        verts_step_top.append(bm.verts.new((x, y, height * 0.4)))

    # Faces for plinth sides
    for i in range(num_sides):
        next_i = (i + 1) % num_sides
        bm.faces.new([verts_bottom[i], verts_bottom[next_i], verts_top[next_i], verts_top[i]])
        bm.faces.new([verts_step_bottom[i], verts_step_bottom[next_i], verts_step_top[next_i], verts_step_top[i]])

    # Top surface of plinth
    bm.faces.new(verts_top)

    # 2. Gnarled Peepal Trunk (Z: 0.5m to 4.5m)
    trunk_levels = [
        (0.50, 0.85, 0.0, 0.0),
        (1.50, 0.75, 0.08, -0.05),
        (2.80, 0.65, -0.10, 0.12),
        (4.20, 0.55, 0.05, 0.15)
    ]
    
    level_verts = []
    for z, r, ox, oy in trunk_levels:
        ring = []
        for i in range(8):
            ang = (2.0 * math.pi * i) / 8
            # Organic asymmetry
            r_var = r * (1.0 + 0.12 * math.sin(ang * 3))
            x = ox + r_var * math.cos(ang)
            y = oy + r_var * math.sin(ang)
            ring.append(bm.verts.new((x, y, z)))
        level_verts.append(ring)

    for l in range(len(trunk_levels) - 1):
        for i in range(8):
            next_i = (i + 1) % 8
            bm.faces.new([level_verts[l][i], level_verts[l][next_i], level_verts[l+1][next_i], level_verts[l+1][i]])

    # 3. Main Sprawling Branches
    branches = [
        # (Start z, direction vector, length, radius)
        (4.0, Vector((1.8, 0.4, 1.2)), 2.8, 0.28),
        (4.2, Vector((-1.6, 1.2, 1.0)), 2.6, 0.26),
        (4.1, Vector((-0.5, -1.8, 1.1)), 2.5, 0.25),
        (4.3, Vector((0.8, -1.4, 1.3)), 2.4, 0.24)
    ]

    canopy_centers = []
    for b_z, b_dir, b_len, b_rad in branches:
        b_norm = b_dir.normalized()
        tip_pos = Vector((0.0, 0.0, b_z)) + b_norm * b_len
        canopy_centers.append(tip_pos)

        # Cylindrical branch segment
        b_cube = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((b_rad * 2, b_rad * 2, b_len, 1.0)))
        # Orient along branch direction
        mid_pos = Vector((0.0, 0.0, b_z)) + b_norm * (b_len * 0.5)
        for v in b_cube['verts']:
            v.co += mid_pos

    # 4. Sprawling Peepal Foliage Canopy Clusters (Spherical / Cloud Masses)
    for c_pos in canopy_centers:
        for offset in [Vector((0, 0, 0.4)), Vector((0.6, 0.4, 0.1)), Vector((-0.5, -0.4, 0.2))]:
            ico = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=1.6)
            for v in ico['verts']:
                # Irregular foliage silhouette
                disp = 0.2 * math.sin(v.co.x * 3) + 0.15 * math.cos(v.co.y * 3)
                v.co = v.co * (1.0 + disp) + c_pos + offset

    # Central crowning canopy
    ico_top = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=2.2)
    for v in ico_top['verts']:
        v.co.z *= 0.75
        v.co += Vector((0.0, 0.0, 5.8))

    # 5. Small Earthen Diya Lamps placed on Chabutra ledge
    for da in [0.4, 1.8, 3.2, 4.6]:
        dx = (radius * 0.88) * math.cos(da)
        dy = (radius * 0.88) * math.sin(da)
        diya = bmesh.ops.create_cone(bm, segments=6, radius1=0.08, radius2=0.03, depth=0.04)
        for v in diya['verts']:
            v.co += Vector((dx, dy, height + 0.02))

    bm.to_mesh(mesh)
    bm.free()

    obj.data.materials.append(mat_bark())
    obj.data.materials.append(mat_foliage())
    obj.data.materials.append(mat_brick())
    obj.data.materials.append(mat_clay())

    return obj


# =========================================================================
# 2. COURTYARD TULSI PLANTER PEDESTAL (TULSI CHAURA)
# =========================================================================
def build_tulsi_pedestal(name="SM_Prop_Tulsi_Pedestal"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()

    # 1. Base Stepped Plinth (0.8m x 0.8m x 0.2m)
    p_base = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.80, 0.80, 0.20, 1.0)))
    for v in p_base['verts']:
        v.co.z += 0.10

    # 2. Carved Pedestal Body (0.60m x 0.60m x 0.65m)
    p_body = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.60, 0.60, 0.65, 1.0)))
    for v in p_body['verts']:
        v.co.z += 0.525

    # 3. Flared Upper Cornice & Soil Basin
    p_cornice = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.72, 0.72, 0.15, 1.0)))
    for v in p_cornice['verts']:
        v.co.z += 0.925

    # 4. Lush Sacred Holy Basil (Tulsi) Plant Bush
    # Multiple leafy icosphere clusters emerging from soil
    t_center = Vector((0.0, 0.0, 1.0))
    for t_off in [
        Vector((0.0, 0.0, 0.25)),
        Vector((0.15, 0.12, 0.18)),
        Vector((-0.14, 0.15, 0.16)),
        Vector((0.12, -0.15, 0.15)),
        Vector((-0.15, -0.12, 0.17))
    ]:
        bush = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.22)
        for v in bush['verts']:
            v.co += t_center + t_off

    # Small Diya on the ledge
    diya = bmesh.ops.create_cone(bm, segments=6, radius1=0.06, radius2=0.02, depth=0.03)
    for v in diya['verts']:
        v.co += Vector((0.30, 0.0, 0.86))

    bm.to_mesh(mesh)
    bm.free()

    obj.data.materials.append(mat_brick())
    obj.data.materials.append(mat_foliage())
    obj.data.materials.append(mat_clay())

    return obj


# =========================================================================
# 3. BHISHTI LEATHER WATER BAG (MASHK)
# =========================================================================
def build_bhishti_mashk(name="SM_Prop_Bhishti_Mashk"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()

    # Leather goatskin water bag body: elongated swollen pouch
    # Width ~0.45m, length ~0.85m, height ~0.35m
    mashk_body = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.38)
    for v in mashk_body['verts']:
        v.co.x *= 1.35   # Length
        v.co.y *= 0.85   # Width
        v.co.z *= 0.70   # Thickness
        # Droop downwards slightly from water weight
        if v.co.z < 0:
            v.co.z *= 1.25
        v.co.z += 0.35

    # Tapered neck with brass nozzle at the front (+X)
    neck = bmesh.ops.create_cone(bm, segments=8, radius1=0.08, radius2=0.04, depth=0.22)
    for v in neck['verts']:
        # Rotate to point along +X
        old_x, old_z = v.co.x, v.co.z
        v.co.x = old_z
        v.co.z = -old_x
        v.co.x += 0.60
        v.co.z += 0.35

    # Brass nozzle ring
    nozzle = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.04, 0.07, 0.07, 1.0)))
    for v in nozzle['verts']:
        v.co.x += 0.72
        v.co.z += 0.35

    # Heavy leather shoulder strap looping across top
    strap = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.80, 0.05, 0.02, 1.0)))
    for v in strap['verts']:
        v.co.z += 0.65

    bm.to_mesh(mesh)
    bm.free()

    obj.data.materials.append(mat_clay())   # Leather tone
    obj.data.materials.append(mat_iron())   # Brass nozzle & fittings

    return obj


# =========================================================================
# 4. CLOTH ROLLS & BOLTS (MANCHESTER & SWADESHI KHADI)
# =========================================================================
def build_cloth_rolls(name="SM_Prop_ClothRolls_Manchester"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()

    # Stack of 5 rolled fabric bolts (length 1.1m, diameter 0.22m)
    # Layer 1 (Bottom 3 rolls)
    y_coords = [-0.25, 0.0, 0.25]
    for y in y_coords:
        roll = bmesh.ops.create_cone(bm, segments=12, radius1=0.11, radius2=0.11, depth=1.1)
        for v in roll['verts']:
            # Align cylinder along X axis
            old_x, old_z = v.co.x, v.co.z
            v.co.x = old_z
            v.co.z = -old_x
            v.co.y += y
            v.co.z += 0.12

    # Layer 2 (Middle 2 rolls)
    for y in [-0.13, 0.13]:
        roll = bmesh.ops.create_cone(bm, segments=12, radius1=0.11, radius2=0.11, depth=1.1)
        for v in roll['verts']:
            old_x, old_z = v.co.x, v.co.z
            v.co.x = old_z
            v.co.z = -old_x
            v.co.y += y
            v.co.z += 0.31

    # Layer 3 (Top 1 roll of Swadeshi hand-spun Khadi)
    roll_top = bmesh.ops.create_cone(bm, segments=12, radius1=0.11, radius2=0.11, depth=1.1)
    for v in roll_top['verts']:
        old_x, old_z = v.co.x, v.co.z
        v.co.x = old_z
        v.co.z = -old_x
        v.co.z += 0.50

    # Folded rectangular Manchester cotton cloths
    for fx, fz in [(-0.35, 0.15), (0.35, 0.15)]:
        folded = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.30, 0.55, 0.06, 1.0)))
        for v in folded['verts']:
            v.co.x += fx
            v.co.z += 0.58

    bm.to_mesh(mesh)
    bm.free()

    obj.data.materials.append(mat_cloth_indigo())
    obj.data.materials.append(mat_cloth_saffron())

    return obj


# =========================================================================
# EXPORT ALL ASSETS
# =========================================================================
def run_generation():
    print("[BLENDER] Starting Historical Foliage & Civilian NPC Props Generation...")
    
    generators = [
        (build_peepal_tree, "SM_Foliage_PeepalTree_Shrine"),
        (build_tulsi_pedestal, "SM_Prop_Tulsi_Pedestal"),
        (build_bhishti_mashk, "SM_Prop_Bhishti_Mashk"),
        (build_cloth_rolls, "SM_Prop_ClothRolls_Manchester")
    ]

    for gen_func, asset_name in generators:
        reset_scene()
        obj = gen_func(asset_name)

        # Center origin
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

    print("[BLENDER] All historical foliage and NPC prop assets successfully generated!")

if __name__ == "__main__":
    run_generation()
