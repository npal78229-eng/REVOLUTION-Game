import bpy

blend_path = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

sandals = bpy.data.objects.get("v05_Kabir_Sandals")
if sandals:
    print(f"=== SANDALS OBJECT ===")
    print(f"Location: {sandals.location}, Rotation: {sandals.rotation_euler}, Scale: {sandals.scale}")
    print(f"Parent: {sandals.parent.name if sandals.parent else 'None'}")
    print(f"Modifiers: {[m.name + ' (' + m.type + ')' for m in sandals.modifiers]}")
    for vg in sandals.vertex_groups:
        print(f"  VG: {vg.name}")
    verts = sandals.data.vertices
    xs = [v.co.x for v in verts]
    ys = [v.co.y for v in verts]
    zs = [v.co.z for v in verts]
    print(f"Bounds X=[{min(xs):.3f}, {max(xs):.3f}], Y=[{min(ys):.3f}, {max(ys):.3f}], Z=[{min(zs):.3f}, {max(zs):.3f}]")

body = bpy.data.objects.get("v05_Kabir_Body")
if body:
    verts = body.data.vertices
    zs = [v.co.z for v in verts]
    print(f"Body Z bounds: [{min(zs):.3f}, {max(zs):.3f}]")
