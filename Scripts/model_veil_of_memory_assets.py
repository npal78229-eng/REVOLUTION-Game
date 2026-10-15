"""
PROJECT REVOLUTION (क्रांति) — Veil of Memory & Memorial Storytelling 3D Assets
Authors 4 solemn, historically respectful period assets for the April 1919 Memorial Sector:
1. SM_Memorial_Historic_Well_Brick (Historic hexagonal Lahori brick well with timber pulley gallows & iron axle)
2. SM_Prop_Overturned_Brass_Lota (Traditional Punjabi brass water vessel resting on its side)
3. SM_Prop_Abandoned_Paper_Kite (Diamond bamboo-and-paper patang kite caught on iron wall bracket)
4. SM_Prop_Wooden_Takhti_Slate (Traditional school wooden takhti slate with carved handle & inkpot)

Dual-exports to Art/Exports, Art/PROJECT, and C:/Users/npal7/PROJECT/PROJECT/
"""

import bpy
import bmesh
import math
import os
import shutil
from mathutils import Vector, Matrix

print("[VEIL_OF_MEMORY] Starting 3D Memorial Assets Generation in Blender 5.2 LTS...")

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
    
    # Save blend files
    b1 = os.path.join(art_project_dir, f"{name}.blend")
    b2 = os.path.join(ext_project_dir, f"{name}.blend")
    bpy.ops.wm.save_as_mainfile(filepath=b1)
    shutil.copyfile(b1, b2)
    
    # Export FBX
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
    print(f"[VEIL_OF_MEMORY] Exported {name} to all 3 target destinations.")

# ===========================================================================
# 1. SM_Memorial_Historic_Well_Brick
# Hexagonal brick parapet well (radius 1.6m, height 1.1m) + timber pulley gallows + iron axle
# ===========================================================================
def build_historic_well():
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Memorial_Historic_Well_Brick_Mesh")
    obj = bpy.data.objects.new("SM_Memorial_Historic_Well_Brick", mesh)
    bpy.context.collection.objects.link(obj)
    
    obj.data.materials.append(get_or_create_mat("M_LahoriBrick_PBR", (0.55, 0.24, 0.14, 1.0), roughness=0.88))
    obj.data.materials.append(get_or_create_mat("M_AgedTeak_PBR", (0.28, 0.17, 0.10, 1.0), roughness=0.75))
    obj.data.materials.append(get_or_create_mat("M_WroughtIron_PBR", (0.15, 0.16, 0.17, 1.0), roughness=0.55, metallic=0.85))
    
    bm = bmesh.new()
    
    # Outer brick parapet cylinder (radius 1.6m, depth 1.1m)
    bmesh.ops.create_cone(
        bm, cap_ends=True, segments=16, radius1=1.65, radius2=1.60, depth=1.1,
        matrix=Matrix.Translation(Vector((0, 0, 0.55)))
    )
    # Inner well shaft void (radius 1.25m, depth 1.8m down)
    bmesh.ops.create_cone(
        bm, cap_ends=True, segments=16, radius1=1.25, radius2=1.25, depth=1.8,
        matrix=Matrix.Translation(Vector((0, 0, 0.2)))
    )
    # Heavy stone coping rim ring around top
    bmesh.ops.create_cone(
        bm, cap_ends=True, segments=16, radius1=1.75, radius2=1.72, depth=0.15,
        matrix=Matrix.Translation(Vector((0, 0, 1.15)))
    )
    
    # Assign brick material (slot 0)
    bm.faces.ensure_lookup_table()
    for f in bm.faces:
        f.material_index = 0
        f.smooth = True
        
    # Timber Gallows Pulley Frame (two upright posts + crossbeam)
    # Post 1 & 2
    for sx in [-1.45, 1.45]:
        bmesh.ops.create_cube(
            bm, size=1.0,
            matrix=Matrix.Translation(Vector((sx, 0, 1.65))) @ Matrix.Diagonal((0.20, 0.20, 2.2, 1.0))
        )
    # Top Crossbeam
    bmesh.ops.create_cube(
        bm, size=1.0,
        matrix=Matrix.Translation(Vector((0, 0, 2.75))) @ Matrix.Diagonal((3.2, 0.22, 0.22, 1.0))
    )
    # Diagonal Knee Braces
    for sx in [-1.15, 1.15]:
        bmesh.ops.create_cube(
            bm, size=1.0,
            matrix=Matrix.Translation(Vector((sx, 0, 2.45))) @ Matrix.Rotation(math.radians(-sx * 28.0), 4, 'Y') @ Matrix.Diagonal((0.55, 0.16, 0.14, 1.0))
        )
        
    # Iron Pulley Wheel and Suspension Rod (Slot 2)
    bmesh.ops.create_cone(
        bm, cap_ends=True, segments=14, radius1=0.28, radius2=0.28, depth=0.08,
        matrix=Matrix.Translation(Vector((0, 0, 2.30))) @ Matrix.Rotation(math.radians(90.0), 4, 'X')
    )
    # Pulley hanging bracket
    bmesh.ops.create_cube(
        bm, size=1.0,
        matrix=Matrix.Translation(Vector((0, 0, 2.55))) @ Matrix.Diagonal((0.08, 0.12, 0.45, 1.0))
    )
    
    # Material assignment for timber and iron
    bm.faces.ensure_lookup_table()
    for f in bm.faces:
        c = f.calc_center_median()
        if c.z > 1.25:
            if abs(c.x) < 0.35 and c.z < 2.50:
                f.material_index = 2 # Iron pulley
            else:
                f.material_index = 1 # Teak gallows
                
    bm.to_mesh(mesh)
    bm.free()
    export_asset("SM_Memorial_Historic_Well_Brick", obj)

# ===========================================================================
# 2. SM_Prop_Overturned_Brass_Lota
# Ornate spherical hammered brass pot resting on its side
# ===========================================================================
def build_overturned_lota():
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Prop_Overturned_Brass_Lota_Mesh")
    obj = bpy.data.objects.new("SM_Prop_Overturned_Brass_Lota", mesh)
    bpy.context.collection.objects.link(obj)
    
    obj.data.materials.append(get_or_create_mat("M_Brass_PBR", (0.82, 0.65, 0.24, 1.0), roughness=0.35, metallic=0.90))
    bm = bmesh.new()
    
    # Spherical body tilted at 75 degrees on the ground (radius 0.12m)
    rot_m = Matrix.Rotation(math.radians(75.0), 4, 'Y')
    bmesh.ops.create_uvsphere(
        bm, u_segments=16, v_segments=12, radius=0.12,
        matrix=Matrix.Translation(Vector((0, 0, 0.10))) @ rot_m
    )
    # Flared neck rim
    bmesh.ops.create_cone(
        bm, cap_ends=True, segments=16, radius1=0.09, radius2=0.065, depth=0.08,
        matrix=Matrix.Translation(Vector((0.12, 0, 0.13))) @ rot_m
    )
    # Flat base foot
    bmesh.ops.create_cone(
        bm, cap_ends=True, segments=14, radius1=0.06, radius2=0.065, depth=0.025,
        matrix=Matrix.Translation(Vector((-0.11, 0, 0.08))) @ rot_m
    )
    
    bm.faces.ensure_lookup_table()
    for f in bm.faces:
        f.material_index = 0
        f.smooth = True
        
    bm.to_mesh(mesh)
    bm.free()
    export_asset("SM_Prop_Overturned_Brass_Lota", obj)

# ===========================================================================
# 3. SM_Prop_Abandoned_Paper_Kite
# Traditional Punjabi Patang (0.55m x 0.55m diamond) with bamboo spine and bow spar
# ===========================================================================
def build_paper_kite():
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Prop_Abandoned_Paper_Kite_Mesh")
    obj = bpy.data.objects.new("SM_Prop_Abandoned_Paper_Kite", mesh)
    bpy.context.collection.objects.link(obj)
    
    obj.data.materials.append(get_or_create_mat("M_Paper_PBR", (0.88, 0.35, 0.15, 1.0), roughness=0.80))
    obj.data.materials.append(get_or_create_mat("M_AgedTeak_PBR", (0.28, 0.17, 0.10, 1.0), roughness=0.75))
    bm = bmesh.new()
    
    # Diamond paper sail (4 vertices)
    v_top = bm.verts.new(Vector((0, 0, 0.35)))
    v_bot = bm.verts.new(Vector((0, 0, -0.25)))
    v_l = bm.verts.new(Vector((-0.26, 0.02, 0.08)))
    v_r = bm.verts.new(Vector((0.26, 0.02, 0.08)))
    f1 = bm.faces.new([v_top, v_r, v_l])
    f2 = bm.faces.new([v_l, v_r, v_bot])
    f1.material_index = 0
    f2.material_index = 0
    
    # Bamboo center spine spar (Z: -0.25 to 0.35)
    bmesh.ops.create_cone(
        bm, cap_ends=True, segments=8, radius1=0.005, radius2=0.004, depth=0.62,
        matrix=Matrix.Translation(Vector((0, 0.003, 0.05)))
    )
    # Bamboo curved horizontal bow spar
    bmesh.ops.create_cone(
        bm, cap_ends=True, segments=8, radius1=0.0045, radius2=0.004, depth=0.54,
        matrix=Matrix.Translation(Vector((0, 0.015, 0.08))) @ Matrix.Rotation(math.radians(90.0), 4, 'Y')
    )
    
    bm.faces.ensure_lookup_table()
    for f in bm.faces:
        if f not in [f1, f2]:
            f.material_index = 1
            f.smooth = True
            
    bm.to_mesh(mesh)
    bm.free()
    export_asset("SM_Prop_Abandoned_Paper_Kite", obj)

# ===========================================================================
# 4. SM_Prop_Wooden_Takhti_Slate
# Traditional wooden student writing board (0.38m x 0.22m) with handle & inkpot
# ===========================================================================
def build_takhti_slate():
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Prop_Wooden_Takhti_Slate_Mesh")
    obj = bpy.data.objects.new("SM_Prop_Wooden_Takhti_Slate", mesh)
    bpy.context.collection.objects.link(obj)
    
    obj.data.materials.append(get_or_create_mat("M_AgedTeak_PBR", (0.28, 0.17, 0.10, 1.0), roughness=0.75))
    obj.data.materials.append(get_or_create_mat("M_Brass_PBR", (0.82, 0.65, 0.24, 1.0), roughness=0.35, metallic=0.90))

    bm = bmesh.new()
    
    # Rectangular wooden plank (0.38m length, 0.20m width, 0.015m thickness)
    bmesh.ops.create_cube(
        bm, size=1.0,
        matrix=Matrix.Translation(Vector((0, 0, 0.01))) @ Matrix.Diagonal((0.20, 0.36, 0.015, 1.0))
    )
    # Carved triangular top handle with suspension hole
    bmesh.ops.create_cone(
        bm, cap_ends=True, segments=6, radius1=0.07, radius2=0.07, depth=0.015,
        matrix=Matrix.Translation(Vector((0, 0.22, 0.01)))
    )
    # Handle suspension hole rim
    bmesh.ops.create_cone(
        bm, cap_ends=True, segments=10, radius1=0.015, radius2=0.015, depth=0.02,
        matrix=Matrix.Translation(Vector((0, 0.22, 0.01)))
    )
    
    # Small brass inkpot (dawaat) resting next to it
    bmesh.ops.create_cone(
        bm, cap_ends=True, segments=12, radius1=0.035, radius2=0.028, depth=0.05,
        matrix=Matrix.Translation(Vector((0.14, -0.05, 0.03)))
    )
    
    bm.faces.ensure_lookup_table()
    for f in bm.faces:
        c = f.calc_center_median()
        if c.x > 0.09 and c.z > 0.015:
            f.material_index = 1 # Brass inkpot
        else:
            f.material_index = 0 # Teak slate
        f.smooth = True
        
    bm.to_mesh(mesh)
    bm.free()
    export_asset("SM_Prop_Wooden_Takhti_Slate", obj)

# Execute All
build_historic_well()
build_overturned_lota()
build_paper_kite()
build_takhti_slate()

print("[VEIL_OF_MEMORY] SUCCESS! All 4 memorial assets modeled and dual-exported.")
