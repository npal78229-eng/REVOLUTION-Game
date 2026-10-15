import unreal

def add_atmo_actor():
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)

    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    all_actors = actor_sub.get_all_level_actors()

    existing = [a for a in all_actors if "AtmosphereController" in a.get_class().get_name()]
    if existing:
        unreal.log_warning(f"AtmosphereController already in level: {existing[0].get_actor_label()}")
        return True

    atmo_class = unreal.load_class(None, "/Script/REVOLUTION.RevolutionAtmosphereController")
    if not atmo_class:
        unreal.log_error("Could not load ARevolutionAtmosphereController class!")
        return False

    actor = actor_sub.spawn_actor_from_class(atmo_class, unreal.Vector(0.0, 0.0, 100.0))
    if actor:
        actor.set_actor_label("AtmosphereController_Historical")
        unreal.log_warning(f"Spawned {actor.get_actor_label()} in level.")
        level_sub.save_current_level()
        unreal.log_warning("Saved L_Validation_Gym successfully with AtmosphereController_Historical!")
        return True
    return False

if __name__ == "__main__":
    add_atmo_actor()
