"""
PROJECT REVOLUTION — Final AAA Kabir Character Polish & Studio Presentation
Adds knee-length kurta skirt with side chaks, expressive facial features, balanced lighting, and dual folder persistence
"""

import bpy
import bmesh
import math
import os
from mathutils import Vector, Matrix

print("[AAA_KABIR] Refining Kurta Skirt, Facial Features & Cinematic Studio Shading...")

arm = bpy.data.objects.get("Kabir_Armature")
body = bpy.data.objects.get("Kabir_Body")
kurta = bpy.data.objects.get("Kabir_Kurta")
patka = bpy.data.objects.get("Kabir_Patka")

# 1. ADD KNEE-LENGTH SKIRT TO KURTA (Z: 0.72 down to 0.48 with side chaks)
bm_k = bmesh.new()
bm_k.from_mesh(kurta.data)

# Add flared lower skirt rings
skirt_rings = [
    # (z, rx, ry, y_off)
    (0.70, 0.142, 0.095, 0.006),
    (0.62, 0.155, 0.104, 0.008),
    (0.54, 0.168, 0.112, 0.010),
    (0.46, 0.178, 0.120, 0.012), # Knee level
]

prev_sk = []
for idx, (z, rx, ry, y_off) in enumerate(skirt_rings):
    curr_sk = []
    num_pts = 18
    for i in range(num_pts):
        ang = 2 * math.pi * i / num_pts
        x = rx * math.sin(ang)
        y = ry * math.cos(ang) + y_off
        v = bm_k.verts.new(Vector((x, y, z)))
        curr_sk.append(v)
    if prev_sk:
        for i in range(num_pts):
            ni = (i + 1) % num_pts
            # Side slits (chaks) at lateral seams (indices 4 and 13)
            if idx >= 2 and (i == 4 or i == 13):
                continue
            bm_k.faces.new([prev_sk[i], prev_sk[ni], curr_sk[ni], curr_sk[i]])
    prev_sk = curr_sk

bm_k.to_mesh(kurta.data)
bm_k.free()
for p in kurta.data.polygons:
    p.use_smooth = True

# 2. FACIAL FEATURES & EYES
mat_dark = bpy.data.materials.get("M_Kabir_Hair")
mat_iris = bpy.data.materials.get("M_Kabir_Iris")
mat_sclera = bpy.data.materials.get("M_Kabir_Sclera")

# Clear any previous eye/brow meshes
for name in ["Kabir_Eye_L", "Kabir_Eye_R", "Kabir_Brows", "Kabir_Lashes_L", "Kabir_Lashes_R"]:
    o = bpy.data.objects.get(name)
    if o:
        bpy.data.objects.remove(o, do_unlink=True)

# Almond Eyeballs nestled at (±0.033, 0.062, 1.308)
for side, sign in [("L", 1), ("R", -1)]:
    m_e = bpy.data.meshes.new(f"Eye_Mesh_{side}")
    o_e = bpy.data.objects.new(f"Kabir_Eye_{side}", m_e)
    bpy.context.collection.objects.link(o_e)
    o_e.data.materials.append(mat_sclera)
    o_e.data.materials.append(mat_iris)
    o_e.parent = arm
    
    bm_e = bmesh.new()
    bmesh.ops.create_uvsphere(bm_e, u_segments=20, v_segments=14, radius=0.012, matrix=Matrix.Translation(Vector((sign * 0.033, 0.062, 1.308))) @ Matrix.Rotation(math.radians(90.0), 4, 'X'))
    for f in bm_e.faces:
        if f.calc_center_median().y > 0.071:
            f.material_index = 1
    bm_e.to_mesh(m_e)
    bm_e.free()
    for p in m_e.polygons:
        p.use_smooth = True

    # Upper Eyelid Lash Line Arch
    m_l = bpy.data.meshes.new(f"Lash_Mesh_{side}")
    o_l = bpy.data.objects.new(f"Kabir_Lashes_{side}", m_l)
    bpy.context.collection.objects.link(o_l)
    o_l.data.materials.append(mat_dark)
    o_l.parent = arm
    bm_l = bmesh.new()
    bmesh.ops.create_cone(bm_l, cap_ends=True, segments=12, radius1=0.014, radius2=0.013, depth=0.005, matrix=Matrix.Translation(Vector((sign * 0.033, 0.066, 1.314))) @ Matrix.Rotation(math.radians(82.0), 4, 'X'))
    bm_l.to_mesh(m_l)
    bm_l.free()
    for p in m_l.polygons:
        p.use_smooth = True

# Dark Arched Eyebrows
m_b = bpy.data.meshes.new("Brows_Mesh")
o_b = bpy.data.objects.new("Kabir_Eyebrows", m_b)
bpy.context.collection.objects.link(o_b)
o_b.data.materials.append(mat_dark)
o_b.parent = arm
bm_b = bmesh.new()
for sign in [-1, 1]:
    brow_pts = [
        Vector((sign * 0.016, 0.072, 1.324)),
        Vector((sign * 0.034, 0.070, 1.332)),
        Vector((sign * 0.052, 0.058, 1.324)),
    ]
    for i in range(len(brow_pts) - 1):
        p1 = brow_pts[i]
        p2 = brow_pts[i+1]
        mid = (p1 + p2) * 0.5
        bmesh.ops.create_cone(bm_b, cap_ends=True, segments=8, radius1=0.005, radius2=0.003, depth=(p2 - p1).length, matrix=Matrix.Translation(mid) @ Matrix.Rotation(math.radians(-sign * 18.0), 4, 'Y') @ Matrix.Diagonal((1.0, 0.35, 1.0, 1.0)))
bm_b.to_mesh(m_b)
bm_b.free()
for p in m_b.polygons:
    p.use_smooth = True

# 3. CALIBRATE BALANCED STUDIO LIGHTING
# Prevent overexposure and washing out of colors
key = bpy.data.objects.get("Sun_Key_AAA")
if key:
    key.location = (-0.9, 1.8, 1.6)
    key.data.energy = 95.0 # Balanced key
    key.data.color = (1.0, 0.94, 0.85)

rim = bpy.data.objects.get("Sky_Rim_AAA")
if rim:
    rim.location = (1.1, -1.4, 1.5)
    rim.data.energy = 60.0 # Balanced rim
    rim.data.color = (0.75, 0.88, 1.0)

fill = bpy.data.objects.get("Fill_Light_AAA")
if fill:
    fill.location = (0.9, 1.4, 0.9)
    fill.data.energy = 35.0 # Soft fill
    fill.data.color = (0.95, 0.90, 0.85)

world = bpy.context.scene.world
if world and world.node_tree:
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.20, 0.21, 0.23, 1.0) # Elegant dark slate neutral studio
        bg.inputs["Strength"].default_value = 0.45

# Hero Camera (Full-Body 3/4)
cam_hero = bpy.data.objects.get("Cam_Hero_FullBody")
if cam_hero:
    cam_hero.location = (-0.42, 2.15, 0.80)
    cam_hero.rotation_euler = (math.radians(88.0), 0.0, math.radians(-169.0))

# Portrait Camera (Face, Eyes, Saffron Patka)
cam_port = bpy.data.objects.get("Cam_Portrait_Face")
if cam_port:
    cam_port.location = (-0.14, 0.88, 1.30)
    cam_port.rotation_euler = (math.radians(88.0), 0.0, math.radians(-171.0))

# 4. SAVE & EXPORT PIPELINE
art_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\PROJECT"
dest_dir = r"C:\Users\npal7\PROJECT\PROJECT"
os.makedirs(art_dir, exist_ok=True)
os.makedirs(dest_dir, exist_ok=True)

blend_art = os.path.join(art_dir, "Kabir_Protagonist_AAA.blend")
blend_dest = os.path.join(dest_dir, "Kabir_Protagonist_AAA.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_art)
bpy.ops.wm.save_as_mainfile(filepath=blend_dest)

fbx_art = os.path.join(art_dir, "SK_Kabir_Protagonist_AAA.fbx")
fbx_dest = os.path.join(dest_dir, "SK_Kabir_Protagonist_AAA.fbx")
bpy.ops.object.select_all(action='SELECT')
for fpath in [fbx_art, fbx_dest]:
    bpy.ops.export_scene.fbx(
        filepath=fpath,
        use_selection=True,
        global_scale=100.0,
        axis_forward='-Z',
        axis_up='Y',
        apply_unit_scale=True,
        bake_space_transform=True,
        mesh_smooth_type='FACE',
        add_leaf_bones=False,
        primary_bone_axis='Y',
        secondary_bone_axis='X'
    )

# Render Hero Still
render_hero_art = os.path.join(art_dir, "Kabir_Protagonist_AAA_Hero.png")
render_hero_dest = os.path.join(dest_dir, "Kabir_Protagonist_AAA_Hero.png")
bpy.context.scene.camera = cam_hero
bpy.context.scene.render.filepath = render_hero_art
bpy.ops.render.render(write_still=True)

import shutil
shutil.copyfile(render_hero_art, render_hero_dest)

# Render Portrait Still
render_port_art = os.path.join(art_dir, "Kabir_Protagonist_AAA_Portrait.png")
render_port_dest = os.path.join(dest_dir, "Kabir_Protagonist_AAA_Portrait.png")
bpy.context.scene.camera = cam_port
bpy.context.scene.render.filepath = render_port_art
bpy.ops.render.render(write_still=True)
shutil.copyfile(render_port_art, render_port_dest)

print(f"[AAA_KABIR] SUCCESS! Saved {blend_art} and {blend_dest}")
print(f"[AAA_KABIR] SUCCESS! Exported rigged FBX to {fbx_art} and {fbx_dest}")
print(f"[AAA_KABIR] SUCCESS! Renders saved to {render_hero_art} and {render_port_art}")
