import unreal

level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
level_sub.load_level("/Game/Maps/L_Validation_Gym")

world = level_sub.get_current_level().get_world()
ws = world.get_world_settings()
gm = ws.get_editor_property("default_game_mode")
unreal.log_warning(f"[GYM_CHECK] L_Validation_Gym DefaultGameMode: {gm}")
