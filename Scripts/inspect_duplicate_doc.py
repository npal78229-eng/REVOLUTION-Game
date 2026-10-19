"""
Print docstring of duplicate_and_retarget
"""
import unreal

def log(msg):
    unreal.log_warning(f"[BATCH_DOC] {msg}")

def main():
    log(str(unreal.IKRetargetBatchOperation.duplicate_and_retarget.__doc__))

if __name__ == "__main__":
    main()
