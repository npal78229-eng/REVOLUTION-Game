import unreal

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Maps/L_Validation_Gym")
actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = actor_sub.get_all_level_actors()

test_x = 40.0
test_y = 1850.0
test_z = 88.0

unreal.log_warning(f"Loaded {len(actors)} actors. Finding actors near ({test_x}, {test_y}, {test_z})...")

for a in actors:
    name = a.get_name()
    label = a.get_actor_label()
    if "CurfewPatrolAI" in a.get_class().get_name() or label == "NPC_Constable_Gurdial":
        continue
    bounds = a.get_actor_bounds(False)
    origin, extent = bounds[0], bounds[1]
    
    # Distance from center to test point
    dx = abs(test_x - origin.x)
    dy = abs(test_y - origin.y)
    dz = abs(test_z - origin.z)
    
    if dx < (extent.x + 100) and dy < (extent.y + 100) and dz < (extent.z + 100):
        unreal.log_warning(f"ACTOR_MATCH: label='{label}' name='{name}' class='{a.get_class().get_name()}' origin=({origin.x:.1f}, {origin.y:.1f}, {origin.z:.1f}) extent=({extent.x:.1f}, {extent.y:.1f}, {extent.z:.1f})")

