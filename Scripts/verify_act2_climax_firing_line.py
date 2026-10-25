import unreal
import json
import os

def verify_act2_climax_firing_line():
    unreal.log_warning("=== REVOLUTION: Verifying Task 40 Act II Climax Firing Line ===")
    
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)
    
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = actor_sub.get_all_level_actors()
    actor_dict = {a.get_actor_label(): a for a in actors}
    
    results = {
        "milestone": "TASK_40_ACT2_CLIMAX_FIRING_LINE",
        "total_level_actors": len(actors),
        "status": "IN_PROGRESS",
        "armored_cars": {},
        "firing_line_riflemen": {},
        "gunsmoke_plumes": {},
        "memorial_walls": {},
        "scatter_debris": {},
        "audio_assets": {},
        "traversal_breach": {},
        "subtests_passed": 0,
        "total_subtests": 7
    }
    
    # 1. Armored Cars blocking entrance
    car_north = actor_dict.get("British_Armored_Car_Obstacle_North")
    car_south = actor_dict.get("British_Armored_Car_Obstacle_South")
    results["armored_cars"]["North"] = car_north is not None
    results["armored_cars"]["South"] = car_south is not None
    if car_north and car_south:
        results["subtests_passed"] += 1
        unreal.log_warning("SUBTEST 1/7: Armored Cars blocking entrance — PASS")
    else:
        unreal.log_error("SUBTEST 1/7: Armored Cars blocking entrance — FAIL")
        
    # 2. Firing Line Riflemen & Dyer on Raised Bank
    riflemen = [
        "Picket_Rifleman_Alpha",
        "Picket_Rifleman_Bravo",
        "Picket_Rifleman_Charlie",
        "Picket_Rifleman_Delta",
        "Officer_GeneralDyer_Command"
    ]
    all_riflemen_ok = True
    for r in riflemen:
        act = actor_dict.get(r)
        present = act is not None
        results["firing_line_riflemen"][r] = present
        if not present:
            all_riflemen_ok = False
            
    if all_riflemen_ok:
        results["subtests_passed"] += 1
        unreal.log_warning("SUBTEST 2/7: British Riflemen on Raised Bank — PASS")
    else:
        unreal.log_error("SUBTEST 2/7: British Riflemen on Raised Bank — FAIL")
        
    # 3. Volumetric Gunsmoke Plumes (MI_Smoke_Gunpowder_Muzzle)
    smokes = [
        "Gunsmoke_Plume_RaisedBank_01",
        "Gunsmoke_Plume_RaisedBank_02",
        "Gunsmoke_Plume_RaisedBank_03"
    ]
    all_smokes_ok = True
    for s in smokes:
        act = actor_dict.get(s)
        present = act is not None
        results["gunsmoke_plumes"][s] = present
        if not present:
            all_smokes_ok = False
            
    if all_smokes_ok:
        results["subtests_passed"] += 1
        unreal.log_warning("SUBTEST 3/7: Volumetric Gunsmoke Plumes — PASS")
    else:
        unreal.log_error("SUBTEST 3/7: Volumetric Gunsmoke Plumes — FAIL")
        
    # 4. Bullet-Pocked Memorial Walls
    walls = [
        "Jallianwala_Bullet_Pocked_Wall_East",
        "Jallianwala_Bullet_Pocked_Wall_East_02",
        "Jallianwala_Bullet_Pocked_Wall_North"
    ]
    all_walls_ok = True
    for w in walls:
        act = actor_dict.get(w)
        present = act is not None
        results["memorial_walls"][w] = present
        if not present:
            all_walls_ok = False
            
    if all_walls_ok:
        results["subtests_passed"] += 1
        unreal.log_warning("SUBTEST 4/7: Bullet-Pocked Memorial Walls — PASS")
    else:
        unreal.log_error("SUBTEST 4/7: Bullet-Pocked Memorial Walls — FAIL")
        
    # 5. Scatter Debris (Turbans, Shoes, Pot Scatter)
    debris = [
        "Story_Panic_Debris_Scatter_Well",
        "Story_Panic_Debris_Scatter_Dais",
        "Story_Panic_Debris_Scatter_Breach",
        "Prop_Fallen_Turban_Scatter_WellApproach",
        "Prop_Fallen_Turban_Scatter_BreachApproach"
    ]
    all_debris_ok = True
    for d in debris:
        act = actor_dict.get(d)
        present = act is not None
        results["scatter_debris"][d] = present
        if not present:
            all_debris_ok = False
            
    if all_debris_ok:
        results["subtests_passed"] += 1
        unreal.log_warning("SUBTEST 5/7: Panic Scatter Debris — PASS")
    else:
        unreal.log_error("SUBTEST 5/7: Panic Scatter Debris — FAIL")
        
    # 6. Audio Asset Verification
    audio_tracks = [
        ("/Game/Audio/SFX/SFX_Bugle_Call_Charge", "BugleCall"),
        ("/Game/Audio/SFX/SFX_Crowd_Panic_Scream", "PanicScream"),
        ("/Game/Audio/SFX/SFX_Military_Boot_March", "BootMarch")
    ]
    all_audio_ok = True
    for path, name in audio_tracks:
        snd = unreal.load_asset(path)
        results["audio_assets"][name] = snd is not None
        if snd is None:
            all_audio_ok = False
            
    if all_audio_ok:
        results["subtests_passed"] += 1
        unreal.log_warning("SUBTEST 6/7: Historical Audio Assets — PASS")
    else:
        unreal.log_error("SUBTEST 6/7: Historical Audio Assets — FAIL")
        
    # 7. Crumbling Wall Breach Parkour Ledge
    breach = actor_dict.get("Jallianwala_Crumbling_Wall_Breach_West")
    results["traversal_breach"]["BreachPresent"] = breach is not None
    if breach:
        loc = breach.get_actor_location()
        results["traversal_breach"]["Location"] = f"X={loc.x:.1f}, Y={loc.y:.1f}, Z={loc.z:.1f}"
        results["subtests_passed"] += 1
        unreal.log_warning(f"SUBTEST 7/7: Crumbling Wall Breach at {results['traversal_breach']['Location']} — PASS")
    else:
        unreal.log_error("SUBTEST 7/7: Crumbling Wall Breach — FAIL")
        
    if results["subtests_passed"] == results["total_subtests"]:
        results["status"] = "PASS"
        unreal.log_warning(f"=== TASK 40 VERIFICATION COMPLETED: PASS ({results['subtests_passed']}/{results['total_subtests']} SUBTESTS) ===")
    else:
        results["status"] = "FAIL"
        unreal.log_error(f"=== TASK 40 VERIFICATION FAILED ({results['subtests_passed']}/{results['total_subtests']} SUBTESTS) ===")
        
    out_json = r"C:\Users\npal7\PROJECT\REVOLUTION\Tests\TASK_40_CLIMAX_VERIFICATION.json"
    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    with open(out_json, "w") as f:
        json.dump(results, f, indent=2)
    unreal.log_warning(f"Saved verification metrics to {out_json}")

if __name__ == "__main__":
    verify_act2_climax_firing_line()
