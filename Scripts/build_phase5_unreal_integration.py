"""
PROJECT REVOLUTION — Phase 5: Complete Unreal Engine 5.5 Integration & Animation Retargeting
1. Setup Materials & assign PBR textures to SKM_Kabir_v05 slots
2. Build IK Rig: IK_Kabir_v05 with 28 Retarget Chains matching Manny
3. Build IK Retargeter: RTG_Manny_To_Kabir_v05
4. Batch Retarget Core Animations: MM_Idle, MM_Walk_Fwd, MM_Run_Fwd, MM_Jump
5. Update Character Blueprint BP_Kabir_v05 with SKM_Kabir_v05
"""

import os
import unreal

def log(msg):
    unreal.log_warning(f"[PHASE_5_INTEGRATOR] {msg}")

def setup_materials(skm):
    log("=== 1. SETTING UP PBR MATERIALS FOR KABIR v05 ===")
    editor_asset_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    mat_dir = "/Game/Characters/Kabir_v05/Materials"
    if not editor_asset_sub.does_directory_exist(mat_dir):
        editor_asset_sub.make_directory(mat_dir)
        
    tex_dir = "/Game/Characters/Kabir_v05/Textures"
    
    slots_config = [
        ("M_Kabir_Skin_PBR", f"{tex_dir}/T_Kabir_Head_BC", f"{tex_dir}/T_Kabir_Head_N", f"{tex_dir}/T_Kabir_Head_ORM"),
        ("M_Kabir_Eye_PBR", f"{tex_dir}/T_Kabir_Eye_BC", None, None),
        ("M_Hair", f"{tex_dir}/T_Kabir_Head_BC", None, None),
        ("M_Kabir_Khadi_PBR", f"{tex_dir}/T_Kabir_Cloth_BC", f"{tex_dir}/T_Kabir_Cloth_N", f"{tex_dir}/T_Kabir_Cloth_ORM"),
        ("M_Kabir_Leather_PBR", f"{tex_dir}/T_Kabir_Leather_BC", f"{tex_dir}/T_Kabir_Leather_N", f"{tex_dir}/T_Kabir_Leather_ORM")
    ]
    
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    mesh_mats = skm.get_editor_property("materials")
    
    for i, (mname, bc_path, n_path, orm_path) in enumerate(slots_config):
        mpath = f"{mat_dir}/{mname}"
        mat = unreal.load_asset(mpath)
        if not mat:
            mat = asset_tools.create_asset(mname, mat_dir, unreal.Material, unreal.MaterialFactoryNew())
            log(f"  Created Material: {mpath}")
            
        if mat:
            bc_tex = unreal.load_asset(bc_path) if bc_path else None
            n_tex = unreal.load_asset(n_path) if n_path else None
            orm_tex = unreal.load_asset(orm_path) if orm_path else None
            
            try:
                if bc_tex:
                    bc_node = unreal.MaterialEditingLibrary.create_material_expression(mat, unreal.MaterialExpressionTextureSample, -400, -200)
                    bc_node.texture = bc_tex
                    unreal.MaterialEditingLibrary.connect_material_property(bc_node, "RGBA", unreal.MaterialProperty.MP_BASE_COLOR)
                    
                if n_tex:
                    n_node = unreal.MaterialEditingLibrary.create_material_expression(mat, unreal.MaterialExpressionTextureSample, -400, 200)
                    n_node.texture = n_tex
                    n_node.sampler_type = unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL
                    unreal.MaterialEditingLibrary.connect_material_property(n_node, "RGB", unreal.MaterialProperty.MP_NORMAL)
                    
                if orm_tex:
                    orm_node = unreal.MaterialEditingLibrary.create_material_expression(mat, unreal.MaterialExpressionTextureSample, -400, 0)
                    orm_node.texture = orm_tex
                    orm_node.sampler_type = unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR
                    unreal.MaterialEditingLibrary.connect_material_property(orm_node, "R", unreal.MaterialProperty.MP_AMBIENT_OCCLUSION)
                    unreal.MaterialEditingLibrary.connect_material_property(orm_node, "G", unreal.MaterialProperty.MP_ROUGHNESS)
                    unreal.MaterialEditingLibrary.connect_material_property(orm_node, "B", unreal.MaterialProperty.MP_METALLIC)
                elif mname == "M_Kabir_Eye_PBR":
                    r_const = unreal.MaterialEditingLibrary.create_material_expression(mat, unreal.MaterialExpressionConstant, -200, 50)
                    r_const.r = 0.05
                    unreal.MaterialEditingLibrary.connect_material_property(r_const, "", unreal.MaterialProperty.MP_ROUGHNESS)
                elif mname == "M_Hair":
                    r_const = unreal.MaterialEditingLibrary.create_material_expression(mat, unreal.MaterialExpressionConstant, -200, 50)
                    r_const.r = 0.85
                    unreal.MaterialEditingLibrary.connect_material_property(r_const, "", unreal.MaterialProperty.MP_ROUGHNESS)
                    
                unreal.MaterialEditingLibrary.recompile_material(mat)
                editor_asset_sub.save_loaded_asset(mat)
            except Exception as e:
                log(f"  Note while wiring material {mname}: {e}")
                
            if i < len(mesh_mats):
                mesh_mats[i].material_interface = mat
                log(f"  Assigned slot [{i}] -> {mat.get_name()}")
                
    skm.set_editor_property("materials", mesh_mats)
    editor_asset_sub.save_loaded_asset(skm)
    log("Materials assigned and saved on SKM_Kabir_v05.")

def build_ik_rig(skm):
    log("=== 2. BUILDING IK RIG: IK_Kabir_v05 ===")
    rig_dir = "/Game/Characters/Kabir_v05/Rigs"
    editor_asset_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    if not editor_asset_sub.does_directory_exist(rig_dir):
        editor_asset_sub.make_directory(rig_dir)
        
    rig_path = f"{rig_dir}/IK_Kabir_v05"
    ik_rig = unreal.load_asset(rig_path)
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    
    if not ik_rig:
        factory = unreal.IKRigDefinitionFactory()
        ik_rig = asset_tools.create_asset("IK_Kabir_v05", rig_dir, unreal.IKRigDefinition, factory)
        log(f"  Created IK Rig asset: {rig_path}")
        
    ctrl = unreal.IKRigController.get_controller(ik_rig)
    ctrl.set_skeletal_mesh(skm)
    ctrl.set_retarget_root("pelvis")
    log("  Set Retarget Root: pelvis")
    
    chains_def = [
        ("Root", "root", "root"),
        ("Spine", "spine_01", "spine_05"),
        ("Neck", "neck_01", "neck_02"),
        ("Head", "head", "head"),
        ("LeftLeg", "thigh_l", "ball_l"),
        ("LeftClavicle", "clavicle_l", "clavicle_l"),
        ("LeftArm", "upperarm_l", "hand_l"),
        ("LeftIndexMetacarpal", "index_metacarpal_l", "index_metacarpal_l"),
        ("LeftMiddleMetacarpal", "middle_metacarpal_l", "middle_metacarpal_l"),
        ("LeftRingMetacarpal", "ring_metacarpal_l", "ring_metacarpal_l"),
        ("LeftPinkyMetacarpal", "pinky_metacarpal_l", "pinky_metacarpal_l"),
        ("LeftThumb", "thumb_01_l", "thumb_03_l"),
        ("LeftIndex", "index_01_l", "index_03_l"),
        ("LeftMiddle", "middle_01_l", "middle_03_l"),
        ("LeftRing", "ring_01_l", "ring_03_l"),
        ("LeftPinky", "pinky_01_l", "pinky_03_l"),
        ("RightLeg", "thigh_r", "ball_r"),
        ("RightClavicle", "clavicle_r", "clavicle_r"),
        ("RightArm", "upperarm_r", "hand_r"),
        ("RightIndexMetacarpal", "index_metacarpal_r", "index_metacarpal_r"),
        ("RightMiddleMetacarpal", "middle_metacarpal_r", "middle_metacarpal_r"),
        ("RightRingMetacarpal", "ring_metacarpal_r", "ring_metacarpal_r"),
        ("RightPinkyMetacarpal", "pinky_metacarpal_r", "pinky_metacarpal_r"),
        ("RightThumb", "thumb_01_r", "thumb_03_r"),
        ("RightIndex", "index_01_r", "index_03_r"),
        ("RightMiddle", "middle_01_r", "middle_03_r"),
        ("RightRing", "ring_01_r", "ring_03_r"),
        ("RightPinky", "pinky_01_r", "pinky_03_r")
    ]
    
    existing_chains = {c.chain_name for c in ctrl.get_retarget_chains()}
    for cname, start_b, end_b in chains_def:
        if cname in existing_chains:
            ctrl.set_retarget_chain_start_bone(cname, start_b)
            ctrl.set_retarget_chain_end_bone(cname, end_b)
        else:
            ctrl.add_retarget_chain(cname, start_b, end_b, "None")
            
    editor_asset_sub.save_loaded_asset(ik_rig)
    log(f"Configured all {len(chains_def)} retarget chains on IK_Kabir_v05.")
    return ik_rig

def build_ik_retargeter(ik_kabir):
    log("=== 3. BUILDING IK RETARGETER: RTG_Manny_To_Kabir_v05 ===")
    rig_dir = "/Game/Characters/Kabir_v05/Rigs"
    editor_asset_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    rtg_path = f"{rig_dir}/RTG_Manny_To_Kabir_v05"
    rtg = unreal.load_asset(rtg_path)
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    
    if not rtg:
        factory = unreal.IKRetargetFactory()
        rtg = asset_tools.create_asset("RTG_Manny_To_Kabir_v05", rig_dir, unreal.IKRetargeter, factory)
        log(f"  Created RTG asset: {rtg_path}")
        
    ctrl = unreal.IKRetargeterController.get_controller(rtg)
    ik_manny = unreal.load_asset("/Game/Characters/Mannequins/Rigs/IK_Mannequin")
    
    ctrl.set_ik_rig(unreal.RetargetSourceOrTarget.SOURCE, ik_manny)
    ctrl.set_ik_rig(unreal.RetargetSourceOrTarget.TARGET, ik_kabir)
    try:
        ctrl.auto_map_chains(unreal.AutoMapChainType.EXACT)
    except Exception:
        try:
            ctrl.auto_map_chains()
        except Exception as e:
            log(f"auto_map_chains note: {e}")
    
    editor_asset_sub.save_loaded_asset(rtg)
    log("RTG_Manny_To_Kabir_v05 configured and saved with auto-mapped chains.")
    return rtg

def retarget_animations(skm, rtg):
    log("=== 4. BATCH RETARGETING CORE ANIMATIONS ===")
    anim_dir = "/Game/Characters/Kabir_v05/Animations"
    editor_asset_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    if not editor_asset_sub.does_directory_exist(anim_dir):
        editor_asset_sub.make_directory(anim_dir)
        
    manny_mesh = unreal.load_asset("/Game/Characters/Mannequins/Meshes/SKM_Manny")
    
    anim_paths = [
        "/Game/Characters/Mannequins/Animations/Manny/MM_Idle",
        "/Game/Characters/Mannequins/Animations/Manny/MM_Walk_Fwd",
        "/Game/Characters/Mannequins/Animations/Manny/MM_Run_Fwd",
        "/Game/Characters/Mannequins/Animations/Manny/MM_Jump"
    ]
    
    assets_to_retarget = []
    for p in anim_paths:
        obj = unreal.load_asset(p)
        if obj:
            adata = editor_asset_sub.find_asset_data(p)
            if adata.is_valid():
                assets_to_retarget.append(adata)
                log(f"  Queued for retarget: {p}")
            else:
                log(f"  Warning: AssetData not valid for {p}")
        else:
            log(f"  Warning: Could not load {p}")
            
    log(f"Retargeting {len(assets_to_retarget)} animations...")
    batch_op = unreal.IKRetargetBatchOperation
    retargeted = batch_op.duplicate_and_retarget(
        assets_to_retarget=assets_to_retarget,
        source_mesh=manny_mesh,
        target_mesh=skm,
        ik_retarget_asset=rtg,
        search="/Game/Characters/Mannequins/Animations/Manny/",
        replace="/Game/Characters/Kabir_v05/Animations/",
        prefix="Kabir_v05_",
        suffix="",
        include_referenced_assets=False
    )
    
    log(f"Successfully retargeted {len(retargeted)} assets.")
    for r in retargeted:
        log(f"  Exported animation: {r.package_name}")

def update_character_blueprint(skm):
    log("=== 5. UPDATING CHARACTER BLUEPRINT BP_Kabir_v05 ===")
    bp_path = "/Game/Characters/Kabir/BP_Kabir_v05"
    bp = unreal.load_asset(bp_path)
    if bp:
        gen_class = unreal.load_object(None, f"{bp_path}_C")
        if gen_class:
            cdo = unreal.get_default_object(gen_class)
            mesh_comp = cdo.get_editor_property("mesh")
            if mesh_comp:
                mesh_comp.set_skeletal_mesh_asset(skm)
                log("  Assigned SKM_Kabir_v05 to BP_Kabir_v05 mesh component.")
        editor_asset_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
        editor_asset_sub.save_loaded_asset(bp)
        log("BP_Kabir_v05 updated successfully.")

def main():
    log("=== BEGINNING PHASE 5: UNREAL ENGINE 5.5 INTEGRATION ===")
    skm = unreal.load_asset("/Game/Characters/Kabir_v05/SKM_Kabir_v05")
    if not skm:
        log("ERROR: Could not load SKM_Kabir_v05.")
        return
        
    setup_materials(skm)
    ik_kabir = build_ik_rig(skm)
    rtg = build_ik_retargeter(ik_kabir)
    retarget_animations(skm, rtg)
    update_character_blueprint(skm)
    log("=== PHASE 5 INTEGRATION COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    main()
