import bpy

print("=== OBJECTS IN SCENE ===")
for obj in bpy.data.objects:
    parent_name = obj.parent.name if obj.parent else None
    print(f"{obj.name}: type={obj.type}, parent={parent_name}")
    for m in obj.modifiers:
        target = getattr(m, 'object', None)
        tname = target.name if target else None
        print(f"   modifier {m.name} ({m.type}): target={tname}")

arm = bpy.data.objects.get("v05_Kabir_Armature")
if arm:
    print("=== ARMATURE ACTIONS ===")
    active_act = arm.animation_data.action.name if (arm.animation_data and arm.animation_data.action) else None
    print(f"Active action: {active_act}")
    for act in bpy.data.actions:
        print(f"Action: {act.name}, frames={act.frame_range}")
