"""
PROJECT REVOLUTION — Test High-Fidelity PBR Skin & Eye Shading on Kabir v06 Adult
Builds complete node trees with BC, Normal, ORM, and SSS maps and renders a portrait.
"""
import os
import math
import bpy

blend_path = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v06\Kabir_v06_Heritage_Ages.blend"
bpy.ops.wm.open_mainfile(filepath=blend_path)

tex_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v05\Textures"
head_bc = os.path.join(tex_dir, "T_Kabir_Head_BC.png")
head_n  = os.path.join(tex_dir, "T_Kabir_Head_N.png")
head_orm = os.path.join(tex_dir, "T_Kabir_Head_ORM.png")
head_sss = os.path.join(tex_dir, "T_Kabir_Head_SSS.png")
eye_bc   = os.path.join(tex_dir, "T_Kabir_Eye_BC.png")

# 1. Build M_Kabir_v06_Skin node tree
mat_skin = bpy.data.materials.get("M_Kabir_v06_Skin")
if not mat_skin:
    mat_skin = bpy.data.materials.new("M_Kabir_v06_Skin")
mat_skin.use_nodes = True
nodes = mat_skin.node_tree.nodes
links = mat_skin.node_tree.links
nodes.clear()

out_node = nodes.new('ShaderNodeOutputMaterial')
out_node.location = (800, 0)

bsdf = nodes.new('ShaderNodeBsdfPrincipled')
bsdf.location = (400, 0)
links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])

# Base Color Image
tex_bc = nodes.new('ShaderNodeTexImage')
tex_bc.image = bpy.data.images.load(head_bc)
tex_bc.location = (-400, 200)

# Color Grading for Warm Indo-Aryan Bronze Undertone (#B37F56)
hue_sat = nodes.new('ShaderNodeHueSaturation')
hue_sat.location = (-100, 200)
hue_sat.inputs['Hue'].default_value = 0.50
hue_sat.inputs['Saturation'].default_value = 1.08
hue_sat.inputs['Value'].default_value = 0.95
links.new(tex_bc.outputs['Color'], hue_sat.inputs['Color'])
links.new(hue_sat.outputs['Color'], bsdf.inputs['Base Color'])

# Normal Map
tex_n = nodes.new('ShaderNodeTexImage')
tex_n.image = bpy.data.images.load(head_n)
tex_n.image.colorspace_settings.name = 'Non-Color'
tex_n.location = (-400, -300)

n_map = nodes.new('ShaderNodeNormalMap')
n_map.location = (-100, -300)
n_map.inputs['Strength'].default_value = 1.15
links.new(tex_n.outputs['Color'], n_map.inputs['Color'])
links.new(n_map.outputs['Normal'], bsdf.inputs['Normal'])

# ORM (Occlusion, Roughness, Metallic)
tex_orm = nodes.new('ShaderNodeTexImage')
tex_orm.image = bpy.data.images.load(head_orm)
tex_orm.image.colorspace_settings.name = 'Non-Color'
tex_orm.location = (-400, -50)

sep_col = nodes.new('ShaderNodeSeparateColor')
sep_col.location = (-100, -50)
links.new(tex_orm.outputs['Color'], sep_col.inputs['Color'])
# G channel = Roughness
links.new(sep_col.outputs['Green'], bsdf.inputs['Roughness'])

# SSS Map
tex_sss = nodes.new('ShaderNodeTexImage')
tex_sss.image = bpy.data.images.load(head_sss)
tex_sss.image.colorspace_settings.name = 'Non-Color'
tex_sss.location = (-400, -550)

if 'Subsurface Weight' in bsdf.inputs:
    links.new(tex_sss.outputs['Color'], bsdf.inputs['Subsurface Weight'])
    if 'Subsurface Radius' in bsdf.inputs:
        bsdf.inputs['Subsurface Radius'].default_value = (1.0, 0.45, 0.25)
    if 'Subsurface Scale' in bsdf.inputs:
        bsdf.inputs['Subsurface Scale'].default_value = 0.015
elif 'Subsurface' in bsdf.inputs:
    links.new(tex_sss.outputs['Color'], bsdf.inputs['Subsurface'])

# 2. Build M_Kabir_v06_Eye node tree
mat_eye = bpy.data.materials.get("M_Kabir_v06_Eye")
if not mat_eye:
    mat_eye = bpy.data.materials.new("M_Kabir_v06_Eye")
mat_eye.use_nodes = True
nodes_e = mat_eye.node_tree.nodes
links_e = mat_eye.node_tree.links
nodes_e.clear()

out_e = nodes_e.new('ShaderNodeOutputMaterial')
out_e.location = (600, 0)
bsdf_e = nodes_e.new('ShaderNodeBsdfPrincipled')
bsdf_e.location = (200, 0)
links_e.new(bsdf_e.outputs['BSDF'], out_e.inputs['Surface'])

tex_eye = nodes_e.new('ShaderNodeTexImage')
tex_eye.image = bpy.data.images.load(eye_bc)
tex_eye.location = (-200, 0)
links_e.new(tex_eye.outputs['Color'], bsdf_e.inputs['Base Color'])
bsdf_e.inputs['Roughness'].default_value = 0.04
if 'IOR' in bsdf_e.inputs:
    bsdf_e.inputs['IOR'].default_value = 1.376

# Setup Camera for Close-Up Face Shot
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, 'RenderEngine') and 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080

cam = scene.camera
if not cam:
    cam_data = bpy.data.cameras.new("Cam_Face_Test")
    cam = bpy.data.objects.new("Cam_Face_Test", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam

# Adult 25 is at X=1.2 in the master blend
cam.location = (1.20, -0.65, 1.63)
cam.rotation_euler = (math.radians(90), 0, 0)
cam.data.lens = 85.0
cam.data.dof.use_dof = True
cam.data.dof.focus_distance = 0.65
cam.data.dof.aperture_fstop = 2.8

# Add cinematic portrait rim & fill lights
rim = bpy.data.lights.new("Rim_Face", 'SPOT')
rim.energy = 450.0
rim.spot_size = math.radians(65)
rim.color = (1.0, 0.88, 0.70)
rim_obj = bpy.data.objects.new("Rim_Face", rim)
rim_obj.location = (1.55, 0.50, 1.95)
rim_obj.rotation_euler = (math.radians(-125), math.radians(20), 0)
scene.collection.objects.link(rim_obj)

fill = bpy.data.lights.new("Fill_Face", 'POINT')
fill.energy = 180.0
fill.color = (0.75, 0.85, 1.0)
fill_obj = bpy.data.objects.new("Fill_Face", fill)
fill_obj.location = (0.70, -0.50, 1.65)
scene.collection.objects.link(fill_obj)

key = bpy.data.lights.new("Key_Face", 'SPOT')
key.energy = 650.0
key.spot_size = math.radians(45)
key.color = (1.0, 0.95, 0.88)
key_obj = bpy.data.objects.new("Key_Face", key)
key_obj.location = (1.50, -0.75, 1.85)
key_obj.rotation_euler = (math.radians(70), math.radians(-15), math.radians(25))
scene.collection.objects.link(key_obj)

out_file = r"C:\Users\npal7\.gemini\antigravity\brain\f71e59c5-c47d-4ecc-9d85-fded280f9f20\Kabir_v06_PBR_Face_Test.png"
scene.render.filepath = out_file
bpy.ops.render.render(write_still=True)
print(f"Rendered test portrait to {out_file} ({os.path.getsize(out_file)} bytes)")
