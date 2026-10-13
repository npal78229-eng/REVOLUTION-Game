"""
PROJECT REVOLUTION — Character Modeling Suite: Kabir (12-Year-Old Protagonist)
Author: Technical Character Artist
Toolchain: Blender 5.2 LTS

Details Kabir with historical 1919 Central Punjab authenticity:
- Proportions: 12-year-old Punjabi boy (height: 1.42m, ~6.5 head proportions)
- Head: Youthful facial features, ears, nose bridge, eyes
- Headwear: Traditional saffron/turmeric Punjabi patka (rumal wrap & juda topknot)
- Upper: Handspun off-white khadi kurta with Nehru mandarin collar & 3 wooden buttons
- Lower: Loose white cotton pajama trousers with knee folds
- Footwear: Traditional brown leather Punjabi juttis with upturned curled toes (nok)
- Gear: Weathered courier satchel with brass buckle & tailor's chalk pouch

Saves to:
- C:\\Users\\npal7\\PROJECT\\REVOLUTION\\Art\\PROJECT\\Kabir_Character_Detailed.blend
- C:\\Users\\npal7\\PROJECT\\PROJECT\\Kabir_Character_Detailed.blend
- Exports FBX to both directories
- Renders high-res presentation images
"""

import bpy
import bmesh
import math
import os
from mathutils import Vector, Matrix

# Clean scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# ---------------------------------------------------------------------------
# PBR Materials
# ---------------------------------------------------------------------------
def create_pbr_mat(name, base_color=(0.5, 0.5, 0.5, 1.0), roughness=0.7, metallic=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = base_color
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = roughness
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = metallic
    return mat

mat_skin = create_pbr_mat("M_Skin_Punjabi", (0.74, 0.49, 0.36, 1.0), roughness=0.58)
mat_patka = create_pbr_mat("M_Patka_Saffron", (0.94, 0.54, 0.08, 1.0), roughness=0.82)
mat_kurta = create_pbr_mat("M_Khadi_Kurta", (0.88, 0.85, 0.78, 1.0), roughness=0.88)
mat_pajama = create_pbr_mat("M_Cotton_Pajama", (0.90, 0.88, 0.84, 1.0), roughness=0.85)
mat_satchel = create_pbr_mat("M_Leather_Satchel", (0.34, 0.20, 0.12, 1.0), roughness=0.62)
mat_jutti = create_pbr_mat("M_Leather_Jutti", (0.28, 0.15, 0.08, 1.0), roughness=0.50)
mat_brass = create_pbr_mat("M_Brass_Buckle", (0.82, 0.68, 0.25, 1.0), roughness=0.35, metallic=0.88)
mat_chalk = create_pbr_mat("M_Chalk_White", (0.96, 0.96, 0.95, 1.0), roughness=0.95)
mat_hair = create_pbr_mat("M_Dark_Hair", (0.08, 0.06, 0.05, 1.0), roughness=0.7)

def create_cylinder(bm, radius, depth, segments=12, matrix=None):
    res = bmesh.ops.create_cone(bm, cap_ends=True, segments=segments, radius1=radius, radius2=radius, depth=depth)
    if matrix is not None:
        bmesh.ops.transform(bm, verts=res['verts'], matrix=matrix)
    return res

# ---------------------------------------------------------------------------
# Construct Kabir Mesh
# ---------------------------------------------------------------------------
mesh_kabir = bpy.data.meshes.new("SM_Kabir_Detailed")
obj_kabir = bpy.data.objects.new("Kabir_Protagonist", mesh_kabir)
bpy.context.collection.objects.link(obj_kabir)

bm = bmesh.new()

# Proportions (12-year-old child: Height = 1.42m)

# 1. FEET & TRADITIONAL LEATHER JUTTIS (Z = 0 to 0.08m)
for sx in [-0.11, 0.11]:
    # Sole & heel
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((sx, 0.02, 0.035))) @ Matrix.Diagonal((0.085, 0.21, 0.045, 1.0)))
    # Curled toe tip (Nok)
    bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.035, radius2=0.008, depth=0.06, matrix=Matrix.Translation(Vector((sx, 0.13, 0.05))) @ Matrix.Rotation(math.radians(-30.0), 4, 'X'))
    # Ankle opening
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((sx, -0.01, 0.065))) @ Matrix.Diagonal((0.075, 0.12, 0.05, 1.0)))

# 2. COTTON PAJAMA / TROUSERS (Z = 0.08 to 0.72m)
for sx in [-0.11, 0.11]:
    create_cylinder(bm, radius=0.052, depth=0.30, segments=12, matrix=Matrix.Translation(Vector((sx, 0.0, 0.24))))
    create_cylinder(bm, radius=0.062, depth=0.08, segments=12, matrix=Matrix.Translation(Vector((sx, 0.01, 0.40))))
    create_cylinder(bm, radius=0.068, depth=0.30, segments=12, matrix=Matrix.Translation(Vector((sx, 0.0, 0.56))))

# Pelvis waist
bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 0.72))) @ Matrix.Diagonal((0.26, 0.17, 0.14, 1.0)))

# 3. HANDSPUN KHADI KURTA (Z = 0.48 to 1.18m)
# Kurta Skirt (reaching past knees)
bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 0.62))) @ Matrix.Diagonal((0.30, 0.20, 0.28, 1.0)))
# Side slits (Chaks)
for sx in [-0.155, 0.155]:
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((sx, 0.0, 0.56))) @ Matrix.Diagonal((0.01, 0.18, 0.16, 1.0)))

# Torso Body
bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 0.96))) @ Matrix.Diagonal((0.28, 0.18, 0.44, 1.0)))

# Chest button placket
bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.092, 1.05))) @ Matrix.Diagonal((0.038, 0.012, 0.22, 1.0)))
# 3 Wooden buttons
for bz in [0.98, 1.05, 1.12]:
    create_cylinder(bm, radius=0.009, depth=0.008, segments=8, matrix=Matrix.Translation(Vector((0.0, 0.10, bz))) @ Matrix.Rotation(math.radians(90.0), 4, 'X'))
# Nehru mandarin band collar
create_cylinder(bm, radius=0.062, depth=0.035, segments=14, matrix=Matrix.Translation(Vector((0.0, 0.0, 1.19))))

# 4. ARMS & SLEEVES
for sign, sx in [(-1, -0.17), (1, 0.17)]:
    # Shoulder cap
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((sx, 0.0, 1.15))) @ Matrix.Diagonal((0.09, 0.14, 0.09, 1.0)))
    # Upper arm
    create_cylinder(bm, radius=0.048, depth=0.22, segments=12, matrix=Matrix.Translation(Vector((sx + sign*0.02, 0.01, 1.02))) @ Matrix.Rotation(math.radians(-sign*12.0), 4, 'Y'))
    # Forearm
    create_cylinder(bm, radius=0.045, depth=0.20, segments=12, matrix=Matrix.Translation(Vector((sx + sign*0.04, 0.03, 0.83))) @ Matrix.Rotation(math.radians(-sign*8.0), 4, 'Y'))
    # Cuff ring
    create_cylinder(bm, radius=0.052, depth=0.03, segments=12, matrix=Matrix.Translation(Vector((sx + sign*0.05, 0.035, 0.74))))
    # Slender youth hand
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((sx + sign*0.055, 0.038, 0.67))) @ Matrix.Diagonal((0.045, 0.065, 0.11, 1.0)))

# 5. NECK & HEAD
create_cylinder(bm, radius=0.048, depth=0.08, segments=12, matrix=Matrix.Translation(Vector((0.0, 0.01, 1.22))))
# Head cranium
bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.02, 1.32))) @ Matrix.Diagonal((0.15, 0.17, 0.18, 1.0)))
# Jaw & chin
bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.045, 1.25))) @ Matrix.Diagonal((0.11, 0.12, 0.08, 1.0)))
# Nose bridge & tip
bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.018, radius2=0.006, depth=0.038, matrix=Matrix.Translation(Vector((0.0, 0.115, 1.305))) @ Matrix.Rotation(math.radians(-75.0), 4, 'X'))
# Ears
for sign in [-1, 1]:
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((sign * 0.085, 0.01, 1.31))) @ Matrix.Diagonal((0.02, 0.035, 0.055, 1.0)))

# 6. TRADITIONAL PUNJABI SAFFRON PATKA
# Main headwrap wrap
create_cylinder(bm, radius=0.088, depth=0.10, segments=16, matrix=Matrix.Translation(Vector((0.0, 0.02, 1.38))))
# Forehead band with V-angle
bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.095, 1.355))) @ Matrix.Diagonal((0.14, 0.022, 0.04, 1.0)))
# Topknot (Juda bun)
create_cylinder(bm, radius=0.042, depth=0.06, segments=14, matrix=Matrix.Translation(Vector((0.0, 0.01, 1.45))))
# Side ties resting on shoulders
for sign in [-1, 1]:
    create_cylinder(bm, radius=0.012, depth=0.14, segments=8, matrix=Matrix.Translation(Vector((sign * 0.075, -0.04, 1.28))) @ Matrix.Rotation(math.radians(sign*15.0), 4, 'Y'))

# 7. COURIER SATCHEL BAG
# Diagonal leather strap
create_cylinder(bm, radius=0.018, depth=0.62, segments=10, matrix=Matrix.Translation(Vector((-0.03, 0.02, 0.97))) @ Matrix.Rotation(math.radians(38.0), 4, 'Y') @ Matrix.Rotation(math.radians(12.0), 4, 'X'))
# Satchel body
bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((-0.18, -0.04, 0.72))) @ Matrix.Diagonal((0.08, 0.24, 0.19, 1.0)))
# Flap
bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((-0.18, -0.082, 0.73))) @ Matrix.Diagonal((0.082, 0.014, 0.14, 1.0)))
# Brass buckle
bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((-0.18, -0.092, 0.68))) @ Matrix.Diagonal((0.045, 0.010, 0.035, 1.0)))

# 8. TAILOR'S CHALK POUCH & RIVER MARBLES (Right waist)
bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.155, 0.02, 0.76))) @ Matrix.Diagonal((0.05, 0.08, 0.09, 1.0)))
bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.155, 0.02, 0.82))) @ Matrix.Diagonal((0.022, 0.035, 0.05, 1.0)))

bm.to_mesh(mesh_kabir)
bm.free()

mesh_kabir.materials.append(mat_kurta)
mesh_kabir.materials.append(mat_patka)
mesh_kabir.materials.append(mat_skin)
mesh_kabir.materials.append(mat_pajama)
mesh_kabir.materials.append(mat_satchel)
mesh_kabir.materials.append(mat_jutti)
mesh_kabir.materials.append(mat_brass)
mesh_kabir.materials.append(mat_chalk)

# ---------------------------------------------------------------------------
# Studio Presentation Lighting & Camera
# ---------------------------------------------------------------------------
# Key light (warm golden sunlight)
light_key = bpy.data.lights.new(name="Key_Light", type='POINT')
light_key.energy = 550.0
light_key.color = (1.0, 0.94, 0.84)
obj_light_key = bpy.data.objects.new("Key_Light", light_key)
obj_light_key.location = (1.5, -2.0, 2.2)
bpy.context.collection.objects.link(obj_light_key)

# Rim light (cool sky backlight)
light_rim = bpy.data.lights.new(name="Rim_Light", type='POINT')
light_rim.energy = 320.0
light_rim.color = (0.75, 0.85, 1.0)
obj_light_rim = bpy.data.objects.new("Rim_Light", light_rim)
obj_light_rim.location = (-1.2, 1.8, 1.9)
bpy.context.collection.objects.link(obj_light_rim)

# Fill light (soft ambient bounce)
light_fill = bpy.data.lights.new(name="Fill_Light", type='POINT')
light_fill.energy = 180.0
light_fill.color = (0.95, 0.92, 0.88)
obj_light_fill = bpy.data.objects.new("Fill_Light", light_fill)
obj_light_fill.location = (-1.5, -1.2, 0.9)
bpy.context.collection.objects.link(obj_light_fill)

# Camera (three-quarter full portrait)
cam_data = bpy.data.cameras.new("Kabir_Presentation_Cam")
obj_cam = bpy.data.objects.new("Kabir_Presentation_Cam", cam_data)
obj_cam.location = (0.8, -2.4, 1.05)
obj_cam.rotation_euler = (math.radians(82.0), 0.0, math.radians(20.0))
bpy.context.collection.objects.link(obj_cam)
bpy.context.scene.camera = obj_cam

# Render settings
bpy.context.scene.render.resolution_x = 1280
bpy.context.scene.render.resolution_y = 960
bpy.context.scene.render.image_settings.file_format = 'PNG'

# ---------------------------------------------------------------------------
# Save to designated PROJECT directories
# ---------------------------------------------------------------------------
project_art_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\PROJECT"
project_dest_dir = r"C:\Users\npal7\PROJECT\PROJECT"
os.makedirs(project_art_dir, exist_ok=True)
os.makedirs(project_dest_dir, exist_ok=True)

blend_path_1 = os.path.join(project_art_dir, "Kabir_Character_Detailed.blend")
blend_path_2 = os.path.join(project_dest_dir, "Kabir_Character_Detailed.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path_1)
bpy.ops.wm.save_as_mainfile(filepath=blend_path_2)

# Export FBX
fbx_path_1 = os.path.join(project_art_dir, "SK_Kabir_Character_Detailed.fbx")
fbx_path_2 = os.path.join(project_dest_dir, "SK_Kabir_Character_Detailed.fbx")

bpy.ops.object.select_all(action='DESELECT')
obj_kabir.select_set(True)
bpy.context.view_layer.objects.active = obj_kabir

bpy.ops.export_scene.fbx(
    filepath=fbx_path_1,
    use_selection=True,
    global_scale=100.0,
    axis_forward='-Z',
    axis_up='Y',
    apply_unit_scale=True,
    bake_space_transform=True,
    mesh_smooth_type='FACE'
)
bpy.ops.export_scene.fbx(
    filepath=fbx_path_2,
    use_selection=True,
    global_scale=100.0,
    axis_forward='-Z',
    axis_up='Y',
    apply_unit_scale=True,
    bake_space_transform=True,
    mesh_smooth_type='FACE'
)

# Render presentation images
render_img_1 = os.path.join(project_art_dir, "Kabir_Presentation_Render.png")
render_img_2 = os.path.join(project_dest_dir, "Kabir_Presentation_Render.png")
bpy.context.scene.render.filepath = render_img_1
bpy.ops.render.render(write_still=True)

# Copy rendered image to second path
import shutil
shutil.copyfile(render_img_1, render_img_2)

print(f"[SUCCESS] Kabir model saved to: {blend_path_1}")
print(f"[SUCCESS] Kabir FBX saved to: {fbx_path_1}")
print(f"[SUCCESS] Render image saved to: {render_img_1}")
