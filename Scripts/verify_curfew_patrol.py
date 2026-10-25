"""
PROJECT REVOLUTION — Task 28 Verification Suite: Curfew Sentry AI Collision Resolution & Patrol Path Restoration
Validates:
1. Master Map L_Validation_Gym loading and actor persistence (>= 209 actors)
2. NPC_Constable_Gurdial (ACurfewPatrolAI) presence, upright capsule orientation (Pitch=0, Roll=0)
3. Safe collision clearance from Modular_Mohalla_CommunalWell (StaticMeshActor_49) (>300cm clearance)
4. Multi-waypoint patrol configuration (3 waypoints along Grand Bazaar corridor)
5. Kerosene hurricane lantern components (StaticMesh, PointLight, SpotLight)
6. Perception and alert state machine interfaces
"""

import sys
import unreal

def log_qa(msg):
    unreal.log_warning(f"[CURFEW_AI_QA] {msg}")

def run_curfew_ai_verification():
    log_qa("================================================================================")
    log_qa("  PROJECT REVOLUTION — TASK 28 CURFEW SENTRY PATROL AI QA SUITE")
    log_qa("================================================================================")

    # 1. Load Master Level
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    level_sub.load_level(level_path)
    all_actors = actor_sub.get_all_level_actors()
    log_qa(f"Total Level Actors in Scene: {len(all_actors)}")
    assert len(all_actors) >= 209, f"Actor count below 209 threshold: {len(all_actors)}"

    # 2. Verify Sentry Actor Presence
    constable = next((a for a in all_actors if a.get_actor_label() == "NPC_Constable_Gurdial"), None)
    assert constable is not None, "NPC_Constable_Gurdial missing from level!"
    log_qa(f"[PASS] NPC_Constable_Gurdial found in gym: {constable.get_name()}")

    # 3. Verify Upright Capsule Orientation
    rot = constable.get_actor_rotation()
    log_qa(f"  Constable Orientation: Pitch={rot.pitch:.2f}, Yaw={rot.yaw:.2f}, Roll={rot.roll:.2f}")
    assert abs(rot.pitch) < 1.0, f"Constable has non-zero pitch: {rot.pitch}!"
    assert abs(rot.roll) < 1.0, f"Constable has non-zero roll: {rot.roll}!"
    log_qa("[PASS] Upright orientation verified (Pitch=0.0, Roll=0.0).")

    # 4. Verify Well Collision Clearance
    well = next((a for a in all_actors if a.get_actor_label() == "Modular_Mohalla_CommunalWell"), None)
    assert well is not None, "Modular_Mohalla_CommunalWell missing from level!"
    well_rot = well.get_actor_rotation()
    log_qa(f"  Well Orientation: Pitch={well_rot.pitch:.2f}, Yaw={well_rot.yaw:.2f}, Roll={well_rot.roll:.2f}")
    assert abs(well_rot.pitch) < 1.0, f"Well has non-zero pitch: {well_rot.pitch}!"

    dist_to_well = (constable.get_actor_location() - well.get_actor_location()).length()
    log_qa(f"  Distance from Constable to Communal Well: {dist_to_well:.2f} cm")
    assert dist_to_well > 300.0, f"Constable too close to well: {dist_to_well} cm!"
    log_qa("[PASS] Safe clearance from Communal Well verified (> 300cm).")

    # 5. Verify Multi-Waypoint Patrol Routine
    wps = constable.get_editor_property("patrol_waypoints")
    log_qa(f"  Configured Patrol Waypoints: {len(wps)}")
    assert len(wps) >= 3, f"Expected at least 3 waypoints, found {len(wps)}!"
    for i, wp in enumerate(wps):
        log_qa(f"    Waypoint[{i}]: ({wp.x:.1f}, {wp.y:.1f}, {wp.z:.1f})")
    assert wps[0].y < wps[1].y < wps[2].y, "Waypoints do not advance along bazaar corridor (+Y)!"
    log_qa("[PASS] Multi-waypoint patrol routine verified along Grand Bazaar.")

    # 6. Verify Lantern Components
    lantern_mesh = constable.get_component_by_class(unreal.StaticMeshComponent)
    assert lantern_mesh is not None, "Lantern mesh component missing!"
    point_light = constable.get_component_by_class(unreal.PointLightComponent)
    assert point_light is not None, "Lantern PointLightComponent missing!"
    spot_light = constable.get_component_by_class(unreal.SpotLightComponent)
    assert spot_light is not None, "Lantern SpotLightComponent (forward beam) missing!"
    log_qa(f"[PASS] Kerosene lantern components verified: Mesh={lantern_mesh.get_name()}, Ambient={point_light.get_name()}, Beam={spot_light.get_name()}")

    # 7. Verify C++ Perception & Alert State Interfaces
    required_methods = [
        "can_see_player",
        "get_detection_percentage",
        "get_alert_state",
        "investigate_sound_location",
        "reset_patrol_state",
        "is_lantern_flickering"
    ]
    for m in required_methods:
        assert hasattr(constable, m), f"CurfewPatrolAI missing method '{m}'!"
        log_qa(f"  [UFUNCTION VERIFIED] {m}")

    # 8. Verify StaticMeshActor_128 (Bazaar Canopy) and Perimeter Barrier Collision Resolution
    canopy_128 = next((a for a in all_actors if a.get_name() == "StaticMeshActor_128" or a.get_actor_label() == "Bazaar_Canopy_Khadi_SouthEast"), None)
    if canopy_128:
        comp = canopy_128.get_component_by_class(unreal.StaticMeshComponent)
        col_name = str(comp.get_collision_profile_name()) if comp else "None"
        col_enabled = comp.get_collision_enabled() if comp else None
        log_qa(f"  StaticMeshActor_128 collision: Profile={col_name}, Enabled={col_enabled}")
        assert col_name == "NoCollision" or col_enabled == unreal.CollisionEnabled.NO_COLLISION, \
            f"StaticMeshActor_128 still has blocking collision: {col_name} / {col_enabled}!"
        log_qa("[PASS] StaticMeshActor_128 awning collision cleared (NoCollision).")

    barrier_200 = next((a for a in all_actors if a.get_actor_label() == "Boundary_Barrier_NorthGate_West"), None)
    if barrier_200:
        b_bounds = barrier_200.get_actor_bounds(False)
        origin, extent = b_bounds[0], b_bounds[1]
        log_qa(f"  Boundary_Barrier_NorthGate_West bounds: Origin={origin}, Extent={extent}")
        # Verify barrier does not overlap patrol corridor Y in [1650, 2050]
        barrier_min_y = origin.y - extent.y
        assert barrier_min_y > 2050.0, f"Boundary_Barrier_NorthGate_West reaches into patrol corridor at Y={barrier_min_y:.1f}!"
        log_qa(f"[PASS] Boundary_Barrier_NorthGate_West clearance verified (South edge at Y={barrier_min_y:.1f} > 2050).")

    # 9. Verify Patrol Route Traversal & Runtime Movement Sweep
    log_qa("--- Verifying Patrol Route Traversal & Capsule Movement Sweeps ---")
    
    # Store initial position to restore after test
    initial_loc = constable.get_actor_location()
    
    for i in range(1, len(wps)):
        start_wp = wps[i-1]
        target_wp = wps[i]
        to_target = target_wp - start_wp
        dist = to_target.length()
        assert dist > 100.0, f"Waypoints [{i-1}] and [{i}] are too close together ({dist:.1f} cm)!"
        
        # Reset sentry to segment start
        constable.set_actor_location(start_wp, sweep=False, teleport=True)
        
        # Step through segment using real engine collision sweep
        steps = 15
        step_vec = to_target * (1.0 / float(steps))
        for step in range(1, steps + 1):
            next_loc = start_wp + step_vec * float(step)
            # Perform sweep movement with Constable's actual character capsule
            sweep_hit = constable.set_actor_location(next_loc, sweep=True, teleport=False)
            
            # Verify the sentry arrived within tolerance and was not blocked
            actual_loc = constable.get_actor_location()
            pos_err = (actual_loc - next_loc).length()
            if pos_err >= 5.0:
                log_qa(f"  [BLOCKED STEP {step}/{steps}] Target: {next_loc}, Actual: {actual_loc}, Err: {pos_err:.2f}")
                assert pos_err < 5.0, f"Patrol movement blocked along WP[{i-1}] -> WP[{i}] at step {step}/{steps}! Blocked at {actual_loc}, target {next_loc}"

        log_qa(f"  [PASS] Segment WP[{i-1}] -> WP[{i}] runtime capsule sweep traversal verified ({dist:.1f} cm, {steps} steps, 0 collisions).")

    # Restore sentinel to original position
    constable.set_actor_location(initial_loc, sweep=False, teleport=True)

    log_qa("================================================================================")
    log_qa("  TASK 28 CURFEW SENTRY PATROL AI RESULT: 100% PASS (0 ERRORS)")
    log_qa("================================================================================")
    return True

if __name__ == "__main__":
    success = run_curfew_ai_verification()
    if not success:
        sys.exit(1)
    sys.exit(0)
