"""
PROJECT REVOLUTION — AAA Protagonist Character: Kabir (12-Year-Old Indian Boy, April 1919 Punjab)
Lead AAA Character Artist & Technical Artist Pipeline
"""

import bpy
import bmesh
import math
import os
from mathutils import Vector, Matrix

print("[AAA_KABIR] Starting AAA Protagonist Generation...")

# ---------------------------------------------------------------------------
# 1. Clean Scene Objects safely
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
# 2. Setup Shaders with Principled BSDF v2
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

# Authentic 1919 Punjabi Palette
mat_skin = make_shader("M_Kabir_Skin_AAA", (0.68, 0.44, 0.30, 1.0), roughness=0.48, sss_weight=0.25, sss_radius=(1.0, 0.65, 0.42))
mat_eyes_sclera = make_shader("M_Kabir_Sclera", (0.92, 0.90, 0.88, 1.0), roughness=0.10)
mat_eyes_iris = make_shader("M_Kabir_Iris", (0.16, 0.09, 0.04, 1.0), roughness=0.06)
mat_patka = make_shader("M_Kabir_Patka_Saffron", (0.94, 0.48, 0.04, 1.0), roughness=0.82, sheen_weight=0.55)
mat_kurta = make_shader("M_Kabir_Khadi_Kurta", (0.86, 0.82, 0.74, 1.0), roughness=0.88, sheen_weight=0.35)
mat_pajama = make_shader("M_Kabir_Cotton_Pajama", (0.88, 0.86, 0.82, 1.0), roughness=0.85, sheen_weight=0.30)
mat_leather = make_shader("M_Kabir_Aged_Leather", (0.30, 0.16, 0.08, 1.0), roughness=0.52, coat_weight=0.30)
mat_brass = make_shader("M_Kabir_Brass", (0.84, 0.70, 0.28, 1.0), roughness=0.32, metallic=0.92)
mat_wood = make_shader("M_Kabir_Wood_Buttons", (0.24, 0.14, 0.08, 1.0), roughness=0.72)
mat_chalk = make_shader("M_Kabir_Chalk", (0.96, 0.96, 0.95, 1.0), roughness=0.95)

# ---------------------------------------------------------------------------
# 3. Procedural Mesh Generation Helper Functions
# ---------------------------------------------------------------------------
def create_mesh_object(name, material):
    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)
    return obj, mesh

def add_subsurf(obj, levels=2, render_levels=2):
    mod = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    mod.levels = levels
    mod.render_levels = render_levels
    mod.quality = 3
    return mod

def smooth_mesh(mesh):
    for p in mesh.polygons:
        p.use_smooth = True

# ---------------------------------------------------------------------------
# 4. Anatomical Head, Face & Facial Features (Continuous Organic Topology)
# ---------------------------------------------------------------------------
# Build an organic quad-based human head cage with sculpted features
obj_head, mesh_head = create_mesh_object("Kabir_Head", mat_skin)
bm_h = bmesh.new()

# Latitude-longitude quad rings for cranium, temples, jaw, chin, cheeks
rings = [
    # (z_center, radius_x, radius_y, y_offset, segments)
    (1.44, 0.035, 0.040, -0.010),  # Cranium Top
    (1.42, 0.065, 0.075, -0.012),  # Upper Cranium
    (1.39, 0.082, 0.092, -0.010),  # Forehead & Crown
    (1.35, 0.086, 0.095, -0.005),  # Brow Ridge / Temples
    (1.32, 0.082, 0.092,  0.000),  # Eye Socket Level
    (1.29, 0.078, 0.086,  0.005),  # Cheekbones (Zygomatic) & Nose Bridge
    (1.26, 0.072, 0.078,  0.010),  # Upper Maxilla / Nose Base
    (1.23, 0.064, 0.068,  0.012),  # Lips / Mouth Crevice
    (1.20, 0.054, 0.058,  0.015),  # Chin & Mandible Base
    (1.17, 0.046, 0.048,  0.005),  # Upper Neck
    (1.13, 0.052, 0.054, -0.005),  # Base of Neck / Throat
]

first_ring_verts = []
prev_verts = []
for z, rx, ry, y_off in rings:
    current_verts = []
    num_pts = 16
    for i in range(num_pts):
        ang = 2 * math.pi * i / num_pts
        # Sculpt juvenile profile: flatten back, contour front for nose/chin
        x = rx * math.sin(ang)
        y = ry * math.cos(ang) + y_off
        
        # Front facial plane projection (around index 0, where cos(ang) is near 1)
        if math.cos(ang) > 0.65:
            if 1.25 <= z <= 1.30:  # Nose projection
                y += 0.032 * (math.cos(ang) - 0.65) / 0.35
            elif 1.22 <= z <= 1.25:  # Lips projection
                y += 0.018 * (math.cos(ang) - 0.65) / 0.35
            elif 1.19 <= z <= 1.22:  # Chin projection
                y += 0.024 * (math.cos(ang) - 0.65) / 0.35
        # Soft juvenile jaw taper on sides
        if z <= 1.22 and abs(math.sin(ang)) > 0.5:
            x *= 0.88
            
        v = bm_h.verts.new(Vector((x, y, z)))
        current_verts.append(v)
        
    if not first_ring_verts:
        first_ring_verts = current_verts
    if prev_verts:
        for i in range(num_pts):
            next_i = (i + 1) % num_pts
            bm_h.faces.new([prev_verts[i], prev_verts[next_i], current_verts[next_i], current_verts[i]])
    prev_verts = current_verts

# Cap cranium top
top_v = bm_h.verts.new(Vector((0.0, -0.010, 1.45)))
for i in range(16):
    next_i = (i + 1) % 16
    bm_h.faces.new([top_v, first_ring_verts[i], first_ring_verts[next_i]])

# Sculpt realistic juvenile nose (detailed bridge, bulb, nostril wings)
nose_tip = bm_h.verts.new(Vector((0.0, 0.124, 1.278)))
nose_bridge = bm_h.verts.new(Vector((0.0, 0.108, 1.312)))
nose_columella = bm_h.verts.new(Vector((0.0, 0.106, 1.264)))
for sign in [-1, 1]:
    n_wing = bm_h.verts.new(Vector((sign * 0.016, 0.108, 1.272)))
    # Nostril facet
    bm_h.faces.new([nose_tip, n_wing, nose_columella])
    bm_h.faces.new([nose_bridge, n_wing, nose_tip])

# Sculpt mouth (Cupid's bow upper lip, vermilion border, fleshy lower lip)
lip_upper_mid = bm_h.verts.new(Vector((0.0, 0.098, 1.242)))
lip_lower_mid = bm_h.verts.new(Vector((0.0, 0.094, 1.228)))
for sign in [-1, 1]:
    mouth_corner = bm_h.verts.new(Vector((sign * 0.024, 0.082, 1.235)))
    bm_h.faces.new([lip_upper_mid, mouth_corner, lip_lower_mid])

# Sculpt Ears (Helix, Antihelix, Lobe)
for sign in [-1, 1]:
    ear_top = bm_h.verts.new(Vector((sign * 0.086, -0.015, 1.335)))
    ear_mid = bm_h.verts.new(Vector((sign * 0.094, -0.018, 1.305)))
    ear_lobe = bm_h.verts.new(Vector((sign * 0.088, -0.016, 1.275)))
    ear_base = bm_h.verts.new(Vector((sign * 0.078, -0.005, 1.305)))
    bm_h.faces.new([ear_top, ear_mid, ear_base])
    bm_h.faces.new([ear_mid, ear_lobe, ear_base])

bm_h.to_mesh(mesh_head)
bm_h.free()
smooth_mesh(mesh_head)
add_subsurf(obj_head, levels=2)

# Realistic Eyeballs (Dark Indian Eyes with glistening cornea)
for side, sign in [("L", 1), ("R", -1)]:
    # Sclera
    obj_eye, m_eye = create_mesh_object(f"Kabir_Eye_{side}", mat_eyes_sclera)
    bm_e = bmesh.new()
    bmesh.ops.create_uvsphere(bm_e, u_segments=16, v_segments=12, radius=0.014, matrix=Matrix.Translation(Vector((sign * 0.034, 0.080, 1.318))))
    bm_e.to_mesh(m_eye)
    bm_e.free()
    smooth_mesh(m_eye)
    add_subsurf(obj_eye, levels=1)

    # Iris & Pupil
    obj_iris, m_iris = create_mesh_object(f"Kabir_Iris_{side}", mat_eyes_iris)
    bm_i = bmesh.new()
    bmesh.ops.create_cone(bm_i, cap_ends=True, segments=14, radius1=0.008, radius2=0.004, depth=0.005, matrix=Matrix.Translation(Vector((sign * 0.034, 0.092, 1.318))) @ Matrix.Rotation(math.radians(90.0), 4, 'X'))
    bm_i.to_mesh(m_iris)
    bm_i.free()
    smooth_mesh(m_iris)

# ---------------------------------------------------------------------------
# 5. Saffron Patka Headdress (Folded Cloth Crown, Juda Topknot, Nape Ties)
# ---------------------------------------------------------------------------
obj_patka, mesh_patka = create_mesh_object("Kabir_Patka", mat_patka)
bm_p = bmesh.new()

# Crown Wrap conformed to cranium
patka_rings = [
    (1.36, 0.089, 0.098, -0.004),
    (1.39, 0.088, 0.097, -0.008),
    (1.42, 0.082, 0.088, -0.010),
    (1.45, 0.068, 0.074, -0.010),
    (1.47, 0.046, 0.052, -0.008)
]
prev_p = []
for z, rx, ry, y_off in patka_rings:
    curr_p = []
    for i in range(16):
        ang = 2 * math.pi * i / 16
        x = rx * math.sin(ang)
        y = ry * math.cos(ang) + y_off
        # Front V-crest characteristic fold
        if math.cos(ang) > 0.6:
            y += 0.014 * (math.cos(ang) - 0.6)
            z_mod = z - 0.012 * (math.cos(ang) - 0.6)
        else:
            z_mod = z
        v = bm_p.verts.new(Vector((x, y, z_mod)))
        curr_p.append(v)
    if prev_p:
        for i in range(16):
            ni = (i + 1) % 16
            bm_p.faces.new([prev_p[i], prev_p[ni], curr_p[ni], curr_p[i]])
    prev_p = curr_p

# Topknot Juda Bun (Saffron cloth-wrapped hair bun)
juda = bmesh.ops.create_uvsphere(bm_p, u_segments=16, v_segments=12, radius=0.045, matrix=Matrix.Translation(Vector((0.0, 0.005, 1.492))) @ Matrix.Diagonal((1.0, 0.95, 0.85, 1.0)))
# Bun tie band
bmesh.ops.create_cone(bm_p, cap_ends=True, segments=16, radius1=0.048, radius2=0.045, depth=0.022, matrix=Matrix.Translation(Vector((0.0, 0.005, 1.468))))

# Flowing Nape Ties (Graceful curved fabric tails flowing down upper back)
for sign in [-1, 1]:
    tie_verts_prev = []
    for step in range(6):
        tz = 1.34 - step * 0.038
        ty = -0.095 - step * 0.008 + math.sin(step) * 0.004
        tx = sign * (0.028 + step * 0.008)
        w = 0.018 * (1.0 - step * 0.12)
        v1 = bm_p.verts.new(Vector((tx - w, ty, tz)))
        v2 = bm_p.verts.new(Vector((tx + w, ty, tz)))
        curr_t = [v1, v2]
        if tie_verts_prev:
            bm_p.faces.new([tie_verts_prev[0], tie_verts_prev[1], curr_t[1], curr_t[0]])
        tie_verts_prev = curr_t

bm_p.to_mesh(mesh_patka)
bm_p.free()
smooth_mesh(mesh_patka)
add_subsurf(obj_patka, levels=2)

# Solidify modifier for authentic fabric thickness
mod_sol_patka = obj_patka.modifiers.new("Solidify", 'SOLIDIFY')
mod_sol_patka.thickness = 0.004

# ---------------------------------------------------------------------------
# 6. Handspun Khadi Kurta (Authentic Drapery, Mandarin Collar, Button Placket)
# ---------------------------------------------------------------------------
obj_kurta, mesh_kurta = create_mesh_object("Kabir_Kurta", mat_kurta)
bm_k = bmesh.new()

# Torso Body Quad Rings (Fitted chest to flared knee-length hem with side chaks)
kurta_rings = [
    # (z, rx, ry, y_offset)
    (1.15, 0.105, 0.082, 0.002), # Collar base
    (1.11, 0.155, 0.098, 0.000), # Upper chest & shoulders
    (1.02, 0.152, 0.094, 0.002), # Mid chest
    (0.92, 0.145, 0.092, 0.004), # Waist
    (0.82, 0.154, 0.098, 0.006), # Hips
    (0.72, 0.168, 0.108, 0.008), # Upper thighs
    (0.62, 0.182, 0.118, 0.010), # Lower thighs
    (0.55, 0.192, 0.126, 0.012), # Bottom hem (knee level)
]

prev_k = []
for idx, (z, rx, ry, y_off) in enumerate(kurta_rings):
    curr_k = []
    num_k = 18
    for i in range(num_k):
        ang = 2 * math.pi * i / num_k
        x = rx * math.sin(ang)
        y = ry * math.cos(ang) + y_off
        # Side slit chaks at lower rings (indices 5, 6, 7)
        if idx >= 5 and abs(math.sin(ang)) > 0.92:
            x *= 1.05  # subtle flare at side opening
        v = bm_k.verts.new(Vector((x, y, z)))
        curr_k.append(v)
    if prev_k:
        for i in range(num_k):
            ni = (i + 1) % num_k
            # Leave open side chaks slits below hips on lateral seams
            if idx >= 6 and (i == 4 or i == 13):
                continue
            bm_k.faces.new([prev_k[i], prev_k[ni], curr_k[ni], curr_k[i]])
    prev_k = curr_k

# Standing Mandarin / Nehru Collar
collar = bmesh.ops.create_cone(bm_k, cap_ends=False, segments=18, radius1=0.068, radius2=0.064, depth=0.045, matrix=Matrix.Translation(Vector((0.0, 0.003, 1.172))))

# Front Tailoring Button Placket
bmesh.ops.create_cube(bm_k, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.096, 1.04))) @ Matrix.Diagonal((0.038, 0.008, 0.22, 1.0)))

# Sleeves (Loose arm drape tapering to rolled cuffs)
for side, sign in [("L", 1), ("R", -1)]:
    sleeve_rings = [
        (Vector((sign * 0.16, 0.00, 1.12)), 0.062),
        (Vector((sign * 0.18, 0.01, 1.02)), 0.054),
        (Vector((sign * 0.20, 0.02, 0.90)), 0.050),
        (Vector((sign * 0.21, 0.03, 0.78)), 0.046),
        (Vector((sign * 0.22, 0.035, 0.72)), 0.050), # Rolled cuff
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

bm_k.to_mesh(mesh_kurta)
bm_k.free()
smooth_mesh(mesh_kurta)
add_subsurf(obj_kurta, levels=2)

mod_sol_kurta = obj_kurta.modifiers.new("Solidify", 'SOLIDIFY')
mod_sol_kurta.thickness = 0.005

# Hand-carved Wooden Buttons (Father's tailor craft)
obj_buttons, mesh_buttons = create_mesh_object("Kabir_Buttons", mat_wood)
bm_btn = bmesh.new()
for bz in [0.96, 1.03, 1.10]:
    bmesh.ops.create_cone(bm_btn, cap_ends=True, segments=12, radius1=0.009, radius2=0.009, depth=0.006, matrix=Matrix.Translation(Vector((0.0, 0.102, bz))) @ Matrix.Rotation(math.radians(90.0), 4, 'X'))
bm_btn.to_mesh(mesh_buttons)
bm_btn.free()
smooth_mesh(mesh_buttons)

# ---------------------------------------------------------------------------
# 7. Anatomical Hands (Articulated 5 Fingers, Palms, Wrists)
# ---------------------------------------------------------------------------
obj_hands, mesh_hands = create_mesh_object("Kabir_Hands", mat_skin)
bm_hnd = bmesh.new()

for side, sign in [("L", 1), ("R", -1)]:
    hx = sign * 0.22
    # Palm body with thenar eminence
    palm = bmesh.ops.create_cube(bm_hnd, size=1.0, matrix=Matrix.Translation(Vector((hx, 0.035, 0.665))) @ Matrix.Diagonal((0.042, 0.062, 0.078, 1.0)))
    # Thumb with opposition
    thumb = bmesh.ops.create_cone(bm_hnd, cap_ends=True, segments=8, radius1=0.009, radius2=0.006, depth=0.045, matrix=Matrix.Translation(Vector((hx - sign*0.024, 0.045, 0.672))) @ Matrix.Rotation(math.radians(sign * 32.0), 4, 'Y') @ Matrix.Rotation(math.radians(15.0), 4, 'X'))
    # 4 Articulated fingers with natural relaxed curvature
    for f_idx in range(4):
        fz = 0.618 - f_idx * 0.007
        fx = hx + (f_idx - 1.5) * 0.009 * sign
        # Proximal phalanx
        p1 = bmesh.ops.create_cone(bm_hnd, cap_ends=True, segments=8, radius1=0.007, radius2=0.0055, depth=0.028, matrix=Matrix.Translation(Vector((fx, 0.040, fz))) @ Matrix.Rotation(math.radians(12.0), 4, 'X'))
        # Distal phalanx with fingertip
        p2 = bmesh.ops.create_cone(bm_hnd, cap_ends=True, segments=8, radius1=0.0055, radius2=0.004, depth=0.024, matrix=Matrix.Translation(Vector((fx, 0.046, fz - 0.024))) @ Matrix.Rotation(math.radians(24.0), 4, 'X'))

bm_hnd.to_mesh(mesh_hands)
bm_hnd.free()
smooth_mesh(mesh_hands)
add_subsurf(obj_hands, levels=2)

# ---------------------------------------------------------------------------
# 8. Cotton Pajama Trousers (Gathered Folds, Ankle Taper)
# ---------------------------------------------------------------------------
obj_pajama, mesh_pajama = create_mesh_object("Kabir_Pajama", mat_pajama)
bm_pj = bmesh.new()

# Pelvis waistband
bmesh.ops.create_cone(bm_pj, cap_ends=True, segments=18, radius1=0.145, radius2=0.138, depth=0.18, matrix=Matrix.Translation(Vector((0.0, 0.005, 0.72))))

# Legs with natural juvenile knee crease and ankle gather folds
for side, sign in [("L", 1), ("R", -1)]:
    lx = sign * 0.105
    leg_rings = [
        (Vector((lx, 0.00, 0.64)), 0.075), # Groin / upper thigh
        (Vector((lx, 0.01, 0.52)), 0.068), # Mid thigh
        (Vector((lx, 0.015, 0.42)), 0.064), # Knee gathering fold
        (Vector((lx, 0.012, 0.32)), 0.058), # Upper calf
        (Vector((lx, 0.008, 0.20)), 0.052), # Lower calf
        (Vector((lx, 0.005, 0.12)), 0.048), # Churidar ankle gather fold
        (Vector((lx, 0.002, 0.07)), 0.046), # Ankle cuff hem
    ]
    prev_l = []
    for center, rad in leg_rings:
        curr_l = []
        for i in range(14):
            ang = 2 * math.pi * i / 14
            # Add cloth crease perturbations
            crease = 0.004 * math.sin(ang * 3 + center.z * 20.0)
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

bm_pj.to_mesh(mesh_pajama)
bm_pj.free()
smooth_mesh(mesh_pajama)
add_subsurf(obj_pajama, levels=2)

mod_sol_pj = obj_pajama.modifiers.new("Solidify", 'SOLIDIFY')
mod_sol_pj.thickness = 0.004

# ---------------------------------------------------------------------------
# 9. Punjabi Leather Juttis (Authentic Curled Nok Toe, Hard Sole Welt)
# ---------------------------------------------------------------------------
obj_juttis, mesh_juttis = create_mesh_object("Kabir_Juttis", mat_leather)
bm_j = bmesh.new()

for side, sign in [("L", 1), ("R", -1)]:
    jx = sign * 0.105
    # Hand-stitched Sole Welt
    bmesh.ops.create_cube(bm_j, size=1.0, matrix=Matrix.Translation(Vector((jx, 0.024, 0.015))) @ Matrix.Diagonal((0.072, 0.21, 0.020, 1.0)))
    
    # Shaped Leather Upper (Vamp, quarters, heel counter)
    jutti_rings = [
        (Vector((jx, -0.06, 0.045)), 0.038, 0.025), # Heel counter
        (Vector((jx, 0.00, 0.048)),  0.044, 0.030), # Instep throat
        (Vector((jx, 0.06, 0.042)),  0.042, 0.026), # Ball of foot
        (Vector((jx, 0.11, 0.036)),  0.032, 0.018), # Toe box base
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
        
    # Iconic Curled Upturned Nok Toe Tip
    nok_tip = bm_j.verts.new(Vector((jx, 0.155, 0.075)))
    for i in range(12):
        ni = (i + 1) % 12
        bm_j.faces.new([curr_jr[i], curr_jr[ni], nok_tip])

bm_j.to_mesh(mesh_juttis)
bm_j.free()
smooth_mesh(mesh_juttis)
add_subsurf(obj_juttis, levels=2)

# ---------------------------------------------------------------------------
# 10. Leather Satchel & Hardware (Crossbody Strap, Buckle, Chalk Pouch)
# ---------------------------------------------------------------------------
obj_satchel, mesh_satchel = create_mesh_object("Kabir_Satchel", mat_leather)
bm_s = bmesh.new()

# Main messenger bag body (Left hip)
bmesh.ops.create_cube(bm_s, size=1.0, matrix=Matrix.Translation(Vector((-0.185, 0.025, 0.72))) @ Matrix.Diagonal((0.085, 0.24, 0.19, 1.0)))
# Bag front closing flap
bmesh.ops.create_cube(bm_s, size=1.0, matrix=Matrix.Translation(Vector((-0.188, 0.085, 0.735))) @ Matrix.Diagonal((0.090, 0.014, 0.15, 1.0)))

# Crossbody leather strap (Right shoulder diagonally across chest to left hip)
strap_pts = [
    Vector((0.17, 0.02, 1.14)),   # Right shoulder
    Vector((0.11, 0.09, 1.06)),   # Right chest
    Vector((0.00, 0.098, 0.96)),  # Sternum center
    Vector((-0.10, 0.088, 0.84)), # Left rib
    Vector((-0.18, 0.04, 0.76)),  # Left hip bag mount
]
prev_st = []
for pt in strap_pts:
    v1 = bm_s.verts.new(pt + Vector((-0.012, 0.005, 0.008)))
    v2 = bm_s.verts.new(pt + Vector((0.012, -0.005, -0.008)))
    curr_st = [v1, v2]
    if prev_st:
        bm_s.faces.new([prev_st[0], prev_st[1], curr_st[1], curr_st[0]])
    prev_st = curr_st

bm_s.to_mesh(mesh_satchel)
bm_s.free()
smooth_mesh(mesh_satchel)
add_subsurf(obj_satchel, levels=2)
mod_sol_s = obj_satchel.modifiers.new("Solidify", 'SOLIDIFY')
mod_sol_s.thickness = 0.005

# Brass Buckle
obj_buckle, mesh_buckle = create_mesh_object("Kabir_Satchel_Buckle", mat_brass)
bm_b = bmesh.new()
bmesh.ops.create_cone(bm_b, cap_ends=True, segments=14, radius1=0.024, radius2=0.024, depth=0.010, matrix=Matrix.Translation(Vector((-0.188, 0.096, 0.67))) @ Matrix.Rotation(math.radians(90.0), 4, 'Y'))
bm_b.to_mesh(mesh_buckle)
bm_b.free()
smooth_mesh(mesh_buckle)

# Right Hip Waist Pouch & Soapstone Tailor's Chalk
obj_pouch, mesh_pouch = create_mesh_object("Kabir_Chalk_Pouch", mat_kurta)
bm_pch = bmesh.new()
bmesh.ops.create_uvsphere(bm_pch, u_segments=12, v_segments=10, radius=0.042, matrix=Matrix.Translation(Vector((0.16, 0.02, 0.74))) @ Matrix.Diagonal((0.7, 1.0, 1.2, 1.0)))
bm_pch.to_mesh(mesh_pouch)
bm_pch.free()
smooth_mesh(mesh_pouch)
add_subsurf(obj_pouch, levels=1)

obj_chalk, mesh_chalk = create_mesh_object("Kabir_Chalk_Stick", mat_chalk)
bm_chk = bmesh.new()
bmesh.ops.create_cube(bm_chk, size=1.0, matrix=Matrix.Translation(Vector((0.16, 0.02, 0.81))) @ Matrix.Diagonal((0.018, 0.032, 0.055, 1.0)))
bm_chk.to_mesh(mesh_chalk)
bm_chk.free()

print("[AAA_KABIR] High-fidelity anatomical assets and authentic period garments generated.")

# ---------------------------------------------------------------------------
# 11. Humanoid Armature Skeleton (UE5 Standard Hierarchy)
# ---------------------------------------------------------------------------
arm_data = bpy.data.armatures.new("Armature_Kabir_AAA")
arm_obj = bpy.data.objects.new("Kabir_AAA_Armature", arm_data)
bpy.context.collection.objects.link(arm_obj)
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.mode_set(mode='EDIT')

eb = arm_data.edit_bones

# Spine Chain
b_root = eb.new("root")
b_root.head = (0.0, 0.0, 0.0)
b_root.tail = (0.0, 0.0, 0.10)

b_pelvis = eb.new("pelvis")
b_pelvis.head = (0.0, 0.0, 0.72)
b_pelvis.tail = (0.0, 0.0, 0.84)
b_pelvis.parent = b_root

b_sp1 = eb.new("spine_01")
b_sp1.head = (0.0, 0.0, 0.84)
b_sp1.tail = (0.0, 0.0, 0.98)
b_sp1.parent = b_pelvis

b_sp2 = eb.new("spine_02")
b_sp2.head = (0.0, 0.0, 0.98)
b_sp2.tail = (0.0, 0.0, 1.10)
b_sp2.parent = b_sp1

b_sp3 = eb.new("spine_03")
b_sp3.head = (0.0, 0.0, 1.10)
b_sp3.tail = (0.0, 0.0, 1.18)
b_sp3.parent = b_sp2

b_neck = eb.new("neck_01")
b_neck.head = (0.0, 0.0, 1.18)
b_neck.tail = (0.0, 0.0, 1.26)
b_neck.parent = b_sp3

b_head = eb.new("head")
b_head.head = (0.0, 0.0, 1.26)
b_head.tail = (0.0, 0.0, 1.48)
b_head.parent = b_neck

# Left and Right Limbs
for side, sign in [("_l", 1), ("_r", -1)]:
    b_clav = eb.new(f"clavicle{side}")
    b_clav.head = (0.0, 0.0, 1.14)
    b_clav.tail = (sign * 0.14, 0.0, 1.14)
    b_clav.parent = b_sp3

    b_uarm = eb.new(f"upperarm{side}")
    b_uarm.head = (sign * 0.16, 0.0, 1.12)
    b_uarm.tail = (sign * 0.20, 0.02, 0.90)
    b_uarm.parent = b_clav

    b_larm = eb.new(f"lowerarm{side}")
    b_larm.head = (sign * 0.20, 0.02, 0.90)
    b_larm.tail = (sign * 0.22, 0.035, 0.72)
    b_larm.parent = b_uarm

    b_hand = eb.new(f"hand{side}")
    b_hand.head = (sign * 0.22, 0.035, 0.72)
    b_hand.tail = (sign * 0.22, 0.04, 0.60)
    b_hand.parent = b_larm

    b_thigh = eb.new(f"thigh{side}")
    b_thigh.head = (sign * 0.105, 0.0, 0.72)
    b_thigh.tail = (sign * 0.105, 0.015, 0.42)
    b_thigh.parent = b_pelvis

    b_calf = eb.new(f"calf{side}")
    b_calf.head = (sign * 0.105, 0.015, 0.42)
    b_calf.tail = (sign * 0.105, 0.005, 0.08)
    b_calf.parent = b_thigh

    b_foot = eb.new(f"foot{side}")
    b_foot.head = (sign * 0.105, 0.005, 0.08)
    b_foot.tail = (sign * 0.105, 0.12, 0.02)
    b_foot.parent = b_calf

bpy.ops.object.mode_set(mode='OBJECT')

print("[AAA_KABIR] Created UE5 Mannequin-compatible humanoid armature skeleton.")

# ---------------------------------------------------------------------------
# 12. Cinematic 3-Point Lighting & Showcase Cameras
# ---------------------------------------------------------------------------
# Key Light (3200K Warm Punjab Morning Sun)
key_data = bpy.data.lights.new(name="Sun_Key_AAA", type='POINT')
key_data.energy = 850.0
key_data.color = (1.0, 0.92, 0.78)
key_obj = bpy.data.objects.new("Sun_Key_AAA", key_data)
key_obj.location = (-1.4, 2.2, 2.2)
bpy.context.collection.objects.link(key_obj)

# Rim Light (Sky Edge Accent)
rim_data = bpy.data.lights.new(name="Sky_Rim_AAA", type='POINT')
rim_data.energy = 550.0
rim_data.color = (0.72, 0.84, 1.0)
rim_obj = bpy.data.objects.new("Sky_Rim_AAA", rim_data)
rim_obj.location = (1.5, -2.0, 1.9)
bpy.context.collection.objects.link(rim_obj)

# Soft Fill Light
fill_data = bpy.data.lights.new(name="Fill_Light_AAA", type='POINT')
fill_data.energy = 280.0
fill_data.color = (0.95, 0.88, 0.80)
fill_obj = bpy.data.objects.new("Fill_Light_AAA", fill_data)
fill_obj.location = (1.2, 1.8, 1.1)
bpy.context.collection.objects.link(fill_obj)

# Hero Full Body Presentation Camera
cam_data = bpy.data.cameras.new("Cam_Hero_FullBody")
cam_data.lens = 55.0
cam_obj = bpy.data.objects.new("Cam_Hero_FullBody", cam_data)
cam_obj.location = (-0.6, 2.5, 1.05)
cam_obj.rotation_euler = (math.radians(88.0), 0.0, math.radians(-166.0))
bpy.context.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj

# Close-up Portrait Camera (Focusing on sculpted face and saffron patka)
cam_face_data = bpy.data.cameras.new("Cam_Portrait_Face")
cam_face_data.lens = 85.0
cam_face_obj = bpy.data.objects.new("Cam_Portrait_Face", cam_face_data)
cam_face_obj.location = (-0.22, 1.15, 1.35)
cam_face_obj.rotation_euler = (math.radians(88.0), 0.0, math.radians(-170.0))
bpy.context.collection.objects.link(cam_face_obj)

# Render settings
bpy.context.scene.render.resolution_x = 1280
bpy.context.scene.render.resolution_y = 960
bpy.context.scene.render.image_settings.file_format = 'PNG'

# ---------------------------------------------------------------------------
# 13. Save Output Files to Designated Folders
# ---------------------------------------------------------------------------
art_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\PROJECT"
dest_dir = r"C:\Users\npal7\PROJECT\PROJECT"
os.makedirs(art_dir, exist_ok=True)
os.makedirs(dest_dir, exist_ok=True)

# Save .blend files
blend_art = os.path.join(art_dir, "Kabir_Protagonist_AAA.blend")
blend_dest = os.path.join(dest_dir, "Kabir_Protagonist_AAA.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_art)
bpy.ops.wm.save_as_mainfile(filepath=blend_dest)

# Export rigged FBX
fbx_art = os.path.join(art_dir, "SK_Kabir_Protagonist_AAA.fbx")
fbx_dest = os.path.join(dest_dir, "SK_Kabir_Protagonist_AAA.fbx")
bpy.ops.object.select_all(action='SELECT')
for path in [fbx_art, fbx_dest]:
    bpy.ops.export_scene.fbx(
        filepath=path,
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

# Render Showcase Still
render_out = os.path.join(art_dir, "Kabir_Protagonist_AAA_Hero.png")
render_dest = os.path.join(dest_dir, "Kabir_Protagonist_AAA_Hero.png")
bpy.context.scene.camera = cam_obj
bpy.context.scene.render.filepath = render_out
bpy.ops.render.render(write_still=True)

import shutil
shutil.copyfile(render_out, render_dest)

# Render Portrait Still
render_portrait_art = os.path.join(art_dir, "Kabir_Protagonist_AAA_Portrait.png")
render_portrait_dest = os.path.join(dest_dir, "Kabir_Protagonist_AAA_Portrait.png")
bpy.context.scene.camera = cam_face_obj
bpy.context.scene.render.filepath = render_portrait_art
bpy.ops.render.render(write_still=True)
shutil.copyfile(render_portrait_art, render_portrait_dest)

print(f"[AAA_KABIR] SUCCESS! Saved blend files to {blend_art} & {blend_dest}")
print(f"[AAA_KABIR] SUCCESS! Exported FBX to {fbx_art} & {fbx_dest}")
print(f"[AAA_KABIR] SUCCESS! Rendered hero and portrait captures.")
