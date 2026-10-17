#!/usr/bin/env python
"""
PROJECT REVOLUTION — Photogrammetry Texture Ingestion & Master Material Setup
Automates:
1. Ingestion of 12 1024x1024 PBR texture maps into /Game/Environment/Mohalla/Textures/
2. Automatic compression & color space configuration (BC, Normal, ORM)
3. Construction of Master Material M_Master_Heritage_PBR
4. Generation and parameter wiring of 4 Material Instances:
   - MI_NanakshahiBrick_Photogrammetry
   - MI_CarvedShisham_Photogrammetry
   - MI_HammeredBrass_Photogrammetry
   - MI_WovenJute_Photogrammetry
5. Assignment of heritage materials to landmark environment static meshes
"""

import os
import unreal

def log(msg):
    unreal.log_warning(f"[PHOTOGRAMMETRY_PIPELINE] {msg}")

def main():
    log("================================================================================")
    log("INITIALIZING TASK 24: PHOTOGRAMMETRY INGESTION & MATERIAL SETUP")
    log("================================================================================")

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    src_tex_dir = os.path.join(project_root, "Art", "Textures")
    dest_tex_path = "/Game/Environment/Mohalla/Textures"
    dest_mat_path = "/Game/Environment/Mohalla/Materials"

    asset_subsystem = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    mel = unreal.MaterialEditingLibrary

    # -------------------------------------------------------------------------
    # 1. INGEST ALL 12 PBR TEXTURE MAPS
    # -------------------------------------------------------------------------
    material_names = ["T_NanakshahiBrick", "T_CarvedShisham", "T_HammeredBrass", "T_WovenJute"]
    suffixes = [("BC", False, False), ("N", True, False), ("ORM", False, True)]

    imported_textures = {}

    for mat_name in material_names:
        for suffix, is_norm, is_orm in suffixes:
            tex_asset_name = f"{mat_name}_{suffix}"
            src_file = os.path.join(src_tex_dir, f"{tex_asset_name}.png")

            if not os.path.isfile(src_file):
                log(f"ERROR: Source texture not found at {src_file}")
                continue

            task = unreal.AssetImportTask()
            task.set_editor_property('filename', src_file)
            task.set_editor_property('destination_path', dest_tex_path)
            task.set_editor_property('destination_name', tex_asset_name)
            task.set_editor_property('replace_existing', True)
            task.set_editor_property('automated', True)
            task.set_editor_property('save', True)

            asset_tools.import_asset_tasks([task])
            tex_obj = unreal.load_asset(f"{dest_tex_path}/{tex_asset_name}")

            if tex_obj:
                if is_norm:
                    tex_obj.set_editor_property('compression_settings', unreal.TextureCompressionSettings.TC_NORMALMAP)
                    tex_obj.set_editor_property('srgb', False)
                    tex_obj.set_editor_property('lod_group', unreal.TextureGroup.TEXTUREGROUP_WORLD_NORMAL_MAP)
                elif is_orm:
                    tex_obj.set_editor_property('compression_settings', unreal.TextureCompressionSettings.TC_MASKS)
                    tex_obj.set_editor_property('srgb', False)
                    tex_obj.set_editor_property('lod_group', unreal.TextureGroup.TEXTUREGROUP_WORLD)
                else:
                    tex_obj.set_editor_property('compression_settings', unreal.TextureCompressionSettings.TC_DEFAULT)
                    tex_obj.set_editor_property('srgb', True)
                    tex_obj.set_editor_property('lod_group', unreal.TextureGroup.TEXTUREGROUP_WORLD)

                asset_subsystem.save_loaded_asset(tex_obj)
                imported_textures[tex_asset_name] = tex_obj
                log(f"  -> Imported and configured: {tex_asset_name}")
            else:
                log(f"ERROR: Failed to load imported texture {tex_asset_name}")

    log(f"Successfully ingested {len(imported_textures)} / 12 photogrammetry textures.")

    # -------------------------------------------------------------------------
    # 2. BUILD MASTER HERITAGE MATERIAL (M_Master_Heritage_PBR)
    # -------------------------------------------------------------------------
    master_mat_name = "M_Master_Heritage_PBR"
    master_mat_path = f"{dest_mat_path}/{master_mat_name}"
    master_mat = unreal.load_asset(master_mat_path)

    if not master_mat:
        mat_factory = unreal.MaterialFactoryNew()
        master_mat = asset_tools.create_asset(master_mat_name, dest_mat_path, unreal.Material, mat_factory)
        log(f"Created new Master Material: {master_mat_name}")

    if master_mat:
        # BaseColor Parameter
        param_bc = mel.create_material_expression(master_mat, unreal.MaterialExpressionTextureSampleParameter2D, -550, -250)
        param_bc.set_editor_property("parameter_name", "BaseColorMap")
        if "T_NanakshahiBrick_BC" in imported_textures:
            param_bc.set_editor_property("texture", imported_textures["T_NanakshahiBrick_BC"])
        mel.connect_material_property(param_bc, "RGB", unreal.MaterialProperty.MP_BASE_COLOR)

        # Normal Parameter
        param_n = mel.create_material_expression(master_mat, unreal.MaterialExpressionTextureSampleParameter2D, -550, 50)
        param_n.set_editor_property("parameter_name", "NormalMap")
        param_n.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL)
        if "T_NanakshahiBrick_N" in imported_textures:
            param_n.set_editor_property("texture", imported_textures["T_NanakshahiBrick_N"])
        mel.connect_material_property(param_n, "RGB", unreal.MaterialProperty.MP_NORMAL)

        # ORM Parameter (Occlusion, Roughness, Metallic)
        param_orm = mel.create_material_expression(master_mat, unreal.MaterialExpressionTextureSampleParameter2D, -550, 350)
        param_orm.set_editor_property("parameter_name", "ORMMap")
        param_orm.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_MASKS)
        if "T_NanakshahiBrick_ORM" in imported_textures:
            param_orm.set_editor_property("texture", imported_textures["T_NanakshahiBrick_ORM"])
        mel.connect_material_property(param_orm, "R", unreal.MaterialProperty.MP_AMBIENT_OCCLUSION)
        mel.connect_material_property(param_orm, "G", unreal.MaterialProperty.MP_ROUGHNESS)
        mel.connect_material_property(param_orm, "B", unreal.MaterialProperty.MP_METALLIC)

        mel.recompile_material(master_mat)
        asset_subsystem.save_loaded_asset(master_mat)
        log("Master Material M_Master_Heritage_PBR recompiled and saved successfully.")

    # -------------------------------------------------------------------------
    # 3. BUILD 4 HERITAGE MATERIAL INSTANCES
    # -------------------------------------------------------------------------
    mi_configs = [
        ("MI_NanakshahiBrick_Photogrammetry", "T_NanakshahiBrick"),
        ("MI_CarvedShisham_Photogrammetry", "T_CarvedShisham"),
        ("MI_HammeredBrass_Photogrammetry", "T_HammeredBrass"),
        ("MI_WovenJute_Photogrammetry", "T_WovenJute")
    ]

    material_instances = {}

    for mi_name, prefix in mi_configs:
        mi_path = f"{dest_mat_path}/{mi_name}"
        mi_obj = unreal.load_asset(mi_path)

        if not mi_obj:
            mi_factory = unreal.MaterialInstanceConstantFactoryNew()
            mi_obj = asset_tools.create_asset(mi_name, dest_mat_path, unreal.MaterialInstanceConstant, mi_factory)
            log(f"Created Material Instance: {mi_name}")

        if mi_obj and master_mat:
            mel.set_material_instance_parent(mi_obj, master_mat)

            bc_tex = imported_textures.get(f"{prefix}_BC")
            n_tex = imported_textures.get(f"{prefix}_N")
            orm_tex = imported_textures.get(f"{prefix}_ORM")

            if bc_tex:
                mel.set_material_instance_texture_parameter_value(mi_obj, "BaseColorMap", bc_tex)
            if n_tex:
                mel.set_material_instance_texture_parameter_value(mi_obj, "NormalMap", n_tex)
            if orm_tex:
                mel.set_material_instance_texture_parameter_value(mi_obj, "ORMMap", orm_tex)

            asset_subsystem.save_loaded_asset(mi_obj)
            material_instances[mi_name] = mi_obj
            log(f"  -> Configured & Saved Material Instance: {mi_name}")

    # -------------------------------------------------------------------------
    # 4. ASSIGN HIGH-FIDELITY PHOTOGRAMMETRY MATERIALS TO ENVIRONMENT MESHES
    # -------------------------------------------------------------------------
    mesh_assignments = [
        # Brick structures -> MI_NanakshahiBrick_Photogrammetry
        ("/Game/Environment/Mohalla/Meshes/SM_Wall_Brick_4x4m_A", 0, "MI_NanakshahiBrick_Photogrammetry"),
        ("/Game/Environment/Mohalla/Meshes/SM_Wall_Brick_Doorway_4x4m", 0, "MI_NanakshahiBrick_Photogrammetry"),
        ("/Game/Environment/Mohalla/Meshes/SM_Wall_Brick_Window_4x4m", 0, "MI_NanakshahiBrick_Photogrammetry"),
        ("/Game/Environment/Mohalla/Meshes/SM_Floor_Ceiling_Slab_4x4m", 0, "MI_NanakshahiBrick_Photogrammetry"),
        ("/Game/Environment/Mohalla/Meshes/SM_Roof_Parapet_4m_A", 0, "MI_NanakshahiBrick_Photogrammetry"),
        ("/Game/Environment/Mohalla/Meshes/SM_Memorial_Historic_Well_Brick", 0, "MI_NanakshahiBrick_Photogrammetry"),
        ("/Game/Environment/Mohalla/Meshes/SM_Railway_Brick_Overpass_Arch", 0, "MI_NanakshahiBrick_Photogrammetry"),

        # Carved wood & haveli furniture -> MI_CarvedShisham_Photogrammetry
        ("/Game/Environment/Mohalla/Meshes/SM_Door_Deorhi_Teak_01", 0, "MI_CarvedShisham_Photogrammetry"),
        ("/Game/Environment/Mohalla/Meshes/SM_Prop_Haveli_Grain_Sandook", 0, "MI_CarvedShisham_Photogrammetry"),
        ("/Game/Environment/Mohalla/Meshes/SM_School_Desk_Bench_Wood", 0, "MI_CarvedShisham_Photogrammetry"),
        ("/Game/Environment/Mohalla/Meshes/SM_School_Blackboard_Easel", 0, "MI_CarvedShisham_Photogrammetry"),

        # Hammered brass metalwork -> MI_HammeredBrass_Photogrammetry
        ("/Game/Environment/Mohalla/Meshes/SM_Prop_Overturned_Brass_Lota", 0, "MI_HammeredBrass_Photogrammetry"),
        ("/Game/Environment/Mohalla/Meshes/SM_Prop_Bazaar_Tarazu_Scale", 0, "MI_HammeredBrass_Photogrammetry"),

        # Jute cordage & burlap sacks -> MI_WovenJute_Photogrammetry
        ("/Game/Environment/Mohalla/Meshes/SM_Prop_GrainSack_Jute_01", 0, "MI_WovenJute_Photogrammetry"),
        ("/Game/Environment/Mohalla/Meshes/SM_Prop_Charpai_RopeBed", 0, "MI_WovenJute_Photogrammetry")
    ]

    assigned_count = 0
    for mesh_path, slot_idx, mi_key in mesh_assignments:
        mesh = unreal.load_asset(mesh_path)
        mi_asset = material_instances.get(mi_key)

        if mesh and mi_asset:
            mesh.set_material(slot_idx, mi_asset)
            asset_subsystem.save_loaded_asset(mesh)
            assigned_count += 1
            log(f"  -> Assigned {mi_key} to {mesh.get_name()} [Slot {slot_idx}]")

    log(f"Assigned photogrammetry materials across {assigned_count} landmark static mesh slots.")

    # Clean up test assets if present
    if asset_subsystem.does_asset_exist("/Game/Environment/Mohalla/Materials/M_Test_Heritage"):
        asset_subsystem.delete_asset("/Game/Environment/Mohalla/Materials/M_Test_Heritage")
        log("Cleaned up temporary test material.")

    log("================================================================================")
    log("TASK 24: PHOTOGRAMMETRY TEXTURE & MATERIAL PIPELINE 100% COMPLETE")
    log("================================================================================")

if __name__ == "__main__":
    main()
