import bpy

tex_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v05\Textures"

for name in ["T_Kabir_Head_BC.png", "T_Kabir_Cloth_BC.png", "T_Kabir_Eye_BC.png", "T_Kabir_Leather_BC.png"]:
    img_path = f"{tex_dir}\\{name}"
    img = bpy.data.images.load(img_path)
    pixels = list(img.pixels[:40]) # first 10 RGBA pixels
    print(f"\nTexture {name}: size={img.size}")
    print(f"Sample pixel RGBA (float): {pixels[:4]}")
    print(f"Sample pixel RGB (0-255): {[int(p * 255) for p in pixels[:3]]}")
    bpy.data.images.remove(img)
