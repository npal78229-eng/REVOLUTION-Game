import unreal

def inspect_details():
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)
    
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = actor_sub.get_all_level_actors()
    
    for a in actors:
        lbl = a.get_actor_label()
        if "AtmosphereController" in a.get_class().get_name() or "Atmosphere" in lbl:
            unreal.log_warning(f"AtmosphereController Actor: {lbl}")
            try:
                state = a.get_editor_property("CurrentAtmosphere")
                unreal.log_warning(f"  CurrentAtmosphere: {state}")
            except Exception as e:
                unreal.log_warning(f"  CurrentAtmosphere err: {e}")
        elif "PostProcess" in a.get_class().get_name():
            unreal.log_warning(f"PostProcess Actor: {lbl}")
            pp_comp = a.get_component_by_class(unreal.PostProcessComponent)
            if pp_comp:
                settings = pp_comp.get_editor_property("settings")
                unreal.log_warning(f"  bOverride_AutoExposureMethod: {settings.get_editor_property('bOverride_AutoExposureMethod')}")
                unreal.log_warning(f"  bOverride_AutoExposureMinBrightness: {settings.get_editor_property('bOverride_AutoExposureMinBrightness')}")
                unreal.log_warning(f"  bOverride_AutoExposureMaxBrightness: {settings.get_editor_property('bOverride_AutoExposureMaxBrightness')}")
                unreal.log_warning(f"  bOverride_AutoExposureBias: {settings.get_editor_property('bOverride_AutoExposureBias')}")
                unreal.log_warning(f"  Exposure Min: {settings.get_editor_property('auto_exposure_min_brightness')}, Max: {settings.get_editor_property('auto_exposure_max_brightness')}, Bias: {settings.get_editor_property('auto_exposure_bias')}")

if __name__ == "__main__":
    inspect_details()
