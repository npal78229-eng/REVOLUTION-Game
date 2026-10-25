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

print("upperarm_r rest tail:", pb["upperarm_r"].tail)
for deg in [20, 30, 40, -20, -30, -40]:
    pb["upperarm_r"].rotation_euler = (0, 0, math.radians(deg))
    bpy.context.view_layer.update()
    print(f"upperarm_r Z={deg} deg: tail={pb['upperarm_r'].tail}")

print("lowerarm_l rest tail:", pb["lowerarm_l"].tail)
for deg in [20, 30, 40, -20, -30, -40]:
    pb["lowerarm_l"].rotation_euler = (math.radians(deg), 0, 0)
    bpy.context.view_layer.update()
    print(f"lowerarm_l X={deg} deg: tail={pb['lowerarm_l'].tail}")

for deg in [20, 30, 40, -20, -30, -40]:
    pb["lowerarm_l"].rotation_euler = (0, 0, math.radians(deg))
    bpy.context.view_layer.update()
    print(f"lowerarm_l Z={deg} deg: tail={pb['lowerarm_l'].tail}")
