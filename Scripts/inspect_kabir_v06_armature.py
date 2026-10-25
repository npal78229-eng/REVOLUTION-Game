import bpy

blend_path = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v06\Kabir_v06_Heritage_Ages.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

print("Objects in scene:")
for obj in bpy.data.objects:
    print(f"  - {obj.name} ({obj.type})")

print("\nArmatures in scene:")
for arm in bpy.data.armatures:
    print(f"  - {arm.name} (bones: {len(arm.bones)})")
