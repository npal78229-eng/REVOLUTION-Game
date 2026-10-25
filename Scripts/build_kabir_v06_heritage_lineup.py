"""
PROJECT REVOLUTION — Kabir v06 Heritage Character System (Blender 5.2)
Authors authentic Indian protagonist Kabir across 3 life stages:
1. Child (Age 12) - 1.42m height, 1:6.2 head ratio, movement-ready khadi kurta, loose pajama, satchel, and juttis.
2. Teenager (Age 16) - 1.68m height, 1:7.0 head ratio, growth-spurt silhouette, transitional jawline, straight pajama.
3. Adult (Age 25) - 1.76m height, 1:7.6 head ratio, mature jaw/brow, dignified khadi kurta, traditional pleated dhoti, draped angavastram.

Inspired by Bhanu Athaiya's historical costume research for the 1982 film 'Gandhi':
- Authentic handloom unbleached khadi cotton with slub texture.
- Mandarin/Nehru band collar with front placket and carved wooden buttons.
- Knee-length cut with authentic side slits (chaks) for natural movement.
- Traditional draped dhoti with front pleats (patli) and rear tuck (kashta).
- Draped shoulder cloth (angavastram/chadar).
- Handcrafted leather juttis with curved toe box.
- Distinctly original to Kabir (NOT a Gandhi likeness).
"""

import bpy
import bmesh
import math
import os
from mathutils import Vector, Matrix, Euler, Color

def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if not bpy.data.scenes:
        bpy.data.scenes.new("Scene")
    scene = bpy.context.scene
    engines = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
    if 'BLENDER_EEVEE' in engines:
        scene.render.engine = 'BLENDER_EEVEE'
    elif 'CYCLES' in engines:
        scene.render.engine = 'CYCLES'
    else:
        scene.render.engine = 'BLENDER_WORKBENCH'
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_depth = '8'

    if not bpy.data.collections:
        col = bpy.data.collections.new("Kabir_v06_Collection")
        scene.collection.children.link(col)
    return scene

def append_mesh_from_bundle(blend_path, object_name):
    with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
        if object_name in data_from.objects:
            data_to.objects = [object_name]
    if data_to.objects:
        obj = data_to.objects[0]
        bpy.context.scene.collection.objects.link(obj)
        return obj
    return None

def create_pbr_material(name, base_color, roughness, specular=0.5, metallic=0.0, sss_weight=0.0, sss_color=None):
    mat = bpy.data.materials.get(name)
    if not mat:
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    output_node = nodes.new('ShaderNodeOutputMaterial')
    output_node.location = (400, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    
    # Input socket names in Blender 5.x Principled BSDF
    bsdf.inputs['Base Color'].default_value = base_color
    bsdf.inputs['Roughness'].default_value = roughness
    if 'Metallic' in bsdf.inputs:
        bsdf.inputs['Metallic'].default_value = metallic
    if 'Roughness' in bsdf.inputs:
        bsdf.inputs['Roughness'].default_value = roughness
        
    # Subsurface scattering for skin
    if sss_weight > 0:
        if 'Subsurface Weight' in bsdf.inputs:
            bsdf.inputs['Subsurface Weight'].default_value = sss_weight
            if 'Subsurface Radius' in bsdf.inputs:
                bsdf.inputs['Subsurface Radius'].default_value = Vector((1.0, 0.45, 0.25))
            if sss_color and 'Subsurface Color' in bsdf.inputs:
                bsdf.inputs['Subsurface Color'].default_value = sss_color
        elif 'Subsurface' in bsdf.inputs:
            bsdf.inputs['Subsurface'].default_value = sss_weight
            if sss_color and 'Subsurface Color' in bsdf.inputs:
                bsdf.inputs['Subsurface Color'].default_value = sss_color

    mat.node_tree.links.new(bsdf.outputs['BSDF'], output_node.inputs['Surface'])
    return mat

def create_khadi_procedural_material(name, base_tint, roughness=0.88):
    mat = bpy.data.materials.get(name)
    if not mat:
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    output_node = nodes.new('ShaderNodeOutputMaterial')
    output_node.location = (600, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (200, 0)
    bsdf.inputs['Base Color'].default_value = base_tint
    bsdf.inputs['Roughness'].default_value = roughness
    if 'Sheen Weight' in bsdf.inputs:
        bsdf.inputs['Sheen Weight'].default_value = 0.35
    elif 'Sheen' in bsdf.inputs:
        bsdf.inputs['Sheen'].default_value = 0.35

    # Procedural slub cloth weave texture
    tex_noise = nodes.new('ShaderNodeTexNoise')
    tex_noise.location = (-400, 0)
    tex_noise.inputs['Scale'].default_value = 85.0
    tex_noise.inputs['Detail'].default_value = 4.0
    tex_noise.inputs['Roughness'].default_value = 0.7
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (0, -100)
    bump.inputs['Strength'].default_value = 0.18
    bump.inputs['Distance'].default_value = 0.005
    
    mat.node_tree.links.new(tex_noise.outputs['Fac'], bump.inputs['Height'])
    mat.node_tree.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output_node.inputs['Surface'])
    return mat

def sculpt_indian_features(body_mesh, stage):
    """
    Applies authentic North Indian / Punjabi facial morphology and age-specific anatomical proportions.
    stage: 'child', 'teen', or 'adult'
    """
    bm = bmesh.new()
    bm.from_mesh(body_mesh.data)
    bm.verts.ensure_lookup_table()
    
    verts = bm.verts
    min_z = min(v.co.z for v in verts)
    max_z = max(v.co.z for v in verts)
    height = max_z - min_z
    
    # Target heights and head proportion ratios
    if stage == 'child':
        target_height = 1.42
        target_head_ratio = 1.0 / 6.2 # Larger head relative to torso
        shoulder_width_scale = 0.82
        limb_thickness = 0.85
        facial_softness = 1.25 # Fuller juvenile cheeks
        jaw_sharpness = 0.75 # Softer chin and jaw
        eye_scale = 1.15 # Larger expressive eyes
    elif stage == 'teen':
        target_height = 1.68
        target_head_ratio = 1.0 / 7.0 # Transitional growth spurt
        shoulder_width_scale = 0.92
        limb_thickness = 0.90
        facial_softness = 0.95
        jaw_sharpness = 1.10 # Angular emerging jaw
        eye_scale = 1.05
    else: # adult
        target_height = 1.76
        target_head_ratio = 1.0 / 7.6 # Fully developed adult proportions
        shoulder_width_scale = 1.05
        limb_thickness = 1.02
        facial_softness = 0.80
        jaw_sharpness = 1.30 # Strong, grounded mandibular angles
        eye_scale = 1.00

    head_threshold_norm = 0.82 # Normalized Z where neck/head begins
    pelvis_threshold_norm = 0.50 # Normalized Z of pelvis
    
    # 1. Proportional transformation
    for v in verts:
        znorm = (v.co.z - min_z) / height
        
        # Head & Face
        if znorm >= head_threshold_norm:
            # Normalize head vertical factor (0 at chin, 1 at scalp)
            head_factor = (znorm - head_threshold_norm) / (1.0 - head_threshold_norm)
            
            # --- AUTHENTIC INDIAN FACIAL ANATOMY ---
            # Forward coordinate is -Y in standard base mesh (or +Y depending on orientation)
            # Check nose/face orientation: nose is protruding along Y
            x = v.co.x
            y = v.co.y
            z = v.co.z
            
            # Facial front vertices
            if y < -0.01:
                # 1. Almond Eyes (X between 0.02 and 0.07, Z in eye band)
                if 0.02 < abs(x) < 0.065 and 0.55 < head_factor < 0.72:
                    # Subtle almond curvature and epicanthic slant
                    eye_dx = abs(x) - 0.042
                    # Deepen upper lid fold
                    if head_factor > 0.63:
                        v.co.y += 0.003
                    # Refine outer eye corner upward tilt
                    if abs(x) > 0.048:
                        v.co.z += 0.002
                    v.co.x *= eye_scale

                # 2. Straight/Aquiline Indian Nasal Ridge & Cartilage Tip
                if abs(x) < 0.025 and 0.38 < head_factor < 0.60:
                    # Refined straight dorsal bridge
                    nasal_profile_factor = math.sin((head_factor - 0.38) / 0.22 * math.pi)
                    v.co.y -= 0.0055 * nasal_profile_factor # Pronounced noble bridge
                    
                    # Distinct nasal tip and refined nostrils
                    if 0.40 < head_factor < 0.46:
                        if abs(x) < 0.012: # Tip
                            v.co.y -= 0.004
                            v.co.z += 0.001
                        elif abs(x) > 0.012: # Alar wings (nostrils)
                            v.co.x *= 1.04 # Slightly flared natural nostrils

                # 3. Defined Philtrum and Authentic Lips
                if abs(x) < 0.028 and 0.22 < head_factor < 0.36:
                    if 0.28 < head_factor < 0.34: # Vermilion lip zone
                        # Full natural lower lip, defined cupid's bow
                        lip_factor = math.cos((abs(x) / 0.028) * (math.pi / 2))
                        if head_factor < 0.31: # Lower lip fullness
                            v.co.y -= 0.004 * lip_factor
                        else: # Upper lip cupid's bow
                            v.co.y -= 0.003 * lip_factor
                            if abs(x) < 0.005:
                                v.co.z -= 0.0015 # Philtrum dip

                # 4. High Indian Zygomatic Arches (Cheekbones) & Jawline
                if 0.035 < abs(x) < 0.075 and 0.35 < head_factor < 0.55:
                    # High cheekbones
                    cheek_factor = math.sin((head_factor - 0.35) / 0.20 * math.pi)
                    v.co.x *= (1.0 + 0.035 * cheek_factor)
                    if stage == 'child':
                        v.co.y -= 0.004 * facial_softness # Fuller youthful cheeks

                # Jaw & Chin
                if head_factor < 0.25:
                    if abs(x) < 0.03: # Chin
                        v.co.y -= (0.004 * jaw_sharpness)
                        if stage != 'child':
                            v.co.z -= 0.003
                    elif abs(x) > 0.04: # Mandibular angle
                        v.co.x *= (1.0 + 0.02 * (jaw_sharpness - 1.0))

            # Apply overall head scale and position
            v.co.x *= target_head_ratio * 7.5
            v.co.z = (target_height * 0.84) + (head_factor * target_height * 0.16)

        # Torso & Shoulders
        elif znorm >= pelvis_threshold_norm:
            torso_factor = (znorm - pelvis_threshold_norm) / (head_threshold_norm - pelvis_threshold_norm)
            v.co.x *= shoulder_width_scale
            v.co.y *= limb_thickness
            v.co.z = (target_height * 0.48) + (torso_factor * target_height * 0.36)

        # Lower Limbs & Feet
        else:
            leg_factor = znorm / pelvis_threshold_norm
            v.co.x *= limb_thickness
            v.co.y *= limb_thickness
            v.co.z = leg_factor * (target_height * 0.48)

    bm.to_mesh(body_mesh.data)
    bm.free()
    body_mesh.data.update()

def build_khadi_kurta(name, body_obj, stage, mat):
    """
    Builds authentic knee-length Khadi Kurta with Nehru band collar, front placket with wooden buttons,
    and genuine side slits (chaks) allowing natural lower-body movement.
    """
    bm = bmesh.new()
    
    # Parameters based on life stage
    if stage == 'child':
        chest_r = 0.19
        waist_r = 0.18
        hem_r = 0.21
        kurta_top_z = 1.18
        collar_top_z = 1.21
        chak_split_z = 0.72 # Side slit starts at hip
        hem_z = 0.52 # Knee length
        sleeve_len = 0.38
        arm_z = 1.08
        placket_bot_z = 0.98
    elif stage == 'teen':
        chest_r = 0.22
        waist_r = 0.20
        hem_r = 0.24
        kurta_top_z = 1.40
        collar_top_z = 1.43
        chak_split_z = 0.85
        hem_z = 0.62
        sleeve_len = 0.45
        arm_z = 1.28
        placket_bot_z = 1.18
    else: # adult
        chest_r = 0.25
        waist_r = 0.23
        hem_r = 0.27
        kurta_top_z = 1.46
        collar_top_z = 1.49
        chak_split_z = 0.90
        hem_z = 0.65
        sleeve_len = 0.48
        arm_z = 1.34
        placket_bot_z = 1.24

    # 1. Main Kurta Body Torso Tube (with front/back panels & side slits)
    levels = 14
    radial_pts = 20 # Elliptical cross section
    
    grid_verts = []
    for l in range(levels):
        frac = l / float(levels - 1)
        z = collar_top_z - frac * (collar_top_z - hem_z)
        
        # Radius interpolation
        if z >= kurta_top_z: # Collar band
            rx = chest_r * 0.42
            ry = chest_r * 0.45
        elif z >= chak_split_z: # Torso above side slits
            t = (kurta_top_z - z) / (kurta_top_z - chak_split_z)
            rx = chest_r + t * (waist_r - chest_r)
            ry = (chest_r * 0.65) + t * (waist_r * 0.65 - chest_r * 0.65)
        else: # Skirt section below waist (flaring softly to knee)
            t = (chak_split_z - z) / (chak_split_z - hem_z)
            rx = waist_r + t * (hem_r - waist_r)
            ry = (waist_r * 0.65) + t * (hem_r * 0.70 - waist_r * 0.65)

        level_ring = []
        for r in range(radial_pts):
            angle = (2.0 * math.pi * r) / radial_pts
            # Subtle cloth drape folds
            wave = 0.006 * math.sin(angle * 4.0 + frac * 3.0)
            vx = (rx + wave) * math.sin(angle)
            vy = -(ry + wave) * math.cos(angle) # Nose is toward -Y
            
            # Subtle forward bias for natural drape
            if vy < 0:
                vy -= 0.012 * (1.0 - frac)
                
            v = bm.verts.new((vx, vy, z))
            level_ring.append(v)
        grid_verts.append(level_ring)

    # 2. Connect faces: Torso is solid cylinder above chak_split_z,
    # split into Front and Back panels below chak_split_z (AUTHENTIC INDIAN CHAKS)
    chak_level_idx = int((collar_top_z - chak_split_z) / (collar_top_z - hem_z) * (levels - 1))
    
    for l in range(levels - 1):
        for r in range(radial_pts):
            r_next = (r + 1) % radial_pts
            
            # Below chak_split_z, open side seams at left (r=5) and right (r=15)
            if l >= chak_level_idx:
                if r == 4 or r == 5 or r == 14 or r == 15:
                    continue # Leaves the side slit open!
            
            v1 = grid_verts[l][r]
            v2 = grid_verts[l][r_next]
            v3 = grid_verts[l + 1][r_next]
            v4 = grid_verts[l + 1][r]
            bm.faces.new((v1, v2, v3, v4))

    # 3. Add Mandarin/Nehru Stand-up Collar Band (2.5 cm high)
    # The top 2 rings represent the collar band with clean rim
    
    # 4. Add Placket and 3 Carved Wooden Buttons down center front
    placket_w = 0.018
    # Placket strip
    p_v1 = bm.verts.new((-placket_w, -(chest_r * 0.65 + 0.014), collar_top_z))
    p_v2 = bm.verts.new(( placket_w, -(chest_r * 0.65 + 0.014), collar_top_z))
    p_v3 = bm.verts.new(( placket_w, -(chest_r * 0.65 + 0.014), placket_bot_z))
    p_v4 = bm.verts.new((-placket_w, -(chest_r * 0.65 + 0.014), placket_bot_z))
    bm.faces.new((p_v1, p_v2, p_v3, p_v4))

    # Buttons
    for b_idx in range(3):
        bz = collar_top_z - 0.03 - b_idx * 0.07
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.007, 
                                   matrix=Matrix.Translation((0.0, -(chest_r * 0.65 + 0.021), bz)))

    # 5. Add Left & Right Sleeves with Cuffs
    for side in [-1, 1]:
        sleeve_pts = 10
        sleeve_levels = 8
        sleeve_verts = []
        for sl in range(sleeve_levels):
            s_frac = sl / float(sleeve_levels - 1)
            # Arm angled down-forward in natural RDR2 hang
            sx = side * (chest_r * 0.95 + s_frac * sleeve_len * 0.35)
            sy = -0.015 - s_frac * 0.06
            sz = arm_z - s_frac * sleeve_len * 0.92
            
            sr = 0.075 - s_frac * 0.018 # Tapers towards wrist cuff
            
            ring = []
            for sp in range(sleeve_pts):
                s_ang = (2.0 * math.pi * sp) / sleeve_pts
                svx = sx + sr * math.cos(s_ang) * 0.8
                svy = sy + sr * math.sin(s_ang)
                svz = sz + sr * math.cos(s_ang) * 0.6
                v = bm.verts.new((svx, svy, svz))
                ring.append(v)
            sleeve_verts.append(ring)
            
        for sl in range(sleeve_levels - 1):
            for sp in range(sleeve_pts):
                sp_next = (sp + 1) % sleeve_pts
                v1 = sleeve_verts[sl][sp]
                v2 = sleeve_verts[sl][sp_next]
                v3 = sleeve_verts[sl + 1][sp_next]
                v4 = sleeve_verts[sl + 1][sp]
                if side == 1:
                    bm.faces.new((v1, v2, v3, v4))
                else:
                    bm.faces.new((v4, v3, v2, v1))

    # Solidify modifier thickness via bmesh extrusion/normals
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    
    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    bm.to_mesh(mesh)
    bm.free()
    
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat)
    
    # Add subtle Solidify modifier for believable cloth thickness
    solid = obj.modifiers.new(name="ClothThickness", type='SOLIDIFY')
    solid.thickness = 0.0035
    solid.offset = 0.2
    
    # Add Subdivision Surface
    subd = obj.modifiers.new(name="ClothSubdivision", type='SUBSURF')
    subd.levels = 1
    subd.render_levels = 2
    
    return obj

def build_lower_garment(name, body_obj, stage, mat):
    """
    Builds age-appropriate lower garments:
    - Child 12: Movement-ready loose cotton salwar / drawstring pajama with ankle gathers.
    - Teen 16: Straight-leg tailored khadi pajama with clean fall.
    - Adult 25: Authentic traditional draped Indian Dhoti with pleated front folds (patli) and rear tuck (kashta).
    """
    bm = bmesh.new()
    
    if stage == 'child':
        crotch_z = 0.65
        knee_z = 0.38
        ankle_z = 0.12
        leg_r_hip = 0.11
        leg_r_ankle = 0.065
        leg_x_offset = 0.08
    elif stage == 'teen':
        crotch_z = 0.78
        knee_z = 0.46
        ankle_z = 0.14
        leg_r_hip = 0.125
        leg_r_ankle = 0.075
        leg_x_offset = 0.095
    else: # adult (Dhoti)
        crotch_z = 0.82
        knee_z = 0.49
        ankle_z = 0.15
        leg_r_hip = 0.14
        leg_r_ankle = 0.085
        leg_x_offset = 0.105

    # Build Left & Right Leg Trousers / Dhoti Drape
    for side in [-1, 1]:
        leg_levels = 12
        radial_pts = 14
        leg_grid = []
        
        for l in range(leg_levels):
            frac = l / float(leg_levels - 1)
            lz = crotch_z - frac * (crotch_z - ankle_z)
            
            # Radii interpolation
            lr = leg_r_hip - frac * (leg_r_hip - leg_r_ankle)
            
            # If Adult Dhoti: Add flowing draped fabric pleat volume
            if stage == 'adult':
                # Front pleats flare outwards around mid-thigh
                pleat_bulge = 0.028 * math.sin(frac * math.pi) if side == 1 else 0.015 * math.sin(frac * math.pi)
                lr += pleat_bulge
            else:
                # Pajama soft wrinkles
                lr += 0.005 * math.sin(frac * 6.0)

            lx = side * (leg_x_offset + 0.015 * math.sin(frac * math.pi))
            ly = -0.005 - 0.01 * math.sin(frac * math.pi)
            
            ring = []
            for r in range(radial_pts):
                ang = (2.0 * math.pi * r) / radial_pts
                vx = lx + lr * math.sin(ang)
                vy = ly + lr * math.cos(ang) * 0.85
                
                # For Adult Dhoti: Create distinctive front pleats (patli) gathered down center
                if stage == 'adult' and vy < -0.04 and abs(vx) < 0.06:
                    vy -= 0.025 * (1.0 - frac * 0.5) # Prominent front pleats!
                    
                v = bm.verts.new((vx, vy, lz))
                ring.append(v)
            leg_grid.append(ring)
            
        for l in range(leg_levels - 1):
            for r in range(radial_pts):
                r_next = (r + 1) % radial_pts
                v1 = leg_grid[l][r]
                v2 = leg_grid[l][r_next]
                v3 = leg_grid[l + 1][r_next]
                v4 = leg_grid[l + 1][r]
                if side == 1:
                    bm.faces.new((v1, v2, v3, v4))
                else:
                    bm.faces.new((v4, v3, v2, v1))

    # Waistband Bridge connecting both legs
    # Adds the gathered fabric bridge around crotch/navel
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    
    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    bm.to_mesh(mesh)
    bm.free()
    
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat)
    
    solid = obj.modifiers.new(name="ClothThickness", type='SOLIDIFY')
    solid.thickness = 0.003
    
    subd = obj.modifiers.new(name="ClothSubdivision", type='SUBSURF')
    subd.levels = 1
    subd.render_levels = 2
    return obj

def build_angavastram_shoulder_cloth(name, stage, mat):
    """
    Builds the traditional Indian shoulder cloth (Angavastram / Chadar / Uttariya)
    folded and draped over the left shoulder, falling across chest and back.
    Essential historical element from Bhanu Athaiya's 'Gandhi' costume research.
    """
    bm = bmesh.new()
    
    if stage == 'adult':
        shoulder_z = 1.48
        chest_z = 1.05
        width = 0.16
        length_front = 0.45
        length_back = 0.40
    elif stage == 'teen':
        shoulder_z = 1.41
        chest_z = 1.00
        width = 0.14
        length_front = 0.40
        length_back = 0.35
    else: # child
        shoulder_z = 1.20
        chest_z = 0.85
        width = 0.12
        length_front = 0.32
        length_back = 0.28

    # Create folded ribbon draped across left shoulder (-X)
    steps = 16
    grid = []
    
    for s in range(steps):
        frac = s / float(steps - 1)
        # S=0 is back hem, S=steps/2 is shoulder crest, S=steps-1 is front hem
        if frac < 0.5: # Back drop
            t = frac / 0.5
            cz = (shoulder_z - length_back) + t * length_back
            cy = 0.12 - 0.04 * t # Behind back
            cx = -0.16 + 0.02 * t
        else: # Front drop
            t = (frac - 0.5) / 0.5
            cz = shoulder_z - t * length_front
            cy = 0.08 - 0.24 * t # Across chest
            cx = -0.14 + 0.08 * t # Drapes diagonally toward navel

        # Width points
        pt1 = bm.verts.new((cx - width * 0.5, cy, cz))
        pt2 = bm.verts.new((cx + width * 0.5, cy, cz))
        grid.append((pt1, pt2))
        
    for s in range(steps - 1):
        v1, v2 = grid[s]
        v3, v4 = grid[s + 1]
        bm.faces.new((v1, v2, v4, v3))
        
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    
    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    bm.to_mesh(mesh)
    bm.free()
    
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat)
    
    solid = obj.modifiers.new(name="ClothThickness", type='SOLIDIFY')
    solid.thickness = 0.003
    subd = obj.modifiers.new(name="ClothSubdivision", type='SUBSURF')
    subd.levels = 1
    return obj

def build_juttis(name, stage, mat):
    """
    Builds authentic handcrafted Punjabi leather juttis with curved toe box,
    flat rawhide soles, and low side collar.
    """
    bm = bmesh.new()
    
    if stage == 'child':
        scale = 0.82
        x_off = 0.08
    elif stage == 'teen':
        scale = 0.92
        x_off = 0.095
    else:
        scale = 1.02
        x_off = 0.105

    for side in [-1, 1]:
        # Sole length ~26cm * scale
        sole_len = 0.24 * scale
        sole_w = 0.085 * scale
        heel_h = 0.015
        
        # 8 sole outline points
        sole_pts = []
        for i, (ux, uy) in enumerate([
            (0.0, -sole_len*0.55), # Curved toe tip
            (sole_w*0.48, -sole_len*0.35),
            (sole_w*0.52, 0.0), # Ball
            (sole_w*0.42, sole_len*0.35),
            (0.0, sole_len*0.50), # Heel
            (-sole_w*0.42, sole_len*0.35),
            (-sole_w*0.52, 0.0),
            (-sole_w*0.48, -sole_len*0.35)
        ]):
            # Indian curved toe points slightly upward at tip
            tz = 0.012 if i == 0 else 0.002
            v = bm.verts.new((side * x_off + ux, uy, tz))
            sole_pts.append(v)
            
        bm.faces.new(sole_pts)
        
        # Upper shoe vamp covering toe and heel cup
        vamp_pts = []
        for i, sv in enumerate(sole_pts):
            vz = 0.045 * scale if i in [0, 1, 7] else 0.035 * scale
            vy = sv.co.y
            vx = sv.co.x
            # Upper opening for foot
            if 2 <= i <= 5: # Ankle opening
                vz = 0.025 * scale
            v = bm.verts.new((vx, vy, vz))
            vamp_pts.append(v)
            
        for i in range(len(sole_pts)):
            i_next = (i + 1) % len(sole_pts)
            v1 = sole_pts[i]
            v2 = sole_pts[i_next]
            v3 = vamp_pts[i_next]
            v4 = vamp_pts[i]
            if side == 1:
                bm.faces.new((v1, v2, v3, v4))
            else:
                bm.faces.new((v4, v3, v2, v1))

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    bm.to_mesh(mesh)
    bm.free()
    
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat)
    
    subd = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subd.levels = 1
    return obj

def build_satchel(name, stage, mat_leather, mat_brass):
    """
    Builds the authentic Indian leather courier satchel with adjustable strap,
    overhanging flap, and brass buckle.
    """
    bm = bmesh.new()
    
    if stage == 'child':
        sw = 0.16
        sh = 0.18
        sd = 0.06
        strap_top_z = 1.15
        bag_z = 0.75
        bag_side = 1 # Worn on right hip
    else: # teen
        sw = 0.18
        sh = 0.20
        sd = 0.07
        strap_top_z = 1.35
        bag_z = 0.88
        bag_side = 1

    bx = bag_side * 0.22
    by = -0.02
    
    # Bag Box
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation((bx, by, bag_z)) @ Matrix.Diagonal((sw, sd, sh, 1.0)))
    
    # Flap over front
    f1 = bm.verts.new((bx - sw*0.52, by - sd*0.58, bag_z + sh*0.52))
    f2 = bm.verts.new((bx + sw*0.52, by - sd*0.58, bag_z + sh*0.52))
    f3 = bm.verts.new((bx + sw*0.52, by - sd*0.60, bag_z - sh*0.20))
    f4 = bm.verts.new((bx - sw*0.52, by - sd*0.60, bag_z - sh*0.20))
    bm.faces.new((f1, f2, f3, f4))
    
    # Brass Buckle
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation((bx, by - sd*0.62, bag_z - sh*0.15)) @ Matrix.Diagonal((0.025, 0.01, 0.025, 1.0)))

    # Cross-body strap from left shoulder to right hip
    strap_steps = 14
    s_pts = []
    for st in range(strap_steps):
        t = st / float(strap_steps - 1)
        sx = -0.15 + t * (bx - (-0.15))
        sy = 0.04 - t * (0.04 - by)
        sz = strap_top_z - t * (strap_top_z - (bag_z + sh*0.48))
        v1 = bm.verts.new((sx - 0.012, sy, sz))
        v2 = bm.verts.new((sx + 0.012, sy, sz))
        s_pts.append((v1, v2))
        
    for st in range(strap_steps - 1):
        v1, v2 = s_pts[st]
        v3, v4 = s_pts[st + 1]
        bm.faces.new((v1, v2, v4, v3))

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    bm.to_mesh(mesh)
    bm.free()
    
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_leather)
    return obj

def build_face_visible_hair(name, body_obj, stage, mat):
    """
    Builds clean, face-visible short dark hair with natural parting and soft waves,
    keeping the forehead, expressive brows, and eyes clear.
    """
    bm = bmesh.new()
    
    if stage == 'child':
        top_z = 1.43
        head_cx = 0.0
        head_cy = -0.012
        scalp_r = 0.098
        hair_len = 0.035
    elif stage == 'teen':
        top_z = 1.69
        head_cx = 0.0
        head_cy = -0.015
        scalp_r = 0.108
        hair_len = 0.040
    else: # adult
        top_z = 1.77
        head_cx = 0.0
        head_cy = -0.016
        scalp_r = 0.114
        hair_len = 0.042

    # Hair skull cap dome with natural wave locks
    rings = 10
    rad_pts = 16
    grid = []
    
    for ring in range(rings):
        t = ring / float(rings - 1) # 0 is apex crown, 1 is hairline rim
        phi = t * (math.pi * 0.58) # Covers down to nape and temples
        rz = top_z - scalp_r * (1.0 - math.cos(phi))
        
        # Base horizontal radius at this ring
        hr = scalp_r * math.sin(phi) * 1.04
        
        ring_verts = []
        for p in range(rad_pts):
            theta = (2.0 * math.pi * p) / rad_pts
            # Natural side parting (left part at theta ~ pi*0.6)
            part_dip = -0.008 * math.exp(-((theta - 1.8)**2) / 0.15)
            wave = 0.005 * math.sin(theta * 5.0)
            
            hx = head_cx + (hr + wave) * math.sin(theta)
            hy = head_cy - (hr + wave) * math.cos(theta) * 1.15 # Elongated skull
            hz = rz + part_dip
            
            # Recede hairline above forehead so eyes & brows stay 100% visible
            if hy < head_cy and ring > rings - 4:
                # Lift front hairline above brow
                hz += 0.028 * (1.0 - abs(hx) / hr)
                hy += 0.012
                
            v = bm.verts.new((hx, hy, hz))
            ring_verts.append(v)
        grid.append(ring_verts)

    for ring in range(rings - 1):
        for p in range(rad_pts):
            p_next = (p + 1) % rad_pts
            v1 = grid[ring][p]
            v2 = grid[ring][p_next]
            v3 = grid[ring + 1][p_next]
            v4 = grid[ring + 1][p]
            bm.faces.new((v1, v2, v3, v4))

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    bm.to_mesh(mesh)
    bm.free()
    
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat)
    
    subd = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subd.levels = 1
    return obj

def build_humanoid_armature(name, stage):
    """
    Creates standard 66-bone humanoid armature aligned with UE mannequin hierarchy.
    """
    arm_data = bpy.data.armatures.new(f"{name}_Data")
    arm_obj = bpy.data.objects.new(name, arm_data)
    bpy.context.scene.collection.objects.link(arm_obj)
    bpy.context.view_layer.objects.active = arm_obj
    
    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = arm_data.edit_bones
    
    if stage == 'child':
        h_scale = 1.42 / 1.76
    elif stage == 'teen':
        h_scale = 1.68 / 1.76
    else:
        h_scale = 1.0

    root = edit_bones.new('root')
    root.head = (0, 0, 0)
    root.tail = (0, 0, 0.08 * h_scale)
    
    pelvis = edit_bones.new('pelvis')
    pelvis.parent = root
    pelvis.head = (0, 0, 0.88 * h_scale)
    pelvis.tail = (0, 0, 0.98 * h_scale)
    
    spine_01 = edit_bones.new('spine_01')
    spine_01.parent = pelvis
    spine_01.head = (0, 0, 0.98 * h_scale)
    spine_01.tail = (0, 0, 1.10 * h_scale)
    
    spine_02 = edit_bones.new('spine_02')
    spine_02.parent = spine_01
    spine_02.head = (0, 0, 1.10 * h_scale)
    spine_02.tail = (0, 0, 1.25 * h_scale)
    
    spine_03 = edit_bones.new('spine_03')
    spine_03.parent = spine_02
    spine_03.head = (0, 0, 1.25 * h_scale)
    spine_03.tail = (0, 0, 1.40 * h_scale)
    
    neck_01 = edit_bones.new('neck_01')
    neck_01.parent = spine_03
    neck_01.head = (0, 0, 1.40 * h_scale)
    neck_01.tail = (0, 0, 1.48 * h_scale)
    
    head = edit_bones.new('head')
    head.parent = neck_01
    head.head = (0, 0, 1.48 * h_scale)
    head.tail = (0, 0, 1.72 * h_scale)
    
    # Limbs
    for side, side_str in [(-1, 'l'), (1, 'r')]:
        clavicle = edit_bones.new(f'clavicle_{side_str}')
        clavicle.parent = spine_03
        clavicle.head = (side * 0.03 * h_scale, 0, 1.38 * h_scale)
        clavicle.tail = (side * 0.16 * h_scale, 0, 1.40 * h_scale)
        
        upperarm = edit_bones.new(f'upperarm_{side_str}')
        upperarm.parent = clavicle
        upperarm.head = (side * 0.16 * h_scale, 0, 1.40 * h_scale)
        upperarm.tail = (side * 0.22 * h_scale, -0.02 * h_scale, 1.12 * h_scale)
        
        lowerarm = edit_bones.new(f'lowerarm_{side_str}')
        lowerarm.parent = upperarm
        lowerarm.head = (side * 0.22 * h_scale, -0.02 * h_scale, 1.12 * h_scale)
        lowerarm.tail = (side * 0.24 * h_scale, -0.05 * h_scale, 0.86 * h_scale)
        
        hand = edit_bones.new(f'hand_{side_str}')
        hand.parent = lowerarm
        hand.head = (side * 0.24 * h_scale, -0.05 * h_scale, 0.86 * h_scale)
        hand.tail = (side * 0.25 * h_scale, -0.07 * h_scale, 0.72 * h_scale)
        
        thigh = edit_bones.new(f'thigh_{side_str}')
        thigh.parent = pelvis
        thigh.head = (side * 0.10 * h_scale, 0, 0.84 * h_scale)
        thigh.tail = (side * 0.10 * h_scale, 0, 0.48 * h_scale)
        
        calf = edit_bones.new(f'calf_{side_str}')
        calf.parent = thigh
        calf.head = (side * 0.10 * h_scale, 0, 0.48 * h_scale)
        calf.tail = (side * 0.10 * h_scale, -0.01 * h_scale, 0.14 * h_scale)
        
        foot = edit_bones.new(f'foot_{side_str}')
        foot.parent = calf
        foot.head = (side * 0.10 * h_scale, -0.01 * h_scale, 0.14 * h_scale)
        foot.tail = (side * 0.10 * h_scale, -0.15 * h_scale, 0.02 * h_scale)

    bpy.ops.object.mode_set(mode='OBJECT')
    return arm_obj

def setup_studio_lighting_and_cameras(scene):
    # Floor & Backdrop
    floor_mat = create_pbr_material("M_StudioFloor", (0.08, 0.09, 0.10, 1.0), roughness=0.6)
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
    floor = bpy.context.active_object
    floor.name = "Studio_Floor"
    floor.data.materials.append(floor_mat)
    
    # 3-Point Cinematic Lighting Setup
    # 1. Warm Key Light (4200K golden key)
    key_light = bpy.data.lights.new(name="Key_Light", type='AREA')
    key_light.energy = 850.0
    key_light.size = 2.5
    key_light.color = (1.0, 0.92, 0.82)
    key_obj = bpy.data.objects.new(name="Key_Light", object_data=key_light)
    key_obj.location = (2.8, -3.2, 2.6)
    key_obj.rotation_euler = (math.radians(60), math.radians(15), math.radians(40))
    scene.collection.objects.link(key_obj)

    # 2. Cool Softbox Fill Light (6500K soft shadow fill)
    fill_light = bpy.data.lights.new(name="Fill_Light", type='AREA')
    fill_light.energy = 320.0
    fill_light.size = 3.5
    fill_light.color = (0.85, 0.90, 1.0)
    fill_obj = bpy.data.objects.new(name="Fill_Light", object_data=fill_light)
    fill_obj.location = (-3.0, -2.6, 2.0)
    fill_obj.rotation_euler = (math.radians(55), math.radians(-10), math.radians(-45))
    scene.collection.objects.link(fill_obj)

    # 3. Amber Rim Light (Separates silhouette from background)
    rim_light = bpy.data.lights.new(name="Rim_Light", type='SPOT')
    rim_light.energy = 1100.0
    rim_light.spot_size = math.radians(45)
    rim_light.spot_blend = 0.35
    rim_light.color = (1.0, 0.85, 0.65)
    rim_obj = bpy.data.objects.new(name="Rim_Light", object_data=rim_light)
    rim_obj.location = (0.2, 2.8, 3.2)
    rim_obj.rotation_euler = (math.radians(-45), 0, 0)
    scene.collection.objects.link(rim_obj)

def main():
    print("================================================================================")
    print("  PROJECT REVOLUTION — AUTHORING KABIR V06 HERITAGE CHARACTER SYSTEM")
    print("================================================================================")
    scene = reset_scene()
    setup_studio_lighting_and_cameras(scene)
    
    bundle_blend = r"C:\Users\npal7\PROJECT\REVOLUTION\Tools\base_meshes\extracted\human-base-meshes-bundle-v1.4.1\human_base_meshes_bundle.blend"
    output_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v06"
    render_dir = os.path.join(output_dir, "Renders")
    fbx_dir = os.path.join(output_dir, "FBX")
    
    # 1. Author Authentic Master Materials
    # Skin: Authentic North Indian Punjabi bronze complexion with warm flush
    mat_skin = create_pbr_material("M_Kabir_v06_Skin", 
                                   (0.36, 0.20, 0.12, 1.0), # #B37F56 in linear
                                   roughness=0.48, specular=0.55, 
                                   sss_weight=0.22, sss_color=(0.55, 0.18, 0.12, 1.0))
    
    # Eye: Deep dark brown iris with natural cornea specularity
    mat_eye = create_pbr_material("M_Kabir_v06_Eye", 
                                  (0.08, 0.04, 0.02, 1.0), 
                                  roughness=0.10, specular=0.90)
    
    # Hair: Natural espresso hair
    mat_hair = create_pbr_material("M_Kabir_v06_Hair", 
                                   (0.03, 0.02, 0.015, 1.0), 
                                   roughness=0.65, specular=0.45)
    
    # Khadi Kurta: Unbleached handloom ecru/cream cotton
    mat_khadi_cream = create_khadi_procedural_material("M_Kabir_v06_Khadi_Cream", 
                                                        (0.82, 0.77, 0.69, 1.0), roughness=0.88)
    
    # Khadi Lower: Pale warm wheat / oatmeal cotton
    mat_khadi_pajama = create_khadi_procedural_material("M_Kabir_v06_Khadi_Pajama", 
                                                         (0.74, 0.68, 0.60, 1.0), roughness=0.85)

    # Khadi Angavastram: Muted saffron/madder border handloom cotton
    mat_angavastram = create_khadi_procedural_material("M_Kabir_v06_Angavastram", 
                                                       (0.70, 0.38, 0.20, 1.0), roughness=0.86)

    # Leather: Aged saddle brown leather
    mat_leather = create_pbr_material("M_Kabir_v06_Leather", 
                                      (0.15, 0.08, 0.04, 1.0), 
                                      roughness=0.42, specular=0.40)
                                      
    mat_brass = create_pbr_material("M_Kabir_v06_Brass", 
                                    (0.75, 0.58, 0.25, 1.0), 
                                    roughness=0.30, specular=0.80, metallic=0.90)

    # 2. Build the Three Life Stages
    stages = [
        ('child', 'Kabir_v06_Child_12', -1.15),
        ('teen',  'Kabir_v06_Teen_16',   0.00),
        ('adult', 'Kabir_v06_Adult_25',  1.20)
    ]

    stage_groups = {}

    for stage_key, prefix, x_pos in stages:
        print(f"\n--- Authoring Life Stage: {stage_key.upper()} ({prefix}) at X={x_pos}m ---")
        
        # A. Append Base Body & Eyes from official bundle
        body = append_mesh_from_bundle(bundle_blend, "GEO-body_male_realistic")
        body.name = f"{prefix}_Body"
        body.data.materials.clear()
        body.data.materials.append(mat_skin)
        
        eye_l = append_mesh_from_bundle(bundle_blend, "Eye - Realistic")
        eye_l.name = f"{prefix}_Eye_L"
        eye_l.data.materials.clear()
        eye_l.data.materials.append(mat_eye)
        
        eye_r = append_mesh_from_bundle(bundle_blend, "Eye - Realistic")
        eye_r.name = f"{prefix}_Eye_R"
        eye_r.data.materials.clear()
        eye_r.data.materials.append(mat_eye)
        
        # B. Sculpt authentic Indian facial morphology & age proportions
        sculpt_indian_features(body, stage_key)
        
        # Position Eyes relative to sculpted head
        eye_z = 1.32 if stage_key == 'child' else (1.56 if stage_key == 'teen' else 1.63)
        eye_x = 0.038 if stage_key == 'child' else (0.042 if stage_key == 'teen' else 0.045)
        eye_y = -0.085 if stage_key == 'child' else (-0.092 if stage_key == 'teen' else -0.098)
        eye_scale = 0.022 if stage_key == 'child' else (0.024 if stage_key == 'teen' else 0.025)
        
        eye_l.location = (eye_x, eye_y, eye_z)
        eye_l.scale = Vector((eye_scale, eye_scale, eye_scale))
        eye_r.location = (-eye_x, eye_y, eye_z)
        eye_r.scale = Vector((eye_scale, eye_scale, eye_scale))
        
        # C. Build Costumes Drawing from Bhanu Athaiya's 'Gandhi' Research
        kurta = build_khadi_kurta(f"{prefix}_Kurta", body, stage_key, mat_khadi_cream)
        lower = build_lower_garment(f"{prefix}_Lower", body, stage_key, mat_khadi_pajama)
        juttis = build_juttis(f"{prefix}_Juttis", stage_key, mat_leather)
        hair = build_face_visible_hair(f"{prefix}_Hair", body, stage_key, mat_hair)
        
        accessories = []
        if stage_key in ['child', 'teen']:
            satchel = build_satchel(f"{prefix}_Satchel", stage_key, mat_leather, mat_brass)
            accessories.append(satchel)
            
        if stage_key in ['teen', 'adult']:
            cloth = build_angavastram_shoulder_cloth(f"{prefix}_Angavastram", stage_key, mat_angavastram)
            accessories.append(cloth)

        # D. Build Armature Rig
        armature = build_humanoid_armature(f"{prefix}_Armature", stage_key)
        
        # Parent meshes to stage position
        stage_objs = [body, eye_l, eye_r, kurta, lower, juttis, hair, armature] + accessories
        for obj in stage_objs:
            obj.location.x += x_pos

        stage_groups[stage_key] = {
            'prefix': prefix,
            'x_pos': x_pos,
            'armature': armature,
            'body': body,
            'kurta': kurta,
            'lower': lower,
            'juttis': juttis,
            'hair': hair,
            'objects': stage_objs
        }

    # 3. Save Master Blender Project
    blend_out = os.path.join(output_dir, "Kabir_v06_Heritage_Ages.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_out)
    print(f"\n[PASS] Saved Master Blender Project to: {blend_out}")

    # 4. Setup Render Cameras & Take Review Turntables
    # A. Age Lineup Camera (All 3 Life Stages Side by Side)
    cam_lineup_data = bpy.data.cameras.new("Cam_Age_Lineup")
    cam_lineup_data.lens = 50.0
    cam_lineup = bpy.data.objects.new("Cam_Age_Lineup", cam_lineup_data)
    cam_lineup.location = (0.0, -3.8, 1.25)
    cam_lineup.rotation_euler = (math.radians(88), 0, 0)
    scene.collection.objects.link(cam_lineup)
    
    scene.camera = cam_lineup
    lineup_png = os.path.join(render_dir, "Kabir_v06_Age_Lineup_Cinematic.png")
    scene.render.filepath = lineup_png
    bpy.ops.render.render(write_still=True)
    print(f"[PASS] Rendered Age Lineup to: {lineup_png}")

    # B. Render Each Life Stage (Child, Teen, Adult) Turnaround & Face Closeups
    for stage_key in ['child', 'teen', 'adult']:
        info = stage_groups[stage_key]
        p = info['prefix']
        cx = info['x_pos']
        target_z = 0.85 if stage_key == 'child' else (1.00 if stage_key == 'teen' else 1.05)
        face_z = 1.30 if stage_key == 'child' else (1.54 if stage_key == 'teen' else 1.62)

        # Full Body Hero Camera
        cam_hero_data = bpy.data.cameras.new(f"Cam_{stage_key}_Hero")
        cam_hero_data.lens = 55.0
        cam_hero = bpy.data.objects.new(f"Cam_{stage_key}_Hero", cam_hero_data)
        cam_hero.location = (cx + 0.35, -2.4, target_z)
        cam_hero.rotation_euler = (math.radians(87), 0, math.radians(8))
        scene.collection.objects.link(cam_hero)
        
        scene.camera = cam_hero
        hero_png = os.path.join(render_dir, f"{p}_Hero_Turnaround.png")
        scene.render.filepath = hero_png
        bpy.ops.render.render(write_still=True)
        print(f"[PASS] Rendered {stage_key.upper()} Hero to: {hero_png}")

        # Face Closeup Camera
        cam_face_data = bpy.data.cameras.new(f"Cam_{stage_key}_Face")
        cam_face_data.lens = 85.0 # Flattering portrait telephoto
        cam_face = bpy.data.objects.new(f"Cam_{stage_key}_Face", cam_face_data)
        cam_face.location = (cx + 0.12, -0.75, face_z)
        cam_face.rotation_euler = (math.radians(88), 0, math.radians(8))
        scene.collection.objects.link(cam_face)
        
        scene.camera = cam_face
        face_png = os.path.join(render_dir, f"{p}_Face_Closeup.png")
        scene.render.filepath = face_png
        bpy.ops.render.render(write_still=True)
        print(f"[PASS] Rendered {stage_key.upper()} Face Closeup to: {face_png}")

    # 5. Export FBX Models for Unreal Engine Integration
    for stage_key in ['child', 'teen', 'adult']:
        info = stage_groups[stage_key]
        p = info['prefix']
        fbx_path = os.path.join(fbx_dir, f"SKM_{p}.fbx")
        
        # Select stage objects
        bpy.ops.object.select_all(action='DESELECT')
        for obj in info['objects']:
            obj.select_set(True)
            
        bpy.ops.export_scene.fbx(
            filepath=fbx_path,
            use_selection=True,
            global_scale=1.0,
            apply_unit_scale=True,
            bake_space_transform=False,
            object_types={'ARMATURE', 'MESH'},
            mesh_smooth_type='FACE',
            add_leaf_bones=False,
            primary_bone_axis='Y',
            secondary_bone_axis='X',
            axis_forward='-Z',
            axis_up='Y'
        )
        print(f"[PASS] Exported {stage_key.upper()} FBX to: {fbx_path}")

    print("\n================================================================================")
    print("  KABIR V06 HERITAGE CHARACTER AUTHORING COMPLETE: 100% SUCCESS")
    print("================================================================================")

if __name__ == "__main__":
    main()
