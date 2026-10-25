import unreal

level_path = "/Game/Maps/L_Validation_Gym"
level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
level_sub.load_level(level_path)

actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = actor_sub.get_all_level_actors()

munadi = next((a for a in actors if a.get_actor_label() == "NPC_Munadi_TownCrier"), None)
if munadi:
    new_loc = unreal.Vector(115.0, 1920.0, 88.0)
    munadi.set_actor_location(new_loc, sweep=False, teleport=True)
    unreal.log_warning(f"NPC_Munadi_TownCrier moved to: {munadi.get_actor_location()}")

saved = level_sub.save_current_level()
unreal.log_warning(f"save_current_level result: {saved}")
