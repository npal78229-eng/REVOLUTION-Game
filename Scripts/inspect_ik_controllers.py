"""
Inspect IK Rig and IK Retargeter controllers in Unreal Engine 5.5
"""
import unreal

def log(msg):
    unreal.log_warning(f"[IK_AUDIT] {msg}")

def main():
    log("=== INSPECTING IK RIGS & RETARGETERS ===")
    
    # 1. Inspect Manny IK Rig
    ik_manny = unreal.load_asset("/Game/Characters/Mannequins/Rigs/IK_Mannequin")
    if ik_manny:
        log(f"Loaded IK_Mannequin: {ik_manny.get_name()}")
        ctrl_manny = unreal.IKRigController.get_controller(ik_manny)
        if ctrl_manny:
            chains = ctrl_manny.get_retarget_chains()
            log(f"IK_Mannequin has {len(chains)} retarget chains:")
            if chains:
                log(f"BoneChain attributes: {dir(chains[0])}")
                for ch in chains:
                    log(f"  Chain: {ch.chain_name}")
                
    # 2. Inspect Kabir_AAA IK Rig
    ik_kabir = unreal.load_asset("/Game/Characters/Kabir_AAA/Rigs/IK_Kabir_AAA")
    if ik_kabir:
        log(f"Loaded IK_Kabir_AAA: {ik_kabir.get_name()}")
        ctrl_kabir = unreal.IKRigController.get_controller(ik_kabir)
        if ctrl_kabir:
            chains = ctrl_kabir.get_retarget_chains()
            log(f"IK_Kabir_AAA has {len(chains)} retarget chains:")
            for ch in chains:
                log(f"  Kabir Chain: {ch.chain_name}")
                
    # 3. Inspect RTG_Mannequin_To_Kabir_AAA
    rtg = unreal.load_asset("/Game/Characters/Kabir_AAA/Rigs/RTG_Mannequin_To_Kabir_AAA")
    if rtg:
        log(f"Loaded RTG: {rtg.get_name()}")
        rtg_ctrl = unreal.IKRetargeterController.get_controller(rtg)
        if rtg_ctrl:
            src_rig = rtg_ctrl.get_source_ik_rig()
            tgt_rig = rtg_ctrl.get_target_ik_rig()
            log(f"  Source: {src_rig.get_name() if src_rig else 'None'}, Target: {tgt_rig.get_name() if tgt_rig else 'None'}")

if __name__ == "__main__":
    main()
