import unreal

def main():
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level("/Game/Maps/L_Validation_Gym")
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = actor_sub.get_all_level_actors()
    unreal.log_warning(f"Total Actors: {len(actors)}")

    # Zone A (Haveli Courtyard) bounds check
    zone_a_actors = []
    min_x, max_x = float('inf'), float('-inf')
    min_y, max_y = float('inf'), float('-inf')
    min_z, max_z = float('inf'), float('-inf')

    blocking_volumes = []

    for a in actors:
        loc = a.get_actor_location()
        cname = a.get_class().get_name()
        label = a.get_actor_label()

        min_x = min(min_x, loc.x)
        max_x = max(max_x, loc.x)
        min_y = min(min_y, loc.y)
        max_y = max(max_y, loc.y)
        min_z = min(min_z, loc.z)
        max_z = max(max_z, loc.z)

        if "Blocking" in cname or "Volume" in cname or "Barrier" in label or "Boundary" in label:
            blocking_volumes.append((label, cname, loc))

        if -300 <= loc.x <= 700 and -300 <= loc.y <= 900:
            zone_a_actors.append((label, cname, loc.x, loc.y, loc.z))

    unreal.log_warning(f"World Bounds across all actors: X=[{min_x:.1f}, {max_x:.1f}], Y=[{min_y:.1f}, {max_y:.1f}], Z=[{min_z:.1f}, {max_z:.1f}]")
    unreal.log_warning(f"Blocking / Barrier volumes found: {len(blocking_volumes)}")
    for l, cn, loc in blocking_volumes:
        unreal.log_warning(f"  Volume: {l} ({cn}) at ({loc.x:.1f}, {loc.y:.1f}, {loc.z:.1f})")

    unreal.log_warning(f"Zone A (Haveli Courtyard) Actors ({len(zone_a_actors)}):")
    for label, cname, x, y, z in sorted(zone_a_actors, key=lambda it: it[0]):
        unreal.log_warning(f"  {label} ({cname}) at ({x:.1f}, {y:.1f}, {z:.1f})")

if __name__ == "__main__":
    main()
