import bpy
import math
import os
import random

blend_path = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

body = bpy.data.objects.get("v05_Kabir_Body")
kurta = bpy.data.objects.get("v05_Kabir_Kurta")
shorts = bpy.data.objects.get("v05_Kabir_Shorts")
satchel = bpy.data.objects.get("v05_Kabir_Satchel")
hair = bpy.data.objects.get("v05_Kabir_Hair")

tex_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v05\Textures"
os.makedirs(tex_dir, exist_ok=True)

# Helper: sRGB 0-255 to Linear float
def s2l(val):
    return (val / 255.0) ** 2.2

# 1. FIX WRIST VERTEX WEIGHTS ON BODY
vg_map = {vg.name: vg.index for vg in body.vertex_groups}
# Clean right wrist (X near -0.38, Z near 0.74)
for v in body.data.vertices:
    for side, sign in [("_r", -1.0), ("_l", 1.0)]:
        dx = v.co.x - (sign * 0.38)
        dy = v.co.y - (-0.01)
        dz = v.co.z - 0.74
        dist = (dx*dx + dy*dy + dz*dz)**0.5
        if dist < 0.08:
            # Remove metacarpal and finger weights from wrist vertices
            for vg_name in [f"index_metacarpal{side}", f"middle_metacarpal{side}", f"ring_metacarpal{side}", f"pinky_metacarpal{side}", f"thumb_01{side}"]:
                if vg_name in vg_map:
                    body.vertex_groups[vg_name].remove([v.index])
            # Re-normalize between lowerarm and hand based on X position
            t = (v.co.x * sign - 0.34) / 0.08 # 0 at lowerarm, 1 at hand
            t = max(0.0, min(1.0, t))
            hand_vg = f"hand{side}"
            arm_vg = f"lowerarm{side}"
            if hand_vg in vg_map and arm_vg in vg_map:
                body.vertex_groups[arm_vg].add([v.index], 1.0 - t, 'REPLACE')
                body.vertex_groups[hand_vg].add([v.index], t, 'REPLACE')

print("Normalized wrist skin weights smoothly between lowerarm and hand.")

# 2. GENERATE RICH WHEATISH-BRONZE PUNJABI SKIN TEXTURE (2048x2048)
head_tex_path = os.path.join(tex_dir, "T_Kabir_Head_BC.png")
size = 2048
head_img = bpy.data.images.get("T_Kabir_Head_BC_Authored")
if not head_img:
    head_img = bpy.data.images.new("T_Kabir_Head_BC_Authored", width=size, height=size, alpha=True)
pixels = [1.0] * (size * size * 4)

rng = random.Random(19190413)

# Authentic Punjabi wheatish bronze tone: #B37F56 -> sRGB(179, 127, 86)
base_lr = s2l(179)
base_lg = s2l(127)
base_lb = s2l(86)

for y in range(size):
    ny = y / size
    for x in range(size):
        nx = x / size
        idx = (y * size + x) * 4
        
        grain = (rng.random() - 0.5) * 0.008
        
        r = base_lr + grain
        g = base_lg + grain * 0.6
        b = base_lb + grain * 0.4
        
        # Forehead warmth
        df_y = (ny - 0.62) / 0.12
        df_x = (nx - 0.50) / 0.18
        if df_x*df_x + df_y*df_y < 1.0:
            fw = (1.0 - (df_x*df_x + df_y*df_y)) * 0.025
            r += fw * 1.1
            g += fw * 0.8
            b += fw * 0.4
            
        # Cheeks blush (smooth natural healthy circulation)
        for cx_b in [0.38, 0.62]:
            dc_x = (nx - cx_b) / 0.07
            dc_y = (ny - 0.47) / 0.06
            if dc_x*dc_x + dc_y*dc_y < 1.0:
                blush = (1.0 - (dc_x*dc_x + dc_y*dc_y)) * 0.045
                r += blush * 1.4
                g += blush * 0.4
                b += blush * 0.2
                
        # Nose bridge soft gradient
        dn_x = (nx - 0.50) / 0.04
        dn_y = (ny - 0.49) / 0.08
        if dn_x*dn_x + dn_y*dn_y < 1.0:
            nw = (1.0 - (dn_x*dn_x + dn_y*dn_y)) * 0.02
            r += nw * 1.2
            g += nw * 0.5
            b += nw * 0.2
            
        # Lips: natural warm child vermilion (#9E4D48 -> sRGB 158, 77, 72)
        dl_x = (nx - 0.50) / 0.065
        dl_y = (ny - 0.418) / 0.018
        dl_dist = dl_x*dl_x + dl_y*dl_y
        if dl_dist < 1.0:
            lip_w = (1.0 - dl_dist)
            lip_lr = s2l(158)
            lip_lg = s2l(77)
            lip_lb = s2l(72)
            r = r * (1.0 - lip_w * 0.70) + lip_lr * (lip_w * 0.70)
            g = g * (1.0 - lip_w * 0.70) + lip_lg * (lip_w * 0.70)
            b = b * (1.0 - lip_w * 0.70) + lip_lb * (lip_w * 0.70)
            
        # Eyebrows: arched authentic dark brown/black child brows (#231712 -> sRGB 35, 23, 18)
        # Positioned right over the brow ridge at ny: 0.522 - 0.540
        for bx_center, is_left in [(0.400, True), (0.600, False)]:
            bx_rel = (nx - bx_center) / 0.052
            arch = (1.0 - bx_rel * bx_rel) * 0.007 if abs(bx_rel) < 1.0 else 0.0
            by_rel = (ny - (0.528 + arch)) / 0.010
            if abs(bx_rel) < 1.0 and abs(by_rel) < 1.0:
                brow_w = (1.0 - bx_rel*bx_rel) * (1.0 - by_rel*by_rel)
                brow_lr = s2l(25)
                brow_lg = s2l(18)
                brow_lb = s2l(14)
                r = r * (1.0 - brow_w * 0.90) + brow_lr * (brow_w * 0.90)
                g = g * (1.0 - brow_w * 0.90) + brow_lg * (brow_w * 0.90)
                b = b * (1.0 - brow_w * 0.90) + brow_lb * (brow_w * 0.90)
                
        pixels[idx] = max(0.0, min(1.0, r))
        pixels[idx + 1] = max(0.0, min(1.0, g))
        pixels[idx + 2] = max(0.0, min(1.0, b))
        pixels[idx + 3] = 1.0

head_img.pixels = pixels
head_img.filepath_raw = head_tex_path
head_img.file_format = 'PNG'
head_img.save()
print(f"Saved linear-correct Punjabi child skin texture to {head_tex_path}")

# 3. GENERATE FINE HANDSPUN UNBLEACHED KHADI COTTON TEXTURE (1024x1024)
cloth_tex_path = os.path.join(tex_dir, "T_Kabir_Cloth_BC.png")
c_size = 1024
cloth_img = bpy.data.images.get("T_Kabir_Cloth_BC_Authored")
if not cloth_img:
    cloth_img = bpy.data.images.new("T_Kabir_Cloth_BC_Authored", width=c_size, height=c_size, alpha=True)
c_pixels = [1.0] * (c_size * c_size * 4)

# Ecru unbleached khadi: #E8DEC8 -> sRGB(232, 222, 200)
khadi_lr = s2l(232)
khadi_lg = s2l(222)
khadi_lb = s2l(200)

for y in range(c_size):
    # Fine weave: micro-frequency thread pitch = 1.5 pixels
    warp = math.sin(y * 1.8) * 0.008
    for x in range(c_size):
        weft = math.sin(x * 1.8) * 0.008
        idx = (y * c_size + x) * 4
        # Subtle slub handloom irregularity
        slub = (rng.random() - 0.5) * 0.012
        r = khadi_lr + warp + weft + slub
        g = khadi_lg + warp * 0.9 + weft * 0.9 + slub * 0.9
        b = khadi_lb + warp * 0.8 + weft * 0.8 + slub * 0.8
        c_pixels[idx] = max(0.0, min(1.0, r))
        c_pixels[idx + 1] = max(0.0, min(1.0, g))
        c_pixels[idx + 2] = max(0.0, min(1.0, b))
        c_pixels[idx + 3] = 1.0

cloth_img.pixels = c_pixels
cloth_img.filepath_raw = cloth_tex_path
cloth_img.file_format = 'PNG'
cloth_img.save()
print(f"Saved fine handspun khadi texture to {cloth_tex_path}")

# 4. Reload all textures in Blender materials
for img in bpy.data.images:
    if any(k in img.filepath for k in ["Head_BC", "Cloth_BC", "Eye_BC"]):
        img.reload()

# Save blend file
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print("Saved Kabir_v05.blend with updated textures and normalized weights.")
