"""
PROJECT REVOLUTION — TEST-39: "Pehchan & Talashi" Colonial Interrogation & Persian Wheel Labor Verification Suite
Validates:
1. APersianWheelActor flume irrigation labor mechanic and +35 basti Vishwas reparation.
2. Sentry interrogation stop-and-challenge (ChallengerHalt -> SatchelSearch -> CleanPass).
3. Contraband satchel detection & curfew arrest escalation (Pamphlets > 0, unvouched).
4. Community-Trust Vouch defusal (Trusted cluster + nearby civilian prevents arrest).
5. Interrogation evasion flight detection and sentry alarm escalation.
"""

import os
import sys
import json
import time
import unreal

def log_qa(msg):
    unreal.log_warning(f"[PEHCHAN_TALASHI_QA] {msg}")

def run_all_tests():
    log_qa("================================================================================")
    log_qa("  TEST-39: PEHCHAN & TALASHI INTERROGATION & PERSIAN WHEEL LABOR VERIFICATION")
    log_qa("================================================================================")

    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)

    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    persian_wheel = None
    canal_door = None

    for a in actor_sub.get_all_level_actors():
        if a.get_actor_label() == "Rural_Persian_Wheel_Rahat_Canal":
            persian_wheel = a
        elif a.get_actor_label() == "Door_CanalBypass_Gate":
            canal_door = a

    assert persian_wheel is not None, "APersianWheelActor 'Rural_Persian_Wheel_Rahat_Canal' not found in gym!"
    assert canal_door is not None, "Door_CanalBypass_Gate not found in gym!"

    trust_sub = persian_wheel.get_community_trust_subsystem()
    if not trust_sub:
        subsystem_class = unreal.load_class(None, "/Script/REVOLUTION.CommunityTrustSubsystem")
        trust_sub = unreal.new_object(subsystem_class)

    results = {}

    # =========================================================================
    # SUBTEST 1: APersianWheelActor Flume Labor & Manual Reparation
    # =========================================================================
    log_qa("--- SUBTEST 1/5: APersianWheelActor Flume Labor & Basti Reparation ---")

    cluster_canal = unreal.Name("Cluster_UBDC_CanalBasti")
    assert persian_wheel.get_editor_property("community_cluster_id") == cluster_canal, "Persian wheel cluster ID mismatch!"
    assert persian_wheel.get_editor_property("labor_trust_bonus") == 35, "Persian wheel labor bonus mismatch!"

    # Register canal door with trust subsystem
    trust_sub.register_cluster_door(cluster_canal, canal_door)

    # Degrade cluster to Compromised
    trust_sub.set_cluster_stance(cluster_canal, unreal.CommunityStance.COMPROMISED)
    assert trust_sub.get_cluster_stance(cluster_canal) == unreal.CommunityStance.COMPROMISED, "Cluster should be Compromised!"
    assert canal_door.is_door_bolted(), "Canal bypass gate should be bolted when Compromised!"

    # Interact with Persian Wheel draught beam
    persian_wheel.reset_flume_state()
    persian_wheel.on_interact(None)

    assert persian_wheel.is_flume_cleared(), "Flume was not marked cleared after interaction!"
    score_after_labor = trust_sub.get_cluster_score(cluster_canal)
    log_qa(f"  After flume labor: Score={score_after_labor}, Stance={trust_sub.get_cluster_stance(cluster_canal)}")
    assert score_after_labor == 50, f"Expected score 50 after +35 labor bonus, got {score_after_labor}"
    assert trust_sub.get_cluster_stance(cluster_canal) == unreal.CommunityStance.NEUTRAL, "Stance should be restored to Neutral!"
    assert not canal_door.is_door_bolted(), "Canal bypass gate was not automatically unbolted!"

    log_qa("SUBTEST 1/5: PASS - APersianWheelActor flume labor restored basti trust and unbolted deorhi gate.")
    results["subtest_1_persian_wheel_labor"] = "PASS"

    # =========================================================================
    # SUBTEST 2: Pehchan & Talashi — Clean Satchel Pass (0 Contraband)
    # =========================================================================
    log_qa("--- SUBTEST 2/5: Pehchan & Talashi — Clean Satchel Pass ---")
    sentry_class = unreal.load_class(None, "/Script/REVOLUTION.CurfewPatrolAI")
    player_class = unreal.load_class(None, "/Script/REVOLUTION.RevolutionCharacter")

    sentry = actor_sub.spawn_actor_from_class(sentry_class, unreal.Vector(100.0, 0.0, 50.0))
    player = actor_sub.spawn_actor_from_class(player_class, unreal.Vector(250.0, 0.0, 50.0))

    sentry.set_confrontation_target(player)
    player.pamphlet_count = 0

    assert sentry.can_initiate_confrontation(player), "Sentry should be eligible to challenge player!"
    sentry.initiate_confrontation(player)

    assert sentry.get_confrontation_state() == unreal.CurfewConfrontationState.CHALLENGER_HALT, "Expected ChallengerHalt state!"
    log_qa("  Sentry initiated ChallengerHalt demand.")

    # Advance through halt (1.0s) to search
    sentry.update_confrontation(1.1)
    assert sentry.get_confrontation_state() == unreal.CurfewConfrontationState.SATCHEL_SEARCH, "Expected SatchelSearch state!"
    log_qa("  Sentry entered SatchelSearch.")

    # Advance through search duration (2.5s) with 0 pamphlets
    sentry.update_confrontation(2.6)
    assert sentry.get_confrontation_state() == unreal.CurfewConfrontationState.CLEAN_PASS, "Expected CleanPass state for empty satchel!"
    log_qa("  Sentry granted CleanPass.")

    # Advance through dismissal to resume patrol
    sentry.update_confrontation(1.1)
    assert sentry.get_confrontation_state() == unreal.CurfewConfrontationState.NONE, "Confrontation state should reset to None!"
    assert sentry.get_alert_state() == unreal.CurfewAlertState.UNAWARE, "Sentry alert should reset to Unaware!"

    log_qa("SUBTEST 2/5: PASS - Clean satchel inspection passed peacefully without curfew alarm.")
    results["subtest_2_clean_satchel_pass"] = "PASS"

    # =========================================================================
    # SUBTEST 3: Pehchan & Talashi — Contraband Satchel Arrest Escalation
    # =========================================================================
    log_qa("--- SUBTEST 3/5: Pehchan & Talashi — Contraband Satchel Arrest Escalation ---")
    sentry.reset_patrol_state()
    player.set_actor_location(unreal.Vector(250.0, 0.0, 50.0), False, False)
    sentry.set_confrontation_target(player)
    player.pamphlet_count = 4 # Carrying banned Satyagraha strike leaflets

    sentry.initiate_confrontation(player)
    sentry.update_confrontation(1.1) # Enter search
    assert sentry.get_confrontation_state() == unreal.CurfewConfrontationState.SATCHEL_SEARCH

    # Frisk duration completes with contraband
    sentry.update_confrontation(2.6)
    assert sentry.get_alert_state() == unreal.CurfewAlertState.ALERTED, "Sentry should escalate to Alerted upon finding leaflets!"
    log_qa("  Sentry detected leaflets: escalated to ALERTED and blew whistle!")

    # Verify incident history recorded penalty
    records = trust_sub.get_incident_history(unreal.Name("Cluster_KotGurdarshan_Bazaar"))
    has_seizure_incident = False
    for r in records:
        if r.incident_tag == unreal.Name("Incident_ContrabandSeizedByCurfew"):
            has_seizure_incident = True
            break
    log_qa(f"  Contraband seizure incident recorded: {has_seizure_incident}")
    assert has_seizure_incident, "Incident_ContrabandSeizedByCurfew not found in incident history!"

    log_qa("SUBTEST 3/5: PASS - Contraband leaflets correctly triggered arrest escalation and whistle.")
    results["subtest_3_contraband_escalation"] = "PASS"

    # =========================================================================
    # SUBTEST 4: Pehchan & Talashi — Community Vouch Protection (Trusted Cluster)
    # =========================================================================
    log_qa("--- SUBTEST 4/5: Pehchan & Talashi — Community Vouch Protection ---")
    sentry.reset_patrol_state()
    player.set_actor_location(unreal.Vector(250.0, 0.0, 50.0), False, False)
    sentry.set_confrontation_target(player)
    player.pamphlet_count = 3 # Contraband present!

    cluster_bazaar = unreal.Name("Cluster_KotGurdarshan_Bazaar")
    trust_sub.set_cluster_stance(cluster_bazaar, unreal.CommunityStance.TRUSTED) # Elevated to Trusted!
    assert trust_sub.get_cluster_stance(cluster_bazaar) == unreal.CommunityStance.TRUSTED

    civ_class = unreal.load_class(None, "/Script/REVOLUTION.CivilianNPCActor")
    civ = actor_sub.spawn_actor_from_class(civ_class, unreal.Vector(320.0, 100.0, 50.0))
    civ.set_editor_property("community_cluster_id", cluster_bazaar)

    sentry.initiate_confrontation(player)
    sentry.update_confrontation(1.1) # Enter search

    # Update confrontation during search with trusted civilian nearby
    sentry.update_confrontation(0.2)
    assert sentry.get_confrontation_state() == unreal.CurfewConfrontationState.COMMUNITY_VOUCH, "Civilian should have vouched for Kabir!"
    log_qa(f"  Civilian successfully delivered protective vouch: '{sentry.get_editor_property('last_confrontation_reason')}'")

    # Sentry listens to vouch (1.2s) and accepts alibi
    sentry.update_confrontation(1.3)
    assert sentry.get_confrontation_state() == unreal.CurfewConfrontationState.CLEAN_PASS, "Sentry should accept civilian alibi and transition to CleanPass!"

    log_qa("SUBTEST 4/5: PASS - Community vouch successfully protected Kabir from contraband arrest.")
    results["subtest_4_community_vouch_protection"] = "PASS"

    # =========================================================================
    # SUBTEST 5: Pehchan & Talashi — Interrogation Evasion Flight Escalation
    # =========================================================================
    log_qa("--- SUBTEST 5/5: Pehchan & Talashi — Interrogation Evasion Flight Escalation ---")
    sentry.reset_patrol_state()
    player.set_actor_location(unreal.Vector(200.0, 0.0, 50.0), False, False)
    sentry.set_confrontation_target(player)
    sentry.initiate_confrontation(player)
    assert sentry.get_confrontation_state() == unreal.CurfewConfrontationState.CHALLENGER_HALT

    # Kabir breaks away and flees outside confrontation radius
    player.set_actor_location(unreal.Vector(750.0, 0.0, 50.0), False, False)
    sentry.update_confrontation(0.1)

    assert sentry.get_alert_state() == unreal.CurfewAlertState.ALERTED, "Fleeing during interrogation must immediately trigger Alerted!"
    log_qa("  Sentry raised immediate alarm upon Kabir breaking away during interrogation.")

    log_qa("SUBTEST 5/5: PASS - Evasion flight correctly escalated sentry to pursuit.")
    results["subtest_5_evasion_flight_escalation"] = "PASS"

    # Clean up test actors
    actor_sub.destroy_actor(sentry)
    actor_sub.destroy_actor(player)
    actor_sub.destroy_actor(civ)

    # Save summary
    audit_file = "C:/Users/npal7/PROJECT/REVOLUTION/Tests/TASK_39_PEHCHAN_TALASHI_VERIFICATION.json"
    audit_data = {
        "suite": "TEST-39",
        "name": "Pehchan & Talashi Interrogation & Persian Wheel Labor Verification",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "status": "PASS",
        "subtests": results
    }
    with open(audit_file, "w", encoding="utf-8") as f:
        json.dump(audit_data, f, indent=2)

    log_qa("================================================================================")
    log_qa("  TEST-39 RESULT: 5 / 5 SUBTESTS PASSED (100% QA CERTIFICATION)")
    log_qa(f"  Audit saved: {audit_file}")
    log_qa("================================================================================")
    return True

if __name__ == "__main__":
    success = run_all_tests()
    if not success:
        sys.exit(1)
