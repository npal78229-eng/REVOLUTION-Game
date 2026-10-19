import unreal

def main():
    gym_map = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(gym_map)

    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = actor_sub.get_all_level_actors()
    ladder = None
    for a in actors:
        if a.get_actor_label() == "Jallianwala_Makeshift_Ladder_North":
            ladder = a
            break

    if ladder:
        loc = ladder.get_actor_location()
        scale = ladder.get_actor_scale3d()
        bounds = ladder.get_actor_bounds(False)
        origin = bounds[0]
        box_extent = bounds[1]
        unreal.log_warning(f"=== JALLIANWALA LADDER IN LEVEL ===")
        unreal.log_warning(f"Loc: ({loc.x:.1f}, {loc.y:.1f}, {loc.z:.1f})")
        unreal.log_warning(f"Scale: ({scale.x:.3f}, {scale.y:.3f}, {scale.z:.3f})")
        unreal.log_warning(f"Bounds Extent: ({box_extent.x:.1f}, {box_extent.y:.1f}, {box_extent.z:.1f})")
        unreal.log_warning(f"Bounds Total Size: X={box_extent.x*2:.1f}, Y={box_extent.y*2:.1f}, Z={box_extent.z*2:.1f}")

if __name__ == "__main__":
    main()
