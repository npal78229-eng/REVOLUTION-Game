"""
Build Kabir v05 Sculpt & Base Body in Blender 5.2 (Revision 3 - Mesh Extraction Pipeline)
Uses standard AAA character workflow:
- Body with child proportions (144 cm, 1:5.8 head ratio)
- Properly seated realistic eyes
- Kurta and Shorts extracted directly from body geometry with normal offset (no boxy cylinders or floating geometry)
- Scalp-extracted hair cap with clean bangs (no facial clipping)
- Realistic lighting and studio renders
"""

import bpy
import bmesh
import math
import os
from mathutils import Vector, Matrix

def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if not bpy.data.scenes:
        bpy.data.scenes.new("Scene")
    scene = bpy.context.scene
    if not bpy.data.collections:
        col = bpy.data.collections.new("Collection")
        scene.collection.children.link(col)

def append_objects(blend_path, object_names):
    loaded = []
    with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
        data_to.objects = [name for name in object_names if name in data_from.objects]
    
    for obj in data_to.objects:
        bpy.context.scene.collection.objects.link(obj)
        loaded.append(obj)
    return loaded

def apply_child_proportions_and_sculpt(body_obj, eye_l, eye_r):
    for obj in [body_obj, eye_l, eye_r]:
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        obj.select_set(False)

    mesh = body_obj.data
    verts = mesh.vertices
    
    min_z = min(v.co.z for v in verts)
    max_z = max(v.co.z for v in verts)
    orig_height = max_z - min_z
    
    min_x = min(v.co.x for v in verts)
    max_x = max(v.co.x for v in verts)
    mid_x = (min_x + max_x) / 2.0
    min_y = min(v.co.y for v in verts)
    max_y = max(v.co.y for v in verts)
    mid_y = (min_y + max_y) / 2.0
    
    for v in verts:
        v.co.x -= mid_x
        v.co.y -= mid_y
        v.co.z -= min_z
        
    for eye in [eye_l, eye_r]:
        for ev in eye.data.vertices:
            ev.co.x -= mid_x
            ev.co.y -= mid_y
            ev.co.z -= min_z

    head_bottom_norm = 1.45 / orig_height
    pelvis_norm = 0.88 / orig_height
    knee_norm = 0.48 / orig_height
    
    target_height = 1.440
    target_head_height = 0.245
    target_chin_z = target_height - target_head_height
    target_pelvis_z = 0.720
    target_knee_z = 0.380
    
    def transform_coord(x, y, z):
        znorm = z / orig_height
        if znorm >= head_bottom_norm:
            hf = (znorm - head_bottom_norm) / (1.0 - head_bottom_norm)
            nz = target_chin_z + hf * target_head_height
            
            wf = 1.05
            df = 1.03
            if hf < 0.4:
                wf = 1.04
                df = 1.02
            elif hf > 0.7:
                wf = 1.07
                df = 1.05
                
            nx = x * wf
            ny = y * df
            
            if y < 0 and 0.22 < hf < 0.60:
                if abs(x) < 0.025 and 0.32 < hf < 0.50:
                    ny -= 0.003
                elif abs(x) < 0.035 and 0.22 < hf < 0.32:
                    ny -= 0.002
            return nx, ny, nz
            
        elif znorm >= pelvis_norm:
            tf = (znorm - pelvis_norm) / (head_bottom_norm - pelvis_norm)
            nz = target_pelvis_z + tf * (target_chin_z - target_pelvis_z)
            shoulder_factor = 0.76 + 0.06 * tf
            depth_factor = 0.78 + 0.05 * tf
            return x * shoulder_factor, y * depth_factor, nz
            
        elif znorm >= knee_norm:
            thf = (znorm - knee_norm) / (pelvis_norm - knee_norm)
            nz = target_knee_z + thf * (target_pelvis_z - target_knee_z)
            return x * 0.82, y * 0.82, nz
        else:
            lf = znorm / knee_norm
            nz = lf * target_knee_z
            return x * 0.85, y * 0.85, nz

    for v in verts:
        v.co.x, v.co.y, v.co.z = transform_coord(v.co.x, v.co.y, v.co.z)
        
    for eye in [eye_l, eye_r]:
        for ev in eye.data.vertices:
            ev.co.x, ev.co.y, ev.co.z = transform_coord(ev.co.x, ev.co.y, ev.co.z)
        eye.data.update()

    mesh.update()
    
    min_final_z = min(v.co.z for v in verts)
    for v in verts:
        v.co.z -= min_final_z
    for eye in [eye_l, eye_r]:
        for ev in eye.data.vertices:
            ev.co.z -= min_final_z
        eye.data.update()
        
    actual_h = max(v.co.z for v in verts)
    scale_corr = target_height / actual_h
    for v in verts:
        v.co.x *= scale_corr
        v.co.y *= scale_corr
        v.co.z *= scale_corr
    for eye in [eye_l, eye_r]:
        for ev in eye.data.vertices:
            ev.co.x *= scale_corr
            ev.co.y *= scale_corr
            ev.co.z *= scale_corr
        eye.data.update()
        
    mesh.update()
    
    body_obj.name = "v05_Kabir_Body"
    body_obj.data.name = "v05_Kabir_Body_Mesh"
    eye_l.name = "v05_Kabir_Eye_L"
    eye_r.name = "v05_Kabir_Eye_R"

def extract_mesh_shell(source_obj, name, face_filter_fn, offset=0.006):
    """Duplicates body geometry based on face filter and offsets along normal."""
    src_mesh = source_obj.data
    bm_src = bmesh.new()
    bm_src.from_mesh(src_mesh)
    bm_src.faces.ensure_lookup_table()
    
    bm_new = bmesh.new()
    
    # Map old verts to new verts
    vert_map = {}
    for f in bm_src.faces:
        if face_filter_fn(f):
            new_verts = []
            for v in f.verts:
                if v not in vert_map:
                    # Offset slightly along normal
                    norm = v.normal.normalized() if v.normal.length > 0 else Vector((0,0,1))
                    nco = v.co + norm * offset
                    nv = bm_new.verts.new(nco)
                    vert_map[v] = nv
                new_verts.append(vert_map[v])
            bm_new.faces.new(new_verts)
            
    bm_src.free()
    
    new_mesh = bpy.data.meshes.new(name + "_Mesh")
    bm_new.to_mesh(new_mesh)
    bm_new.free()
    new_mesh.update()
    
    new_obj = bpy.data.objects.new(name, new_mesh)
    bpy.context.scene.collection.objects.link(new_obj)
    
    for poly in new_mesh.polygons:
        poly.use_smooth = True
        
    return new_obj

def build_extracted_kurta(body_obj):
    """Extracts kurta upper body from torso and upper arms, then adds natural drape."""
    def kurta_filter(face):
        z = face.calc_center_median().z
        x = abs(face.calc_center_median().x)
        # Torso: neck down to pelvis (0.70 <= z <= 1.18)
        if 0.70 <= z <= 1.18 and x <= 0.18:
            return True
        # Upper arms / sleeves (down to mid-forearm z >= 0.82)
        if 0.82 <= z <= 1.18 and x > 0.15:
            return True
        return False
        
    kurta_obj = extract_mesh_shell(body_obj, "v05_Kabir_Kurta", kurta_filter, offset=0.008)
    
    # Now extend the bottom hem of the kurta downwards to mid-thigh (Z ~ 0.54)
    # to form the classic loose khadi tunic drape
    bm = bmesh.new()
    bm.from_mesh(kurta_obj.data)
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    
    # Find boundary edges near bottom (Z ~ 0.70) on the torso
    bottom_edges = [e for e in bm.edges if e.is_boundary and all(v.co.z < 0.74 and abs(v.co.x) < 0.18 for v in e.verts)]
    
    if bottom_edges:
        # Extrude downwards in 3 gentle tiers
        for step in range(3):
            t = (step + 1) / 3.0
            target_z = 0.70 - t * 0.16 # down to 0.54
            flare = 1.0 + 0.08 * t
            
            res = bmesh.ops.extrude_edge_only(bm, edges=bottom_edges)
            new_verts = [v for v in res['geom'] if isinstance(v, bmesh.types.BMVert)]
            for v in new_verts:
                v.co.z = target_z
                v.co.x *= flare
                v.co.y *= flare
            bottom_edges = [e for e in res['geom'] if isinstance(e, bmesh.types.BMEdge) and e.is_boundary]
            
    bm.to_mesh(kurta_obj.data)
    bm.free()
    kurta_obj.data.update()
    
    sol = kurta_obj.modifiers.new("Solidify", 'SOLIDIFY')
    sol.thickness = 0.002
    return kurta_obj

def build_extracted_shorts(body_obj):
    """Extracts shorts directly from pelvis and thighs down to above knees."""
    def shorts_filter(face):
        z = face.calc_center_median().z
        x = abs(face.calc_center_median().x)
        # Pelvis & thighs (0.44 <= z <= 0.74, and not feet/calves)
        if 0.44 <= z <= 0.74 and x < 0.18:
            return True
        return False
        
    shorts_obj = extract_mesh_shell(body_obj, "v05_Kabir_Shorts", shorts_filter, offset=0.006)
    sol = shorts_obj.modifiers.new("Solidify", 'SOLIDIFY')
    sol.thickness = 0.002
    return shorts_obj

def build_extracted_hair(body_obj):
    """Extracts scalp and upper cranium faces, offsets outwards to form natural hair mass."""
    def scalp_filter(face):
        cen = face.calc_center_median()
        z = cen.z
        y = cen.y
        # Scalp is top of head (z >= 1.32) and cranium/sides
        # Exclude face front: where z < 1.36 and y < -0.04
        if z >= 1.31:
            if z < 1.36 and y < -0.045:
                return False # Forehead and eyes
            return True
        elif z >= 1.25 and y > 0.02: # Back of head down to nape
            return True
        return False
        
    hair_obj = extract_mesh_shell(body_obj, "v05_Kabir_Hair", scalp_filter, offset=0.012)
    
    # Add subtle organic noise to hair vertices to give tousled lock volume
    bm = bmesh.new()
    bm.from_mesh(hair_obj.data)
    for v in bm.verts:
        # Tousled texture
        wave = 0.004 * math.sin(v.co.x * 40.0 + v.co.z * 30.0)
        v.co += v.normal * wave
        # Bring slight fringe forward over forehead
        if v.co.z > 1.34 and v.co.y < -0.02:
            v.co.y -= 0.008
            v.co.z -= 0.004
            
    bm.to_mesh(hair_obj.data)
    bm.free()
    hair_obj.data.update()
    
    sol = hair_obj.modifiers.new("Solidify", 'SOLIDIFY')
    sol.thickness = 0.004
    return hair_obj

def build_sandals():
    verts_list = []
    faces_list = []
    
    for side in [-1, 1]:
        base_idx = len(verts_list)
        cx = side * 0.108
        num_sole = 14
        for z in [0.002, 0.012]:
            for i in range(num_sole):
                ang = 2.0 * math.pi * i / num_sole
                sx = cx + 0.038 * math.sin(ang)
                sy = 0.02 + 0.105 * math.cos(ang)
                verts_list.append((sx, sy, z))
                
        for i in range(num_sole):
            i_next = (i + 1) % num_sole
            v1 = base_idx + i
            v2 = base_idx + i_next
            v3 = base_idx + num_sole + i_next
            v4 = base_idx + num_sole + i
            faces_list.append((v1, v2, v3, v4))
            
        strap_base = len(verts_list)
        for u in range(5):
            ut = u / 4.0
            sy = -0.015 + ut * 0.045
            sz = 0.014 + 0.030 * math.sin(ut * math.pi)
            verts_list.append((cx - 0.036, sy, sz))
            verts_list.append((cx + 0.036, sy, sz))
            
        for u in range(4):
            v1 = strap_base + u * 2
            v2 = strap_base + u * 2 + 1
            v3 = strap_base + (u + 1) * 2 + 1
            v4 = strap_base + (u + 1) * 2
            faces_list.append((v1, v4, v3, v2))

    sandals_mesh = bpy.data.meshes.new("v05_Kabir_Sandals_Mesh")
    sandals_mesh.from_pydata(verts_list, [], faces_list)
    sandals_mesh.update()
    
    sandals_obj = bpy.data.objects.new("v05_Kabir_Sandals", sandals_mesh)
    bpy.context.scene.collection.objects.link(sandals_obj)
    for poly in sandals_mesh.polygons:
        poly.use_smooth = True
    return sandals_obj

def build_satchel():
    verts_list = []
    faces_list = []
    
    bx, by, bz = 0.16, 0.02, 0.62
    dx, dy, dz = 0.035, 0.11, 0.13
    
    b_verts = [
        (bx - dx, by - dy, bz - dz), (bx + dx, by - dy, bz - dz),
        (bx + dx, by + dy, bz - dz), (bx - dx, by + dy, bz - dz),
        (bx - dx, by - dy, bz + dz), (bx + dx, by - dy, bz + dz),
        (bx + dx, by + dy, bz + dz), (bx - dx, by + dy, bz + dz),
    ]
    verts_list.extend(b_verts)
    b_faces = [
        (0, 1, 2, 3), (4, 7, 6, 5),
        (0, 4, 5, 1), (1, 5, 6, 2),
        (2, 6, 7, 3), (3, 7, 4, 0)
    ]
    faces_list.extend(b_faces)
    
    strap_base = len(verts_list)
    strap_pts = 16
    for s in range(strap_pts):
        t = s / (strap_pts - 1)
        sx = -0.155 + t * 0.315
        sz = 1.18 - t * 0.44
        sy = 0.11 * math.sin(t * math.pi) - 0.02
        verts_list.append((sx, sy, sz - 0.012))
        verts_list.append((sx, sy, sz + 0.012))
        
    for s in range(strap_pts - 1):
        v1 = strap_base + s * 2
        v2 = strap_base + s * 2 + 1
        v3 = strap_base + (s + 1) * 2 + 1
        v4 = strap_base + (s + 1) * 2
        faces_list.append((v1, v2, v3, v4))

    satchel_mesh = bpy.data.meshes.new("v05_Kabir_Satchel_Mesh")
    satchel_mesh.from_pydata(verts_list, [], faces_list)
    satchel_mesh.update()
    
    satchel_obj = bpy.data.objects.new("v05_Kabir_Satchel", satchel_mesh)
    bpy.context.scene.collection.objects.link(satchel_obj)
    for poly in satchel_mesh.polygons:
        poly.use_smooth = True
    return satchel_obj

def assign_materials(body, eye_l, eye_r, kurta, shorts, sandals, satchel, hair):
    # Skin
    mat_skin = bpy.data.materials.new(name="M_Skin")
    bsdf = mat_skin.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.64, 0.46, 0.35, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.42
        if 'Subsurface Weight' in bsdf.inputs:
            bsdf.inputs['Subsurface Weight'].default_value = 0.18
        elif 'Subsurface' in bsdf.inputs:
            bsdf.inputs['Subsurface'].default_value = 0.18
    body.data.materials.append(mat_skin)
    
    # Eyes
    mat_eye = bpy.data.materials.new(name="M_Eye")
    bsdf_e = mat_eye.node_tree.nodes.get("Principled BSDF")
    if bsdf_e:
        bsdf_e.inputs['Base Color'].default_value = (0.15, 0.08, 0.04, 1.0)
        bsdf_e.inputs['Roughness'].default_value = 0.05
        bsdf_e.inputs['IOR'].default_value = 1.376
    eye_l.data.materials.append(mat_eye)
    eye_r.data.materials.append(mat_eye)
    
    # Khadi Kurta
    mat_kurta = bpy.data.materials.new(name="M_Kurta")
    bsdf_k = mat_kurta.node_tree.nodes.get("Principled BSDF")
    if bsdf_k:
        bsdf_k.inputs['Base Color'].default_value = (0.84, 0.81, 0.74, 1.0)
        bsdf_k.inputs['Roughness'].default_value = 0.82
    kurta.data.materials.append(mat_kurta)
    
    # Shorts
    mat_shorts = bpy.data.materials.new(name="M_Shorts")
    bsdf_s = mat_shorts.node_tree.nodes.get("Principled BSDF")
    if bsdf_s:
        bsdf_s.inputs['Base Color'].default_value = (0.75, 0.72, 0.66, 1.0)
        bsdf_s.inputs['Roughness'].default_value = 0.85
    shorts.data.materials.append(mat_shorts)
    
    # Sandals
    mat_sandals = bpy.data.materials.new(name="M_Sandals")
    bsdf_sd = mat_sandals.node_tree.nodes.get("Principled BSDF")
    if bsdf_sd:
        bsdf_sd.inputs['Base Color'].default_value = (0.28, 0.18, 0.12, 1.0)
        bsdf_sd.inputs['Roughness'].default_value = 0.60
    sandals.data.materials.append(mat_sandals)
    
    # Satchel
    mat_satchel = bpy.data.materials.new(name="M_Satchel")
    bsdf_st = mat_satchel.node_tree.nodes.get("Principled BSDF")
    if bsdf_st:
        bsdf_st.inputs['Base Color'].default_value = (0.34, 0.28, 0.20, 1.0)
        bsdf_st.inputs['Roughness'].default_value = 0.85
    satchel.data.materials.append(mat_satchel)
    
    # Hair
    mat_hair = bpy.data.materials.new(name="M_Hair")
    bsdf_h = mat_hair.node_tree.nodes.get("Principled BSDF")
    if bsdf_h:
        bsdf_h.inputs['Base Color'].default_value = (0.05, 0.04, 0.035, 1.0)
        bsdf_h.inputs['Roughness'].default_value = 0.50
    hair.data.materials.append(mat_hair)

def setup_studio():
    bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, 0))
    floor = bpy.context.active_object
    floor.name = "Studio_Floor"
    mat_fl = bpy.data.materials.new(name="M_StudioFloor")
    b_fl = mat_fl.node_tree.nodes.get("Principled BSDF")
    if b_fl:
        b_fl.inputs['Base Color'].default_value = (0.16, 0.17, 0.18, 1.0)
        b_fl.inputs['Roughness'].default_value = 0.90
    floor.data.materials.append(mat_fl)
    
    # Key light (3200K golden sunlight)
    key_d = bpy.data.lights.new(name="Key_Light", type='AREA')
    key_d.energy = 320.0
    key_d.size = 1.4
    key_d.color = (1.0, 0.89, 0.76)
    key_obj = bpy.data.objects.new("Key_Light", key_d)
    key_obj.location = (1.4, -2.2, 2.3)
    key_obj.rotation_euler = (math.radians(50), 0, math.radians(35))
    bpy.context.scene.collection.objects.link(key_obj)
    
    # Fill light
    fill_d = bpy.data.lights.new(name="Fill_Light", type='AREA')
    fill_d.energy = 110.0
    fill_d.size = 2.2
    fill_d.color = (0.76, 0.82, 0.95)
    fill_obj = bpy.data.objects.new("Fill_Light", fill_d)
    fill_obj.location = (-1.8, -1.6, 1.6)
    fill_obj.rotation_euler = (math.radians(40), 0, math.radians(-45))
    bpy.context.scene.collection.objects.link(fill_obj)
    
    # Rim light
    rim_d = bpy.data.lights.new(name="Rim_Light", type='AREA')
    rim_d.energy = 220.0
    rim_d.size = 1.6
    rim_d.color = (1.0, 0.96, 0.92)
    rim_obj = bpy.data.objects.new("Rim_Light", rim_d)
    rim_obj.location = (-0.9, 1.9, 2.1)
    rim_obj.rotation_euler = (math.radians(-50), 0, math.radians(160))
    bpy.context.scene.collection.objects.link(rim_obj)

def render_camera(cam_pos, cam_rot, out_path, lens_mm=45):
    scene = bpy.context.scene
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = out_path
    
    cam_data = bpy.data.cameras.new("Cam")
    cam_data.lens = lens_mm
    cam_obj = bpy.data.objects.new("Cam", cam_data)
    cam_obj.location = cam_pos
    cam_obj.rotation_euler = cam_rot
    scene.collection.objects.link(cam_obj)
    scene.camera = cam_obj
    
    bpy.ops.render.render(write_still=True)
    
    bpy.data.objects.remove(cam_obj, do_unlink=True)
    bpy.data.cameras.remove(cam_data)

def main():
    print("=== STARTING KABIR V05 (MESH EXTRACTION WORKFLOW) ===")
    reset_scene()
    
    bundle_blend = r"C:\Users\npal7\PROJECT\REVOLUTION\Tools\base_meshes\extracted\human-base-meshes-bundle-v1.4.1\human_base_meshes_bundle.blend"
    
    objs = append_objects(bundle_blend, [
        "GEO-body_male_realistic",
        "GEO-body_male_realistic.eye.L",
        "GEO-body_male_realistic.eye.R"
    ])
    
    body = next(o for o in objs if "body" in o.name)
    eye_l = next(o for o in objs if "eye.L" in o.name)
    eye_r = next(o for o in objs if "eye.R" in o.name)
    
    print("Applying child proportions & facial features...")
    apply_child_proportions_and_sculpt(body, eye_l, eye_r)
    
    print("Extracting fitted kurta, shorts, and hair directly from body topology...")
    kurta = build_extracted_kurta(body)
    shorts = build_extracted_shorts(body)
    hair = build_extracted_hair(body)
    sandals = build_sandals()
    satchel = build_satchel()
    
    print("Assigning materials...")
    assign_materials(body, eye_l, eye_r, kurta, shorts, sandals, satchel, hair)
    
    print("Setting up studio lighting and floor...")
    setup_studio()
    
    render_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v05\Renders"
    
    print("Rendering 4 photographic views...")
    # 1. Front Full Body
    render_camera(
        cam_pos=(0.0, -3.8, 0.72),
        cam_rot=(math.radians(90), 0, 0),
        out_path=os.path.join(render_dir, "v05_Render_Front.png"),
        lens_mm=45
    )
    
    # 2. Side Profile
    render_camera(
        cam_pos=(3.8, 0.0, 0.72),
        cam_rot=(math.radians(90), 0, math.radians(90)),
        out_path=os.path.join(render_dir, "v05_Render_Side.png"),
        lens_mm=45
    )
    
    # 3. Three-Quarter View
    render_camera(
        cam_pos=(2.4, -2.8, 0.95),
        cam_rot=(math.radians(82), 0, math.radians(40)),
        out_path=os.path.join(render_dir, "v05_Render_ThreeQuarter.png"),
        lens_mm=48
    )
    
    # 4. Close-Up Face Portrait
    render_camera(
        cam_pos=(0.0, -0.95, 1.31),
        cam_rot=(math.radians(90), 0, 0),
        out_path=os.path.join(render_dir, "v05_Render_Face_Closeup.png"),
        lens_mm=75
    )
    
    # Save blends
    blend_user_path = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend"
    blend_art_path = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v05\Kabir_v05.blend"
    
    print(f"Saving to {blend_user_path}...")
    bpy.ops.wm.save_as_mainfile(filepath=blend_user_path)
    
    print(f"Saving to {blend_art_path}...")
    bpy.ops.wm.save_as_mainfile(filepath=blend_art_path)
    
    all_objs = [body, eye_l, eye_r, kurta, shorts, sandals, satchel, hair]
    total_tris = sum(len(o.data.polygons) for o in all_objs) * 2
    body_bbox_z = [v.co.z for v in body.data.vertices]
    
    print("=== PIPELINE METRICS ===")
    print(f"Total Triangles: ~{total_tris} tris (Budget: 25k-35k)")
    print(f"Body Height: {max(body_bbox_z) - min(body_bbox_z):.4f} m (Target: 1.440 m)")
    print(f"Min Z: {min(body_bbox_z):.4f} m (Target: 0.000 m)")
    print("=== DONE ===")

if __name__ == "__main__":
    main()
