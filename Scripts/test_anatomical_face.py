"""
High-Precision Anatomical Sculpted Face for 12-Year-Old Kabir
"""
import bpy
import bmesh
import math
from mathutils import Vector, Matrix

# Clear test objects
for o in ["Kabir_AAA_Head", "Kabir_Eye_L", "Kabir_Eye_R", "Cam_Test_Face", "Light_Key_Test", "Light_Fill_Test"]:
    if o in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[o], do_unlink=True)

# 1. Skin & Eye Materials
def get_or_create_mat(name, color, roughness=0.5, sss=0.0):
    mat = bpy.data.materials.get(name)
    if not mat:
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
    bsdf = next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Roughness"].default_value = roughness
        if "Subsurface Weight" in bsdf.inputs and sss > 0:
            bsdf.inputs["Subsurface Weight"].default_value = sss
    return mat

mat_skin = get_or_create_mat("M_Kabir_Skin_Sculpt", (0.68, 0.44, 0.30, 1.0), roughness=0.48, sss=0.25)
mat_sclera = get_or_create_mat("M_Kabir_Sclera_Sculpt", (0.94, 0.92, 0.90, 1.0), roughness=0.08)
mat_iris = get_or_create_mat("M_Kabir_Iris_Sculpt", (0.14, 0.08, 0.04, 1.0), roughness=0.05)

# 2. Build Anatomical Head Mesh
m_head = bpy.data.meshes.new("Kabir_AAA_Head_Mesh")
obj_head = bpy.data.objects.new("Kabir_AAA_Head", m_head)
bpy.context.collection.objects.link(obj_head)
obj_head.data.materials.append(mat_skin)

bm = bmesh.new()

# Grid of anatomical facial vertices
# Rows from forehead down to neck
# Columns from midline X=0 to lateral edge
# We will define right side (X >= 0) and mirror to left side (X < 0)

coords_right = {
    # (row, col): (x, y, z)
    # Row 0: Upper Forehead / Hairline (Z = 1.40)
    (0, 0): (0.000, 0.076, 1.400),
    (0, 1): (0.028, 0.074, 1.400),
    (0, 2): (0.054, 0.062, 1.395),
    (0, 3): (0.072, 0.038, 1.385),
    (0, 4): (0.078, -0.010, 1.380),
    (0, 5): (0.000, -0.090, 1.380), # Back head

    # Row 1: Mid Forehead (Z = 1.365)
    (1, 0): (0.000, 0.082, 1.365),
    (1, 1): (0.030, 0.080, 1.365),
    (1, 2): (0.058, 0.068, 1.360),
    (1, 3): (0.076, 0.042, 1.350),
    (1, 4): (0.082, -0.010, 1.345),
    (1, 5): (0.000, -0.095, 1.345),

    # Row 2: Brow Ridge & Glabella (Z = 1.338)
    (2, 0): (0.000, 0.085, 1.338),
    (2, 1): (0.032, 0.082, 1.340), # Brow peak
    (2, 2): (0.060, 0.068, 1.335), # Outer brow
    (2, 3): (0.078, 0.040, 1.325), # Temple
    (2, 4): (0.084, -0.012, 1.320), # Ear top
    (2, 5): (0.000, -0.096, 1.320),

    # Row 3: Eye Orbit Upper / Eyelid Fold (Z = 1.322)
    (3, 0): (0.000, 0.086, 1.322), # Nose bridge top
    (3, 1): (0.033, 0.072, 1.326), # Upper eyelid arch (in front of recessed eye at Y=0.060)
    (3, 2): (0.056, 0.065, 1.320), # Outer canthus
    (3, 3): (0.076, 0.038, 1.305),
    (3, 4): (0.086, -0.014, 1.300), # Ear canal
    (3, 5): (0.000, -0.095, 1.300),

    # Row 4: Eye Orbit Lower / Cheekbone (Z = 1.305)
    (4, 0): (0.000, 0.094, 1.305), # Mid nose bridge
    (4, 1): (0.033, 0.070, 1.306), # Lower eyelid rim
    (4, 2): (0.058, 0.062, 1.300), # Zygomatic arch
    (4, 3): (0.074, 0.032, 1.285),
    (4, 4): (0.084, -0.012, 1.275), # Ear lobe
    (4, 5): (0.000, -0.092, 1.275),

    # Row 5: Nose Tip & Cheeks (Z = 1.276)
    (5, 0): (0.000, 0.116, 1.276), # Pronasale (Nose Tip!)
    (5, 1): (0.018, 0.098, 1.272), # Nostril wing
    (5, 2): (0.052, 0.065, 1.270), # Full juvenile cheek
    (5, 3): (0.070, 0.026, 1.255),
    (5, 4): (0.076, -0.010, 1.245),
    (5, 5): (0.000, -0.088, 1.245),

    # Row 6: Subnasale / Upper Lip (Z = 1.248)
    (6, 0): (0.000, 0.092, 1.248), # Philtrum center
    (6, 1): (0.014, 0.090, 1.246), # Cupid's bow peak
    (6, 2): (0.030, 0.076, 1.240), # Mouth corner (commissure)
    (6, 3): (0.058, 0.040, 1.230), # Cheek corner
    (6, 4): (0.068, -0.008, 1.220), # Jaw angle
    (6, 5): (0.000, -0.080, 1.220),

    # Row 7: Lower Lip & Mentolabial (Z = 1.222)
    (7, 0): (0.000, 0.091, 1.222), # Lower lip center
    (7, 1): (0.014, 0.086, 1.220), # Lower lip lateral
    (7, 2): (0.028, 0.075, 1.226), # Lower corner
    (7, 3): (0.054, 0.038, 1.210),
    (7, 4): (0.064, -0.006, 1.200),
    (7, 5): (0.000, -0.075, 1.200),

    # Row 8: Chin & Mandible (Z = 1.188)
    (8, 0): (0.000, 0.086, 1.188), # Chin apex
    (8, 1): (0.016, 0.082, 1.188), # Chin pad
    (8, 2): (0.038, 0.060, 1.185), # Jawline curve
    (8, 3): (0.052, 0.030, 1.180),
    (8, 4): (0.060, -0.005, 1.175),
    (8, 5): (0.000, -0.070, 1.175),

    # Row 9: Upper Neck (Z = 1.145)
    (9, 0): (0.000, 0.054, 1.145), # Throat
    (9, 1): (0.022, 0.048, 1.145),
    (9, 2): (0.038, 0.038, 1.145),
    (9, 3): (0.048, 0.018, 1.145),
    (9, 4): (0.052, -0.005, 1.145),
    (9, 5): (0.000, -0.062, 1.145),
}

# Create vertices on both sides
v_grid = {} # (row, col, sign) -> bmesh vert
max_rows = 10
max_cols = 6

for row in range(max_rows):
    for col in range(max_cols):
        x, y, z = coords_right[(row, col)]
        if col == 0 or col == 5: # midline points
            v = bm.verts.new(Vector((0.0, y, z)))
            v_grid[(row, col, 1)] = v
            v_grid[(row, col, -1)] = v
        else:
            v_r = bm.verts.new(Vector((x, y, z)))
            v_l = bm.verts.new(Vector((-x, y, z)))
            v_grid[(row, col, 1)] = v_r
            v_grid[(row, col, -1)] = v_l

# Build quads
for sign in [1, -1]:
    for r in range(max_rows - 1):
        for c in range(max_cols - 1):
            v00 = v_grid[(r, c, sign)]
            v01 = v_grid[(r, c+1, sign)]
            v10 = v_grid[(r+1, c, sign)]
            v11 = v_grid[(r+1, c+1, sign)]
            
            # Winding order based on sign
            if sign == 1:
                bm.faces.new([v00, v01, v11, v10])
            else:
                bm.faces.new([v00, v10, v11, v01])

# Cap cranium top
crown_v = bm.verts.new(Vector((0.0, -0.010, 1.435)))
for sign in [1, -1]:
    for c in range(max_cols - 1):
        v1 = v_grid[(0, c, sign)]
        v2 = v_grid[(0, c+1, sign)]
        if sign == 1:
            bm.faces.new([crown_v, v1, v2])
        else:
            bm.faces.new([crown_v, v2, v1])

# Finish Head Mesh
bm.to_mesh(m_head)
bm.free()

for p in m_head.polygons:
    p.use_smooth = True

subsurf = obj_head.modifiers.new("Subdivision", 'SUBSURF')
subsurf.levels = 2
subsurf.render_levels = 2

# 3. Create Eyeballs nestled properly inside the orbits
for side, sign in [("L", 1), ("R", -1)]:
    m_eye = bpy.data.meshes.new(f"Eye_Mesh_{side}")
    o_eye = bpy.data.objects.new(f"Kabir_Eye_{side}", m_eye)
    bpy.context.collection.objects.link(o_eye)
    o_eye.data.materials.append(mat_sclera)
    o_eye.data.materials.append(mat_iris)
    
    bm_e = bmesh.new()
    # Eyeball center at (±0.033, 0.060, 1.315), radius 0.013m
    # Rotated so iris faces forward (+Y)
    sphere = bmesh.ops.create_uvsphere(bm_e, u_segments=24, v_segments=16, radius=0.0135, matrix=Matrix.Translation(Vector((sign * 0.033, 0.060, 1.315))) @ Matrix.Rotation(math.radians(90.0), 4, 'X'))
    
    # Assign iris material to front pole faces
    for f in bm_e.faces:
        if f.calc_center_median().y > 0.071:
            f.material_index = 1
        else:
            f.material_index = 0
            
    bm_e.to_mesh(m_eye)
    bm_e.free()
    for p in m_eye.polygons:
        p.use_smooth = True

# 4. Studio Lights & Portrait Camera
l_key = bpy.data.lights.new("Light_Key_Test", 'POINT')
l_key.energy = 650.0
l_key.color = (1.0, 0.94, 0.85)
o_lkey = bpy.data.objects.new("Light_Key_Test", l_key)
o_lkey.location = (-0.6, 1.2, 1.7)
bpy.context.collection.objects.link(o_lkey)

l_fill = bpy.data.lights.new("Light_Fill_Test", 'POINT')
l_fill.energy = 260.0
l_fill.color = (0.80, 0.88, 1.0)
o_lfill = bpy.data.objects.new("Light_Fill_Test", l_fill)
o_lfill.location = (0.8, 1.0, 1.3)
bpy.context.collection.objects.link(o_lfill)

c_data = bpy.data.cameras.new("Cam_Test_Face")
c_data.lens = 85.0
c_obj = bpy.data.objects.new("Cam_Test_Face", c_data)
c_obj.location = (-0.14, 0.95, 1.31)
c_obj.rotation_euler = (math.radians(88.0), 0.0, math.radians(-172.0))
bpy.context.collection.objects.link(c_obj)
bpy.context.scene.camera = c_obj

print("High-precision anatomical face generated successfully!")
