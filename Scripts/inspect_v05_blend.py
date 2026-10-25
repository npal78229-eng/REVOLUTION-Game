import bpy

blend_path = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

arm = bpy.data.objects.get("v05_Kabir_Armature")
if arm:
    print("\n=== ARMATURE BONES ===")
    print(f"Total bones: {len(arm.data.bones)}")
    for b in arm.data.bones:
        if any(k in b.name for k in ['pelvis', 'spine', 'arm', 'hand', 'thigh', 'calf', 'foot', 'head', 'clavicle']):
            print(f"  Bone {b.name}: head={b.head}, tail={b.tail}")

print("\n=== MATERIALS & TEXTURES ===")
for mat in bpy.data.materials:
    print(f"\nMaterial: {mat.name}, use_nodes={mat.use_nodes}")
    if mat.use_nodes and mat.node_tree:
        for node in mat.node_tree.nodes:
            if node.type == 'TEX_IMAGE' and node.image:
                print(f"  - Image Node: {node.name}, image={node.image.name}, filepath={node.image.filepath}")
            elif node.type == 'BSDF_PRINCIPLED':
                bc = node.inputs['Base Color'].default_value[:]
                print(f"  - Principled BSDF Base Color: {bc[:3]}, Roughness: {node.inputs['Roughness'].default_value}")

print("\n=== ACTIONS ===")
for act in bpy.data.actions:
    print(f"Action: {act.name}, frame_range={act.frame_range}")
