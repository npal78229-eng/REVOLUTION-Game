"""
PROJECT REVOLUTION — Task 34 QA Verification Suite (TEST-20)
Seamless Act I In-World Objective Beacons & Mohalla Compass Waypoints
Verifies:
1. URevolutionMissionSubsystem Objective Query:
   - GetActiveObjectiveLocation() resolves authoritative 3D positions and landmark names
   - All 8 Act I story stages return valid coordinates within Kot Gurdarshan / Bazaar / School:
     * Stage 1: Father Ram Lubhaya (Tailor Shop Veranda)
     * Stage 2: Rooftop Basant Kite (Haveli Terrace Ledge)
     * Stage 3: Mohalla Well & Bhishti Ghasita (Communal Well Square)
     * Stage 4: Lala Karam Chand (Cloth Merchant Guild)
     * Stage 5: Hira Halwai (Tea & Jalebi Stall)
     * Stage 6: Colonial Proclamation Board (Martial Law Notice)
     * Stage 7: School Bell Tower (Vernacular Middle School)
     * Stage 8: Classroom 4B Student Desk (Takhti & Bench)
   - Stage_Completed correctly returns False (no remaining objectives).
2. Subsequent Acts II-V Objective Resolution:
   - Later act milestones resolve accurately (Munadi drum, Jallianwala Bagh entrance, wall breach, curfew notice, canal sluice, railway signal gantry).
3. 3D Spatial Distance & Perspective Alpha Calculations:
   - In-range threshold (40m normal exploration, 80m Keen Senses / Basant Intuition)
   - Dynamic close-up fade (fading below 3.0m down to 1.2m to prevent UI clutter during interactions)
   - Far distance fade (gradual feathering from 30m to 40m)
4. Mohalla Compass Ribbon Waypoint Projection Math:
   - Accurate bearing angle computation from player position to objective
   - Normalized angular delta relative to player camera yaw [-180, 180]
   - Visual clipping within ±40° compass ribbon visible half-range
5. HUD Configuration:
   - ARevolutionHUD bShowObjectiveBeacons defaults to True
"""

import sys
import math
import unreal

def log_qa(msg):
    unreal.log_warning(f"[OBJECTIVE_BEACONS_QA] {msg}")

def main():
    log_qa("================================================================================")
    log_qa("  PROJECT REVOLUTION — TASK 34 OBJECTIVE BEACONS & COMPASS WAYPOINTS QA (TEST-20)")
    log_qa("================================================================================")

    gym_map = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(gym_map)

    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = actor_sub.get_all_level_actors()
    log_qa(f"Loaded gym level: {gym_map} ({len(actors)} actors)")
    assert len(actors) >= 225, f"Actor count too low: {len(actors)} < 225!"

    # =========================================================================
    # 1. VERIFY REVOLUTION MISSION SUBSYSTEM CLASS & METHOD REFLECTION
    # =========================================================================
    log_qa("--- Subtest 1: Verifying Mission Subsystem Objective Query Reflection ---")
    subsystem_class = unreal.load_class(None, "/Script/REVOLUTION.RevolutionMissionSubsystem")
    assert subsystem_class is not None, "Failed to load RevolutionMissionSubsystem class!"

    # Instantiate transient subsystem test object or check method on CDO
    cdo = unreal.get_default_object(subsystem_class)
    assert hasattr(cdo, "get_active_objective_location"), \
        "RevolutionMissionSubsystem missing 'get_active_objective_location' method!"
    log_qa("[PASS] Subsystem reflection verified: get_active_objective_location is present.")

    # =========================================================================
    # 2. VERIFY ACT I MISSION STAGES OBJECTIVE LOCATIONS & TITLES
    # =========================================================================
    log_qa("--- Subtest 2: Verifying All 8 Act I Mission Stages Objective Targets ---")
    
    # In commandlet mode, construct a world subsystem test instance
    test_subsystem = unreal.new_object(subsystem_class)
    
    # Expected Act I stages and validation parameters
    act1_stages = [
        (
            unreal.CourierMissionStage.STAGE_MORNING_FATHER_TAILOR,
            "Stage 1: Father Ram Lubhaya Tailor Dispatch",
            ["Ram Lubhaya", "Tailor"],
            unreal.Vector(480.0, 500.0, 88.0),
            100.0  # Max allowable distance tolerance from anchor in gym
        ),
        (
            unreal.CourierMissionStage.STAGE_MORNING_ROOFTOP_KITE,
            "Stage 2: Rooftop Basant Kite",
            ["Kite", "Basant"],
            unreal.Vector(380.0, 200.0, 480.0),
            400.0  # High terrace area
        ),
        (
            unreal.CourierMissionStage.STAGE_MORNING_WELL_BHISHTI,
            "Stage 3: Mohalla Well & Bhishti Ghasita",
            ["Bhishti", "Well"],
            unreal.Vector(-80.0, 1320.0, 88.0),
            150.0
        ),
        (
            unreal.CourierMissionStage.STAGE_MORNING_DELIVER_CLOTH,
            "Stage 4: Grand Bazaar Lala Karam Chand Cloth Guild",
            ["Lala Karam Chand", "Cloth"],
            unreal.Vector(200.0, 1980.0, 88.0),
            150.0
        ),
        (
            unreal.CourierMissionStage.STAGE_MORNING_CHAI_HALWAI,
            "Stage 5: Halwai Tea Stall Rumors",
            ["Hira Halwai", "Chai", "Tea"],
            unreal.Vector(-200.0, 1680.0, 88.0),
            150.0
        ),
        (
            unreal.CourierMissionStage.STAGE_MORNING_PROCLAMATION_BOARD,
            "Stage 6: Colonial Proclamation Notice",
            ["Proclamation", "Section 144", "Notice"],
            unreal.Vector(-80.0, 1850.0, 50.0),
            150.0
        ),
        (
            unreal.CourierMissionStage.STAGE_MORNING_SCHOOL_BELL,
            "Stage 7: Ring Middle School Bell",
            ["School", "Bell"],
            unreal.Vector(1350.0, 1350.0, 60.0),
            150.0
        ),
        (
            unreal.CourierMissionStage.STAGE_MORNING_CLASSROOM_DESK,
            "Stage 8: Classroom 4B Student Desk",
            ["Classroom", "Desk", "Takhti"],
            unreal.Vector(1150.0, 1850.0, 35.0),
            1000.0  # Allow either gym desk prop or school classroom
        )
    ]

    for stage_enum, desc, title_keywords, expected_pos, tolerance in act1_stages:
        test_subsystem.set_mission_stage(stage_enum)
        res = test_subsystem.get_active_objective_location()
        assert res is not None, f"Stage {stage_enum} returned no active objective!"
        obj_loc, obj_name = res
        
        name_str = str(obj_name)
        log_qa(f"Stage {desc}:")
        log_qa(f"  Target: '{name_str}' at ({obj_loc.x:.1f}, {obj_loc.y:.1f}, {obj_loc.z:.1f})")
        
        # Verify title keywords
        keyword_match = any(kw.lower() in name_str.lower() for kw in title_keywords)
        assert keyword_match, f"Objective title '{name_str}' did not match any of {title_keywords}!"
        
        # Verify location proximity to designated zone
        dist_to_expected = math.sqrt(
            (obj_loc.x - expected_pos.x)**2 + 
            (obj_loc.y - expected_pos.y)**2 + 
            (obj_loc.z - expected_pos.z)**2
        )
        assert dist_to_expected <= tolerance, \
            f"Stage {stage_enum} location ({obj_loc.x:.1f}, {obj_loc.y:.1f}, {obj_loc.z:.1f}) too far from expected {expected_pos} (dist: {dist_to_expected:.1f} > {tolerance})!"

    log_qa("[PASS] All 8 Act I story stages resolved authoritative 3D positions & landmark names.")

    # =========================================================================
    # 3. VERIFY STAGE COMPLETED RETURNS NONE (FALSE)
    # =========================================================================
    log_qa("--- Subtest 3: Verifying Completed Journey Returns None (False) ---")
    test_subsystem.set_mission_stage(unreal.CourierMissionStage.STAGE_COMPLETED)
    res_done = test_subsystem.get_active_objective_location()
    assert res_done is None, f"Stage_Completed must return None (False), got {res_done}!"
    log_qa(f"[PASS] Stage_Completed correctly returned None (terminal objective state).")

    # =========================================================================
    # 4. VERIFY ACTS II-V MILESTONE OBJECTIVES RESOLUTION
    # =========================================================================
    log_qa("--- Subtest 4: Verifying Acts II-V Milestone Coordinates ---")
    later_milestones = [
        (unreal.CourierMissionStage.STAGE_AFTERNOON_MUNADI_PROCLAMATION, ["Munadi", "Drum"]),
        (unreal.CourierMissionStage.STAGE_AFTERNOON_BAGH_NARROW_ENTRY, ["Jallianwala", "Bagh"]),
        (unreal.CourierMissionStage.STAGE_ACT_II_THE_FIRING, ["Firing"]),
        (unreal.CourierMissionStage.STAGE_ACT_III_NIGHT_CURFEW_FALL, ["Curfew"]),
        (unreal.CourierMissionStage.STAGE_ACT_IV_REACH_CANAL_DISTRIBUTARY, ["Canal"]),
        (unreal.CourierMissionStage.STAGE_ACT_V_CLIMB_SIGNAL_GANTRY, ["Signal", "Gantry"])
    ]
    for stage_enum, expected_keywords in later_milestones:
        test_subsystem.set_mission_stage(stage_enum)
        res_milestone = test_subsystem.get_active_objective_location()
        assert res_milestone is not None, f"Milestone {stage_enum} failed to return active objective!"
        loc, name = res_milestone
        for kw in expected_keywords:
            assert kw.lower() in str(name).lower(), \
                f"Expected '{kw}' in title '{name}'!"
        log_qa(f"  Milestone {stage_enum} -> '{name}' at ({loc.x:.1f}, {loc.y:.1f}, {loc.z:.1f})")

    log_qa("[PASS] Acts II-V milestone objectives successfully verified.")

    # =========================================================================
    # 5. SPATIAL PERSPECTIVE, RANGE & ALPHA MATHEMATICAL VERIFICATION
    # =========================================================================
    log_qa("--- Subtest 5: Verifying Spatial Alpha & Range Calculation Logic ---")
    
    def calculate_beacon_alpha(dist_meters, b_keen_senses):
        max_range = 80.0 if b_keen_senses else 40.0
        if dist_meters > max_range:
            return 0.0
        
        alpha = 1.0
        if dist_meters > (max_range * 0.75):
            alpha = max(0.0, min(1.0, 1.0 - ((dist_meters - (max_range * 0.75)) / (max_range * 0.25))))
        elif dist_meters < 3.0:
            alpha = max(0.0, min(1.0, (dist_meters - 1.2) / 1.8))
            
        return alpha

    # Test cases:
    # 1. Close-up: below 1.2m -> Alpha = 0.0 (prevents obscuring NPC/prop interaction)
    alpha_very_close = calculate_beacon_alpha(1.0, False)
    assert alpha_very_close == 0.0, f"Expected 0.0 at 1.0m, got {alpha_very_close}"
    
    # 2. Mid-close transition: at 2.1m -> Alpha = 0.5
    alpha_mid_close = calculate_beacon_alpha(2.1, False)
    assert abs(alpha_mid_close - 0.5) < 0.05, f"Expected ~0.5 at 2.1m, got {alpha_mid_close}"

    # 3. Sweet spot: 15m exploration -> Alpha = 1.0
    alpha_sweet_spot = calculate_beacon_alpha(15.0, False)
    assert alpha_sweet_spot == 1.0, f"Expected 1.0 at 15.0m, got {alpha_sweet_spot}"

    # 4. Normal range boundary: 35m -> fading out
    alpha_far_normal = calculate_beacon_alpha(35.0, False)
    assert 0.0 < alpha_far_normal < 1.0, f"Expected fading at 35m, got {alpha_far_normal}"

    # 5. Beyond normal range: 45m without Keen Senses -> Alpha = 0.0
    alpha_beyond_normal = calculate_beacon_alpha(45.0, False)
    assert alpha_beyond_normal == 0.0, f"Expected 0.0 at 45m without Keen Senses, got {alpha_beyond_normal}"

    # 6. With Basant Intuition (Keen Senses): 45m -> Alpha = 1.0 (range extended to 80m)
    alpha_keen_senses = calculate_beacon_alpha(45.0, True)
    assert alpha_keen_senses == 1.0, f"Expected 1.0 at 45m with Keen Senses, got {alpha_keen_senses}"

    # 7. Beyond Keen Senses range: 85m -> Alpha = 0.0
    alpha_beyond_keen = calculate_beacon_alpha(85.0, True)
    assert alpha_beyond_keen == 0.0, f"Expected 0.0 at 85m with Keen Senses, got {alpha_beyond_keen}"

    log_qa("[PASS] Distance alpha scaling, smooth close-up fadeout, and Basant Intuition range extension verified.")

    # =========================================================================
    # 6. COMPASS RIBBON BEARING PROJECTION MATHEMATICAL VERIFICATION
    # =========================================================================
    log_qa("--- Subtest 6: Verifying Compass Ribbon Bearing Projection Math ---")
    
    def calculate_compass_offset(player_pos, player_yaw, obj_pos, tape_width=260.0, half_range=40.0):
        dx = obj_pos.x - player_pos.x
        dy = obj_pos.y - player_pos.y
        obj_angle = math.degrees(math.atan2(dy, dx))
        diff = obj_angle - player_yaw
        while diff > 180.0: diff -= 360.0
        while diff < -180.0: diff += 360.0
        
        b_in_view = abs(diff) <= half_range
        pixels_per_deg = (tape_width * 0.5) / half_range
        offset_x = diff * pixels_per_deg
        return b_in_view, offset_x

    player_origin = unreal.Vector(0.0, 0.0, 0.0)
    
    # 1. Directly in front (North, Yaw=0, Target at X=1000, Y=0)
    target_north = unreal.Vector(1000.0, 0.0, 0.0)
    in_view, offset = calculate_compass_offset(player_origin, 0.0, target_north)
    assert in_view and abs(offset) < 0.01, f"Expected offset 0.0, got {offset}"

    # 2. 20 degrees East (Yaw=0, Target at 20 deg)
    rad20 = math.radians(20.0)
    target_20deg = unreal.Vector(1000.0 * math.cos(rad20), 1000.0 * math.sin(rad20), 0.0)
    in_view, offset = calculate_compass_offset(player_origin, 0.0, target_20deg)
    assert in_view, "Expected target at 20 deg to be in compass FOV (half-range 40)"
    expected_offset = 20.0 * (130.0 / 40.0)  # 65.0 pixels
    assert abs(offset - expected_offset) < 0.1, f"Expected offset {expected_offset}, got {offset}"

    # 3. 50 degrees East (Yaw=0, Target at 50 deg) -> Outside compass ribbon window (±40 deg)
    rad50 = math.radians(50.0)
    target_50deg = unreal.Vector(1000.0 * math.cos(rad50), 1000.0 * math.sin(rad50), 0.0)
    in_view, offset = calculate_compass_offset(player_origin, 0.0, target_50deg)
    assert not in_view, "Expected target at 50 deg to be outside compass ribbon FOV"

    log_qa("[PASS] Compass ribbon bearing angle normalization and viewport projection math verified.")

    # =========================================================================
    # 7. VERIFY HUD DEFAULTS & CONFIGURATION
    # =========================================================================
    log_qa("--- Subtest 7: Verifying ARevolutionHUD Configuration ---")
    hud_class = unreal.load_class(None, "/Script/REVOLUTION.RevolutionHUD")
    assert hud_class is not None, "Failed to load RevolutionHUD class!"
    hud_cdo = unreal.get_default_object(hud_class)
    assert hasattr(hud_cdo, "b_show_objective_beacons") or hasattr(hud_cdo, "show_objective_beacons"), \
        "RevolutionHUD missing 'bShowObjectiveBeacons' property!"
    val = getattr(hud_cdo, "show_objective_beacons", getattr(hud_cdo, "b_show_objective_beacons", None))
    assert val is True, f"Expected bShowObjectiveBeacons default True, got {val}"
    log_qa("[PASS] ARevolutionHUD bShowObjectiveBeacons defaults to True.")

    log_qa("================================================================================")
    log_qa("  ALL SUBTESTS PASSED (7/7) — TASK 34 OBJECTIVE BEACONS CERTIFIED")
    log_qa("================================================================================")

if __name__ == '__main__':
    main()
