"""
PROJECT REVOLUTION — Master AAA Protagonist Character: Kabir (12yo Indian Boy, April 1919)
Production Character Pipeline: Anatomical Base Mesh + Authentic 1919 Attire + UE5 Rig
"""

import bpy
import bmesh
import math
import os
from mathutils import Vector, Matrix

print("[AAA_KABIR] Initializing Master Production Pipeline...")

# ---------------------------------------------------------------------------
# 1. Clean Scene
# ---------------------------------------------------------------------------
for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj, do_unlink=True)
for mesh in list(bpy.data.meshes):
    bpy.data.meshes.remove(mesh, do_unlink=True)
for arm in list(bpy.data.armatures):
    bpy.data.armatures.remove(arm, do_unlink=True)
for mat in list(bpy.data.materials):
    bpy.data.materials.remove(mat, do_unlink=True)
for cam in list(bpy.data.cameras):
    bpy.data.cameras.remove(cam, do_unlink=True)
for light in list(bpy.data.lights):
    bpy.data.lights.remove(light, do_unlink=True)

# ---------------------------------------------------------------------------
# 2. Import CC0 Anatomical Base Mesh & Rig
# ---------------------------------------------------------------------------
glb_path = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\male_base_mesh.glb"
bpy.ops.import_scene.gltf(filepath=glb_path)

body_obj = bpy.data.objects.get("mesh")
arm_obj = bpy.data.objects.get("metarig")
body_obj.name = "Kabir_Body"
arm_obj.name = "Kabir_Armature"

# Hide armature from viewport render
arm_obj.hide_viewport = True
arm_obj.hide_render = True

# ---------------------------------------------------------------------------
# 3. Reshape & Proportions: 12-Year-Old Kabir (Height = 1.42m, 6.5 Heads)
# ---------------------------------------------------------------------------
# Base mesh height is ~1.95m. Target height is 1.42m.
scale_factor = 1.42 / 1.95

# Apply juvenile anatomical adjustments to vertices
vg_head = body_obj.vertex_groups.get("spine.005")
head_indices = set()
if vg_head:
    head_indices = {v.index for v in body_obj.data.vertices if vg_head.index in [g.group for g in v.groups]}

for v in body_obj.data.vertices:
    co = v.co
    # Overall juvenile scale
    co *= scale_factor
    
    # 12-year-old boy head proportion (slightly larger head relative to torso)
    if v.index in head_indices or co.z > 1.18:
        # Head center at z ~ 1.28
        dz = co.z - 1.28
        co.x *= 1.12
        co.y *= 1.10
        co.z = 1.28 + dz * 1.12
    # Softer juvenile shoulders (narrower deltoids)
    elif 0.85 < co.z <= 1.18:
        co.x *= 0.92
    v.co = co

body_obj.data.update()

# Scale armature to match
arm_obj.scale = (scale_factor, scale_factor, scale_factor)
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

print("[AAA_KABIR] Anatomical body rescaled to 1.42m juvenile proportions.")

# ---------------------------------------------------------------------------
# 4. Realistic PBR Materials (Principled BSDF v2)
# ---------------------------------------------------------------------------
def make_shader(name, base_color, roughness=0.5, metallic=0.0, sss_weight=0.0, sss_radius=(1.0, 0.6, 0.4), sheen_weight=0.0, coat_weight=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = base_color
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = roughness
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = metallic
        if "Subsurface Weight" in bsdf.inputs and sss_weight > 0:
            bsdf.inputs["Subsurface Weight"].default_value = sss_weight
            bsdf.inputs["Subsurface Radius"].default_value = sss_radius
            if "Subsurface Scale" in bsdf.inputs:
                bsdf.inputs["Subsurface Scale"].default_value = 0.05
        if "Sheen Weight" in bsdf.inputs and sheen_weight > 0:
            bsdf.inputs["Sheen Weight"].default_value = sheen_weight
        if "Coat Weight" in bsdf.inputs and coat_weight > 0:
            bsdf.inputs["Coat Weight"].default_value = coat_weight
    return mat

mat_skin = make_shader("M_Kabir_Skin_AAA", (0.68, 0.44, 0.30, 1.0), roughness=0.48, sss_weight=0.22, sss_radius=(1.0, 0.65, 0.42))
mat_eyes_sclera = make_shader("M_Kabir_Sclera", (0.94, 0.92, 0.90, 1.0), roughness=0.08)
mat_eyes_iris = make_shader("M_Kabir_Iris", (0.15, 0.08, 0.04, 1.0), roughness=0.05)
mat_patka = make_shader("M_Kabir_Patka_Saffron", (0.95, 0.48, 0.04, 1.0), roughness=0.82, sheen_weight=0.60)
mat_kurta = make_shader("M_Kabir_Khadi_Kurta", (0.86, 0.82, 0.74, 1.0), roughness=0.88, sheen_weight=0.35)
mat_pajama = make_shader("M_Kabir_Cotton_Pajama", (0.88, 0.86, 0.82, 1.0), roughness=0.85, sheen_weight=0.30)
mat_leather = make_shader("M_Kabir_Aged_Leather", (0.30, 0.16, 0.08, 1.0), roughness=0.52, coat_weight=0.32)
mat_brass = make_shader("M_Kabir_Brass", (0.84, 0.70, 0.28, 1.0), roughness=0.32, metallic=0.92)
mat_wood = make_shader("M_Kabir_Wood_Buttons", (0.24, 0.14, 0.08, 1.0), roughness=0.72)
mat_dark_hair = make_shader("M_Kabir_Hair", (0.06, 0.04, 0.03, 1.0), roughness=0.65)
mat_chalk = make_shader("M_Kabir_Chalk", (0.96, 0.96, 0.95, 1.0), roughness=0.95)

# Assign skin shader to body
body_obj.data.materials.clear()
body_obj.data.materials.append(mat_skin)

# Smooth shading & subdivision on body
for p in body_obj.data.polygons:
    p.use_smooth = True
mod_sub = body_obj.modifiers.new("Subdivision", 'SUBSURF')
mod_sub.levels = 1
mod_sub.render_levels = 2

# Helper for creating clothing & accessory objects
def create_piece(name, mat):
    m = bpy.data.meshes.new(f"{name}_Mesh")
    o = bpy.data.objects.new(name, m)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(mat)
    return o, m

# ---------------------------------------------------------------------------
# 5. Facial Features: Almond Eyes, Dark Brows & Hair
# ---------------------------------------------------------------------------
# Eyeballs nestled at (±0.033, 0.060, 1.305)
for side, sign in [("L", 1), ("R", -1)]:
    o_eye, m_eye = create_piece(f"Kabir_Eye_{side}", mat_eyes_sclera)
    o_eye.data.materials.append(mat_eyes_iris)
    bm_e = bmesh.new()
    bmesh.ops.create_uvsphere(bm_e, u_segments=20, v_segments=14, radius=0.0125, matrix=Matrix.Translation(Vector((sign * 0.033, 0.060, 1.305))) @ Matrix.Rotation(math.radians(90.0), 4, 'X'))
    for f in bm_e.faces:
        if f.calc_center_median().y > 0.070:
            f.material_index = 1
    bm_e.to_mesh(m_eye)
    bm_e.free()
    for p in m_eye.polygons:
        p.use_smooth = True

    # Upper Eyelid & Eyelash Rim
    o_lid, m_lid = create_piece(f"Kabir_Lashes_{side}", mat_dark_hair)
    bm_l = bmesh.new()
    bmesh.ops.create_cone(bm_l, cap_ends=True, segments=12, radius1=0.0145, radius2=0.0135, depth=0.005, matrix=Matrix.Translation(Vector((sign * 0.033, 0.065, 1.312))) @ Matrix.Rotation(math.radians(82.0), 4, 'X'))
    bm_l.to_mesh(m_lid)
    bm_l.free()
    for p in m_lid.polygons:
        p.use_smooth = True

# Arched Dark Eyebrows
o_brow, m_brow = create_piece("Kabir_Eyebrows", mat_dark_hair)
bm_b = bmesh.new()
for sign in [-1, 1]:
    brow_pts = [
        Vector((sign * 0.016, 0.074, 1.320)),
        Vector((sign * 0.033, 0.072, 1.328)),
        Vector((sign * 0.050, 0.060, 1.320)),
    ]
    for i in range(len(brow_pts) - 1):
        p1 = brow_pts[i]
        p2 = brow_pts[i+1]
        mid = (p1 + p2) * 0.5
        bmesh.ops.create_cone(bm_b, cap_ends=True, segments=8, radius1=0.005, radius2=0.003, depth=(p2 - p1).length, matrix=Matrix.Translation(mid) @ Matrix.Rotation(math.radians(-sign * 18.0), 4, 'Y') @ Matrix.Diagonal((1.0, 0.35, 1.0, 1.0)))
bm_b.to_mesh(m_brow)
bm_b.free()
for p in m_brow.polygons:
    p.use_smooth = True

# ---------------------------------------------------------------------------
# 6. Saffron Patka Headdress (Folded Wrap, Juda Topknot, Nape Ties)
# ---------------------------------------------------------------------------
o_patka, m_patka = create_piece("Kabir_Patka", mat_patka)
bm_p = bmesh.new()

# Fitted skull wrap (conforming from brow line up around the head)
bmesh.ops.create_uvsphere(bm_p, u_segments=24, v_segments=16, radius=0.088, matrix=Matrix.Translation(Vector((0.0, -0.008, 1.345))) @ Matrix.Diagonal((0.98, 1.06, 1.08, 1.0)))

# Forehead V-Crest Band (Characteristic folded cloth band resting right above brow)
bmesh.ops.create_cone(bm_p, cap_ends=True, segments=20, radius1=0.088, radius2=0.085, depth=0.030, matrix=Matrix.Translation(Vector((0.0, 0.004, 1.335))) @ Matrix.Diagonal((0.98, 1.06, 1.0, 1.0)))
bmesh.ops.create_cube(bm_p, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.078, 1.335))) @ Matrix.Diagonal((0.078, 0.010, 0.022, 1.0)))

# Topknot Juda Bun (Saffron cloth-wrapped topknot resting on cranium)
bmesh.ops.create_uvsphere(bm_p, u_segments=20, v_segments=14, radius=0.044, matrix=Matrix.Translation(Vector((0.0, 0.002, 1.448))) @ Matrix.Diagonal((1.0, 0.95, 0.88, 1.0)))

# Juda wrap cord / tie band
bmesh.ops.create_cone(bm_p, cap_ends=True, segments=18, radius1=0.046, radius2=0.044, depth=0.020, matrix=Matrix.Translation(Vector((0.0, 0.002, 1.425))))

# Draped Nape Ties flowing down the back of the neck
for sign in [-1, 1]:
    bmesh.ops.create_cone(bm_p, cap_ends=True, segments=10, radius1=0.014, radius2=0.008, depth=0.22, matrix=Matrix.Translation(Vector((sign * 0.045, -0.062, 1.235))) @ Matrix.Rotation(math.radians(-sign * 8.0), 4, 'Y') @ Matrix.Rotation(math.radians(12.0), 4, 'X'))

bm_p.to_mesh(m_patka)
bm_p.free()
for p in m_patka.polygons:
    p.use_smooth = True
mod_sol_patka = o_patka.modifiers.new("Solidify", 'SOLIDIFY')
mod_sol_patka.thickness = 0.004

# ---------------------------------------------------------------------------
# 7. Handspun Khadi Kurta (Mandarin Collar, Button Placket, Side Chaks)
# ---------------------------------------------------------------------------
o_kurta, m_kurta = create_piece("Kabir_Kurta", mat_kurta)
bm_k = bmesh.new()

# Torso Body Quad Rings (Chest to knee-length hem with side slits)
kurta_rings = [
    (1.16, 0.088, 0.074, 0.002), # Collar base
    (1.10, 0.142, 0.092, 0.000), # Shoulders
    (1.00, 0.138, 0.088, 0.002), # Chest
    (0.88, 0.132, 0.085, 0.004), # Waist
    (0.76, 0.142, 0.092, 0.006), # Hips
    (0.66, 0.155, 0.102, 0.008), # Upper thighs
    (0.56, 0.168, 0.110, 0.010), # Lower thighs
    (0.48, 0.178, 0.118, 0.012), # Knee-length hem
]

prev_k = []
for idx, (z, rx, ry, y_off) in enumerate(kurta_rings):
    curr_k = []
    num_k = 18
    for i in range(num_k):
        ang = 2 * math.pi * i / num_k
        x = rx * math.sin(ang)
        y = ry * math.cos(ang) + y_off
        v = bm_k.verts.new(Vector((x, y, z)))
        curr_k.append(v)
    if prev_k:
        for i in range(num_k):
            ni = (i + 1) % num_k
            # Leave open side chaks slits below hips (lateral seams)
            if idx >= 5 and (i == 4 or i == 13):
                continue
            bm_k.faces.new([prev_k[i], prev_k[ni], curr_k[ni], curr_k[i]])
    prev_k = curr_k

# Standing Mandarin / Nehru Collar
bmesh.ops.create_cone(bm_k, cap_ends=False, segments=18, radius1=0.062, radius2=0.058, depth=0.042, matrix=Matrix.Translation(Vector((0.0, 0.003, 1.178))))

# Front Button Placket
bmesh.ops.create_cube(bm_k, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.090, 1.02))) @ Matrix.Diagonal((0.034, 0.008, 0.22, 1.0)))

# Sleeves (Upper arm to rolled forearm cuffs)
for side, sign in [("L", 1), ("R", -1)]:
    sleeve_rings = [
        (Vector((sign * 0.14, 0.00, 1.10)), 0.056),
        (Vector((sign * 0.16, 0.01, 1.00)), 0.048),
        (Vector((sign * 0.18, 0.02, 0.88)), 0.044),
        (Vector((sign * 0.19, 0.03, 0.76)), 0.040),
        (Vector((sign * 0.20, 0.032, 0.70)), 0.044), # Rolled cuff
    ]
    prev_s = []
    for center, rad in sleeve_rings:
        curr_s = []
        for i in range(12):
            ang = 2 * math.pi * i / 12
            vx = center.x + rad * math.sin(ang) * 0.9
            vy = center.y + rad * math.cos(ang)
            vz = center.z
            v = bm_k.verts.new(Vector((vx, vy, vz)))
            curr_s.append(v)
        if prev_s:
            for i in range(12):
                ni = (i + 1) % 12
                bm_k.faces.new([prev_s[i], prev_s[ni], curr_s[ni], curr_s[i]])
        prev_s = curr_s

bm_k.to_mesh(m_kurta)
bm_k.free()
for p in m_kurta.polygons:
    p.use_smooth = True
mod_sub_k = o_kurta.modifiers.new("Subdivision", 'SUBSURF')
mod_sub_k.levels = 1
mod_sol_k = o_kurta.modifiers.new("Solidify", 'SOLIDIFY')
mod_sol_k.thickness = 0.004

# 3 Carved Wooden Buttons
o_btn, m_btn = create_piece("Kabir_Buttons", mat_wood)
bm_btn = bmesh.new()
for bz in [0.94, 1.01, 1.08]:
    bmesh.ops.create_cone(bm_btn, cap_ends=True, segments=12, radius1=0.008, radius2=0.008, depth=0.005, matrix=Matrix.Translation(Vector((0.0, 0.096, bz))) @ Matrix.Rotation(math.radians(90.0), 4, 'X'))
bm_btn.to_mesh(m_btn)
bm_btn.free()
for p in m_btn.polygons:
    p.use_smooth = True

# ---------------------------------------------------------------------------
# 8. Cotton Pajama Trousers (Gathered Knee & Ankle Churidar Folds)
# ---------------------------------------------------------------------------
o_pj, m_pj = create_piece("Kabir_Pajama", mat_pajama)
bm_pj = bmesh.new()

# Pelvis waistband
bmesh.ops.create_cone(bm_pj, cap_ends=True, segments=18, radius1=0.135, radius2=0.128, depth=0.16, matrix=Matrix.Translation(Vector((0.0, 0.005, 0.68))))

for side, sign in [("L", 1), ("R", -1)]:
    lx = sign * 0.095
    leg_rings = [
        (Vector((lx, 0.00, 0.60)), 0.068), # Groin / thigh
        (Vector((lx, 0.01, 0.48)), 0.062), # Mid thigh
        (Vector((lx, 0.012, 0.38)), 0.058), # Knee gather fold
        (Vector((lx, 0.010, 0.28)), 0.052), # Upper calf
        (Vector((lx, 0.006, 0.18)), 0.046), # Lower calf
        (Vector((lx, 0.004, 0.10)), 0.042), # Churidar ankle gather
        (Vector((lx, 0.002, 0.06)), 0.040), # Ankle hem
    ]
    prev_l = []
    for center, rad in leg_rings:
        curr_l = []
        for i in range(14):
            ang = 2 * math.pi * i / 14
            crease = 0.003 * math.sin(ang * 3 + center.z * 22.0)
            vx = center.x + (rad + crease) * math.sin(ang)
            vy = center.y + (rad + crease) * math.cos(ang)
            vz = center.z
            v = bm_pj.verts.new(Vector((vx, vy, vz)))
            curr_l.append(v)
        if prev_l:
            for i in range(14):
                ni = (i + 1) % 14
                bm_pj.faces.new([prev_l[i], prev_l[ni], curr_l[ni], curr_l[i]])
        prev_l = curr_l

bm_pj.to_mesh(m_pj)
bm_pj.free()
for p in m_pj.polygons:
    p.use_smooth = True
mod_sub_pj = o_pj.modifiers.new("Subdivision", 'SUBSURF')
mod_sub_pj.levels = 1
mod_sol_pj = o_pj.modifiers.new("Solidify", 'SOLIDIFY')
mod_sol_pj.thickness = 0.004

# ---------------------------------------------------------------------------
# 9. Handcrafted Punjabi Leather Juttis (Curled Nok Toe, Hard Sole Welt)
# ---------------------------------------------------------------------------
o_jutti, m_jutti = create_piece("Kabir_Juttis", mat_leather)
bm_j = bmesh.new()

for side, sign in [("L", 1), ("R", -1)]:
    jx = sign * 0.095
    # Stitched Sole Welt
    bmesh.ops.create_cube(bm_j, size=1.0, matrix=Matrix.Translation(Vector((jx, 0.022, 0.014))) @ Matrix.Diagonal((0.068, 0.19, 0.018, 1.0)))
    
    # Leather Upper
    jutti_rings = [
        (Vector((jx, -0.05, 0.040)), 0.034, 0.022),
        (Vector((jx, 0.00, 0.044)),  0.040, 0.026),
        (Vector((jx, 0.05, 0.038)),  0.038, 0.024),
        (Vector((jx, 0.10, 0.032)),  0.028, 0.016),
    ]
    prev_jr = []
    for center, rx, rz in jutti_rings:
        curr_jr = []
        for i in range(12):
            ang = 2 * math.pi * i / 12
            vx = center.x + rx * math.sin(ang)
            vy = center.y
            vz = center.z + rz * math.cos(ang)
            v = bm_j.verts.new(Vector((vx, vy, vz)))
            curr_jr.append(v)
        if prev_jr:
            for i in range(12):
                ni = (i + 1) % 12
                bm_j.faces.new([prev_jr[i], prev_jr[ni], curr_jr[ni], curr_jr[i]])
        prev_jr = curr_jr
        
    # Curled Nok Toe Tip
    nok_tip = bm_j.verts.new(Vector((jx, 0.145, 0.068)))
    for i in range(12):
        ni = (i + 1) % 12
        bm_j.faces.new([curr_jr[i], curr_jr[ni], nok_tip])

bm_j.to_mesh(m_jutti)
bm_j.free()
for p in m_jutti.polygons:
    p.use_smooth = True
mod_sub_j = o_jutti.modifiers.new("Subdivision", 'SUBSURF')
mod_sub_j.levels = 1

# ---------------------------------------------------------------------------
# 10. Crossbody Leather Satchel & Hardware (Brass Buckle, Chalk Pouch)
# ---------------------------------------------------------------------------
o_satchel, m_satchel = create_piece("Kabir_Satchel", mat_leather)
bm_s = bmesh.new()

# Messenger bag body (Left hip)
bmesh.ops.create_cube(bm_s, size=1.0, matrix=Matrix.Translation(Vector((-0.165, 0.022, 0.68))) @ Matrix.Diagonal((0.078, 0.22, 0.17, 1.0)))
# Closing flap
bmesh.ops.create_cube(bm_s, size=1.0, matrix=Matrix.Translation(Vector((-0.168, 0.078, 0.695))) @ Matrix.Diagonal((0.082, 0.012, 0.13, 1.0)))

# Crossbody strap (Right shoulder across chest to left hip)
strap_pts = [
    Vector((0.15, 0.02, 1.10)),
    Vector((0.09, 0.08, 1.02)),
    Vector((0.00, 0.092, 0.92)),
    Vector((-0.09, 0.082, 0.80)),
    Vector((-0.16, 0.035, 0.72)),
]
prev_st = []
for pt in strap_pts:
    v1 = bm_s.verts.new(pt + Vector((-0.010, 0.004, 0.006)))
    v2 = bm_s.verts.new(pt + Vector((0.010, -0.004, -0.006)))
    curr_st = [v1, v2]
    if prev_st:
        bm_s.faces.new([prev_st[0], prev_st[1], curr_st[1], curr_st[0]])
    prev_st = curr_st

bm_s.to_mesh(m_satchel)
bm_s.free()
for p in m_satchel.polygons:
    p.use_smooth = True
mod_sol_s = o_satchel.modifiers.new("Solidify", 'SOLIDIFY')
mod_sol_s.thickness = 0.004

# Tarnished Brass Buckle
o_bkl, m_bkl = create_piece("Kabir_Satchel_Buckle", mat_brass)
bm_bkl = bmesh.new()
bmesh.ops.create_cone(bm_bkl, cap_ends=True, segments=14, radius1=0.022, radius2=0.022, depth=0.008, matrix=Matrix.Translation(Vector((-0.168, 0.088, 0.635))) @ Matrix.Rotation(math.radians(90.0), 4, 'Y'))
bm_bkl.to_mesh(m_bkl)
bm_bkl.free()
for p in m_bkl.polygons:
    p.use_smooth = True

# Waist Pouch & Soapstone Tailor's Chalk Stick (Right hip)
o_pch, m_pch = create_piece("Kabir_Chalk_Pouch", mat_kurta)
bm_pch = bmesh.new()
bmesh.ops.create_uvsphere(bm_pch, u_segments=12, v_segments=10, radius=0.038, matrix=Matrix.Translation(Vector((0.145, 0.02, 0.70))) @ Matrix.Diagonal((0.7, 1.0, 1.2, 1.0)))
bm_pch.to_mesh(m_pch)
bm_pch.free()
for p in m_pch.polygons:
    p.use_smooth = True

o_chk, m_chk = create_piece("Kabir_Chalk_Stick", mat_chalk)
bm_chk = bmesh.new()
bmesh.ops.create_cube(bm_chk, size=1.0, matrix=Matrix.Translation(Vector((0.145, 0.02, 0.76))) @ Matrix.Diagonal((0.016, 0.028, 0.048, 1.0)))
bm_chk.to_mesh(m_chk)
bm_chk.free()

print("[AAA_KABIR] Complete 1919 historical wardrobe and accessories assembled.")

# ---------------------------------------------------------------------------
# 11. Studio Lighting & Showcase Cameras
# ---------------------------------------------------------------------------
# Warm Punjabi Sun Key Light
l_key = bpy.data.lights.new("Sun_Key_AAA", 'POINT')
l_key.energy = 750.0
l_key.color = (1.0, 0.94, 0.82)
o_lkey = bpy.data.objects.new("Sun_Key_AAA", l_key)
o_lkey.location = (-1.2, 2.2, 2.0)
bpy.context.collection.objects.link(o_lkey)

# Cool Sky Rim Light
l_rim = bpy.data.lights.new("Sky_Rim_AAA", 'POINT')
l_rim.energy = 480.0
l_rim.color = (0.75, 0.85, 1.0)
o_lrim = bpy.data.objects.new("Sky_Rim_AAA", l_rim)
o_lrim.location = (1.4, -1.8, 1.8)
bpy.context.collection.objects.link(o_lrim)

# Diffuse Ambient Fill Light
l_fill = bpy.data.lights.new("Fill_Light_AAA", 'POINT')
l_fill.energy = 260.0
l_fill.color = (0.95, 0.90, 0.85)
o_lfill = bpy.data.objects.new("Fill_Light_AAA", l_fill)
o_lfill.location = (1.1, 1.6, 1.0)
bpy.context.collection.objects.link(o_lfill)

# Hero Full-Body Three-Quarter Camera
cam_hero_data = bpy.data.cameras.new("Cam_Hero_FullBody")
cam_hero_data.lens = 52.0
cam_hero_obj = bpy.data.objects.new("Cam_Hero_FullBody", cam_hero_data)
cam_hero_obj.location = (-0.55, 2.35, 0.95)
cam_hero_obj.rotation_euler = (math.radians(88.0), 0.0, math.radians(-168.0))
bpy.context.collection.objects.link(cam_hero_obj)
bpy.context.scene.camera = cam_hero_obj

# Close-up Portrait Camera (Head, Face & Saffron Patka)
cam_port_data = bpy.data.cameras.new("Cam_Portrait_Face")
cam_port_data.lens = 85.0
cam_port_obj = bpy.data.objects.new("Cam_Portrait_Face", cam_port_data)
cam_port_obj.location = (-0.18, 1.05, 1.30)
cam_port_obj.rotation_euler = (math.radians(88.0), 0.0, math.radians(-172.0))
bpy.context.collection.objects.link(cam_port_obj)

# Render settings
bpy.context.scene.render.resolution_x = 1280
bpy.context.scene.render.resolution_y = 960
bpy.context.scene.render.image_settings.file_format = 'PNG'

# ---------------------------------------------------------------------------
# 12. Save & Export to Both Designated Folders
# ---------------------------------------------------------------------------
art_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\PROJECT"
dest_dir = r"C:\Users\npal7\PROJECT\PROJECT"
os.makedirs(art_dir, exist_ok=True)
os.makedirs(dest_dir, exist_ok=True)

# Save .blend mainfiles
blend_art = os.path.join(art_dir, "Kabir_Protagonist_AAA.blend")
blend_dest = os.path.join(dest_dir, "Kabir_Protagonist_AAA.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_art)
bpy.ops.wm.save_as_mainfile(filepath=blend_dest)

# Export rigged FBX
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
bpy.context.scene.camera = cam_hero_obj
bpy.context.scene.render.filepath = render_hero_art
bpy.ops.render.render(write_still=True)

import shutil
shutil.copyfile(render_hero_art, render_hero_dest)

# Render Portrait Still
render_port_art = os.path.join(art_dir, "Kabir_Protagonist_AAA_Portrait.png")
render_port_dest = os.path.join(dest_dir, "Kabir_Protagonist_AAA_Portrait.png")
bpy.context.scene.camera = cam_port_obj
bpy.context.scene.render.filepath = render_port_art
bpy.ops.render.render(write_still=True)
shutil.copyfile(render_port_art, render_port_dest)

print(f"[AAA_KABIR] SUCCESS! Saved blend files to {blend_art} & {blend_dest}")
print(f"[AAA_KABIR] SUCCESS! Exported FBX to {fbx_art} & {fbx_dest}")
print(f"[AAA_KABIR] SUCCESS! Renders saved to {render_hero_art} & {render_port_art}")
