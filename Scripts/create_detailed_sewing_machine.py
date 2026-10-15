"""
PROJECT REVOLUTION — Master Prop Detailing: Master Tailor Singer Treadle Sewing Machine & Workstation
Kot Gurdarshan, April 1919 Punjab — Ram Lubhaya's Tailoring Workshop
Authentic Singer 15K Class Treadle Machine with Victorian Filigree, Teakwood Table, Shears & Cloth Bolts
"""

import bpy
import bmesh
import math
import os
from mathutils import Vector, Matrix

print("[PROP_SEWING_MACHINE] Initializing Sewing Machine & Workstation Pipeline...")

# ---------------------------------------------------------------------------
# 1. Clean Scene
# ---------------------------------------------------------------------------
for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj, do_unlink=True)
for mesh in list(bpy.data.meshes):
    bpy.data.meshes.remove(mesh, do_unlink=True)
for arm in list(bpy.data.armatures):
    bpy.data.armatures.remove(arm, do_unlink=True)
for mat in list(bpy.data.materials):
    bpy.data.materials.remove(mat, do_unlink=True)
for cam in list(bpy.data.cameras):
    bpy.data.cameras.remove(cam, do_unlink=True)
for light in list(bpy.data.lights):
    bpy.data.lights.remove(light, do_unlink=True)

# ---------------------------------------------------------------------------
# 2. PBR Materials
# ---------------------------------------------------------------------------
def make_shader(name, base_color, roughness=0.5, metallic=0.0, clearcoat=0.0, sheen=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = base_color
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = roughness
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = metallic
        if "Coat Weight" in bsdf.inputs and clearcoat > 0:
            bsdf.inputs["Coat Weight"].default_value = clearcoat
        elif "Clearcoat" in bsdf.inputs and clearcoat > 0:
            bsdf.inputs["Clearcoat"].default_value = clearcoat
        if "Sheen Weight" in bsdf.inputs and sheen > 0:
            bsdf.inputs["Sheen Weight"].default_value = sheen
    return mat

# Shaders
mat_black_enamel = make_shader("M_Singer_JapanBlack", (0.02, 0.02, 0.02, 1.0), roughness=0.15, clearcoat=0.8)
mat_cast_iron = make_shader("M_Treadle_CastIron", (0.08, 0.08, 0.09, 1.0), roughness=0.68, metallic=0.85)
mat_teak_wood = make_shader("M_Teak_Varnished", (0.38, 0.22, 0.11, 1.0), roughness=0.35, clearcoat=0.3)
mat_steel_chrome = make_shader("M_Polished_Steel", (0.90, 0.90, 0.92, 1.0), roughness=0.12, metallic=1.0)
mat_brass = make_shader("M_Antique_Brass", (0.84, 0.70, 0.28, 1.0), roughness=0.32, metallic=0.95)
mat_leather_belt = make_shader("M_Leather_Belt", (0.28, 0.16, 0.08, 1.0), roughness=0.62)
mat_gold_trim = make_shader("M_Gold_Filigree", (0.88, 0.76, 0.32, 1.0), roughness=0.28, metallic=0.90)
mat_khadi_cloth = make_shader("M_Khadi_Fabric", (0.86, 0.82, 0.74, 1.0), roughness=0.88, sheen=0.45)
mat_indigo_cloth = make_shader("M_Indigo_Cloth", (0.08, 0.14, 0.28, 1.0), roughness=0.85, sheen=0.40)
mat_saffron_thread = make_shader("M_Saffron_Thread", (0.95, 0.48, 0.04, 1.0), roughness=0.80)
mat_chalk = make_shader("M_Tailor_Chalk", (0.96, 0.96, 0.95, 1.0), roughness=0.95)

# Helper to create an object with material
def create_prop_mesh(name, material):
    m = bpy.data.meshes.new(f"{name}_Mesh")
    o = bpy.data.objects.new(name, m)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(material)
    return o, m

# ---------------------------------------------------------------------------
# 3. Cast-Iron Treadle Stand (Floor to Table Base, Height ~ 0.72m)
# ---------------------------------------------------------------------------
obj_treadle, mesh_treadle = create_prop_mesh("Treadle_Stand_CastIron", mat_cast_iron)
bm_t = bmesh.new()

# Left and Right Victorian Openwork Side Frames (Decorative A-frames)
for side_x in [-0.28, 0.28]:
    # Vertical leg uprights
    bmesh.ops.create_cube(bm_t, size=1.0, matrix=Matrix.Translation(Vector((side_x, -0.16, 0.36))) @ Matrix.Diagonal((0.025, 0.035, 0.70, 1.0)))
    bmesh.ops.create_cube(bm_t, size=1.0, matrix=Matrix.Translation(Vector((side_x, 0.16, 0.36))) @ Matrix.Diagonal((0.025, 0.035, 0.70, 1.0)))
    
    # Bottom floor runner foot with decorative pad
    bmesh.ops.create_cube(bm_t, size=1.0, matrix=Matrix.Translation(Vector((side_x, 0.0, 0.02))) @ Matrix.Diagonal((0.035, 0.42, 0.035, 1.0)))
    # Top table mounting rail
    bmesh.ops.create_cube(bm_t, size=1.0, matrix=Matrix.Translation(Vector((side_x, 0.0, 0.70))) @ Matrix.Diagonal((0.035, 0.38, 0.030, 1.0)))
    
    # Decorative Victorian arched filigree cross-members
    for fz in [0.22, 0.48]:
        bmesh.ops.create_cube(bm_t, size=1.0, matrix=Matrix.Translation(Vector((side_x, 0.0, fz))) @ Matrix.Diagonal((0.018, 0.32, 0.022, 1.0)))
    # Diagonal brace struts
    for sign in [-1, 1]:
        bmesh.ops.create_cone(bm_t, cap_ends=True, segments=8, radius1=0.010, radius2=0.010, depth=0.36, matrix=Matrix.Translation(Vector((side_x, sign * 0.08, 0.36))) @ Matrix.Rotation(math.radians(sign * 28.0), 4, 'X'))

# Horizontal Cross Stretcher Bars (connecting left and right frames)
bmesh.ops.create_cone(bm_t, cap_ends=True, segments=12, radius1=0.012, radius2=0.012, depth=0.56, matrix=Matrix.Translation(Vector((0.0, 0.0, 0.18))) @ Matrix.Rotation(math.radians(90.0), 4, 'Y'))
bmesh.ops.create_cone(bm_t, cap_ends=True, segments=12, radius1=0.014, radius2=0.014, depth=0.56, matrix=Matrix.Translation(Vector((0.0, 0.0, 0.55))) @ Matrix.Rotation(math.radians(90.0), 4, 'Y'))

# Cast-Iron Foot Treadle Pedal (Mounted low on pivot shaft)
# Slotted Victorian lattice footplate (0.28m wide x 0.18m deep)
bmesh.ops.create_cube(bm_t, size=1.0, matrix=Matrix.Translation(Vector((0.02, 0.04, 0.12))) @ Matrix.Rotation(math.radians(-14.0), 4, 'X') @ Matrix.Diagonal((0.26, 0.18, 0.018, 1.0)))
# Pedal pivot bar
bmesh.ops.create_cone(bm_t, cap_ends=True, segments=10, radius1=0.009, radius2=0.009, depth=0.32, matrix=Matrix.Translation(Vector((0.02, 0.0, 0.12))) @ Matrix.Rotation(math.radians(90.0), 4, 'Y'))

# Pitman Connecting Rod (from treadle pedal to flywheel crank)
bmesh.ops.create_cone(bm_t, cap_ends=True, segments=8, radius1=0.007, radius2=0.007, depth=0.34, matrix=Matrix.Translation(Vector((0.18, -0.01, 0.28))) @ Matrix.Rotation(math.radians(8.0), 4, 'X'))

# Large Spoked Cast-Iron Flywheel (Right side, Diameter ~ 0.32m)
flywheel_pos = Vector((0.21, -0.02, 0.42))
# Outer rim with belt groove
bmesh.ops.create_cone(bm_t, cap_ends=True, segments=24, radius1=0.16, radius2=0.16, depth=0.022, matrix=Matrix.Translation(flywheel_pos) @ Matrix.Rotation(math.radians(90.0), 4, 'Y'))
# Center hub
bmesh.ops.create_cone(bm_t, cap_ends=True, segments=16, radius1=0.038, radius2=0.038, depth=0.035, matrix=Matrix.Translation(flywheel_pos) @ Matrix.Rotation(math.radians(90.0), 4, 'Y'))
# 5 Curved Flywheel Spokes
for i in range(5):
    ang = 2 * math.pi * i / 5
    spoke_mat = Matrix.Translation(flywheel_pos) @ Matrix.Rotation(ang, 4, 'X') @ Matrix.Rotation(math.radians(90.0), 4, 'Z')
    bmesh.ops.create_cone(bm_t, cap_ends=True, segments=8, radius1=0.008, radius2=0.006, depth=0.13, matrix=spoke_mat @ Matrix.Translation(Vector((0.0, 0.0, 0.08))))

bm_t.to_mesh(mesh_treadle)
bm_t.free()
for p in mesh_treadle.polygons:
    p.use_smooth = True

# ---------------------------------------------------------------------------
# 4. Solid Teakwood Tabletop & Drawers (Table Surface at Z = 0.74m)
# ---------------------------------------------------------------------------
obj_table, mesh_table = create_prop_mesh("Workstation_Teak_Table", mat_teak_wood)
bm_w = bmesh.new()

# Main Tabletop (Width 0.88m, Depth 0.44m, Thickness 0.032m)
bmesh.ops.create_cube(bm_w, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 0.735))) @ Matrix.Diagonal((0.88, 0.44, 0.032, 1.0)))

# Left Drop-Leaf Extension Flap (Hinged extension)
bmesh.ops.create_cube(bm_w, size=1.0, matrix=Matrix.Translation(Vector((-0.55, 0.0, 0.735))) @ Matrix.Diagonal((0.22, 0.44, 0.030, 1.0)))

# Wooden Under-Frame Skirt & Drawer Casings
bmesh.ops.create_cube(bm_w, size=1.0, matrix=Matrix.Translation(Vector((0.0, 0.0, 0.695))) @ Matrix.Diagonal((0.84, 0.40, 0.048, 1.0)))

# Left Side Double Drawers Box
bmesh.ops.create_cube(bm_w, size=1.0, matrix=Matrix.Translation(Vector((-0.26, 0.0, 0.58))) @ Matrix.Diagonal((0.18, 0.36, 0.19, 1.0)))
# Two Drawer Front Moldings
bmesh.ops.create_cube(bm_w, size=1.0, matrix=Matrix.Translation(Vector((-0.26, 0.185, 0.635))) @ Matrix.Diagonal((0.165, 0.012, 0.080, 1.0)))
bmesh.ops.create_cube(bm_w, size=1.0, matrix=Matrix.Translation(Vector((-0.26, 0.185, 0.535))) @ Matrix.Diagonal((0.165, 0.012, 0.080, 1.0)))

# Right Single Drawer Box
bmesh.ops.create_cube(bm_w, size=1.0, matrix=Matrix.Translation(Vector((0.26, 0.0, 0.62))) @ Matrix.Diagonal((0.18, 0.36, 0.11, 1.0)))
bmesh.ops.create_cube(bm_w, size=1.0, matrix=Matrix.Translation(Vector((0.26, 0.185, 0.62))) @ Matrix.Diagonal((0.165, 0.012, 0.095, 1.0)))

bm_w.to_mesh(mesh_table)
bm_w.free()
for p in mesh_table.polygons:
    p.use_smooth = True

# Brass Drawer Cup Pulls (Shell / cup handles)
obj_pulls, mesh_pulls = create_prop_mesh("Drawer_Pulls_Brass", mat_brass)
bm_p = bmesh.new()
for px, pz in [(-0.26, 0.635), (-0.26, 0.535), (0.26, 0.62)]:
    bmesh.ops.create_cone(bm_p, cap_ends=True, segments=12, radius1=0.018, radius2=0.018, depth=0.008, matrix=Matrix.Translation(Vector((px, 0.192, pz))) @ Matrix.Rotation(math.radians(90.0), 4, 'X'))
bm_p.to_mesh(mesh_pulls)
bm_p.free()
for p in mesh_pulls.polygons:
    p.use_smooth = True

# ---------------------------------------------------------------------------
# 5. Singer 15K Sewing Machine Head (Black Japan Lacquer & Gold Filigree)
# ---------------------------------------------------------------------------
obj_singer, mesh_singer = create_prop_mesh("Singer_15K_Machine_Body", mat_black_enamel)
bm_s = bmesh.new()

# Rectangular Machine Bedplate (recessed into tabletop at Z = 0.75m)
bmesh.ops.create_cube(bm_s, size=1.0, matrix=Matrix.Translation(Vector((0.02, 0.0, 0.755))) @ Matrix.Diagonal((0.36, 0.175, 0.014, 1.0)))

# Vertical Arm Pillar (Right side upright column)
bmesh.ops.create_cone(bm_s, cap_ends=True, segments=18, radius1=0.042, radius2=0.036, depth=0.19, matrix=Matrix.Translation(Vector((0.14, 0.0, 0.855))))

# Horizontal Overarm (Curved arch spanning from pillar to needle head)
bmesh.ops.create_cone(bm_s, cap_ends=True, segments=18, radius1=0.038, radius2=0.032, depth=0.24, matrix=Matrix.Translation(Vector((0.02, 0.0, 0.942))) @ Matrix.Rotation(math.radians(90.0), 4, 'Y'))

# Needle Head Casting (Left side vertical housing)
bmesh.ops.create_cone(bm_s, cap_ends=True, segments=16, radius1=0.034, radius2=0.028, depth=0.16, matrix=Matrix.Translation(Vector((-0.10, 0.0, 0.88))))

# Spool Pin (Mounted on top of arm)
bmesh.ops.create_cone(bm_s, cap_ends=True, segments=8, radius1=0.003, radius2=0.002, depth=0.055, matrix=Matrix.Translation(Vector((0.08, 0.0, 0.985))))

# Stitch Length Regulator Lever (Pillar face)
bmesh.ops.create_cone(bm_s, cap_ends=True, segments=8, radius1=0.006, radius2=0.004, depth=0.032, matrix=Matrix.Translation(Vector((0.14, 0.042, 0.84))) @ Matrix.Rotation(math.radians(90.0), 4, 'X'))

# Gold Filigree Decorative Trim Rings & Medallion Decals
bmesh.ops.create_cone(bm_s, cap_ends=True, segments=18, radius1=0.043, radius2=0.043, depth=0.008, matrix=Matrix.Translation(Vector((0.14, 0.0, 0.78))))
bmesh.ops.create_cone(bm_s, cap_ends=True, segments=18, radius1=0.039, radius2=0.039, depth=0.008, matrix=Matrix.Translation(Vector((0.02, 0.0, 0.942))) @ Matrix.Rotation(math.radians(90.0), 4, 'Y'))

bm_s.to_mesh(mesh_singer)
bm_s.free()
for p in mesh_singer.polygons:
    p.use_smooth = True

# ---------------------------------------------------------------------------
# 6. Polished Steel Chrome Mechanics (Faceplate, Handwheel, Needle Bar)
# ---------------------------------------------------------------------------
obj_steel, mesh_steel = create_prop_mesh("Singer_Chrome_Mechanics", mat_steel_chrome)
bm_ch = bmesh.new()

# Engraved Victorian Faceplate (Left end of machine head)
bmesh.ops.create_cube(bm_ch, size=1.0, matrix=Matrix.Translation(Vector((-0.136, 0.0, 0.88))) @ Matrix.Diagonal((0.005, 0.052, 0.14, 1.0)))

# Slide Plate & Throat Plate (On bedplate beneath needle)
bmesh.ops.create_cube(bm_ch, size=1.0, matrix=Matrix.Translation(Vector((-0.10, 0.0, 0.763))) @ Matrix.Diagonal((0.11, 0.08, 0.004, 1.0)))

# Needle Bar (Vertical moving shaft)
bmesh.ops.create_cone(bm_ch, cap_ends=True, segments=8, radius1=0.003, radius2=0.003, depth=0.09, matrix=Matrix.Translation(Vector((-0.10, 0.0, 0.81))))

# Sewing Needle & Clamp
bmesh.ops.create_cone(bm_ch, cap_ends=True, segments=6, radius1=0.0015, radius2=0.0003, depth=0.038, matrix=Matrix.Translation(Vector((-0.10, 0.0, 0.778))))

# Presser Foot (Dual toes holding cloth)
bmesh.ops.create_cube(bm_ch, size=1.0, matrix=Matrix.Translation(Vector((-0.10, 0.008, 0.766))) @ Matrix.Diagonal((0.016, 0.024, 0.005, 1.0)))
# Presser bar vertical shaft
bmesh.ops.create_cone(bm_ch, cap_ends=True, segments=8, radius1=0.0035, radius2=0.0035, depth=0.08, matrix=Matrix.Translation(Vector((-0.10, -0.012, 0.815))))

# Balance Wheel / Handwheel (Right side, Diameter ~ 0.13m)
wheel_pos = Vector((0.195, 0.0, 0.942))
# Outer rim with belt groove
bmesh.ops.create_cone(bm_ch, cap_ends=True, segments=24, radius1=0.065, radius2=0.065, depth=0.022, matrix=Matrix.Translation(wheel_pos) @ Matrix.Rotation(math.radians(90.0), 4, 'Y'))
# Center chrome stop-motion knob
bmesh.ops.create_cone(bm_ch, cap_ends=True, segments=16, radius1=0.024, radius2=0.024, depth=0.034, matrix=Matrix.Translation(wheel_pos + Vector((0.008, 0, 0))) @ Matrix.Rotation(math.radians(90.0), 4, 'Y'))

# Thread Tension Assembly (Discs, conical beehive spring, thumb nut)
bmesh.ops.create_cone(bm_ch, cap_ends=True, segments=12, radius1=0.014, radius2=0.014, depth=0.016, matrix=Matrix.Translation(Vector((-0.07, 0.038, 0.88))) @ Matrix.Rotation(math.radians(90.0), 4, 'X'))

# Bobbin Winder Assembly (Attached near handwheel)
bmesh.ops.create_cone(bm_ch, cap_ends=True, segments=10, radius1=0.008, radius2=0.008, depth=0.035, matrix=Matrix.Translation(Vector((0.165, 0.035, 0.89))) @ Matrix.Rotation(math.radians(90.0), 4, 'X'))

bm_ch.to_mesh(mesh_steel)
bm_ch.free()
for p in mesh_steel.polygons:
    p.use_smooth = True

# ---------------------------------------------------------------------------
# 7. Leather Drive Belt & Thread Spool
# ---------------------------------------------------------------------------
obj_belt, mesh_belt = create_prop_mesh("Leather_Drive_Belt", mat_leather_belt)
bm_blt = bmesh.new()

# Closed looping belt spanning from machine handwheel (Z=0.942) down to flywheel (Z=0.42)
belt_top = Vector((0.195, 0.0, 0.942))
belt_bot = Vector((0.21, -0.02, 0.42))
for sign in [-1, 1]:
    p1 = belt_top + Vector((0.0, sign * 0.055, 0.0))
    p2 = belt_bot + Vector((0.0, sign * 0.14, 0.0))
    mid = (p1 + p2) * 0.5
    length = (p2 - p1).length
    bmesh.ops.create_cone(bm_blt, cap_ends=True, segments=8, radius1=0.0035, radius2=0.0035, depth=length, matrix=Matrix.Translation(mid) @ Matrix.Rotation(math.atan2(p2.y - p1.y, p2.z - p1.z), 4, 'X'))

bm_blt.to_mesh(mesh_belt)
bm_blt.free()

# Wooden Thread Spool with Saffron Cotton Thread (on spool pin)
obj_spool, mesh_spool = create_prop_mesh("Cotton_Thread_Spool", mat_saffron_thread)
bm_sp = bmesh.new()
# Wooden spool flanges & wound saffron thread cylinder
bmesh.ops.create_cone(bm_sp, cap_ends=True, segments=14, radius1=0.014, radius2=0.014, depth=0.036, matrix=Matrix.Translation(Vector((0.08, 0.0, 0.985))))
bm_sp.to_mesh(mesh_spool)
bm_sp.free()
for p in mesh_spool.polygons:
    p.use_smooth = True

# ---------------------------------------------------------------------------
# 8. Master Tailor Tools & Workshop Props on Table
# ---------------------------------------------------------------------------
# Heavy Forged Tailor's Shears (12-Inch shears lying beside machine)
obj_shears, mesh_shears = create_prop_mesh("Tailor_Forged_Shears", mat_steel_chrome)
obj_shears.data.materials.append(mat_brass)
bm_sh = bmesh.new()

shears_pos = Vector((-0.24, 0.10, 0.755))
# Steel Blades
bmesh.ops.create_cube(bm_sh, size=1.0, matrix=Matrix.Translation(shears_pos + Vector((0.04, 0.0, 0.003))) @ Matrix.Rotation(math.radians(-15.0), 4, 'Z') @ Matrix.Diagonal((0.14, 0.018, 0.004, 1.0)))
# Brass-plated Loop Handles (slot 1)
handle_mat = Matrix.Translation(shears_pos - Vector((0.05, 0.0, 0.0))) @ Matrix.Rotation(math.radians(-15.0), 4, 'Z')
loop1 = bmesh.ops.create_cone(bm_sh, cap_ends=True, segments=12, radius1=0.022, radius2=0.016, depth=0.008, matrix=handle_mat @ Matrix.Translation(Vector((0.0, 0.018, 0.004))))
loop2 = bmesh.ops.create_cone(bm_sh, cap_ends=True, segments=12, radius1=0.028, radius2=0.022, depth=0.008, matrix=handle_mat @ Matrix.Translation(Vector((0.0, -0.018, 0.004))))
for elem in [loop1, loop2]:
    for f in elem.get('faces', []):
        f.material_index = 1

bm_sh.to_mesh(mesh_shears)
bm_sh.free()
for p in mesh_shears.polygons:
    p.use_smooth = True

# Rolled Bolts of Khadi & Indigo Cotton Cloth (Stacked on table corner)
obj_cloth1, mesh_cloth1 = create_prop_mesh("Khadi_Cloth_Bolt", mat_khadi_cloth)
bm_cl1 = bmesh.new()
bmesh.ops.create_cone(bm_cl1, cap_ends=True, segments=16, radius1=0.048, radius2=0.048, depth=0.32, matrix=Matrix.Translation(Vector((-0.32, -0.10, 0.795))) @ Matrix.Rotation(math.radians(90.0), 4, 'X'))
bm_cl1.to_mesh(mesh_cloth1)
bm_cl1.free()
for p in mesh_cloth1.polygons:
    p.use_smooth = True

obj_cloth2, mesh_cloth2 = create_prop_mesh("Indigo_Cloth_Bolt", mat_indigo_cloth)
bm_cl2 = bmesh.new()
bmesh.ops.create_cone(bm_cl2, cap_ends=True, segments=16, radius1=0.042, radius2=0.042, depth=0.30, matrix=Matrix.Translation(Vector((-0.32, -0.10, 0.875))) @ Matrix.Rotation(math.radians(90.0), 4, 'X'))
bm_cl2.to_mesh(mesh_cloth2)
bm_cl2.free()
for p in mesh_cloth2.polygons:
    p.use_smooth = True

# Soapstone Tailor's Chalk (Sharpened triangular slab)
obj_chalk, mesh_chalk = create_prop_mesh("Tailor_Soapstone_Chalk", mat_chalk)
bm_ck = bmesh.new()
bmesh.ops.create_cone(bm_ck, cap_ends=True, segments=3, radius1=0.028, radius2=0.028, depth=0.006, matrix=Matrix.Translation(Vector((-0.08, 0.12, 0.755))))
bm_ck.to_mesh(mesh_chalk)
bm_ck.free()
for p in mesh_chalk.polygons:
    p.use_smooth = True

print("[PROP_SEWING_MACHINE] Machine body, treadle stand, teak table, shears, and cloth bolts constructed.")

# ---------------------------------------------------------------------------
# 9. Cinematic Studio Lighting & Showcase Cameras
# ---------------------------------------------------------------------------
# Key Light (Warm 3200K Workshop Sunlight)
l_key = bpy.data.lights.new("Sun_Key_Machine", 'POINT')
l_key.energy = 95.0
l_key.color = (1.0, 0.94, 0.85)
o_lkey = bpy.data.objects.new("Sun_Key_Machine", l_key)
o_lkey.location = (-0.8, 1.2, 1.4)
bpy.context.collection.objects.link(o_lkey)

# Rim Light (Accentuating polished chrome & black lacquer edge)
l_rim = bpy.data.lights.new("Rim_Light_Machine", 'POINT')
l_rim.energy = 65.0
l_rim.color = (0.75, 0.88, 1.0)
o_lrim = bpy.data.objects.new("Rim_Light_Machine", l_rim)
o_lrim.location = (0.9, -1.0, 1.3)
bpy.context.collection.objects.link(o_lrim)

# Fill Light (Warm diffuse ambient)
l_fill = bpy.data.lights.new("Fill_Light_Machine", 'POINT')
l_fill.energy = 35.0
l_fill.color = (0.95, 0.90, 0.85)
o_lfill = bpy.data.objects.new("Fill_Light_Machine", l_fill)
o_lfill.location = (0.8, 0.9, 0.8)
bpy.context.collection.objects.link(o_lfill)

# Studio World Neutral Slate Background
world = bpy.context.scene.world
if not world:
    world = bpy.data.worlds.new("Studio_World")
    bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs["Color"].default_value = (0.18, 0.19, 0.21, 1.0)
    bg.inputs["Strength"].default_value = 0.50

# Hero Camera (Front Three-Quarter Full Workstation View)
cam_hero = bpy.data.cameras.new("Cam_Hero_SewingMachine")
cam_hero.lens = 50.0
cam_hero_obj = bpy.data.objects.new("Cam_Hero_SewingMachine", cam_hero)
cam_hero_obj.location = (-0.75, 1.35, 1.15)
cam_hero_obj.rotation_euler = (math.radians(65.0), 0.0, math.radians(-152.0))
bpy.context.collection.objects.link(cam_hero_obj)
bpy.context.scene.camera = cam_hero_obj

# Detail Camera (Close-up of Singer 15K Machine Head, Shears & Brass Mechanics)
cam_detail = bpy.data.cameras.new("Cam_Detail_MachineHead")
cam_detail.lens = 85.0
cam_detail_obj = bpy.data.objects.new("Cam_Detail_MachineHead", cam_detail)
cam_detail_obj.location = (-0.35, 0.65, 0.98)
cam_detail_obj.rotation_euler = (math.radians(72.0), 0.0, math.radians(-155.0))
bpy.context.collection.objects.link(cam_detail_obj)

# Render settings
bpy.context.scene.render.resolution_x = 1280
bpy.context.scene.render.resolution_y = 960
bpy.context.scene.render.image_settings.file_format = 'PNG'

# ---------------------------------------------------------------------------
# 10. Save & Export to Both Designated Folders
# ---------------------------------------------------------------------------
art_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\PROJECT"
dest_dir = r"C:\Users\npal7\PROJECT\PROJECT"
os.makedirs(art_dir, exist_ok=True)
os.makedirs(dest_dir, exist_ok=True)

# Save .blend mainfiles
blend_art = os.path.join(art_dir, "Prop_Tailor_SewingMachine.blend")
blend_dest = os.path.join(dest_dir, "Prop_Tailor_SewingMachine.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_art)
bpy.ops.wm.save_as_mainfile(filepath=blend_dest)

# Export Static Mesh FBX
fbx_art = os.path.join(art_dir, "SM_Prop_Tailor_SewingMachine.fbx")
fbx_dest = os.path.join(dest_dir, "SM_Prop_Tailor_SewingMachine.fbx")

# Select all mesh objects
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
    if o.type == 'MESH':
        o.select_set(True)

for fpath in [fbx_art, fbx_dest]:
    bpy.ops.export_scene.fbx(
        filepath=fpath,
        use_selection=True,
        global_scale=100.0,
        axis_forward='-Z',
        axis_up='Y',
        apply_unit_scale=True,
        bake_space_transform=True,
        mesh_smooth_type='FACE'
    )

# Render Hero Shot
render_hero_art = os.path.join(art_dir, "Prop_Tailor_SewingMachine_Hero.png")
render_hero_dest = os.path.join(dest_dir, "Prop_Tailor_SewingMachine_Hero.png")
bpy.context.scene.camera = cam_hero_obj
bpy.context.scene.render.filepath = render_hero_art
bpy.ops.render.render(write_still=True)

import shutil
shutil.copyfile(render_hero_art, render_hero_dest)

# Render Detail Shot
render_detail_art = os.path.join(art_dir, "Prop_Tailor_SewingMachine_Detail.png")
render_detail_dest = os.path.join(dest_dir, "Prop_Tailor_SewingMachine_Detail.png")
bpy.context.scene.camera = cam_detail_obj
bpy.context.scene.render.filepath = render_detail_art
bpy.ops.render.render(write_still=True)
shutil.copyfile(render_detail_art, render_detail_dest)

print(f"[PROP_SEWING_MACHINE] SUCCESS! Saved .blend files to {blend_art} and {blend_dest}")
print(f"[PROP_SEWING_MACHINE] SUCCESS! Exported FBX to {fbx_art} and {fbx_dest}")
print(f"[PROP_SEWING_MACHINE] SUCCESS! Rendered Hero & Detail captures to both folders.")
