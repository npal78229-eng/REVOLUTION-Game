"""
PROJECT REVOLUTION — Configure Persian Wheel (Rahat) Interactive Labor Actor in L_Validation_Gym
Replaces static mesh actor with APersianWheelActor at (-1150, 2050, 0)
"""

import unreal

def setup_persian_wheel():
    unreal.log_warning("=== REVOLUTION: Configuring Interactive Persian Wheel Actor ===")

    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)

    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    persian_class = unreal.load_class(None, "/Script/REVOLUTION.PersianWheelActor")

    if not persian_class:
        unreal.log_error("Failed to load /Script/REVOLUTION.PersianWheelActor class!")
        return False

    loc = unreal.Vector(-1150.0, 2050.0, 0.0)
    rot = unreal.Rotator(0.0, 0.0, -15.0) # Pitch, Roll, Yaw in Unreal order or FRotator(pitch, yaw, roll)

    # Remove existing static mesh actor if present
    for a in actor_sub.get_all_level_actors():
        if a.get_actor_label() == "Rural_Persian_Wheel_Rahat_Canal":
            unreal.log_warning(f"Destroying old actor: {a.get_actor_label()} ({a.get_class().get_name()})")
            actor_sub.destroy_actor(a)

    # Spawn APersianWheelActor
    wheel_actor = actor_sub.spawn_actor_from_class(persian_class, loc, rot)
    if not wheel_actor:
        unreal.log_error("Failed to spawn APersianWheelActor!")
        return False

    wheel_actor.set_actor_label("Rural_Persian_Wheel_Rahat_Canal")
    wheel_actor.set_editor_property("community_cluster_id", unreal.Name("Cluster_UBDC_CanalBasti"))
    wheel_actor.set_editor_property("labor_trust_bonus", 35)
    wheel_actor.set_editor_property("flume_cleared", False)

    unreal.log_warning(f"Spawned APersianWheelActor '{wheel_actor.get_actor_label()}' at {wheel_actor.get_actor_location()}")
    unreal.log_warning(f"  Cluster: {wheel_actor.get_editor_property('community_cluster_id')}")
    unreal.log_warning(f"  Bonus: {wheel_actor.get_editor_property('labor_trust_bonus')}")

    # Save level
    b_saved = level_sub.save_current_level()
    unreal.log_warning(f"Level saved cleanly: {b_saved}")
    return True

if __name__ == "__main__":
    setup_persian_wheel()
