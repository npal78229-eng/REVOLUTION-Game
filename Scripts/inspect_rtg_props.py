"""
Inspect source and target rig properties on IKRetargeter and its controller
"""
import unreal

def log(msg):
    unreal.log_warning(f"[RTG_INSPECT] {msg}")

def main():
    rtg = unreal.load_asset("/Game/Characters/Kabir_AAA/Rigs/RTG_Mannequin_To_Kabir_AAA")
    ctrl = unreal.IKRetargeterController.get_controller(rtg)
    
    log(f"rtg attributes: {[m for m in dir(rtg) if 'rig' in m.lower() or 'source' in m.lower() or 'target' in m.lower()]}")
    log(f"ctrl attributes: {[m for m in dir(ctrl) if 'rig' in m.lower() or 'source' in m.lower() or 'target' in m.lower()]}")

if __name__ == "__main__":
    main()
