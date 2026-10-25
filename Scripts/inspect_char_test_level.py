"""
Inspect L_Character_Test_v02
"""
import unreal

level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
loaded = level_sub.load_level("/Game/Maps/L_Character_Test_v02")

actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = actor_sub.get_all_level_actors()

unreal.log_warning(f"L_Character_Test_v02 loaded: {loaded}, actors: {len(actors)}")
for a in actors:
    unreal.log_warning(f"  {a.get_actor_label()} ({a.get_class().get_name()}) loc={a.get_actor_location()}")
