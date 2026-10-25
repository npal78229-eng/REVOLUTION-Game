import bpy
import math
import os

blend_path = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

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

# Position camera for face close-up: looking at Z=1.33, Y=-0.08
cam.location = (0.0, -0.65, 1.33)
cam.rotation_euler = (math.radians(90.0), 0.0, 0.0)
cam.data.lens = 85.0

out_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Tests\Screenshots"
out_file = os.path.join(out_dir, "blender_test_face_eyes.png")
scene.render.filepath = out_file
bpy.ops.render.render(write_still=True)
print(f"Rendered face test to {out_file} ({os.path.getsize(out_file)} bytes)")
