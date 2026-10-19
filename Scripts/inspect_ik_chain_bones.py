"""
Inspect IKRigController methods and IK_Mannequin chains start/end bones
"""
import unreal

def log(msg):
    unreal.log_warning(f"[IK_CTRL] {msg}")

def main():
    ik_manny = unreal.load_asset("/Game/Characters/Mannequins/Rigs/IK_Mannequin")
    ctrl = unreal.IKRigController.get_controller(ik_manny)
    
    log(f"Retarget Root: {ctrl.get_retarget_root()}")
    chains = ctrl.get_retarget_chains()
    for ch in chains:
        cname = ch.chain_name
        # Check start and end bone methods
        start_b = ctrl.get_retarget_chain_start_bone(cname)
        end_b = ctrl.get_retarget_chain_end_bone(cname)
        log(f"Chain '{cname}': Start='{start_b}', End='{end_b}'")

if __name__ == "__main__":
    main()
