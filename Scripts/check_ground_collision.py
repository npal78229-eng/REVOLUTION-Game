import unreal

def log(msg):
    unreal.log_warning(f"[CHECK_GROUND] {msg}")

level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
level_sub.load_level("/Game/Maps/L_Mohalla_Home")

actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = actor_sub.get_all_level_actors()

for a in actors:
    if a.get_actor_label() == "Ground_Dirt":
        smc = a.static_mesh_component
        log(f"Ground_Dirt StaticMesh: {smc.static_mesh.get_name() if smc.static_mesh else 'None'}")
        log(f"Ground_Dirt CollisionProfile: {smc.get_collision_profile_name()}")
        log(f"Ground_Dirt CollisionEnabled: {smc.get_collision_enabled()}")
        log(f"Ground_Dirt Mobility: {smc.mobility}")
        bounds = a.get_actor_bounds(False)
        log(f"Ground_Dirt bounds: origin={bounds[0]} extent={bounds[1]}")
        break

# Also check all actors with 'BlockAll' or blocking collision around spawn
log("Checking all actors near PlayerStart (-800, 120, 100) for overlapping collision:")
for a in actors:
    loc = a.get_actor_location()
    if abs(loc.x - (-800)) < 100 and abs(loc.y - 120) < 100:
        log(f"Actor at spawn: {a.get_actor_label()} ({a.get_class().get_name()}) loc={loc}")
