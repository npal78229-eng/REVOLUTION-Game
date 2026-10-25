"""
PROJECT REVOLUTION — Kabir v06 Comprehensive Combat, Locomotion & Agility Animation Suite
Authors 16 RDR2-inspired animations, models the 1919 Webley Mk VI service revolver,
binds skin weights to garments, bakes animation actions, exports FBXs, and renders review shots.
"""

import os
import sys
import math
import bpy
from mathutils import Vector, Euler, Matrix

def log(msg):
    print(f"[KABIR_v06_ANIM] {msg}")

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def create_pbr_material(name, base_color, roughness, metallic=0.0):
    mat = bpy.data.materials.get(name)
    if not mat:
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    out = nodes.new('ShaderNodeOutputMaterial')
    out.location = (400, 0)
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = base_color
    bsdf.inputs['Roughness'].default_value = roughness
    if 'Metallic' in bsdf.inputs:
        bsdf.inputs['Metallic'].default_value = metallic
    mat.node_tree.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat

def build_webley_revolver():
    """
    Constructs a period-accurate 1919 Webley Mk VI .455 Service Revolver prop.
    """
    log("Building 1919 Webley Mk VI Service Revolver prop...")
    mat_metal = create_pbr_material("M_Webley_Gunmetal", (0.04, 0.04, 0.045, 1.0), roughness=0.28, metallic=0.95)
    mat_wood = create_pbr_material("M_Webley_Walnut", (0.12, 0.06, 0.025, 1.0), roughness=0.35, metallic=0.0)
    
    parts = []
    
    # 1. Barrel (6-inch military barrel)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.15, vertices=12, location=(0, 0.09, 0.035))
    barrel = bpy.context.active_object
    barrel.rotation_euler = (math.radians(90), 0, 0)
    barrel.data.materials.append(mat_metal)
    parts.append(barrel)
    
    # Front sight blade
    bpy.ops.mesh.primitive_cube_add(size=0.006, location=(0, 0.16, 0.048))
    blade = bpy.context.active_object
    blade.scale = (0.3, 1.2, 1.5)
    blade.data.materials.append(mat_metal)
    parts.append(blade)
    
    # 2. Revolver Cylinder (6 chambers)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.022, depth=0.042, vertices=16, location=(0, -0.01, 0.032))
    cylinder = bpy.context.active_object
    cylinder.rotation_euler = (math.radians(90), 0, 0)
    cylinder.data.materials.append(mat_metal)
    parts.append(cylinder)
    
    # 3. Frame & Receiver
    bpy.ops.mesh.primitive_cube_add(size=0.03, location=(0, -0.015, 0.015))
    frame = bpy.context.active_object
    frame.scale = (0.6, 2.2, 1.2)
    frame.data.materials.append(mat_metal)
    parts.append(frame)
    
    # 4. Hammer
    bpy.ops.mesh.primitive_cube_add(size=0.01, location=(0, -0.045, 0.042))
    hammer = bpy.context.active_object
    hammer.scale = (0.4, 0.8, 1.2)
    hammer.data.materials.append(mat_metal)
    parts.append(hammer)
    
    # 5. Trigger Guard & Trigger
    bpy.ops.mesh.primitive_torus_add(major_radius=0.014, minor_radius=0.003, location=(0, 0.0, 0.002))
    tguard = bpy.context.active_object
    tguard.rotation_euler = (0, math.radians(90), 0)
    tguard.data.materials.append(mat_metal)
    parts.append(tguard)
    
    # 6. Checkered Walnut Grip
    bpy.ops.mesh.primitive_cylinder_add(radius=0.016, depth=0.09, vertices=12, location=(0, -0.048, -0.035))
    grip = bpy.context.active_object
    grip.rotation_euler = (math.radians(22), 0, 0)
    grip.scale = (0.7, 1.2, 1.0)
    grip.data.materials.append(mat_wood)
    parts.append(grip)
    
    # Lanyard Ring
    bpy.ops.mesh.primitive_torus_add(major_radius=0.008, minor_radius=0.002, location=(0, -0.062, -0.078))
    ring = bpy.context.active_object
    ring.data.materials.append(mat_metal)
    parts.append(ring)
    
    # Join parts into single Webley object
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = barrel
    bpy.ops.object.join()
    
    revolver = bpy.context.active_object
    revolver.name = "Prop_Webley_Revolver"
    log("Webley Mk VI Revolver constructed successfully.")
    return revolver

def bind_garments_and_props(stage_prefix, arm_obj):
    """
    Binds body, clothing, and props to armature with vertex groups and armature modifiers.
    """
    log(f"Binding garments and props for {stage_prefix}...")
    
    # 1. Body
    body = bpy.data.objects.get(f"{stage_prefix}_Body")
    if body:
        bpy.ops.object.select_all(action='DESELECT')
        body.select_set(True)
        arm_obj.select_set(True)
        bpy.context.view_layer.objects.active = arm_obj
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')
        log(f"  Bound {body.name} with automatic weights.")
        
    # 2. Kurta
    kurta = bpy.data.objects.get(f"{stage_prefix}_Kurta")
    if kurta:
        bpy.ops.object.select_all(action='DESELECT')
        kurta.select_set(True)
        arm_obj.select_set(True)
        bpy.context.view_layer.objects.active = arm_obj
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')
        log(f"  Bound {kurta.name} with automatic weights.")
        
    # 3. Lower Garment (Pajama / Dhoti)
    lower = bpy.data.objects.get(f"{stage_prefix}_Lower")
    if lower:
        bpy.ops.object.select_all(action='DESELECT')
        lower.select_set(True)
        arm_obj.select_set(True)
        bpy.context.view_layer.objects.active = arm_obj
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')
        log(f"  Bound {lower.name} with automatic weights.")
        
    # 4. Juttis
    juttis = bpy.data.objects.get(f"{stage_prefix}_Juttis")
    if juttis:
        bpy.ops.object.select_all(action='DESELECT')
        juttis.select_set(True)
        arm_obj.select_set(True)
        bpy.context.view_layer.objects.active = arm_obj
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')
        log(f"  Bound {juttis.name} with automatic weights.")
        
    # 5. Angavastram (if present)
    anga = bpy.data.objects.get(f"{stage_prefix}_Angavastram")
    if anga:
        bpy.ops.object.select_all(action='DESELECT')
        anga.select_set(True)
        arm_obj.select_set(True)
        bpy.context.view_layer.objects.active = arm_obj
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')
        log(f"  Bound {anga.name} with automatic weights.")
        
    # 6. Hair & Eyes (Rigidly follow head bone)
    for item_name in [f"{stage_prefix}_Hair", f"{stage_prefix}_Eye_L", f"{stage_prefix}_Eye_R"]:
        item = bpy.data.objects.get(item_name)
        if item:
            item.parent = arm_obj
            item.parent_type = 'BONE'
            item.parent_bone = 'head'
            log(f"  Parented {item.name} to bone 'head'.")
            
    # 7. Satchel (if present)
    satchel = bpy.data.objects.get(f"{stage_prefix}_Satchel")
    if satchel:
        satchel.parent = arm_obj
        satchel.parent_type = 'BONE'
        satchel.parent_bone = 'spine_02'
        log(f"  Parented {satchel.name} to bone 'spine_02'.")

def set_active_action(arm_obj, act):
    if not arm_obj.animation_data:
        arm_obj.animation_data_create()
    arm_obj.animation_data.action = act

def reset_pose(arm_obj):
    for pb in arm_obj.pose.bones:
        pb.location = (0, 0, 0)
        pb.rotation_euler = (0, 0, 0)
        pb.scale = (1, 1, 1)

def apply_relaxed_idle_base(pb):
    # Natural gravity drape for arms
    # Clavicles slightly relaxed
    pb["clavicle_l"].rotation_euler = Euler((math.radians(1.5), 0, math.radians(-2.0)), 'XYZ')
    pb["clavicle_r"].rotation_euler = Euler((math.radians(1.5), 0, math.radians(2.0)), 'XYZ')
    
    # Upper arms resting alongside ribcage
    pb["upperarm_l"].rotation_euler = Euler((math.radians(-6.0), math.radians(3.0), math.radians(6.0)), 'XYZ')
    pb["upperarm_r"].rotation_euler = Euler((math.radians(-6.0), math.radians(-3.0), math.radians(-6.0)), 'XYZ')
    
    # Forearms with gentle natural elbow angle
    pb["lowerarm_l"].rotation_euler = Euler((math.radians(12.0), 0, math.radians(4.0)), 'XYZ')
    pb["lowerarm_r"].rotation_euler = Euler((math.radians(12.0), 0, math.radians(-4.0)), 'XYZ')

def keyframe_all_bones(arm_obj, frame):
    for pb in arm_obj.pose.bones:
        pb.keyframe_insert(data_path="location", frame=frame)
        pb.keyframe_insert(data_path="rotation_euler", frame=frame)

# =============================================================================
# ANIMATION AUTHORING GENERATORS (RDR2 PHYSICS & HISTORICAL REALISM)
# =============================================================================

def author_locomotion_suite(arm_obj):
    """
    Authors: Idle (120f), Walk (30f), Run (20f), Stop (16f), Crouch_Idle (60f), Crouch_Walk (32f)
    """
    pb = arm_obj.pose.bones
    scene = bpy.context.scene
    actions = {}
    
    # -------------------------------------------------------------
    # 1. Anim_Kabir_v06_Idle (120 frames / 4.0s @ 30fps)
    # -------------------------------------------------------------
    act_name = "Anim_Kabir_v06_Idle"
    act = bpy.data.actions.new(name=act_name)
    set_active_action(arm_obj, act)
    actions[act_name] = (act, 0, 120)
    
    for frame in range(121):
        scene.frame_set(frame)
        reset_pose(arm_obj)
        apply_relaxed_idle_base(pb)
        
        # Asymmetrical weight shift (pelvis shifted 0.8 cm over right leg)
        pb["pelvis"].location.x = 0.008
        pb["pelvis"].rotation_euler.y = math.radians(-1.2)
        
        # Sinusoidal chest breathing wave (4.0s cycle)
        breath = math.sin((frame / 120.0) * math.pi * 2.0)
        pb["spine_02"].location.z = breath * 0.004
        pb["spine_02"].rotation_euler.x = math.radians(breath * 1.5)
        pb["spine_03"].rotation_euler.x = math.radians(breath * 1.8)
        
        # Observation head micro-glances
        if frame < 60:
            head_scan = math.sin((frame / 60.0) * math.pi) * 12.0 # 12 deg left scan
            pb["neck_01"].rotation_euler.z = math.radians(head_scan * 0.35)
            pb["head"].rotation_euler.z = math.radians(head_scan * 0.65)
            pb["head"].rotation_euler.x = math.radians(head_scan * 0.15)
        else:
            head_scan = -math.sin(((frame - 60) / 60.0) * math.pi) * 9.0 # 9 deg right scan
            pb["neck_01"].rotation_euler.z = math.radians(head_scan * 0.35)
            pb["head"].rotation_euler.z = math.radians(head_scan * 0.65)
            pb["head"].rotation_euler.x = math.radians(abs(head_scan) * 0.1)
            
        keyframe_all_bones(arm_obj, frame)
    log(f"Baked {act_name} (120 frames).")

    # -------------------------------------------------------------
    # 2. Anim_Kabir_v06_Walk (30 frames / 1.0s @ 30fps)
    # -------------------------------------------------------------
    act_name = "Anim_Kabir_v06_Walk"
    act = bpy.data.actions.new(name=act_name)
    set_active_action(arm_obj, act)
    actions[act_name] = (act, 0, 30)
    
    for frame in range(31):
        scene.frame_set(frame)
        reset_pose(arm_obj)
        apply_relaxed_idle_base(pb)
        
        phi = (frame / 30.0) * math.pi * 2.0
        # Vertical bobbing: drops on heel strike (phi=0, pi), rises on passing (phi=pi/2, 3pi/2)
        bob = math.cos(phi * 2.0) * 0.014
        pb["pelvis"].location.z = bob
        pb["pelvis"].rotation_euler.y = math.sin(phi) * math.radians(3.2)
        pb["pelvis"].rotation_euler.z = -math.sin(phi) * math.radians(4.0)
        
        # Thoracic spine counter-twist
        pb["spine_02"].rotation_euler.z = math.sin(phi) * math.radians(3.5)
        pb["spine_03"].rotation_euler.z = math.sin(phi) * math.radians(2.2)
        
        # Left Leg
        thigh_l = math.cos(phi) * 24.0
        pb["thigh_l"].rotation_euler.x = math.radians(thigh_l)
        if math.sin(phi) < 0: # swing phase passing
            pb["calf_l"].rotation_euler.x = math.radians(-math.sin(phi) * 46.0)
            pb["foot_l"].rotation_euler.x = math.radians(-math.sin(phi) * 12.0)
        else:
            pb["calf_l"].rotation_euler.x = math.radians(max(0.0, -thigh_l * 0.25))
            
        # Right Leg (phase offset pi)
        thigh_r = -math.cos(phi) * 24.0
        pb["thigh_r"].rotation_euler.x = math.radians(thigh_r)
        if math.sin(phi) > 0:
            pb["calf_r"].rotation_euler.x = math.radians(math.sin(phi) * 46.0)
            pb["foot_r"].rotation_euler.x = math.radians(math.sin(phi) * 12.0)
        else:
            pb["calf_r"].rotation_euler.x = math.radians(max(0.0, -thigh_r * 0.25))
            
        # Arm Swings (counter-swing)
        arm_l = -math.cos(phi) * 20.0
        pb["upperarm_l"].rotation_euler.x += math.radians(arm_l)
        pb["lowerarm_l"].rotation_euler.x += math.radians(abs(arm_l) * 0.35)
        
        arm_r = math.cos(phi) * 20.0
        pb["upperarm_r"].rotation_euler.x += math.radians(arm_r)
        pb["lowerarm_r"].rotation_euler.x += math.radians(abs(arm_r) * 0.35)
        
        keyframe_all_bones(arm_obj, frame)
    log(f"Baked {act_name} (30 frames).")

    # -------------------------------------------------------------
    # 3. Anim_Kabir_v06_Run (20 frames / 0.67s @ 30fps)
    # -------------------------------------------------------------
    act_name = "Anim_Kabir_v06_Run"
    act = bpy.data.actions.new(name=act_name)
    set_active_action(arm_obj, act)
    actions[act_name] = (act, 0, 20)
    
    for frame in range(21):
        scene.frame_set(frame)
        reset_pose(arm_obj)
        apply_relaxed_idle_base(pb)
        
        phi = (frame / 20.0) * math.pi * 2.0
        # Forward athletic lean
        pb["pelvis"].rotation_euler.x = math.radians(8.5)
        pb["spine_01"].rotation_euler.x = math.radians(4.0)
        pb["spine_02"].rotation_euler.x = math.radians(3.0)
        
        # Flight apex bounce
        pb["pelvis"].location.z = math.cos(phi * 2.0) * 0.035
        pb["pelvis"].rotation_euler.y = math.sin(phi) * math.radians(4.5)
        
        # High knee drive
        thigh_l = math.cos(phi) * 42.0
        pb["thigh_l"].rotation_euler.x = math.radians(thigh_l)
        if math.sin(phi) < 0:
            pb["calf_l"].rotation_euler.x = math.radians(-math.sin(phi) * 75.0)
            
        thigh_r = -math.cos(phi) * 42.0
        pb["thigh_r"].rotation_euler.x = math.radians(thigh_r)
        if math.sin(phi) > 0:
            pb["calf_r"].rotation_euler.x = math.radians(math.sin(phi) * 75.0)
            
        # Pumping bent arms (60 deg fixed elbow bend)
        arm_l = -math.cos(phi) * 35.0
        pb["upperarm_l"].rotation_euler.x += math.radians(arm_l)
        pb["lowerarm_l"].rotation_euler.x = math.radians(60.0)
        
        arm_r = math.cos(phi) * 35.0
        pb["upperarm_r"].rotation_euler.x += math.radians(arm_r)
        pb["lowerarm_r"].rotation_euler.x = math.radians(60.0)
        
        keyframe_all_bones(arm_obj, frame)
    log(f"Baked {act_name} (20 frames).")

    # -------------------------------------------------------------
    # 4. Anim_Kabir_v06_Stop (16 frames / 0.53s @ 30fps)
    # -------------------------------------------------------------
    act_name = "Anim_Kabir_v06_Stop"
    act = bpy.data.actions.new(name=act_name)
    set_active_action(arm_obj, act)
    actions[act_name] = (act, 0, 16)
    
    for frame in range(17):
        scene.frame_set(frame)
        reset_pose(arm_obj)
        apply_relaxed_idle_base(pb)
        
        t = frame / 16.0
        # Lead foot hard strike and deceleration absorption
        if frame < 6:
            decay = frame / 6.0
            pb["pelvis"].location.z = -decay * 0.025
            pb["pelvis"].rotation_euler.x = math.radians((1.0 - decay) * 6.0)
            pb["thigh_r"].rotation_euler.x = math.radians((1.0 - decay) * 18.0)
            pb["calf_r"].rotation_euler.x = math.radians(decay * 15.0)
        else:
            settle = (frame - 6) / 10.0
            pb["pelvis"].location.z = -0.025 * (1.0 - settle)
            pb["pelvis"].rotation_euler.x = math.radians((1.0 - settle) * 2.0)
            
        keyframe_all_bones(arm_obj, frame)
    log(f"Baked {act_name} (16 frames).")

    # -------------------------------------------------------------
    # 5. Anim_Kabir_v06_Crouch_Idle (60 frames / 2.0s @ 30fps)
    # -------------------------------------------------------------
    act_name = "Anim_Kabir_v06_Crouch_Idle"
    act = bpy.data.actions.new(name=act_name)
    set_active_action(arm_obj, act)
    actions[act_name] = (act, 0, 60)
    
    for frame in range(61):
        scene.frame_set(frame)
        reset_pose(arm_obj)
        
        # Deep crouch center of gravity
        pb["pelvis"].location.z = -0.36
        pb["pelvis"].rotation_euler.x = math.radians(18.0)
        pb["spine_01"].rotation_euler.x = math.radians(12.0)
        pb["spine_02"].rotation_euler.x = math.radians(8.0)
        
        # Knees splayed out
        pb["thigh_l"].rotation_euler = Euler((math.radians(-62.0), math.radians(-15.0), math.radians(10.0)), 'XYZ')
        pb["calf_l"].rotation_euler.x = math.radians(105.0)
        pb["foot_l"].rotation_euler.x = math.radians(-38.0)
        
        pb["thigh_r"].rotation_euler = Euler((math.radians(-58.0), math.radians(15.0), math.radians(-10.0)), 'XYZ')
        pb["calf_r"].rotation_euler.x = math.radians(98.0)
        pb["foot_r"].rotation_euler.x = math.radians(-34.0)
        
        # Left hand resting on knee, right hand at hip
        pb["upperarm_l"].rotation_euler = Euler((math.radians(25.0), 0, math.radians(12.0)), 'XYZ')
        pb["lowerarm_l"].rotation_euler = Euler((math.radians(45.0), 0, math.radians(-18.0)), 'XYZ')
        pb["upperarm_r"].rotation_euler = Euler((math.radians(15.0), 0, math.radians(-8.0)), 'XYZ')
        pb["lowerarm_r"].rotation_euler = Euler((math.radians(35.0), 0, math.radians(12.0)), 'XYZ')
        
        # Breathing & vigilant scan
        breath = math.sin((frame / 60.0) * math.pi * 2.0)
        pb["spine_02"].location.z += breath * 0.003
        pb["head"].rotation_euler.z = math.radians(math.sin((frame / 60.0) * math.pi * 2.0) * 8.0)
        
        keyframe_all_bones(arm_obj, frame)
    log(f"Baked {act_name} (60 frames).")

    # -------------------------------------------------------------
    # 6. Anim_Kabir_v06_Crouch_Walk (32 frames / 1.07s @ 30fps)
    # -------------------------------------------------------------
    act_name = "Anim_Kabir_v06_Crouch_Walk"
    act = bpy.data.actions.new(name=act_name)
    set_active_action(arm_obj, act)
    actions[act_name] = (act, 0, 32)
    
    for frame in range(33):
        scene.frame_set(frame)
        reset_pose(arm_obj)
        
        phi = (frame / 32.0) * math.pi * 2.0
        pb["pelvis"].location.z = -0.34 + math.cos(phi * 2.0) * 0.015
        pb["pelvis"].rotation_euler.x = math.radians(16.0)
        pb["spine_01"].rotation_euler.x = math.radians(10.0)
        pb["spine_02"].rotation_euler.x = math.radians(8.0)
        
        # Leg crawl cadence
        pb["thigh_l"].rotation_euler.x = math.radians(-50.0 + math.cos(phi) * 18.0)
        pb["calf_l"].rotation_euler.x = math.radians(85.0 + max(0.0, -math.sin(phi) * 25.0))
        
        pb["thigh_r"].rotation_euler.x = math.radians(-50.0 - math.cos(phi) * 18.0)
        pb["calf_r"].rotation_euler.x = math.radians(85.0 + max(0.0, math.sin(phi) * 25.0))
        
        # Stealth creeping hands
        pb["upperarm_l"].rotation_euler.x = math.radians(20.0 - math.cos(phi) * 12.0)
        pb["lowerarm_l"].rotation_euler.x = math.radians(50.0)
        pb["upperarm_r"].rotation_euler.x = math.radians(20.0 + math.cos(phi) * 12.0)
        pb["lowerarm_r"].rotation_euler.x = math.radians(50.0)
        
        keyframe_all_bones(arm_obj, frame)
    log(f"Baked {act_name} (32 frames).")

    return actions

def author_combat_suite(arm_obj):
    """
    Authors: Weapon_Pickup (45f), Weapon_Draw (24f), Weapon_Aim (30f), Weapon_Shoot (18f), Weapon_Holster (24f)
    """
    pb = arm_obj.pose.bones
    scene = bpy.context.scene
    actions = {}
    
    # -------------------------------------------------------------
    # 7. Anim_Kabir_v06_Weapon_Pickup (45 frames / 1.5s @ 30fps)
    # -------------------------------------------------------------
    act_name = "Anim_Kabir_v06_Weapon_Pickup"
    act = bpy.data.actions.new(name=act_name)
    set_active_action(arm_obj, act)
    actions[act_name] = (act, 0, 45)
    
    for frame in range(46):
        scene.frame_set(frame)
        reset_pose(arm_obj)
        apply_relaxed_idle_base(pb)
        
        if frame <= 18:
            # Stoop down phase (0 -> 18)
            t = frame / 18.0
            pb["pelvis"].location.z = -t * 0.42
            pb["pelvis"].rotation_euler.x = math.radians(t * 26.0)
            pb["spine_01"].rotation_euler.x = math.radians(t * 16.0)
            pb["spine_02"].rotation_euler.x = math.radians(t * 14.0)
            
            # Right leg drops, left leg steps forward
            pb["thigh_r"].rotation_euler.x = math.radians(-t * 65.0)
            pb["calf_r"].rotation_euler.x = math.radians(t * 110.0)
            pb["thigh_l"].rotation_euler.x = math.radians(-t * 45.0)
            pb["calf_l"].rotation_euler.x = math.radians(t * 70.0)
            
            # Right arm reaches down to ground
            pb["upperarm_r"].rotation_euler = Euler((math.radians(t * 45.0), 0, math.radians(-t * 15.0)), 'XYZ')
            pb["lowerarm_r"].rotation_euler = Euler((math.radians(t * 30.0), 0, math.radians(-t * 20.0)), 'XYZ')
            
        elif frame <= 28:
            # Grasp weapon at ground level (18 -> 28)
            pb["pelvis"].location.z = -0.42
            pb["pelvis"].rotation_euler.x = math.radians(26.0)
            pb["spine_01"].rotation_euler.x = math.radians(16.0)
            pb["spine_02"].rotation_euler.x = math.radians(14.0)
            pb["thigh_r"].rotation_euler.x = math.radians(-65.0)
            pb["calf_r"].rotation_euler.x = math.radians(110.0)
            pb["thigh_l"].rotation_euler.x = math.radians(-45.0)
            pb["calf_l"].rotation_euler.x = math.radians(70.0)
            
            # Grasping hand
            pb["upperarm_r"].rotation_euler = Euler((math.radians(48.0), 0, math.radians(-15.0)), 'XYZ')
            pb["lowerarm_r"].rotation_euler = Euler((math.radians(35.0), 0, math.radians(-20.0)), 'XYZ')
            pb["hand_r"].rotation_euler = Euler((math.radians(25.0), 0, math.radians(15.0)), 'XYZ')
            
        else:
            # Rise back to standing ready (28 -> 45)
            t = (frame - 28) / 17.0
            inv_t = 1.0 - t
            pb["pelvis"].location.z = -inv_t * 0.42
            pb["pelvis"].rotation_euler.x = math.radians(inv_t * 26.0)
            pb["spine_01"].rotation_euler.x = math.radians(inv_t * 16.0)
            pb["spine_02"].rotation_euler.x = math.radians(inv_t * 14.0)
            pb["thigh_r"].rotation_euler.x = math.radians(-inv_t * 65.0)
            pb["calf_r"].rotation_euler.x = math.radians(inv_t * 110.0)
            pb["thigh_l"].rotation_euler.x = math.radians(-inv_t * 45.0)
            pb["calf_l"].rotation_euler.x = math.radians(inv_t * 70.0)
            
            # Holding weapon at chest/low-ready
            pb["upperarm_r"].rotation_euler = Euler((math.radians(inv_t * 45.0 + t * 25.0), 0, math.radians(-10.0)), 'XYZ')
            pb["lowerarm_r"].rotation_euler = Euler((math.radians(inv_t * 30.0 + t * 65.0), 0, math.radians(5.0)), 'XYZ')
            pb["hand_r"].rotation_euler = Euler((math.radians(20.0), 0, math.radians(10.0)), 'XYZ')
            
        keyframe_all_bones(arm_obj, frame)
    log(f"Baked {act_name} (45 frames).")

    # -------------------------------------------------------------
    # 8. Anim_Kabir_v06_Weapon_Draw (24 frames / 0.8s @ 30fps)
    # -------------------------------------------------------------
    act_name = "Anim_Kabir_v06_Weapon_Draw"
    act = bpy.data.actions.new(name=act_name)
    set_active_action(arm_obj, act)
    actions[act_name] = (act, 0, 24)
    
    for frame in range(25):
        scene.frame_set(frame)
        reset_pose(arm_obj)
        apply_relaxed_idle_base(pb)
        
        t = frame / 24.0
        if frame < 8:
            # Reach for hip/satchel
            d = frame / 8.0
            pb["upperarm_r"].rotation_euler = Euler((math.radians(d * -15.0), 0, math.radians(-d * 18.0)), 'XYZ')
            pb["lowerarm_r"].rotation_euler = Euler((math.radians(d * 45.0), 0, math.radians(d * 22.0)), 'XYZ')
            pb["clavicle_r"].rotation_euler.y = math.radians(-d * 4.0)
        elif frame < 15:
            # Pull weapon vertically out of holster
            d = (frame - 8) / 7.0
            pb["upperarm_r"].rotation_euler = Euler((math.radians(-15.0 + d * 35.0), 0, math.radians(-18.0 + d * 10.0)), 'XYZ')
            pb["lowerarm_r"].rotation_euler = Euler((math.radians(45.0 + d * 40.0), 0, math.radians(22.0 - d * 15.0)), 'XYZ')
        else:
            # Snap forward into low ready
            d = (frame - 15) / 9.0
            pb["upperarm_r"].rotation_euler = Euler((math.radians(20.0 + d * 25.0), 0, math.radians(-8.0)), 'XYZ')
            pb["lowerarm_r"].rotation_euler = Euler((math.radians(85.0 - d * 25.0), 0, math.radians(7.0)), 'XYZ')
            pb["hand_r"].rotation_euler = Euler((math.radians(d * 20.0), 0, 0), 'XYZ')
            # Supporting left hand rises
            pb["upperarm_l"].rotation_euler = Euler((math.radians(d * 30.0), 0, math.radians(15.0)), 'XYZ')
            pb["lowerarm_l"].rotation_euler = Euler((math.radians(d * 55.0), 0, math.radians(-10.0)), 'XYZ')
            
        keyframe_all_bones(arm_obj, frame)
    log(f"Baked {act_name} (24 frames).")

    # -------------------------------------------------------------
    # 9. Anim_Kabir_v06_Weapon_Aim (30 frames / 1.0s loop @ 30fps)
    # -------------------------------------------------------------
    act_name = "Anim_Kabir_v06_Weapon_Aim"
    act = bpy.data.actions.new(name=act_name)
    set_active_action(arm_obj, act)
    actions[act_name] = (act, 0, 30)
    
    for frame in range(31):
        scene.frame_set(frame)
        reset_pose(arm_obj)
        
        # Staggered athletic combat stance
        pb["pelvis"].rotation_euler.z = math.radians(-12.0)
        pb["thigh_r"].rotation_euler = Euler((math.radians(8.0), 0, math.radians(10.0)), 'XYZ')
        pb["thigh_l"].rotation_euler = Euler((math.radians(-10.0), 0, math.radians(-10.0)), 'XYZ')
        
        # Chest squared to target
        pb["spine_02"].rotation_euler.z = math.radians(10.0)
        pb["spine_03"].rotation_euler.z = math.radians(4.0)
        
        # Right arm extended along sightline
        pb["clavicle_r"].rotation_euler = Euler((math.radians(4.0), 0, math.radians(6.0)), 'XYZ')
        pb["upperarm_r"].rotation_euler = Euler((math.radians(72.0), math.radians(-4.0), math.radians(-12.0)), 'XYZ')
        pb["lowerarm_r"].rotation_euler = Euler((math.radians(18.0), 0, math.radians(8.0)), 'XYZ')
        pb["hand_r"].rotation_euler = Euler((math.radians(15.0), 0, math.radians(-6.0)), 'XYZ')
        
        # Left arm supporting grip
        pb["clavicle_l"].rotation_euler = Euler((math.radians(4.0), 0, math.radians(-4.0)), 'XYZ')
        pb["upperarm_l"].rotation_euler = Euler((math.radians(52.0), 0, math.radians(28.0)), 'XYZ')
        pb["lowerarm_l"].rotation_euler = Euler((math.radians(70.0), 0, math.radians(-24.0)), 'XYZ')
        
        # Head aligned with sightline
        pb["neck_01"].rotation_euler = Euler((math.radians(-6.0), 0, math.radians(2.0)), 'XYZ')
        pb["head"].rotation_euler = Euler((math.radians(-4.0), math.radians(-3.0), math.radians(2.0)), 'XYZ')
        
        # Subtle breath micro-sway (1.0s loop)
        sway = math.sin((frame / 30.0) * math.pi * 2.0)
        pb["upperarm_r"].rotation_euler.x += math.radians(sway * 0.4)
        pb["lowerarm_r"].rotation_euler.x += math.radians(sway * 0.2)
        
        keyframe_all_bones(arm_obj, frame)
    log(f"Baked {act_name} (30 frames).")

    # -------------------------------------------------------------
    # 10. Anim_Kabir_v06_Weapon_Shoot (18 frames / 0.6s @ 30fps)
    # -------------------------------------------------------------
    act_name = "Anim_Kabir_v06_Weapon_Shoot"
    act = bpy.data.actions.new(name=act_name)
    set_active_action(arm_obj, act)
    actions[act_name] = (act, 0, 18)
    
    for frame in range(19):
        scene.frame_set(frame)
        reset_pose(arm_obj)
        
        # Base Aim Stance
        pb["pelvis"].rotation_euler.z = math.radians(-12.0)
        pb["spine_02"].rotation_euler.z = math.radians(10.0)
        pb["spine_03"].rotation_euler.z = math.radians(4.0)
        pb["upperarm_r"].rotation_euler = Euler((math.radians(72.0), math.radians(-4.0), math.radians(-12.0)), 'XYZ')
        pb["lowerarm_r"].rotation_euler = Euler((math.radians(18.0), 0, math.radians(8.0)), 'XYZ')
        pb["hand_r"].rotation_euler = Euler((math.radians(15.0), 0, math.radians(-6.0)), 'XYZ')
        pb["upperarm_l"].rotation_euler = Euler((math.radians(52.0), 0, math.radians(28.0)), 'XYZ')
        pb["lowerarm_l"].rotation_euler = Euler((math.radians(70.0), 0, math.radians(-24.0)), 'XYZ')
        pb["head"].rotation_euler = Euler((math.radians(-4.0), math.radians(-3.0), math.radians(2.0)), 'XYZ')
        
        # Recoil Impulse Profile (RDR2 heavy firearm kickback)
        if frame == 0:
            recoil_kick = 0.0
        elif frame <= 2: # Explosive muzzle kick
            recoil_kick = (frame / 2.0) * 1.0
        elif frame <= 8: # Elastic damped return
            recoil_kick = 1.0 - ((frame - 2) / 6.0) * 0.8
        else: # Settle to ready
            recoil_kick = 0.2 * (1.0 - ((frame - 8) / 10.0))
            
        pb["hand_r"].rotation_euler.x += math.radians(recoil_kick * 16.0)
        pb["lowerarm_r"].rotation_euler.x += math.radians(recoil_kick * 8.0)
        pb["upperarm_r"].rotation_euler.x += math.radians(recoil_kick * 5.0)
        pb["clavicle_r"].rotation_euler.x += math.radians(recoil_kick * 3.5)
        pb["spine_03"].rotation_euler.x += math.radians(recoil_kick * 2.2)
        pb["head"].rotation_euler.x -= math.radians(recoil_kick * 1.5)
        
        keyframe_all_bones(arm_obj, frame)
    log(f"Baked {act_name} (18 frames).")

    # -------------------------------------------------------------
    # 11. Anim_Kabir_v06_Weapon_Holster (24 frames / 0.8s @ 30fps)
    # -------------------------------------------------------------
    act_name = "Anim_Kabir_v06_Weapon_Holster"
    act = bpy.data.actions.new(name=act_name)
    set_active_action(arm_obj, act)
    actions[act_name] = (act, 0, 24)
    
    for frame in range(25):
        scene.frame_set(frame)
        reset_pose(arm_obj)
        
        t = frame / 24.0
        if frame < 10:
            # Lower weapon and pivot muzzle down
            d = frame / 10.0
            pb["upperarm_r"].rotation_euler = Euler((math.radians(72.0 - d * 50.0), 0, math.radians(-12.0 - d * 6.0)), 'XYZ')
            pb["lowerarm_r"].rotation_euler = Euler((math.radians(18.0 + d * 45.0), 0, math.radians(8.0 + d * 14.0)), 'XYZ')
            pb["hand_r"].rotation_euler = Euler((math.radians(15.0 - d * 25.0), 0, 0), 'XYZ')
        elif frame < 17:
            # Slide into holster/satchel
            d = (frame - 10) / 7.0
            pb["upperarm_r"].rotation_euler = Euler((math.radians(22.0 - d * 30.0), 0, math.radians(-18.0)), 'XYZ')
            pb["lowerarm_r"].rotation_euler = Euler((math.radians(63.0 - d * 20.0), 0, math.radians(22.0)), 'XYZ')
            pb["hand_r"].rotation_euler = Euler((math.radians(-10.0), 0, 0), 'XYZ')
        else:
            # Hands drop to relaxed idle drape
            d = (frame - 17) / 7.0
            pb["upperarm_r"].rotation_euler = Euler((math.radians(-8.0 + d * 2.0), 0, math.radians(-18.0 + d * 12.0)), 'XYZ')
            pb["lowerarm_r"].rotation_euler = Euler((math.radians(43.0 - d * 31.0), 0, math.radians(22.0 - d * 18.0)), 'XYZ')
            
        keyframe_all_bones(arm_obj, frame)
    log(f"Baked {act_name} (24 frames).")

    return actions

def author_traversal_and_narrative_suite(arm_obj):
    """
    Authors: Jump (24f), Climb_Ladder (30f), Mantle (36f), Satchel_Open (40f), Curfew_Listen (60f)
    """
    pb = arm_obj.pose.bones
    scene = bpy.context.scene
    actions = {}
    
    # -------------------------------------------------------------
    # 12. Anim_Kabir_v06_Jump (24 frames / 0.8s @ 30fps)
    # -------------------------------------------------------------
    act_name = "Anim_Kabir_v06_Jump"
    act = bpy.data.actions.new(name=act_name)
    set_active_action(arm_obj, act)
    actions[act_name] = (act, 0, 24)
    
    for frame in range(25):
        scene.frame_set(frame)
        reset_pose(arm_obj)
        
        if frame < 6: # Anticipation squat
            t = frame / 6.0
            pb["pelvis"].location.z = -t * 0.16
            pb["thigh_l"].rotation_euler.x = math.radians(-t * 35.0)
            pb["calf_l"].rotation_euler.x = math.radians(t * 60.0)
            pb["thigh_r"].rotation_euler.x = math.radians(-t * 35.0)
            pb["calf_r"].rotation_euler.x = math.radians(t * 60.0)
            pb["upperarm_l"].rotation_euler.x = math.radians(-t * 28.0)
            pb["upperarm_r"].rotation_euler.x = math.radians(-t * 28.0)
        elif frame < 15: # Airborne apex
            t = (frame - 6) / 9.0
            pb["pelvis"].location.z = math.sin(t * math.pi) * 0.38
            pb["thigh_l"].rotation_euler.x = math.radians(15.0 - t * 25.0)
            pb["calf_l"].rotation_euler.x = math.radians(t * 45.0)
            pb["thigh_r"].rotation_euler.x = math.radians(15.0 - t * 25.0)
            pb["calf_r"].rotation_euler.x = math.radians(t * 45.0)
            pb["upperarm_l"].rotation_euler.x = math.radians(35.0 * (1.0 - t))
            pb["upperarm_r"].rotation_euler.x = math.radians(35.0 * (1.0 - t))
        else: # Landing shock absorption
            t = (frame - 15) / 9.0
            pb["pelvis"].location.z = -(1.0 - t) * 0.18
            pb["thigh_l"].rotation_euler.x = math.radians(-(1.0 - t) * 40.0)
            pb["calf_l"].rotation_euler.x = math.radians((1.0 - t) * 65.0)
            pb["thigh_r"].rotation_euler.x = math.radians(-(1.0 - t) * 40.0)
            pb["calf_r"].rotation_euler.x = math.radians((1.0 - t) * 65.0)
            
        keyframe_all_bones(arm_obj, frame)
    log(f"Baked {act_name} (24 frames).")

    # -------------------------------------------------------------
    # 13. Anim_Kabir_v06_Climb_Ladder (30 frames / 1.0s loop @ 30fps)
    # -------------------------------------------------------------
    act_name = "Anim_Kabir_v06_Climb_Ladder"
    act = bpy.data.actions.new(name=act_name)
    set_active_action(arm_obj, act)
    actions[act_name] = (act, 0, 30)
    
    for frame in range(31):
        scene.frame_set(frame)
        reset_pose(arm_obj)
        
        phi = (frame / 30.0) * math.pi * 2.0
        # Alternating rung grasp
        arm_l_reach = math.cos(phi)
        pb["upperarm_l"].rotation_euler = Euler((math.radians(110.0 + arm_l_reach * 25.0), 0, math.radians(-15.0)), 'XYZ')
        pb["lowerarm_l"].rotation_euler = Euler((math.radians(45.0 - arm_l_reach * 20.0), 0, 0), 'XYZ')
        
        arm_r_reach = -math.cos(phi)
        pb["upperarm_r"].rotation_euler = Euler((math.radians(110.0 + arm_r_reach * 25.0), 0, math.radians(15.0)), 'XYZ')
        pb["lowerarm_r"].rotation_euler = Euler((math.radians(45.0 - arm_r_reach * 20.0), 0, 0), 'XYZ')
        
        # Stepping rungs
        pb["thigh_l"].rotation_euler.x = math.radians(-35.0 - arm_r_reach * 25.0)
        pb["calf_l"].rotation_euler.x = math.radians(65.0 + arm_r_reach * 25.0)
        pb["thigh_r"].rotation_euler.x = math.radians(-35.0 - arm_l_reach * 25.0)
        pb["calf_r"].rotation_euler.x = math.radians(65.0 + arm_l_reach * 25.0)
        
        keyframe_all_bones(arm_obj, frame)
    log(f"Baked {act_name} (30 frames).")

    # -------------------------------------------------------------
    # 14. Anim_Kabir_v06_Mantle (36 frames / 1.2s @ 30fps)
    # -------------------------------------------------------------
    act_name = "Anim_Kabir_v06_Mantle"
    act = bpy.data.actions.new(name=act_name)
    set_active_action(arm_obj, act)
    actions[act_name] = (act, 0, 36)
    
    for frame in range(37):
        scene.frame_set(frame)
        reset_pose(arm_obj)
        
        t = frame / 36.0
        if frame < 12: # Grasp parapet ledge
            d = frame / 12.0
            pb["upperarm_l"].rotation_euler.x = math.radians(d * 95.0)
            pb["upperarm_r"].rotation_euler.x = math.radians(d * 95.0)
            pb["lowerarm_l"].rotation_euler.x = math.radians(d * 45.0)
            pb["lowerarm_r"].rotation_euler.x = math.radians(d * 45.0)
        elif frame < 24: # Pull up and leg hook
            d = (frame - 12) / 12.0
            pb["pelvis"].location.z = d * 0.45
            pb["upperarm_l"].rotation_euler.x = math.radians(95.0 - d * 60.0)
            pb["upperarm_r"].rotation_euler.x = math.radians(95.0 - d * 60.0)
            pb["thigh_r"].rotation_euler.x = math.radians(-d * 75.0)
            pb["calf_r"].rotation_euler.x = math.radians(d * 110.0)
        else: # Push onto rooftop and stand
            d = (frame - 24) / 12.0
            pb["pelvis"].location.z = 0.45 + d * 0.20
            pb["pelvis"].location.y = d * 0.35
            pb["thigh_r"].rotation_euler.x = math.radians(-75.0 + d * 75.0)
            pb["calf_r"].rotation_euler.x = math.radians(110.0 - d * 110.0)
            pb["thigh_l"].rotation_euler.x = math.radians(d * 15.0)
            
        keyframe_all_bones(arm_obj, frame)
    log(f"Baked {act_name} (36 frames).")

    # -------------------------------------------------------------
    # 15. Anim_Kabir_v06_Satchel_Open (40 frames / 1.33s @ 30fps)
    # -------------------------------------------------------------
    act_name = "Anim_Kabir_v06_Satchel_Open"
    act = bpy.data.actions.new(name=act_name)
    set_active_action(arm_obj, act)
    actions[act_name] = (act, 0, 40)
    
    for frame in range(41):
        scene.frame_set(frame)
        reset_pose(arm_obj)
        apply_relaxed_idle_base(pb)
        
        t = frame / 40.0
        # Left hand holds satchel base
        pb["upperarm_l"].rotation_euler = Euler((math.radians(12.0), 0, math.radians(18.0)), 'XYZ')
        pb["lowerarm_l"].rotation_euler = Euler((math.radians(35.0), 0, math.radians(-25.0)), 'XYZ')
        
        # Right hand opens flap and inspects dispatch
        if frame < 15:
            d = frame / 15.0
            pb["upperarm_r"].rotation_euler = Euler((math.radians(-d * 10.0), 0, math.radians(-d * 15.0)), 'XYZ')
            pb["lowerarm_r"].rotation_euler = Euler((math.radians(d * 50.0), 0, math.radians(d * 18.0)), 'XYZ')
        elif frame < 30:
            # Lift dispatch to chest level
            d = (frame - 15) / 15.0
            pb["upperarm_r"].rotation_euler = Euler((math.radians(-10.0 + d * 45.0), 0, math.radians(-15.0 + d * 10.0)), 'XYZ')
            pb["lowerarm_r"].rotation_euler = Euler((math.radians(50.0 + d * 35.0), 0, math.radians(18.0 - d * 10.0)), 'XYZ')
            pb["head"].rotation_euler.x = math.radians(18.0) # head looks down at document
        else:
            # Stow back
            d = (frame - 30) / 10.0
            pb["upperarm_r"].rotation_euler = Euler((math.radians(35.0 - d * 35.0), 0, math.radians(-5.0 - d * 5.0)), 'XYZ')
            pb["lowerarm_r"].rotation_euler = Euler((math.radians(85.0 - d * 70.0), 0, 0), 'XYZ')
            pb["head"].rotation_euler.x = math.radians(18.0 * (1.0 - d))
            
        keyframe_all_bones(arm_obj, frame)
    log(f"Baked {act_name} (40 frames).")

    # -------------------------------------------------------------
    # 16. Anim_Kabir_v06_Curfew_Listen (60 frames / 2.0s @ 30fps)
    # -------------------------------------------------------------
    act_name = "Anim_Kabir_v06_Curfew_Listen"
    act = bpy.data.actions.new(name=act_name)
    set_active_action(arm_obj, act)
    actions[act_name] = (act, 0, 60)
    
    for frame in range(61):
        scene.frame_set(frame)
        reset_pose(arm_obj)
        
        # Hugging wall
        pb["pelvis"].rotation_euler.z = math.radians(15.0)
        pb["spine_02"].rotation_euler.z = math.radians(-8.0)
        
        # Right hand touching wall for stability
        pb["upperarm_r"].rotation_euler = Euler((math.radians(35.0), 0, math.radians(-22.0)), 'XYZ')
        pb["lowerarm_r"].rotation_euler = Euler((math.radians(45.0), 0, math.radians(18.0)), 'XYZ')
        
        # Head tilted attentively listening for curfew sentries
        listen_tilt = math.sin((frame / 60.0) * math.pi * 2.0)
        pb["neck_01"].rotation_euler = Euler((math.radians(-4.0), math.radians(8.0), math.radians(14.0 + listen_tilt * 3.0)), 'XYZ')
        pb["head"].rotation_euler = Euler((math.radians(2.0), math.radians(6.0), math.radians(10.0 + listen_tilt * 4.0)), 'XYZ')
        
        keyframe_all_bones(arm_obj, frame)
    log(f"Baked {act_name} (60 frames).")

    return actions

def main():
    log("================================================================================")
    log("  PROJECT REVOLUTION — AUTHORING KABIR v06 COMPLETE ANIMATION & COMBAT SUITE")
    log("================================================================================")
    
    blend_path = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v06\Kabir_v06_Heritage_Ages.blend"
    bpy.ops.wm.open_mainfile(filepath=blend_path)
    
    output_base = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v06"
    anim_dir = os.path.join(output_base, "Animations")
    render_dir = os.path.join(output_base, "Renders")
    ensure_dir(anim_dir)
    ensure_dir(render_dir)
    
    # 1. Build Webley Mk VI Revolver Prop
    revolver = build_webley_revolver()
    
    # Target Adult Armature for master combat & locomotion baking
    arm_obj = bpy.data.objects.get("Kabir_v06_Adult_25_Armature")
    if not arm_obj:
        log("ERROR: Could not find Kabir_v06_Adult_25_Armature.")
        sys.exit(1)
        
    # Bind garments and props
    bind_garments_and_props("Kabir_v06_Adult_25", arm_obj)
    
    # Attach Revolver to right hand bone
    revolver.parent = arm_obj
    revolver.parent_type = 'BONE'
    revolver.parent_bone = 'hand_r'
    revolver.location = (0, 0.08, 0.01)
    revolver.rotation_euler = (math.radians(-90), 0, math.radians(90))
    log("Attached Prop_Webley_Revolver to bone 'hand_r'.")
    
    # Author all 16 animations
    all_actions = {}
    all_actions.update(author_locomotion_suite(arm_obj))
    all_actions.update(author_combat_suite(arm_obj))
    all_actions.update(author_traversal_and_narrative_suite(arm_obj))
    
    log(f"Total animations authored: {len(all_actions)}")
    
    # Export FBX for each action (centered at origin for game engines)
    orig_x = arm_obj.location.x
    arm_obj.location.x = 0.0
    
    for act_name, (act, fstart, fend) in all_actions.items():
        set_active_action(arm_obj, act)
        bpy.context.scene.frame_start = fstart
        bpy.context.scene.frame_end = fend
        
        fbx_path = os.path.join(anim_dir, f"{act_name}.fbx")
        
        bpy.ops.object.select_all(action='DESELECT')
        arm_obj.select_set(True)
        
        bpy.ops.export_scene.fbx(
            filepath=fbx_path,
            use_selection=True,
            global_scale=1.0,
            apply_unit_scale=True,
            bake_space_transform=False,
            object_types={'ARMATURE'},
            add_leaf_bones=False,
            primary_bone_axis='Y',
            secondary_bone_axis='X',
            axis_forward='-Z',
            axis_up='Y',
            bake_anim=True,
            bake_anim_use_nla_strips=False,
            bake_anim_use_all_actions=False,
            bake_anim_force_startend_keying=True
        )
        log(f"Exported FBX: {fbx_path} ({os.path.getsize(fbx_path):,} bytes)")
        
    # Restore position for lineup review rendering
    arm_obj.location.x = orig_x
        
    # Render Cinematic Review Renders
    log("=== Rendering 5 Dynamic Action Snapshots ===")
    scene = bpy.context.scene
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    
    # Camera setup
    cam_data = bpy.data.cameras.new("Cam_Action_Review")
    cam_data.lens = 65.0
    cam_obj = bpy.data.objects.new("Cam_Action_Review", cam_data)
    cam_obj.location = (1.55, -2.2, 1.35)
    cam_obj.rotation_euler = (math.radians(82), 0, math.radians(12))
    scene.collection.objects.link(cam_obj)
    scene.camera = cam_obj
    
    review_shots = [
        ("Anim_Kabir_v06_Weapon_Aim", 15, "Kabir_v06_Action_Weapon_Aim.png"),
        ("Anim_Kabir_v06_Weapon_Shoot", 2, "Kabir_v06_Action_Weapon_Shoot_Recoil.png"),
        ("Anim_Kabir_v06_Weapon_Pickup", 22, "Kabir_v06_Action_Weapon_Pickup.png"),
        ("Anim_Kabir_v06_Walk", 15, "Kabir_v06_Action_Walk_Cadence.png"),
        ("Anim_Kabir_v06_Crouch_Idle", 30, "Kabir_v06_Action_Stealth_Crouch.png")
    ]
    
    for act_name, frame_num, png_name in review_shots:
        act, _, _ = all_actions[act_name]
        set_active_action(arm_obj, act)
        scene.frame_set(frame_num)
        
        # Adjust camera for pickup / crouch
        if "Pickup" in act_name or "Crouch" in act_name:
            cam_obj.location = (1.55, -2.0, 0.95)
            cam_obj.rotation_euler = (math.radians(84), 0, math.radians(12))
        else:
            cam_obj.location = (1.55, -2.2, 1.35)
            cam_obj.rotation_euler = (math.radians(82), 0, math.radians(12))
            
        out_png = os.path.join(render_dir, png_name)
        scene.render.filepath = out_png
        bpy.ops.render.render(write_still=True)
        log(f"Rendered Action Review: {out_png}")
        
    # Save master blend file with all actions & props preserved
    bpy.ops.wm.save_mainfile(filepath=blend_path)
    log(f"Saved master blend: {blend_path}")
    log("ANIMATION SUITE COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
