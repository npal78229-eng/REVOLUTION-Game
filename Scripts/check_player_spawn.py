import unreal

def log(msg):
    unreal.log_warning(f"[CHECK_SPAWN] {msg}")

level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
level_sub.load_level("/Game/Maps/L_Mohalla_Home")

actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = actor_sub.get_all_level_actors()

# Find PlayerStart
ps = None
for a in actors:
    if isinstance(a, unreal.PlayerStart):
        ps = a
        break

if not ps:
    log("NO PLAYER START FOUND!")
else:
    ps_loc = ps.get_actor_location()
    log(f"PlayerStart location: {ps_loc}")

    # Find actors near PlayerStart within 500 units
    nearby = []
    for a in actors:
        if a == ps:
            continue
        dist = (a.get_actor_location() - ps_loc).length()
        if dist < 600.0:
            nearby.append((dist, a))

    nearby.sort(key=lambda x: x[0])
    log(f"Found {len(nearby)} actors within 600 units of PlayerStart:")
    for dist, a in nearby[:20]:
        log(f"  - [{dist:.1f} cm] {a.get_actor_label()} ({a.get_class().get_name()}) loc={a.get_actor_location()}")

# Check all StaticMeshActors near (-800, 120)
floor_candidates = []
for a in actors:
    if isinstance(a, unreal.StaticMeshActor):
        loc = a.get_actor_location()
        if abs(loc.x - (-800)) < 300 and abs(loc.y - 120) < 300:
            smc = a.static_mesh_component
            sm = smc.static_mesh if smc else None
            bounds = a.get_actor_bounds(False)
            floor_candidates.append((a.get_actor_label(), sm.get_name() if sm else "None", loc, bounds))

log(f"Direct overlapping floor/wall candidates around (-800, 120): {len(floor_candidates)}")
for label, sm_name, loc, (origin, box_extent) in floor_candidates:
    log(f"  * {label} [Mesh: {sm_name}] loc={loc} origin={origin} extent={box_extent}")
