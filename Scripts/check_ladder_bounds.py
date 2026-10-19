import unreal

def main():
    mesh_path = "/Game/Environment/Mohalla/Meshes/SM_Prop_Makeshift_Timber_Ladder"
    mesh = unreal.load_asset(mesh_path)
    if not mesh:
        unreal.log_warning(f"Failed to load {mesh_path}")
        return
    
    bounds = mesh.get_bounds()
    box_extent = bounds.box_extent
    origin = bounds.origin
    unreal.log_warning(f"=== LADDER MESH BOUNDS ===")
    unreal.log_warning(f"Origin: ({origin.x:.1f}, {origin.y:.1f}, {origin.z:.1f})")
    unreal.log_warning(f"Box Extent: ({box_extent.x:.1f}, {box_extent.y:.1f}, {box_extent.z:.1f})")
    unreal.log_warning(f"Total Size: X={box_extent.x*2:.1f}, Y={box_extent.y*2:.1f}, Z={box_extent.z*2:.1f}")

if __name__ == "__main__":
    main()
