import unreal

def log(msg):
    unreal.log_warning(f"[CHECK_FLOORS] {msg}")

level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
level_sub.load_level("/Game/Maps/L_Mohalla_Home")

actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = actor_sub.get_all_level_actors()

floor_actors = []
for a in actors:
    if isinstance(a, unreal.StaticMeshActor):
        label = a.get_actor_label()
        loc = a.get_actor_location()
        smc = a.static_mesh_component
        mesh_name = smc.static_mesh.get_name() if (smc and smc.static_mesh) else ""
        if "Floor" in label or "Floor" in mesh_name or "Street" in label or "Ground" in label or "Cobble" in label or "Paving" in label or "Slab" in label:
            bounds = a.get_actor_bounds(False)
            floor_actors.append((label, mesh_name, loc, bounds))

log(f"Total floor/street actors found: {len(floor_actors)}")
for label, mesh_name, loc, (origin, extent) in floor_actors:
    log(f"Floor '{label}' [{mesh_name}] loc={loc} origin={origin} extent={extent}")

# Specifically check under (-800, 120)
under_spawn = []
for label, mesh_name, loc, (origin, extent) in floor_actors:
    min_x = origin.x - extent.x
    max_x = origin.x + extent.x
    min_y = origin.y - extent.y
    max_y = origin.y + extent.y
    if min_x <= -800 <= max_x and min_y <= 120 <= max_y:
        under_spawn.append((label, mesh_name, loc, origin.z + extent.z))

log(f"Floors directly containing (-800, 120): {len(under_spawn)}")
for label, mesh_name, loc, top_z in under_spawn:
    log(f"  --> MATCH: '{label}' top_z={top_z}")
