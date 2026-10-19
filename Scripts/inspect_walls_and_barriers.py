import unreal

def main():
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level("/Game/Maps/L_Validation_Gym")
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = actor_sub.get_all_level_actors()

    walls = []
    parapets = []
    barriers = []

    for a in actors:
        label = a.get_actor_label()
        loc = a.get_actor_location()
        if "Wall" in label:
            walls.append((label, loc))
        elif "Parapet" in label:
            parapets.append((label, loc))
        elif "Barrier" in label or "Gate" in label:
            barriers.append((label, loc))

    unreal.log_warning(f"Walls in Level ({len(walls)}):")
    for l, loc in sorted(walls, key=lambda it: (it[1].y, it[1].x)):
        unreal.log_warning(f"  Wall: {l} at ({loc.x:.1f}, {loc.y:.1f}, {loc.z:.1f})")

    unreal.log_warning(f"Parapets in Level ({len(parapets)}):")
    for l, loc in sorted(parapets, key=lambda it: (it[1].y, it[1].x)):
        unreal.log_warning(f"  Parapet: {l} at ({loc.x:.1f}, {loc.y:.1f}, {loc.z:.1f})")

    unreal.log_warning(f"Barriers/Gates in Level ({len(barriers)}):")
    for l, loc in sorted(barriers, key=lambda it: (it[1].y, it[1].x)):
        unreal.log_warning(f"  Barrier: {l} at ({loc.x:.1f}, {loc.y:.1f}, {loc.z:.1f})")

if __name__ == "__main__":
    main()
