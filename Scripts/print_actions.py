"""
Print all action names in Kabir_v06_Heritage_Ages.blend
"""
import bpy

blend_path = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v06\Kabir_v06_Heritage_Ages.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)
print("=== ACTIONS IN BLEND ===")
for a in bpy.data.actions:
    print(f"ACTION: {a.name}")
print("=== END ACTIONS ===")
