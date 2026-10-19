import unreal

def main():
    gym_map = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(gym_map)

    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = actor_sub.get_all_level_actors()

    print("\n================ ROOFTOP & 1F HAVELI ACTORS ================")
    for a in actors:
        loc = a.get_actor_location()
        label = a.get_actor_label()
        if -500 <= loc.x <= 700 and -600 <= loc.y <= 700 and loc.z >= 350:
            sm = a.get_component_by_class(unreal.StaticMeshComponent)
            mesh_name = sm.get_editor_property("static_mesh").get_name() if (sm and sm.get_editor_property("static_mesh")) else "None"
            rot = a.get_actor_rotation()
            print(f"[{loc.z:5.1f}] {label:40s} | Mesh: {mesh_name:30s} | Loc: ({loc.x:6.1f}, {loc.y:6.1f}, {loc.z:6.1f}) | Yaw: {rot.yaw:.1f}")

if __name__ == "__main__":
    main()
