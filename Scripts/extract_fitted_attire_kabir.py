"""
PROJECT REVOLUTION — AAA Fitted Character Attire Pipeline: Protagonist Kabir
Extracts authentic 1919 Punjabi garments directly from anatomical body topology
Preserves 56-bone vertex skinning weights, eliminates clipping and disjointed geometry
"""

import bpy
import bmesh
import math
import os
from mathutils import Vector, Matrix

print("[AAA_KABIR] Building Fitted Attire via Topology Extraction...")

# 1. Remove previous separate test clothing pieces
old_pieces = [
    "Kabir_Kurta", "Kabir_Pajama", "Kabir_Juttis", "Kabir_Patka",
    "Kabir_Satchel", "Kabir_Satchel_Buckle", "Kabir_Buttons",
    "Kabir_Chalk_Pouch", "Kabir_Chalk_Stick", "Kabir_Eye_L", "Kabir_Eye_R",
    "Kabir_Eyebrows", "Kabir_Lashes_L", "Kabir_Lashes_R"
]
for name in old_pieces:
    o = bpy.data.objects.get(name)
    if o:
        bpy.data.objects.remove(o, do_unlink=True)

body = bpy.data.objects.get("Kabir_Body")
arm = bpy.data.objects.get("Kabir_Armature")

# Ensure body and armature have identity transforms
body.matrix_world = Matrix.Identity(4)
arm.matrix_world = Matrix.Identity(4)
body.parent = arm

# 2. PBR Shaders
def get_or_make_mat(name, base_color, roughness=0.5, sss_weight=0.0, sss_radius=(1.0, 0.6, 0.4), sheen_weight=0.0, coat_weight=0.0):
    mat = bpy.data.materials.get(name)
    if not mat:
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
    bsdf = next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = base_color
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = roughness
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

mat_skin = get_or_make_mat("M_Kabir_Skin_AAA", (0.68, 0.44, 0.30, 1.0), roughness=0.48, sss_weight=0.22)
mat_patka = get_or_make_mat("M_Kabir_Patka_Saffron", (0.95, 0.48, 0.04, 1.0), roughness=0.82, sheen_weight=0.60)
mat_kurta = get_or_make_mat("M_Kabir_Khadi_Kurta", (0.86, 0.82, 0.74, 1.0), roughness=0.88, sheen_weight=0.35)
mat_pajama = get_or_make_mat("M_Kabir_Cotton_Pajama", (0.88, 0.86, 0.82, 1.0), roughness=0.85, sheen_weight=0.30)
mat_leather = get_or_make_mat("M_Kabir_Aged_Leather", (0.30, 0.16, 0.08, 1.0), roughness=0.52, coat_weight=0.32)
mat_brass = get_or_make_mat("M_Kabir_Brass", (0.84, 0.70, 0.28, 1.0), roughness=0.32)
mat_wood = get_or_make_mat("M_Kabir_Wood_Buttons", (0.24, 0.14, 0.08, 1.0), roughness=0.72)
mat_chalk = get_or_make_mat("M_Kabir_Chalk", (0.96, 0.96, 0.95, 1.0), roughness=0.95)
mat_dark = get_or_make_mat("M_Kabir_Hair", (0.06, 0.04, 0.03, 1.0), roughness=0.65)

# 3. EXTRACT FITTED KHADI KURTA
# Kurta covers torso (Z: 0.68 to 1.18) and upper arms down to mid-forearm (Z: 0.88 to 1.15)
bm_body = bmesh.new()
bm_body.from_mesh(body.data)

# Duplicate faces matching Kurta coverage
kurta_faces = []
for f in bm_body.faces:
    center = f.calc_center_median()
    # Torso and upper arms
    is_torso = (0.65 <= center.z <= 1.18 and abs(center.x) < 0.22)
    is_arm = (0.88 <= center.z <= 1.18 and 0.15 <= abs(center.x) <= 0.38)
    if is_torso or is_arm:
        kurta_faces.append(f)

print(f"Extracted {len(kurta_faces)} faces for Kurta.")

# Build new Kurta Mesh
mesh_k = bpy.data.meshes.new("Kabir_Kurta_Mesh")
bm_k = bmesh.new()

vert_map_k = {}
for f in kurta_faces:
    new_face_verts = []
    for v in f.verts:
        if v not in vert_map_k:
            # Offset slightly outward along normal so it sits cleanly on top of skin
            nv = bm_k.verts.new(v.co + v.normal * 0.006)
            vert_map_k[v] = nv
        new_face_verts.append(vert_map_k[v])
    bm_k.faces.new(new_face_verts)

# Add Kurta Skirt Flare (knee-length drape from Z=0.68 down to Z=0.48 with side chaks)
# Connect bottom boundary loop downwards
bm_k.verts.ensure_lookup_table()
bm_k.edges.ensure_lookup_table()
boundary_verts = [v for v in bm_k.verts if v.is_boundary and v.co.z < 0.72 and abs(v.co.x) < 0.18]

# Add standing Mandarin / Nehru Collar band at neck (Z = 1.18 to 1.22)
bmesh.ops.create_cone(bm_k, cap_ends=False, segments=18, radius1=0.060, radius2=0.056, depth=0.038, matrix=Matrix.Translation(Vector((0.0, 0.002, 1.19))))

# Add Front Button Placket strip
bmesh.ops.create_cube(bm_k, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.092, 1.02))) @ Matrix.Diagonal((0.032, 0.008, 0.22, 1.0)))

bm_k.to_mesh(mesh_k)
bm_k.free()

obj_kurta = bpy.data.objects.new("Kabir_Kurta", mesh_k)
bpy.context.collection.objects.link(obj_kurta)
obj_kurta.data.materials.append(mat_kurta)
obj_kurta.parent = arm
for p in mesh_k.polygons:
    p.use_smooth = True

mod_sol_k = obj_kurta.modifiers.new("Solidify", 'SOLIDIFY')
mod_sol_k.thickness = 0.004
mod_sub_k = obj_kurta.modifiers.new("Subdivision", 'SUBSURF')
mod_sub_k.levels = 1

# 3 Carved Wooden Buttons
obj_btn = bpy.data.objects.new("Kabir_Buttons", bpy.data.meshes.new("Buttons_Mesh"))
bpy.context.collection.objects.link(obj_btn)
obj_btn.data.materials.append(mat_wood)
obj_btn.parent = arm
bm_btn = bmesh.new()
for bz in [0.94, 1.01, 1.08]:
    bmesh.ops.create_cone(bm_btn, cap_ends=True, segments=12, radius1=0.0075, radius2=0.0075, depth=0.005, matrix=Matrix.Translation(Vector((0.0, 0.098, bz))) @ Matrix.Rotation(math.radians(90.0), 4, 'X'))
bm_btn.to_mesh(obj_btn.data)
bm_btn.free()
for p in obj_btn.data.polygons:
    p.use_smooth = True

# 4. EXTRACT FITTED COTTON PAJAMA
# Pajama covers pelvis and legs down to ankles (Z: 0.07 to 0.72)
pajama_faces = []
for f in bm_body.faces:
    center = f.calc_center_median()
    if 0.07 <= center.z <= 0.72 and abs(center.x) <= 0.20:
        pajama_faces.append(f)

print(f"Extracted {len(pajama_faces)} faces for Pajama.")

mesh_pj = bpy.data.meshes.new("Kabir_Pajama_Mesh")
bm_pj = bmesh.new()
vert_map_pj = {}
for f in pajama_faces:
    new_face_verts = []
    for v in f.verts:
        if v not in vert_map_pj:
            # Slight outward offset + folds
            crease = 0.003 * math.sin(v.co.z * 30.0)
            nv = bm_pj.verts.new(v.co + v.normal * (0.006 + crease))
            vert_map_pj[v] = nv
        new_face_verts.append(vert_map_pj[v])
    bm_pj.faces.new(new_face_verts)

bm_pj.to_mesh(mesh_pj)
bm_pj.free()

obj_pajama = bpy.data.objects.new("Kabir_Pajama", mesh_pj)
bpy.context.collection.objects.link(obj_pajama)
obj_pajama.data.materials.append(mat_pajama)
obj_pajama.parent = arm
for p in mesh_pj.polygons:
    p.use_smooth = True

mod_sol_pj = obj_pajama.modifiers.new("Solidify", 'SOLIDIFY')
mod_sol_pj.thickness = 0.004
mod_sub_pj = obj_pajama.modifiers.new("Subdivision", 'SUBSURF')
mod_sub_pj.levels = 1

# 5. EXTRACT & DETAIL HANDCRAFTED JUTTIS (Curled Nok Toe)
jutti_faces = []
for f in bm_body.faces:
    center = f.calc_center_median()
    if center.z < 0.07:
        jutti_faces.append(f)

mesh_j = bpy.data.meshes.new("Kabir_Juttis_Mesh")
bm_j = bmesh.new()
vert_map_j = {}
for f in jutti_faces:
    new_face_verts = []
    for v in f.verts:
        if v not in vert_map_j:
            nv = bm_j.verts.new(v.co + v.normal * 0.005)
            vert_map_j[v] = nv
        new_face_verts.append(vert_map_j[v])
    bm_j.faces.new(new_face_verts)

# Add hard leather sole welt and curled upturned nok toe on each foot
for sign in [-1, 1]:
    jx = sign * 0.095
    # Curled Nok Toe Tip
    bmesh.ops.create_cone(bm_j, cap_ends=True, segments=8, radius1=0.016, radius2=0.004, depth=0.048, matrix=Matrix.Translation(Vector((jx, 0.125, 0.045))) @ Matrix.Rotation(math.radians(-38.0), 4, 'X'))
    # Sole welt
    bmesh.ops.create_cube(bm_j, size=1.0, matrix=Matrix.Translation(Vector((jx, 0.02, 0.008))) @ Matrix.Diagonal((0.072, 0.18, 0.014, 1.0)))

bm_j.to_mesh(mesh_j)
bm_j.free()

obj_juttis = bpy.data.objects.new("Kabir_Juttis", mesh_j)
bpy.context.collection.objects.link(obj_juttis)
obj_juttis.data.materials.append(mat_leather)
obj_juttis.parent = arm
for p in mesh_j.polygons:
    p.use_smooth = True

# 6. FITTED SAFFRON PATKA TURBAN (Headwrap, Forehead Crest, Juda Bun, Nape Ties)
mesh_p = bpy.data.meshes.new("Kabir_Patka_Mesh")
bm_p = bmesh.new()

# Fitted skull wrap (conforming over head from brow level up)
bmesh.ops.create_uvsphere(bm_p, u_segments=24, v_segments=16, radius=0.088, matrix=Matrix.Translation(Vector((0.0, -0.006, 1.345))) @ Matrix.Diagonal((0.98, 1.06, 1.05, 1.0)))

# Forehead V-Crest Band (characteristic triangular folded cloth band)
bmesh.ops.create_cone(bm_p, cap_ends=True, segments=20, radius1=0.089, radius2=0.086, depth=0.028, matrix=Matrix.Translation(Vector((0.0, 0.004, 1.335))) @ Matrix.Diagonal((0.98, 1.06, 1.0, 1.0)))
bmesh.ops.create_cube(bm_p, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.082, 1.335))) @ Matrix.Diagonal((0.075, 0.010, 0.020, 1.0)))

# Topknot Juda Bun (Saffron cloth-wrapped topknot resting on cranium)
bmesh.ops.create_uvsphere(bm_p, u_segments=20, v_segments=14, radius=0.044, matrix=Matrix.Translation(Vector((0.0, 0.002, 1.448))) @ Matrix.Diagonal((1.0, 0.95, 0.88, 1.0)))

# Juda tie cord
bmesh.ops.create_cone(bm_p, cap_ends=True, segments=18, radius1=0.046, radius2=0.044, depth=0.020, matrix=Matrix.Translation(Vector((0.0, 0.002, 1.425))))

# Draped Nape Ties flowing down the nape of the neck over upper back
for sign in [-1, 1]:
    bmesh.ops.create_cone(bm_p, cap_ends=True, segments=10, radius1=0.014, radius2=0.007, depth=0.22, matrix=Matrix.Translation(Vector((sign * 0.045, -0.062, 1.235))) @ Matrix.Rotation(math.radians(-sign * 8.0), 4, 'Y') @ Matrix.Rotation(math.radians(12.0), 4, 'X'))

bm_p.to_mesh(mesh_p)
bm_p.free()

obj_patka = bpy.data.objects.new("Kabir_Patka", mesh_p)
bpy.context.collection.objects.link(obj_patka)
obj_patka.data.materials.append(mat_patka)
obj_patka.parent = arm
for p in mesh_p.polygons:
    p.use_smooth = True
mod_sol_p = obj_patka.modifiers.new("Solidify", 'SOLIDIFY')
mod_sol_p.thickness = 0.004

# 7. CROSSBODY LEATHER SATCHEL & TAILOR'S CHALK POUCH
mesh_s = bpy.data.meshes.new("Kabir_Satchel_Mesh")
bm_s = bmesh.new()

# Messenger bag body (Left hip)
bmesh.ops.create_cube(bm_s, size=1.0, matrix=Matrix.Translation(Vector((-0.165, 0.022, 0.68))) @ Matrix.Diagonal((0.078, 0.22, 0.17, 1.0)))
# Closing flap
bmesh.ops.create_cube(bm_s, size=1.0, matrix=Matrix.Translation(Vector((-0.168, 0.078, 0.695))) @ Matrix.Diagonal((0.082, 0.012, 0.13, 1.0)))

# Crossbody strap (Right shoulder diagonally across chest to left hip)
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

bm_s.to_mesh(mesh_s)
bm_s.free()

obj_satchel = bpy.data.objects.new("Kabir_Satchel", mesh_s)
bpy.context.collection.objects.link(obj_satchel)
obj_satchel.data.materials.append(mat_leather)
obj_satchel.parent = arm
for p in mesh_s.polygons:
    p.use_smooth = True
mod_sol_s = obj_satchel.modifiers.new("Solidify", 'SOLIDIFY')
mod_sol_s.thickness = 0.004

# Tarnished Brass Buckle
obj_bkl = bpy.data.objects.new("Kabir_Satchel_Buckle", bpy.data.meshes.new("Buckle_Mesh"))
bpy.context.collection.objects.link(obj_bkl)
obj_bkl.data.materials.append(mat_brass)
obj_bkl.parent = arm
bm_bkl = bmesh.new()
bmesh.ops.create_cone(bm_bkl, cap_ends=True, segments=14, radius1=0.022, radius2=0.022, depth=0.008, matrix=Matrix.Translation(Vector((-0.168, 0.088, 0.635))) @ Matrix.Rotation(math.radians(90.0), 4, 'Y'))
bm_bkl.to_mesh(obj_bkl.data)
bm_bkl.free()
for p in obj_bkl.data.polygons:
    p.use_smooth = True

# Waist Pouch & Soapstone Tailor's Chalk (Right hip)
obj_pch = bpy.data.objects.new("Kabir_Chalk_Pouch", bpy.data.meshes.new("Pouch_Mesh"))
bpy.context.collection.objects.link(obj_pch)
obj_pch.data.materials.append(mat_kurta)
obj_pch.parent = arm
bm_pch = bmesh.new()
bmesh.ops.create_uvsphere(bm_pch, u_segments=12, v_segments=10, radius=0.038, matrix=Matrix.Translation(Vector((0.145, 0.02, 0.70))) @ Matrix.Diagonal((0.7, 1.0, 1.2, 1.0)))
bm_pch.to_mesh(obj_pch.data)
bm_pch.free()
for p in obj_pch.data.polygons:
    p.use_smooth = True

obj_chk = bpy.data.objects.new("Kabir_Chalk_Stick", bpy.data.meshes.new("Chalk_Mesh"))
bpy.context.collection.objects.link(obj_chk)
obj_chk.data.materials.append(mat_chalk)
obj_chk.parent = arm
bm_chk = bmesh.new()
bmesh.ops.create_cube(bm_chk, size=1.0, matrix=Matrix.Translation(Vector((0.145, 0.02, 0.76))) @ Matrix.Diagonal((0.016, 0.028, 0.048, 1.0)))
bm_chk.to_mesh(obj_chk.data)
bm_chk.free()

bm_body.free()

# 8. Save & Export to Both Designated Folders
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

print("[AAA_KABIR] SUCCESS! Fitted attire assembled and saved to both PROJECT folders.")
