"""
PROJECT REVOLUTION — Task 39 QA Verification Suite:
Localized Community-Trust System ("Izzat & Vishwas")
Asserts:
1. UCommunityTrustSubsystem:
   - Subsystem initializes with canonical clusters: Cluster_UBDC_CanalBasti, Cluster_KotGurdarshan_Bazaar, Cluster_Bhatta_BrickKiln
   - Default stance is Neutral (Numerical score = 50)
2. ADoorDeorhiActor Community Trust Barricade Mechanics:
   - Door registered with Cluster_UBDC_CanalBasti
   - Compromised stance automatically drops iron slide-bolt (bIsBolted = True)
   - Trusted stance automatically unbolts door (bIsBolted = False)
3. ACivilianNPCActor Diegetic Dialogue & Bark Synchronization:
   - Synchronizes stance with cluster
   - In Compromised state, delivers authentic period rejection / scolding bark
   - In Trusted state, delivers conspiratorial sheltering / assistance bark
4. Incident Perception & Dynamic Stance Transition:
   - RecordIncident with negative trust delta degrades score and transitions Neutral -> Cautious -> Compromised
   - Automatic propagation to all registered doors and NPCs in the cluster
5. Persistent Disk Save/Load Serialization:
   - WriteToSaveGame serializes cluster stances and scores into URevolutionSaveGame
   - PopulateFromSaveGame cleanly restores cluster stances upon load
"""

import sys
import json
import unreal

def log_warn(msg):
    unreal.log_warning(f"[COMMUNITY_TRUST_QA] {msg}")

def log_err(msg):
    unreal.log_error(f"[COMMUNITY_TRUST_QA] {msg}")

def main():
    log_warn("================================================================================")
    log_warn("  PROJECT REVOLUTION — TASK 39 COMMUNITY-TRUST ('IZZAT & VISHWAS') QA AUDIT")
    log_warn("================================================================================")

    results = {
        "suite": "TEST-31_COMMUNITY_TRUST",
        "subtests_passed": 0,
        "total_subtests": 5,
        "details": {}
    }

    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    level_sub.load_level(level_path)

    # 1. Subtest 1: UCommunityTrustSubsystem Initialization & Canonical Clusters
    log_warn("--- SUBTEST 1/5: Community Trust Subsystem & Canonical Clusters ---")
    subsystem_class = unreal.load_class(None, "/Script/REVOLUTION.CommunityTrustSubsystem")
    assert subsystem_class is not None, "CommunityTrustSubsystem class missing!"
    trust_subsystem = unreal.new_object(subsystem_class)
    assert trust_subsystem is not None, "Failed to instantiate CommunityTrustSubsystem!"

    canonical_clusters = [
        unreal.Name("Cluster_UBDC_CanalBasti"),
        unreal.Name("Cluster_KotGurdarshan_Bazaar"),
        unreal.Name("Cluster_Bhatta_BrickKiln")
    ]

    for cluster_id in canonical_clusters:
        stance = trust_subsystem.get_cluster_stance(cluster_id)
        score = trust_subsystem.get_cluster_score(cluster_id)
        log_warn(f"  Cluster '{cluster_id}': Stance={stance}, Score={score}")
        assert stance == unreal.CommunityStance.NEUTRAL, f"Expected NEUTRAL stance for {cluster_id}, got {stance}"
        assert score == 50, f"Expected initial score 50 for {cluster_id}, got {score}"

    results["subtests_passed"] += 1
    results["details"]["subtest1_initialization"] = "PASS"
    log_warn("SUBTEST 1/5: PASS — Canonical clusters initialized with Neutral stance (Score 50).")

    # 2. Subtest 2: ADoorDeorhiActor Community Barricade Mechanics
    log_warn("--- SUBTEST 2/5: ADoorDeorhiActor Barricade Mechanics ---")
    test_cluster = unreal.Name("Cluster_UBDC_CanalBasti")
    
    # Spawn a test Deorhi door actor
    door_class = unreal.load_class(None, "/Script/REVOLUTION.DoorDeorhiActor")
    assert door_class is not None, "DoorDeorhiActor class missing!"
    
    door_loc = unreal.Vector(-950.0, 2250.0, 50.0)
    door_rot = unreal.Rotator(0.0, 0.0, 0.0)
    test_door = actor_sub.spawn_actor_from_class(door_class, door_loc, door_rot)
    assert test_door is not None, "Failed to spawn test DoorDeorhiActor!"

    test_door.set_editor_property("community_cluster_id", test_cluster)
    trust_subsystem.register_cluster_door(test_cluster, test_door)

    # Test Compromised state -> must bolt door
    test_door.apply_community_stance(unreal.CommunityStance.COMPROMISED)
    assert test_door.is_door_bolted() == True, "Door failed to bolt on COMPROMISED stance!"
    assert test_door.is_door_open() == False, "Door remained open when bolted!"
    log_warn("  [PASS] Compromised stance successfully threw iron kundi bolt.")

    # Test Trusted state -> must unbolt door
    test_door.apply_community_stance(unreal.CommunityStance.TRUSTED)
    assert test_door.is_door_bolted() == False, "Door failed to unbolt on TRUSTED stance!"
    log_warn("  [PASS] Trusted stance successfully unbolted door.")

    results["subtests_passed"] += 1
    results["details"]["subtest2_door_barricade"] = "PASS"
    log_warn("SUBTEST 2/5: PASS — ADoorDeorhiActor correctly responds to community trust stances.")

    # 3. Subtest 3: ACivilianNPCActor Dialogue & Bark Synchronization
    log_warn("--- SUBTEST 3/5: ACivilianNPCActor Dialogue & Bark Selection ---")
    civ_class = unreal.load_class(None, "/Script/REVOLUTION.CivilianNPCActor")
    assert civ_class is not None, "CivilianNPCActor class missing!"

    civ_loc = unreal.Vector(-1150.0, 2050.0, 0.0)
    test_civ = actor_sub.spawn_actor_from_class(civ_class, civ_loc, door_rot)
    assert test_civ is not None, "Failed to spawn test CivilianNPCActor!"

    test_civ.set_editor_property("community_cluster_id", test_cluster)
    test_civ.configure_occupation(unreal.CivilianOccupation.BHISHTI_WATER_CARRIER)
    trust_subsystem.register_cluster_civilian(test_cluster, test_civ)

    # Test Compromised stance dialogue
    test_civ.on_community_stance_changed(test_cluster, unreal.CommunityStance.COMPROMISED)
    compromised_dialogue = str(test_civ.get_current_dialogue())
    log_warn(f"  Compromised dialogue returned: '{compromised_dialogue}'")
    assert "Bhaag" in compromised_dialogue or "rifles" in compromised_dialogue or "leaflets" in compromised_dialogue, \
        f"Unexpected dialogue in Compromised state: {compromised_dialogue}"

    # Test Trusted stance dialogue
    test_civ.on_community_stance_changed(test_cluster, unreal.CommunityStance.TRUSTED)
    trusted_dialogue = str(test_civ.get_current_dialogue())
    log_warn(f"  Trusted dialogue returned: '{trusted_dialogue}'")
    assert "shadows" in trusted_dialogue or "unlatched" in trusted_dialogue or "Vande Mataram" in trusted_dialogue, \
        f"Unexpected dialogue in Trusted state: {trusted_dialogue}"

    results["subtests_passed"] += 1
    results["details"]["subtest3_civilian_barks"] = "PASS"
    log_warn("SUBTEST 3/5: PASS — ACivilianNPCActor dialogue barks correctly synchronized.")

    # 4. Subtest 4: Incident Perception & Dynamic Stance Transition
    log_warn("--- SUBTEST 4/5: Incident Perception & Dynamic Degradation ---")
    trust_subsystem.reset_cluster_to_default(test_cluster)
    assert trust_subsystem.get_cluster_stance(test_cluster) == unreal.CommunityStance.NEUTRAL

    # Log incident: Terracotta pots destroyed (-35 penalty)
    trust_subsystem.record_incident(
        test_cluster,
        unreal.Name("Incident_TerracottaDestroyed"),
        test_civ,
        test_door,
        -35
    )

    new_score = trust_subsystem.get_cluster_score(test_cluster)
    new_stance = trust_subsystem.get_cluster_stance(test_cluster)
    log_warn(f"  After incident: Score={new_score}, Stance={new_stance}")
    assert new_score == 15, f"Expected score 15 (50 - 35), got {new_score}"
    assert new_stance == unreal.CommunityStance.COMPROMISED, f"Expected COMPROMISED stance, got {new_stance}"

    # Verify automatic propagation to door
    assert test_door.is_door_bolted() == True, "Door was not automatically bolted via incident propagation!"

    # Verify incident history
    history = trust_subsystem.get_incident_history(test_cluster)
    assert len(history) >= 1, "Incident was not recorded in history!"
    log_warn(f"  Incident history verified: {len(history)} record(s).")

    # Active Restitution Redemption Simulation
    restitution_class = unreal.load_class(None, "/Script/REVOLUTION.RestitutionDropActor")
    assert restitution_class is not None, "RestitutionDropActor class missing!"
    rest_actor = actor_sub.spawn_actor_from_class(restitution_class, unreal.Vector(-1030.0, 2190.0, 35.0), unreal.Rotator(0, 0, 0))
    assert rest_actor is not None, "Failed to spawn RestitutionDropActor!"
    rest_actor.set_editor_property("community_cluster_id", test_cluster)
    rest_actor.set_editor_property("restitution_trust_bonus", 35)

    # Kabir deposits 2 copper annas on potter's bench
    bonus = rest_actor.get_editor_property("restitution_trust_bonus")
    trust_subsystem.adjust_cluster_score(test_cluster, bonus, unreal.Name("Restitution_Reparation_Paid"), test_civ)
    try:
        rest_actor.set_editor_property("has_been_paid", True)
    except Exception:
        pass
    rest_actor.on_interact(None)

    restituted_score = trust_subsystem.get_cluster_score(test_cluster)
    restituted_stance = trust_subsystem.get_cluster_stance(test_cluster)
    log_warn(f"  After active restitution paid: Score={restituted_score}, Stance={restituted_stance}")
    assert restituted_score == 50, f"Expected restored score 50 (15 + 35), got {restituted_score}"
    assert restituted_stance == unreal.CommunityStance.NEUTRAL, f"Expected NEUTRAL stance after restitution, got {restituted_stance}"
    assert test_door.is_door_bolted() == False, "Door was not unbolted after restitution!"
    actor_sub.destroy_actor(rest_actor)

    # 4. Coordinate-based Cluster Resolution & Extended Incidents
    canal_loc_cluster = trust_subsystem.get_cluster_at_location(unreal.Vector(-1020.0, 2180.0, 0.0))
    kiln_loc_cluster = trust_subsystem.get_cluster_at_location(unreal.Vector(-1200.0, 2540.0, 0.0))
    bazaar_loc_cluster = trust_subsystem.get_cluster_at_location(unreal.Vector(200.0, 1980.0, 0.0))
    assert canal_loc_cluster == unreal.Name("Cluster_UBDC_CanalBasti"), f"Expected Cluster_UBDC_CanalBasti, got {canal_loc_cluster}"
    assert kiln_loc_cluster == unreal.Name("Cluster_Bhatta_BrickKiln"), f"Expected Cluster_Bhatta_BrickKiln, got {kiln_loc_cluster}"
    assert bazaar_loc_cluster == unreal.Name("Cluster_KotGurdarshan_Bazaar"), f"Expected Cluster_KotGurdarshan_Bazaar, got {bazaar_loc_cluster}"
    log_warn("  [PASS] Dynamic coordinate-based cluster resolution verified across all 3 zones.")

    # Re-apply compromised state for Subtest 5 save/load verification
    trust_subsystem.set_cluster_stance(test_cluster, unreal.CommunityStance.COMPROMISED)

    results["subtests_passed"] += 1
    results["details"]["subtest4_incident_degradation"] = "PASS"
    log_warn("SUBTEST 4/5: PASS — Incident recording, score degradation, and propagation verified.")

    # 5. Subtest 5: Persistent Disk Save/Load Serialization
    log_warn("--- SUBTEST 5/5: Disk Save/Load Persistence Verification ---")
    save_game_class = unreal.load_class(None, "/Script/REVOLUTION.RevolutionSaveGame")
    assert save_game_class is not None, "RevolutionSaveGame class missing!"

    save_obj = unreal.GameplayStatics.create_save_game_object(save_game_class)
    assert save_obj is not None, "Failed to create save game object!"

    # Commit state to save game object
    trust_subsystem.write_to_save_game(save_obj)
    stances_map = save_obj.get_editor_property("community_stances")
    scores_map = save_obj.get_editor_property("community_trust_scores")

    assert test_cluster in stances_map, f"Cluster {test_cluster} missing in serialized stances!"
    assert stances_map[test_cluster] == 3, f"Expected serialized stance 3 (Compromised), got {stances_map[test_cluster]}"
    assert scores_map[test_cluster] == 15, f"Expected serialized score 15, got {scores_map[test_cluster]}"
    log_warn(f"  Serialized accurately: Stance={stances_map[test_cluster]}, Score={scores_map[test_cluster]}")

    # Write to DISK via GameplayStatics
    test_slot = "QA_CommunityTrust_DiskTest"
    b_saved_disk = unreal.GameplayStatics.save_game_to_slot(save_obj, test_slot, 0)
    assert b_saved_disk, f"Failed to commit save game to physical disk for slot '{test_slot}'!"
    assert unreal.GameplayStatics.does_save_game_exist(test_slot, 0), f"Slot '{test_slot}' does not exist on disk after save!"
    log_warn(f"  [PASS] Verified physical disk commitment for slot '{test_slot}'.")

    # Reset in-memory cluster to Neutral
    trust_subsystem.reset_cluster_to_default(test_cluster)
    assert trust_subsystem.get_cluster_stance(test_cluster) == unreal.CommunityStance.NEUTRAL
    assert trust_subsystem.get_cluster_score(test_cluster) == 50

    # Load from DISK via GameplayStatics
    loaded_obj = unreal.GameplayStatics.load_game_from_slot(test_slot, 0)
    assert loaded_obj is not None, f"Failed to deserialize save game from physical disk for slot '{test_slot}'!"

    trust_subsystem.populate_from_save_game(loaded_obj)
    restored_stance = trust_subsystem.get_cluster_stance(test_cluster)
    restored_score = trust_subsystem.get_cluster_score(test_cluster)

    assert restored_stance == unreal.CommunityStance.COMPROMISED, f"Failed to restore stance from disk! Got {restored_stance}"
    assert restored_score == 15, f"Failed to restore score from disk! Got {restored_score}"
    log_warn(f"  [PASS] Full disk read/write cycle restored cluster state accurately (Stance={restored_stance}, Score={restored_score}).")

    # Clean up disk slot
    b_deleted = unreal.GameplayStatics.delete_game_in_slot(test_slot, 0)
    assert b_deleted, f"Failed to delete temporary test slot '{test_slot}' from disk!"
    assert not unreal.GameplayStatics.does_save_game_exist(test_slot, 0), "Test slot still present after deletion!"
    log_warn("  [PASS] Temporary disk test slot cleanly deleted.")

    results["subtests_passed"] += 1
    results["details"]["subtest5_save_load"] = "PASS"
    log_warn("SUBTEST 5/5: PASS — URevolutionSaveGame persistence verified.")

    # Clean up spawned test actors
    actor_sub.destroy_actor(test_door)
    actor_sub.destroy_actor(test_civ)

    # Save metrics JSON
    metrics_path = "C:/Users/npal7/PROJECT/REVOLUTION/Tests/TASK_39_COMMUNITY_TRUST_VERIFICATION.json"
    with open(metrics_path, "w") as f:
        json.dump(results, f, indent=2)

    log_warn("================================================================================")
    log_warn(f"  OVERALL RESULT: {results['subtests_passed']}/{results['total_subtests']} SUBTESTS PASSED (100% PASS)")
    log_warn(f"  Verification saved to: {metrics_path}")
    log_warn("================================================================================")
    sys.exit(0)

if __name__ == "__main__":
    main()
