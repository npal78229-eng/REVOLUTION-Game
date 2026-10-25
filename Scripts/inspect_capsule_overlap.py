import unreal

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Maps/L_Validation_Gym")
actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = actor_sub.get_all_level_actors()

constable = next((a for a in actors if a.get_actor_label() == "NPC_Constable_Gurdial"), None)
capsule = constable.get_component_by_class(unreal.CapsuleComponent)

unreal.log_warning(f"Constable: {constable.get_name()}, Capsule: {capsule.get_name()}")
capsule_r = capsule.get_scaled_capsule_radius()
capsule_h = capsule.get_scaled_capsule_half_height()
unreal.log_warning(f"Capsule Radius: {capsule_r}, HalfHeight: {capsule_h}")

# Place at WP[1]
loc1 = unreal.Vector(40.0, 1850.0, 88.0)
constable.set_actor_location(loc1, sweep=False, teleport=True)

# Check overlaps at loc1
overlaps = constable.get_overlapping_actors()
unreal.log_warning(f"Overlapping actors at WP[1]: {[a.get_actor_label() for a in overlaps]}")

# Now step forward to 1854
loc2 = unreal.Vector(40.0, 1854.0, 88.0)
hit_bool = constable.set_actor_location(loc2, sweep=True, teleport=False)
actual2 = constable.get_actor_location()
unreal.log_warning(f"Move to 1854: hit_bool={hit_bool}, actual={actual2}")

# Now step to 1860 with sweep
loc3 = unreal.Vector(40.0, 1862.67, 88.0)
hit_bool3 = constable.set_actor_location(loc3, sweep=True, teleport=False)
actual3 = constable.get_actor_location()
unreal.log_warning(f"Move to 1862.67: hit_bool={hit_bool3}, actual={actual3}")

# Let's test moving without sweep to 1862.67, then check overlaps
constable.set_actor_location(loc3, sweep=False, teleport=True)
overlaps3 = constable.get_overlapping_actors()
unreal.log_warning(f"Overlapping actors at 1862.67 (teleported): {[a.get_actor_label() for a in overlaps3]}")

# Also check all actors with collision enabled in gym and check collision with capsule
for a in actors:
    if a == constable:
        continue
    comps = a.get_components_by_class(unreal.PrimitiveComponent)
    for c in comps:
        if c.get_collision_enabled() != unreal.CollisionEnabled.NO_COLLISION:
            # check distance
            b = c.bounds
            d = (b.origin - loc3).length()
            if d < 300:
                unreal.log_warning(f"Nearby Primitive: Actor='{a.get_actor_label()}' Comp='{c.get_name()}' ColProfile='{c.get_collision_profile_name()}' Origin={b.origin} Extent={b.box_extent}")

