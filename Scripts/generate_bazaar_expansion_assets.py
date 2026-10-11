"""
PROJECT REVOLUTION — 3D Asset Generator & Bazaar Expansion Builder
Toolchain: Blender 5.2 LTS Headless Pipeline
Generates modular architectural slabs, communal well, market stalls, spice baskets, and shopfront elements.
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
    """Retrieves or creates a standardized PBR Principled BSDF material in the active scene."""
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

def mat_plaster():
    return get_pbr_material("M_LimePlaster_PBR", (0.82, 0.78, 0.70, 1.0), roughness=0.90, metallic=0.0)

def mat_iron():
    return get_pbr_material("M_WroughtIron_PBR", (0.12, 0.12, 0.13, 1.0), roughness=0.65, metallic=0.85)

def mat_jute():
    return get_pbr_material("M_JuteRope_PBR", (0.65, 0.52, 0.35, 1.0), roughness=0.92, metallic=0.0)

def mat_clay():
    return get_pbr_material("M_Terracotta_PBR", (0.68, 0.36, 0.20, 1.0), roughness=0.88, metallic=0.0)

# --- 1. FLOOR & CEILING MODULAR SLAB (4m x 4m x 0.25m) ---
def build_floor_slab(name="SM_Floor_Ceiling_Slab_4x4m"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()
    # Create solid 4m x 4m x 0.25m box with top surface at Z = 0.0
    slab = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((4.0, 4.0, 0.25, 1.0)))
    for v in slab['verts']:
        v.co.z -= 0.125  # top is at Z = 0.0, bottom is at Z = -0.25

    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(mat_brick())
    mesh.materials.append(mat_plaster())
    return obj

# --- 2. COMMUNAL STONE WELL & CHOPAL (Mohalla Well) ---
def build_mohalla_well(name="SM_Mohalla_Well_Stone"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()
    
    # 1. Circular Stepped Plinth Base (Apron)
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=24,
        radius1=2.6,
        radius2=2.6,
        depth=0.20,
        matrix=Matrix.Translation((0, 0, 0.10))
    )
    
    # 2. Outer Octagonal Stone Cylinder Well Wall
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=8,
        radius1=1.5,
        radius2=1.5,
        depth=1.0,
        matrix=Matrix.Translation((0, 0, 0.70))
    )
    
    # 3. Inner Hollow Cylinder (Interior well shaft)
    # Coping rim detail
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=16,
        radius1=1.6,
        radius2=1.6,
        depth=0.15,
        matrix=Matrix.Translation((0, 0, 1.15))
    )

    # 4. Timber Upright Posts (Left and Right)
    lp = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.18, 0.18, 2.6, 1.0)))
    for v in lp['verts']:
        v.co.x -= 1.35
        v.co.z += 1.30

    rp = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.18, 0.18, 2.6, 1.0)))
    for v in rp['verts']:
        v.co.x += 1.35
        v.co.z += 1.30

    # 5. Timber Crossbeam
    cb = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((3.0, 0.20, 0.20, 1.0)))
    for v in cb['verts']:
        v.co.z += 2.50

    # 6. Iron Pulley Wheel and Axle
    axle = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.6, 0.06, 0.06, 1.0)))
    for v in axle['verts']:
        v.co.z += 2.25

    pulley = bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=16,
        radius1=0.25,
        radius2=0.25,
        depth=0.08,
        matrix=Matrix.Rotation(math.radians(90.0), 4, 'Y') @ Matrix.Translation((0, 0, 2.25))
    )

    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(mat_brick())
    mesh.materials.append(mat_teak())
    mesh.materials.append(mat_iron())
    return obj

# --- 3. BAZAAR MARKET STALL & AWNING ---
def build_market_stall(name="SM_Market_Stall_Wood_Awning"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()

    # 4 Timber Corner Posts
    post_coords = [(-1.5, -0.9), (1.5, -0.9), (-1.5, 0.9), (1.5, 0.9)]
    for px, py in post_coords:
        p = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.12, 0.12, 2.5, 1.0)))
        for v in p['verts']:
            v.co.x += px
            v.co.y += py
            v.co.z += 1.25

    # Raised Display Counter / Bench
    bench = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((3.1, 1.6, 0.75, 1.0)))
    for v in bench['verts']:
        v.co.z += 0.375

    bench_top = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((3.3, 1.8, 0.08, 1.0)))
    for v in bench_top['verts']:
        v.co.z += 0.79

    # Sloped Awning Canopy Frame
    rafter_l = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.10, 2.2, 0.10, 1.0)))
    for v in rafter_l['verts']:
        v.co.x -= 1.5
        v.co.z += 2.45
        v.co.y *= 1.0
        v.co.z += v.co.y * 0.15  # slight slope

    rafter_r = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.10, 2.2, 0.10, 1.0)))
    for v in rafter_r['verts']:
        v.co.x += 1.5
        v.co.z += 2.45
        v.co.z += v.co.y * 0.15

    # Canopy Cloth / Awning Slab
    canopy = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((3.4, 2.3, 0.06, 1.0)))
    for v in canopy['verts']:
        v.co.z += 2.52
        v.co.z += v.co.y * 0.15

    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(mat_teak())
    mesh.materials.append(mat_jute())
    mesh.materials.append(mat_clay())
    return obj

# --- 4. WOVEN SPICE & GRAIN BASKET (Tokri) ---
def build_spice_basket(name="SM_Prop_SpiceBasket_Woven"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()

    # Outer tapered woven cane basket
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=18,
        radius1=0.25,
        radius2=0.35,
        depth=0.28,
        matrix=Matrix.Translation((0, 0, 0.14))
    )

    # Rounded mounded spice heap inside basket
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=18,
        radius1=0.34,
        radius2=0.08,
        depth=0.14,
        matrix=Matrix.Translation((0, 0, 0.28))
    )

    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(mat_jute())
    mesh.materials.append(mat_clay())
    return obj

# --- 5. HANGING WOODEN MERCHANT SHOP SIGN ---
def build_shop_sign(name="SM_Prop_ShopSign_Wood"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()

    # Wooden signboard plaque
    plaque = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((1.6, 0.08, 0.55, 1.0)))
    for v in plaque['verts']:
        v.co.z += 0.275

    # Decorative wooden border
    border = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((1.7, 0.10, 0.65, 1.0)))
    for v in border['verts']:
        v.co.z += 0.275

    # Wrought iron mounting brackets
    mb_l = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.06, 0.14, 0.40, 1.0)))
    for v in mb_l['verts']:
        v.co.x -= 0.65
        v.co.z += 0.70

    mb_r = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.06, 0.14, 0.40, 1.0)))
    for v in mb_r['verts']:
        v.co.x += 0.65
        v.co.z += 0.70

    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(mat_teak())
    mesh.materials.append(mat_iron())
    return obj

# --- 6. TEAK FOLDING SHOP SHUTTER (Takhtas) ---
def build_shop_shutter(name="SM_Shop_Shutter_Foldable"):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()

    # Main wooden shutter plank wall
    shutter = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((3.6, 0.12, 2.5, 1.0)))
    for v in shutter['verts']:
        v.co.z += 1.25

    # Horizontal iron locking bars (Top, Mid, Bottom)
    for bz in [0.4, 1.25, 2.1]:
        bar = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((3.7, 0.16, 0.08, 1.0)))
        for v in bar['verts']:
            v.co.z += bz

    # Center heavy iron hasp & padlock loop
    hasp = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.25, 0.22, 0.18, 1.0)))
    for v in hasp['verts']:
        v.co.z += 1.25

    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(mat_teak())
    mesh.materials.append(mat_iron())
    return obj

def export_expansion_assets():
    reset_scene()
    print("=== GENERATING BAZAAR & MOHALLA EXPANSION ASSETS ===")

    builders = [
        ("SM_Floor_Ceiling_Slab_4x4m", build_floor_slab),
        ("SM_Mohalla_Well_Stone", build_mohalla_well),
        ("SM_Market_Stall_Wood_Awning", build_market_stall),
        ("SM_Prop_SpiceBasket_Woven", build_spice_basket),
        ("SM_Prop_ShopSign_Wood", build_shop_sign),
        ("SM_Shop_Shutter_Foldable", build_shop_shutter),
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

    print("=== BAZAAR EXPANSION ASSET EXPORT COMPLETE ===")

if __name__ == "__main__":
    export_expansion_assets()
