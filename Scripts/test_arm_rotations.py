import bpy
import math

blend_path = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

arm = bpy.data.objects.get("v05_Kabir_Armature")
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')

pb = arm.pose.bones

for b in pb:
    b.rotation_mode = 'XYZ'
    b.location = (0, 0, 0)
    b.rotation_euler = (0, 0, 0)

# Test rotation on upperarm_l
for test_angle in [math.radians(20), math.radians(40), math.radians(-20), math.radians(-40)]:
    pb["upperarm_l"].rotation_euler = (0, 0, test_angle)
    bpy.context.view_layer.update()
    tail = pb["upperarm_l"].tail
    print(f"Angle {math.degrees(test_angle):.0f} deg on Z: upperarm_l tail={tail}")

for test_angle in [math.radians(20), math.radians(40), math.radians(-20), math.radians(-40)]:
    pb["upperarm_l"].rotation_euler = (test_angle, 0, 0)
    bpy.context.view_layer.update()
    tail = pb["upperarm_l"].tail
    print(f"Angle {math.degrees(test_angle):.0f} deg on X: upperarm_l tail={tail}")

for test_angle in [math.radians(20), math.radians(40), math.radians(-20), math.radians(-40)]:
    pb["upperarm_l"].rotation_euler = (0, test_angle, 0)
    bpy.context.view_layer.update()
    tail = pb["upperarm_l"].tail
    print(f"Angle {math.degrees(test_angle):.0f} deg on Y: upperarm_l tail={tail}")
