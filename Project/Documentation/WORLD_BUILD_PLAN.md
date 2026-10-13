# REVOLUTION - World Build Plan (Milestone 1)

Level: `/Game/Maps/L_Mohalla_Home` (new; `L_Validation_Gym` untouched). Unreal 5.5.4.
GameMode: `BP_Mohalla_Daytime_GameMode` (plain GameModeBase -> pawn `BP_Kabir`, HUD `RevolutionHUD`). It deliberately does NOT use `RevolutionGameMode`, which spawns the curfew-night stealth scenario and night atmosphere.

## Layout (cm; origin = middle of the main street; street runs along X, ~6 m wide)
| Zone | Where | Status |
|---|---|---|
| Family home (3x2 modules, front door, 2 rooms, roof + parapets) | x -1400..-200, y 350..1150 (north side) | built; 6 inspectable props |
| Neighbour houses | N: x -3000..-1800 and 200..1000; S: x -3000..-1800, -1400..-200, 200..1000 | built (shells + roofs) |
| Market plaza (8 stalls, goods, shutters, back walls) | x 1400..3400, y -1100..1100 | built |
| Stone well landmark | (3700, 0) | built |
| School / community yard (walled, veranda, tree, blackboard) | x -4600..-3400, y 350..1550 | built, placeholder |
| Countryside (fields, tree clumps, mud walls, hedge belt at +-95 m) | east of x 4000 and ring | built, placeholder |

Player starts at (-800, 120) facing the family-home door.

## Next phases
1. Visual review and fixes (orientation, overlaps, dirt/decal variation, real textures).
2. Place Balcony_Jharokha and Roof_Stairs; alley and street detail; vegetation; lighting polish.
3. Performance profiling.
