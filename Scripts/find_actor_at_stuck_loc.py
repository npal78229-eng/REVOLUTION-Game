import unreal

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Maps/L_Validation_Gym")
actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = actor_sub.get_all_level_actors()

unreal.log_warning(f"Searching {len(actors)} actors around X=118, Y=1795, Z=91...")

matches = []
for a in actors:
    smc = a.get_component_by_class(unreal.StaticMeshComponent)
    if not smc:
        continue
    loc = a.get_actor_location()
    bounds = a.get_actor_bounds(False)
    origin, extent = bounds[0], bounds[1]
    
    # Check distance from (118.87, 1795.29, 91.40)
    dx = abs(118.87 - origin.x)
    dy = abs(1795.29 - origin.y)
    dz = abs(91.40 - origin.z)
    
    if dx < (extent.x + 80) and dy < (extent.y + 80) and dz < (extent.z + 80):
        mesh = smc.get_editor_property("static_mesh")
        mesh_name = mesh.get_name() if mesh else "None"
        col_prof = smc.get_collision_profile_name()
        col_en = smc.get_collision_enabled()
        matches.append((a, mesh_name, col_prof, col_en, origin, extent))

for m in matches:
    a, mesh_name, col_prof, col_en, origin, extent = m
    unreal.log_warning(f"  [MATCH] '{a.get_actor_label()}' ({a.get_name()}) | Mesh: {mesh_name} | Profile: {col_prof} | Col: {col_en} | Bounds: {origin} +- {extent}")
