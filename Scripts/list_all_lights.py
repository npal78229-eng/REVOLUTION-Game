import unreal

def list_lights():
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)
    
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = actor_sub.get_all_level_actors()
    
    for a in actors:
        for comp in a.get_components_by_class(unreal.LightComponent):
            mob = str(comp.get_editor_property("mobility"))
            unreal.log_warning(f"Light Actor '{a.get_actor_label()}' ({comp.get_name()}): Mobility={mob}, Intensity={comp.get_editor_property('intensity')}")

if __name__ == "__main__":
    list_lights()
