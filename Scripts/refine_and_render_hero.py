import bpy
import math
import os
import random

blend_path = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

tex_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v05\Textures"

def s2l(val):
    return (val / 255.0) ** 2.2

# 1. Update Skin Texture: smooth nose, rich dark brown eyebrows, warm glowing bronze
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
        
        grain = (rng.random() - 0.5) * 0.006
        r = base_lr + grain
        g = base_lg + grain * 0.6
        b = base_lb + grain * 0.4
        
        # Smooth cheeks blush
        for cx_b in [0.38, 0.62]:
            dc_x = (nx - cx_b) / 0.08
            dc_y = (ny - 0.47) / 0.07
            if dc_x*dc_x + dc_y*dc_y < 1.0:
                blush = (1.0 - (dc_x*dc_x + dc_y*dc_y)) * 0.035
                r += blush * 1.3
                g += blush * 0.3
                b += blush * 0.1
                
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
            
        # Eyebrows: arched authentic dark espresso brown child brows (#1E1510)
        for bx_center in [0.400, 0.600]:
            bx_rel = (nx - bx_center) / 0.055
            arch = (1.0 - bx_rel * bx_rel) * 0.008 if abs(bx_rel) < 1.0 else 0.0
            by_rel = (ny - (0.528 + arch)) / 0.011
            if abs(bx_rel) < 1.0 and abs(by_rel) < 1.0:
                brow_w = (1.0 - bx_rel*bx_rel) * (1.0 - by_rel*by_rel)
                brow_lr = s2l(22)
                brow_lg = s2l(16)
                brow_lb = s2l(12)
                r = r * (1.0 - brow_w * 0.92) + brow_lr * (brow_w * 0.92)
                g = g * (1.0 - brow_w * 0.92) + brow_lg * (brow_w * 0.92)
                b = b * (1.0 - brow_w * 0.92) + brow_lb * (brow_w * 0.92)
                
        pixels[idx] = max(0.0, min(1.0, r))
        pixels[idx + 1] = max(0.0, min(1.0, g))
        pixels[idx + 2] = max(0.0, min(1.0, b))
        pixels[idx + 3] = 1.0

head_img.pixels = pixels
head_img.filepath_raw = head_tex_path
head_img.file_format = 'PNG'
head_img.save()

# 2. Update Hair Material: dark black-brown (#1A1412) with soft specular sheen
mat_hair = bpy.data.materials.get("M_Hair")
if mat_hair and mat_hair.node_tree:
    bsdf = mat_hair.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (s2l(24), s2l(18), s2l(15), 1.0)
        bsdf.inputs['Roughness'].default_value = 0.65

# 3. Reload textures
for img in bpy.data.images:
    if "Head_BC" in img.filepath or "Cloth_BC" in img.filepath or "Eye_BC" in img.filepath:
        img.reload()

# 4. Set Natural Idle Pose
arm = bpy.data.objects.get("v05_Kabir_Armature")
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')
pb = arm.pose.bones

for b in pb:
    b.rotation_mode = 'XYZ'
    b.location = (0, 0, 0)
    b.rotation_euler = (0, 0, 0)

# Natural posture
pb["pelvis"].location = (0.008, 0.002, -0.004)
pb["pelvis"].rotation_euler = (math.radians(-1.0), math.radians(0.5), math.radians(1.2))

pb["spine_01"].rotation_euler = (math.radians(1.5), 0.0, math.radians(-0.8))
pb["spine_02"].rotation_euler = (math.radians(1.0), 0.0, math.radians(-0.6))
pb["spine_03"].rotation_euler = (math.radians(-1.2), 0.0, math.radians(0.5))
pb["spine_04"].rotation_euler = (math.radians(-1.0), 0.0, 0.0)
pb["spine_05"].rotation_euler = (math.radians(-0.8), 0.0, 0.0)

pb["neck_01"].rotation_euler = (math.radians(-1.5), math.radians(-0.8), math.radians(2.0))
pb["head"].rotation_euler = (math.radians(-2.0), math.radians(1.0), math.radians(3.5))

# Arms hanging naturally alongside torso
pb["clavicle_l"].rotation_euler = (math.radians(-1.0), 0.0, math.radians(-2.0))
pb["upperarm_l"].rotation_euler = (math.radians(-6.0), math.radians(5.0), math.radians(28.0))
pb["lowerarm_l"].rotation_euler = (math.radians(-14.0), math.radians(8.0), math.radians(18.0))
pb["hand_l"].rotation_euler = (math.radians(-4.0), 0.0, math.radians(8.0))

pb["clavicle_r"].rotation_euler = (math.radians(-0.5), 0.0, math.radians(1.5))
pb["upperarm_r"].rotation_euler = (math.radians(-5.0), math.radians(-4.0), math.radians(-27.0))
pb["lowerarm_r"].rotation_euler = (math.radians(-12.0), math.radians(-6.0), math.radians(-16.0))
pb["hand_r"].rotation_euler = (math.radians(-4.0), 0.0, math.radians(-7.0))

# Fingers relaxed child curl
for side in ["_l", "_r"]:
    sign = 1.0 if side == "_l" else -1.0
    if f"thumb_01{side}" in pb:
        pb[f"thumb_01{side}"].rotation_euler = (math.radians(8.0), math.radians(sign * 12.0), math.radians(sign * 10.0))
        pb[f"thumb_02{side}"].rotation_euler = (0.0, math.radians(sign * 15.0), 0.0)
        pb[f"thumb_03{side}"].rotation_euler = (0.0, math.radians(sign * 15.0), 0.0)
    for f in ["index", "middle", "ring", "pinky"]:
        for idx, bend in [("01", 18.0), ("02", 24.0), ("03", 16.0)]:
            bname = f"{f}_{idx}{side}"
            if bname in pb:
                pb[bname].rotation_euler = (math.radians(bend), 0.0, math.radians(sign * 2.0))

pb["thigh_l"].rotation_euler = (math.radians(1.0), 0.0, math.radians(-1.5))
pb["calf_l"].rotation_euler = (math.radians(-1.5), 0.0, 0.0)
pb["foot_l"].rotation_euler = (math.radians(0.5), 0.0, math.radians(1.0))

pb["thigh_r"].rotation_euler = (math.radians(-1.5), 0.0, math.radians(2.0))
pb["calf_r"].rotation_euler = (math.radians(1.0), 0.0, 0.0)
pb["foot_r"].rotation_euler = (math.radians(0.5), 0.0, math.radians(-1.0))

bpy.ops.object.mode_set(mode='OBJECT')

# Save blend
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

# Render Full Body Hero View
scene = bpy.context.scene
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
cam = bpy.data.objects.get("Camera")
if not cam:
    cam = bpy.data.objects.get("HeroCamera")
if not cam:
    cam_data = bpy.data.cameras.new("HeroCamera")
    cam = bpy.data.objects.new("HeroCamera", cam_data)
    scene.collection.objects.link(cam)
scene.camera = cam

# Full body hero shot from front-three-quarter
cam.location = (0.45, -2.5, 0.82)
cam.rotation_euler = (math.radians(88.0), 0.0, math.radians(10.0))
cam.data.lens = 45.0

out_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Tests\Screenshots"
out_file = os.path.join(out_dir, "blender_test_full_hero.png")
scene.render.filepath = out_file
bpy.ops.render.render(write_still=True)
print(f"Rendered full body hero to {out_file}")
