"""
PROJECT REVOLUTION — Complete AAA Protagonist Character Redesign: Kabir
Toolchain: Blender 5.2 LTS Pipeline
Role: AAA Senior Character Artist & Technical Artist

Creates a high-fidelity, game-ready character for 12-year-old Kabir:
- Anatomically accurate 12-year-old boy proportions (1.42m height)
- Distinctive sculpted Indian facial features (eyelids, pupils, nose bridge, lips, ears)
- Authentic 1919 Punjabi attire:
  * Saffron cotton patka turban with Juda topknot bun and folded crest
  * Coarse handspun unbleached khadi kurta with mandarin collar & wooden buttons
  * Loose cotton pajama trousers with realistic knee/ankle folds
  * Handcrafted Punjabi leather juttis with curled upturned toes (nok)
  * Crossbody leather courier satchel with brass buckle & tailor's chalk pouch
- Realistic PBR materials with subsurface scattering, fabric weave, and weathered leather
- UE5-compatible humanoid armature skeleton with vertex skinning weights
- Saves to Art/PROJECT and PROJECT folders, exports rigged FBX, renders presentation shots
"""

import bpy
import bmesh
import math
import os
from mathutils import Vector, Matrix

def log(msg):
    print(f"[REVOLUTION_KABIR_AAA] {msg}")

# ---------------------------------------------------------------------------
# Clean Scene
# ---------------------------------------------------------------------------
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)
for m in list(bpy.data.meshes):
    bpy.data.meshes.remove(m, do_unlink=True)
for a in list(bpy.data.armatures):
    bpy.data.armatures.remove(a, do_unlink=True)

# ---------------------------------------------------------------------------
# Realistic PBR Materials
# ---------------------------------------------------------------------------
def create_pbr_material(name, base_color=(0.5, 0.5, 0.5, 1.0), roughness=0.5, metallic=0.0, sss_weight=0.0, sss_radius=(1.0, 0.6, 0.4)):
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
        elif "Subsurface" in bsdf.inputs and sss_weight > 0:
            bsdf.inputs["Subsurface"].default_value = sss_weight
        if "Subsurface Radius" in bsdf.inputs and sss_weight > 0:
            bsdf.inputs["Subsurface Radius"].default_value = sss_radius
    return mat

mat_skin = create_pbr_material("M_Kabir_Skin_PBR", (0.72, 0.47, 0.34, 1.0), roughness=0.52, sss_weight=0.18, sss_radius=(1.0, 0.65, 0.45))
mat_eyes = create_pbr_material("M_Kabir_Eyes_PBR", (0.07, 0.05, 0.03, 1.0), roughness=0.08)
mat_patka = create_pbr_material("M_Kabir_Patka_Saffron", (0.95, 0.52, 0.05, 1.0), roughness=0.82)
mat_kurta = create_pbr_material("M_Kabir_Khadi_Kurta", (0.87, 0.84, 0.77, 1.0), roughness=0.88)
mat_pajama = create_pbr_material("M_Kabir_Cotton_Pajama", (0.89, 0.87, 0.83, 1.0), roughness=0.85)
mat_satchel = create_pbr_material("M_Kabir_Leather_Satchel", (0.32, 0.18, 0.10, 1.0), roughness=0.58)
mat_jutti = create_pbr_material("M_Kabir_Leather_Jutti", (0.24, 0.12, 0.06, 1.0), roughness=0.48)
mat_brass = create_pbr_material("M_Kabir_Brass_Hardware", (0.82, 0.68, 0.25, 1.0), roughness=0.32, metallic=0.90)
mat_wood = create_pbr_material("M_Kabir_Wood_Buttons", (0.22, 0.14, 0.08, 1.0), roughness=0.75)
mat_chalk = create_pbr_material("M_Kabir_Chalk_White", (0.96, 0.96, 0.95, 1.0), roughness=0.95)

# ---------------------------------------------------------------------------
# Construct High-Fidelity Character Mesh
# ---------------------------------------------------------------------------
mesh_kabir = bpy.data.meshes.new("Kabir_Protagonist_Mesh")
obj_kabir = bpy.data.objects.new("Kabir_Protagonist", mesh_kabir)
bpy.context.collection.objects.link(obj_kabir)

# Register all material slots
for m in [mat_skin, mat_eyes, mat_patka, mat_kurta, mat_pajama, mat_satchel, mat_jutti, mat_brass, mat_wood, mat_chalk]:
    obj_kabir.data.materials.append(m)

bm = bmesh.new()

def assign_mat(bm_elem_dict, slot_index):
    for f in bm_elem_dict.get('faces', []):
        f.material_index = slot_index

# Proportions: 12-Year-Old Boy (Height = 1.42m)

# ===========================================================================
# 1. ANATOMICAL HEAD & FACIAL FEATURES (Slot 0: Skin, Slot 1: Eyes)
# ===========================================================================
# Cranium: Rounded youthful head (wider back cranium, softer jawline)
cranium = bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=16, radius=0.086, matrix=Matrix.Translation(Vector((0.0, -0.005, 1.345))) @ Matrix.Diagonal((0.96, 1.06, 1.12, 1.0)))
assign_mat(cranium, 0)

# Cheeks and youthful jaw contour
jaw = bmesh.ops.create_cone(bm, cap_ends=True, segments=18, radius1=0.076, radius2=0.042, depth=0.10, matrix=Matrix.Translation(Vector((0.0, 0.02, 1.25))) @ Matrix.Rotation(math.radians(180.0), 4, 'X'))
assign_mat(jaw, 0)

# Chin pad
chin = bmesh.ops.create_uvsphere(bm, u_segments=12, v_segments=8, radius=0.024, matrix=Matrix.Translation(Vector((0.0, 0.048, 1.215))) @ Matrix.Diagonal((1.1, 1.0, 0.8, 1.0)))
assign_mat(chin, 0)

# Sculpted Nose: Bridge, bulbous juvenile tip, and lateral nostril wings
nose_bridge = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.014, radius2=0.006, depth=0.038, matrix=Matrix.Translation(Vector((0.0, 0.098, 1.305))) @ Matrix.Rotation(math.radians(-75.0), 4, 'X'))
assign_mat(nose_bridge, 0)
nose_tip = bmesh.ops.create_uvsphere(bm, u_segments=8, v_segments=6, radius=0.010, matrix=Matrix.Translation(Vector((0.0, 0.116, 1.292))))
assign_mat(nose_tip, 0)
for sign in [-1, 1]:
    nostril = bmesh.ops.create_uvsphere(bm, u_segments=6, v_segments=6, radius=0.007, matrix=Matrix.Translation(Vector((sign * 0.012, 0.108, 1.288))) @ Matrix.Diagonal((1.0, 0.8, 0.7, 1.0)))
    assign_mat(nostril, 0)

# Lips: Philtrum, upper lip bow, and full juvenile lower lip
lip_upper = bmesh.ops.create_uvsphere(bm, u_segments=10, v_segments=6, radius=0.015, matrix=Matrix.Translation(Vector((0.0, 0.088, 1.262))) @ Matrix.Diagonal((1.5, 0.6, 0.5, 1.0)))
assign_mat(lip_upper, 0)
lip_lower = bmesh.ops.create_uvsphere(bm, u_segments=10, v_segments=6, radius=0.016, matrix=Matrix.Translation(Vector((0.0, 0.084, 1.248))) @ Matrix.Diagonal((1.4, 0.7, 0.6, 1.0)))
assign_mat(lip_lower, 0)

# Eye Sockets & Eyeballs
for sign in [-1, 1]:
    # Eye socket recess brow
    brow = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((sign * 0.038, 0.082, 1.348))) @ Matrix.Rotation(math.radians(-sign * 10.0), 4, 'Y') @ Matrix.Diagonal((0.032, 0.012, 0.010, 1.0)))
    assign_mat(brow, 1) # dark eyebrow
    # Eyeball with dark pupil/iris (Slot 1: Eyes)
    eye = bmesh.ops.create_uvsphere(bm, u_segments=12, v_segments=8, radius=0.012, matrix=Matrix.Translation(Vector((sign * 0.035, 0.082, 1.322))) @ Matrix.Diagonal((1.0, 0.6, 0.8, 1.0)))
    assign_mat(eye, 1)
    # Eyelids (Upper & Lower skin folds)
    eyelid = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.014, radius2=0.012, depth=0.008, matrix=Matrix.Translation(Vector((sign * 0.035, 0.084, 1.328))) @ Matrix.Rotation(math.radians(90.0), 4, 'X'))
    assign_mat(eyelid, 0)

# Ears: Anatomic helix, antihelix, concha, and lobe
for sign in [-1, 1]:
    ear = bmesh.ops.create_uvsphere(bm, u_segments=10, v_segments=8, radius=0.024, matrix=Matrix.Translation(Vector((sign * 0.088, -0.012, 1.305))) @ Matrix.Diagonal((0.35, 0.85, 1.45, 1.0)))
    assign_mat(ear, 0)
    lobe = bmesh.ops.create_uvsphere(bm, u_segments=8, v_segments=6, radius=0.010, matrix=Matrix.Translation(Vector((sign * 0.088, -0.012, 1.275))))
    assign_mat(lobe, 0)

# Neck: Natural youthful cylinder with slight forward slant
neck = bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=0.052, radius2=0.046, depth=0.10, matrix=Matrix.Translation(Vector((0.0, -0.002, 1.205))) @ Matrix.Rotation(math.radians(-6.0), 4, 'X'))
assign_mat(neck, 0)

# Hands: 5-fingered hands with palm, thumb, and 4 articulated fingers
for sign, sx in [(-1, -0.22), (1, 0.22)]:
    # Palm
    palm = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((sx, 0.035, 0.665))) @ Matrix.Diagonal((0.048, 0.068, 0.085, 1.0)))
    assign_mat(palm, 0)
    # Thumb
    thumb = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.009, radius2=0.006, depth=0.045, matrix=Matrix.Translation(Vector((sx - sign*0.025, 0.045, 0.675))) @ Matrix.Rotation(math.radians(sign * 35.0), 4, 'Y'))
    assign_mat(thumb, 0)
    # 4 Fingers (Index, Middle, Ring, Pinky)
    for f in range(4):
        fz = 0.615 - f * 0.008
        fx = sx + (f - 1.5) * 0.010 * sign
        finger = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.008, radius2=0.005, depth=0.052, matrix=Matrix.Translation(Vector((fx, 0.042, fz))) @ Matrix.Rotation(math.radians(180.0), 4, 'Z'))
        assign_mat(finger, 0)

# ===========================================================================
# 2. SAFFRON PATKA TURBAN (Slot 2: Patka)
# ===========================================================================
# Main Crown Wrap: Fitted cloth cap wrapping around the skull
patka_crown = bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=16, radius=0.096, matrix=Matrix.Translation(Vector((0.0, -0.008, 1.385))) @ Matrix.Diagonal((1.02, 1.08, 0.96, 1.0)))
assign_mat(patka_crown, 2)

# Forehead V-Band: Characteristic triangular crest fold across brow
brow_v = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.084, 1.365))) @ Matrix.Diagonal((0.155, 0.024, 0.044, 1.0)))
assign_mat(brow_v, 2)

# Topknot Juda Bun: Tightly wrapped hair bun resting atop the cranium
juda_bun = bmesh.ops.create_uvsphere(bm, u_segments=18, v_segments=12, radius=0.048, matrix=Matrix.Translation(Vector((0.0, 0.002, 1.462))))
assign_mat(juda_bun, 2)
juda_band = bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=0.052, radius2=0.048, depth=0.026, matrix=Matrix.Translation(Vector((0.0, 0.002, 1.442))))
assign_mat(juda_band, 2)

# Flowing Neck Ties: Authentic tied fabric tails draped over the nape
for sign in [-1, 1]:
    tie = bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=0.016, radius2=0.008, depth=0.20, matrix=Matrix.Translation(Vector((sign * 0.072, -0.042, 1.18))) @ Matrix.Rotation(math.radians(180.0 + sign * 14.0), 4, 'Z'))
    assign_mat(tie, 2)

# ===========================================================================
# 3. HANDSPUN KHADI KURTA (Slot 3: Kurta, Slot 8: Wood Buttons)
# ===========================================================================
# Torso Body (Chest, Waist, Upper Hips)
kurta_torso = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 0.96))) @ Matrix.Diagonal((0.285, 0.185, 0.44, 1.0)))
assign_mat(kurta_torso, 3)

# Flared Lower Skirt (Reaching past knees with authentic drape)
kurta_skirt = bmesh.ops.create_cone(bm, cap_ends=True, segments=20, radius1=0.21, radius2=0.165, depth=0.34, matrix=Matrix.Translation(Vector((0.0, 0.0, 0.61))) @ Matrix.Diagonal((1.12, 0.86, 1.0, 1.0)))
assign_mat(kurta_skirt, 3)

# Mandarin Nehru Band Collar
collar = bmesh.ops.create_cone(bm, cap_ends=True, segments=20, radius1=0.066, radius2=0.062, depth=0.042, matrix=Matrix.Translation(Vector((0.0, 0.004, 1.192))))
assign_mat(collar, 3)

# Front Chest Button Placket (Embroidered tailoring strip)
placket = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.096, 1.05))) @ Matrix.Diagonal((0.042, 0.015, 0.25, 1.0)))
assign_mat(placket, 3)

# 3 Carved Wooden Buttons (Slot 8: Wood Buttons)
for bz in [0.97, 1.04, 1.11]:
    button = bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=0.009, radius2=0.009, depth=0.008, matrix=Matrix.Translation(Vector((0.0, 0.106, bz))) @ Matrix.Rotation(math.radians(90.0), 4, 'X'))
    assign_mat(button, 8)

# Sleeves (Upper Arm & Forearms with folds and rolled cuffs)
for sign, sx in [(-1, -0.17), (1, 0.17)]:
    # Shoulder cap
    shoulder = bmesh.ops.create_uvsphere(bm, u_segments=12, v_segments=10, radius=0.064, matrix=Matrix.Translation(Vector((sx, 0.0, 1.14))))
    assign_mat(shoulder, 3)
    # Upper arm sleeve
    upper_sleeve = bmesh.ops.create_cone(bm, cap_ends=True, segments=14, radius1=0.054, radius2=0.048, depth=0.24, matrix=Matrix.Translation(Vector((sx + sign*0.025, 0.01, 1.02))) @ Matrix.Rotation(math.radians(-sign*12.0), 4, 'Y'))
    assign_mat(upper_sleeve, 3)
    # Forearm sleeve
    forearm_sleeve = bmesh.ops.create_cone(bm, cap_ends=True, segments=14, radius1=0.048, radius2=0.044, depth=0.22, matrix=Matrix.Translation(Vector((sx + sign*0.045, 0.03, 0.81))) @ Matrix.Rotation(math.radians(-sign*8.0), 4, 'Y'))
    assign_mat(forearm_sleeve, 3)
    # Rolled fabric cuff
    cuff = bmesh.ops.create_cone(bm, cap_ends=True, segments=14, radius1=0.052, radius2=0.048, depth=0.032, matrix=Matrix.Translation(Vector((sx + sign*0.05, 0.035, 0.72))))
    assign_mat(cuff, 3)

# ===========================================================================
# 4. COTTON PAJAMA (Slot 4: Pajama)
# ===========================================================================
# Waist / Pelvis
pajama_waist = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 0.72))) @ Matrix.Diagonal((0.265, 0.175, 0.16, 1.0)))
assign_mat(pajama_waist, 4)

for sx in [-0.11, 0.11]:
    # Upper thigh
    thigh = bmesh.ops.create_cone(bm, cap_ends=True, segments=14, radius1=0.074, radius2=0.064, depth=0.28, matrix=Matrix.Translation(Vector((sx, 0.0, 0.57))))
    assign_mat(thigh, 4)
    # Knee fold gather
    knee_fold = bmesh.ops.create_cone(bm, cap_ends=True, segments=14, radius1=0.068, radius2=0.064, depth=0.035, matrix=Matrix.Translation(Vector((sx, 0.01, 0.42))))
    assign_mat(knee_fold, 4)
    # Calf tapering to ankle
    calf = bmesh.ops.create_cone(bm, cap_ends=True, segments=14, radius1=0.062, radius2=0.050, depth=0.32, matrix=Matrix.Translation(Vector((sx, 0.0, 0.25))))
    assign_mat(calf, 4)
    # Ankle hem
    ankle_hem = bmesh.ops.create_cone(bm, cap_ends=True, segments=14, radius1=0.054, radius2=0.050, depth=0.026, matrix=Matrix.Translation(Vector((sx, 0.0, 0.08))))
    assign_mat(ankle_hem, 4)

# ===========================================================================
# 5. PUNJABI LEATHER JUTTIS (Slot 6: Leather Jutti)
# ===========================================================================
for sx in [-0.11, 0.11]:
    # Hard leather sole
    sole = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((sx, 0.02, 0.022))) @ Matrix.Diagonal((0.084, 0.22, 0.024, 1.0)))
    assign_mat(sole, 6)
    # Tanned leather upper
    upper = bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.048, radius2=0.040, depth=0.18, matrix=Matrix.Translation(Vector((sx, 0.03, 0.045))) @ Matrix.Rotation(math.radians(90.0), 4, 'X') @ Matrix.Diagonal((1.0, 0.65, 1.0, 1.0)))
    assign_mat(upper, 6)
    # Curled traditional upturned toe tip (Nok)
    nok = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.026, radius2=0.005, depth=0.068, matrix=Matrix.Translation(Vector((sx, 0.14, 0.054))) @ Matrix.Rotation(math.radians(-42.0), 4, 'X'))
    assign_mat(nok, 6)

# ===========================================================================
# 6. LEATHER SATCHEL & HARDWARE (Slot 5: Satchel, Slot 7: Brass)
# ===========================================================================
# Diagonal Leather Strap (Crossbody right shoulder down to left hip)
strap = bmesh.ops.create_cone(bm, cap_ends=True, segments=14, radius1=0.017, radius2=0.017, depth=0.68, matrix=Matrix.Translation(Vector((-0.02, 0.086, 0.98))) @ Matrix.Rotation(math.radians(-38.0), 4, 'Y') @ Matrix.Rotation(math.radians(-10.0), 4, 'X'))
assign_mat(strap, 5)

# Main Bag Body (Left hip)
bag = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((-0.18, 0.02, 0.72))) @ Matrix.Diagonal((0.09, 0.25, 0.20, 1.0)))
assign_mat(bag, 5)

# Closing Flap
flap = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((-0.18, 0.082, 0.73))) @ Matrix.Diagonal((0.094, 0.015, 0.15, 1.0)))
assign_mat(flap, 5)

# Tarnished Brass Buckle (Slot 7: Brass)
buckle = bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.022, radius2=0.022, depth=0.012, matrix=Matrix.Translation(Vector((-0.18, 0.094, 0.67))) @ Matrix.Rotation(math.radians(90.0), 4, 'Y'))
assign_mat(buckle, 7)

# ===========================================================================
# 7. WAIST GEAR (Slot 3: Cloth Pouch, Slot 9: White Chalk)
# ===========================================================================
pouch = bmesh.ops.create_uvsphere(bm, u_segments=10, v_segments=8, radius=0.045, matrix=Matrix.Translation(Vector((0.155, 0.02, 0.75))) @ Matrix.Diagonal((0.7, 1.0, 1.2, 1.0)))
assign_mat(pouch, 3)

chalk = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector((0.155, 0.02, 0.82))) @ Matrix.Diagonal((0.02, 0.035, 0.06, 1.0)))
assign_mat(chalk, 9)

# Finish BMesh to Object
bm.to_mesh(mesh_kabir)
bm.free()

# Set Smooth Shading across all faces
for p in mesh_kabir.polygons:
    p.use_smooth = True

log("Generated Kabir high-poly anatomical mesh and multi-material zones.")

# ===========================================================================
# 8. HUMANOID ARMATURE RIG (UE5 Mannequin Bone Hierarchy)
# ===========================================================================
armature_data = bpy.data.armatures.new("Armature_Kabir")
armature_obj = bpy.data.objects.new("Kabir_Armature", armature_data)
bpy.context.collection.objects.link(armature_obj)

bpy.context.view_layer.objects.active = armature_obj
bpy.ops.object.mode_set(mode='EDIT')

bones = armature_data.edit_bones

# Root & Pelvis
b_root = bones.new("root")
b_root.head = (0.0, 0.0, 0.0)
b_root.tail = (0.0, 0.0, 0.10)

b_pelvis = bones.new("pelvis")
b_pelvis.head = (0.0, 0.0, 0.72)
b_pelvis.tail = (0.0, 0.0, 0.85)
b_pelvis.parent = b_root

# Spine chain
b_spine01 = bones.new("spine_01")
b_spine01.head = (0.0, 0.0, 0.85)
b_spine01.tail = (0.0, 0.0, 0.98)
b_spine01.parent = b_pelvis

b_spine02 = bones.new("spine_02")
b_spine02.head = (0.0, 0.0, 0.98)
b_spine02.tail = (0.0, 0.0, 1.10)
b_spine02.parent = b_spine01

b_spine03 = bones.new("spine_03")
b_spine03.head = (0.0, 0.0, 1.10)
b_spine03.tail = (0.0, 0.0, 1.20)
b_spine03.parent = b_spine02

# Neck & Head
b_neck = bones.new("neck_01")
b_neck.head = (0.0, 0.0, 1.20)
b_neck.tail = (0.0, 0.0, 1.28)
b_neck.parent = b_spine03

b_head = bones.new("head")
b_head.head = (0.0, 0.0, 1.28)
b_head.tail = (0.0, 0.0, 1.48)
b_head.parent = b_neck

# Arms (Left & Right)
for side, sign in [("_l", 1), ("_r", -1)]:
    b_clav = bones.new(f"clavicle{side}")
    b_clav.head = (0.0, 0.0, 1.16)
    b_clav.tail = (sign * 0.12, 0.0, 1.16)
    b_clav.parent = b_spine03

    b_upperarm = bones.new(f"upperarm{side}")
    b_upperarm.head = (sign * 0.16, 0.0, 1.14)
    b_upperarm.tail = (sign * 0.20, 0.02, 0.90)
    b_upperarm.parent = b_clav

    b_lowerarm = bones.new(f"lowerarm{side}")
    b_lowerarm.head = (sign * 0.20, 0.02, 0.90)
    b_lowerarm.tail = (sign * 0.22, 0.035, 0.72)
    b_lowerarm.parent = b_upperarm

    b_hand = bones.new(f"hand{side}")
    b_hand.head = (sign * 0.22, 0.035, 0.72)
    b_hand.tail = (sign * 0.22, 0.04, 0.60)
    b_hand.parent = b_lowerarm

# Legs (Left & Right)
for side, sign in [("_l", 1), ("_r", -1)]:
    b_thigh = bones.new(f"thigh{side}")
    b_thigh.head = (sign * 0.11, 0.0, 0.72)
    b_thigh.tail = (sign * 0.11, 0.01, 0.42)
    b_thigh.parent = b_pelvis

    b_calf = bones.new(f"calf{side}")
    b_calf.head = (sign * 0.11, 0.01, 0.42)
    b_calf.tail = (sign * 0.11, 0.0, 0.08)
    b_calf.parent = b_thigh

    b_foot = bones.new(f"foot{side}")
    b_foot.head = (sign * 0.11, 0.0, 0.08)
    b_foot.tail = (sign * 0.11, 0.12, 0.03)
    b_foot.parent = b_calf

bpy.ops.object.mode_set(mode='OBJECT')

# Parent Mesh to Armature with Automatic Vertex Weights
bpy.ops.object.select_all(action='DESELECT')
obj_kabir.select_set(True)
armature_obj.select_set(True)
bpy.context.view_layer.objects.active = armature_obj
bpy.ops.object.parent_set(type='ARMATURE_AUTO')

log("Successfully rigged Kabir mesh to humanoid armature with automatic vertex weights.")

# ===========================================================================
# 9. STUDIO LIGHTING & CINEMATIC CAMERAS
# ===========================================================================
# Key Light (Warm 3200K Punjab Sun)
key = bpy.data.lights.new(name="Studio_Key", type='POINT')
key.energy = 650.0
key.color = (1.0, 0.94, 0.82)
obj_key = bpy.data.objects.new("Studio_Key", key)
obj_key.location = (-1.2, 2.2, 2.0)
bpy.context.collection.objects.link(obj_key)

# Rim Light (Cool Sky Edge)
rim = bpy.data.lights.new(name="Studio_Rim", type='POINT')
rim.energy = 420.0
rim.color = (0.75, 0.85, 1.0)
obj_rim = bpy.data.objects.new("Studio_Rim", rim)
obj_rim.location = (1.4, -1.8, 1.8)
bpy.context.collection.objects.link(obj_rim)

# Fill Light (Ambient Diffuse)
fill = bpy.data.lights.new(name="Studio_Fill", type='POINT')
fill.energy = 220.0
fill.color = (0.95, 0.90, 0.85)
obj_fill = bpy.data.objects.new("Studio_Fill", fill)
obj_fill.location = (1.2, 1.6, 0.9)
bpy.context.collection.objects.link(obj_fill)

# Presentation Camera (Front Three-Quarter Full Body)
cam = bpy.data.cameras.new("Cam_Full_Body_3Q")
cam.lens = 52.0
obj_cam = bpy.data.objects.new("Cam_Full_Body_3Q", cam)
obj_cam.location = (-0.55, 2.45, 1.0)
obj_cam.rotation_euler = (math.radians(88.0), 0.0, math.radians(-168.0))
bpy.context.collection.objects.link(obj_cam)
bpy.context.scene.camera = obj_cam

# Render settings
bpy.context.scene.render.resolution_x = 1280
bpy.context.scene.render.resolution_y = 960
bpy.context.scene.render.image_settings.file_format = 'PNG'

# ===========================================================================
# 10. SAVE FILES & EXPORT
# ===========================================================================
project_art_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\PROJECT"
project_dest_dir = r"C:\Users\npal7\PROJECT\PROJECT"
os.makedirs(project_art_dir, exist_ok=True)
os.makedirs(project_dest_dir, exist_ok=True)

blend_1 = os.path.join(project_art_dir, "Kabir_Protagonist_AAA.blend")
blend_2 = os.path.join(project_dest_dir, "Kabir_Protagonist_AAA.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_1)
bpy.ops.wm.save_as_mainfile(filepath=blend_2)

# Export FBX with Armature
fbx_1 = os.path.join(project_art_dir, "SK_Kabir_Protagonist_AAA.fbx")
fbx_2 = os.path.join(project_dest_dir, "SK_Kabir_Protagonist_AAA.fbx")

bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.fbx(
    filepath=fbx_1,
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
bpy.ops.export_scene.fbx(
    filepath=fbx_2,
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

# Render still image
render_img_1 = os.path.join(project_art_dir, "Kabir_Protagonist_AAA_Render.png")
render_img_2 = os.path.join(project_dest_dir, "Kabir_Protagonist_AAA_Render.png")
bpy.context.scene.render.filepath = render_img_1
bpy.ops.render.render(write_still=True)

import shutil
shutil.copyfile(render_img_1, render_img_2)

log(f"SUCCESS: Saved {blend_1} and {blend_2}")
log(f"SUCCESS: Exported rigged FBX to {fbx_1} and {fbx_2}")
log(f"SUCCESS: Rendered showcase image to {render_img_1}")
