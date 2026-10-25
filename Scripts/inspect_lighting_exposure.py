import unreal

def inspect_lighting():
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)
    
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = actor_sub.get_all_level_actors()
    
    unreal.log_warning(f"=== INSPECTING LIGHTING & EXPOSURE IN {level_path} ({len(actors)} actors) ===")
    
    pp_vols = []
    dir_lights = []
    sky_lights = []
    static_count = 0
    stationary_count = 0
    movable_count = 0
    
    for a in actors:
        cname = a.get_class().get_name()
        if "PostProcess" in cname:
            pp_vols.append(a)
        elif "DirectionalLight" in cname:
            dir_lights.append(a)
        elif "SkyLight" in cname:
            sky_lights.append(a)
            
        for comp in a.get_components_by_class(unreal.LightComponent):
            mob = comp.get_editor_property("mobility")
            mob_str = str(mob)
            if "STATIC" in mob_str:
                static_count += 1
            elif "STATIONARY" in mob_str:
                stationary_count += 1
            elif "MOVABLE" in mob_str:
                movable_count += 1
                
    unreal.log_warning(f"Lights mobility: STATIC={static_count}, STATIONARY={stationary_count}, MOVABLE={movable_count}")
    
    for dl in dir_lights:
        comp = dl.get_component_by_class(unreal.DirectionalLightComponent)
        if comp:
            unreal.log_warning(f"DirectionalLight '{dl.get_actor_label()}': Mobility={comp.get_editor_property('mobility')}, Intensity={comp.get_editor_property('intensity')}")
            
    for sl in sky_lights:
        comp = sl.get_component_by_class(unreal.SkyLightComponent)
        if comp:
            unreal.log_warning(f"SkyLight '{sl.get_actor_label()}': Mobility={comp.get_editor_property('mobility')}, Intensity={comp.get_editor_property('intensity')}, RealTimeCapture={comp.get_editor_property('real_time_capture')}")
            
    for pp in pp_vols:
        unreal.log_warning(f"PostProcessVolume '{pp.get_actor_label()}': Unbound={pp.get_editor_property('unbound')}")
        settings = pp.get_editor_property("settings")
        try:
            method = settings.get_editor_property("auto_exposure_method")
            min_ev = settings.get_editor_property("auto_exposure_min_brightness")
            max_ev = settings.get_editor_property("auto_exposure_max_brightness")
            bias = settings.get_editor_property("auto_exposure_bias")
            unreal.log_warning(f"  Exposure: Method={method}, Min={min_ev}, Max={max_ev}, Bias={bias}")
        except Exception as e:
            unreal.log_warning(f"  Exposure properties error: {e}")

if __name__ == "__main__":
    inspect_lighting()
