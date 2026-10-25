import unreal

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Maps/L_Validation_Gym")
actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = actor_sub.get_all_level_actors()

constable = next((a for a in actors if a.get_actor_label() == "NPC_Constable_Gurdial"), None)
munadi = next((a for a in actors if a.get_actor_label() == "NPC_Munadi_TownCrier"), None)

if munadi:
    munadi.set_actor_location(unreal.Vector(115.0, 1920.0, 88.0), sweep=False, teleport=True)
    unreal.log_warning(f"Temporarily moved Munadi to {munadi.get_actor_location()}")

wps = constable.get_editor_property("patrol_waypoints")
unreal.log_warning(f"Testing patrol sweep along {len(wps)} waypoints...")

for i in range(1, len(wps)):
    start_wp = wps[i-1]
    target_wp = wps[i]
    to_target = target_wp - start_wp
    dist = to_target.length()
    steps = 15
    step_vec = to_target * (1.0 / float(steps))
    
    constable.set_actor_location(start_wp, sweep=False, teleport=True)
    blocked = False
    for step in range(1, steps + 1):
        next_loc = start_wp + step_vec * float(step)
        hit_res = constable.set_actor_location(next_loc, sweep=True, teleport=False)
        actual_loc = constable.get_actor_location()
        pos_err = (actual_loc - next_loc).length()
        if pos_err >= 5.0:
            unreal.log_warning(f"  [BLOCKED Segment {i-1}->{i} Step {step}/{steps}] Target: {next_loc}, Actual: {actual_loc}, Err: {pos_err:.2f}")
            unreal.log_warning(f"  Hit text: {hit_res.export_text()}")
            blocked = True
            break
    if not blocked:
        unreal.log_warning(f"  [PASS] Segment WP[{i-1}] -> WP[{i}] traversed cleanly ({steps} steps, 0 collisions)!")

