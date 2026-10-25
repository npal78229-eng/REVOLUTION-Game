import bpy
import math
import os
import random

master_blend = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend"
bpy.ops.wm.open_mainfile(filepath=master_blend)

tex_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v05\Textures"
art_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v05"
os.makedirs(tex_dir, exist_ok=True)
os.makedirs(art_dir, exist_ok=True)

def s2l(val):
    return (val / 255.0) ** 2.2

# =========================================================================
# 1. MAP NON-FACE BODY UVs TO CLEAN UNIFORM SKIN REGION
# =========================================================================
body = bpy.data.objects.get("v05_Kabir_Body")
assert body, "v05_Kabir_Body not found"

uv_layer = body.data.uv_layers.active
if not uv_layer:
    uv_layer = body.data.uv_layers.new(name="UVMap")
uv_data = uv_layer.data

head_center_z = 1.330
head_half_height = 0.160
head_half_width = 0.130

for poly in body.data.polygons:
    p_verts = [body.data.vertices[vi] for vi in poly.vertices]
    avg_z = sum(v.co.z for v in p_verts) / len(p_verts)
    avg_y = sum(v.co.y for v in p_verts) / len(p_verts)
    
    if avg_z > 1.20 and avg_y < -0.01:
        for loop_idx in poly.loop_indices:
            vi = body.data.loops[loop_idx].vertex_index
            v = body.data.vertices[vi]
            u = 0.50 - (v.co.x / (head_half_width * 2.2))
            v_coord = 0.48 + ((v.co.z - head_center_z) / (head_half_height * 2.2))
            uv_data[loop_idx].uv = (max(0.02, min(0.98, u)), max(0.02, min(0.98, v_coord)))
    else:
        for loop_idx in poly.loop_indices:
            vi = body.data.loops[loop_idx].vertex_index
            v = body.data.vertices[vi]
            u_body = 0.10 + (v.co.x * 0.15)
            v_body = 0.12 + (v.co.z / 1.44) * 0.08
            uv_data[loop_idx].uv = (max(0.05, min(0.24, u_body)), max(0.05, min(0.24, v_body)))

print("UVs successfully mapped.")

# =========================================================================
# 2. GENERATE KHADI CLOTH TEXTURE (1024x1024)
# =========================================================================
cloth_tex_path = os.path.join(tex_dir, "T_Kabir_Cloth_BC.png")
c_size = 1024
cloth_img = bpy.data.images.get("T_Kabir_Cloth_BC_Authored")
if not cloth_img:
    cloth_img = bpy.data.images.new("T_Kabir_Cloth_BC_Authored", width=c_size, height=c_size, alpha=True)
c_pixels = [1.0] * (c_size * c_size * 4)

khadi_lr = s2l(232)
khadi_lg = s2l(222)
khadi_lb = s2l(200)

rng = random.Random(19190413)

for y in range(c_size):
    for x in range(c_size):
        idx = (y * c_size + x) * 4
        slub = (rng.random() - 0.5) * 0.008
        r = khadi_lr + slub
        g = khadi_lg + slub * 0.9
        b = khadi_lb + slub * 0.8
        c_pixels[idx] = max(0.0, min(1.0, r))
        c_pixels[idx + 1] = max(0.0, min(1.0, g))
        c_pixels[idx + 2] = max(0.0, min(1.0, b))
        c_pixels[idx + 3] = 1.0

cloth_img.pixels = c_pixels
cloth_img.filepath_raw = cloth_tex_path
cloth_img.file_format = 'PNG'
cloth_img.save()

for img in bpy.data.images:
    if any(k in img.filepath for k in ["Head_BC", "Cloth_BC", "Eye_BC"]):
        img.reload()

# =========================================================================
# 3. CLEAN VERTEX WEIGHTS FOR SATCHEL AND SANDALS
# =========================================================================
# Satchel
satchel = bpy.data.objects.get("v05_Kabir_Satchel")
if satchel:
    bad_groups = [vg.name for vg in satchel.vertex_groups if any(k in vg.name for k in ['calf', 'foot', 'ball', 'lowerarm', 'hand', 'thumb', 'index', 'middle', 'ring', 'pinky', 'root'])]
    for bg in bad_groups:
        satchel.vertex_groups.remove(satchel.vertex_groups[bg])
    for v in satchel.data.vertices:
        tot = sum(g.weight for g in v.groups)
        if tot > 0:
            for g in v.groups:
                g.weight /= tot
        else:
            if 'pelvis' not in satchel.vertex_groups:
                satchel.vertex_groups.new(name='pelvis')
            satchel.vertex_groups['pelvis'].add([v.index], 1.0, 'REPLACE')
    print("Cleaned satchel weights.")

# Sandals
sandals = bpy.data.objects.get("v05_Kabir_Sandals")
if sandals:
    bpy.context.view_layer.objects.active = sandals
    dt = sandals.modifiers.new(name='DT_Weights', type='DATA_TRANSFER')
    dt.object = body
    dt.use_vert_data = True
    dt.data_types_verts = {'VGROUP_WEIGHTS'}
    dt.vert_mapping = 'NEAREST'
    bpy.ops.object.datalayout_transfer(modifier='DT_Weights')
    bpy.ops.object.modifier_apply(modifier='DT_Weights')
    if 'root' in sandals.vertex_groups:
        sandals.vertex_groups.remove(sandals.vertex_groups['root'])
    for v in sandals.data.vertices:
        tot = sum(g.weight for g in v.groups)
        if tot > 0:
            for g in v.groups:
                g.weight /= tot
    print("Cleaned sandals weights.")

# =========================================================================
# 4. RIG & ANIMATION HELPERS
# =========================================================================
arm = bpy.data.objects.get("v05_Kabir_Armature")
assert arm, "v05_Kabir_Armature not found"

bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')
pb = arm.pose.bones

def reset_pose():
    for b in pb:
        b.rotation_mode = 'XYZ'
        b.location = (0, 0, 0)
        b.rotation_euler = (0, 0, 0)
        b.scale = (1, 1, 1)

def apply_relaxed_child_idle_base():
    # Asymmetric stance: weight biased onto right leg
    pb["pelvis"].location = (-0.008, 0.002, 0.0)
    pb["pelvis"].rotation_euler = (math.radians(-1.0), math.radians(1.0), math.radians(-1.2))
    
    # Natural spine curvature
    pb["spine_01"].rotation_euler = (math.radians(1.5), 0.0, math.radians(-0.5))
    pb["spine_02"].rotation_euler = (math.radians(1.0), 0.0, math.radians(-0.4))
    pb["spine_03"].rotation_euler = (math.radians(-1.5), 0.0, math.radians(0.3))
    pb["spine_04"].rotation_euler = (math.radians(-0.5), 0.0, 0.0)
    pb["spine_05"].rotation_euler = (math.radians(-0.5), 0.0, 0.0)
    
    pb["neck_01"].rotation_euler = (math.radians(-1.0), 0.0, math.radians(1.0))
    pb["head"].rotation_euler = (math.radians(-1.5), 0.0, math.radians(2.0))
    
    # Perfectly symmetrical relaxed arm hang alongside torso & thighs
    pb["upperarm_l"].rotation_euler = (math.radians(-25.0), math.radians(60.0), 0.0)
    pb["upperarm_r"].rotation_euler = (math.radians(-25.0), math.radians(-60.0), 0.0)
    pb["lowerarm_l"].rotation_euler = (math.radians(-5.0), math.radians(60.0), math.radians(-15.0))
    pb["lowerarm_r"].rotation_euler = (math.radians(-5.0), math.radians(-60.0), math.radians(15.0))
    
    # Curled fingers
    for side in ["_l", "_r"]:
        sign = 1.0 if side == "_l" else -1.0
        if f"thumb_01{side}" in pb:
            pb[f"thumb_01{side}"].rotation_euler = (math.radians(8.0), math.radians(sign * 12.0), math.radians(sign * 10.0))
            pb[f"thumb_02{side}"].rotation_euler = (0.0, math.radians(sign * 15.0), 0.0)
            pb[f"thumb_03{side}"].rotation_euler = (0.0, math.radians(sign * 15.0), 0.0)
        for f in ["index", "middle", "ring", "pinky"]:
            for idx, bend in [("01", 18.0), ("02", 24.0), ("03", 16.0)]:
                bname = f"{f}_{idx}{side}"
                if bname in pb:
                    pb[bname].rotation_euler = (math.radians(bend), 0.0, math.radians(sign * 2.0))
                    
    # Right supporting leg (straight, firm)
    pb["thigh_r"].rotation_euler = (0.0, 0.0, math.radians(1.5))
    pb["calf_r"].rotation_euler = (0.0, 0.0, 0.0)
    pb["foot_r"].rotation_euler = (0.0, 0.0, math.radians(-2.0))
    
    # Left relaxed leg (subtle knee bend)
    pb["thigh_l"].rotation_euler = (math.radians(-2.0), 0.0, math.radians(-1.5))
    pb["calf_l"].rotation_euler = (math.radians(3.5), 0.0, 0.0)
    pb["foot_l"].rotation_euler = (math.radians(1.0), 0.0, math.radians(1.5))

def keyframe_all(frame):
    for b in pb:
        b.keyframe_insert(data_path="location", frame=frame)
        b.keyframe_insert(data_path="rotation_euler", frame=frame)

# =========================================================================
# 5. AUTHOR ANIM_KABIR_V05_IDLE (120 FRAMES = 4.0 SEC @ 30 FPS)
# =========================================================================
if not arm.animation_data:
    arm.animation_data_create()

action_idle_name = "Anim_Kabir_v05_Idle"
action_idle = bpy.data.actions.get(action_idle_name)
if action_idle:
    bpy.data.actions.remove(action_idle)
action_idle = bpy.data.actions.new(name=action_idle_name)
arm.animation_data.action = action_idle

scene = bpy.context.scene
scene.frame_start = 0
scene.frame_end = 120

print("Baking Anim_Kabir_v05_Idle (120 frames)...")
for frame in range(121):
    scene.frame_set(frame)
    reset_pose()
    apply_relaxed_child_idle_base()
    
    # 4-second breathing wave
    breath = math.sin((frame / 120.0) * math.pi * 2.0)
    pb["spine_03"].rotation_euler.x += math.radians(breath * 1.6)
    pb["spine_04"].rotation_euler.x += math.radians(breath * 1.2)
    pb["clavicle_l"].rotation_euler.z += math.radians(-breath * 1.0)
    pb["clavicle_r"].rotation_euler.z += math.radians(breath * 1.0)
    pb["pelvis"].location.z += breath * 0.0015
    
    # Curfew alert scanning head turns
    # Frame 0-35: alert neutral
    # Frame 35-65: turn left (up to 7 deg)
    # Frame 65-85: return to neutral
    # Frame 85-115: turn right (up to 5 deg)
    # Frame 115-120: return neutral
    if 35 <= frame <= 65:
        progress = math.sin(((frame - 35) / 30.0) * math.pi)
        pb["neck_01"].rotation_euler.z += math.radians(progress * 2.5)
        pb["head"].rotation_euler.z += math.radians(progress * 4.5)
    elif 85 <= frame <= 115:
        progress = math.sin(((frame - 85) / 30.0) * math.pi)
        pb["neck_01"].rotation_euler.z -= math.radians(progress * 2.0)
        pb["head"].rotation_euler.z -= math.radians(progress * 3.5)
        
    keyframe_all(frame)

print("Baked Anim_Kabir_v05_Idle.")

# =========================================================================
# 6. AUTHOR ANIM_KABIR_V05_WALK (30 FRAMES = 1.0 SEC @ 30 FPS)
# =========================================================================
action_walk_name = "Anim_Kabir_v05_Walk"
action_walk = bpy.data.actions.get(action_walk_name)
if action_walk:
    bpy.data.actions.remove(action_walk)
action_walk = bpy.data.actions.new(name=action_walk_name)
arm.animation_data.action = action_walk

scene.frame_start = 0
scene.frame_end = 30

print("Baking Anim_Kabir_v05_Walk (30 frames)...")
for frame in range(31):
    scene.frame_set(frame)
    reset_pose()
    
    phi = (frame / 30.0) * math.pi * 2.0
    
    # 1. Forward momentum lean & pelvis dynamics
    # Bob lowest on heel strikes (phi = 0, pi), highest on passing (phi = pi/2, 3pi/2)
    bob = -math.cos(phi * 2.0) * 0.012
    pb["pelvis"].location = (0.0, 0.0, bob)
    pb["pelvis"].rotation_euler = (
        math.radians(3.5),                           # forward lean
        math.sin(phi) * math.radians(3.0),          # pelvic roll (Trendelenburg)
        math.sin(phi) * math.radians(3.5)           # pelvic yaw towards forward step
    )
    
    # 2. Torso counter-twist & spine natural S-curve
    pb["spine_01"].rotation_euler = (math.radians(1.5), 0.0, -math.sin(phi) * math.radians(2.0))
    pb["spine_02"].rotation_euler = (math.radians(1.0), 0.0, -math.sin(phi) * math.radians(2.5))
    pb["spine_03"].rotation_euler = (math.radians(-1.5), 0.0, -math.sin(phi) * math.radians(2.0))
    pb["neck_01"].rotation_euler = (math.radians(-1.0), 0.0, math.sin(phi) * math.radians(0.8))
    pb["head"].rotation_euler = (math.radians(-1.5), 0.0, math.sin(phi) * math.radians(1.2))
    
    # 3. Leg Kinematics (RDR2 grounded heel strike -> roll -> push-off)
    # Forward swing = negative X, backward extension = positive X
    # Left Leg: forward at phi = 0
    thigh_l_angle = -math.cos(phi) * 20.0
    pb["thigh_l"].rotation_euler.x = math.radians(thigh_l_angle)
    
    # Left Calf (Knee flexion >= 0): bends during swing phase (phi from pi to 2pi, where sin(phi) < 0)
    if math.sin(phi) < 0: # Left leg is swinging forward
        swing_bend = -math.sin(phi) * 44.0
        pb["calf_l"].rotation_euler.x = math.radians(swing_bend)
        # Ankle dorsiflexion during swing to clear toe
        pb["foot_l"].rotation_euler.x = math.radians(-8.0 * -math.sin(phi))
    else: # Left leg in stance phase
        # Soft absorption bend on initial impact
        stance_bend = math.sin(phi) * 6.0
        pb["calf_l"].rotation_euler.x = math.radians(stance_bend)
        # Heel strike roll: dorsiflexion (-10 deg) at phi=0 rolling to toe-off (+12 deg) at phi=pi
        foot_roll = -math.cos(phi) * 12.0
        pb["foot_l"].rotation_euler.x = math.radians(foot_roll)
        
    # Right Leg: opposite phase (phi + pi)
    thigh_r_angle = math.cos(phi) * 20.0
    pb["thigh_r"].rotation_euler.x = math.radians(thigh_r_angle)
    
    if math.sin(phi) > 0: # Right leg is swinging forward (0 to pi)
        swing_bend = math.sin(phi) * 44.0
        pb["calf_r"].rotation_euler.x = math.radians(swing_bend)
        pb["foot_r"].rotation_euler.x = math.radians(-8.0 * math.sin(phi))
    else: # Right leg in stance phase
        stance_bend = -math.sin(phi) * 6.0
        pb["calf_r"].rotation_euler.x = math.radians(stance_bend)
        foot_roll = math.cos(phi) * 12.0
        pb["foot_r"].rotation_euler.x = math.radians(foot_roll)
        
    # Feet slight outward flare
    pb["foot_l"].rotation_euler.z = math.radians(1.5)
    pb["foot_r"].rotation_euler.z = math.radians(-1.5)
    
    # 4. Phase-Locked Natural Arm Swing
    # Left arm swings back when left leg swings forward (phi = 0)
    # Right arm swings forward when left leg swings forward
    arm_swing_mag = 16.0
    arm_l_fwd = math.cos(phi) * arm_swing_mag # positive when arm swings fwd
    arm_r_fwd = -math.cos(phi) * arm_swing_mag
    
    # Left arm: base is (-25, 60, 0), lowerarm is (-5, 60, -15)
    # In bone coordinates: rotating X negatively or rotating Z?
    # Let's adjust upperarm X and lowerarm X to create smooth natural swing:
    # Forward swing flexes shoulder forward (decreasing X) and flexes elbow (increasing lowerarm flexion)
    pb["upperarm_l"].rotation_euler = (
        math.radians(-25.0 - arm_l_fwd * 0.8),
        math.radians(60.0),
        math.radians(arm_l_fwd * 0.4)
    )
    pb["lowerarm_l"].rotation_euler = (
        math.radians(-5.0 - max(0.0, arm_l_fwd) * 0.6),
        math.radians(60.0),
        math.radians(-15.0)
    )
    
    # Right arm: base is (-25, -60, 0), lowerarm is (-5, -60, 15)
    pb["upperarm_r"].rotation_euler = (
        math.radians(-25.0 - arm_r_fwd * 0.8),
        math.radians(-60.0),
        math.radians(-arm_r_fwd * 0.4)
    )
    pb["lowerarm_r"].rotation_euler = (
        math.radians(-5.0 - max(0.0, arm_r_fwd) * 0.6),
        math.radians(-60.0),
        math.radians(15.0)
    )
    
    # Curled fingers
    for side in ["_l", "_r"]:
        sign = 1.0 if side == "_l" else -1.0
        if f"thumb_01{side}" in pb:
            pb[f"thumb_01{side}"].rotation_euler = (math.radians(8.0), math.radians(sign * 12.0), math.radians(sign * 10.0))
            pb[f"thumb_02{side}"].rotation_euler = (0.0, math.radians(sign * 15.0), 0.0)
            pb[f"thumb_03{side}"].rotation_euler = (0.0, math.radians(sign * 15.0), 0.0)
        for f in ["index", "middle", "ring", "pinky"]:
            for idx, bend in [("01", 18.0), ("02", 24.0), ("03", 16.0)]:
                bname = f"{f}_{idx}{side}"
                if bname in pb:
                    pb[bname].rotation_euler = (math.radians(bend), 0.0, math.radians(sign * 2.0))
                    
    keyframe_all(frame)

print("Baked Anim_Kabir_v05_Walk.")

# =========================================================================
# 7. AUTHOR ANIM_KABIR_V05_RUN (20 FRAMES = 0.67 SEC @ 30 FPS)
# =========================================================================
action_run_name = "Anim_Kabir_v05_Run"
action_run = bpy.data.actions.get(action_run_name)
if action_run:
    bpy.data.actions.remove(action_run)
action_run = bpy.data.actions.new(name=action_run_name)
arm.animation_data.action = action_run

scene.frame_start = 0
scene.frame_end = 20

print("Baking Anim_Kabir_v05_Run (20 frames)...")
for frame in range(21):
    scene.frame_set(frame)
    reset_pose()
    
    phi = (frame / 20.0) * math.pi * 2.0
    
    # 1. Athletic sprint lean & vertical flight bounce
    bob = -math.cos(phi * 2.0) * 0.025
    pb["pelvis"].location = (0.0, 0.0, bob)
    pb["pelvis"].rotation_euler = (
        math.radians(9.0),                          # strong athletic forward lean
        math.sin(phi) * math.radians(4.5),         # pelvic roll
        math.sin(phi) * math.radians(5.0)          # pelvic yaw
    )
    
    pb["spine_01"].rotation_euler = (math.radians(3.0), 0.0, -math.sin(phi) * math.radians(3.0))
    pb["spine_02"].rotation_euler = (math.radians(2.5), 0.0, -math.sin(phi) * math.radians(3.5))
    pb["spine_03"].rotation_euler = (math.radians(-1.0), 0.0, -math.sin(phi) * math.radians(3.0))
    pb["neck_01"].rotation_euler = (math.radians(-1.5), 0.0, math.sin(phi) * math.radians(1.0))
    pb["head"].rotation_euler = (math.radians(-3.0), 0.0, math.sin(phi) * math.radians(1.5))
    
    # 2. Dynamic Leg Drive
    thigh_l_angle = -math.cos(phi) * 34.0
    pb["thigh_l"].rotation_euler.x = math.radians(thigh_l_angle)
    if math.sin(phi) < 0: # Swing phase
        swing_bend = -math.sin(phi) * 65.0
        pb["calf_l"].rotation_euler.x = math.radians(swing_bend)
        pb["foot_l"].rotation_euler.x = math.radians(-12.0 * -math.sin(phi))
    else: # Stance phase
        stance_bend = math.sin(phi) * 12.0
        pb["calf_l"].rotation_euler.x = math.radians(stance_bend)
        foot_roll = -math.cos(phi) * 18.0
        pb["foot_l"].rotation_euler.x = math.radians(foot_roll)
        
    thigh_r_angle = math.cos(phi) * 34.0
    pb["thigh_r"].rotation_euler.x = math.radians(thigh_r_angle)
    if math.sin(phi) > 0: # Swing phase
        swing_bend = math.sin(phi) * 65.0
        pb["calf_r"].rotation_euler.x = math.radians(swing_bend)
        pb["foot_r"].rotation_euler.x = math.radians(-12.0 * math.sin(phi))
    else: # Stance phase
        stance_bend = -math.sin(phi) * 12.0
        pb["calf_r"].rotation_euler.x = math.radians(stance_bend)
        foot_roll = math.cos(phi) * 18.0
        pb["foot_r"].rotation_euler.x = math.radians(foot_roll)
        
    pb["foot_l"].rotation_euler.z = math.radians(1.5)
    pb["foot_r"].rotation_euler.z = math.radians(-1.5)
    
    # 3. Pumping Bent Sprint Arms (RDR2 Sprint)
    run_arm_mag = 32.0
    arm_l_fwd = math.cos(phi) * run_arm_mag
    arm_r_fwd = -math.cos(phi) * run_arm_mag
    
    pb["upperarm_l"].rotation_euler = (
        math.radians(-25.0 - arm_l_fwd * 0.9),
        math.radians(45.0), # pulled closer to torso
        math.radians(arm_l_fwd * 0.5)
    )
    pb["lowerarm_l"].rotation_euler = (
        math.radians(-25.0 - max(0.0, arm_l_fwd) * 0.8), # bent elbow pumping
        math.radians(45.0),
        math.radians(-20.0)
    )
    
    pb["upperarm_r"].rotation_euler = (
        math.radians(-25.0 - arm_r_fwd * 0.9),
        math.radians(-45.0),
        math.radians(-arm_r_fwd * 0.5)
    )
    pb["lowerarm_r"].rotation_euler = (
        math.radians(-25.0 - max(0.0, arm_r_fwd) * 0.8),
        math.radians(-45.0),
        math.radians(20.0)
    )
    
    # Sprint curled hands
    for side in ["_l", "_r"]:
        sign = 1.0 if side == "_l" else -1.0
        if f"thumb_01{side}" in pb:
            pb[f"thumb_01{side}"].rotation_euler = (math.radians(12.0), math.radians(sign * 15.0), math.radians(sign * 12.0))
        for f in ["index", "middle", "ring", "pinky"]:
            for idx, bend in [("01", 28.0), ("02", 35.0), ("03", 22.0)]:
                bname = f"{f}_{idx}{side}"
                if bname in pb:
                    pb[bname].rotation_euler = (math.radians(bend), 0.0, math.radians(sign * 2.0))
                    
    keyframe_all(frame)

print("Baked Anim_Kabir_v05_Run.")

# =========================================================================
# 8. AUTHOR ANIM_KABIR_V05_STOP (16 FRAMES = 0.53 SEC @ 30 FPS)
# =========================================================================
action_stop_name = "Anim_Kabir_v05_Stop"
action_stop = bpy.data.actions.get(action_stop_name)
if action_stop:
    bpy.data.actions.remove(action_stop)
action_stop = bpy.data.actions.new(name=action_stop_name)
arm.animation_data.action = action_stop

scene.frame_start = 0
scene.frame_end = 16

print("Baking Anim_Kabir_v05_Stop (16 frames)...")
for frame in range(17):
    scene.frame_set(frame)
    reset_pose()
    
    t = frame / 16.0
    # Deceleration curve (smoothstep ease-out)
    ease = 1.0 - (1.0 - t) * (1.0 - t)
    
    # Start from walk stride: left foot planted, right leg trailing
    # End at perfect relaxed idle posture
    if frame < 8:
        stride_decay = (1.0 - frame / 8.0)
        pb["pelvis"].location = (
            -0.008 * ease,
            0.002 * ease,
            -0.010 * stride_decay * math.cos(t * math.pi)
        )
        pb["pelvis"].rotation_euler = (
            math.radians(3.5 * (1.0 - ease) - 1.0 * ease),
            math.radians(1.0 * ease),
            math.radians(-1.2 * ease)
        )
        pb["thigh_l"].rotation_euler.x = math.radians(-12.0 * stride_decay - 2.0 * ease)
        pb["calf_l"].rotation_euler.x = math.radians(6.0 * stride_decay + 3.5 * ease)
        pb["thigh_r"].rotation_euler.x = math.radians(10.0 * stride_decay)
        pb["calf_r"].rotation_euler.x = math.radians(4.0 * stride_decay)
    else:
        apply_relaxed_child_idle_base()
        rebound = math.sin((frame - 8) / 8.0 * math.pi) * 0.003
        pb["pelvis"].location.z += rebound
        pb["spine_03"].rotation_euler.x += math.radians(rebound * 50.0)
        
    keyframe_all(frame)

print("Baked Anim_Kabir_v05_Stop.")

# Reset to Idle action
arm.animation_data.action = action_idle
scene.frame_start = 0
scene.frame_end = 120

bpy.ops.object.mode_set(mode='OBJECT')

# =========================================================================
# 9. EXPORT ALL ANIMATION FBXs
# =========================================================================
bpy.ops.object.select_all(action='DESELECT')
arm.select_set(True)
bpy.context.view_layer.objects.active = arm

actions_to_export = [
    (action_idle, "Anim_Kabir_v05_Idle.fbx", 0, 120),
    (action_walk, "Anim_Kabir_v05_Walk.fbx", 0, 30),
    (action_run, "Anim_Kabir_v05_Run.fbx", 0, 20),
    (action_stop, "Anim_Kabir_v05_Stop.fbx", 0, 16)
]

for act, fbx_filename, fstart, fend in actions_to_export:
    arm.animation_data.action = act
    scene.frame_start = fstart
    scene.frame_end = fend
    out_path = os.path.join(art_dir, fbx_filename)
    
    bpy.ops.export_scene.fbx(
        filepath=out_path,
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
    print(f"Exported {fbx_filename} ({os.path.getsize(out_path)} bytes).")

# =========================================================================
# 10. EXPORT GAME-READY SKELETAL MESH FBX
# =========================================================================
mesh_objects = [
    bpy.data.objects.get("v05_Kabir_Body"),
    bpy.data.objects.get("v05_Kabir_Kurta"),
    bpy.data.objects.get("v05_Kabir_Shorts"),
    bpy.data.objects.get("v05_Kabir_Hair"),
    bpy.data.objects.get("v05_Kabir_Sandals"),
    bpy.data.objects.get("v05_Kabir_Satchel"),
    bpy.data.objects.get("v05_Kabir_Eye_L"),
    bpy.data.objects.get("v05_Kabir_Eye_R")
]

bpy.ops.object.select_all(action='DESELECT')
arm.select_set(True)
for m in mesh_objects:
    if m:
        m.select_set(True)
bpy.context.view_layer.objects.active = arm

skm_fbx_path = os.path.join(art_dir, "SKM_Kabir_v05.fbx")
bpy.ops.export_scene.fbx(
    filepath=skm_fbx_path,
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
print(f"Exported clean SKM_Kabir_v05.fbx ({os.path.getsize(skm_fbx_path)} bytes).")

# Save master blend file
bpy.ops.wm.save_as_mainfile(filepath=master_blend)
print("Saved master blend file Kabir_v05.blend successfully!")
