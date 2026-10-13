# Environment Production Log

## 2026-10-11
- Inspected project: UE 5.5.4; C++ module REVOLUTION (RevolutionCharacter/GameMode/HUD, CurfewPatrolAI, PariahDogActor, InteractableInterface, InspectableProp, MissionSubsystem, AtmosphereController, ...); one map `L_Validation_Gym`.
- 4 materials had no nodes -> rebuilt (base colour/roughness/metallic) and saved.
- Created `BP_Kabir` (RevolutionCharacter + SKM_Manny + ABP_Manny), `BP_RevolutionGameMode`, IA_Sprint/IA_Crouch/IA_Interact and keys in `IMC_Default`.
- Created `L_Mohalla_Home`: lighting, 200 m ground, family home, 5 neighbour houses, market, well, school yard, countryside, boundary, PlayerStart, NavMeshBoundsVolume.
- Scripted PIE test: stable spawn height (~20 s, no falling); walking north passes the front doorway and interior doorway and stops at the back wall.

## 2026-10-12
- `RevolutionGameMode` spawns a curfew-night scenario near the origin (watchman, dog, mission markers, hazards) and an atmosphere controller (night lighting, distant-train sound). That would clash with the daytime street.
- Created `BP_Mohalla_Daytime_GameMode` and set it on `L_Mohalla_Home`; `BP_RevolutionGameMode` and `L_Validation_Gym` unchanged.
- Replaced 6 family-home placeholder props with `InspectableProp` actors (lantern, 2 charpais, kulhad, kite spool, grain sack).
- Scripted PIE check: game mode = BP_Mohalla_Daytime_GameMode, pawn = BP_Kabir at (-800,120,73), 6 InspectableProps report prompts (e.g. "Inspect Hurricane Lantern") and can_interact = true, 0 atmosphere controllers, 1 character, no gameplay spawn logs.
- NOT verified: what appears on screen when interacting (calling on_interact from script returned nothing and logged nothing), keyboard input, how the level looks, frame rate.

## 2026-10-12 (later)
- Placed the jharokha balcony over the family home front door (-800, 350, 180) and the masonry roof stairs in the gap next to the family home (-1600, 930, 0). Saved.
- Stairs are placed as set-dressing; I have not verified they connect to the roof or are walkable.
- Created CHARACTER_DESIGN.md with the Kabir working brief. No costume materials assigned yet.
- NOT verified in Play: whether the balcony and stairs look right on screen or block the player.

## 2026-10-12 - Roof access stairs (final layout)
- Removed earlier 45-degree block actor FamilyHome_Roof_Stairs (mesh asset SM_Roof_Stairs_Masonry_01 untouched; it was unsuitable: front face blocked entry and the slope is about 45 degrees).
- Removed actor FamilyHome_ParaL_0 (west roof parapet, y 348-752 at x -1400) to open the roof access. Mesh asset untouched. Opening is the full 404 cm length of that parapet section.
- Built 10 brick steps RoofStairs_Step_00..09 (Cube primitives with M_LahoriBrick_PBR), run north-south at x = -1600, 350 cm wide (fills clear space between the neighbour wall at x -1775 and family home wall at x -1425). Each tread 40 cm deep, riser 40 cm, top at 400 cm. Heights checked by trace.
- Added RoofStairs_Guard_Parapet (SM_Roof_Parapet_4m_A) at (-1600, 780, 0): stops overshoot off the top tread.
- Play tests (scripted, 2026-10-12):
  - Climb: from street (-1600, 250) up to top tread (y 730, z about 473 centre, i.e. standing on the 400 cm top). PASS.
  - Roof crossing: from top tread onto roof at x about -1215, standing height. PASS.
  - Return to top: walked back to x about -1555, on top surface. PASS.
  - Descent: from top (-1600, 706) to street (-1600, 226, z 73). Samples follow each tread without falling through. PASS (coarse sampling; not frame-by-frame).
- NOT verified: visual appearance, first-person/camera view, stairs with real captured frame rate, both directions repeated.
