import unreal

def log(msg):
    unreal.log_warning(f"[INSPECT_MOHALLA] {msg}")

log("================ INSPECTING L_MOHALLA_HOME ================")

level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
level_sub.load_level("/Game/Maps/L_Mohalla_Home")

actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = actor_sub.get_all_level_actors()

log(f"Total Actors in L_Mohalla_Home: {len(actors)}")

world = level_sub.get_current_level().get_world()
world_settings = world.get_world_settings()
log(f"WorldSettings DefaultGameMode: {world_settings.get_editor_property('default_game_mode')}")

player_starts = [a for a in actors if isinstance(a, unreal.PlayerStart)]
log(f"PlayerStart count: {len(player_starts)}")
for ps in player_starts:
    loc = ps.get_actor_location()
    rot = ps.get_actor_rotation()
    log(f"PlayerStart '{ps.get_actor_label()}': Location=({loc.x}, {loc.y}, {loc.z}), Rotation=({rot.pitch}, {rot.yaw}, {rot.roll})")

# Check for actors within 100cm of PlayerStart
for ps in player_starts:
    ps_loc = ps.get_actor_location()
    for a in actors:
        if a == ps:
            continue
        dist = (a.get_actor_location() - ps_loc).length()
        if dist < 120.0:
            log(f"NEARBY ACTOR to PlayerStart: {a.get_actor_label()} ({a.get_class().get_name()}) dist={dist:.1f} loc={a.get_actor_location()}")

# Check all actor classes
classes_count = {}
for a in actors:
    cname = a.get_class().get_name()
    classes_count[cname] = classes_count.get(cname, 0) + 1

for cname, count in sorted(classes_count.items()):
    log(f"Class {cname}: {count}")

log("================ INSPECTION COMPLETE ================")
