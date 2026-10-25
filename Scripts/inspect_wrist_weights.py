import bpy

blend_path = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

body = bpy.data.objects.get("v05_Kabir_Body")
vg_map = {vg.index: vg.name for vg in body.vertex_groups}

# Check vertices near right wrist: rest head of hand_r is at (-0.38, -0.01, 0.74)
bad_verts = []
for v in body.data.vertices:
    # check distance to hand_r rest head
    dx = v.co.x - (-0.38)
    dy = v.co.y - (-0.01)
    dz = v.co.z - 0.74
    dist = (dx*dx + dy*dy + dz*dz)**0.5
    if dist < 0.08:
        # Check bone weights
        weights = {vg_map[g.group]: g.weight for g in v.groups if g.group in vg_map}
        # Check if vertex has no hand or forearm weight
        arm_w = weights.get('lowerarm_r', 0.0) + weights.get('hand_r', 0.0)
        if arm_w < 0.5:
            bad_verts.append((v.index, dist, weights))

print(f"Found {len(bad_verts)} vertices near right wrist with abnormal weights:")
for idx, d, w in bad_verts[:10]:
    print(f"  v[{idx}]: dist={d:.3f}, weights={w}")
