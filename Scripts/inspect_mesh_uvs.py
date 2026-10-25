import bpy

blend_path = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

for name in ["v05_Kabir_Eye_L", "v05_Kabir_Eye_R", "v05_Kabir_Hair", "v05_Kabir_Body"]:
    obj = bpy.data.objects.get(name)
    if obj:
        print(f"=== {name} ===")
        print(f"Materials: {[m.name for m in obj.data.materials]}")
        uvs = obj.data.uv_layers.active.data
        xs = [d.uv.x for d in uvs]
        ys = [d.uv.y for d in uvs]
        print(f"UV range: X=[{min(xs):.3f}, {max(xs):.3f}], Y=[{min(ys):.3f}, {max(ys):.3f}]")
