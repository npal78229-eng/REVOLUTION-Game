import unreal

def run_fixes():
    unreal.log_warning("=========================================================")
    unreal.log_warning("  PROJECT REVOLUTION — FIXING LIGHTING, COLLISION & ASSETS")
    unreal.log_warning("=========================================================")

    # 1. Load Master Level
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    level_sub.load_level(level_path)

    actors = actor_sub.get_all_level_actors()
    unreal.log_warning(f"Loaded {level_path} with {len(actors)} actors.")

    # -------------------------------------------------------------
    # DEFECT 1: CONVERT ALL LIGHTS TO MOVABLE (LUMEN DYNAMIC LIGHTING)
    # -------------------------------------------------------------
    converted_lights_count = 0
    for a in actors:
        lbl = a.get_actor_label()
        for comp in a.get_components_by_class(unreal.LightComponent):
            mob = comp.get_editor_property("mobility")
            mob_str = str(mob)
            if "STATIC" in mob_str or "STATIONARY" in mob_str:
                comp.set_editor_property("mobility", unreal.ComponentMobility.MOVABLE)
                converted_lights_count += 1
                unreal.log_warning(f"Converted light to MOVABLE: '{lbl}' ({comp.get_name()})")

    unreal.log_warning(f"Total lights converted to MOVABLE: {converted_lights_count}")

    # Remove or rebalance unshadowed fill lights at player start
    for a in actors:
        lbl = a.get_actor_label()
        if lbl in ["Hero_Sun_Fill_Light", "Hero_Key_Light", "Hero_Rim_Light"]:
            comp = a.get_component_by_class(unreal.PointLightComponent)
            if comp:
                # Reduce to gentle, natural ambient fill
                comp.set_editor_property("intensity", 250.0)
                comp.set_editor_property("mobility", unreal.ComponentMobility.MOVABLE)
                unreal.log_warning(f"Rebalanced hero light '{lbl}' to 250 lux fill.")

    # Tune PostProcessVolume_Global for proper auto-exposure
    pp_found = False
    for a in actors:
        if a.get_actor_label() == "PostProcessVolume_Global":
            pp_found = True
            pp_vol = a
            pp_vol.set_editor_property("unbound", True)
            settings = pp_vol.get_editor_property("settings")
            
            # Auto Exposure Settings
            settings.set_editor_property("override_auto_exposure_method", True)
            settings.set_editor_property("auto_exposure_method", unreal.AutoExposureMethod.AEM_HISTOGRAM)
            
            settings.set_editor_property("override_auto_exposure_min_brightness", True)
            settings.set_editor_property("auto_exposure_min_brightness", 0.03)
            
            settings.set_editor_property("override_auto_exposure_max_brightness", True)
            settings.set_editor_property("auto_exposure_max_brightness", 16.0)
            
            settings.set_editor_property("override_auto_exposure_bias", True)
            settings.set_editor_property("auto_exposure_bias", 0.0)
            
            settings.set_editor_property("override_auto_exposure_speed_up", True)
            settings.set_editor_property("auto_exposure_speed_up", 3.0)
            
            settings.set_editor_property("override_auto_exposure_speed_down", True)
            settings.set_editor_property("auto_exposure_speed_down", 1.0)
            
            pp_vol.set_editor_property("settings", settings)
            unreal.log_warning("PostProcessVolume_Global auto-exposure overrides enabled (Histogram [0.03, 16.0]).")
            break

    assert pp_found, "PostProcessVolume_Global not found!"

    # -------------------------------------------------------------
    # DEFECT 4: FIX PATROL COLLISION (StaticMeshActor_128 / Canopy)
    # -------------------------------------------------------------
    canopy_fixed_count = 0
    for a in actors:
        lbl = a.get_actor_label()
        name = a.get_name()
        if "Canopy" in lbl or "Awning" in lbl or name == "StaticMeshActor_128":
            comp = a.get_component_by_class(unreal.StaticMeshComponent)
            if comp:
                comp.set_collision_profile_name("NoCollision")
                comp.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
                canopy_fixed_count += 1
                unreal.log_warning(f"Set collision to NoCollision for awning/canopy '{lbl}' ({name})")

    unreal.log_warning(f"Total canopy/awning actors set to NoCollision: {canopy_fixed_count}")

    # Save level changes
    unreal.EditorLevelLibrary.save_current_level()
    unreal.log_warning(f"Saved level {level_path} successfully.")

    # -------------------------------------------------------------
    # DEFECT 3: FIX MATERIAL USAGE FLAGS FOR SKELETAL MESHES
    # -------------------------------------------------------------
    asset_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    
    materials_to_check = [
        "/Game/Environment/Mohalla/Materials/M_ClothIndigo_PBR",
        "/Game/Environment/Mohalla/Materials/M_ClothSaffron_PBR",
        "/Game/Environment/Mohalla/Materials/M_ClothTurban_PBR",
        "/Game/Characters/Mannequins/Materials/M_Manny_Simple",
        "/Game/Characters/Kabir_v05/M_Kabir_Khadi_PBR",
        "/Game/Characters/Kabir_v05/M_Kabir_Skin_PBR",
        "/Game/Characters/Kabir_v05/M_Kabir_Leather_PBR",
        "/Game/Characters/Kabir_v05/M_Kabir_Eye_PBR",
        "/Game/Characters/Kabir_v05/M_Hair"
    ]
    
    for mat_path in materials_to_check:
        if unreal.EditorAssetLibrary.does_asset_exist(mat_path):
            mat = unreal.EditorAssetLibrary.load_asset(mat_path)
            if isinstance(mat, unreal.Material):
                used_skm = mat.get_editor_property("b_used_with_skeletal_mesh")
                if not used_skm:
                    mat.set_editor_property("b_used_with_skeletal_mesh", True)
                    unreal.MaterialEditingLibrary.recompile_material(mat)
                    unreal.EditorAssetLibrary.save_loaded_asset(mat)
                    unreal.log_warning(f"Updated and recompiled b_used_with_skeletal_mesh = True on {mat_path}")
                else:
                    unreal.log_warning(f"Material {mat_path} already has b_used_with_skeletal_mesh = True")
            elif isinstance(mat, unreal.MaterialInstanceConstant):
                # Check parent material
                parent = mat.get_editor_property("parent")
                if parent and isinstance(parent, unreal.Material):
                    if not parent.get_editor_property("b_used_with_skeletal_mesh"):
                        parent.set_editor_property("b_used_with_skeletal_mesh", True)
                        unreal.MaterialEditingLibrary.recompile_material(parent)
                        unreal.EditorAssetLibrary.save_loaded_asset(parent)
                        unreal.log_warning(f"Updated parent material {parent.get_path_name()} b_used_with_skeletal_mesh = True")

    unreal.log_warning("=========================================================")
    unreal.log_warning("  FIXES COMPLETE: LEVEL AND ASSETS SAVED SUCCESSFULLY")
    unreal.log_warning("=========================================================")

if __name__ == "__main__":
    run_fixes()
