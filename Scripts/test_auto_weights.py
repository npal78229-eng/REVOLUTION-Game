import bpy

blend_path = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v06\Kabir_v06_Heritage_Ages.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

arm = bpy.data.objects.get("Kabir_v06_Adult_25_Armature")
body = bpy.data.objects.get("Kabir_v06_Adult_25_Body")

# Clear selection
bpy.ops.object.select_all(action='DESELECT')
body.select_set(True)
arm.select_set(True)
bpy.context.view_layer.objects.active = arm

try:
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    print("SUCCESS: Parented body to armature with automatic weights!")
    print(f"Vertex groups count on body: {len(body.vertex_groups)}")
    for vg in body.vertex_groups:
        print(f"  VG: {vg.name}")
except Exception as e:
    print(f"ERROR: {e}")
