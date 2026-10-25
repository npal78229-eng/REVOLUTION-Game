import bpy

blend_path = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

body = bpy.data.objects.get("v05_Kabir_Body")
# Find vertices on the face: Z > 1.25, Y < -0.05
face_verts = [v for v in body.data.vertices if v.co.z > 1.25 and v.co.y < -0.05]
print(f"Total face vertices: {len(face_verts)}")

uv_layer = body.data.uv_layers.active.data
# Check UVs of face polygons
face_vert_indices = set(v.index for v in face_verts)
face_uvs = []
for poly in body.data.polygons:
    if any(vi in face_vert_indices for vi in poly.vertices):
        for loop_idx in poly.loop_indices:
            face_uvs.append(uv_layer[loop_idx].uv)

if face_uvs:
    xs = [uv.x for uv in face_uvs]
    ys = [uv.y for uv in face_uvs]
    print(f"Face UV bounds: X=[{min(xs):.3f}, {max(xs):.3f}], Y=[{min(ys):.3f}, {max(ys):.3f}]")
