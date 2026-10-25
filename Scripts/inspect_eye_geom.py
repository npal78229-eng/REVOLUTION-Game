import bpy
import math

blend_path = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

eye_l = bpy.data.objects.get("v05_Kabir_Eye_L")
if eye_l:
    verts = eye_l.data.vertices
    xs = [v.co.x for v in verts]
    ys = [v.co.y for v in verts]
    zs = [v.co.z for v in verts]
    center = (sum(xs)/len(xs), sum(ys)/len(ys), sum(zs)/len(zs))
    print(f"Eye_L world loc: {eye_l.location}")
    print(f"Eye_L local center: {center}")
    print(f"Eye_L X=[{min(xs):.4f}, {max(xs):.4f}], Y=[{min(ys):.4f}, {max(ys):.4f}], Z=[{min(zs):.4f}, {max(zs):.4f}]")
    
    # Check which direction the eye faces:
    # Most anterior vertex (min Y or max Y):
    front_vert = min(verts, key=lambda v: v.co.y)
    back_vert = max(verts, key=lambda v: v.co.y)
    print(f"Most -Y vert: {front_vert.co}")
    print(f"Most +Y vert: {back_vert.co}")
