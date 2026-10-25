import unreal

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Maps/L_Validation_Gym")
actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = actor_sub.get_all_level_actors()
constable = next((a for a in actors if a.get_actor_label() == "NPC_Constable_Gurdial"), None)

loc1 = unreal.Vector(40.0, 1850.0, 88.0)
constable.set_actor_location(loc1, sweep=False, teleport=True)
loc3 = unreal.Vector(40.0, 1862.67, 88.0)
hit_res = constable.set_actor_location(loc3, sweep=True, teleport=False)

unreal.log_warning(f"HitResult export_text:\n{hit_res.export_text()}")
unreal.log_warning(f"HitResult to_tuple:\n{hit_res.to_tuple()}")

