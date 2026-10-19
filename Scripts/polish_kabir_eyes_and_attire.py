"""
Polish Kabir v05 Eyes & Attire Cuffs:
1. Aligns eye gaze directly forward (adjusts Z rotation of left/right eye meshes).
2. Cleanly welds and bevels kurta hem and sleeve cuffs for solid stitched seams.
3. Re-renders face closeup and front views.
"""

import bpy
import bmesh
import math
import os
from mathutils import Vector

def align_eyes():
    # Rotate each eye about its own center to aim the pupil forward (-Y)
    for name, angle_deg in [("v05_Kabir_Eye_L", 24), ("v05_Kabir_Eye_R", -24)]:
        obj = bpy.data.objects.get(name)
        if obj:
            # Find center of eye
            verts = obj.data.vertices
            cx = sum(v.co.x for v in verts) / len(verts)
            cy = sum(v.co.y for v in verts) / len(verts)
            cz = sum(v.co.z for v in verts) / len(verts)
            
            rad = math.radians(angle_deg)
            cos_a = math.cos(rad)
            sin_a = math.sin(rad)
            
            for v in verts:
                # Translate to local eye origin
                lx = v.co.x - cx
                ly = v.co.y - cy
                # Rotate around Z
                nx = lx * cos_a - ly * sin_a
                ny = lx * sin_a + ly * cos_a
                v.co.x = cx + nx
                v.co.y = cy + ny
            obj.data.update()
            print(f"  Rotated {name} by {angle_deg} deg around Z.")

def clean_kurta_rims():
    kurta = bpy.data.objects.get("v05_Kabir_Kurta")
    if kurta:
        # Ensure smooth normals and remove double/split vertices
        bm = bmesh.new()
        bm.from_mesh(kurta.data)
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)
        # Recalculate face normals outward
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(kurta.data)
        bm.free()
        kurta.data.update()
        
        # Solidify modifier ensures thick, solid cloth hem
        sol = kurta.modifiers.get("Solidify")
        if not sol:
            sol = kurta.modifiers.new("Solidify", 'SOLIDIFY')
        sol.thickness = 0.003
        sol.offset = 0.0
        sol.use_rim = True
        sol.use_rim_only = False
        print("  Cleaned kurta normals and verified solid rim.")

def main():
    master_blend = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend"
    bpy.ops.wm.open_mainfile(filepath=master_blend)
    
    tex_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v05\Textures"
    render_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v05\Renders"
    
    print("Aligning eyes and cleaning attire rims...")
    align_eyes()
    clean_kurta_rims()
    
    scene = bpy.context.scene
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.image_settings.file_format = 'PNG'
    
    # 1. Close-up Face Portrait
    cam_d = bpy.data.cameras.new("CloseupCam")
    cam_d.lens = 75
    cam = bpy.data.objects.new("CloseupCam", cam_d)
    cam.location = (0.0, -0.95, 1.31)
    cam.rotation_euler = (math.radians(90), 0, 0)
    scene.collection.objects.link(cam)
    scene.camera = cam
    scene.render.filepath = os.path.join(render_dir, "v05_Textured_Face_Closeup.png")
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam, do_unlink=True)
    bpy.data.cameras.remove(cam_d)
    
    # 2. Front View
    cam_f_d = bpy.data.cameras.new("FrontCam")
    cam_f_d.lens = 45
    cam_f = bpy.data.objects.new("FrontCam", cam_f_d)
    cam_f.location = (0.0, -3.8, 0.72)
    cam_f.rotation_euler = (math.radians(90), 0, 0)
    scene.collection.objects.link(cam_f)
    scene.camera = cam_f
    scene.render.filepath = os.path.join(render_dir, "v05_Textured_Front.png")
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam_f, do_unlink=True)
    bpy.data.cameras.remove(cam_f_d)
    
    # Save blend files
    bpy.ops.wm.save_as_mainfile(filepath=master_blend)
    art_blend = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v05\Kabir_v05.blend"
    bpy.ops.wm.save_as_mainfile(filepath=art_blend)
    print("=== EYE ALIGNMENT & RIM POLISH COMPLETE ===")

if __name__ == "__main__":
    main()
