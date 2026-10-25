"""
PROJECT REVOLUTION — Authentic Child Idle Locomotion Generator for Kabir v05
Generates a 60-frame seamlessly looping breathing and observation idle cycle
authored natively for v05_Kabir_Armature in Blender, perfectly matching bone axes and proportions.
"""

import bpy
import math
import os

def create_idle_action():
    master_blend = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend"
    bpy.ops.wm.open_mainfile(filepath=master_blend)
    
    arm = bpy.data.objects.get("v05_Kabir_Armature")
    assert arm, "v05_Kabir_Armature not found in Kabir_v05.blend"
    
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode='POSE')
    
    # Ensure animation data
    if not arm.animation_data:
        arm.animation_data_create()
        
    action_name = "Anim_Kabir_v05_Idle"
    action = bpy.data.actions.get(action_name)
    if action:
        bpy.data.actions.remove(action)
    action = bpy.data.actions.new(name=action_name)
    arm.animation_data.action = action
    
    scene = bpy.context.scene
    scene.frame_start = 0
    scene.frame_end = 60
    
    pb = arm.pose.bones
    
    # Reset all bones to rest first
    for b in pb:
        b.rotation_mode = 'XYZ'
        b.location = (0, 0, 0)
        b.rotation_euler = (0, 0, 0)
        b.scale = (1, 1, 1)
        
    keyframes_data = [
        # (frame, bone_name, loc_or_rot, value_tuple)
        # 0. Pelvis subtle breathing and micro weight shift
        (0, "pelvis", "location", (0.0, 0.0, 0.0)),
        (15, "pelvis", "location", (0.001, -0.001, -0.004)),
        (30, "pelvis", "location", (0.0, 0.001, 0.003)),
        (45, "pelvis", "location", (-0.001, 0.0, -0.002)),
        (60, "pelvis", "location", (0.0, 0.0, 0.0)),
        
        (0, "pelvis", "rotation_euler", (0.0, 0.0, 0.0)),
        (15, "pelvis", "rotation_euler", (math.radians(-0.4), 0.0, math.radians(0.3))),
        (30, "pelvis", "rotation_euler", (math.radians(0.5), 0.0, math.radians(-0.2))),
        (45, "pelvis", "rotation_euler", (math.radians(-0.2), 0.0, math.radians(0.2))),
        (60, "pelvis", "rotation_euler", (0.0, 0.0, 0.0)),
        
        # 1. Spine chain - respiratory expansion and relaxation
        (0, "spine_01", "rotation_euler", (0.0, 0.0, 0.0)),
        (15, "spine_01", "rotation_euler", (math.radians(-0.5), 0.0, 0.0)),
        (30, "spine_01", "rotation_euler", (math.radians(0.6), 0.0, 0.0)),
        (45, "spine_01", "rotation_euler", (math.radians(-0.2), 0.0, 0.0)),
        (60, "spine_01", "rotation_euler", (0.0, 0.0, 0.0)),
        
        (0, "spine_03", "rotation_euler", (0.0, 0.0, 0.0)),
        (15, "spine_03", "rotation_euler", (math.radians(-0.7), 0.0, math.radians(0.3))),
        (30, "spine_03", "rotation_euler", (math.radians(0.8), 0.0, math.radians(-0.2))),
        (45, "spine_03", "rotation_euler", (math.radians(-0.3), 0.0, math.radians(0.1))),
        (60, "spine_03", "rotation_euler", (0.0, 0.0, 0.0)),
        
        (0, "spine_05", "rotation_euler", (0.0, 0.0, 0.0)),
        (15, "spine_05", "rotation_euler", (math.radians(-0.6), 0.0, 0.0)),
        (30, "spine_05", "rotation_euler", (math.radians(0.7), 0.0, 0.0)),
        (45, "spine_05", "rotation_euler", (math.radians(-0.2), 0.0, 0.0)),
        (60, "spine_05", "rotation_euler", (0.0, 0.0, 0.0)),
        
        # 2. Neck and Head - gentle alert 12-year-old observant gaze
        (0, "neck_01", "rotation_euler", (0.0, 0.0, 0.0)),
        (20, "neck_01", "rotation_euler", (math.radians(0.4), math.radians(-0.3), math.radians(0.4))),
        (40, "neck_01", "rotation_euler", (math.radians(-0.5), math.radians(0.2), math.radians(-0.3))),
        (60, "neck_01", "rotation_euler", (0.0, 0.0, 0.0)),
        
        (0, "head", "rotation_euler", (0.0, 0.0, 0.0)),
        (18, "head", "rotation_euler", (math.radians(-1.0), math.radians(0.6), math.radians(1.2))),
        (38, "head", "rotation_euler", (math.radians(0.8), math.radians(-0.5), math.radians(-1.0))),
        (60, "head", "rotation_euler", (0.0, 0.0, 0.0)),
        
        # 3. Clavicles & Arms - gentle breathing heave and relaxed hang
        (0, "clavicle_l", "rotation_euler", (0.0, 0.0, 0.0)),
        (15, "clavicle_l", "rotation_euler", (math.radians(-0.4), 0.0, math.radians(-0.5))),
        (30, "clavicle_l", "rotation_euler", (math.radians(0.5), 0.0, math.radians(0.6))),
        (60, "clavicle_l", "rotation_euler", (0.0, 0.0, 0.0)),
        
        (0, "clavicle_r", "rotation_euler", (0.0, 0.0, 0.0)),
        (15, "clavicle_r", "rotation_euler", (math.radians(-0.4), 0.0, math.radians(0.5))),
        (30, "clavicle_r", "rotation_euler", (math.radians(0.5), 0.0, math.radians(-0.6))),
        (60, "clavicle_r", "rotation_euler", (0.0, 0.0, 0.0)),
        
        (0, "upperarm_l", "rotation_euler", (0.0, 0.0, 0.0)),
        (15, "upperarm_l", "rotation_euler", (math.radians(0.6), 0.0, math.radians(-0.4))),
        (35, "upperarm_l", "rotation_euler", (math.radians(-0.7), 0.0, math.radians(0.5))),
        (60, "upperarm_l", "rotation_euler", (0.0, 0.0, 0.0)),
        
        (0, "upperarm_r", "rotation_euler", (0.0, 0.0, 0.0)),
        (15, "upperarm_r", "rotation_euler", (math.radians(0.6), 0.0, math.radians(0.4))),
        (35, "upperarm_r", "rotation_euler", (math.radians(-0.7), 0.0, math.radians(-0.5))),
        (60, "upperarm_r", "rotation_euler", (0.0, 0.0, 0.0)),
    ]
    
    for frame, bone_name, prop_type, val in keyframes_data:
        if bone_name in pb:
            b = pb[bone_name]
            scene.frame_set(frame)
            if prop_type == "location":
                b.location = val
                b.keyframe_insert(data_path="location", frame=frame)
            elif prop_type == "rotation_euler":
                b.rotation_euler = val
                b.keyframe_insert(data_path="rotation_euler", frame=frame)
                
    print(f"Created action '{action_name}'.")
    
    # Save main file
    bpy.ops.wm.save_as_mainfile(filepath=master_blend)
    
    # Export animation FBX
    out_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v05"
    out_fbx = os.path.join(out_dir, "Anim_Kabir_v05_Idle.fbx")
    
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    
    bpy.ops.export_scene.fbx(
        filepath=out_fbx,
        use_selection=True,
        global_scale=1.0,
        apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_ALL',
        axis_forward='-Y',
        axis_up='Z',
        object_types={'ARMATURE'},
        add_leaf_bones=False,
        primary_bone_axis='Y',
        secondary_bone_axis='X',
        armature_nodetype='NULL',
        bake_anim=True,
        bake_anim_use_all_bones=True,
        bake_anim_use_nla_strips=False,
        bake_anim_use_all_actions=False,
        bake_anim_step=1.0
    )
    print(f"Exported idle animation FBX to {out_fbx} ({os.path.getsize(out_fbx)} bytes).")

if __name__ == "__main__":
    create_idle_action()
