import bpy
import os

blend_path = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, 'RenderEngine') and 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100

# Ensure camera exists
cam = bpy.data.objects.get("Camera")
if not cam:
    cam_data = bpy.data.cameras.new("HeroCamera")
    cam = bpy.data.objects.new("Camera", cam_data)
    scene.collection.objects.link(cam)
scene.camera = cam

# Set front hero camera
cam.location = (0.0, -2.4, 1.05)
cam.rotation_euler = (1.5708, 0.0, 0.0) # looking +Y at chest height (Z=1.05)
cam.data.lens = 50.0

out_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Tests\Screenshots"
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, "blender_test_current_state.png")
scene.render.filepath = out_file
bpy.ops.render.render(write_still=True)
print(f"Rendered test state to {out_file} ({os.path.getsize(out_file)} bytes)")
