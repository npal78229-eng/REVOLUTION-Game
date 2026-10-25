import bpy
import math

blend_path = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v06\Kabir_v06_Heritage_Ages.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

arm_obj = bpy.data.objects.get("Kabir_v06_Adult_25_Armature")
if arm_obj:
    print(f"Bones in {arm_obj.name}:")
    for b in arm_obj.data.bones:
        parent_name = b.parent.name if b.parent else "None"
        print(f"  {b.name:<15} parent: {parent_name:<15} head: ({b.head.x:.2f}, {b.head.y:.2f}, {b.head.z:.2f}) tail: ({b.tail.x:.2f}, {b.tail.y:.2f}, {b.tail.z:.2f})")
