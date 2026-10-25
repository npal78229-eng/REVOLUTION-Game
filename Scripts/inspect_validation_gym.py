"""
Inspect L_Validation_Gym
"""
import unreal

level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
level_sub.load_level("/Game/Maps/L_Validation_Gym")

actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = actor_sub.get_all_level_actors()

unreal.log_warning(f"L_Validation_Gym total actors: {len(actors)}")
for a in actors[:15]:
    unreal.log_warning(f"  {a.get_actor_label()} ({a.get_class().get_name()}) loc={a.get_actor_location()}")
