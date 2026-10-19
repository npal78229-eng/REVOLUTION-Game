"""
Print attributes of Unreal FBX import options
"""
import unreal

def log(msg):
    unreal.log_warning(f"[FBX_OPTS] {msg}")

def main():
    ui = unreal.FbxImportUI()
    log("FbxImportUI attributes:")
    log(str([a for a in dir(ui) if not a.startswith("_")]))
    
    skel = unreal.FbxSkeletalMeshImportData()
    log("FbxSkeletalMeshImportData attributes:")
    log(str([a for a in dir(skel) if not a.startswith("_")]))

if __name__ == "__main__":
    main()
