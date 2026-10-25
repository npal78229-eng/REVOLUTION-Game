"""
PROJECT REVOLUTION — Fix Kabir v05 UV Unwrapping & Re-export FBX
Ensures clean, properly unwrapped UVs for all meshes (Body, Kurta, Shorts, Hair, Sandals, Satchel, Eyes)
in the [0.01, 0.99] UV space so PBR textures map accurately without stretching or border clipping.
"""

import bpy
import math
import os

def main():
    blend_path = r"C:\Users\npal7\Documents\Blender\Kabir_v05\Kabir_v05.blend"
    bpy.ops.wm.open_mainfile(filepath=blend_path)
    
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
        
    mesh_names = [
        "v05_Kabir_Body",
        "v05_Kabir_Kurta",
        "v05_Kabir_Shorts",
        "v05_Kabir_Hair",
        "v05_Kabir_Sandals",
        "v05_Kabir_Satchel",
        "v05_Kabir_Eye_L",
        "v05_Kabir_Eye_R"
    ]
    
    mesh_objects = []
    for name in mesh_names:
        obj = bpy.data.objects.get(name)
        if not obj:
            print(f"Warning: {name} not found!")
            continue
        mesh_objects.append(obj)
        
        # Ensure active UV layer
        if not obj.data.uv_layers:
            obj.data.uv_layers.new(name="UVMap")
        obj.data.uv_layers.active = obj.data.uv_layers[0]
        
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=math.radians(66.0), island_margin=0.02)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        uvs = obj.data.uv_layers.active.data
        xs = [d.uv.x for d in uvs]
        ys = [d.uv.y for d in uvs]
        print(f"  {name} clean UV: X=[{min(xs):.4f}, {max(xs):.4f}], Y=[{min(ys):.4f}, {max(ys):.4f}]")
        
    # Armature
    arm_obj = bpy.data.objects.get("v05_Kabir_Armature")
    assert arm_obj, "v05_Kabir_Armature not found!"
    
    # Save main file
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    art_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Character\Kabir_v05"
    art_blend = os.path.join(art_dir, "Kabir_v05.blend")
    bpy.ops.wm.save_as_mainfile(filepath=art_blend)
    print("Saved master blend files.")
    
    # Export Skeletal Mesh FBX
    fbx_path = os.path.join(art_dir, "SKM_Kabir_v05.fbx")
    bpy.ops.object.select_all(action='DESELECT')
    arm_obj.select_set(True)
    for o in mesh_objects:
        o.select_set(True)
    bpy.context.view_layer.objects.active = arm_obj
    
    bpy.ops.export_scene.fbx(
        filepath=fbx_path,
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
    print(f"Exported clean SKM_Kabir_v05.fbx to {fbx_path} ({os.path.getsize(fbx_path)} bytes).")

if __name__ == "__main__":
    main()
