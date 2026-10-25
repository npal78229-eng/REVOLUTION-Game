import unreal

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Maps/L_Validation_Gym")
actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = actor_sub.get_all_level_actors()

constable = next((a for a in actors if a.get_actor_label() == "NPC_Constable_Gurdial"), None)
world = constable.get_world() if constable else None

start = unreal.Vector(40.0, 1850.0, 88.0)
end = unreal.Vector(40.0, 1862.67, 88.0)
radius = 42.0
half_height = 96.0

# Perform capsule trace
hit = unreal.HitResult()
# unreal.SystemLibrary.capsule_trace_single(world_context_object, start, end, radius, half_height, trace_channel, trace_complex, actors_to_ignore, draw_debug_type, ignore_self, trace_color, trace_hit_color, draw_time)
actors_to_ignore = [constable] if constable else []

hit_result = unreal.SystemLibrary.capsule_trace_single(
    world,
    start,
    end,
    radius,
    half_height,
    unreal.TraceTypeQuery.TRACE_TYPE_QUERY1, # Visibility
    False, # complex
    actors_to_ignore,
    unreal.DrawDebugTrace.NONE,
    True, # ignore self
    unreal.LinearColor.RED,
    unreal.LinearColor.GREEN,
    0.0
)

unreal.log_warning(f"Capsule Trace Visibility Hit: {hit_result}")

# Also try Camera / Pawn trace
# Let's inspect all static mesh actors near X=40, Y=1850-1865
for a in actors:
    if a.get_actor_label() in ["Story_Bazaar_Cart_Thela", "Modular_Bazaar_KhadiBolt1", "Modular_Bazaar_Stall_ClothKhadi", "Street_Drain_Gutter_BazaarNorth", "Boundary_Barrier_NorthGate_West"]:
        loc = a.get_actor_location()
        scale = a.get_actor_scale3d()
        smc = a.get_component_by_class(unreal.StaticMeshComponent)
        col_prof = smc.get_collision_profile_name() if smc else "None"
        unreal.log_warning(f"ACTOR_DETAIL: label='{a.get_actor_label()}' name='{a.get_name()}' loc={loc} scale={scale} profile={col_prof}")

