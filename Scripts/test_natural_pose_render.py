import bpy
import math
import os

blend_path = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

arm = bpy.data.objects.get("v05_Kabir_Armature")
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')
pb = arm.pose.bones

for b in pb:
    b.rotation_mode = 'XYZ'
    b.location = (0, 0, 0)
    b.rotation_euler = (0, 0, 0)

# Set natural posture
# 1. Pelvis subtle child weight shift (left hip slightly supported)
pb["pelvis"].location = (0.008, 0.002, -0.004)
pb["pelvis"].rotation_euler = (math.radians(-1.0), math.radians(0.5), math.radians(1.2))

# 2. Spine counter-balance
pb["spine_01"].rotation_euler = (math.radians(1.5), 0.0, math.radians(-0.8))
pb["spine_02"].rotation_euler = (math.radians(1.0), 0.0, math.radians(-0.6))
pb["spine_03"].rotation_euler = (math.radians(-1.2), 0.0, math.radians(0.5))
pb["spine_04"].rotation_euler = (math.radians(-1.0), 0.0, 0.0)
pb["spine_05"].rotation_euler = (math.radians(-0.8), 0.0, 0.0)

# 3. Head & neck alert child observation
pb["neck_01"].rotation_euler = (math.radians(-1.5), math.radians(-0.8), math.radians(2.0))
pb["head"].rotation_euler = (math.radians(-2.0), math.radians(1.0), math.radians(3.5))

# 4. Arms hanging naturally alongside torso
# Left arm
pb["clavicle_l"].rotation_euler = (math.radians(-1.0), 0.0, math.radians(-2.0))
pb["upperarm_l"].rotation_euler = (math.radians(-6.0), math.radians(5.0), math.radians(28.0))
pb["lowerarm_l"].rotation_euler = (math.radians(-14.0), math.radians(8.0), math.radians(18.0))
pb["hand_l"].rotation_euler = (math.radians(-4.0), 0.0, math.radians(8.0))

# Right arm
pb["clavicle_r"].rotation_euler = (math.radians(-0.5), 0.0, math.radians(1.5))
pb["upperarm_r"].rotation_euler = (math.radians(-5.0), math.radians(-4.0), math.radians(-27.0))
pb["lowerarm_r"].rotation_euler = (math.radians(-12.0), math.radians(-6.0), math.radians(-16.0))
pb["hand_r"].rotation_euler = (math.radians(-4.0), 0.0, math.radians(-7.0))

# 5. Natural relaxed child finger curl
for side in ["_l", "_r"]:
    sign = 1.0 if side == "_l" else -1.0
    # Thumb
    if f"thumb_01{side}" in pb:
        pb[f"thumb_01{side}"].rotation_euler = (math.radians(8.0), math.radians(sign * 12.0), math.radians(sign * 10.0))
        pb[f"thumb_02{side}"].rotation_euler = (0.0, math.radians(sign * 15.0), 0.0)
        pb[f"thumb_03{side}"].rotation_euler = (0.0, math.radians(sign * 15.0), 0.0)
    # Fingers
    for f in ["index", "middle", "ring", "pinky"]:
        for idx, bend in [("01", 18.0), ("02", 24.0), ("03", 16.0)]:
            bname = f"{f}_{idx}{side}"
            if bname in pb:
                pb[bname].rotation_euler = (math.radians(bend), 0.0, math.radians(sign * 2.0))

# 6. Legs & Feet natural standing support
pb["thigh_l"].rotation_euler = (math.radians(1.0), 0.0, math.radians(-1.5))
pb["calf_l"].rotation_euler = (math.radians(-1.5), 0.0, 0.0)
pb["foot_l"].rotation_euler = (math.radians(0.5), 0.0, math.radians(1.0))

pb["thigh_r"].rotation_euler = (math.radians(-1.5), 0.0, math.radians(2.0))
pb["calf_r"].rotation_euler = (math.radians(1.0), 0.0, 0.0)
pb["foot_r"].rotation_euler = (math.radians(0.5), 0.0, math.radians(-1.0))

bpy.ops.object.mode_set(mode='OBJECT')

scene = bpy.context.scene
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100

cam = bpy.data.objects.get("Camera")
if not cam:
    cam_data = bpy.data.cameras.new("HeroCamera")
    cam = bpy.data.objects.new("Camera", cam_data)
    scene.collection.objects.link(cam)
scene.camera = cam

# Position camera for full-body three-quarter view
cam.location = (0.8, -2.6, 0.95)
cam.rotation_euler = (math.radians(82.0), 0.0, math.radians(18.0))
cam.data.lens = 55.0

out_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Tests\Screenshots"
out_file = os.path.join(out_dir, "blender_test_natural_pose.png")
scene.render.filepath = out_file
bpy.ops.render.render(write_still=True)
print(f"Rendered natural pose test to {out_file} ({os.path.getsize(out_file)} bytes)")
