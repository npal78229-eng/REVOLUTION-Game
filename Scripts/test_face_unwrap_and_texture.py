import bpy
import math
import os

blend_path = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

body = bpy.data.objects.get("v05_Kabir_Body")
assert body, "v05_Kabir_Body not found"

tex_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v05\Textures"
os.makedirs(tex_dir, exist_ok=True)
head_tex_path = os.path.join(tex_dir, "T_Kabir_Head_BC.png")

# 1. Create 2048x2048 high-fidelity face texture
size = 2048
head_img = bpy.data.images.new("T_Kabir_Head_BC_Authored", width=size, height=size, alpha=True)
pixels = [1.0] * (size * size * 4)

import random
rng = random.Random(19190413)

# Authentic 12yo North Indian / Punjabi child skin palette:
# Base wheatish bronze: RGB(179, 127, 86) -> (0.702, 0.498, 0.337)
base_r = 0.702
base_g = 0.498
base_b = 0.337

for y in range(size):
    ny = y / size # 0 at bottom, 1 at top
    for x in range(size):
        nx = x / size # 0 at left, 1 at right
        idx = (y * size + x) * 4
        
        # Micro pore grain
        grain = (rng.random() - 0.5) * 0.015
        
        # Base skin tone
        r = base_r + grain
        g = base_g + grain * 0.8
        b = base_b + grain * 0.6
        
        # Forehead warmth (ny: 0.56 - 0.70, nx: 0.35 - 0.65)
        df_y = (ny - 0.62) / 0.10
        df_x = (nx - 0.50) / 0.16
        df_dist = df_x*df_x + df_y*df_y
        if df_dist < 1.0:
            fw = (1.0 - df_dist) * 0.03
            r += fw * 1.1
            g += fw * 0.9
            b += fw * 0.4
            
        # Cheeks blush (ny: 0.44 - 0.50, nx: 0.35 - 0.43 and 0.57 - 0.65)
        for cx_b in [0.39, 0.61]:
            dc_x = (nx - cx_b) / 0.06
            dc_y = (ny - 0.47) / 0.05
            dc_dist = dc_x*dc_x + dc_y*dc_y
            if dc_dist < 1.0:
                blush = (1.0 - dc_dist) * 0.065
                r += blush * 1.3
                g += blush * 0.3
                b += blush * 0.1
                
        # Nose bridge warmth & tip
        dn_x = (nx - 0.50) / 0.035
        dn_y = (ny - 0.48) / 0.07
        if dn_x*dn_x + dn_y*dn_y < 1.0:
            nw = (1.0 - (dn_x*dn_x + dn_y*dn_y)) * 0.045
            r += nw * 1.2
            g += nw * 0.4
            b += nw * 0.1
            
        # Lips: natural child rosy-warm vermilion (ny: 0.40 - 0.435, nx: 0.43 - 0.57)
        dl_x = (nx - 0.50) / 0.065
        dl_y = (ny - 0.418) / 0.016
        dl_dist = dl_x*dl_x + dl_y*dl_y
        if dl_dist < 1.0:
            lip_w = (1.0 - dl_dist)
            # Lip tone: #9E4D48 -> (0.62, 0.30, 0.28)
            r = r * (1.0 - lip_w * 0.65) + 0.62 * (lip_w * 0.65)
            g = g * (1.0 - lip_w * 0.65) + 0.30 * (lip_w * 0.65)
            b = b * (1.0 - lip_w * 0.65) + 0.28 * (lip_w * 0.65)
            # Upper lip shadow
            if ny > 0.418:
                r -= lip_w * 0.04
                g -= lip_w * 0.03
                b -= lip_w * 0.02
                
        # Eyebrows: arched authentic dark brown/black child brows
        # Left brow: nx ~ 0.36 to 0.45, ny ~ 0.52 to 0.54
        # Right brow: nx ~ 0.55 to 0.64, ny ~ 0.52 to 0.54
        for bx_center, is_left in [(0.405, True), (0.595, False)]:
            bx_rel = (nx - bx_center) / 0.055
            # arch: slightly higher toward center/arch
            arch = (1.0 - bx_rel * bx_rel) * 0.008 if abs(bx_rel) < 1.0 else 0.0
            by_rel = (ny - (0.530 + arch)) / 0.012
            if abs(bx_rel) < 1.0 and abs(by_rel) < 1.0:
                brow_w = (1.0 - bx_rel*bx_rel) * (1.0 - by_rel*by_rel)
                # Brow color: #1E1510 -> (0.12, 0.08, 0.06)
                r = r * (1.0 - brow_w * 0.85) + 0.12 * (brow_w * 0.85)
                g = g * (1.0 - brow_w * 0.85) + 0.08 * (brow_w * 0.85)
                b = b * (1.0 - brow_w * 0.85) + 0.06 * (brow_w * 0.85)
                
        pixels[idx] = max(0.0, min(1.0, r))
        pixels[idx + 1] = max(0.0, min(1.0, g))
        pixels[idx + 2] = max(0.0, min(1.0, b))
        pixels[idx + 3] = 1.0

head_img.pixels = pixels
head_img.filepath_raw = head_tex_path
head_img.file_format = 'PNG'
head_img.save()
print(f"Saved authored 2K skin texture to {head_tex_path}")

# 2. Map frontal face UVs onto v05_Kabir_Body
uv_layer = body.data.uv_layers.active
if not uv_layer:
    uv_layer = body.data.uv_layers.new(name="UVMap")
uv_data = uv_layer.data

head_center_z = 1.330
head_center_y = -0.075
head_half_height = 0.160
head_half_width = 0.130

# Unproject/map vertices on the head
for poly in body.data.polygons:
    p_verts = [body.data.vertices[vi] for vi in poly.vertices]
    avg_z = sum(v.co.z for v in p_verts) / len(p_verts)
    avg_y = sum(v.co.y for v in p_verts) / len(p_verts)
    
    # Check if face/front of head: Z > 1.20 and Y < -0.01
    if avg_z > 1.20 and avg_y < -0.01:
        for loop_idx in poly.loop_indices:
            vi = body.data.loops[loop_idx].vertex_index
            v = body.data.vertices[vi]
            # U: centered at 0.50. Face width ~ 0.22m
            u = 0.50 - (v.co.x / (head_half_width * 2.2))
            # V: centered at 0.48. Face height ~ 0.26m
            v_coord = 0.48 + ((v.co.z - head_center_z) / (head_half_height * 2.2))
            uv_data[loop_idx].uv = (max(0.02, min(0.98, u)), max(0.02, min(0.98, v_coord)))
    elif avg_z > 1.20:
        # Back/sides of head: map into perimeter skin area
        for loop_idx in poly.loop_indices:
            uv_data[loop_idx].uv = (0.15, 0.85)

# Reload in material
mat_skin = bpy.data.materials.get("M_Kabir_Skin_PBR")
if mat_skin and mat_skin.node_tree:
    for node in mat_skin.node_tree.nodes:
        if node.type == 'TEX_IMAGE' and "Head_BC" in node.image.name:
            node.image = bpy.data.images.load(head_tex_path)
            node.image.reload()

# Also enhance Hair material: deep dark espresso brown with specular sheen
mat_hair = bpy.data.materials.get("M_Hair")
if mat_hair and mat_hair.node_tree:
    bsdf = mat_hair.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        # #1A1412 rich dark brown/black
        bsdf.inputs['Base Color'].default_value = (0.018, 0.014, 0.012, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.55
        bsdf.inputs['Anisotropic'].default_value = 0.65 if 'Anisotropic' in bsdf.inputs else 0.0

bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print("Saved blend with authored face texture and UV mapping.")
