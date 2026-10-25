import bpy

blend_path = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

for l in bpy.data.lights:
    print(f"Light: {l.name}, type={l.type}, energy={l.energy}, color={l.color[:]}")
