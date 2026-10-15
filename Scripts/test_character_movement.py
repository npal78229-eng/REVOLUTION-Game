import unreal

def log(msg):
    unreal.log_warning(f"[TEST_MOVE] {msg}")

log("================ TESTING KABIR MOVEMENT SIMULATION ================")

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
log(f"Spawn location: {start_loc}")

# Spawn BP_Kabir
kabir_bp = unreal.EditorAssetLibrary.load_asset("/Game/Characters/Kabir/BP_Kabir")
kabir_class = kabir_bp.generated_class()

kabir_actor = actor_sub.spawn_actor_from_class(kabir_class, start_loc)
if not kabir_actor:
    log("FAILED to spawn Kabir actor!")
else:
    log(f"Spawned Kabir: {kabir_actor.get_actor_label()}")
    loc_before = kabir_actor.get_actor_location()
    log(f"Location before: {loc_before}")

    cmc = kabir_actor.character_movement
    log(f"MaxWalkSpeed: {cmc.max_walk_speed}")
    log(f"GravityScale: {cmc.gravity_scale}")

    # Test adding movement input
    kabir_actor.add_movement_input(unreal.Vector(1, 0, 0), 1.0)
    pending = kabir_actor.get_pending_movement_input_vector()
    log(f"PendingInputVector: {pending}")
    assert pending.x > 0.9, f"Pending input vector should be (1,0,0), got {pending}"

    # Verify input actions on CDO
    cdo = unreal.get_default_object(kabir_class)
    imc = cdo.get_editor_property("default_mapping_context")
    move_action = cdo.get_editor_property("move_action")
    look_action = cdo.get_editor_property("look_action")
    jump_action = cdo.get_editor_property("jump_action")
    log(f"DefaultMappingContext: {imc.get_name() if imc else 'None'}")
    log(f"MoveAction: {move_action.get_name() if move_action else 'None'}")
    log(f"LookAction: {look_action.get_name() if look_action else 'None'}")
    log(f"JumpAction: {jump_action.get_name() if jump_action else 'None'}")

    assert imc is not None, "DefaultMappingContext must be assigned!"
    assert move_action is not None, "MoveAction must be assigned!"

    log("ALL MOVEMENT CHECKS PASSED FOR KABIR!")

    actor_sub.destroy_actor(kabir_actor)

log("================ TEST COMPLETE ================")
