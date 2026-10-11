import unreal

def verify():
    unreal.log("================ VERIFYING DISTRICT C (SCHOOL) & WORKSHOP EXPANSION ================")
    
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)
    world = level_sub.get_current_level().get_world()

    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    all_actors = actor_sub.get_all_level_actors()
    unreal.log(f"Total level actors found: {len(all_actors)}")

    school_pieces = 0
    modular_pieces = 0
    for a in all_actors:
        lbl = a.get_actor_label()
        if "School_" in lbl:
            school_pieces += 1
        elif "Modular_" in lbl:
            modular_pieces += 1

    unreal.log(f"Mohalla & Bazaar Modular Pieces: {modular_pieces}")
    unreal.log(f"District C School & Workshop Pieces: {school_pieces}")

    # Trace validation across School and Workshop
    test_locs = [
        ("Father's Singer Sewing Machine", unreal.Vector(200.0, 520.0, 500.0), 0.0),
        ("School Gateway Archway", unreal.Vector(800.0, 1350.0, 500.0), 0.0),
        ("School Central Bell Tower", unreal.Vector(1350.0, 1350.0, 500.0), 0.0),
        ("Classroom 4B Roof Slab", unreal.Vector(1350.0, 1850.0, 1000.0), 400.0),
        ("Classroom 4B Student Desk", unreal.Vector(1150.0, 1850.0, 500.0), 0.0),
        ("Classroom 4B Slate Blackboard", unreal.Vector(1350.0, 1980.0, 500.0), 0.0)
    ]

    all_passed = True
    for name, start, expected_z in test_locs:
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

    unreal.log(f"================ SCHOOL & EXPANSION VERIFICATION: {'ALL PASSED (100% SOLID)' if all_passed else 'SOME FAILED'} ================")

if __name__ == "__main__":
    verify()
