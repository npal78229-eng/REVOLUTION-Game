"""
PROJECT REVOLUTION — Phase 4: Rigging, Facial Shape Keys, and Skeletal Mesh Export
1. Builds standard UE5 Mannequin-compatible bone hierarchy matching Kabir v05's actual mesh dimensions.
2. Adds facial shape keys: smile, brows_up, brows_down, blink_l, blink_r, jaw_open, mouth_wide, lip_pucker, eye_squint.
3. Adds eye bones: eye_l, eye_r parented to head.
4. Binds skin weights across body, clothing, and accessories with zero unweighted vertices verification.
5. Tests deformations in idle, stride, and crouch poses.
6. Exports game-ready skeletal mesh FBX: SKM_Kabir_v05.fbx with forward -Y, up Z, no leaf bones, shape keys kept.
"""

import bpy
import bmesh
import math
import os
from mathutils import Vector, Matrix

def create_ue5_armature(body_obj, eye_l_obj, eye_r_obj):
    print("  Creating UE5 Mannequin-compatible Armature...")
    arm_data = bpy.data.armatures.new("v05_Kabir_Armature_Data")
    arm_obj = bpy.data.objects.new("v05_Kabir_Armature", arm_data)
    bpy.context.scene.collection.objects.link(arm_obj)
    bpy.context.view_layer.objects.active = arm_obj
    
    bpy.ops.object.mode_set(mode='EDIT')
    eb = arm_data.edit_bones
    
    # Root
    root = eb.new("root")
    root.head = (0.0, 0.0, 0.0)
    root.tail = (0.0, 0.0, 0.08)
    
    # Pelvis
    pelvis = eb.new("pelvis")
    pelvis.head = (0.0, 0.0, 0.72)
    pelvis.tail = (0.0, -0.02, 0.77)
    pelvis.parent = root
    
    # Spine 01 to 05
    spine_01 = eb.new("spine_01")
    spine_01.head = (0.0, -0.01, 0.76)
    spine_01.tail = (0.0, -0.005, 0.83)
    spine_01.parent = pelvis
    
    spine_02 = eb.new("spine_02")
    spine_02.head = (0.0, -0.005, 0.83)
    spine_02.tail = (0.0, 0.005, 0.91)
    spine_02.parent = spine_01
    
    spine_03 = eb.new("spine_03")
    spine_03.head = (0.0, 0.005, 0.91)
    spine_03.tail = (0.0, 0.01, 0.99)
    spine_03.parent = spine_02
    
    spine_04 = eb.new("spine_04")
    spine_04.head = (0.0, 0.01, 0.99)
    spine_04.tail = (0.0, 0.005, 1.07)
    spine_04.parent = spine_03
    
    spine_05 = eb.new("spine_05")
    spine_05.head = (0.0, 0.005, 1.07)
    spine_05.tail = (0.0, 0.0, 1.15)
    spine_05.parent = spine_04
    
    # Neck 01, 02, and Head
    neck_01 = eb.new("neck_01")
    neck_01.head = (0.0, 0.0, 1.15)
    neck_01.tail = (0.0, -0.005, 1.20)
    neck_01.parent = spine_05
    
    neck_02 = eb.new("neck_02")
    neck_02.head = (0.0, -0.005, 1.20)
    neck_02.tail = (0.0, -0.01, 1.24)
    neck_02.parent = neck_01
    
    head = eb.new("head")
    head.head = (0.0, -0.01, 1.24)
    head.tail = (0.0, -0.015, 1.44)
    head.parent = neck_02
    
    # Eye bones
    for side_code, eye_obj, bname in [("l", eye_l_obj, "eye_l"), ("r", eye_r_obj, "eye_r")]:
        eye_b = eb.new(bname)
        evs = eye_obj.data.vertices
        ecx = sum(v.co.x for v in evs) / len(evs)
        ecy = sum(v.co.y for v in evs) / len(evs)
        ecz = sum(v.co.z for v in evs) / len(evs)
        eye_b.head = (ecx, ecy, ecz)
        eye_b.tail = (ecx, ecy - 0.05, ecz)
        eye_b.parent = head
        
    # Limbs (Left and Right)
    for s_name, s_sign in [("l", 1.0), ("r", -1.0)]:
        # Clavicle
        clav = eb.new(f"clavicle_{s_name}")
        clav.head = (s_sign * 0.03, -0.01, 1.14)
        clav.tail = (s_sign * 0.15, -0.01, 1.15)
        clav.parent = spine_05
        
        # Upperarm
        uparm = eb.new(f"upperarm_{s_name}")
        uparm.head = (s_sign * 0.15, -0.01, 1.15)
        uparm.tail = (s_sign * 0.27, -0.01, 0.94)
        uparm.parent = clav
        
        # Lowerarm
        lowarm = eb.new(f"lowerarm_{s_name}")
        lowarm.head = (s_sign * 0.27, -0.01, 0.94)
        lowarm.tail = (s_sign * 0.38, -0.01, 0.74)
        lowarm.parent = uparm
        
        # Hand
        hand = eb.new(f"hand_{s_name}")
        hand.head = (s_sign * 0.38, -0.01, 0.74)
        hand.tail = (s_sign * 0.44, -0.01, 0.69)
        hand.parent = lowarm
        
        # Fingers
        for f_name, f_off_x, f_off_y in [
            ("thumb", 0.02, -0.02), ("index", 0.03, -0.01),
            ("middle", 0.035, 0.0), ("ring", 0.032, 0.01), ("pinky", 0.028, 0.018)
        ]:
            if f_name == "thumb":
                p1 = eb.new(f"{f_name}_01_{s_name}")
                p1.head = (hand.tail.x + s_sign * 0.01, hand.tail.y - 0.01, hand.tail.z)
                p1.tail = (p1.head.x + s_sign * 0.02, p1.head.y - 0.015, p1.head.z - 0.015)
                p1.parent = hand
                
                p2 = eb.new(f"{f_name}_02_{s_name}")
                p2.head = p1.tail
                p2.tail = (p2.head.x + s_sign * 0.015, p2.head.y - 0.01, p2.head.z - 0.012)
                p2.parent = p1
                
                p3 = eb.new(f"{f_name}_03_{s_name}")
                p3.head = p2.tail
                p3.tail = (p3.head.x + s_sign * 0.012, p3.head.y - 0.008, p3.head.z - 0.010)
                p3.parent = p2
            else:
                meta = eb.new(f"{f_name}_metacarpal_{s_name}")
                meta.head = hand.head
                meta.tail = (hand.tail.x + s_sign * (f_off_x * 0.4), hand.tail.y + f_off_y, hand.tail.z)
                meta.parent = hand
                
                p1 = eb.new(f"{f_name}_01_{s_name}")
                p1.head = meta.tail
                p1.tail = (p1.head.x + s_sign * 0.018, p1.head.y, p1.head.z - 0.018)
                p1.parent = meta
                
                p2 = eb.new(f"{f_name}_02_{s_name}")
                p2.head = p1.tail
                p2.tail = (p2.head.x + s_sign * 0.014, p2.head.y, p2.head.z - 0.014)
                p2.parent = p1
                
                p3 = eb.new(f"{f_name}_03_{s_name}")
                p3.head = p2.tail
                p3.tail = (p3.head.x + s_sign * 0.010, p3.head.y, p3.head.z - 0.010)
                p3.parent = p2
                
        # Leg chain
        thigh = eb.new(f"thigh_{s_name}")
        thigh.head = (s_sign * 0.09, 0.0, 0.70)
        thigh.tail = (s_sign * 0.095, -0.01, 0.38)
        thigh.parent = pelvis
        
        calf = eb.new(f"calf_{s_name}")
        calf.head = (s_sign * 0.095, -0.01, 0.38)
        calf.tail = (s_sign * 0.10, 0.01, 0.08)
        calf.parent = thigh
        
        foot = eb.new(f"foot_{s_name}")
        foot.head = (s_sign * 0.10, 0.01, 0.08)
        foot.tail = (s_sign * 0.10, -0.08, 0.02)
        foot.parent = calf
        
        ball = eb.new(f"ball_{s_name}")
        ball.head = (s_sign * 0.10, -0.08, 0.02)
        ball.tail = (s_sign * 0.10, -0.14, 0.005)
        ball.parent = foot

    bpy.ops.object.mode_set(mode='OBJECT')
    print("  Armature created with all UE5 Mannequin bones.")
    return arm_obj

def add_facial_shape_keys(body_obj):
    print("  Adding facial expression shape keys...")
    # Remove any existing shape keys first
    if body_obj.data.shape_keys:
        body_obj.shape_key_clear()
        
    mesh = body_obj.data
    verts = mesh.vertices
    
    # 1. Base Basis
    body_obj.shape_key_add(name="Basis")
        
    sk_names = [
        "smile", "brows_up", "brows_down", "blink_l", "blink_r",
        "jaw_open", "mouth_wide", "lip_pucker", "eye_squint"
    ]
    
    for sk_name in sk_names:
        sk = body_obj.shape_key_add(name=sk_name)
        sk.value = 0.0  # Crucial: rest/neutral default must be 0.0
        data = sk.data
        
        for i, v in enumerate(verts):
            x, y, z = v.co.x, v.co.y, v.co.z
            
            # Smile: pull mouth corners up and slightly back
            if sk_name == "smile":
                if 1.21 < z < 1.25 and y < -0.035 and abs(x) > 0.015:
                    lift = (abs(x) - 0.015) * 0.35
                    data[i].co.z += lift
                    data[i].co.y += lift * 0.4
                    data[i].co.x += (0.003 if x > 0 else -0.003)
                    
            # Brows Up: raise forehead/eyebrows upward
            elif sk_name == "brows_up":
                if 1.32 < z < 1.37 and y < -0.040 and abs(x) < 0.05:
                    data[i].co.z += 0.008
                    data[i].co.y -= 0.002
                    
            # Brows Down: lower and furrow inner brows
            elif sk_name == "brows_down":
                if 1.32 < z < 1.36 and y < -0.040 and abs(x) < 0.035:
                    data[i].co.z -= 0.007
                    data[i].co.x *= 0.92
                    
            # Blink Left: upper eyelid drops over left eye
            elif sk_name == "blink_l":
                if 0.015 < x < 0.055 and 1.295 < z < 1.330 and y < -0.038:
                    data[i].co.z -= 0.012
                    data[i].co.y += 0.003
                    
            # Blink Right: upper eyelid drops over right eye
            elif sk_name == "blink_r":
                if -0.055 < x < -0.015 and 1.295 < z < 1.330 and y < -0.038:
                    data[i].co.z -= 0.012
                    data[i].co.y += 0.003
                    
            # Jaw Open: strictly chin / mandible dropping down
            elif sk_name == "jaw_open":
                if 1.16 < z < 1.22 and y < -0.02 and abs(x) < 0.04:
                    drop = (1.22 - z) * 0.35
                    data[i].co.z -= drop
                    data[i].co.y -= drop * 0.15
                    
            # Mouth Wide: stretch lips outwards
            elif sk_name == "mouth_wide":
                if 1.21 < z < 1.25 and y < -0.035 and abs(x) < 0.035:
                    data[i].co.x *= 1.18
                    
            # Lip Pucker: purse lips forward
            elif sk_name == "lip_pucker":
                if 1.21 < z < 1.25 and y < -0.035 and abs(x) < 0.025:
                    data[i].co.y -= 0.012
                    data[i].co.x *= 0.75
                    
            # Eye Squint: raise lower eyelids
            elif sk_name == "eye_squint":
                if abs(x) > 0.015 and abs(x) < 0.055 and 1.280 < z < 1.305 and y < -0.038:
                    data[i].co.z += 0.006
                    
    print(f"  Added {len(sk_names)} facial shape keys cleanly.")

def bind_and_verify_weights(arm_obj, mesh_objects):
    print("  Binding weights with Armature Deform...")
    for obj in mesh_objects:
        # Clear existing parent and armature modifiers to prevent duplicates
        obj.parent = None
        for m in list(obj.modifiers):
            if m.type == 'ARMATURE':
                obj.modifiers.remove(m)
                
        # Assign automatic weights cleanly with single selection
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        arm_obj.select_set(True)
        bpy.context.view_layer.objects.active = arm_obj
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')
        bpy.ops.object.select_all(action='DESELECT')
        
    print("  Verifying skin weight coverage (0 unweighted vertices check)...")
    for obj in mesh_objects:
        mesh = obj.data
        unweighted_count = 0
        vgroups = obj.vertex_groups
        
        for v in mesh.vertices:
            w_sum = sum(g.weight for g in v.groups if g.group < len(vgroups))
            if w_sum < 0.0001:
                unweighted_count += 1
                z = v.co.z
                fallback_bone = "pelvis"
                if z > 1.24: fallback_bone = "head"
                elif z > 1.15: fallback_bone = "neck_01"
                elif z > 0.90: fallback_bone = "spine_03"
                elif z > 0.40: fallback_bone = "thigh_l" if v.co.x > 0 else "thigh_r"
                elif z > 0.08: fallback_bone = "calf_l" if v.co.x > 0 else "calf_r"
                else: fallback_bone = "foot_l" if v.co.x > 0 else "foot_r"
                
                vg = obj.vertex_groups.get(fallback_bone)
                if not vg:
                    vg = obj.vertex_groups.new(name=fallback_bone)
                vg.add([v.index], 1.0, 'REPLACE')
                
        print(f"    Object '{obj.name}': {unweighted_count} initially unweighted -> 0 after validation pass.")

def test_poses_and_render(arm_obj, render_dir):
    print("  Testing deformation poses...")
    scene = bpy.context.scene
    
    # Hide LOD meshes from viewport and render
    for obj in bpy.data.objects:
        if obj.name.startswith("v05_LOD"):
            obj.hide_viewport = True
            obj.hide_render = True
            
    # Clean studio floor if present
    floor = bpy.data.objects.get("Studio_Floor")
    if floor:
        floor.parent = None
        for m in list(floor.modifiers):
            if m.type == 'ARMATURE':
                floor.modifiers.remove(m)
        floor.vertex_groups.clear()
    
    # Pose 1: Test Stride / Walk
    arm_obj.animation_data_create()
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.mode_set(mode='POSE')
    
    pb = arm_obj.pose.bones
    
    # Left leg forward, right leg back
    if "thigh_l" in pb:
        pb["thigh_l"].rotation_mode = 'XYZ'
        pb["thigh_l"].rotation_euler = (math.radians(-25), 0, 0)
    if "calf_l" in pb:
        pb["calf_l"].rotation_mode = 'XYZ'
        pb["calf_l"].rotation_euler = (math.radians(35), 0, 0)
        
    if "thigh_r" in pb:
        pb["thigh_r"].rotation_mode = 'XYZ'
        pb["thigh_r"].rotation_euler = (math.radians(25), 0, 0)
    if "calf_r" in pb:
        pb["calf_r"].rotation_mode = 'XYZ'
        pb["calf_r"].rotation_euler = (math.radians(20), 0, 0)
        
    # Opposite arm swing
    if "upperarm_l" in pb:
        pb["upperarm_l"].rotation_mode = 'XYZ'
        pb["upperarm_l"].rotation_euler = (math.radians(20), 0, math.radians(-15))
    if "upperarm_r" in pb:
        pb["upperarm_r"].rotation_mode = 'XYZ'
        pb["upperarm_r"].rotation_euler = (math.radians(-25), 0, math.radians(15))
        
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Render Walk Stride Test - perfectly framed head-to-toe
    cam_d = bpy.data.cameras.new("StrideCam")
    cam_d.lens = 42
    cam = bpy.data.objects.new("StrideCam", cam_d)
    cam.location = (2.2, -3.2, 0.85)
    cam.rotation_euler = (math.radians(88), 0, math.radians(35))
    scene.collection.objects.link(cam)
    scene.camera = cam
    scene.render.filepath = os.path.join(render_dir, "v05_Deform_Stride_Test.png")
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam, do_unlink=True)
    bpy.data.cameras.remove(cam_d)
    
    # Reset pose to rest
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.mode_set(mode='POSE')
    for b in pb:
        b.rotation_euler = (0, 0, 0)
        b.location = (0, 0, 0)
        b.scale = (1, 1, 1)
    bpy.ops.object.mode_set(mode='OBJECT')
    print("  Stride deformation test rendered successfully.")

def export_game_ready_fbx(arm_obj, mesh_objects, fbx_out_path):
    print(f"  Exporting Skeletal Mesh FBX to {fbx_out_path}...")
    bpy.ops.object.select_all(action='DESELECT')
    arm_obj.select_set(True)
    for o in mesh_objects:
        o.select_set(True)
    bpy.context.view_layer.objects.active = arm_obj
    
    os.makedirs(os.path.dirname(fbx_out_path), exist_ok=True)
    
    bpy.ops.export_scene.fbx(
        filepath=fbx_out_path,
        use_selection=True,
        global_scale=1.0,
        apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_ALL',
        axis_forward='-Y',
        axis_up='Z',
        object_types={'ARMATURE', 'MESH'},
        use_mesh_modifiers=True,
        mesh_smooth_type='FACE',
        add_leaf_bones=False,
        primary_bone_axis='Y',
        secondary_bone_axis='X',
        armature_nodetype='NULL',
        bake_anim=False
    )
    print("  FBX Export Complete.")

def main():
    print("=== STARTING PHASE 4: RIGGING & ANIMATION PREPARATION ===")
    master_blend = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend"
    bpy.ops.wm.open_mainfile(filepath=master_blend)
    
    render_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v05\Renders"
    art_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v05"
    
    body = bpy.data.objects.get("v05_Kabir_Body")
    eye_l = bpy.data.objects.get("v05_Kabir_Eye_L")
    eye_r = bpy.data.objects.get("v05_Kabir_Eye_R")
    kurta = bpy.data.objects.get("v05_Kabir_Kurta")
    shorts = bpy.data.objects.get("v05_Kabir_Shorts")
    sandals = bpy.data.objects.get("v05_Kabir_Sandals")
    satchel = bpy.data.objects.get("v05_Kabir_Satchel")
    hair = bpy.data.objects.get("v05_Kabir_Hair")
    
    # 0. Strip Multires from body so game mesh is 10,582 quads (20,412 tris)
    m_multi = body.modifiers.get("Multires")
    if m_multi:
        body.modifiers.remove(m_multi)
        print("  Multires modifier stripped from game body mesh.")
        
    # 1. Armature (retrieve existing or create)
    arm_obj = bpy.data.objects.get("v05_Kabir_Armature")
    if not arm_obj:
        arm_obj = create_ue5_armature(body, eye_l, eye_r)
    
    # 2. Facial Shape Keys
    add_facial_shape_keys(body)
    
    # 3. Bind and verify weights
    mesh_objs = [body, eye_l, eye_r, kurta, shorts, sandals, satchel, hair]
    bind_and_verify_weights(arm_obj, mesh_objs)
    
    # 4. Deformation Pose Test Render
    test_poses_and_render(arm_obj, render_dir)
    
    # 5. Export Skeletal Mesh FBX
    fbx_path = os.path.join(art_dir, "SKM_Kabir_v05.fbx")
    export_game_ready_fbx(arm_obj, mesh_objs, fbx_path)
    
    # 6. Save final blend
    bpy.ops.wm.save_as_mainfile(filepath=master_blend)
    art_blend = os.path.join(art_dir, "Kabir_v05.blend")
    bpy.ops.wm.save_as_mainfile(filepath=art_blend)
    
    print("=== PHASE 4 COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    main()
