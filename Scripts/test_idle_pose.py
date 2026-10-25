import bpy
import math

blend_path = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

arm = bpy.data.objects.get("v05_Kabir_Armature")
assert arm, "v05_Kabir_Armature not found"

bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')

pb = arm.pose.bones

# Reset all pose bones
for b in pb:
    b.rotation_mode = 'XYZ'
    b.location = (0, 0, 0)
    b.rotation_euler = (0, 0, 0)
    b.scale = (1, 1, 1)

# Natural child standing posture:
# In rest pose:
# upperarm_l has rest head at (0.15, -0.01, 1.15), tail at (0.27, -0.01, 0.94)
# In local bone space of upperarm_l:
# Let's see what each rotation axis does.
# Let's inspect local axes of upperarm_l and upperarm_r.
print("upperarm_l bone matrix:", pb["upperarm_l"].bone.matrix_local)
print("lowerarm_l bone matrix:", pb["lowerarm_l"].bone.matrix_local)
