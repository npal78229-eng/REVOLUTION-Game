import bpy

blend1_path = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend1"
bpy.ops.wm.open_mainfile(filepath=blend1_path)

body = bpy.data.objects.get("v05_Kabir_Body")
uv_layer = body.data.uv_layers[0].data

tiles = {}
for poly in body.data.polygons:
    # Get average UV of poly
    u_avg = sum(uv_layer[li].uv.x for li in poly.loop_indices) / len(poly.loop_indices)
    v_avg = sum(uv_layer[li].uv.y for li in poly.loop_indices) / len(poly.loop_indices)
    tile_u = int(u_avg)
    tile_v = int(v_avg)
    tile_id = 1001 + tile_u + tile_v * 10
    
    # Check what body part this poly is
    vert_z = sum(body.data.vertices[vi].co.z for vi in poly.vertices) / len(poly.vertices)
    vert_y = sum(body.data.vertices[vi].co.y for vi in poly.vertices) / len(poly.vertices)
    
    if tile_id not in tiles:
        tiles[tile_id] = {"count": 0, "zs": [], "ys": []}
    tiles[tile_id]["count"] += 1
    tiles[tile_id]["zs"].append(vert_z)
    tiles[tile_id]["ys"].append(vert_y)

for tid in sorted(tiles.keys()):
    t = tiles[tid]
    avg_z = sum(t["zs"]) / len(t["zs"])
    avg_y = sum(t["ys"]) / len(t["ys"])
    print(f"UDIM {tid}: {t['count']} polys, avg Z={avg_z:.2f} (min={min(t['zs']):.2f}, max={max(t['zs']):.2f}), avg Y={avg_y:.2f}")
