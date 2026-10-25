import unreal

def check_exposure_props():
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)
    
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for a in actor_sub.get_all_level_actors():
        if a.get_actor_label() == "PostProcessVolume_Global":
            settings = a.get_editor_property("settings")
            for prop in dir(settings):
                if "exposure" in prop.lower() or "brightness" in prop.lower():
                    try:
                        val = getattr(settings, prop)
                        unreal.log_warning(f"PP property: {prop} = {val}")
                    except:
                        pass

if __name__ == "__main__":
    check_exposure_props()
