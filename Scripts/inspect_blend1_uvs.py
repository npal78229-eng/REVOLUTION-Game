import bpy

blend1_path = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend1"
bpy.ops.wm.open_mainfile(filepath=blend1_path)

body = bpy.data.objects.get("v05_Kabir_Body")
if body:
    print("=== Kabir_v05.blend1 BODY UVs ===")
    for uv_layer in body.data.uv_layers:
        xs = [d.uv.x for d in uv_layer.data]
        ys = [d.uv.y for d in uv_layer.data]
        print(f"Layer {uv_layer.name}: X=[{min(xs):.3f}, {max(xs):.3f}], Y=[{min(ys):.3f}, {max(ys):.3f}]")
