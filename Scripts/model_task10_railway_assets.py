"""
PROJECT REVOLUTION (क्रांति) — Task 10: Railway Junction & Colonial Civil Lines Assets
Authors 4 monumental 3D assets for Layer 4 Northern Boundary in Blender 5.2 LTS:
1. SM_Railway_Tracks_Ballast_Bed_4m (Indian broad-gauge 5ft 6in steel rails, creosote sleepers & stone ballast)
2. SM_Railway_Brick_Overpass_Arch (Monumental colonial brick arch overpass separating mohallas from Civil Lines)
3. SM_Colonial_Railway_Signal_Gantry (6.5m lattice iron semaphore tower with signal arm & ladder)
4. SM_Civil_Lines_Club_Perimeter_Railing (Cast-iron spearhead security palisade with brick pilasters)

Dual-exports to Art/Exports, Art/PROJECT, and C:/Users/npal7/PROJECT/PROJECT/
"""

import bpy
import bmesh
import math
import os
import shutil
from mathutils import Vector, Matrix

print("[TASK10_RAILWAY] Starting 3D Railway & Civil Lines Assets Generation in Blender 5.2 LTS...")

export_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Exports"
art_project_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\PROJECT"
ext_project_dir = r"C:\Users\npal7\PROJECT\PROJECT"

os.makedirs(export_dir, exist_ok=True)
os.makedirs(art_project_dir, exist_ok=True)
os.makedirs(ext_project_dir, exist_ok=True)

def reset_scene():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for mesh in list(bpy.data.meshes):
        bpy.data.meshes.remove(mesh, do_unlink=True)

def get_or_create_mat(name, color, roughness=0.7, metallic=0.0):
    mat = bpy.data.materials.get(name)
    if not mat:
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if bsdf:
            if "Base Color" in bsdf.inputs:
                bsdf.inputs["Base Color"].default_value = color
            if "Roughness" in bsdf.inputs:
                bsdf.inputs["Roughness"].default_value = roughness
            if "Metallic" in bsdf.inputs:
                bsdf.inputs["Metallic"].default_value = metallic
    return mat

def export_asset(name, obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    b1 = os.path.join(art_project_dir, f"{name}.blend")
    b2 = os.path.join(ext_project_dir, f"{name}.blend")
    bpy.ops.wm.save_as_mainfile(filepath=b1)
    shutil.copyfile(b1, b2)
    
    f1 = os.path.join(export_dir, f"{name}.fbx")
    f2 = os.path.join(art_project_dir, f"{name}.fbx")
    f3 = os.path.join(ext_project_dir, f"{name}.fbx")
    
    bpy.ops.export_scene.fbx(
        filepath=f1,
        use_selection=True,
        global_scale=100.0,
        axis_forward='-Z',
        axis_up='Y',
        apply_unit_scale=True,
        bake_space_transform=True,
        mesh_smooth_type='FACE',
        add_leaf_bones=False
    )
    shutil.copyfile(f1, f2)
    shutil.copyfile(f1, f3)
    print(f"[TASK10_RAILWAY] Exported {name} successfully to all destinations.")

# ===========================================================================
# 1. SM_Railway_Tracks_Ballast_Bed_4m
# 4.0m modular Indian broad-gauge (1.676m gauge) railway tracks with ballast
# ===========================================================================
def build_railway_tracks():
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Railway_Tracks_Ballast_Bed_4m_Mesh")
    obj = bpy.data.objects.new("SM_Railway_Tracks_Ballast_Bed_4m", mesh)
    bpy.context.collection.objects.link(obj)
    
    obj.data.materials.append(get_or_create_mat("M_DirtRoad_PBR", (0.35, 0.32, 0.28, 1.0), roughness=0.95)) # Gravel ballast
    obj.data.materials.append(get_or_create_mat("M_AgedTeak_PBR", (0.18, 0.12, 0.08, 1.0), roughness=0.85)) # Creosote sleepers
    obj.data.materials.append(get_or_create_mat("M_WroughtIron_PBR", (0.20, 0.22, 0.24, 1.0), roughness=0.38, metallic=0.92)) # Steel rails
    
    bm = bmesh.new()
    
    # 1. Stone Ballast Embankment (Trapezoidal prism: 4.0m long Y, 2.8m bottom width, 2.3m top width, 0.30m height)
    bmesh.ops.create_cube(
        bm, size=1.0,
        matrix=Matrix.Translation(Vector((0, 0, 0.12))) @ Matrix.Diagonal((2.6, 4.0, 0.24, 1.0))
    )
    bm.faces.ensure_lookup_table()
    for f in bm.faces:
        f.material_index = 0 # Ballast
        
    # 2. Six Timber Sleepers (width 0.25m, length 2.4m, thickness 0.14m, spaced along Y)
    sleeper_y_coords = [-1.5, -0.9, -0.3, 0.3, 0.9, 1.5]
    for sy in sleeper_y_coords:
        bmesh.ops.create_cube(
            bm, size=1.0,
            matrix=Matrix.Translation(Vector((0, sy, 0.28))) @ Matrix.Diagonal((2.35, 0.24, 0.14, 1.0))
        )
    bm.faces.ensure_lookup_table()
    for f in bm.faces:
        if f.calc_center_median().z > 0.22 and abs(f.calc_center_median().x) < 1.25:
            f.material_index = 1 # Teak sleeper
            
    # 3. Dual Broad-Gauge Steel Rails (Gauge: 1.676m -> x = ±0.838m, height 0.16m)
    for sign in [-1, 1]:
        rx = sign * 0.838
        # Rail base foot (width 0.14m, thickness 0.03m)
        bmesh.ops.create_cube(
            bm, size=1.0,
            matrix=Matrix.Translation(Vector((rx, 0, 0.36))) @ Matrix.Diagonal((0.14, 4.0, 0.03, 1.0))
        )
        # Rail vertical web (width 0.04m, height 0.10m)
        bmesh.ops.create_cube(
            bm, size=1.0,
            matrix=Matrix.Translation(Vector((rx, 0, 0.42))) @ Matrix.Diagonal((0.04, 4.0, 0.10, 1.0))
        )
        # Rail crown head (width 0.08m, height 0.05m)
        bmesh.ops.create_cube(
            bm, size=1.0,
            matrix=Matrix.Translation(Vector((rx, 0, 0.49))) @ Matrix.Diagonal((0.08, 4.0, 0.05, 1.0))
        )
    
    bm.faces.ensure_lookup_table()
    for f in bm.faces:
        if f.calc_center_median().z > 0.34:
            f.material_index = 2 # Steel rail
        f.smooth = True
        
    bm.to_mesh(mesh)
    bm.free()
    export_asset("SM_Railway_Tracks_Ballast_Bed_4m", obj)

# ===========================================================================
# 2. SM_Railway_Brick_Overpass_Arch
# Monumental 8.0m span, 5.0m clearance colonial arched railway bridge
# ===========================================================================
def build_railway_overpass():
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Railway_Brick_Overpass_Arch_Mesh")
    obj = bpy.data.objects.new("SM_Railway_Brick_Overpass_Arch", mesh)
    bpy.context.collection.objects.link(obj)
    
    obj.data.materials.append(get_or_create_mat("M_LahoriBrick_PBR", (0.58, 0.25, 0.14, 1.0), roughness=0.88)) # Brick
    obj.data.materials.append(get_or_create_mat("M_WroughtIron_PBR", (0.16, 0.18, 0.20, 1.0), roughness=0.55, metallic=0.85)) # Iron railing
    
    bm = bmesh.new()
    
    # Left & Right Solid Brick Abutment Piers (width 2.2m, depth 4.0m, height 5.2m)
    for sign in [-1, 1]:
        px = sign * 5.1
        bmesh.ops.create_cube(
            bm, size=1.0,
            matrix=Matrix.Translation(Vector((px, 0, 2.6))) @ Matrix.Diagonal((2.2, 4.0, 5.2, 1.0))
        )
        # Chamfered stone plinth footing
        bmesh.ops.create_cube(
            bm, size=1.0,
            matrix=Matrix.Translation(Vector((px, 0, 0.3))) @ Matrix.Diagonal((2.5, 4.3, 0.6, 1.0))
        )
        
    # Semi-Circular Arch Ring Vault (Span: 8.0m, inner radius 4.0m, outer radius 4.8m, depth 4.0m)
    num_arch_segs = 16
    for i in range(num_arch_segs):
        a1 = math.pi * i / num_arch_segs
        a2 = math.pi * (i + 1) / num_arch_segs
        # Segment mid angle
        amid = (a1 + a2) * 0.5
        ax = 4.4 * math.cos(amid)
        az = 4.4 * math.sin(amid) + 0.6 # Springing line at 0.6m
        w = 0.85
        th = 0.55
        rot_ang = amid - (math.pi * 0.5)
        bmesh.ops.create_cube(
            bm, size=1.0,
            matrix=Matrix.Translation(Vector((ax, 0, az))) @ Matrix.Rotation(-rot_ang, 4, 'Y') @ Matrix.Diagonal((w, 4.0, th, 1.0))
        )
        
    # Roadway Deck Slab across top (width 12.4m, depth 4.2m, thickness 0.6m at Z = 5.3m)
    bmesh.ops.create_cube(
        bm, size=1.0,
        matrix=Matrix.Translation(Vector((0, 0, 5.3))) @ Matrix.Diagonal((12.4, 4.2, 0.6, 1.0))
    )
    
    # Bridge Parapet Safety Walls (height 1.1m, thickness 0.35m at Y = ±2.0m)
    for sign in [-1, 1]:
        py = sign * 2.0
        bmesh.ops.create_cube(
            bm, size=1.0,
            matrix=Matrix.Translation(Vector((0, py, 6.1))) @ Matrix.Diagonal((12.4, 0.35, 1.1, 1.0))
        )
        # Stone coping rim on parapet
        bmesh.ops.create_cube(
            bm, size=1.0,
            matrix=Matrix.Translation(Vector((0, py, 6.7))) @ Matrix.Diagonal((12.6, 0.45, 0.14, 1.0))
        )
        
    # Cast Iron Victorian Lamp Brackets on Parapets
    for sign in [-1, 1]:
        bmesh.ops.create_cone(
            bm, cap_ends=True, segments=10, radius1=0.06, radius2=0.04, depth=1.4,
            matrix=Matrix.Translation(Vector((sign * 3.5, 2.1, 7.3)))
        )
        bmesh.ops.create_cone(
            bm, cap_ends=True, segments=10, radius1=0.06, radius2=0.04, depth=1.4,
            matrix=Matrix.Translation(Vector((sign * 3.5, -2.1, 7.3)))
        )
        
    bm.faces.ensure_lookup_table()
    for f in bm.faces:
        if f.calc_center_median().z > 6.8:
            f.material_index = 1 # Iron lamp posts
        else:
            f.material_index = 0 # Brick
        f.smooth = True
        
    bm.to_mesh(mesh)
    bm.free()
    export_asset("SM_Railway_Brick_Overpass_Arch", obj)

# ===========================================================================
# 3. SM_Colonial_Railway_Signal_Gantry
# 6.5m lattice iron semaphore railway signal tower with ladder and arms
# ===========================================================================
def build_signal_gantry():
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Colonial_Railway_Signal_Gantry_Mesh")
    obj = bpy.data.objects.new("SM_Colonial_Railway_Signal_Gantry", mesh)
    bpy.context.collection.objects.link(obj)
    
    obj.data.materials.append(get_or_create_mat("M_WroughtIron_PBR", (0.18, 0.20, 0.22, 1.0), roughness=0.45, metallic=0.90))
    obj.data.materials.append(get_or_create_mat("M_ClothSaffron_PBR", (0.85, 0.15, 0.12, 1.0), roughness=0.60)) # Red semaphore arm
    
    bm = bmesh.new()
    
    # Base Concrete/Masonry Plinth (1.4m x 1.4m x 0.4m)
    bmesh.ops.create_cube(
        bm, size=1.0,
        matrix=Matrix.Translation(Vector((0, 0, 0.2))) @ Matrix.Diagonal((1.4, 1.4, 0.4, 1.0))
    )
    
    # 4 Lattice Angle-Iron Uprights (tapering from 1.0m base to 0.6m top at Z = 6.0m)
    for sx in [-1, 1]:
        for sy in [-1, 1]:
            bmesh.ops.create_cone(
                bm, cap_ends=True, segments=6, radius1=0.05, radius2=0.035, depth=5.8,
                matrix=Matrix.Translation(Vector((sx * 0.42, sy * 0.42, 3.2)))
            )
            
    # Horizontal Lattice Bracing Rings (at Z = 1.4m, 2.6m, 3.8m, 5.0m)
    for bz in [1.4, 2.6, 3.8, 5.0]:
        bmesh.ops.create_cube(
            bm, size=1.0,
            matrix=Matrix.Translation(Vector((0, 0, bz))) @ Matrix.Diagonal((0.85, 0.85, 0.06, 1.0))
        )
        
    # Maintenance Platform Gallery at Z = 5.2m (1.5m x 1.5m with safety railing)
    bmesh.ops.create_cube(
        bm, size=1.0,
        matrix=Matrix.Translation(Vector((0, 0, 5.2))) @ Matrix.Diagonal((1.4, 1.4, 0.08, 1.0))
    )
    # Railing around gallery
    for sx in [-0.65, 0.65]:
        bmesh.ops.create_cube(
            bm, size=1.0,
            matrix=Matrix.Translation(Vector((sx, 0, 5.7))) @ Matrix.Diagonal((0.05, 1.4, 0.9, 1.0))
        )
        bmesh.ops.create_cube(
            bm, size=1.0,
            matrix=Matrix.Translation(Vector((0, sx, 5.7))) @ Matrix.Diagonal((1.4, 0.05, 0.9, 1.0))
        )
        
    # Vertical Signal Mast extending from Z = 5.2m to 7.2m
    bmesh.ops.create_cone(
        bm, cap_ends=True, segments=10, radius1=0.07, radius2=0.05, depth=2.0,
        matrix=Matrix.Translation(Vector((0, 0, 6.2)))
    )
    
    # Semaphore Signal Arm (1.4m length horizontal bar at Z = 6.6m)
    bmesh.ops.create_cube(
        bm, size=1.0,
        matrix=Matrix.Translation(Vector((0.70, 0, 6.6))) @ Matrix.Diagonal((1.3, 0.04, 0.22, 1.0))
    )
    # Circular spectacle red/green lens frame
    bmesh.ops.create_cone(
        bm, cap_ends=True, segments=12, radius1=0.14, radius2=0.14, depth=0.05,
        matrix=Matrix.Translation(Vector((0.08, 0, 6.6))) @ Matrix.Rotation(math.radians(90.0), 4, 'X')
    )
    
    # Maintenance Ladder along back (+Y side)
    for lz in range(12):
        step_z = 0.5 + lz * 0.42
        bmesh.ops.create_cone(
            bm, cap_ends=True, segments=6, radius1=0.018, radius2=0.018, depth=0.45,
            matrix=Matrix.Translation(Vector((0, 0.45, step_z))) @ Matrix.Rotation(math.radians(90.0), 4, 'Y')
        )
        
    bm.faces.ensure_lookup_table()
    for f in bm.faces:
        c = f.calc_center_median()
        if c.z > 6.4 and c.x > 0.2:
            f.material_index = 1 # Red signal blade
        else:
            f.material_index = 0 # Wrought iron
        f.smooth = True
        
    bm.to_mesh(mesh)
    bm.free()
    export_asset("SM_Colonial_Railway_Signal_Gantry", obj)

# ===========================================================================
# 4. SM_Civil_Lines_Club_Perimeter_Railing
# 4.0m cast-iron spearhead security railing with Lahori brick pilasters
# ===========================================================================
def build_perimeter_railing():
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Civil_Lines_Club_Perimeter_Railing_Mesh")
    obj = bpy.data.objects.new("SM_Civil_Lines_Club_Perimeter_Railing", mesh)
    bpy.context.collection.objects.link(obj)
    
    obj.data.materials.append(get_or_create_mat("M_LahoriBrick_PBR", (0.58, 0.25, 0.14, 1.0), roughness=0.88))
    obj.data.materials.append(get_or_create_mat("M_WroughtIron_PBR", (0.16, 0.18, 0.20, 1.0), roughness=0.45, metallic=0.92))
    
    bm = bmesh.new()
    
    # Twin End Brick Pilasters (0.55m x 0.55m, height 2.2m at X = ±2.0m)
    for sx in [-2.0, 2.0]:
        bmesh.ops.create_cube(
            bm, size=1.0,
            matrix=Matrix.Translation(Vector((sx, 0, 1.05))) @ Matrix.Diagonal((0.55, 0.55, 2.1, 1.0))
        )
        # Pyramidal stone capstone
        bmesh.ops.create_cone(
            bm, cap_ends=True, segments=4, radius1=0.42, radius2=0.04, depth=0.35,
            matrix=Matrix.Translation(Vector((sx, 0, 2.25))) @ Matrix.Rotation(math.radians(45.0), 4, 'Z')
        )
        
    # Low Masonry Curb Wall between pilasters (length 3.5m, width 0.35m, height 0.45m)
    bmesh.ops.create_cube(
        bm, size=1.0,
        matrix=Matrix.Translation(Vector((0, 0, 0.22))) @ Matrix.Diagonal((3.5, 0.35, 0.45, 1.0))
    )
    
    bm.faces.ensure_lookup_table()
    for f in bm.faces:
        f.material_index = 0 # Brick
        
    # Twin Horizontal Iron Runner Bars (at Z = 0.65m and Z = 1.75m)
    for rz in [0.65, 1.75]:
        bmesh.ops.create_cube(
            bm, size=1.0,
            matrix=Matrix.Translation(Vector((0, 0, rz))) @ Matrix.Diagonal((3.5, 0.05, 0.04, 1.0))
        )
        
    # 18 Vertical Spearhead Iron Pickets (spaced along X: -1.6m to +1.6m)
    num_pickets = 18
    for i in range(num_pickets):
        px = -1.6 + (3.2 * i / (num_pickets - 1))
        # Vertical shaft
        bmesh.ops.create_cube(
            bm, size=1.0,
            matrix=Matrix.Translation(Vector((px, 0, 1.2))) @ Matrix.Diagonal((0.035, 0.035, 1.4, 1.0))
        )
        # Spearhead finial top at Z = 1.95m
        bmesh.ops.create_cone(
            bm, cap_ends=True, segments=4, radius1=0.035, radius2=0.005, depth=0.18,
            matrix=Matrix.Translation(Vector((px, 0, 1.98))) @ Matrix.Rotation(math.radians(45.0), 4, 'Z')
        )
        
    bm.faces.ensure_lookup_table()
    for f in bm.faces:
        if f.calc_center_median().z > 0.48 and abs(f.calc_center_median().x) < 1.72:
            f.material_index = 1 # Wrought iron
        f.smooth = True
        
    bm.to_mesh(mesh)
    bm.free()
    export_asset("SM_Civil_Lines_Club_Perimeter_Railing", obj)

# Run All 4 Builders
build_railway_tracks()
build_railway_overpass()
build_signal_gantry()
build_perimeter_railing()

print("[TASK10_RAILWAY] COMPLETE SUCCESS! All 4 railway and civil lines assets generated and dual-exported.")
