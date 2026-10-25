import bpy
import math
import os

blend_path = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

# 1. Generate high-fidelity 1024x1024 eye texture
tex_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v05\Textures"
os.makedirs(tex_dir, exist_ok=True)
eye_tex_path = os.path.join(tex_dir, "T_Kabir_Eye_BC.png")

size = 1024
eye_img = bpy.data.images.new("T_Kabir_Eye_BC_New", width=size, height=size, alpha=True)
pixels = [1.0] * (size * size * 4)

cx = size / 2.0
cy = size / 2.0
r_pupil = size * 0.10
r_iris = size * 0.26
r_limbal = size * 0.285

for y in range(size):
    dy = y - cy
    for x in range(size):
        dx = x - cx
        dist = math.sqrt(dx*dx + dy*dy)
        idx = (y * size + x) * 4
        
        if dist <= r_pupil:
            # Pure black pupil
            r, g, b = 0.015, 0.012, 0.01
        elif dist <= r_iris:
            # Rich dark Indian chestnut brown iris with golden-amber striations
            t = (dist - r_pupil) / (r_iris - r_pupil)
            angle = math.atan2(dy, dx)
            striae = math.sin(angle * 24.0) * 0.04 + math.sin(angle * 48.0) * 0.02
            # Inner warm chestnut transitioning to deeper outer brown
            r = 0.22 + t * 0.08 + striae
            g = 0.12 + t * 0.04 + striae * 0.6
            b = 0.06 + t * 0.02 + striae * 0.3
        elif dist <= r_limbal:
            # Dark limbal ring
            t = (dist - r_iris) / (r_limbal - r_iris)
            r = 0.06 * (1.0 - t) + 0.70 * t
            g = 0.04 * (1.0 - t) + 0.68 * t
            b = 0.03 * (1.0 - t) + 0.66 * t
        else:
            # Natural sclera: soft warm off-white with micro-vessels
            sclera_edge = (dist - r_limbal) / (size * 0.5 - r_limbal)
            r = 0.88 - sclera_edge * 0.04
            g = 0.85 - sclera_edge * 0.06
            b = 0.82 - sclera_edge * 0.08
            
        pixels[idx] = max(0.0, min(1.0, r))
        pixels[idx + 1] = max(0.0, min(1.0, g))
        pixels[idx + 2] = max(0.0, min(1.0, b))
        pixels[idx + 3] = 1.0

eye_img.pixels = pixels
eye_img.filepath_raw = eye_tex_path
eye_img.file_format = 'PNG'
eye_img.save()
print(f"Saved high-fidelity eye texture to {eye_tex_path}")

# 2. Fix UV projection for both eyes
for eye_name in ["v05_Kabir_Eye_L", "v05_Kabir_Eye_R"]:
    eye = bpy.data.objects.get(eye_name)
    if not eye:
        continue
    verts = eye.data.vertices
    xs = [v.co.x for v in verts]
    ys = [v.co.y for v in verts]
    zs = [v.co.z for v in verts]
    ecx = (min(xs) + max(xs)) / 2.0
    ecz = (min(zs) + max(zs)) / 2.0
    radius = (max(xs) - min(xs)) / 2.0
    
    # Project UV:
    uv_layer = eye.data.uv_layers.active
    if not uv_layer:
        uv_layer = eye.data.uv_layers.new(name="UVMap")
    uv_data = uv_layer.data
    
    for poly in eye.data.polygons:
        for loop_idx in poly.loop_indices:
            vert_idx = eye.data.loops[loop_idx].vertex_index
            v = verts[vert_idx]
            # normalized coordinates relative to eye center
            # scale factor so iris takes up ~35-40% of the cornea
            scale = 1.15
            u = 0.5 - (v.co.x - ecx) / (radius * 2.0 * scale)
            v_coord = 0.5 + (v.co.z - ecz) / (radius * 2.0 * scale)
            
            # If vertex is on the back hemisphere (Y > center_y), tuck into sclera edge
            if v.co.y > -0.090:
                u = 0.05
                v_coord = 0.05
                
            uv_data[loop_idx].uv = (u, v_coord)
            
    print(f"Fixed frontal UV projection on {eye_name}")

# 3. Reload texture in Blender material
mat_eye = bpy.data.materials.get("M_Kabir_Eye_PBR")
if mat_eye and mat_eye.node_tree:
    for node in mat_eye.node_tree.nodes:
        if node.type == 'TEX_IMAGE':
            node.image = bpy.data.images.load(eye_tex_path)
            node.image.reload()
    bsdf = mat_eye.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Roughness'].default_value = 0.04
        bsdf.inputs['IOR'].default_value = 1.38

# Save blend
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print("Saved Kabir_v05.blend with updated eyes.")
