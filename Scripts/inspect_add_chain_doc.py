"""
Inspect add_retarget_chain docstring
"""
import unreal

def log(msg):
    unreal.log_warning(f"[ADD_CHAIN] {msg}")

def main():
    log(str(unreal.IKRigController.add_retarget_chain.__doc__))

if __name__ == "__main__":
    main()
