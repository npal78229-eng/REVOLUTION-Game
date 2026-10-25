"""
Test applying real 2K PBR textures to Kabir_v06_Adult_25
"""
import os
import bpy

blend_path = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v06\Kabir_v06_Heritage_Ages.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

tex_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v05\Textures"
head_bc = os.path.join(tex_dir, "T_Kabir_Head_BC.png")
head_n  = os.path.join(tex_dir, "T_Kabir_Head_N.png")
head_orm = os.path.join(tex_dir, "T_Kabir_Head_ORM.png")
head_sss = os.path.join(tex_dir, "T_Kabir_Head_SSS.png")
eye_bc   = os.path.join(tex_dir, "T_Kabir_Eye_BC.png")

print(f"Textures exist: BC={os.path.exists(head_bc)}, N={os.path.exists(head_n)}, ORM={os.path.exists(head_orm)}, SSS={os.path.exists(head_sss)}, Eye={os.path.exists(eye_bc)}")
