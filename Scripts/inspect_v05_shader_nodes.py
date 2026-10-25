"""
Inspect Kabir_v05 skin shader node tree
"""
import bpy

blend_path = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v05\Kabir_v05.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

body = bpy.data.objects.get("v05_Kabir_Body")
if body:
    print("Body UVs:", [uv.name for uv in body.data.uv_layers])
    print("Body materials:", [m.name for m in body.data.materials if m])

for mat_name in ["M_Kabir_Skin_PBR", "M_Kabir_Khadi_PBR", "M_Kabir_Eye_PBR", "M_Hair", "M_Kabir_Leather_PBR"]:
    mat = bpy.data.materials.get(mat_name)
    if mat and mat.node_tree:
        print(f"\n--- Material: {mat_name} ---")
        for node in mat.node_tree.nodes:
            if node.type == 'TEX_IMAGE' and node.image:
                print(f"  Image Node: {node.name} -> {node.image.filepath or node.image.name}")
            elif node.type == 'BSDF_PRINCIPLED':
                print(f"  Principled BSDF inputs connected:")
                for inp in node.inputs:
                    if inp.is_linked:
                        from_node = inp.links[0].from_node
                        print(f"    {inp.name} <- {from_node.name} ({from_node.type})")
