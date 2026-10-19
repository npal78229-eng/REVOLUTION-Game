"""
Inspect exact BoneChain properties in IK_Mannequin
"""
import unreal

def log(msg):
    unreal.log_warning(f"[CHAIN_AUDIT] {msg}")

def main():
    ik_manny = unreal.load_asset("/Game/Characters/Mannequins/Rigs/IK_Mannequin")
    ctrl = unreal.IKRigController.get_controller(ik_manny)
    chains = ctrl.get_retarget_chains()
    for ch in chains:
        tup = ch.to_tuple()
        log(f"{ch.chain_name}: {tup}")

if __name__ == "__main__":
    main()
