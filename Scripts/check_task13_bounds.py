import unreal

def check_bounds():
    meshes = [
        "SM_Locomotive_Engine_PunjabMail",
        "SM_Civil_Lines_Clubhouse_Bungalow",
        "SM_Cantonment_Guardhouse_Picket",
        "SM_Prop_Cantonment_Archive_Cabinet"
    ]
    for m in meshes:
        path = f"/Game/Environment/Mohalla/Meshes/{m}"
        asset = unreal.load_asset(path)
        if asset:
            bounds = asset.get_bounds()
            unreal.log_warning(f"[TASK13_BOUNDS] {m}: Origin={bounds.origin}, BoxExtent={bounds.box_extent}, SphereRadius={bounds.sphere_radius}")
        else:
            unreal.log_error(f"[TASK13_BOUNDS] Failed to load {path}")

if __name__ == "__main__":
    check_bounds()
