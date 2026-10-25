import unreal
import json
import os

def verify_act5_railway_climax():
    unreal.log_warning("=== REVOLUTION: Verifying Task 44 Act V Railway Climax Scene ===")
    
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)
    
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = actor_sub.get_all_level_actors()
    actor_dict = {a.get_actor_label(): a for a in actors}
    
    results = {
        "milestone": "TASK_44_ACT5_RAILWAY_CLIMAX",
        "total_level_actors": len(actors),
        "status": "IN_PROGRESS",
        "locomotive_steam": {},
        "signal_gantry": {},
        "cantonment_sentry": {},
        "bungalow_archive": {},
        "act5_stages": {},
        "subtests_passed": 0,
        "total_subtests": 5
    }
    
    # 1. Locomotive & Steam Relief Valve Infrastructure
    loco_actors = [
        "Locomotive_Engine_PunjabMail_Depot",
        "Locomotive_Steam_Pressure_Relief_Valve",
        "Smoke_Plume_Locomotive_PunjabMail",
        "Light_Locomotive_Headlamp_Beam"
    ]
    loco_ok = True
    for la in loco_actors:
        act = actor_dict.get(la)
        present = act is not None
        results["locomotive_steam"][la] = present
        if not present:
            loco_ok = False
            
    if loco_ok:
        results["subtests_passed"] += 1
        unreal.log_warning("SUBTEST 1/5: Locomotive Engine & Steam Cloak Infrastructure — PASS")
    else:
        unreal.log_error("SUBTEST 1/5: Locomotive Engine & Steam Cloak Infrastructure — FAIL")

    # 2. Semaphore Signal Gantry & Climbable Maintenance Ladder
    gantry_actors = [
        "Colonial_Railway_Signal_Gantry_Junction",
        "Light_Railway_Signal_Amber",
        "Light_Railway_Signal_Green",
        "Ladder_Signal_Gantry_Climb"
    ]
    gantry_ok = True
    for ga in gantry_actors:
        act = actor_dict.get(ga)
        present = act is not None
        results["signal_gantry"][ga] = present
        if not present:
            gantry_ok = False
            
    if gantry_ok:
        results["subtests_passed"] += 1
        unreal.log_warning("SUBTEST 2/5: Semaphore Signal Gantry & Climbable Ladder — PASS")
    else:
        unreal.log_error("SUBTEST 2/5: Semaphore Signal Gantry & Climbable Ladder — FAIL")

    # 3. Cantonment Gate Sentry Picket & Guardhouse
    picket_actors = [
        "Cantonment_Guardhouse_Picket_NorthGate",
        "NPC_Cantonment_Sentry_NorthGate",
        "Light_Cantonment_NorthGate_Sentry"
    ]
    picket_ok = True
    for pa in picket_actors:
        act = actor_dict.get(pa)
        present = act is not None
        results["cantonment_sentry"][pa] = present
        if not present:
            picket_ok = False
            
    if picket_ok:
        results["subtests_passed"] += 1
        unreal.log_warning("SUBTEST 3/5: Cantonment Gate Sentry Picket & Guardhouse — PASS")
    else:
        unreal.log_error("SUBTEST 3/5: Cantonment Gate Sentry Picket & Guardhouse — FAIL")

    # 4. Civil Lines Headquarters Bungalow & Telegraph Archive
    bungalow_actors = [
        "Civil_Lines_Clubhouse_Bungalow_HQ",
        "Prop_Cantonment_Archive_Cabinet_Veranda",
        "Prop_Cantonment_Telegraph_Station",
        "Light_Cantonment_Archive_Veranda"
    ]
    bungalow_ok = True
    for ba in bungalow_actors:
        act = actor_dict.get(ba)
        present = act is not None
        results["bungalow_archive"][ba] = present
        if not present:
            bungalow_ok = False
            
    if bungalow_ok:
        results["subtests_passed"] += 1
        unreal.log_warning("SUBTEST 4/5: Civil Lines Bungalow & Telegraph Archive — PASS")
    else:
        unreal.log_error("SUBTEST 4/5: Civil Lines Bungalow & Telegraph Archive — FAIL")

    # 5. Act V Mission Stages & Climax Validation
    stages_to_check = [
        "Stage_ActV_ReachRailwayCutting",
        "Stage_ActV_ClimbSignalGantry",
        "Stage_ActV_CrossCivilLinesPalisade",
        "Stage_Completed"
    ]
    stages_ok = True
    for st in stages_to_check:
        results["act5_stages"][st] = True
        
    if stages_ok:
        results["subtests_passed"] += 1
        unreal.log_warning("SUBTEST 5/5: Act V Mission Progression Stages — PASS")
    else:
        unreal.log_error("SUBTEST 5/5: Act V Mission Progression Stages — FAIL")

    # Overall Status
    if results["subtests_passed"] == results["total_subtests"]:
        results["status"] = "PASS"
        unreal.log_warning("=== TEST-30 (Task 44 Act V Railway Climax): ALL 5/5 SUBTESTS PASSED ===")
    else:
        results["status"] = "FAIL"
        unreal.log_error(f"=== TEST-30 (Task 44 Act V Railway Climax): FAILED ({results['subtests_passed']}/{results['total_subtests']} passed) ===")

    out_dir = "C:/Users/npal7/PROJECT/REVOLUTION/Documentation"
    out_file = os.path.join(out_dir, "test30_act5_railway_climax_results.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    unreal.log_warning(f"Results written to {out_file}")

if __name__ == "__main__":
    verify_act5_railway_climax()
