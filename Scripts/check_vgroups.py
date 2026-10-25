import bpy

blend_path = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v06\Kabir_v06_Heritage_Ages.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

body = bpy.data.objects.get("Kabir_v06_Adult_25_Body")
if body:
    print(f"Body modifiers: {[m.type for m in body.modifiers]}")
    print(f"Body vertex groups count: {len(body.vertex_groups)}")
    if body.vertex_groups:
        print(f"  First 10 vgroups: {[vg.name for vg in body.vertex_groups[:10]]}")
