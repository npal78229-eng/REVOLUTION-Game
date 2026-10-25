"""
Compare v05 and v06 meshes and UVs
"""
import bpy

blend_v05 = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v05\Kabir_v05.blend"
bpy.ops.wm.open_mainfile(filepath=blend_v05)
b05 = bpy.data.objects.get("v05_Kabir_Body")
print(f"v05 body verts: {len(b05.data.vertices)}, uvs: {[u.name for u in b05.data.uv_layers]}")

blend_v06 = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v06\Kabir_v06_Heritage_Ages.blend"
bpy.ops.wm.open_mainfile(filepath=blend_v06)
b06 = bpy.data.objects.get("Kabir_v06_Adult_25_Body")
print(f"v06 body verts: {len(b06.data.vertices)}, uvs: {[u.name for u in b06.data.uv_layers]}")
