import bpy
import mathutils

blend_path = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

arm = bpy.data.objects.get("v05_Kabir_Armature")
pb = arm.pose.bones

print("=== POSE BONES HIERARCHY & ROTATION MODES ===")
for b in pb:
    parent_name = b.parent.name if b.parent else "None"
    print(f"{b.name:20} -> parent={parent_name:15} rot_mode={b.rotation_mode}")
    print(f"   rest head={b.bone.head_local}, tail={b.bone.tail_local}")
