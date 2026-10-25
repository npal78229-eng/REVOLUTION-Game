import unreal

mesh = unreal.EditorAssetLibrary.load_asset("/Game/Environment/Mohalla/Meshes/SM_Checkpoint_Picket_Sandbag_Barrier")
if mesh:
    bounds = mesh.get_bounds()
    unreal.log_warning(f"StaticMesh Bounds: Origin={bounds.origin}, BoxExtent={bounds.box_extent}, SphereRadius={bounds.sphere_radius}")
    num_lods = mesh.get_num_lods()
    num_sections = mesh.get_num_sections(0)
    unreal.log_warning(f"LODs: {num_lods}, Sections: {num_sections}")
    # Check body setup / simple collision
    body_setup = mesh.get_editor_property("body_setup")
    if body_setup:
        unreal.log_warning(f"BodySetup: CollisionTraceFlag={body_setup.get_editor_property('collision_trace_flag')}")
        agg_geom = body_setup.get_editor_property("agg_geom")
        unreal.log_warning(f"AggGeom: BoxElems={len(agg_geom.box_elems)}, SphylElems={len(agg_geom.sphyl_elems)}, ConvexElems={len(agg_geom.convex_elems)}")
        for i, b in enumerate(agg_geom.box_elems):
            unreal.log_warning(f"  Box[{i}]: Center={b.center}, X={b.x}, Y={b.y}, Z={b.z}")
        for i, c in enumerate(agg_geom.convex_elems):
            unreal.log_warning(f"  Convex[{i}]: BoxExtent={c.elem_box.get_extent()} Center={c.elem_box.get_center()}")
