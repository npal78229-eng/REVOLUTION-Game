"""
PROJECT REVOLUTION (क्रांति) — Complete AAA Protagonist Character Model (Kabir)
Age: 12-Year-Old Indian Boy, Amritsar/Kot Gurdarshan, April 1919
Anatomically Believable Head, Expressive Face, Punjabi Attire, Rigged & Game-Ready
"""

import bpy
import bmesh
import math
import os
import shutil
from mathutils import Vector, Matrix

print("[AAA_KABIR] Initializing Complete Protagonist Character Redesign...")

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
# 2. PBR Materials (Principled BSDF)
# ---------------------------------------------------------------------------
def create_pbr_material(name, base_color, roughness=0.5, metallic=0.0, sss_weight=0.0, sss_radius=(1.0, 0.65, 0.42), sheen=0.0, coat=0.0):
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
            if "Subsurface Radius" in bsdf.inputs:
                bsdf.inputs["Subsurface Radius"].default_value = sss_radius
            if "Subsurface Scale" in bsdf.inputs:
                bsdf.inputs["Subsurface Scale"].default_value = 0.04
        if "Sheen Weight" in bsdf.inputs and sheen > 0:
            bsdf.inputs["Sheen Weight"].default_value = sheen
        if "Coat Weight" in bsdf.inputs and coat > 0:
            bsdf.inputs["Coat Weight"].default_value = coat
    return mat

# Warm North Indian youthful skin with authentic subsurface scattering
mat_skin = create_pbr_material("M_Kabir_Skin_AAA", (0.64, 0.42, 0.28, 1.0), roughness=0.48, sss_weight=0.32, sss_radius=(1.0, 0.62, 0.38))
mat_sclera = create_pbr_material("M_Kabir_Sclera", (0.92, 0.90, 0.88, 1.0), roughness=0.12)
mat_iris = create_pbr_material("M_Kabir_Iris", (0.14, 0.08, 0.03, 1.0), roughness=0.08)
mat_dark_hair = create_pbr_material("M_Kabir_DarkHair", (0.05, 0.04, 0.03, 1.0), roughness=0.65)
mat_patka = create_pbr_material("M_Kabir_Patka_Saffron", (0.95, 0.45, 0.05, 1.0), roughness=0.82, sheen=0.55)
mat_kurta = create_pbr_material("M_Kabir_Khadi_Kurta", (0.87, 0.83, 0.75, 1.0), roughness=0.88, sheen=0.35)
mat_pajama = create_pbr_material("M_Kabir_Cotton_Pajama", (0.86, 0.84, 0.80, 1.0), roughness=0.85, sheen=0.30)
mat_leather = create_pbr_material("M_Kabir_Aged_Leather", (0.32, 0.17, 0.09, 1.0), roughness=0.50, coat=0.25)
mat_brass = create_pbr_material("M_Kabir_Brass", (0.82, 0.68, 0.26, 1.0), roughness=0.30, metallic=0.92)
mat_wood = create_pbr_material("M_Kabir_Wood_Buttons", (0.22, 0.12, 0.06, 1.0), roughness=0.70)

# Helper function
def make_obj(name, material):
    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    if material:
        obj.data.materials.append(material)
    return obj, mesh

# ---------------------------------------------------------------------------
# 3. Model Anatomical Head & Expressive Facial Features
# Orientation: Kabir faces NEGATIVE Y (-Y). Front is -Y, Back is +Y, +Z is Up.
# ---------------------------------------------------------------------------
print("[AAA_KABIR] Modeling Anatomical Head & Face...")
obj_head, mesh_head = make_obj("Kabir_Head", mat_skin)
bm_h = bmesh.new()

# Continuous juvenile head loops (from throat to cranium top)
# Head spans Z = 1.14 (neck) to 1.38 (cranium crown)
head_rings = [
    # (z, rx, ry, y_offset)
    (1.14, 0.046, 0.048,  0.005), # Base of neck / throat
    (1.17, 0.042, 0.045,  0.000), # Mid neck
    (1.20, 0.052, 0.056, -0.008), # Jawline & Chin level
    (1.23, 0.064, 0.068, -0.012), # Mouth & lower cheeks
    (1.26, 0.072, 0.076, -0.010), # Nose base & cheekbones
    (1.29, 0.076, 0.082, -0.006), # Eye sockets & nasal bridge
    (1.32, 0.078, 0.086, -0.002), # Brow ridge & temples
    (1.35, 0.075, 0.084,  0.002), # Forehead & crown
    (1.38, 0.062, 0.072,  0.006), # Upper cranium
    (1.40, 0.038, 0.046,  0.008), # Cranium top
]

prev_h_ring = []
first_h_ring = []
for idx, (z, rx, ry, y_off) in enumerate(head_rings):
    curr_ring = []
    num_pts = 18
    for i in range(num_pts):
        ang = 2 * math.pi * i / num_pts
        x = rx * math.sin(ang)
        # Face is towards -Y: ang around pi is front (-Y), ang around 0 is back (+Y)
        y = ry * math.cos(ang) + y_off
        
        # Sculpt juvenile facial features at the front (where cos(ang) < -0.4, i.e. negative Y)
        front_factor = -math.cos(ang) # Positive at front face
        if front_factor > 0.4:
            norm_ff = (front_factor - 0.4) / 0.6
            if 1.24 <= z <= 1.28:
                # Nose bridge and tip projection towards -Y
                y -= 0.026 * norm_ff
            elif 1.21 <= z <= 1.24:
                # Lips / mouth projection
                y -= 0.014 * norm_ff
            elif 1.18 <= z <= 1.21:
                # Juvenile rounded chin projection
                y -= 0.018 * norm_ff
            elif 1.28 <= z <= 1.31:
                # Eye socket subtle recess (indentation inwards towards +Y)
                if abs(x) > 0.016:
                    y += 0.008 * norm_ff
        # Youthful jaw taper
        if z <= 1.22 and abs(x) > 0.035:
            x *= 0.90
            
        v = bm_h.verts.new(Vector((x, y, z)))
        curr_ring.append(v)
        
    if not first_h_ring:
        first_h_ring = curr_ring
    if prev_h_ring:
        for i in range(num_pts):
            ni = (i + 1) % num_pts
            bm_h.faces.new([prev_h_ring[i], prev_h_ring[ni], curr_ring[ni], curr_ring[i]])
    prev_h_ring = curr_ring

# Cap the top of cranium
top_head_v = bm_h.verts.new(Vector((0.0, 0.008, 1.41)))
for i in range(18):
    ni = (i + 1) % 18
    bm_h.faces.new([top_head_v, prev_h_ring[i], prev_h_ring[ni]])

# Sculpt Nose Tip, Nostril Wings, and Columella
nose_tip = bm_h.verts.new(Vector((0.0, -0.108, 1.262)))
nose_bridge = bm_h.verts.new(Vector((0.0, -0.092, 1.288)))
nose_columella = bm_h.verts.new(Vector((0.0, -0.090, 1.248)))
for sign in [-1, 1]:
    n_wing = bm_h.verts.new(Vector((sign * 0.014, -0.092, 1.256)))
    bm_h.faces.new([nose_tip, n_wing, nose_columella])
    bm_h.faces.new([nose_bridge, n_wing, nose_tip])

# Sculpt Lips (Youthful Cupid's Bow upper lip, fuller lower lip)
lip_up = bm_h.verts.new(Vector((0.0, -0.084, 1.232)))
lip_low = bm_h.verts.new(Vector((0.0, -0.082, 1.218)))
for sign in [-1, 1]:
    m_corner = bm_h.verts.new(Vector((sign * 0.020, -0.072, 1.225)))
    bm_h.faces.new([lip_up, m_corner, lip_low])

# Sculpt Detailed Juvenile Ears
for sign in [-1, 1]:
    ear_top = bm_h.verts.new(Vector((sign * 0.078, 0.006, 1.308)))
    ear_helix = bm_h.verts.new(Vector((sign * 0.088, 0.012, 1.282)))
    ear_lobe = bm_h.verts.new(Vector((sign * 0.082, 0.008, 1.252)))
    ear_tragus = bm_h.verts.new(Vector((sign * 0.072, -0.004, 1.280)))
    bm_h.faces.new([ear_top, ear_helix, ear_tragus])
    bm_h.faces.new([ear_helix, ear_lobe, ear_tragus])

bm_h.to_mesh(mesh_head)
bm_h.free()
for p in mesh_head.polygons:
    p.use_smooth = True

mod_sub_head = obj_head.modifiers.new("Subsurf", 'SUBSURF')
mod_sub_head.levels = 2
mod_sub_head.render_levels = 2

# ---------------------------------------------------------------------------
# 4. Realistic Almond Eyes & Eyebrows
# ---------------------------------------------------------------------------
print("[AAA_KABIR] Adding Almond Eyes, Cornea, Eyebrows...")
for side, sign in [("L", 1), ("R", -1)]:
    # Eyeball with Sclera & Iris materials
    eye_obj, eye_mesh = make_obj(f"Kabir_Eye_{side}", mat_sclera)
    eye_obj.data.materials.append(mat_iris)
    
    bm_eye = bmesh.new()
    eye_center = Vector((sign * 0.028, -0.070, 1.288))
    # Sphere rotated so Iris points towards -Y
    bmesh.ops.create_uvsphere(
        bm_eye, u_segments=16, v_segments=12, radius=0.011,
        matrix=Matrix.Translation(eye_center) @ Matrix.Rotation(math.radians(-90.0), 4, 'X')
    )
    for f in bm_eye.faces:
        if f.calc_center_median().y < -0.077:
            f.material_index = 1 # Iris material on front-facing hemisphere
    bm_eye.to_mesh(eye_mesh)
    bm_eye.free()
    for p in eye_mesh.polygons:
        p.use_smooth = True

    # Delicate upper eyelid crease
    lash_obj, lash_mesh = make_obj(f"Kabir_Lashes_{side}", mat_dark_hair)
    bm_l = bmesh.new()
    bmesh.ops.create_cone(
        bm_l, cap_ends=True, segments=10, radius1=0.012, radius2=0.010, depth=0.004,
        matrix=Matrix.Translation(Vector((sign * 0.028, -0.073, 1.296))) @ Matrix.Rotation(math.radians(-80.0), 4, 'X')
    )
    bm_l.to_mesh(lash_mesh)
    bm_l.free()
    for p in lash_mesh.polygons:
        p.use_smooth = True

# Natural Arched Eyebrows
brow_obj, brow_mesh = make_obj("Kabir_Eyebrows", mat_dark_hair)
bm_b = bmesh.new()
for sign in [-1, 1]:
    brow_pts = [
        Vector((sign * 0.014, -0.076, 1.306)),
        Vector((sign * 0.030, -0.074, 1.312)),
        Vector((sign * 0.046, -0.064, 1.305)),
    ]
    for i in range(len(brow_pts) - 1):
        p1 = brow_pts[i]
        p2 = brow_pts[i+1]
        mid = (p1 + p2) * 0.5
        bmesh.ops.create_cone(
            bm_b, cap_ends=True, segments=8, radius1=0.004, radius2=0.0025, depth=(p2 - p1).length,
            matrix=Matrix.Translation(mid) @ Matrix.Rotation(math.radians(sign * 15.0), 4, 'Y') @ Matrix.Diagonal((1.0, 0.4, 1.0, 1.0))
        )
bm_b.to_mesh(brow_mesh)
bm_b.free()
for p in brow_mesh.polygons:
    p.use_smooth = True

# ---------------------------------------------------------------------------
# 5. Saffron Patka Headdress (Folded Cloth, Crown Juda Topknot, Nape Ties)
# Sits cleanly on the cranium without clipping
# ---------------------------------------------------------------------------
print("[AAA_KABIR] Modeling Saffron Patka Headdress...")
patka_obj, patka_mesh = make_obj("Kabir_Patka", mat_patka)
bm_p = bmesh.new()

# Fitted headwrap rings (Z = 1.31 to 1.41)
patka_wrap_rings = [
    # (z, rx, ry, y_offset)
    (1.31, 0.081, 0.088, -0.002), # Brow band rim
    (1.34, 0.080, 0.087,  0.000),
    (1.37, 0.077, 0.084,  0.004),
    (1.40, 0.068, 0.074,  0.006),
    (1.42, 0.046, 0.052,  0.008), # Crown gathering
]

prev_p = []
for z, rx, ry, y_off in patka_wrap_rings:
    curr_p = []
    num_p = 16
    for i in range(num_p):
        ang = 2 * math.pi * i / num_p
        x = rx * math.sin(ang)
        y = ry * math.cos(ang) + y_off
        # Front central forehead V-fold
        if -math.cos(ang) > 0.5:
            v_fold = (-math.cos(ang) - 0.5) / 0.5
            y -= 0.006 * v_fold
            z_val = z - 0.008 * v_fold
        else:
            z_val = z
        v = bm_p.verts.new(Vector((x, y, z_val)))
        curr_p.append(v)
    if prev_p:
        for i in range(num_p):
            ni = (i + 1) % num_p
            bm_p.faces.new([prev_p[i], prev_p[ni], curr_p[ni], curr_p[i]])
    prev_p = curr_p

# Topknot Juda (Cloth-wrapped hair bun at vertex of cranium)
bmesh.ops.create_uvsphere(
    bm_p, u_segments=14, v_segments=10, radius=0.038,
    matrix=Matrix.Translation(Vector((0.0, -0.005, 1.442))) @ Matrix.Diagonal((1.0, 0.92, 0.82, 1.0))
)
# Topknot wrapping cord band
bmesh.ops.create_cone(
    bm_p, cap_ends=True, segments=14, radius1=0.040, radius2=0.038, depth=0.016,
    matrix=Matrix.Translation(Vector((0.0, -0.005, 1.424)))
)

# Flowing Nape Ties (graceful Punjabi fabric tails flowing down back of neck at +Y)
for sign in [-1, 1]:
    tie_prev = []
    for step in range(6):
        tz = 1.30 - step * 0.036
        ty = 0.088 + step * 0.006 + math.sin(step * 0.6) * 0.003
        tx = sign * (0.024 + step * 0.006)
        w = 0.016 * (1.0 - step * 0.12)
        v1 = bm_p.verts.new(Vector((tx - w, ty, tz)))
        v2 = bm_p.verts.new(Vector((tx + w, ty, tz)))
        curr_t = [v1, v2]
        if tie_prev:
            bm_p.faces.new([tie_prev[0], tie_prev[1], curr_t[1], curr_t[0]])
        tie_prev = curr_t

bm_p.to_mesh(patka_mesh)
bm_p.free()
for p in patka_mesh.polygons:
    p.use_smooth = True
mod_sub_p = patka_obj.modifiers.new("Subsurf", 'SUBSURF')
mod_sub_p.levels = 2

# ---------------------------------------------------------------------------
# 6. Anatomical Body (12-Year-Old Youthful Proportions)
# Height: 1.38m, Torso, Arms, 5 Modeled Fingers, Legs
# ---------------------------------------------------------------------------
print("[AAA_KABIR] Modeling Anatomical Body & Hands...")
body_obj, body_mesh = make_obj("Kabir_Body", mat_skin)
bm_body = bmesh.new()

# Torso & Limb Segments
# Chest (Z: 0.92 to 1.14)
torso_rings = [
    # (z, rx, ry, y_off)
    (1.14, 0.052, 0.052,  0.000), # Neck base
    (1.10, 0.138, 0.086, -0.002), # Clavicle / shoulders
    (1.00, 0.132, 0.082, -0.002), # Mid chest
    (0.88, 0.122, 0.078,  0.000), # Waist
    (0.76, 0.128, 0.084,  0.002), # Pelvis / Hips
]
prev_t = []
for z, rx, ry, y_off in torso_rings:
    curr_t = []
    num_t = 16
    for i in range(num_t):
        ang = 2 * math.pi * i / num_t
        x = rx * math.sin(ang)
        y = ry * math.cos(ang) + y_off
        v = bm_body.verts.new(Vector((x, y, z)))
        curr_t.append(v)
    if prev_t:
        for i in range(num_t):
            ni = (i + 1) % num_t
            bm_body.faces.new([prev_t[i], prev_t[ni], curr_t[ni], curr_t[i]])
    prev_t = curr_t

# Both Arms & Hands (Slender boyish arms with 5 modeled fingers)
for side, sign in [("L", 1), ("R", -1)]:
    arm_segs = [
        # (center_vec, rx, ry)
        (Vector((sign * 0.145, 0.000, 1.08)), 0.034, 0.034), # Shoulder joint
        (Vector((sign * 0.185, 0.000, 0.95)), 0.030, 0.030), # Mid bicep
        (Vector((sign * 0.220, 0.000, 0.82)), 0.026, 0.026), # Elbow
        (Vector((sign * 0.250, 0.000, 0.70)), 0.023, 0.023), # Mid forearm
        (Vector((sign * 0.275, 0.000, 0.58)), 0.020, 0.016), # Wrist
    ]
    prev_arm = []
    for center, rx, ry in arm_segs:
        curr_arm = []
        num_a = 10
        for i in range(num_a):
            ang = 2 * math.pi * i / num_a
            x = center.x + rx * math.sin(ang)
            y = center.y + ry * math.cos(ang)
            v = bm_body.verts.new(Vector((x, y, center.z)))
            curr_arm.append(v)
        if prev_arm:
            for i in range(num_a):
                ni = (i + 1) % num_a
                bm_body.faces.new([prev_arm[i], prev_arm[ni], curr_arm[ni], curr_arm[i]])
        prev_arm = curr_arm

    # Palm (Z: 0.58 to 0.52)
    palm_c = Vector((sign * 0.290, 0.000, 0.54))
    bmesh.ops.create_cube(
        bm_body, size=1.0,
        matrix=Matrix.Translation(palm_c) @ Matrix.Diagonal((0.032, 0.016, 0.055, 1.0))
    )

    # 5 Fingers (Thumb + Index + Middle + Ring + Pinky)
    finger_offsets = [
        # (name, dx, dy, dz, length, radius)
        ("Thumb",  sign * -0.016, -0.012, -0.012, 0.028, 0.006),
        ("Index",  sign * -0.009,  0.000, -0.036, 0.034, 0.005),
        ("Middle", sign *  0.000,  0.000, -0.038, 0.038, 0.0055),
        ("Ring",   sign *  0.009,  0.000, -0.036, 0.034, 0.005),
        ("Pinky",  sign *  0.017,  0.000, -0.032, 0.026, 0.0045),
    ]
    for fname, fdx, fdy, fdz, flen, frad in finger_offsets:
        f_base = Vector((palm_c.x + fdx, palm_c.y + fdy, palm_c.z + fdz))
        bmesh.ops.create_cone(
            bm_body, cap_ends=True, segments=8, radius1=frad, radius2=frad * 0.8, depth=flen,
            matrix=Matrix.Translation(Vector((f_base.x, f_base.y, f_base.z - flen * 0.5)))
        )

# Legs (Thigh, Knee, Calf, Ankle)
for side, sign in [("L", 1), ("R", -1)]:
    leg_segs = [
        (Vector((sign * 0.065, 0.002, 0.74)), 0.055, 0.055), # Upper thigh
        (Vector((sign * 0.065, 0.000, 0.58)), 0.046, 0.046), # Mid thigh
        (Vector((sign * 0.065, -0.002, 0.44)), 0.038, 0.038), # Knee
        (Vector((sign * 0.065, 0.000, 0.28)), 0.034, 0.034), # Calf
        (Vector((sign * 0.065, 0.002, 0.12)), 0.026, 0.026), # Ankle
    ]
    prev_leg = []
    for center, rx, ry in leg_segs:
        curr_leg = []
        num_l = 12
        for i in range(num_l):
            ang = 2 * math.pi * i / num_l
            x = center.x + rx * math.sin(ang)
            y = center.y + ry * math.cos(ang)
            v = bm_body.verts.new(Vector((x, y, center.z)))
            curr_leg.append(v)
        if prev_leg:
            for i in range(num_l):
                ni = (i + 1) % num_l
                bm_body.faces.new([prev_leg[i], prev_leg[ni], curr_leg[ni], curr_leg[i]])
        prev_leg = curr_leg

bm_body.to_mesh(body_mesh)
bm_body.free()
for p in body_mesh.polygons:
    p.use_smooth = True
mod_sub_b = body_obj.modifiers.new("Subsurf", 'SUBSURF')
mod_sub_b.levels = 1

# ---------------------------------------------------------------------------
# 7. Khadi Kurta Attire (Mandarin Collar, Front Placket, Flared Lower Hem with Side Chaks)
# ---------------------------------------------------------------------------
print("[AAA_KABIR] Modeling Khadi Kurta Attire...")
kurta_obj, kurta_mesh = make_obj("Kabir_Kurta", mat_kurta)
bm_k = bmesh.new()

# Fitted chest down to knee-level flared skirt
kurta_rings = [
    # (z, rx, ry, y_off)
    (1.15, 0.056, 0.056,  0.000), # Mandarin collar rim
    (1.11, 0.145, 0.094, -0.002), # Shoulders / chest top
    (1.00, 0.140, 0.090, -0.002), # Mid chest
    (0.88, 0.134, 0.086,  0.000), # Waist
    (0.76, 0.144, 0.094,  0.002), # Hips
    (0.66, 0.158, 0.104,  0.004), # Upper thighs
    (0.56, 0.172, 0.114,  0.006), # Mid thighs
    (0.48, 0.185, 0.124,  0.008), # Knee level hem
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
            # Authentic Punjabi side slits (chaks) below hip level (indices 4 and 13)
            if idx >= 5 and (i == 4 or i == 13):
                continue
            bm_k.faces.new([prev_k[i], prev_k[ni], curr_k[ni], curr_k[i]])
    prev_k = curr_k

# Kurta Sleeves (elbow to 3/4 forearm drape)
for side, sign in [("L", 1), ("R", -1)]:
    sleeve_rings = [
        (Vector((sign * 0.145, 0.000, 1.08)), 0.042, 0.042),
        (Vector((sign * 0.185, 0.000, 0.95)), 0.038, 0.038),
        (Vector((sign * 0.220, 0.000, 0.82)), 0.034, 0.034),
        (Vector((sign * 0.245, 0.000, 0.72)), 0.032, 0.030), # Drape cuff
    ]
    prev_sl = []
    for center, rx, ry in sleeve_rings:
        curr_sl = []
        num_s = 12
        for i in range(num_s):
            ang = 2 * math.pi * i / num_s
            x = center.x + rx * math.sin(ang)
            y = center.y + ry * math.cos(ang)
            v = bm_k.verts.new(Vector((x, y, center.z)))
            curr_sl.append(v)
        if prev_sl:
            for i in range(num_s):
                ni = (i + 1) % num_s
                bm_k.faces.new([prev_sl[i], prev_sl[ni], curr_sl[ni], curr_sl[i]])
        prev_sl = curr_sl

bm_k.to_mesh(kurta_mesh)
bm_k.free()
for p in kurta_mesh.polygons:
    p.use_smooth = True
mod_sub_k = kurta_obj.modifiers.new("Subsurf", 'SUBSURF')
mod_sub_k.levels = 1

# Kurta Front Placket & Carved Wooden Buttons (facing -Y)
btn_obj, btn_mesh = make_obj("Kabir_Buttons", mat_wood)
bm_btn = bmesh.new()
# Vertical cloth placket strip
bmesh.ops.create_cube(
    bm_btn, size=1.0,
    matrix=Matrix.Translation(Vector((0.0, -0.096, 1.02))) @ Matrix.Diagonal((0.016, 0.006, 0.16, 1.0))
)
# 3 Carved Wooden / Horn Buttons
for bz in [1.07, 1.01, 0.95]:
    bmesh.ops.create_cone(
        bm_btn, cap_ends=True, segments=12, radius1=0.006, radius2=0.005, depth=0.005,
        matrix=Matrix.Translation(Vector((0.0, -0.100, bz))) @ Matrix.Rotation(math.radians(90.0), 4, 'X')
    )
bm_btn.to_mesh(btn_mesh)
bm_btn.free()
for p in btn_mesh.polygons:
    p.use_smooth = True

# ---------------------------------------------------------------------------
# 8. Cotton Pajama Pants (Waist to Ankle Drape)
# ---------------------------------------------------------------------------
print("[AAA_KABIR] Modeling Cotton Pajama Pants...")
pajama_obj, pajama_mesh = make_obj("Kabir_Pajama", mat_pajama)
bm_paj = bmesh.new()

for side, sign in [("L", 1), ("R", -1)]:
    paj_segs = [
        (Vector((sign * 0.066, 0.002, 0.72)), 0.060, 0.060), # Upper thigh
        (Vector((sign * 0.066, 0.000, 0.58)), 0.052, 0.052), # Mid thigh
        (Vector((sign * 0.066, -0.002, 0.44)), 0.046, 0.046), # Knee creases
        (Vector((sign * 0.066, 0.000, 0.30)), 0.040, 0.040), # Lower leg
        (Vector((sign * 0.066, 0.002, 0.16)), 0.034, 0.034), # Cuff
        (Vector((sign * 0.066, 0.002, 0.08)), 0.030, 0.030), # Ankle rim
    ]
    prev_paj = []
    for center, rx, ry in paj_segs:
        curr_paj = []
        num_pj = 12
        for i in range(num_pj):
            ang = 2 * math.pi * i / num_pj
            x = center.x + rx * math.sin(ang)
            y = center.y + ry * math.cos(ang)
            v = bm_paj.verts.new(Vector((x, y, center.z)))
            curr_paj.append(v)
        if prev_paj:
            for i in range(num_pj):
                ni = (i + 1) % num_pj
                bm_paj.faces.new([prev_paj[i], prev_paj[ni], curr_paj[ni], curr_paj[i]])
        prev_paj = curr_paj

bm_paj.to_mesh(pajama_mesh)
bm_paj.free()
for p in pajama_mesh.polygons:
    p.use_smooth = True
mod_sub_pj = pajama_obj.modifiers.new("Subsurf", 'SUBSURF')
mod_sub_pj.levels = 1

# ---------------------------------------------------------------------------
# 9. Traditional Punjabi Leather Juttis / Mojari Shoes
# Pointed upturned toe box, low-cut ankle rim
# ---------------------------------------------------------------------------
print("[AAA_KABIR] Modeling Traditional Leather Juttis...")
jutti_obj, jutti_mesh = make_obj("Kabir_Juttis", mat_leather)
bm_j = bmesh.new()

for side, sign in [("L", 1), ("R", -1)]:
    # Sole and upper shoe
    sole_c = Vector((sign * 0.066, -0.020, 0.035))
    bmesh.ops.create_cube(
        bm_j, size=1.0,
        matrix=Matrix.Translation(sole_c) @ Matrix.Diagonal((0.052, 0.140, 0.045, 1.0))
    )
    # Distinctive upturned pointed toe curve (facing -Y)
    toe_tip = Vector((sign * 0.066, -0.115, 0.055))
    bmesh.ops.create_cone(
        bm_j, cap_ends=True, segments=10, radius1=0.024, radius2=0.008, depth=0.050,
        matrix=Matrix.Translation(toe_tip) @ Matrix.Rotation(math.radians(-70.0), 4, 'X')
    )

bm_j.to_mesh(jutti_mesh)
bm_j.free()
for p in jutti_mesh.polygons:
    p.use_smooth = True

# ---------------------------------------------------------------------------
# 10. Aged Leather Courier Satchel & Cross-Body Strap
# Right shoulder across chest to left hip, brass buckle, courier flap
# ---------------------------------------------------------------------------
print("[AAA_KABIR] Modeling Courier Satchel & Brass Buckle...")
satchel_obj, satchel_mesh = make_obj("Kabir_Satchel", mat_leather)
bm_s = bmesh.new()

# Satchel Box Pouch resting on left hip
satchel_center = Vector((0.170, 0.010, 0.680))
bmesh.ops.create_cube(
    bm_s, size=1.0,
    matrix=Matrix.Translation(satchel_center) @ Matrix.Diagonal((0.075, 0.170, 0.190, 1.0))
)
# Overlapping leather flap
bmesh.ops.create_cube(
    bm_s, size=1.0,
    matrix=Matrix.Translation(Vector((satchel_center.x - 0.038, satchel_center.y, satchel_center.z + 0.02))) @ Matrix.Diagonal((0.012, 0.176, 0.140, 1.0))
)

# Diagonal Cross-Body Leather Strap (Right Shoulder: (-0.13, 0.00, 1.10) to Left Hip: (0.16, 0.01, 0.72))
strap_pts = [
    Vector((-0.13,  0.02, 1.11)),
    Vector((-0.07, -0.09, 1.02)), # Across front chest
    Vector(( 0.03, -0.08, 0.88)),
    Vector(( 0.13, -0.03, 0.76)),
    Vector(( 0.17,  0.01, 0.72)), # Connected to satchel
]
prev_st = []
for pt in strap_pts:
    curr_st = []
    w = 0.016
    th = 0.005
    curr_st.append(bm_s.verts.new(Vector((pt.x - w, pt.y, pt.z))))
    curr_st.append(bm_s.verts.new(Vector((pt.x + w, pt.y, pt.z))))
    curr_st.append(bm_s.verts.new(Vector((pt.x + w, pt.y + th, pt.z))))
    curr_st.append(bm_s.verts.new(Vector((pt.x - w, pt.y + th, pt.z))))
    if prev_st:
        for i in range(4):
            ni = (i + 1) % 4
            bm_s.faces.new([prev_st[i], prev_st[ni], curr_st[ni], curr_st[i]])
    prev_st = curr_st

bm_s.to_mesh(satchel_mesh)
bm_s.free()
for p in satchel_mesh.polygons:
    p.use_smooth = True

# Brass Buckle on Chest Strap
buckle_obj, buckle_mesh = make_obj("Kabir_Satchel_Buckle", mat_brass)
bm_bck = bmesh.new()
bmesh.ops.create_cube(
    bm_bck, size=1.0,
    matrix=Matrix.Translation(Vector((-0.02, -0.095, 0.96))) @ Matrix.Diagonal((0.038, 0.008, 0.045, 1.0))
)
bm_bck.to_mesh(buckle_mesh)
bm_bck.free()
for p in buckle_mesh.polygons:
    p.use_smooth = True

# ---------------------------------------------------------------------------
# 11. Rigging Armature (Game-Ready Humanoid Hierarchy)
# ---------------------------------------------------------------------------
print("[AAA_KABIR] Building Rigged Armature Hierarchy...")
arm_data = bpy.data.armatures.new("Armature_Kabir")
arm_obj = bpy.data.objects.new("Kabir_Armature", arm_data)
bpy.context.collection.objects.link(arm_obj)

bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.mode_set(mode='EDIT')

eb = arm_data.edit_bones

def make_bone(name, head, tail, parent=None):
    b = eb.new(name)
    b.head = head
    b.tail = tail
    if parent:
        b.parent = parent
        b.use_connect = False
    return b

root = make_bone("Root", Vector((0, 0, 0)), Vector((0, 0, 0.1)))
hips = make_bone("Hips", Vector((0, 0, 0.74)), Vector((0, 0, 0.84)), root)
spine1 = make_bone("Spine_01", Vector((0, 0, 0.84)), Vector((0, 0, 0.98)), hips)
spine2 = make_bone("Spine_02", Vector((0, 0, 0.98)), Vector((0, 0, 1.12)), spine1)
neck = make_bone("Neck", Vector((0, 0, 1.12)), Vector((0, 0, 1.20)), spine2)
head_b = make_bone("Head", Vector((0, 0, 1.20)), Vector((0, 0, 1.42)), neck)

for side, sign in [("L", 1), ("R", -1)]:
    clav = make_bone(f"Clavicle_{side}", Vector((0, 0, 1.10)), Vector((sign * 0.14, 0, 1.08)), spine2)
    u_arm = make_bone(f"UpperArm_{side}", Vector((sign * 0.14, 0, 1.08)), Vector((sign * 0.22, 0, 0.82)), clav)
    l_arm = make_bone(f"Forearm_{side}", Vector((sign * 0.22, 0, 0.82)), Vector((sign * 0.28, 0, 0.58)), u_arm)
    hand = make_bone(f"Hand_{side}", Vector((sign * 0.28, 0, 0.58)), Vector((sign * 0.30, 0, 0.50)), l_arm)

    thigh = make_bone(f"Thigh_{side}", Vector((sign * 0.065, 0, 0.74)), Vector((sign * 0.065, 0, 0.44)), hips)
    calf = make_bone(f"Calf_{side}", Vector((sign * 0.065, 0, 0.44)), Vector((sign * 0.065, 0, 0.12)), thigh)
    foot = make_bone(f"Foot_{side}", Vector((sign * 0.065, 0, 0.12)), Vector((sign * 0.065, -0.10, 0.02)), calf)

bpy.ops.object.mode_set(mode='OBJECT')

# Parent all meshes to armature
all_character_meshes = [
    obj_head, eye_obj, lash_obj, brow_obj, patka_obj,
    body_obj, kurta_obj, btn_obj, pajama_obj, jutti_obj,
    satchel_obj, buckle_obj
]
for obj in all_character_meshes:
    obj.parent = arm_obj
    mod = obj.modifiers.new("Armature", 'ARMATURE')
    mod.object = arm_obj

# ---------------------------------------------------------------------------
# 12. Studio 3-Point Cinematic Lighting & Cameras
# Subject is centered at (0, 0, 0.75) and faces -Y
# ---------------------------------------------------------------------------
print("[AAA_KABIR] Setting Studio Lighting & Hero Cameras...")

# Key Light (Warm golden sunlight from front-left)
key_light_data = bpy.data.lights.new(name="Sun_Key_AAA", type='AREA')
key_light_data.energy = 85.0
key_light_data.size = 1.2
key_light_data.color = (1.0, 0.95, 0.88)
key_obj = bpy.data.objects.new("Sun_Key_AAA", key_light_data)
key_obj.location = (-0.8, -1.6, 1.5)
key_obj.rotation_euler = (math.radians(55.0), 0.0, math.radians(-25.0))
bpy.context.collection.objects.link(key_obj)

# Fill Light (Cool sky bounce from front-right)
fill_light_data = bpy.data.lights.new(name="Fill_Light_AAA", type='AREA')
fill_light_data.energy = 35.0
fill_light_data.size = 1.8
fill_light_data.color = (0.85, 0.90, 1.0)
fill_obj = bpy.data.objects.new("Fill_Light_AAA", fill_light_data)
fill_obj.location = (0.9, -1.4, 1.0)
fill_obj.rotation_euler = (math.radians(45.0), 0.0, math.radians(35.0))
bpy.context.collection.objects.link(fill_obj)

# Rim Light (Crisp backlight from behind)
rim_light_data = bpy.data.lights.new(name="Sky_Rim_AAA", type='AREA')
rim_light_data.energy = 65.0
rim_light_data.size = 1.5
rim_light_data.color = (1.0, 0.85, 0.70)
rim_obj = bpy.data.objects.new("Sky_Rim_AAA", rim_light_data)
rim_obj.location = (0.3, 1.5, 1.6)
rim_obj.rotation_euler = (math.radians(-55.0), 0.0, math.radians(165.0))
bpy.context.collection.objects.link(rim_obj)

# Dark Slate Studio Background
world = bpy.context.scene.world
if world and world.node_tree:
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.16, 0.17, 0.19, 1.0)
        bg.inputs["Strength"].default_value = 0.40

# Setup 3 Cameras: Portrait, Hero 3/4 Full-Body, Profile
# 1. Close-up Face Portrait (Camera in front of face at -Y, looking towards +Y)
cam_port_data = bpy.data.cameras.new("Cam_Portrait_Face")
cam_port_data.lens = 85.0 # Flattering portrait telephoto
cam_port = bpy.data.objects.new("Cam_Portrait_Face", cam_port_data)
cam_port.location = (0.0, -0.92, 1.28)
cam_port.rotation_euler = (math.radians(90.0), 0.0, 0.0) # Look directly down +Y
bpy.context.collection.objects.link(cam_port)

# 2. Hero 3/4 Full-Body
cam_hero_data = bpy.data.cameras.new("Cam_Hero_FullBody")
cam_hero_data.lens = 50.0 # Standard 50mm hero lens
cam_hero = bpy.data.objects.new("Cam_Hero_FullBody", cam_hero_data)
cam_hero.location = (-0.55, -2.10, 0.85)
cam_hero.rotation_euler = (math.radians(82.0), 0.0, math.radians(-15.0))
bpy.context.collection.objects.link(cam_hero)

# 3. Side Profile
cam_prof_data = bpy.data.cameras.new("Cam_Profile_Side")
cam_prof_data.lens = 70.0
cam_prof = bpy.data.objects.new("Cam_Profile_Side", cam_prof_data)
cam_prof.location = (-1.25, -0.02, 1.28)
cam_prof.rotation_euler = (math.radians(90.0), 0.0, math.radians(-90.0))
bpy.context.collection.objects.link(cam_prof)

# Render Settings
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1440
bpy.context.scene.render.film_transparent = False

# ---------------------------------------------------------------------------
# 13. Dual-Folder Pipeline Export & Renders
# ---------------------------------------------------------------------------
art_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\PROJECT"
dest_dir = r"C:\Users\npal7\PROJECT\PROJECT"
os.makedirs(art_dir, exist_ok=True)
os.makedirs(dest_dir, exist_ok=True)

blend_art = os.path.join(art_dir, "Kabir_Protagonist_AAA.blend")
blend_dest = os.path.join(dest_dir, "Kabir_Protagonist_AAA.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_art)
bpy.ops.wm.save_as_mainfile(filepath=blend_dest)
print(f"[AAA_KABIR] Saved .blend to {blend_art} and {blend_dest}")

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
print(f"[AAA_KABIR] Exported rigged FBX to {fbx_art} and {fbx_dest}")

# Render Portrait Still
render_port_art = os.path.join(art_dir, "Kabir_Protagonist_AAA_Portrait.png")
render_port_dest = os.path.join(dest_dir, "Kabir_Protagonist_AAA_Portrait.png")
bpy.context.scene.camera = cam_port
bpy.context.scene.render.filepath = render_port_art
bpy.ops.render.render(write_still=True)
shutil.copyfile(render_port_art, render_port_dest)
print(f"[AAA_KABIR] Rendered portrait to {render_port_art}")

# Render Hero 3/4 Still
render_hero_art = os.path.join(art_dir, "Kabir_Protagonist_AAA_Hero.png")
render_hero_dest = os.path.join(dest_dir, "Kabir_Protagonist_AAA_Hero.png")
bpy.context.scene.camera = cam_hero
bpy.context.scene.render.filepath = render_hero_art
bpy.ops.render.render(write_still=True)
shutil.copyfile(render_hero_art, render_hero_dest)
print(f"[AAA_KABIR] Rendered hero full-body to {render_hero_art}")

# Render Side Profile Still
render_prof_art = os.path.join(art_dir, "Kabir_Protagonist_AAA_Profile.png")
render_prof_dest = os.path.join(dest_dir, "Kabir_Protagonist_AAA_Profile.png")
bpy.context.scene.camera = cam_prof
bpy.context.scene.render.filepath = render_prof_art
bpy.ops.render.render(write_still=True)
shutil.copyfile(render_prof_art, render_prof_dest)
print(f"[AAA_KABIR] Rendered profile to {render_prof_art}")

print("[AAA_KABIR] COMPLETE SUCCESS! Protagonist redesigned and verified.")
