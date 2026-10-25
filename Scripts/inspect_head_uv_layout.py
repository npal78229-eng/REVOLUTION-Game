import bpy

blend1_path = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend1"
bpy.ops.wm.open_mainfile(filepath=blend1_path)

body = bpy.data.objects.get("v05_Kabir_Body")
uv_layer = body.data.uv_layers[0].data

# Check vertices in UDIM 1001 (U in [0, 1], V in [0, 1])
head_polys = []
for poly in body.data.polygons:
    u_avg = sum(uv_layer[li].uv.x for li in poly.loop_indices) / len(poly.loop_indices)
    v_avg = sum(uv_layer[li].uv.y for li in poly.loop_indices) / len(poly.loop_indices)
    if 0.0 <= u_avg <= 1.0 and 0.0 <= v_avg <= 1.0:
        head_polys.append(poly)

print(f"Total polygons in UDIM 1001 (Tile 0,0): {len(head_polys)}")
u_vals = [uv_layer[li].uv.x for p in head_polys for li in p.loop_indices]
v_vals = [uv_layer[li].uv.y for p in head_polys for li in p.loop_indices]
print(f"U bounds: [{min(u_vals):.3f}, {max(u_vals):.3f}], V bounds: [{min(v_vals):.3f}, {max(v_vals):.3f}]")

# Check nose tip, chin, forehead UVs in UDIM 1001
verts = body.data.vertices
nose_v = min([v for v in verts if v.co.z > 1.25], key=lambda v: v.co.y)
print(f"Nose tip vert[{nose_v.index}]: co={nose_v.co}")
for poly in head_polys:
    if nose_v.index in poly.vertices:
        for li in poly.loop_indices:
            if body.data.loops[li].vertex_index == nose_v.index:
                print(f"  Nose tip UV: {uv_layer[li].uv}")
                break
        break
