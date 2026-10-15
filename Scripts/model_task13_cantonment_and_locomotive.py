"""
PROJECT REVOLUTION — Task 13 3D Asset Modeling (Blender 5.2 LTS)
Layer 4 & 5 Climax: The Colonial Civil Lines & Steam Locomotive Depot

Assets Created:
1. SM_Locomotive_Engine_PunjabMail (British 4-6-0 broad-gauge steam engine with boiler, cab, driving wheels, cowcatcher)
2. SM_Civil_Lines_Clubhouse_Bungalow (Colonial administrative bungalow with deep Doric veranda, hipped iron roof, sash windows)
3. SM_Cantonment_Guardhouse_Picket (Fortified brick sentry post with rifle embrasures, sandbags, and flagpole)
4. SM_Prop_Cantonment_Archive_Cabinet (Colonial teak archive cabinet with pigeonhole slots, curfew dispatches, brass pulls)

Exports to:
- C:/Users/npal7/PROJECT/REVOLUTION/Art/Exports/
- C:/Users/npal7/PROJECT/REVOLUTION/Art/PROJECT/
- C:/Users/npal7/PROJECT/PROJECT/
"""

import bpy
import bmesh
import math
import os
import shutil
from mathutils import Vector, Matrix

EXPORT_DIRS = [
    "C:/Users/npal7/PROJECT/REVOLUTION/Art/Exports",
    "C:/Users/npal7/PROJECT/REVOLUTION/Art/PROJECT",
    "C:/Users/npal7/PROJECT/PROJECT"
]
for d in EXPORT_DIRS:
    os.makedirs(d, exist_ok=True)

def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if not bpy.data.scenes:
        bpy.data.scenes.new("Scene")

def create_pbr_material(name, base_color, roughness=0.6, metallic=0.0):
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
    return mat

def export_active_asset(asset_name):
    # Select all mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj

    # Save Blend file
    blend_path = os.path.join("C:/Users/npal7/PROJECT/REVOLUTION/Art/PROJECT", f"{asset_name}.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"[BLENDER] Saved: {blend_path}")

    # Export FBX to all target directories
    for d in EXPORT_DIRS:
        fbx_path = os.path.join(d, f"{asset_name}.fbx")
        bpy.ops.export_scene.fbx(
            filepath=fbx_path,
            use_selection=False,
            global_scale=1.0,
            apply_unit_scale=True,
            apply_scale_options='FBX_SCALE_ALL',
            axis_forward='-Z',
            axis_up='Y',
            bake_space_transform=True,
            object_types={'MESH'},
            mesh_smooth_type='FACE'
        )
        print(f"[BLENDER] Exported FBX: {fbx_path} ({os.path.getsize(fbx_path)} bytes)")

# ===========================================================================
# 1. SM_Locomotive_Engine_PunjabMail
# ===========================================================================
def build_steam_locomotive():
    reset_scene()
    print("[TASK 13] Building SM_Locomotive_Engine_PunjabMail...")

    mat_black_steel = create_pbr_material("M_Loco_BlackSteel", (0.08, 0.08, 0.09, 1.0), roughness=0.38, metallic=0.88)
    mat_brass = create_pbr_material("M_Loco_Brass", (0.85, 0.70, 0.28, 1.0), roughness=0.28, metallic=0.92)
    mat_dark_iron = create_pbr_material("M_Loco_DarkIron", (0.12, 0.12, 0.13, 1.0), roughness=0.65, metallic=0.75)
    mat_wood_cab = create_pbr_material("M_Loco_TeakCab", (0.28, 0.16, 0.08, 1.0), roughness=0.72)
    mat_lamp_glass = create_pbr_material("M_Loco_Glass", (0.92, 0.95, 0.98, 1.0), roughness=0.10)

    # Chassis frame (10.5m long, 2.4m wide, 0.5m thick, elevated at Z = 1.05m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 1.05))
    chassis = bpy.context.active_object
    chassis.name = "Loco_Chassis"
    chassis.scale = (2.4, 10.5, 0.45)
    bpy.ops.object.transform_apply(scale=True)
    chassis.data.materials.append(mat_dark_iron)

    # Front buffer beam & cowcatcher plow (+Y is front)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 5.35, 0.85))
    buffer_beam = bpy.context.active_object
    buffer_beam.scale = (2.6, 0.25, 0.5)
    bpy.ops.object.transform_apply(scale=True)
    buffer_beam.data.materials.append(mat_black_steel)

    # Round buffer disks
    for side in [-0.95, 0.95]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=0.35, location=(side, 5.55, 0.95))
        buf = bpy.context.active_object
        buf.rotation_euler = (math.radians(90), 0, 0)
        bpy.ops.object.transform_apply(rotation=True)
        buf.data.materials.append(mat_dark_iron)

    # Cylindrical boiler (D = 1.7m, length = 6.2m, centered around Y = 1.2m, Z = 2.15m)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.85, depth=6.2, location=(0.0, 1.2, 2.15))
    boiler = bpy.context.active_object
    boiler.name = "Loco_Boiler"
    boiler.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(rotation=True)
    boiler.data.materials.append(mat_black_steel)

    # Brass boiler cladding bands
    for by in [-1.5, -0.5, 0.5, 1.5, 2.5, 3.5]:
        bpy.ops.mesh.primitive_torus_add(major_radius=0.86, minor_radius=0.035, location=(0.0, by, 2.15))
        band = bpy.context.active_object
        band.rotation_euler = (math.radians(90), 0, 0)
        bpy.ops.object.transform_apply(rotation=True)
        band.data.materials.append(mat_brass)

    # Smokebox front door & hinge
    bpy.ops.mesh.primitive_cylinder_add(radius=0.84, depth=0.25, location=(0.0, 4.35, 2.15))
    smokebox_door = bpy.context.active_object
    smokebox_door.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(rotation=True)
    smokebox_door.data.materials.append(mat_dark_iron)

    # Smokestack (chimney, Z = 3.0m to 4.2m)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.26, depth=1.1, location=(0.0, 3.8, 3.55))
    stack = bpy.context.active_object
    stack.data.materials.append(mat_black_steel)

    # Chimney copper rim
    bpy.ops.mesh.primitive_torus_add(major_radius=0.28, minor_radius=0.04, location=(0.0, 3.8, 4.1))
    rim = bpy.context.active_object
    rim.data.materials.append(mat_brass)

    # Steam Dome & Sandbox Dome
    for dy in [2.2, 0.2]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.42, location=(0.0, dy, 3.1))
        dome = bpy.context.active_object
        dome.scale = (0.85, 0.85, 1.25)
        bpy.ops.object.transform_apply(scale=True)
        dome.data.materials.append(mat_brass)

    # Driver's Cab (Y = -2.0m to -4.6m, Z = 1.2m to 3.8m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -3.2, 2.5))
    cab = bpy.context.active_object
    cab.scale = (2.55, 2.6, 2.4)
    bpy.ops.object.transform_apply(scale=True)
    cab.data.materials.append(mat_wood_cab)

    # Cab curved roof
    bpy.ops.mesh.primitive_cylinder_add(radius=1.35, depth=2.8, location=(0.0, -3.2, 3.7))
    cab_roof = bpy.context.active_object
    cab_roof.rotation_euler = (math.radians(90), 0, 0)
    cab_roof.scale = (1.0, 0.35, 1.0)
    bpy.ops.object.transform_apply(rotation=True, scale=True)
    cab_roof.data.materials.append(mat_black_steel)

    # Front Headlamp Lantern (Z = 3.2m, Y = 4.45m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 4.45, 3.2))
    lamp = bpy.context.active_object
    lamp.scale = (0.45, 0.45, 0.55)
    bpy.ops.object.transform_apply(scale=True)
    lamp.data.materials.append(mat_brass)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.1, location=(0.0, 4.70, 3.2))
    lens = bpy.context.active_object
    lens.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(rotation=True)
    lens.data.materials.append(mat_lamp_glass)

    # 6 Large Spoked Driving Wheels (Radius = 0.85m, Z = 0.85m)
    driving_y = [0.8, -0.9, -2.5]
    for side in [-1.22, 1.22]:
        for wy in driving_y:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.85, depth=0.16, location=(side, wy, 0.85))
            wheel = bpy.context.active_object
            wheel.rotation_euler = (0, math.radians(90), 0)
            bpy.ops.object.transform_apply(rotation=True)
            wheel.data.materials.append(mat_dark_iron)

            # Central hub
            bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=0.22, location=(side + (0.04 if side > 0 else -0.04), wy, 0.85))
            hub = bpy.context.active_object
            hub.rotation_euler = (0, math.radians(90), 0)
            bpy.ops.object.transform_apply(rotation=True)
            hub.data.materials.append(mat_brass)

    # 4 Front Bogie Wheels (Radius = 0.45m, Z = 0.45m)
    bogie_y = [2.9, 4.3]
    for side in [-1.15, 1.15]:
        for wy in bogie_y:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.45, depth=0.14, location=(side, wy, 0.45))
            b_wheel = bpy.context.active_object
            b_wheel.rotation_euler = (0, math.radians(90), 0)
            bpy.ops.object.transform_apply(rotation=True)
            b_wheel.data.materials.append(mat_dark_iron)

    # Coupling Side Rods connecting driving wheels
    for side in [-1.34, 1.34]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side, -0.85, 0.65))
        rod = bpy.context.active_object
        rod.scale = (0.06, 3.5, 0.12)
        bpy.ops.object.transform_apply(scale=True)
        rod.data.materials.append(mat_dark_iron)

    export_active_asset("SM_Locomotive_Engine_PunjabMail")

# ===========================================================================
# 2. SM_Civil_Lines_Clubhouse_Bungalow
# ===========================================================================
def build_clubhouse_bungalow():
    reset_scene()
    print("[TASK 13] Building SM_Civil_Lines_Clubhouse_Bungalow...")

    mat_plinth_stone = create_pbr_material("M_Colonial_PlinthStone", (0.55, 0.52, 0.48, 1.0), roughness=0.82)
    mat_white_brick = create_pbr_material("M_Colonial_WhitewashBrick", (0.90, 0.88, 0.84, 1.0), roughness=0.75)
    mat_corrugated_roof = create_pbr_material("M_Colonial_CorrugatedZinc", (0.35, 0.38, 0.42, 1.0), roughness=0.45, metallic=0.72)
    mat_teak_trim = create_pbr_material("M_Colonial_TeakDark", (0.24, 0.15, 0.08, 1.0), roughness=0.68)
    mat_glass = create_pbr_material("M_Colonial_GlassSash", (0.85, 0.90, 0.92, 1.0), roughness=0.08)

    # 1. Raised Stone Plinth (14.0m wide X, 9.0m deep Y, 0.6m high Z)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.3))
    plinth = bpy.context.active_object
    plinth.name = "Bungalow_Plinth"
    plinth.scale = (14.0, 9.0, 0.6)
    bpy.ops.object.transform_apply(scale=True)
    plinth.data.materials.append(mat_plinth_stone)

    # Front Entrance Steps (3.6m wide, 1.4m projection, 3 steps)
    for i in range(3):
        step_z = 0.15 * (i + 1)
        step_y = -4.5 - (0.4 * (3 - i))
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, step_y, step_z * 0.5))
        st = bpy.context.active_object
        st.scale = (3.6, 0.4, step_z)
        bpy.ops.object.transform_apply(scale=True)
        st.data.materials.append(mat_plinth_stone)

    # 2. Main Enclosed Building (13.2m wide, 5.8m deep, shifted towards +Y so front veranda is open)
    # Veranda occupies Y = -4.2 to -1.8 (2.4m deep veranda floor)
    # Main building sits Y = -1.8 to 4.2 (6.0m deep, Z = 0.6 to 4.4, height 3.8m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 1.2, 2.5))
    main_body = bpy.context.active_object
    main_body.name = "Bungalow_MainHall"
    main_body.scale = (13.2, 6.0, 3.8)
    bpy.ops.object.transform_apply(scale=True)
    main_body.data.materials.append(mat_white_brick)

    # 3. Veranda Classical Tuscan Columns (6 columns along Y = -4.1, Z = 0.6 to 3.8)
    col_x_positions = [-6.0, -3.6, -1.2, 1.2, 3.6, 6.0]
    for cx in col_x_positions:
        # Square column base
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, -4.1, 0.8))
        cb = bpy.context.active_object
        cb.scale = (0.55, 0.55, 0.4)
        bpy.ops.object.transform_apply(scale=True)
        cb.data.materials.append(mat_plinth_stone)

        # Cylindrical shaft
        bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=2.8, location=(cx, -4.1, 2.4))
        cs = bpy.context.active_object
        cs.data.materials.append(mat_white_brick)

        # Capital
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, -4.1, 3.9))
        cc = bpy.context.active_object
        cc.scale = (0.58, 0.58, 0.25)
        bpy.ops.object.transform_apply(scale=True)
        cc.data.materials.append(mat_plinth_stone)

    # Veranda Entablature / Architrave beam (spans X = -6.4 to 6.4, Y = -4.1, Z = 4.05)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -4.1, 4.05))
    beam = bpy.context.active_object
    beam.scale = (13.6, 0.55, 0.35)
    bpy.ops.object.transform_apply(scale=True)
    beam.data.materials.append(mat_white_brick)

    # 4. Veranda Low Decorative Timber Balustrade between outer columns
    balustrade_spans = [(-6.0, -3.6), (-3.6, -1.2), (1.2, 3.6), (3.6, 6.0)]
    for x1, x2 in balustrade_spans:
        mid_x = (x1 + x2) * 0.5
        span_len = abs(x2 - x1) - 0.55
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(mid_x, -4.1, 1.15))
        bal = bpy.context.active_object
        bal.scale = (span_len, 0.14, 0.7)
        bpy.ops.object.transform_apply(scale=True)
        bal.data.materials.append(mat_teak_trim)

    # 5. Grand Double Entrance Doorway (X = 0.0, Y = -1.82, Z = 0.6 to 3.2)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -1.82, 1.9))
    door_frame = bpy.context.active_object
    door_frame.scale = (2.2, 0.15, 2.6)
    bpy.ops.object.transform_apply(scale=True)
    door_frame.data.materials.append(mat_teak_trim)

    # Semicircular fanlight transom over door
    bpy.ops.mesh.primitive_cylinder_add(radius=0.95, depth=0.12, location=(0.0, -1.82, 3.2))
    fanlight = bpy.context.active_object
    fanlight.rotation_euler = (math.radians(90), 0, 0)
    fanlight.scale = (1.0, 0.5, 1.0)
    bpy.ops.object.transform_apply(rotation=True, scale=True)
    fanlight.data.materials.append(mat_glass)

    # 6. Colonial Sash Windows with Shutter Louvers
    win_x_positions = [-4.6, -2.4, 2.4, 4.6]
    for wx in win_x_positions:
        # Window frame & glass
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(wx, -1.82, 2.2))
        win = bpy.context.active_object
        win.scale = (1.2, 0.12, 1.8)
        bpy.ops.object.transform_apply(scale=True)
        win.data.materials.append(mat_glass)

        # Louver shutter panels on sides
        for s_side in [-0.75, 0.75]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(wx + s_side, -1.84, 2.2))
            shutter = bpy.context.active_object
            shutter.scale = (0.35, 0.08, 1.75)
            bpy.ops.object.transform_apply(scale=True)
            shutter.data.materials.append(mat_teak_trim)

    # 7. Sloped Corrugated Zinc Hipped Roof (Z = 4.4 to 6.2)
    # Base overhang (14.6m X, 9.8m Y)
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=8.6, radius2=2.4, depth=1.8, location=(0.0, 0.0, 5.3))
    roof = bpy.context.active_object
    roof.name = "Bungalow_Roof"
    roof.rotation_euler = (0, 0, math.radians(45))
    roof.scale = (1.20, 0.78, 1.0)
    bpy.ops.object.transform_apply(rotation=True, scale=True)
    roof.data.materials.append(mat_corrugated_roof)

    # Roof ridge cap
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 6.25))
    ridge = bpy.context.active_object
    ridge.scale = (4.8, 0.4, 0.25)
    bpy.ops.object.transform_apply(scale=True)
    ridge.data.materials.append(mat_corrugated_roof)

    export_active_asset("SM_Civil_Lines_Clubhouse_Bungalow")

# ===========================================================================
# 3. SM_Cantonment_Guardhouse_Picket
# ===========================================================================
def build_guardhouse_picket():
    reset_scene()
    print("[TASK 13] Building SM_Cantonment_Guardhouse_Picket...")

    mat_whitewash = create_pbr_material("M_Picket_Whitewash", (0.88, 0.86, 0.82, 1.0), roughness=0.78)
    mat_sandbag = create_pbr_material("M_Picket_BurlapSandbag", (0.58, 0.50, 0.38, 1.0), roughness=0.92)
    mat_corrugated_tin = create_pbr_material("M_Picket_TinRoof", (0.38, 0.40, 0.42, 1.0), roughness=0.48, metallic=0.68)
    mat_teak = create_pbr_material("M_Picket_Teak", (0.24, 0.14, 0.07, 1.0), roughness=0.75)
    mat_iron = create_pbr_material("M_Picket_GalvIron", (0.32, 0.34, 0.36, 1.0), roughness=0.35, metallic=0.85)

    # 1. Whitewashed Brick Guardhouse Structure (3.6m wide, 3.0m deep, 3.2m tall)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 1.6))
    gh = bpy.context.active_object
    gh.name = "Picket_Guardhouse"
    gh.scale = (3.6, 3.0, 3.2)
    bpy.ops.object.transform_apply(scale=True)
    gh.data.materials.append(mat_whitewash)

    # Rifle firing embrasures (narrow horizontal slits on front and flanks)
    for ey in [-1.51, 1.51]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, ey, 1.85))
        embr = bpy.context.active_object
        embr.scale = (1.4, 0.12, 0.22)
        bpy.ops.object.transform_apply(scale=True)
        embr.data.materials.append(mat_iron)

    # Front Entrance Doorway (X = 0.8, Y = -1.52, Z = 0 to 2.2)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.8, -1.52, 1.1))
    door = bpy.context.active_object
    door.scale = (1.0, 0.14, 2.2)
    bpy.ops.object.transform_apply(scale=True)
    door.data.materials.append(mat_teak)

    # Iron inspection viewport grille
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.8, -1.53, 1.55))
    view_slit = bpy.context.active_object
    view_slit.scale = (0.3, 0.16, 0.2)
    bpy.ops.object.transform_apply(scale=True)
    view_slit.data.materials.append(mat_iron)

    # 2. Sloped Corrugated Tin Shed Roof (4.2m wide, 3.6m deep, angled slope)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -0.1, 3.45))
    roof = bpy.context.active_object
    roof.scale = (4.2, 3.6, 0.15)
    roof.rotation_euler = (math.radians(8.0), 0, 0)
    bpy.ops.object.transform_apply(rotation=True, scale=True)
    roof.data.materials.append(mat_corrugated_tin)

    # 3. Curved Sandbag Defensive Revetment (Wrapping the left front flank)
    # Tier 1 (Z = 0.15)
    bag_coords = [
        (-1.8, -1.8, 0.15), (-1.2, -1.8, 0.15), (-0.6, -1.8, 0.15),
        (-2.2, -1.3, 0.15), (-2.2, -0.7, 0.15), (-2.2, -0.1, 0.15)
    ]
    for bx, by, bz in bag_coords:
        # Tier 1
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, by, bz))
        b1 = bpy.context.active_object
        b1.scale = (0.55, 0.32, 0.26)
        bpy.ops.object.transform_apply(scale=True)
        b1.data.materials.append(mat_sandbag)

        # Tier 2 (offset)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx + 0.05, by + 0.05, bz + 0.25))
        b2 = bpy.context.active_object
        b2.scale = (0.55, 0.32, 0.26)
        bpy.ops.object.transform_apply(scale=True)
        b2.data.materials.append(mat_sandbag)

        # Tier 3
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, by, bz + 0.50))
        b3 = bpy.context.active_object
        b3.scale = (0.55, 0.32, 0.26)
        bpy.ops.object.transform_apply(scale=True)
        b3.data.materials.append(mat_sandbag)

    # 4. Galvanized Iron Flagpole (6.2m tall, beside guardhouse at X = 2.4, Y = -1.2)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.065, depth=6.2, location=(2.4, -1.2, 3.1))
    pole = bpy.context.active_object
    pole.data.materials.append(mat_iron)

    # Flagpole gold ball finial
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.14, location=(2.4, -1.2, 6.25))
    finial = bpy.context.active_object
    finial.data.materials.append(mat_iron)

    # Flagpole square concrete pedestal base
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(2.4, -1.2, 0.25))
    base = bpy.context.active_object
    base.scale = (0.6, 0.6, 0.5)
    bpy.ops.object.transform_apply(scale=True)
    base.data.materials.append(mat_whitewash)

    export_active_asset("SM_Cantonment_Guardhouse_Picket")

# ===========================================================================
# 4. SM_Prop_Cantonment_Archive_Cabinet
# ===========================================================================
def build_archive_cabinet():
    reset_scene()
    print("[TASK 13] Building SM_Prop_Cantonment_Archive_Cabinet...")

    mat_teak = create_pbr_material("M_Cabinet_Teak", (0.28, 0.16, 0.09, 1.0), roughness=0.55)
    mat_brass = create_pbr_material("M_Cabinet_Brass", (0.85, 0.72, 0.30, 1.0), roughness=0.30, metallic=0.92)
    mat_wire_mesh = create_pbr_material("M_Cabinet_BronzeMesh", (0.42, 0.36, 0.24, 1.0), roughness=0.65, metallic=0.60)
    mat_parchment = create_pbr_material("M_Cabinet_ParchmentPaper", (0.88, 0.84, 0.74, 1.0), roughness=0.85)

    # 1. Main Cabinet Frame (1.4m wide, 0.55m deep, 2.1m tall)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 1.05))
    frame = bpy.context.active_object
    frame.name = "Archive_Frame"
    frame.scale = (1.4, 0.55, 2.1)
    bpy.ops.object.transform_apply(scale=True)
    frame.data.materials.append(mat_teak)

    # Cornice Top Rim
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 2.15))
    cornice = bpy.context.active_object
    cornice.scale = (1.48, 0.62, 0.12)
    bpy.ops.object.transform_apply(scale=True)
    cornice.data.materials.append(mat_teak)

    # Plinth Base with turned bracket feet
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.08))
    plinth = bpy.context.active_object
    plinth.scale = (1.44, 0.58, 0.16)
    bpy.ops.object.transform_apply(scale=True)
    plinth.data.materials.append(mat_teak)

    # 2. Upper Shelves (Z = 0.85 to 2.05m)
    # Recessed shelf cavity (Y = -0.28 to +0.25)
    for sz in [1.15, 1.45, 1.75]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -0.02, sz))
        shelf = bpy.context.active_object
        shelf.scale = (1.28, 0.48, 0.04)
        bpy.ops.object.transform_apply(scale=True)
        shelf.data.materials.append(mat_teak)

    # 3. Stacked Document Dockets & Curfew Dispatches on Shelves
    docket_positions = [
        (-0.45, -0.05, 1.25), (-0.15, -0.05, 1.25), (0.25, -0.05, 1.25),
        (-0.35, -0.05, 1.55), (0.15, -0.05, 1.55), (0.42, -0.05, 1.55),
        (-0.25, -0.05, 1.85), (0.20, -0.05, 1.85)
    ]
    for dx, dy, dz in docket_positions:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(dx, dy, dz))
        docket = bpy.context.active_object
        docket.scale = (0.26, 0.36, 0.14)
        bpy.ops.object.transform_apply(scale=True)
        docket.data.materials.append(mat_parchment)

    # Rolled telegram / map scroll tubes
    for sx, sz in [(-0.52, 1.88), (-0.48, 1.88), (0.50, 1.88)]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.38, location=(sx, -0.05, sz))
        scroll = bpy.context.active_object
        scroll.rotation_euler = (math.radians(90), 0, 0)
        bpy.ops.object.transform_apply(rotation=True)
        scroll.data.materials.append(mat_parchment)

    # 4. Lower Filing Drawers (4 drawers: 2 rows of 2)
    drawer_coords = [
        (-0.34, -0.26, 0.62), (0.34, -0.26, 0.62),
        (-0.34, -0.26, 0.32), (0.34, -0.26, 0.32)
    ]
    for drx, dry, drz in drawer_coords:
        # Drawer face
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(drx, dry, drz))
        dr = bpy.context.active_object
        dr.scale = (0.58, 0.05, 0.25)
        bpy.ops.object.transform_apply(scale=True)
        dr.data.materials.append(mat_teak)

        # Brass cup handle pull
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(drx, dry - 0.04, drz))
        pull = bpy.context.active_object
        pull.scale = (0.14, 0.03, 0.06)
        bpy.ops.object.transform_apply(scale=True)
        pull.data.materials.append(mat_brass)

    # 5. Upper Dual Door Frames with Wire Grille Inserts
    for side in [-0.34, 0.34]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side, -0.27, 1.48))
        d_frame = bpy.context.active_object
        d_frame.scale = (0.62, 0.04, 1.18)
        bpy.ops.object.transform_apply(scale=True)
        d_frame.data.materials.append(mat_teak)

        # Wire mesh inset
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side, -0.275, 1.48))
        mesh_panel = bpy.context.active_object
        mesh_panel.scale = (0.50, 0.01, 1.04)
        bpy.ops.object.transform_apply(scale=True)
        mesh_panel.data.materials.append(mat_wire_mesh)

        # Brass keyhole escutcheon
        bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=0.03, location=(side + (-0.22 if side < 0 else 0.22), -0.29, 1.48))
        keyhole = bpy.context.active_object
        keyhole.rotation_euler = (math.radians(90), 0, 0)
        bpy.ops.object.transform_apply(rotation=True)
        keyhole.data.materials.append(mat_brass)

    export_active_asset("SM_Prop_Cantonment_Archive_Cabinet")

def main():
    print("================ PROJECT REVOLUTION TASK 13 3D ASSET GENERATOR ================")
    build_steam_locomotive()
    build_clubhouse_bungalow()
    build_guardhouse_picket()
    build_archive_cabinet()
    print("================ ALL TASK 13 ASSETS BUILT & EXPORTED TO ALL DIRECTORIES ================")

if __name__ == "__main__":
    main()
