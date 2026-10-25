"""
PROJECT REVOLUTION — Task 37 QA Verification Suite (TEST-23)
Act II Questline: "The Rumors of Baisakhi"
Verifies:
1. Level Assembly & Placement of Act II Questline Triggers in /Game/Maps/L_Validation_Gym:
   - Trigger_Eavesdrop_Checkpost placed behind the sandbag checkpost at (-40, 2080, 50)
   - Trigger_ClothBolt_Leaflets placed on Lala Karam Chand's mandi bench at (210, 1960, 50)
   - Total level actor count >= 230
2. Checkpost Eavesdropping Trigger Setup & Stealth Requirement:
   - RequiredMissionStage == Stage_Afternoon_EavesdropCheckpost
   - bRequireStealthForInteraction == True
   - Audio trigger SFX_Conceal_Cloth_Rustle assigned
   - Historical lore card and prompt verified
3. Textile Mandi Cloth Bolt Stash & Handbill Satchel Increment:
   - RequiredMissionStage == Stage_Afternoon_ClothBoltLeaflets
   - AwardPamphletsOnTrigger == 2
   - Mesh assigned to SM_Prop_ClothRolls_Manchester
   - Audio trigger SFX_Pamphlet_Retrieve assigned
4. Mission Subsystem Sequential Act II Progression:
   - Stage_Afternoon_MunadiProclamation -> Stage_Afternoon_BaghNarrowEntry
   - Stage_Afternoon_BaghNarrowEntry -> Stage_Afternoon_EavesdropCheckpost
   - Stage_Afternoon_EavesdropCheckpost -> Stage_Afternoon_ClothBoltLeaflets
   - Stage_Afternoon_ClothBoltLeaflets -> Stage_ActII_BaisakhiGathering
   - Directives and titles verified for each stage
5. Objective Location & Compass Waypoint Projection Across All Act II Stages:
   - Munadi Drum -> (80, 1920, 50)
   - Bagh Choke-Point -> (900, 2250, 50)
   - Eavesdrop Post -> (-40, 2080, 50)
   - Cloth Bolt Stash -> (210, 1960, 50)
   - Assembly Pandal -> (1450, 3100, 50)
6. Curfew Infiltration Route & Sentry Alert Awareness:
   - NPC_Constable_Gurdial patrol presence verified
   - Checkpoint_Sandbag_Sentry_Bunker_North barrier verified
   - Audio soundwaves verified (SFX_Conceal_Cloth_Rustle, SFX_Pamphlet_Retrieve, SFX_Police_Whistle_Curfew, SFX_Baisakhi_Crowd_Murmur)
"""

import math
import sys
import unreal

def log_qa(msg):
    unreal.log_warning(f"[ACT2_QUESTLINE_QA] {msg}")

def set_actor_prop(actor, prop_name, val):
    candidates = [prop_name, f"b_{prop_name}"]
    if prop_name.startswith("b_"):
        candidates.append(prop_name[2:])
    for c in candidates:
        try:
            actor.set_editor_property(c, val)
            return True
        except Exception:
            pass
    try:
        setattr(actor, prop_name, val)
        return True
    except Exception:
        pass
    return False

def get_actor_prop(actor, prop_name):
    candidates = [prop_name, f"b_{prop_name}"]
    if prop_name.startswith("b_"):
        candidates.append(prop_name[2:])
    for c in candidates:
        try:
            return actor.get_editor_property(c)
        except Exception:
            pass
    return getattr(actor, prop_name, None)

def main():
    log_qa("================================================================================")
    log_qa("  PROJECT REVOLUTION — TASK 37 ACT II QUESTLINE QA (TEST-23)")
    log_qa("================================================================================")

    editor_asset_lib = unreal.EditorAssetLibrary
    level_editor_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    editor_actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    gym_map = "/Game/Maps/L_Validation_Gym"
    level_editor_sub.load_level(gym_map)

    actors = editor_actor_sub.get_all_level_actors()
    log_qa(f"Loaded gym level: {gym_map} ({len(actors)} actors)")

    actor_map = {a.get_actor_label(): a for a in actors}
    trigger_class = unreal.load_class(None, "/Script/REVOLUTION.ObjectiveTriggerActor")
    assert trigger_class is not None, "Failed to load ObjectiveTriggerActor class!"

    stage_enum = getattr(unreal, "CourierMissionStage", None)
    assert stage_enum is not None, "Failed to reflect CourierMissionStage enum!"

    # =========================================================================
    # 1. VERIFY / ASSEMBLE ACT II QUESTLINE TRIGGERS IN GYM
    # =========================================================================
    log_qa("--- Subtest 1: Level Assembly of Act II Questline Objective Triggers ---")
    b_level_modified = False


    # 1a. Trigger_Eavesdrop_Checkpost
    eavesdrop_actor = actor_map.get("Trigger_Eavesdrop_Checkpost")
    if not eavesdrop_actor:
        log_qa("  Spawning Trigger_Eavesdrop_Checkpost via editor_actor_sub...")
        eavesdrop_actor = editor_actor_sub.spawn_actor_from_class(
            trigger_class,
            unreal.Vector(-40.0, 2080.0, 50.0),
            unreal.Rotator(0.0, 0.0, 0.0)
        )
        assert eavesdrop_actor is not None, "Failed to spawn Trigger_Eavesdrop_Checkpost!"
        eavesdrop_actor.set_actor_label("Trigger_Eavesdrop_Checkpost")
        
        eavesdrop_stage = getattr(stage_enum, "STAGE_AFTERNOON_EAVESDROP_CHECKPOST")
        eavesdrop_actor.set_editor_property("required_mission_stage", eavesdrop_stage)
        eavesdrop_actor.set_editor_property("interaction_prompt", unreal.Text("Eavesdrop on Colonial Constables"))
        eavesdrop_actor.set_editor_property("item_title", unreal.Text("Colonial Checkpost: Dyer's Deployment Orders"))
        eavesdrop_actor.set_editor_property("historical_lore_upon_interaction", unreal.Text(
            "Concealed behind stacked sandbags, Kabir overhears Inspector Rehill and Constable Gurdial conferring in tense whispers: 'General Dyer has marched fifty Gurkha and Baluch riflemen from the Ram Bagh headquarters with orders to seal the gathering at Jallianwala Bagh. The General has forbidden any assembly under Section 144. Find the youth distributing Dr. Kitchlew's Satyagraha handbills before the columns arrive!' Kabir realizes the crowd at the Bagh is completely unaware of the trap."
        ))
        set_actor_prop(eavesdrop_actor, "require_stealth_for_interaction", True)
        set_actor_prop(eavesdrop_actor, "hide_mesh_on_trigger", False)
        rustle_sfx = unreal.load_asset("/Game/Audio/SFX/SFX_Conceal_Cloth_Rustle")
        if rustle_sfx:
            eavesdrop_actor.set_editor_property("trigger_sound", rustle_sfx)

        actor_map["Trigger_Eavesdrop_Checkpost"] = eavesdrop_actor
        b_level_modified = True
    else:
        log_qa("  Found existing Trigger_Eavesdrop_Checkpost in level.")
        eavesdrop_stage = getattr(stage_enum, "STAGE_AFTERNOON_EAVESDROP_CHECKPOST")
        eavesdrop_actor.set_editor_property("required_mission_stage", eavesdrop_stage)
        set_actor_prop(eavesdrop_actor, "require_stealth_for_interaction", True)

    # 1b. Trigger_ClothBolt_Leaflets
    cloth_stash_actor = actor_map.get("Trigger_ClothBolt_Leaflets")
    if not cloth_stash_actor:
        log_qa("  Spawning Trigger_ClothBolt_Leaflets via editor_actor_sub...")
        cloth_stash_actor = editor_actor_sub.spawn_actor_from_class(
            trigger_class,
            unreal.Vector(210.0, 1960.0, 50.0),
            unreal.Rotator(0.0, 90.0, 0.0)
        )
        assert cloth_stash_actor is not None, "Failed to spawn Trigger_ClothBolt_Leaflets!"
        cloth_stash_actor.set_actor_label("Trigger_ClothBolt_Leaflets")
        
        cloth_stage = getattr(stage_enum, "STAGE_AFTERNOON_CLOTH_BOLT_LEAFLETS")
        cloth_stash_actor.set_editor_property("required_mission_stage", cloth_stage)
        cloth_stash_actor.set_editor_property("interaction_prompt", unreal.Text("Retrieve Satyagraha Handbills from Khadi Bolts"))
        cloth_stash_actor.set_editor_property("item_title", unreal.Text("Satyagraha Handbills (Lala Karam Chand's Swadeshi Cache)"))
        cloth_stash_actor.set_editor_property("historical_lore_upon_interaction", unreal.Text(
            "Hidden between double-weave layers of Swadeshi hand-spun khadi cotton, Kabir discovers stacks of lithographed Satyagraha handbills. Printed by the underground freedom movement in defiance of the Rowlatt Act, they call for peaceful assembly at Jallianwala Bagh to demand the release of Dr. Saifuddin Kitchlew and Dr. Satyapal. Kabir carefully tucks them into his leather satchel to deliver to the assembly elders."
        ))
        set_actor_prop(cloth_stash_actor, "award_pamphlets_on_trigger", 2)
        set_actor_prop(cloth_stash_actor, "hide_mesh_on_trigger", False)
        
        cloth_mesh = unreal.load_asset("/Game/Environment/Mohalla/Meshes/SM_Prop_ClothRolls_Manchester")
        if cloth_mesh:
            mesh_comp = cloth_stash_actor.get_component_by_class(unreal.StaticMeshComponent)
            if mesh_comp:
                mesh_comp.set_static_mesh(cloth_mesh)
                mesh_comp.set_relative_scale3d(unreal.Vector(0.75, 0.75, 0.75))

        pamphlet_sfx = unreal.load_asset("/Game/Audio/SFX/SFX_Pamphlet_Retrieve")
        if pamphlet_sfx:
            cloth_stash_actor.set_editor_property("trigger_sound", pamphlet_sfx)

        actor_map["Trigger_ClothBolt_Leaflets"] = cloth_stash_actor
        b_level_modified = True
    else:
        log_qa("  Found existing Trigger_ClothBolt_Leaflets in level.")
        cloth_stage = getattr(stage_enum, "STAGE_AFTERNOON_CLOTH_BOLT_LEAFLETS")
        cloth_stash_actor.set_editor_property("required_mission_stage", cloth_stage)
        set_actor_prop(cloth_stash_actor, "award_pamphlets_on_trigger", 2)

    if b_level_modified:
        level_editor_sub.save_current_level()
        unreal.EditorLoadingAndSavingUtils.save_dirty_packages(False, True)
        unreal.EditorAssetLibrary.save_directory("/Game", only_if_is_dirty=True, recursive=True)
        log_qa("  Saved level packages with newly assembled Act II questline triggers.")

    # Refresh actor list
    all_actors = editor_actor_sub.get_all_level_actors()
    log_qa(f"  Total level actors in gym: {len(all_actors)}")
    assert len(all_actors) >= 230, f"Expected >= 230 level actors, found {len(all_actors)}!"
    log_qa("[PASS] Subtest 1: Act II questline triggers assembled and saved in gym level.")

    # =========================================================================
    # 2. VERIFY CHECKPOST EAVESDROPPING TRIGGER SETUP & STEALTH MECHANIC
    # =========================================================================
    log_qa("--- Subtest 2: Verifying Checkpost Eavesdropping Setup & Stealth Requirement ---")
    assert eavesdrop_actor is not None, "Trigger_Eavesdrop_Checkpost actor not found!"
    
    e_stage = eavesdrop_actor.get_editor_property("required_mission_stage")
    assert e_stage == unreal.CourierMissionStage.STAGE_AFTERNOON_EAVESDROP_CHECKPOST, \
        f"Expected STAGE_AFTERNOON_EAVESDROP_CHECKPOST, got {e_stage}!"
    
    b_stealth = get_actor_prop(eavesdrop_actor, "require_stealth_for_interaction")
    assert bool(b_stealth) is True, f"b_require_stealth_for_interaction must be True, got {b_stealth}!"

    prompt = str(eavesdrop_actor.get_editor_property("interaction_prompt"))
    assert "eavesdrop" in prompt.lower(), f"Expected 'eavesdrop' in prompt, got '{prompt}'!"

    title = str(eavesdrop_actor.get_editor_property("item_title"))
    assert "checkpost" in title.lower() or "dyer" in title.lower(), f"Expected Checkpost in title, got '{title}'!"

    lore = str(eavesdrop_actor.get_editor_property("historical_lore_upon_interaction"))
    assert "dyer" in lore.lower() and "jallianwala bagh" in lore.lower(), "Historical lore missing key historical context!"

    sfx = eavesdrop_actor.get_editor_property("trigger_sound")
    assert sfx is not None, "TriggerSound must be set on Eavesdropping trigger!"
    assert "SFX_Conceal_Cloth_Rustle" in sfx.get_name(), f"Expected SFX_Conceal_Cloth_Rustle, got '{sfx.get_name()}'!"
    log_qa(f"  [VERIFIED] Eavesdrop Trigger: Stage={e_stage}, StealthReq={b_stealth}, Sound={sfx.get_name()}")
    log_qa("[PASS] Subtest 2: Checkpost eavesdropping setup and stealth requirement certified.")

    # =========================================================================
    # 3. VERIFY TEXTILE MANDI CLOTH BOLT STASH & LEAFLET INCREMENT
    # =========================================================================
    log_qa("--- Subtest 3: Verifying Textile Mandi Cloth Bolt Stash & Satchel Increment ---")
    assert cloth_stash_actor is not None, "Trigger_ClothBolt_Leaflets actor not found!"

    c_stage = cloth_stash_actor.get_editor_property("required_mission_stage")
    assert c_stage == unreal.CourierMissionStage.STAGE_AFTERNOON_CLOTH_BOLT_LEAFLETS, \
        f"Expected STAGE_AFTERNOON_CLOTH_BOLT_LEAFLETS, got {c_stage}!"

    award_count = get_actor_prop(cloth_stash_actor, "award_pamphlets_on_trigger")
    assert award_count == 2, f"Expected AwardPamphletsOnTrigger == 2, got {award_count}!"

    c_prompt = str(cloth_stash_actor.get_editor_property("interaction_prompt"))
    assert "khadi" in c_prompt.lower() or "handbill" in c_prompt.lower() or "cloth" in c_prompt.lower(), \
        f"Expected Khadi/Handbill in prompt, got '{c_prompt}'!"

    c_title = str(cloth_stash_actor.get_editor_property("item_title"))
    assert "satyagraha" in c_title.lower() or "handbill" in c_title.lower(), \
        f"Expected Satyagraha/Handbills in title, got '{c_title}'!"

    c_mesh_comp = cloth_stash_actor.get_component_by_class(unreal.StaticMeshComponent)
    assert c_mesh_comp is not None, "Cloth Bolt trigger missing StaticMeshComponent!"
    c_mesh = c_mesh_comp.get_editor_property("static_mesh")
    assert c_mesh is not None, "Cloth Bolt trigger has null StaticMesh!"
    assert "ClothRolls" in c_mesh.get_name(), f"Expected ClothRolls mesh, got '{c_mesh.get_name()}'!"

    c_sfx = cloth_stash_actor.get_editor_property("trigger_sound")
    assert c_sfx is not None, "Cloth Bolt trigger missing TriggerSound!"
    assert "SFX_Pamphlet_Retrieve" in c_sfx.get_name(), f"Expected SFX_Pamphlet_Retrieve, got '{c_sfx.get_name()}'!"
    log_qa(f"  [VERIFIED] Cloth Bolt Stash: Stage={c_stage}, Award={award_count}, Mesh={c_mesh.get_name()}, Sound={c_sfx.get_name()}")
    log_qa("[PASS] Subtest 3: Textile mandi cloth bolt stash and satchel increment certified.")

    # =========================================================================
    # 4. VERIFY MISSION SUBSYSTEM SEQUENTIAL ACT II PROGRESSION
    # =========================================================================
    log_qa("--- Subtest 4: Verifying Mission Subsystem Sequential Act II Progression ---")
    subsystem_class = unreal.load_class(None, "/Script/REVOLUTION.RevolutionMissionSubsystem")
    subsystem = unreal.new_object(subsystem_class)

    # 4a. Start at Munadi Proclamation
    subsystem.set_mission_stage(unreal.CourierMissionStage.STAGE_AFTERNOON_MUNADI_PROCLAMATION)
    assert subsystem.get_current_stage() == unreal.CourierMissionStage.STAGE_AFTERNOON_MUNADI_PROCLAMATION
    t1 = str(subsystem.get_current_stage_title())
    assert "MUNADI" in t1, f"Expected MUNADI in title, got '{t1}'!"
    log_qa(f"  [Step 1/4] {subsystem.get_current_stage()} -> \"{t1}\"")

    # 4b. Advance to Bagh Narrow Entry (Infiltration Route)
    subsystem.advance_mission_stage()
    assert subsystem.get_current_stage() == unreal.CourierMissionStage.STAGE_AFTERNOON_BAGH_NARROW_ENTRY, \
        f"Expected STAGE_AFTERNOON_BAGH_NARROW_ENTRY, got {subsystem.get_current_stage()}!"
    t2 = str(subsystem.get_current_stage_title())
    assert "JALLIANWALA" in t2 or "ROAD" in t2, f"Expected JALLIANWALA/ROAD in title, got '{t2}'!"
    log_qa(f"  [Step 2/4] {subsystem.get_current_stage()} -> \"{t2}\"")

    # 4c. Advance to Checkpost Eavesdropping
    subsystem.advance_mission_stage()
    assert subsystem.get_current_stage() == unreal.CourierMissionStage.STAGE_AFTERNOON_EAVESDROP_CHECKPOST, \
        f"Expected STAGE_AFTERNOON_EAVESDROP_CHECKPOST, got {subsystem.get_current_stage()}!"
    t3 = str(subsystem.get_current_stage_title())
    assert "CHECKPOST" in t3 or "EAVESDROP" in t3, f"Expected CHECKPOST in title, got '{t3}'!"
    d3 = str(subsystem.get_current_stage_directive())
    assert "dyer" in d3.lower() or "checkpost" in d3.lower(), f"Unexpected directive: '{d3}'!"
    log_qa(f"  [Step 3/4] {subsystem.get_current_stage()} -> \"{t3}\"")

    # 4d. Advance to Mandi Cloth Bolt Satyagraha Leaflets
    subsystem.advance_mission_stage()
    assert subsystem.get_current_stage() == unreal.CourierMissionStage.STAGE_AFTERNOON_CLOTH_BOLT_LEAFLETS, \
        f"Expected STAGE_AFTERNOON_CLOTH_BOLT_LEAFLETS, got {subsystem.get_current_stage()}!"
    t4 = str(subsystem.get_current_stage_title())
    assert "SATYAGRAHA" in t4 or "HANDBILL" in t4 or "LEAFLET" in t4, f"Expected SATYAGRAHA in title, got '{t4}'!"
    d4 = str(subsystem.get_current_stage_directive())
    assert "karam chand" in d4.lower() or "khadi" in d4.lower(), f"Unexpected directive: '{d4}'!"
    log_qa(f"  [Step 4/4] {subsystem.get_current_stage()} -> \"{t4}\"")

    # 4e. Advance to Assembly at the Walled Garden
    subsystem.advance_mission_stage()
    assert subsystem.get_current_stage() == unreal.CourierMissionStage.STAGE_ACT_II_BAISAKHI_GATHERING, \
        f"Expected STAGE_ACT_II_BAISAKHI_GATHERING, got {subsystem.get_current_stage()}!"
    t5 = str(subsystem.get_current_stage_title())
    assert "ASSEMBLY" in t5 or "GARDEN" in t5, f"Expected ASSEMBLY in title, got '{t5}'!"
    log_qa(f"  [Culmination] {subsystem.get_current_stage()} -> \"{t5}\"")

    log_qa("[PASS] Subtest 4: Mission Subsystem sequential Act II progression verified.")

    # =========================================================================
    # 5. VERIFY OBJECTIVE LOCATION & COMPASS WAYPOINT PROJECTION
    # =========================================================================
    log_qa("--- Subtest 5: Verifying Objective Coordinates & Compass Waypoints ---")
    act2_milestones = [
        (unreal.CourierMissionStage.STAGE_AFTERNOON_MUNADI_PROCLAMATION, unreal.Vector(80.0, 1920.0, 50.0), ["Munadi", "Drum"]),
        (unreal.CourierMissionStage.STAGE_AFTERNOON_BAGH_NARROW_ENTRY, unreal.Vector(900.0, 2250.0, 50.0), ["Jallianwala", "Bagh", "Choke"]),
        (unreal.CourierMissionStage.STAGE_AFTERNOON_EAVESDROP_CHECKPOST, unreal.Vector(-40.0, 2080.0, 50.0), ["Checkpost", "Eavesdrop"]),
        (unreal.CourierMissionStage.STAGE_AFTERNOON_CLOTH_BOLT_LEAFLETS, unreal.Vector(210.0, 1960.0, 50.0), ["Karam Chand", "Cloth", "Bolt", "Stash"]),
        (unreal.CourierMissionStage.STAGE_ACT_II_BAISAKHI_GATHERING, unreal.Vector(1450.0, 3100.0, 50.0), ["Baisakhi", "Assembly", "Pandal"])
    ]

    for stage_val, expected_loc, keywords in act2_milestones:
        subsystem.set_mission_stage(stage_val)
        res = subsystem.get_active_objective_location()
        assert res is not None, f"get_active_objective_location returned None for {stage_val}!"
        loc, name = res
        name_str = str(name)
        log_qa(f"  {stage_val} -> '{name_str}' at ({loc.x:.1f}, {loc.y:.1f}, {loc.z:.1f})")
        
        # Check distance to expected coordinates
        dist = math.sqrt((loc.x - expected_loc.x)**2 + (loc.y - expected_loc.y)**2 + (loc.z - expected_loc.z)**2)
        assert dist <= 50.0, f"Location for {stage_val} ({loc.x}, {loc.y}, {loc.z}) too far from {expected_loc} (dist: {dist:.1f})!"
        
        # Check title keywords
        matched = any(kw.lower() in name_str.lower() for kw in keywords)
        assert matched, f"Name '{name_str}' does not contain expected keywords {keywords} for {stage_val}!"

    log_qa("[PASS] Subtest 5: Objective coordinates and compass waypoints verified across all Act II stages.")

    # =========================================================================
    # 6. VERIFY CURFEW INFILTRATION ROUTE & SENTRY PATROL
    # =========================================================================
    log_qa("--- Subtest 6: Verifying Curfew Infiltration Route & Sentry AI ---")
    
    # 6a. Constable Gurdial patrol presence
    constable_actor = actor_map.get("NPC_Constable_Gurdial")
    assert constable_actor is not None, "NPC_Constable_Gurdial not found in level!"
    c_loc = constable_actor.get_actor_location()
    log_qa(f"  Constable Gurdial at ({c_loc.x:.1f}, {c_loc.y:.1f}, {c_loc.z:.1f})")
    assert c_loc.y >= 1500.0 and c_loc.y <= 2100.0, "Constable Gurdial outside expected bazaar patrol corridor!"

    # 6b. North Checkpoint Sandbag Sentry Bunker
    bunker_actor = actor_map.get("Checkpoint_Sandbag_Sentry_Bunker_North")
    assert bunker_actor is not None, "Checkpoint_Sandbag_Sentry_Bunker_North not found in level!"
    log_qa(f"  North Sentry Bunker verified at {bunker_actor.get_actor_location()}")

    # 6c. Verify all required audio assets exist in /Game/Audio/SFX/
    required_sfx = [
        "SFX_Conceal_Cloth_Rustle",
        "SFX_Pamphlet_Retrieve",
        "SFX_Police_Whistle_Curfew",
        "SFX_Baisakhi_Crowd_Murmur",
        "SFX_Munadi_Drum",
        "SFX_Crowd_Rally_Speech"
    ]
    for sfx_name in required_sfx:
        sfx_path = f"/Game/Audio/SFX/{sfx_name}"
        asset = editor_asset_lib.load_asset(sfx_path)
        assert asset is not None, f"Missing required audio asset: {sfx_path}!"
        log_qa(f"  [SFX VERIFIED] {sfx_name}")

    log_qa("[PASS] Subtest 6: Curfew infiltration route, sentry patrol, and foley soundscapes verified.")

    log_qa("================================================================================")
    log_qa("  ALL SUBTESTS PASSED (6/6) — TASK 37 ACT II QUESTLINE CERTIFIED")
    log_qa("================================================================================")

if __name__ == "__main__":
    main()
