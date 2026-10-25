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
    
    # Face region (frontal head): Z > 1.20 and Y < -0.01
    if avg_z > 1.20 and avg_y < -0.01:
        for loop_idx in poly.loop_indices:
            vi = body.data.loops[loop_idx].vertex_index
            v = body.data.vertices[vi]
            u = 0.50 - (v.co.x / (head_half_width * 2.2))
            v_coord = 0.48 + ((v.co.z - head_center_z) / (head_half_height * 2.2))
            uv_data[loop_idx].uv = (max(0.02, min(0.98, u)), max(0.02, min(0.98, v_coord)))
    else:
        # All other body polygons (neck, arms, hands, torso, legs, feet):
        # Map strictly to pristine uniform skin corner: U in [0.08, 0.20], V in [0.08, 0.20]
        # Spread subtly so texels are smoothly sampled without any lip/brow bleed
        for loop_idx in poly.loop_indices:
            vi = body.data.loops[loop_idx].vertex_index
            v = body.data.vertices[vi]
            # normalized position within body
            u_body = 0.10 + (v.co.x * 0.15)
            v_body = 0.12 + (v.co.z / 1.44) * 0.08
            uv_data[loop_idx].uv = (max(0.05, min(0.24, u_body)), max(0.05, min(0.24, v_body)))

print("Successfully mapped all body UVs with zero facial feature bleed.")

# =========================================================================
# 2. GENERATE SMOOTH AUTHENTIC KHADI CLOTH TEXTURE (1024x1024)
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
        # Gentle organic handloom slub irregularity
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
print("Saved smooth authentic khadi cotton texture.")

# Reload all images
for img in bpy.data.images:
    if any(k in img.filepath for k in ["Head_BC", "Cloth_BC", "Eye_BC"]):
        img.reload()

# =========================================================================
# 3. AUTHOR NATIVE IDLE ANIMATION (Anim_Kabir_v05_Idle) — 120 FRAMES
# =========================================================================
arm = bpy.data.objects.get("v05_Kabir_Armature")
assert arm, "v05_Kabir_Armature not found"

bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')

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

pb = arm.pose.bones

def reset_pose():
    for b in pb:
        b.rotation_mode = 'XYZ'
        b.location = (0, 0, 0)
        b.rotation_euler = (0, 0, 0)
        b.scale = (1, 1, 1)

def apply_relaxed_child_idle_base():
    # Pelvis: weight shifted to left foot
    pb["pelvis"].location = (0.008, 0.002, -0.004)
    pb["pelvis"].rotation_euler = (math.radians(-1.0), math.radians(0.5), math.radians(1.2))
    
    # Spine natural gentle posture
    pb["spine_01"].rotation_euler = (math.radians(1.5), 0.0, math.radians(-0.8))
    pb["spine_02"].rotation_euler = (math.radians(1.0), 0.0, math.radians(-0.6))
    pb["spine_03"].rotation_euler = (math.radians(-1.2), 0.0, math.radians(0.5))
    pb["spine_04"].rotation_euler = (math.radians(-1.0), 0.0, 0.0)
    pb["spine_05"].rotation_euler = (math.radians(-0.8), 0.0, 0.0)
    
    pb["neck_01"].rotation_euler = (math.radians(-1.5), math.radians(-0.8), math.radians(2.0))
    pb["head"].rotation_euler = (math.radians(-2.0), math.radians(1.0), math.radians(3.5))
    
    # Arms resting naturally alongside body
    pb["clavicle_l"].rotation_euler = (math.radians(-1.0), 0.0, math.radians(-2.0))
    pb["upperarm_l"].rotation_euler = (math.radians(-6.0), math.radians(5.0), math.radians(28.0))
    pb["lowerarm_l"].rotation_euler = (math.radians(-14.0), math.radians(8.0), math.radians(18.0))
    pb["hand_l"].rotation_euler = (math.radians(-4.0), 0.0, math.radians(8.0))
    
    pb["clavicle_r"].rotation_euler = (math.radians(-0.5), 0.0, math.radians(1.5))
    pb["upperarm_r"].rotation_euler = (math.radians(-5.0), math.radians(-4.0), math.radians(-27.0))
    pb["lowerarm_r"].rotation_euler = (math.radians(-12.0), math.radians(-6.0), math.radians(-16.0))
    pb["hand_r"].rotation_euler = (math.radians(-4.0), 0.0, math.radians(-7.0))
    
    # Natural child curled fingers
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
                    
    pb["thigh_l"].rotation_euler = (math.radians(1.0), 0.0, math.radians(-1.5))
    pb["calf_l"].rotation_euler = (math.radians(-1.5), 0.0, 0.0)
    pb["foot_l"].rotation_euler = (math.radians(0.5), 0.0, math.radians(1.0))
    
    pb["thigh_r"].rotation_euler = (math.radians(-1.5), 0.0, math.radians(2.0))
    pb["calf_r"].rotation_euler = (math.radians(1.0), 0.0, 0.0)
    pb["foot_r"].rotation_euler = (math.radians(0.5), 0.0, math.radians(-1.0))

print("Authoring 120-frame seamless breathing & observation idle cycle...")
for frame in range(121):
    scene.frame_set(frame)
    reset_pose()
    apply_relaxed_child_idle_base()
    
    # Breathing wave: 4-second period (120 frames)
    # Sine wave for chest rise and fall
    breath = math.sin((frame / 120.0) * math.pi * 2.0)
    
    # Chest expansion on inhalation
    pb["spine_03"].rotation_euler.x += math.radians(breath * 2.2)
    pb["spine_04"].rotation_euler.x += math.radians(breath * 1.6)
    pb["spine_05"].rotation_euler.x += math.radians(breath * 1.2)
    pb["clavicle_l"].rotation_euler.z += math.radians(-breath * 1.5)
    pb["clavicle_r"].rotation_euler.z += math.radians(breath * 1.5)
    pb["upperarm_l"].rotation_euler.z += math.radians(breath * 0.8)
    pb["upperarm_r"].rotation_euler.z += math.radians(-breath * 0.8)
    pb["pelvis"].location.z += breath * 0.002
    
    # Alert observation: head turns subtly left at frame 35, returns at 65, right at 95
    if frame <= 60:
        head_turn = math.sin((frame / 60.0) * math.pi) * 5.0 # up to 5 deg left
        pb["neck_01"].rotation_euler.z += math.radians(head_turn * 0.4)
        pb["head"].rotation_euler.z += math.radians(head_turn * 0.7)
        pb["head"].rotation_euler.x += math.radians(head_turn * 0.2)
    else:
        head_turn = -math.sin(((frame - 60) / 60.0) * math.pi) * 3.5 # up to 3.5 deg right
        pb["neck_01"].rotation_euler.z += math.radians(head_turn * 0.4)
        pb["head"].rotation_euler.z += math.radians(head_turn * 0.7)
        
    # Keyframe all pose bones
    for b in pb:
        b.keyframe_insert(data_path="location", frame=frame)
        b.keyframe_insert(data_path="rotation_euler", frame=frame)

print("Baked 120-frame Anim_Kabir_v05_Idle.")

# =========================================================================
# 4. AUTHOR NATIVE WALK CYCLE (Anim_Kabir_v05_Walk) — 30 FRAMES (1.0 SEC)
# =========================================================================
action_walk_name = "Anim_Kabir_v05_Walk"
action_walk = bpy.data.actions.get(action_walk_name)
if action_walk:
    bpy.data.actions.remove(action_walk)
action_walk = bpy.data.actions.new(name=action_walk_name)
arm.animation_data.action = action_walk
scene.frame_start = 0
scene.frame_end = 30

print("Authoring 30-frame natural child walk cycle...")
for frame in range(31):
    scene.frame_set(frame)
    reset_pose()
    apply_relaxed_child_idle_base()
    
    # Walk cycle phase: phi from 0 to 2*pi
    phi = (frame / 30.0) * math.pi * 2.0
    
    # Vertical bob: drops on heel strike (phi = 0 and pi), rises on passing (phi = pi/2 and 3*pi/2)
    bob = math.cos(phi * 2.0) * 0.015
    pb["pelvis"].location.z += bob
    # Pelvis roll (hip drop to swinging side)
    pb["pelvis"].rotation_euler.y = math.sin(phi) * math.radians(3.0)
    pb["pelvis"].rotation_euler.z = -math.sin(phi) * math.radians(4.0)
    
    # Torso counter-twist
    pb["spine_02"].rotation_euler.z = math.sin(phi) * math.radians(3.5)
    pb["spine_04"].rotation_euler.z = math.sin(phi) * math.radians(2.5)
    
    # Left Leg (Forward at phi=0, Passing at phi=pi/2, Back at phi=pi)
    thigh_l_rot = math.cos(phi) * 22.0
    pb["thigh_l"].rotation_euler.x = math.radians(thigh_l_rot)
    # Knee bends during swing phase
    if math.sin(phi) < 0: # back to front passing
        knee_bend = -math.sin(phi) * 45.0
        pb["calf_l"].rotation_euler.x = math.radians(knee_bend)
    else:
        pb["calf_l"].rotation_euler.x = math.radians(max(0.0, -thigh_l_rot * 0.3))
        
    # Right Leg (Opposite phase: phi + pi)
    thigh_r_rot = -math.cos(phi) * 22.0
    pb["thigh_r"].rotation_euler.x = math.radians(thigh_r_rot)
    if math.sin(phi) > 0:
        knee_bend = math.sin(phi) * 45.0
        pb["calf_r"].rotation_euler.x = math.radians(knee_bend)
    else:
        pb["calf_r"].rotation_euler.x = math.radians(max(0.0, -thigh_r_rot * 0.3))
        
    # Arm Swings: Counter-swing (Left arm forward when right leg forward)
    arm_l_swing = -math.cos(phi) * 18.0
    pb["upperarm_l"].rotation_euler.x += math.radians(arm_l_swing)
    pb["lowerarm_l"].rotation_euler.x += math.radians(abs(arm_l_swing) * 0.3)
    
    arm_r_swing = math.cos(phi) * 18.0
    pb["upperarm_r"].rotation_euler.x += math.radians(arm_r_swing)
    pb["lowerarm_r"].rotation_euler.x += math.radians(abs(arm_r_swing) * 0.3)
    
    for b in pb:
        b.keyframe_insert(data_path="location", frame=frame)
        b.keyframe_insert(data_path="rotation_euler", frame=frame)

print("Baked 30-frame Anim_Kabir_v05_Walk.")

# =========================================================================
# 5. AUTHOR NATIVE RUN CYCLE (Anim_Kabir_v05_Run) — 20 FRAMES (0.67 SEC)
# =========================================================================
action_run_name = "Anim_Kabir_v05_Run"
action_run = bpy.data.actions.get(action_run_name)
if action_run:
    bpy.data.actions.remove(action_run)
action_run = bpy.data.actions.new(name=action_run_name)
arm.animation_data.action = action_run
scene.frame_start = 0
scene.frame_end = 20

print("Authoring 20-frame athletic child sprint cycle...")
for frame in range(21):
    scene.frame_set(frame)
    reset_pose()
    apply_relaxed_child_idle_base()
    
    phi = (frame / 20.0) * math.pi * 2.0
    
    # Dynamic forward lean (10 degrees forward)
    pb["pelvis"].rotation_euler.x = math.radians(10.0)
    pb["spine_01"].rotation_euler.x += math.radians(4.0)
    pb["spine_03"].rotation_euler.x += math.radians(3.0)
    
    # Running vertical bounce
    pb["pelvis"].location.z += math.cos(phi * 2.0) * 0.028
    pb["pelvis"].rotation_euler.y = math.sin(phi) * math.radians(4.5)
    pb["pelvis"].rotation_euler.z = -math.sin(phi) * math.radians(6.0)
    
    # Larger stride
    thigh_l_rot = math.cos(phi) * 38.0
    pb["thigh_l"].rotation_euler.x = math.radians(thigh_l_rot)
    if math.sin(phi) < 0:
        pb["calf_l"].rotation_euler.x = math.radians(-math.sin(phi) * 65.0)
    else:
        pb["calf_l"].rotation_euler.x = math.radians(max(0.0, -thigh_l_rot * 0.4))
        
    thigh_r_rot = -math.cos(phi) * 38.0
    pb["thigh_r"].rotation_euler.x = math.radians(thigh_r_rot)
    if math.sin(phi) > 0:
        pb["calf_r"].rotation_euler.x = math.radians(math.sin(phi) * 65.0)
    else:
        pb["calf_r"].rotation_euler.x = math.radians(max(0.0, -thigh_r_rot * 0.4))
        
    # Deep bent arm pumping (elbows bent 60 deg, pumping forward/back)
    pb["lowerarm_l"].rotation_euler.z = math.radians(35.0) # bent elbow
    pb["lowerarm_r"].rotation_euler.z = math.radians(-35.0)
    
    arm_l_swing = -math.cos(phi) * 34.0
    pb["upperarm_l"].rotation_euler.x += math.radians(arm_l_swing)
    
    arm_r_swing = math.cos(phi) * 34.0
    pb["upperarm_r"].rotation_euler.x += math.radians(arm_r_swing)
    
    for b in pb:
        b.keyframe_insert(data_path="location", frame=frame)
        b.keyframe_insert(data_path="rotation_euler", frame=frame)

print("Baked 20-frame Anim_Kabir_v05_Run.")

# Reset active action to Idle for default state
arm.animation_data.action = action_idle
scene.frame_start = 0
scene.frame_end = 120

bpy.ops.object.mode_set(mode='OBJECT')

# =========================================================================
# 6. EXPORT ALL ANIMATION FBXs
# =========================================================================
bpy.ops.object.select_all(action='DESELECT')
arm.select_set(True)
bpy.context.view_layer.objects.active = arm

actions_to_export = [
    (action_idle, "Anim_Kabir_v05_Idle.fbx", 0, 120),
    (action_walk, "Anim_Kabir_v05_Walk.fbx", 0, 30),
    (action_run, "Anim_Kabir_v05_Run.fbx", 0, 20)
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
# 7. EXPORT GAME-READY SKELETAL MESH FBX
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
print("Saved master blend file Kabir_v05.blend.")
