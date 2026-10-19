"""
Inspect set_ik_rig docstring
"""
import unreal

def log(msg):
    unreal.log_warning(f"[SET_IK_RIG] {msg}")

def main():
    rtg = unreal.load_asset("/Game/Characters/Kabir_AAA/Rigs/RTG_Mannequin_To_Kabir_AAA")
    ctrl = unreal.IKRetargeterController.get_controller(rtg)
    log(str(ctrl.set_ik_rig.__doc__))

if __name__ == "__main__":
    main()
