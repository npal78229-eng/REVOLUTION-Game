import unreal
import json
import os

def verify_act4_climax_brick_kiln():
    unreal.log_warning("=== REVOLUTION: Verifying Task 43 Act IV Brick Kiln Climax Scene ===")
    
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)
    
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = actor_sub.get_all_level_actors()
    actor_dict = {a.get_actor_label(): a for a in actors}
    
    results = {
        "milestone": "TASK_43_ACT4_CLIMAX_BRICK_KILN",
        "total_level_actors": len(actors),
        "status": "IN_PROGRESS",
        "kiln_structures": {},
        "smoke_plume": {},
        "kiln_lighting": {},
        "underground_press_props": {},
        "resistance_npc": {},
        "subtests_passed": 0,
        "total_subtests": 5
    }
    
    # 1. Bull's Trench Brick Kiln Conical Chimney
    chimney_label = "Industrial_Brick_Kiln_Bhatta_Chimney"
    act_chimney = actor_dict.get(chimney_label)
    chimney_ok = False
    if act_chimney:
        loc = act_chimney.get_actor_location()
        if abs(loc.x - (-1250.0)) < 10.0 and abs(loc.y - 2650.0) < 10.0:
            chimney_ok = True
    results["kiln_structures"][chimney_label] = chimney_ok
    if chimney_ok:
        results["subtests_passed"] += 1
        unreal.log_warning("SUBTEST 1/5: Bhatta Conical Chimney — PASS")
    else:
        unreal.log_error(f"SUBTEST 1/5: Bhatta Conical Chimney — FAIL (found={act_chimney is not None})")

    # 2. RDR2-Inspired Industrial Smoke Plume
    smoke_label = "Smoke_Plume_Bhatta_Kiln"
    act_smoke = actor_dict.get(smoke_label)
    smoke_ok = False
    if act_smoke:
        loc = act_smoke.get_actor_location()
        # Should be drafted at chimney top Z ~ 780
        if abs(loc.x - (-1250.0)) < 20.0 and abs(loc.y - 2650.0) < 20.0 and loc.z >= 750.0:
            sm_comp = act_smoke.get_component_by_class(unreal.StaticMeshComponent)
            if sm_comp:
                mat = sm_comp.get_material(0)
                mat_name = mat.get_name() if mat else ""
                smoke_ok = "Smoke" in mat_name or "Haveli" in mat_name or mat is not None
    results["smoke_plume"][smoke_label] = smoke_ok
    if smoke_ok:
        results["subtests_passed"] += 1
        unreal.log_warning("SUBTEST 2/5: RDR2 Industrial Smoke Plume at Chimney Top — PASS")
    else:
        unreal.log_error("SUBTEST 2/5: RDR2 Industrial Smoke Plume at Chimney Top — FAIL")

    # 3. Kiln Subterranean Flue Ember Fire Glow Light
    flue_light_label = "Light_Bhatta_Kiln_Flue_Glow"
    act_flue_light = actor_dict.get(flue_light_label)
    flue_ok = False
    if act_flue_light:
        comp = act_flue_light.get_component_by_class(unreal.PointLightComponent)
        if comp:
            intensity = comp.get_editor_property("intensity")
            radius = comp.get_editor_property("attenuation_radius")
            flue_ok = intensity >= 1500.0 and radius >= 300.0
    results["kiln_lighting"][flue_light_label] = flue_ok
    if flue_ok:
        results["subtests_passed"] += 1
        unreal.log_warning("SUBTEST 3/5: Subterranean Kiln Flue Fire Glow — PASS")
    else:
        unreal.log_error("SUBTEST 3/5: Subterranean Kiln Flue Fire Glow — FAIL")

    # 4. Underground Lithographic Printing Press & Clandestine Cache
    press_props = [
        "Story_Clandestine_Safehouse_Supply_Cache",
        "Prop_Safehouse_Handbill_Bundles",
        "Prop_Safehouse_Printing_Lantern",
        "Light_Safehouse_Printing_Lantern"
    ]
    press_ok = True
    for p in press_props:
        act = actor_dict.get(p)
        present = act is not None
        results["underground_press_props"][p] = present
        if not present:
            press_ok = False
    if press_ok:
        results["subtests_passed"] += 1
        unreal.log_warning("SUBTEST 4/5: Underground Printing Press & Handbill Cache — PASS")
    else:
        unreal.log_error("SUBTEST 4/5: Underground Printing Press & Handbill Cache — FAIL")

    # 5. Resistance Courier Contact NPC
    npc_label = "NPC_Resistance_Courier_Liaison"
    act_npc = actor_dict.get(npc_label)
    npc_ok = False
    if act_npc:
        loc = act_npc.get_actor_location()
        if abs(loc.x - (-1200.0)) < 50.0 and abs(loc.y - 2540.0) < 50.0:
            npc_ok = True
    results["resistance_npc"][npc_label] = npc_ok
    if npc_ok:
        results["subtests_passed"] += 1
        unreal.log_warning("SUBTEST 5/5: Resistance Courier Liaison NPC — PASS")
    else:
        unreal.log_error("SUBTEST 5/5: Resistance Courier Liaison NPC — FAIL")

    # Overall Status
    if results["subtests_passed"] == results["total_subtests"]:
        results["status"] = "PASS"
        unreal.log_warning("=== TEST-29 (Task 43 Act IV Brick Kiln Climax): ALL 5/5 SUBTESTS PASSED ===")
    else:
        results["status"] = "FAIL"
        unreal.log_error(f"=== TEST-29 (Task 43 Act IV Brick Kiln Climax): FAILED ({results['subtests_passed']}/{results['total_subtests']} passed) ===")

    out_dir = "C:/Users/npal7/PROJECT/REVOLUTION/Documentation"
    out_file = os.path.join(out_dir, "test29_act4_climax_brick_kiln_results.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    unreal.log_warning(f"Results written to {out_file}")

if __name__ == "__main__":
    verify_act4_climax_brick_kiln()
