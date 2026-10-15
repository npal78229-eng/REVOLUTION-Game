import unreal

def log(msg):
    unreal.log_warning(f"[PIE_VERIFY] {msg}")

log("================ VERIFYING PLAYER CONTROLLER & KABIR MOVEMENT ================")

level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
level_sub.load_level("/Game/Maps/L_Mohalla_Home")

actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

# Find PlayerStart
ps = None
for a in actor_sub.get_all_level_actors():
    if isinstance(a, unreal.PlayerStart):
        ps = a
        break

start_loc = ps.get_actor_location() if ps else unreal.Vector(-800, 120, 100)

# Spawn BP_Kabir
kabir_bp = unreal.EditorAssetLibrary.load_asset("/Game/Characters/Kabir/BP_Kabir")
kabir_class = kabir_bp.generated_class()
kabir_actor = actor_sub.spawn_actor_from_class(kabir_class, start_loc)

# Spawn PlayerController
pc_actor = actor_sub.spawn_actor_from_class(unreal.PlayerController, start_loc)

if kabir_actor and pc_actor:
    log(f"Spawned Kabir: {kabir_actor.get_name()}")
    log(f"Spawned PC: {pc_actor.get_name()}")

    # Possess Kabir
    pc_actor.possess(kabir_actor)
    log(f"Kabir Controller after possession: {kabir_actor.get_controller()}")

    # Call AddMovementInput
    kabir_actor.add_movement_input(unreal.Vector(1, 0, 0), 1.0, False)
    pending = kabir_actor.get_pending_movement_input_vector()
    log(f"Pending Movement Vector with Controller: {pending}")

    assert pending.x > 0.9, f"Movement vector should be non-zero after AddMovementInput! Got: {pending}"
    log("[SUCCESS] Movement input successfully registered on Kabir with Controller!")

    actor_sub.destroy_actor(kabir_actor)
    actor_sub.destroy_actor(pc_actor)
else:
    log("[FAIL] Could not spawn Kabir or PlayerController!")

log("================ VERIFICATION COMPLETE ================")
