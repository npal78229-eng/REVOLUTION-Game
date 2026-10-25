"""
PROJECT REVOLUTION — Fast Action Snapshot Renderer (Blender 5.2 EEVEE)
Poses Kabir_v06_Adult_25 directly in key action moments and renders high-res 1080p snapshots.
"""

import os
import math
import shutil
import bpy

def log(msg):
    print(f"[FAST_RENDER] {msg}", flush=True)

def reset_pose(arm_obj):
    for pb in arm_obj.pose.bones:
        pb.location = (0, 0, 0)
        pb.rotation_euler = (0, 0, 0)
        pb.scale = (1, 1, 1)

def apply_relaxed_idle_base(pb):
    pb["clavicle_l"].rotation_euler.y = math.radians(2)
    pb["clavicle_r"].rotation_euler.y = math.radians(-2)
    pb["upperarm_l"].rotation_euler = (math.radians(12), math.radians(4), math.radians(-8))
    pb["upperarm_r"].rotation_euler = (math.radians(12), math.radians(-4), math.radians(8))
    pb["lowerarm_l"].rotation_euler.x = math.radians(18)
    pb["lowerarm_r"].rotation_euler.x = math.radians(18)
    pb["hand_l"].rotation_euler.x = math.radians(5)
    pb["hand_r"].rotation_euler.x = math.radians(5)
    pb["thigh_l"].rotation_euler.z = math.radians(2)
    pb["thigh_r"].rotation_euler.z = math.radians(-2)

def main():
    log("================================================================================")
    log("  RENDERING REMAINING HIGH-RES ACTION SNAPSHOTS")
    log("================================================================================")
    
    blend_path = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v06\Kabir_v06_Heritage_Ages.blend"
    bpy.ops.wm.open_mainfile(filepath=blend_path)
    
    output_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v06\Renders"
    artifact_dir = r"C:\Users\npal7\.gemini\antigravity\brain\f71e59c5-c47d-4ecc-9d85-fded280f9f20"
    os.makedirs(output_dir, exist_ok=True)
    
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, 'RenderEngine') and 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    
    arm_obj = bpy.data.objects.get("Kabir_v06_Adult_25_Armature")
    if not arm_obj:
        log("ERROR: Adult armature not found!")
        return
        
    pb = arm_obj.pose.bones
    
    # Setup Camera
    cam_data = bpy.data.cameras.new("Cam_Fast_Action")
    cam_data.lens = 65.0
    cam_obj = bpy.data.objects.new("Cam_Fast_Action", cam_data)
    scene.collection.objects.link(cam_obj)
    scene.camera = cam_obj
    
    # -------------------------------------------------------------
    # 1. RUN / SPRINT (Frame 10: Peak right knee drive, athletic forward lean)
    # -------------------------------------------------------------
    reset_pose(arm_obj)
    apply_relaxed_idle_base(pb)
    pb["pelvis"].location = (0.015, -0.04, 0.045)
    pb["pelvis"].rotation_euler = (math.radians(11.0), math.radians(4.5), math.radians(-5.0))
    pb["spine_01"].rotation_euler.x = math.radians(7.0)
    pb["spine_02"].rotation_euler = (math.radians(5.0), 0, math.radians(4.0))
    pb["thigh_r"].rotation_euler = (math.radians(-48.0), 0, math.radians(-4.0))
    pb["calf_r"].rotation_euler.x = math.radians(82.0)
    pb["foot_r"].rotation_euler.x = math.radians(-16.0)
    pb["thigh_l"].rotation_euler = (math.radians(34.0), 0, math.radians(2.0))
    pb["calf_l"].rotation_euler.x = math.radians(14.0)
    pb["foot_l"].rotation_euler.x = math.radians(22.0)
    pb["upperarm_l"].rotation_euler = (math.radians(-48.0), 0, math.radians(-12.0))
    pb["lowerarm_l"].rotation_euler.x = math.radians(78.0)
    pb["upperarm_r"].rotation_euler = (math.radians(36.0), 0, math.radians(14.0))
    pb["lowerarm_r"].rotation_euler.x = math.radians(52.0)
    
    cam_obj.location = (1.65, -2.4, 1.25)
    cam_obj.rotation_euler = (math.radians(82), 0, math.radians(10))
    out_png = os.path.join(output_dir, "Kabir_v06_Action_Run_Sprint.png")
    scene.render.filepath = out_png
    bpy.ops.render.render(write_still=True)
    shutil.copy2(out_png, os.path.join(artifact_dir, "Kabir_v06_Action_Run_Sprint.png"))
    log("Rendered & Copied: Kabir_v06_Action_Run_Sprint.png")

    # -------------------------------------------------------------
    # 2. STOP / DECELERATION (Frame 8: Lead foot plant, hip drop -2.8cm, brake)
    # -------------------------------------------------------------
    reset_pose(arm_obj)
    apply_relaxed_idle_base(pb)
    pb["pelvis"].location = (0.0, -0.015, -0.028)
    pb["pelvis"].rotation_euler = (math.radians(-6.0), math.radians(-2.0), math.radians(3.0))
    pb["spine_01"].rotation_euler.x = math.radians(-4.0)
    pb["spine_02"].rotation_euler.x = math.radians(-3.0)
    pb["thigh_r"].rotation_euler = (math.radians(-28.0), 0, math.radians(-3.0))
    pb["calf_r"].rotation_euler.x = math.radians(32.0)
    pb["foot_r"].rotation_euler.x = math.radians(14.0)
    pb["thigh_l"].rotation_euler = (math.radians(14.0), 0, math.radians(2.0))
    pb["calf_l"].rotation_euler.x = math.radians(38.0)
    pb["foot_l"].rotation_euler.x = math.radians(-8.0)
    pb["upperarm_l"].rotation_euler = (math.radians(22.0), 0, math.radians(-14.0))
    pb["upperarm_r"].rotation_euler = (math.radians(20.0), 0, math.radians(14.0))
    pb["lowerarm_l"].rotation_euler.x = math.radians(35.0)
    pb["lowerarm_r"].rotation_euler.x = math.radians(35.0)
    
    cam_obj.location = (1.65, -2.4, 1.20)
    cam_obj.rotation_euler = (math.radians(82), 0, math.radians(10))
    out_png = os.path.join(output_dir, "Kabir_v06_Action_Stop_Decel.png")
    scene.render.filepath = out_png
    bpy.ops.render.render(write_still=True)
    shutil.copy2(out_png, os.path.join(artifact_dir, "Kabir_v06_Action_Stop_Decel.png"))
    log("Rendered & Copied: Kabir_v06_Action_Stop_Decel.png")

    # -------------------------------------------------------------
    # 3. JUMP APEX (Frame 12: +38cm launch, legs tucked, momentum)
    # -------------------------------------------------------------
    reset_pose(arm_obj)
    apply_relaxed_idle_base(pb)
    pb["pelvis"].location.z = 0.38
    pb["pelvis"].rotation_euler.x = math.radians(5.0)
    pb["thigh_l"].rotation_euler = (math.radians(-32.0), 0, math.radians(3.0))
    pb["calf_l"].rotation_euler.x = math.radians(65.0)
    pb["foot_l"].rotation_euler.x = math.radians(-18.0)
    pb["thigh_r"].rotation_euler = (math.radians(-38.0), 0, math.radians(-3.0))
    pb["calf_r"].rotation_euler.x = math.radians(72.0)
    pb["foot_r"].rotation_euler.x = math.radians(-20.0)
    pb["upperarm_l"].rotation_euler = (math.radians(-55.0), 0, math.radians(-25.0))
    pb["upperarm_r"].rotation_euler = (math.radians(-50.0), 0, math.radians(25.0))
    pb["lowerarm_l"].rotation_euler.x = math.radians(45.0)
    pb["lowerarm_r"].rotation_euler.x = math.radians(45.0)
    
    cam_obj.location = (1.65, -2.5, 1.45)
    cam_obj.rotation_euler = (math.radians(80), 0, math.radians(10))
    out_png = os.path.join(output_dir, "Kabir_v06_Action_Jump_Apex.png")
    scene.render.filepath = out_png
    bpy.ops.render.render(write_still=True)
    shutil.copy2(out_png, os.path.join(artifact_dir, "Kabir_v06_Action_Jump_Apex.png"))
    log("Rendered & Copied: Kabir_v06_Action_Jump_Apex.png")

    # -------------------------------------------------------------
    # 4. MANTLE HEAVE (Frame 18: Ledge grab, bicep pull, leg hook over parapet)
    # -------------------------------------------------------------
    reset_pose(arm_obj)
    apply_relaxed_idle_base(pb)
    pb["pelvis"].location = (0.0, 0.08, 0.42)
    pb["pelvis"].rotation_euler = (math.radians(22.0), 0, math.radians(5.0))
    pb["spine_01"].rotation_euler.x = math.radians(18.0)
    pb["spine_02"].rotation_euler.x = math.radians(12.0)
    pb["clavicle_l"].rotation_euler.z = math.radians(12.0)
    pb["clavicle_r"].rotation_euler.z = math.radians(-12.0)
    pb["upperarm_l"].rotation_euler = (math.radians(-78.0), 0, math.radians(-15.0))
    pb["upperarm_r"].rotation_euler = (math.radians(-75.0), 0, math.radians(15.0))
    pb["lowerarm_l"].rotation_euler.x = math.radians(95.0)
    pb["lowerarm_r"].rotation_euler.x = math.radians(92.0)
    pb["hand_l"].rotation_euler.x = math.radians(-25.0)
    pb["hand_r"].rotation_euler.x = math.radians(-25.0)
    pb["thigh_r"].rotation_euler = (math.radians(-75.0), 0, math.radians(-12.0))
    pb["calf_r"].rotation_euler.x = math.radians(110.0)
    pb["foot_r"].rotation_euler.x = math.radians(-20.0)
    pb["thigh_l"].rotation_euler = (math.radians(20.0), 0, math.radians(4.0))
    pb["calf_l"].rotation_euler.x = math.radians(15.0)
    
    cam_obj.location = (1.55, -2.2, 1.40)
    cam_obj.rotation_euler = (math.radians(80), 0, math.radians(10))
    out_png = os.path.join(output_dir, "Kabir_v06_Action_Mantle_Heave.png")
    scene.render.filepath = out_png
    bpy.ops.render.render(write_still=True)
    shutil.copy2(out_png, os.path.join(artifact_dir, "Kabir_v06_Action_Mantle_Heave.png"))
    log("Rendered & Copied: Kabir_v06_Action_Mantle_Heave.png")

    # -------------------------------------------------------------
    # 5. LADDER CLIMB (Frame 15: Alternating rung grip, vertical climb)
    # -------------------------------------------------------------
    reset_pose(arm_obj)
    apply_relaxed_idle_base(pb)
    pb["pelvis"].location = (0.0, 0.04, 0.22)
    pb["spine_01"].rotation_euler.x = math.radians(6.0)
    pb["upperarm_l"].rotation_euler = (math.radians(-115.0), 0, math.radians(-12.0))
    pb["lowerarm_l"].rotation_euler.x = math.radians(72.0)
    pb["hand_l"].rotation_euler.x = math.radians(-20.0)
    pb["upperarm_r"].rotation_euler = (math.radians(-45.0), 0, math.radians(14.0))
    pb["lowerarm_r"].rotation_euler.x = math.radians(98.0)
    pb["hand_r"].rotation_euler.x = math.radians(-25.0)
    pb["thigh_r"].rotation_euler = (math.radians(-52.0), 0, math.radians(-4.0))
    pb["calf_r"].rotation_euler.x = math.radians(82.0)
    pb["foot_r"].rotation_euler.x = math.radians(-15.0)
    pb["thigh_l"].rotation_euler = (math.radians(8.0), 0, math.radians(3.0))
    pb["calf_l"].rotation_euler.x = math.radians(18.0)
    pb["foot_l"].rotation_euler.x = math.radians(10.0)
    
    cam_obj.location = (1.55, -2.2, 1.30)
    cam_obj.rotation_euler = (math.radians(82), 0, math.radians(10))
    out_png = os.path.join(output_dir, "Kabir_v06_Action_Ladder_Climb.png")
    scene.render.filepath = out_png
    bpy.ops.render.render(write_still=True)
    shutil.copy2(out_png, os.path.join(artifact_dir, "Kabir_v06_Action_Ladder_Climb.png"))
    log("Rendered & Copied: Kabir_v06_Action_Ladder_Climb.png")

    # -------------------------------------------------------------
    # 6. CURFEW COVER LISTEN (Frame 30: Wall cover, head tilted listening)
    # -------------------------------------------------------------
    reset_pose(arm_obj)
    apply_relaxed_idle_base(pb)
    pb["pelvis"].location = (-0.03, 0.05, -0.06)
    pb["pelvis"].rotation_euler = (math.radians(4.0), math.radians(-3.0), math.radians(-18.0))
    pb["spine_01"].rotation_euler = (math.radians(6.0), math.radians(-4.0), math.radians(12.0))
    pb["spine_02"].rotation_euler = (math.radians(4.0), math.radians(-2.0), math.radians(8.0))
    pb["neck_01"].rotation_euler = (math.radians(-4.0), math.radians(14.0), math.radians(-28.0))
    pb["head"].rotation_euler = (math.radians(-6.0), math.radians(8.0), math.radians(-15.0))
    # Left hand braced flat against wall
    pb["upperarm_l"].rotation_euler = (math.radians(-25.0), math.radians(18.0), math.radians(-42.0))
    pb["lowerarm_l"].rotation_euler.x = math.radians(85.0)
    pb["hand_l"].rotation_euler = (math.radians(-22.0), 0, math.radians(15.0))
    # Right hand holding Webley at low ready
    pb["upperarm_r"].rotation_euler = (math.radians(18.0), math.radians(-8.0), math.radians(12.0))
    pb["lowerarm_r"].rotation_euler.x = math.radians(68.0)
    pb["hand_r"].rotation_euler = (math.radians(8.0), 0, 0)
    
    cam_obj.location = (1.45, -1.8, 1.35)
    cam_obj.rotation_euler = (math.radians(82), 0, math.radians(10))
    out_png = os.path.join(output_dir, "Kabir_v06_Action_Curfew_Listen.png")
    scene.render.filepath = out_png
    bpy.ops.render.render(write_still=True)
    shutil.copy2(out_png, os.path.join(artifact_dir, "Kabir_v06_Action_Curfew_Listen.png"))
    log("Rendered & Copied: Kabir_v06_Action_Curfew_Listen.png")

    # -------------------------------------------------------------
    # 7. SATCHEL OPEN / COURIER DISPATCH (Frame 20: Flap pull, dispatch inspection)
    # -------------------------------------------------------------
    reset_pose(arm_obj)
    apply_relaxed_idle_base(pb)
    pb["pelvis"].rotation_euler.z = math.radians(8.0)
    pb["spine_01"].rotation_euler.x = math.radians(8.0)
    pb["spine_02"].rotation_euler.x = math.radians(10.0)
    pb["neck_01"].rotation_euler.x = math.radians(18.0)
    pb["head"].rotation_euler.x = math.radians(15.0)
    # Left hand pulling satchel flap at hip
    pb["upperarm_l"].rotation_euler = (math.radians(18.0), math.radians(12.0), math.radians(-18.0))
    pb["lowerarm_l"].rotation_euler.x = math.radians(75.0)
    pb["hand_l"].rotation_euler = (math.radians(20.0), 0, math.radians(-15.0))
    # Right hand reaching into bag / holding dispatch
    pb["upperarm_r"].rotation_euler = (math.radians(22.0), math.radians(-14.0), math.radians(12.0))
    pb["lowerarm_r"].rotation_euler.x = math.radians(82.0)
    pb["hand_r"].rotation_euler = (math.radians(15.0), 0, math.radians(10.0))
    
    cam_obj.location = (1.45, -1.6, 1.20)
    cam_obj.rotation_euler = (math.radians(84), 0, math.radians(10))
    out_png = os.path.join(output_dir, "Kabir_v06_Action_Satchel_Open.png")
    scene.render.filepath = out_png
    bpy.ops.render.render(write_still=True)
    shutil.copy2(out_png, os.path.join(artifact_dir, "Kabir_v06_Action_Satchel_Open.png"))
    log("Rendered & Copied: Kabir_v06_Action_Satchel_Open.png")

    log("ALL FAST ACTION RENDERS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
