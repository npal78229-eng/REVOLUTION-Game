import unreal

world = unreal.EditorLoadingAndSavingUtils.load_map("/Game/Maps/L_Validation_Gym")
actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = actor_sub.get_all_level_actors()

munadi = next((a for a in actors if a.get_actor_label() == "NPC_Munadi_TownCrier"), None)
assert munadi is not None, "NPC_Munadi_TownCrier not found!"

new_loc = unreal.Vector(115.0, 1920.0, 88.0)
munadi.set_actor_location(new_loc, sweep=False, teleport=True)
unreal.log_warning(f"Set Munadi loc: {munadi.get_actor_location()}")

res = unreal.EditorLoadingAndSavingUtils.save_dirty_packages(False, True)
unreal.log_warning(f"save_dirty_packages: {res}")

saved_dir = unreal.EditorAssetLibrary.save_directory("/Game/Maps", only_if_is_dirty=False, recursive=True)
unreal.log_warning(f"save_directory result: {saved_dir}")

