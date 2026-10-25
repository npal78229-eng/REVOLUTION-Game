import bpy

blend_path = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

for mat in bpy.data.materials:
    print(f"\n================ Material: {mat.name} ================")
    if mat.node_tree:
        for link in mat.node_tree.links:
            print(f"  {link.from_node.name}.{link.from_socket.name} -> {link.to_node.name}.{link.to_socket.name}")
