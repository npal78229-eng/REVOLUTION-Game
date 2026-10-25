"""
Inspect v05 clothing meshes and UVs
"""
import bpy

blend_v05 = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v05\Kabir_v05.blend"
bpy.ops.wm.open_mainfile(filepath=blend_v05)
for name in ["v05_Kabir_Kurta", "v05_Kabir_Satchel", "v05_Kabir_Sandals", "v05_Kabir_Hair"]:
    obj = bpy.data.objects.get(name)
    if obj:
        print(f"{name}: verts={len(obj.data.vertices)}, uvs={[u.name for u in obj.data.uv_layers]}, mats={[m.name for m in obj.data.materials if m]}")
