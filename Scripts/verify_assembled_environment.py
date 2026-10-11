import unreal

def verify():
    unreal.log("================ VERIFYING ASSEMBLED MOHALLA & BAZAAR ENVIRONMENT ================")
    
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)
    world = level_sub.get_current_level().get_world()

    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    all_actors = actor_sub.get_all_level_actors()
    unreal.log(f"Total level actors found in L_Validation_Gym: {len(all_actors)}")

    modular_count = 0
    prop_count = 0
    light_count = 0
    foundation_slab = None
    player_start = None

    for a in all_actors:
        label = a.get_actor_label()
        if "Modular_" in label:
            modular_count += 1
        elif "Light" in label or "Sun" in label or "Atmosphere" in label:
            light_count += 1
        elif "Foundation_Slab" in label:
            foundation_slab = a
        elif isinstance(a, unreal.PlayerStart) or "PlayerStart" in label:
            player_start = a

    unreal.log(f"Modular Architecture & Street Pieces: {modular_count}")
    unreal.log(f"Lighting & Atmospheric Actors: {light_count}")
    unreal.log(f"Solid Foundation Slab Present: {foundation_slab is not None}")
    unreal.log(f"PlayerStart Present: {player_start is not None} at {player_start.get_actor_location() if player_start else 'None'}")

    # Comprehensive multi-zone raycast validation points: (Zone Name, Test Start, Expected Floor Z)
    test_zones = [
        ("Zone A: Kabir Courtyard Floor", unreal.Vector(0.0, -150.0, 500.0), 0.0),
        ("Zone A: Family Living Quarters", unreal.Vector(0.0, -400.0, 500.0), 0.0),
        ("Zone A: Tailor Workshop Floor", unreal.Vector(400.0, 400.0, 500.0), 0.0),
        ("Zone A: 1F Rooftop Terrace Slab", unreal.Vector(0.0, 400.0, 1000.0), 400.0),
        ("Zone A: 1F West Terrace Slab", unreal.Vector(-400.0, 0.0, 1000.0), 400.0),
        ("Zone A: 1F East Terrace Slab", unreal.Vector(400.0, 0.0, 1000.0), 400.0),
        ("Zone B: Deorhi Alley Threshold", unreal.Vector(0.0, 750.0, 500.0), 0.0),
        ("Zone B: Deorhi Connecting Galli", unreal.Vector(0.0, 950.0, 500.0), 0.0),
        ("Zone C: Communal Well Apron", unreal.Vector(0.0, 1350.0, 500.0), 10.0),
        ("Zone C: Chopal Seating Platform", unreal.Vector(220.0, 1350.0, 500.0), 0.0),
        ("Zone D: Grand Bazaar Street Galli", unreal.Vector(0.0, 1800.0, 500.0), 0.0),
        ("Zone D: Spice Merchant Stall", unreal.Vector(-400.0, 1950.0, 500.0), 75.0),
        ("Zone D: Halwai Tea Shop Stall", unreal.Vector(-200.0, 1650.0, 500.0), 75.0),
        ("Zone D: Mandi Grain Procurement", unreal.Vector(400.0, 1650.0, 500.0), 0.0)
    ]

    all_passed = True
    for name, start, expected_z in test_zones:
        end = unreal.Vector(start.x, start.y, -100.0)
        hit = unreal.SystemLibrary.line_trace_single(
            world,
            start,
            end,
            unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,
            False,
            [],
            unreal.DrawDebugTrace.NONE,
            True
        )
        tup = hit.to_tuple()
        blocking_hit = tup[0]
        impact_z = tup[4].z
        normal_z = tup[6].z
        
        status = "PASS" if blocking_hit and impact_z >= expected_z - 15.0 and normal_z > 0.4 else "FAIL"
        if status == "FAIL":
            all_passed = False
        unreal.log(f"[{status}] {name}: Hit={blocking_hit}, ImpactZ={impact_z:.1f} (expected ~{expected_z:.1f}), NormalZ={normal_z:.2f}")

    unreal.log(f"================ ASSEMBLED ENVIRONMENT VALIDATION: {'ALL PASSED (100% SOLID)' if all_passed else 'SOME FAILED'} ================")

    # Run PIE lifecycle test
    unreal.log("Testing PIE Session Lifecycle...")
    level_sub.editor_request_begin_play()
    unreal.log("Requested PIE BeginPlay.")

if __name__ == "__main__":
    verify()
