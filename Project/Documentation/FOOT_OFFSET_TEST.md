# Foot Offset Test - BP_Kabir mesh relative Z

ORIGINAL VALUE (must be restored if the test is reverted): -90.0 cm (relative_location = (0, 0, -90), rotation yaw -90, scale 0.78).

Baseline (verified in PIE, 2026-10-12, L_Mohalla_Home):
- Pawn z at spawn: 73.15 cm; capsule bottom: 2.15 cm above floor (floor z = 0).
- Mesh pivot (feet): -16.85 cm, i.e. feet about 16.85 cm below the floor.
- Walking north from spawn for 120 ticks: pawn z stayed 73.15, feet stayed -16.85 relative to floor, Kabir stopped at the back wall (y about 1092).

TEST: change Z to -71.0 (feet at capsule bottom). Result below.

## Result (Play test, 2026-10-12)
- Changed mesh relative Z from -90 to -71 on BP_Kabir (ORIGINAL -90 recorded above; saved).
- Spawn: pawn z 73.15 (unchanged); feet now +2.15 cm above floor (was -16.85 cm below). The 2 cm gap comes from the spawn height (73.15 = capsule resting 2.15 cm above the floor). Recommended follow-up: check Player Start Z (80) and resting height; not changed.
- Walking north 120 ticks: pawn z 73.15 constant, feet +2.15 constant, reached back wall (y 1092.5). Same as baseline movement.
- Jump: launched from 73.15 to peak about 188.7 (about 115 cm), landed back at 73.2 (standing height). Movement intact.
- Decision: KEEP -71. Grounding improved and movement unchanged, so the revert condition was not met.
- NOT tested: stairs (max step 45 cm), sprint, crouch, slopes, and the landing on the new Kabir mesh (the test used the Mannequin mesh; the new character doesn't exist yet).

## Stairs / slope status (2026-10-12)
- Not tested. The walk test ran straight north from spawn and did not reach the roof-stairs mesh at (-1600, 930). Stairs in the level are set dressing, so the step-height check (45 cm) is still open.

## Stairs test result (2026-10-12) - replaces the 'not tested' note
- Method: teleported Kabir to (-1600, 470) in Play and walked north 28+ ticks into the stairs.
- Result: BLOCKED at y 538 by the stairs' front face (a solid vertical wall from ground to at least 380 cm, at y = 570). Kabir could not climb.
- Stair profile (editor traces at x = -1600): top surface 375 cm at y 600, 325 at 650, 275 at 700, 225 at 750, 150 at 800, 100 at 850, 50 at 900. That is a 1:1 slope (about 45 degrees), with one convex collision hull.
- Implication: as placed, SM_Roof_Stairs_Masonry_01 is NOT a walkable route. A 45-degree slope is at or above the usual walkable limit (about 45 degrees) and the front face blocks entry. The 45 cm step height doesn't apply to this slope.
- Not changed. Options for the owner to choose: (a) keep as decorative set dressing; (b) replace with a gentler ramp or discrete steps no higher than 45 cm each; (c) rotate so the high end faces away from the street and build a separate access route.

## Roof stairs result (2026-10-12) - replaces earlier stairs note
- The 45-degree block failed (blocked). Replaced by 10 walkable steps (see ENVIRONMENT_PRODUCTION_LOG.md). Climb, roof crossing and descent pass in scripted Play tests with the -71 offset.
