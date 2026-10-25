import bpy
import math

blend_path = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v06\Kabir_v06_Heritage_Ages.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

arm = bpy.data.objects.get("Kabir_v06_Adult_25_Armature")
body = bpy.data.objects.get("Kabir_v06_Adult_25_Body")

# Bind body
bpy.ops.object.select_all(action='DESELECT')
body.select_set(True)
arm.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.object.parent_set(type='ARMATURE_AUTO')

# Enter pose mode and rotate upperarm_r
bpy.ops.object.mode_set(mode='POSE')
pbone = arm.pose.bones.get("upperarm_r")
pbone.rotation_mode = 'XYZ'
pbone.rotation_euler.x = math.radians(70.0)

print(f"Posed upperarm_r rotation: {pbone.rotation_euler.x:.2f} rad")
# Evaluate mesh deformation
depsgraph = bpy.context.evaluated_depsgraph_get()
body_eval = body.evaluated_get(depsgraph)
mesh_eval = body_eval.to_mesh()
print(f"Evaluated mesh has {len(mesh_eval.vertices)} vertices successfully deformed by pose!")
body_eval.to_mesh_clear()
