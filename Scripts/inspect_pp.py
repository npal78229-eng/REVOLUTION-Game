import unreal

def inspect_pp():
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)
    
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for a in actor_sub.get_all_level_actors():
        if a.get_actor_label() == "PostProcessVolume_Global":
            settings = a.get_editor_property("settings")
            # In UE, settings is FPostProcessSettings
            unreal.log_warning(f"PP Settings: AutoExposureMethod={settings.auto_exposure_method}")
            unreal.log_warning(f"  MinBrightness={settings.auto_exposure_min_brightness}, MaxBrightness={settings.auto_exposure_max_brightness}, Bias={settings.auto_exposure_bias}")
            unreal.log_warning(f"  AutoExposureApplyPhysicalCameraExposure={settings.auto_exposure_apply_physical_camera_exposure}")
        elif a.get_actor_label() == "DirectionalLight_Sun":
            comp = a.get_component_by_class(unreal.DirectionalLightComponent)
            unreal.log_warning(f"DirectionalLight_Sun: Intensity={comp.get_editor_property('intensity')}, Mobility={comp.get_editor_property('mobility')}")
        elif a.get_actor_label() == "SkyLight_RealTime":
            comp = a.get_component_by_class(unreal.SkyLightComponent)
            unreal.log_warning(f"SkyLight_RealTime: Intensity={comp.get_editor_property('intensity')}, Mobility={comp.get_editor_property('mobility')}")

if __name__ == "__main__":
    inspect_pp()
