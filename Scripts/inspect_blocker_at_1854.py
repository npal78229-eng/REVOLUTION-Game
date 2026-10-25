import unreal

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Maps/L_Validation_Gym")
actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = actor_sub.get_all_level_actors()

test_x = 40.0
test_y = 1854.0
test_z = 88.0

unreal.log_warning(f"Searching actors near X={test_x}, Y={test_y}, Z={test_z} (Radius 250)...")

for a in actors:
    # Skip the constable himself!
    if "CurfewPatrolAI" in a.get_class().get_name() or a.get_actor_label() == "NPC_Constable_Gurdial":
        continue
    
    loc = a.get_actor_location()
    bounds = a.get_actor_bounds(False)
    origin, extent = bounds[0], bounds[1]
    
    # Distance to test point
    dx = abs(test_x - origin.x)
    dy = abs(test_y - origin.y)
    dz = abs(test_z - origin.z)
    
    if dx <= (extent.x + 50.0) and dy <= (extent.y + 50.0) and dz <= (extent.z + 100.0):
        # Check components
        smc = a.get_component_by_class(unreal.PrimitiveComponent)
        col_prof = smc.get_collision_profile_name() if smc else "N/A"
        col_en = smc.get_collision_enabled() if smc else "N/A"
        unreal.log_warning(f"  [NEARBY] '{a.get_actor_label()}' ({a.get_name()}) | Class: {a.get_class().get_name()} | Profile: {col_prof} | ColEnabled: {col_en} | Bounds: {origin} +- {extent}")

