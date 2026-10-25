"""
PROJECT REVOLUTION — Render Extended Action Suite & Webley Prop
Renders:
1. Anim_Kabir_v06_Run (Frame 10 - Peak forward sprint stride)
2. Anim_Kabir_v06_Stop (Frame 8 - RDR2 lead-foot plant & deceleration dip)
3. Anim_Kabir_v06_Jump (Frame 12 - Apex leap height)
4. Anim_Kabir_v06_Mantle (Frame 18 - Rooftop ledge heave)
5. Anim_Kabir_v06_Climb_Ladder (Frame 15 - Hand-over-hand ladder ascent)
6. Anim_Kabir_v06_Curfew_Listen (Frame 30 - Sentry listening cover)
7. Anim_Kabir_v06_Satchel_Open (Frame 20 - Courier dispatch inspection)
8. Prop_Webley_Revolver_Hero (Macro closeup of the 1919 service sidearm)
"""

import os
import math
import shutil
import bpy

def log(msg):
    print(f"[EXTENDED_RENDER] {msg}", flush=True)

def main():
    log("================================================================================")
    log("  RENDERING EXTENDED ACTION SHOWCASE & WEBLEY PROP")
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
    scene.render.film_transparent = False
    
    arm_obj = bpy.data.objects.get("Kabir_v06_Adult_25_Armature")
    if not arm_obj:
        log("ERROR: Adult armature not found!")
        return
        
    cam = scene.camera
    if not cam:
        cam_data = bpy.data.cameras.new("Cam_Extended")
        cam = bpy.data.objects.new("Cam_Extended", cam_data)
        scene.collection.objects.link(cam)
        scene.camera = cam
    cam.data.lens = 60.0
    
    shots = [
        ("Anim_Kabir_v06_Run", 10, "Kabir_v06_Action_Run_Sprint.png", (1.65, -2.4, 1.25), (math.radians(82), 0, math.radians(10))),
        ("Anim_Kabir_v06_Stop", 8, "Kabir_v06_Action_Stop_Decel.png", (1.65, -2.4, 1.20), (math.radians(82), 0, math.radians(10))),
        ("Anim_Kabir_v06_Jump", 12, "Kabir_v06_Action_Jump_Apex.png", (1.65, -2.5, 1.45), (math.radians(80), 0, math.radians(10))),
        ("Anim_Kabir_v06_Mantle", 18, "Kabir_v06_Action_Mantle_Heave.png", (1.55, -2.2, 1.40), (math.radians(80), 0, math.radians(10))),
        ("Anim_Kabir_v06_Climb_Ladder", 15, "Kabir_v06_Action_Ladder_Climb.png", (1.55, -2.2, 1.30), (math.radians(82), 0, math.radians(10))),
        ("Anim_Kabir_v06_Curfew_Listen", 30, "Kabir_v06_Action_Curfew_Listen.png", (1.45, -1.8, 1.35), (math.radians(82), 0, math.radians(10))),
        ("Anim_Kabir_v06_Satchel_Open", 20, "Kabir_v06_Action_Satchel_Open.png", (1.45, -1.6, 1.20), (math.radians(84), 0, math.radians(10)))
    ]
    
    for act_name, frame, filename, cam_loc, cam_rot in shots:
        act = bpy.data.actions.get(act_name)
        if not act:
            log(f"WARNING: Action {act_name} not found!")
            continue
            
        if arm_obj.animation_data is None:
            arm_obj.animation_data_create()
        arm_obj.animation_data.action = act
        scene.frame_set(frame)
        
        cam.location = cam_loc
        cam.rotation_euler = cam_rot
        
        out_path = os.path.join(output_dir, filename)
        scene.render.filepath = out_path
        bpy.ops.render.render(write_still=True)
        log(f"Rendered: {filename}")
        
        # Copy to artifact directory
        dest_art = os.path.join(artifact_dir, filename)
        shutil.copy2(out_path, dest_art)
        log(f"  Copied to artifact dir: {dest_art}")
        
    # Now render Webley Revolver Prop closeup
    revolver = bpy.data.objects.get("Prop_Webley_Revolver")
    if revolver:
        log("Rendering Webley Revolver hero closeup...")
        # Point camera at right hand / revolver
        # In Aim pose (frame 15)
        aim_act = bpy.data.actions.get("Anim_Kabir_v06_Weapon_Aim")
        if aim_act:
            arm_obj.animation_data.action = aim_act
            scene.frame_set(15)
            
        cam.data.lens = 90.0
        # Revolver is at chest/aim height
        cam.location = (1.1, -1.0, 1.35)
        cam.rotation_euler = (math.radians(85), 0, math.radians(-35))
        
        webley_png = os.path.join(output_dir, "Kabir_v06_Prop_Webley_Revolver_Closeup.png")
        scene.render.filepath = webley_png
        bpy.ops.render.render(write_still=True)
        log(f"Rendered Webley closeup: {webley_png}")
        
        dest_art = os.path.join(artifact_dir, "Kabir_v06_Prop_Webley_Revolver_Closeup.png")
        shutil.copy2(webley_png, dest_art)
        log(f"  Copied Webley closeup to: {dest_art}")
        
    log("ALL EXTENDED ACTION RENDERS COMPLETED!")

if __name__ == "__main__":
    main()
