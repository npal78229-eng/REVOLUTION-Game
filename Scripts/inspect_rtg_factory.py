"""
Inspect IKRig and IKRetargeter factories and creation methods in Unreal 5.5
"""
import unreal

def log(msg):
    unreal.log_warning(f"[RTG_FACTORY] {msg}")

def main():
    log("=== CHECKING FACTORIES & CONTROLLER METHODS ===")
    
    # Check IKRigDefinition factory
    for f in [unreal.IKRigDefinitionFactory, unreal.IKRetargetFactory]:
        log(f"Factory: {f.__name__}")
        
    rtg = unreal.load_asset("/Game/Characters/Kabir_AAA/Rigs/RTG_Mannequin_To_Kabir_AAA")
    if rtg:
        ctrl = unreal.IKRetargeterController.get_controller(rtg)
        log("IKRetargeterController methods:")
        methods = [m for m in dir(ctrl) if "retarget" in m.lower() or "anim" in m.lower() or "map" in m.lower() or "chain" in m.lower() or "pose" in m.lower()]
        log(str(methods))

if __name__ == "__main__":
    main()
