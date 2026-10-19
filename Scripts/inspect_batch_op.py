"""
Inspect IKRetargetBatchOperation in Unreal 5.5
"""
import unreal

def log(msg):
    unreal.log_warning(f"[BATCH_OP] {msg}")

def main():
    if hasattr(unreal, "IKRetargetBatchOperation"):
        log("Found IKRetargetBatchOperation:")
        log(str(dir(unreal.IKRetargetBatchOperation)))
    else:
        log("IKRetargetBatchOperation not found in unreal module.")

if __name__ == "__main__":
    main()
