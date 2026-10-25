"""
Inspect Kabir_v06 UVs and meshes
"""
import bpy

blend_path = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v06\Kabir_v06_Heritage_Ages.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

print("=== KABIR_v06 OBJECTS & UVs ===")
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        uvs = [uv.name for uv in obj.data.uv_layers]
        mats = [m.name for m in obj.data.materials if m]
        print(f"Mesh: {obj.name} | Verts: {len(obj.data.vertices)} | UVs: {uvs} | Mats: {mats}")
