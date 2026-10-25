import bpy
import math
import os

blend_path = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

# 1. Enhance Satchel: Add 3D thickness so it's an authentic leather bag
satchel = bpy.data.objects.get("v05_Kabir_Satchel")
if satchel:
    # Check if solidify modifier exists
    solid = satchel.modifiers.get("Solidify")
    if not solid:
        solid = satchel.modifiers.new("Solidify", 'SOLIDIFY')
        solid.thickness = 0.025 # 2.5 cm depth
        solid.offset = 1.0
        print("Added Solidify modifier to v05_Kabir_Satchel.")

# 2. Clean cylindrical/box UV unwrap on Kurta and Shorts for uniform khadi drape
for c_name in ["v05_Kabir_Kurta", "v05_Kabir_Shorts"]:
    obj = bpy.data.objects.get(c_name)
    if obj:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        # Cylinder projection or smart project with angle limit 75 deg and margin 0.01
        bpy.ops.uv.smart_project(angle_limit=math.radians(75.0), island_margin=0.01)
        bpy.ops.object.mode_set(mode='OBJECT')
        print(f"Cleaned UV mapping on {c_name}.")

# 3. Position camera for full-body view from hair to sandals
scene = bpy.context.scene
cam = None
for obj in bpy.data.objects:
    if obj.type == 'CAMERA':
        cam = obj
        break
if not cam:
    cam_data = bpy.data.cameras.new("HeroCamera")
    cam = bpy.data.objects.new("HeroCamera", cam_data)
    scene.collection.objects.link(cam)
scene.camera = cam

# Frame 144cm character perfectly (Z from 0.0 to 1.44)
cam.location = (0.55, -2.85, 0.76)
cam.rotation_euler = (math.radians(88.5), 0.0, math.radians(11.0))
cam.data.lens = 42.0

bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print("Saved blend with enhanced clothing and camera.")

# Render full body test
out_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Tests\Screenshots"
out_file = os.path.join(out_dir, "blender_test_full_hero.png")
scene.render.filepath = out_file
bpy.ops.render.render(write_still=True)
print(f"Rendered full body hero to {out_file}")
