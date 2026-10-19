"""
Enhance Kabir v05 PBR Shaders:
1. Realistic skin roughness (0.52 - 0.62) to remove plastic sheen.
2. Detailed eye texture with pupil, striated iris, limbal ring, and sclera.
3. Natural dark hair shading.
4. Re-renders beauty and closeup views.
"""

import bpy
import math
import os
import struct
import zlib
import random

def write_png(filename, width, height, rgba_data):
    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF)
    sig = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0))
    raw_rows = bytearray()
    row_stride = width * 4
    for y in range(height):
        raw_rows.append(0)
        raw_rows.extend(rgba_data[y * row_stride : (y + 1) * row_stride])
    idat = chunk(b'IDAT', zlib.compress(bytes(raw_rows), 6))
    iend = chunk(b'IEND', b'')
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as f:
        f.write(sig + ihdr + idat + iend)

def clamp(val, min_v=0, max_v=255):
    return max(min_v, min(max_v, int(val)))

def update_skin_orm(tex_dir):
    orm_path = os.path.join(tex_dir, "T_Kabir_Head_ORM.png")
    size = 2048
    orm = bytearray(size * size * 4)
    rng = random.Random(1919)
    for y in range(size):
        ny = y / size
        for x in range(size):
            nx = x / size
            idx = (y * size + x) * 4
            dx = nx - 0.5
            dy = ny - 0.5
            dist = math.sqrt(dx*dx + dy*dy)
            # Roughness: 140 (0.55) general, 125 (0.49) on nose/forehead, 155 (0.61) on cheeks/neck
            rough = 145 + int((rng.random() - 0.5) * 8)
            if dist < 0.2:
                rough -= 12 # subtle natural T-zone oiliness
            orm[idx] = 245      # AO
            orm[idx + 1] = clamp(rough) # Roughness
            orm[idx + 2] = 0    # Metallic
            orm[idx + 3] = 255
    write_png(orm_path, size, size, orm)
    print("  Updated T_Kabir_Head_ORM.png with natural matte roughness.")

def generate_eye_texture(tex_dir):
    size = 512
    eye_bc = bytearray(size * size * 4)
    cx, cy = size / 2.0, size / 2.0
    r_pupil = size * 0.12
    r_iris = size * 0.32
    r_limbal = size * 0.34
    
    rng = random.Random(1919)
    
    for y in range(size):
        for x in range(size):
            idx = (y * size + x) * 4
            dx = x - cx
            dy = y - cy
            dist = math.sqrt(dx*dx + dy*dy)
            angle = math.atan2(dy, dx)
            
            if dist <= r_pupil:
                # Deep black pupil
                r, g, b = 12, 10, 10
            elif dist <= r_iris:
                # Striated golden-brown iris
                t = (dist - r_pupil) / (r_iris - r_pupil)
                striae = math.sin(angle * 32.0) * 18.0 + math.sin(angle * 64.0) * 10.0
                # Warm amber brown transitioning to deeper chestnut
                base_r = 110 + int(t * 40 + striae)
                base_g = 68 + int(t * 22 + striae * 0.6)
                base_b = 32 + int(t * 12 + striae * 0.3)
                r, g, b = clamp(base_r), clamp(base_g), clamp(base_b)
            elif dist <= r_limbal:
                # Dark limbal ring
                lt = (dist - r_iris) / (r_limbal - r_iris)
                r = clamp(35 + int(lt * 140))
                g = clamp(25 + int(lt * 155))
                b = clamp(20 + int(lt * 165))
            else:
                # Sclera (off-white with subtle reddish veins near edges)
                sclera_edge = (dist - r_limbal) / (size * 0.5 - r_limbal)
                vein = 0.0
                if rng.random() > 0.96 and sclera_edge > 0.3:
                    vein = 35.0
                r = clamp(232 - int(sclera_edge * 15) + vein)
                g = clamp(225 - int(sclera_edge * 28))
                b = clamp(220 - int(sclera_edge * 32))
                
            eye_bc[idx] = r
            eye_bc[idx + 1] = g
            eye_bc[idx + 2] = b
            eye_bc[idx + 3] = 255
            
    eye_path = os.path.join(tex_dir, "T_Kabir_Eye_BC.png")
    write_png(eye_path, size, size, eye_bc)
    print("  Generated T_Kabir_Eye_BC.png.")
    return eye_path

def main():
    master_blend = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend"
    bpy.ops.wm.open_mainfile(filepath=master_blend)
    
    tex_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v05\Textures"
    render_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v05\Renders"
    
    update_skin_orm(tex_dir)
    eye_tex_path = generate_eye_texture(tex_dir)
    
    # Reload updated ORM image
    for img in bpy.data.images:
        if "ORM" in img.name or "Eye" in img.name:
            img.reload()
            
    # Set up Eye PBR Material
    mat_eye = bpy.data.materials.get("M_Kabir_Eye_PBR")
    if not mat_eye:
        mat_eye = bpy.data.materials.new(name="M_Kabir_Eye_PBR")
        mat_eye.use_nodes = True
    bsdf_e = mat_eye.node_tree.nodes.get("Principled BSDF")
    if bsdf_e:
        tex_e = mat_eye.node_tree.nodes.new('ShaderNodeTexImage')
        tex_e.image = bpy.data.images.load(eye_tex_path)
        mat_eye.node_tree.links.new(tex_e.outputs['Color'], bsdf_e.inputs['Base Color'])
        bsdf_e.inputs['Roughness'].default_value = 0.04
        bsdf_e.inputs['IOR'].default_value = 1.376
        
    for name in ["v05_Kabir_Eye_L", "v05_Kabir_Eye_R"]:
        o = bpy.data.objects.get(name)
        if o:
            o.data.materials.clear()
            o.data.materials.append(mat_eye)
            
    # Adjust hair shading to deep natural charcoal black
    hair = bpy.data.objects.get("v05_Kabir_Hair")
    if hair and hair.data.materials:
        mat_h = hair.data.materials[0]
        bsdf_h = mat_h.node_tree.nodes.get("Principled BSDF")
        if bsdf_h:
            bsdf_h.inputs['Base Color'].default_value = (0.025, 0.022, 0.020, 1.0)
            bsdf_h.inputs['Roughness'].default_value = 0.65
            
    # Re-render Face Closeup
    scene = bpy.context.scene
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.image_settings.file_format = 'PNG'
    
    # Closeup cam
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
    
    # Three-quarter cam
    cam_3q_d = bpy.data.cameras.new("3QCam")
    cam_3q_d.lens = 45
    cam_3q = bpy.data.objects.new("3QCam", cam_3q_d)
    cam_3q.location = (2.8, -3.2, 0.72)
    cam_3q.rotation_euler = (math.radians(90), 0, math.radians(41))
    scene.collection.objects.link(cam_3q)
    scene.camera = cam_3q
    scene.render.filepath = os.path.join(render_dir, "v05_Textured_ThreeQuarter.png")
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam_3q, do_unlink=True)
    bpy.data.cameras.remove(cam_3q_d)
    
    # Save blends
    bpy.ops.wm.save_as_mainfile(filepath=master_blend)
    art_blend = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v05\Kabir_v05.blend"
    bpy.ops.wm.save_as_mainfile(filepath=art_blend)
    print("=== ENHANCEMENT COMPLETE ===")

if __name__ == "__main__":
    main()
