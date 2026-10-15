# REVOLUTION - Project Audit and Next-Stage Prompt
Date: 2026-10-12. Engine: Unreal 5.5.4. Hardware tested: GTX 1650 (4 GB), 16 GB RAM, 8 threads.

## 1. Verdict
NOT ready for AAA production yet. The foundation is sound: project structure, C++ base classes, input, lighting setup, a working daytime game mode, a playable spawn, and a first walkable roof-access test. Everything visual (character, environment, materials) is still at preview or placeholder level. Continue, but in the order below.

## 2. Status by system (verified / partial / not started)
| System | Status | Evidence |
|---|---|---|
| Project and engine setup | Verified | UE 5.5.4; C++ module REVOLUTION; Lumen on; screen percentage 75 |
| Playable character (BP_Kabir) | Partial | Parent RevolutionCharacter; uses SKM_Manny placeholder; mesh z offset -71 (feet on floor) |
| Input (move, look, jump, sprint, crouch, interact) | Partial | Bindings exist; keys verified in standalone simulated input only; not verified by a human |
| Daytime level L_Mohalla_Home | Partial | Primitive houses, market, school yard, countryside; placeholder materials |
| Roof access stairs | Verified in scripted tests | Climb, roof crossing, return, descent all passed; owner says looks good for preview; brick cube steps |
| Inspectable props (6) | Partial | Prompts report via script; on-screen panel not verified; on_interact returned nothing |
| Curfew/stealth content (C++) | Present but unused by daytime level | RevolutionGameMode spawns watchman, dog, hazards; BP_Mohalla_Daytime_GameMode avoids it |
| Mission system | Present | Log shows "Act I 'The Morning Courier' active" |
| Performance | Partial | Standalone 1080p: about 120 fps steady; 1% low about 40-60 fps from hitches; no test in heavy areas |
| Character model | Placeholder | v01-v04 Blender models are primitive-based; not sculpted |
| Character skeleton | Partial | 64-bone rig, weights bound, pose-tested; animations not tested; no IK Rig or retarget |
| Character animation | Not started | No retarget, no tests of idle, walk, run, jump on new rig |
| Environment materials | Placeholder | Flat colours; some missing references (M_Terracotta_PBR, M_JuteRope_PBR) |
| Historical research | Partial | Architecture supported; 1910s costume and objects unverified |
| Audio | Partial | Train sound plays; no audio design pass |
| Story and quests | Not started | Only a mission-system stub |
| Documentation | Partial | 16 documents; several have appended sections and overlap |

## 3. Mistakes and gaps to correct (honest list)
1. Playable character is still the Manny mannequin. v02-v04 models are not in the game. Decide the replacement path before more modelling.
2. Rig is not tested for animation. Claims about "animations will work" are NOT verified.
3. Earlier wording overstated some results. Examples: "daytime setup works" was based on scripted tests only; the standalone route test was not controlled, so its path is unverified.
4. Keyboard controls were never tested by a human in Play. Simulated keys in the standalone build are only a proxy.
5. Interact panel: prompts are verified in script; what appears on screen is not.
6. Foot offset kept at -71. The 2 cm spawn float is unresolved; the Player Start height has not been changed.
7. Roof stairs are brick cubes, not stair art. Retexture/remodel is still needed.
8. The parapet over the roof access was removed (opening about 404 cm). Consider a proper gap or a rail.
9. Historical clues conflict: the code says "1919 Mohalla" and "1920s Punjab", while the owner's direction is rural UP c. 1910-1920. Resolve before costume and architecture work.
10. Costume direction: the reference concept (turban, blue, gold, weapons) conflicts with the approved direction (realistic, no headwear, undyed cotton, no weapons). The owner must confirm which applies.
11. Blender files: several saved copies exist (v02, v03, v04 in Documents and in the project). v03 is weak. Keep v04 and v02 as references; the project copies are the source of truth.
12. Blender session: the in-session v01 head was removed during v02 work. The saved v01 file on disk is intact.
13. Blender preference: when screenshots are shared, also save the .blend and delete the previous saved version.
14. Environment Python in the editor and the Blender add-on both dropped out during the session. Long jobs need checking before and after.
15. Lumen and 2K textures on a GTX 1650 are untested under real load. The current measurement is light and mostly idle.
16. Missing mesh references: some meshes point to materials that do not exist. Check before packaging.
17. Test levels (L_Character_Test_v02) are not production maps. Keep them separate from the game level.

## 4. Character design and modelling: recommendations
Decide first (owner): style (realistic child, as approved), costume (undyed cotton, no weapons), headwear (none by default), and whether a stylised concept (reference photo) is an option for the game. Do not mix styles.

Pipeline (free options first, paid only with approval):
- Concept: 3-view sheet (front, side, back) and a head turnaround. Use the reference photo for silhouette and colour only, not for copying.
- Base mesh: sculpt in Blender Sculpt mode (free). Multires for detail. A child head ratio about 1:5.5 to 1:6; large eyes are not needed for realism.
- Retopology: Instant Meshes (free) or Blender Remesh and manual retopo. Quad Remesher is paid; do not use without approval.
- UVs: Blender Smart UV Project, then check texel density (2K face and head, 1K body and clothes).
- Textures: Poly Haven (CC0) for skin and fabric references; paint in Blender Texture Paint or Krita (free). Substance Painter is paid; do not use without approval.
- Hair: Unreal Groom (free in UE 5.5 with the groom plugin) for a short cut, or hair cards. Avoid high-strand groom for gameplay LOD.
- Clothing: kurta and shorts as fitted shells (already done in v04); add folds with sculpt and a cloth pass later. Marvelous Designer is paid.
- Rig: Blender Rigify (free) with UE5 Mannequin-compatible names; or the current 64-bone rig, extended with twist bones.
- Facial: 30-52 morph targets for cinematic close-ups (smile, brows, eyes, mouth shapes). Use Unreal's Live Link only if mocap is approved.
- MetaHuman: free Epic tool, excellent for adults, but it is not designed for child characters. Do not rely on it for this protagonist without checking.
- Mocap and animation libraries: Mixamo (free animations, retargetable to humanoid rigs). Check licence for commercial release.
- Budgets: LOD0 25k-35k triangles; LOD1 about 12k; LOD2 about 5k. Materials: one shared master with instances.
- Milestones: concept approved -> base mesh approved -> retopo and UV -> textures -> rig and skinning -> animation test -> integration into BP_Kabir.

## 5. Environment recommendations
- Replace primitive houses and props with modular kits (walls, doors, windows, roofs) built to the same dimensions as the wall module (4 m).
- Materials: use Poly Haven CC0 textures for brick, mud plaster, wood, cloth; fix missing references first.
- Lighting: keep the daytime sun, add baked lighting or keep Lumen and test cost on the GTX 1650.
- Props: use free Megascans through Fab if the Unreal licence applies; check the current terms.
- Gameplay: remove or quarantine the unused curfew content, or design it as a later chapter with its own game mode.

## 6. Prompt to update things (copy into the next session)
You are the lead technical artist and Unreal developer for REVOLUTION (UE 5.5.4). Use the Unreal and Blender connections to inspect before changing anything. Do not delete or overwrite existing assets. Do not change BP_Kabir's mesh unless the test passes.

1. Read Documentation/PROJECT_AUDIT_AND_NEXT_PROMPT.md and PROJECT_DIRECTION.md. Confirm the decisions marked OPEN with the owner before modelling.
2. Character: decide the replacement path. Preferred: base mesh sculpted in Blender, using the v04 layout as reference. Output Kabir_v05.blend to Documents/Blender/Kabir_v05/ and an FBX to Art/Character/Kabir_v05/. Target: 25k-35k LOD0 triangles, 2K face and head textures.
3. Rig: extend Kabir_v04 rig with twist bones. Create an IK Rig for the Mannequin and for the new rig. Create an IK Retargeter. Test idle, walk, run and jump in L_Character_Test_v02 and report which bones fail.
4. Integration: only after step 3 passes, create a copy of BP_Kabir (BP_Kabir_v05) that uses the new mesh. Do not replace BP_Kabir until the owner approves.
5. Environment: replace the roof stairs brick cubes with proper stair art, keep the walkable dimensions (40 cm rise, 40 cm tread, 350 cm width), and re-test climb, roof crossing and descent.
6. Materials: fix missing references (M_Terracotta_PBR, M_JuteRope_PBR). Retexture the main walls and steps from CC0 sources.
7. Performance: repeat the standalone route test at 1920x1080 twice, and report whether the spikes repeat on the second run. Record average, 1% low and the stutter count each time.
8. Documentation: update each file you change; mark anything unverified as unverified. Do not claim a test passed unless it was run.
9. Report: what changed, what was tested, what failed, and the three highest-priority next tasks.
Stop and ask the owner before any paid tool, plugin, or asset, and before any change to the gameplay setup.

## 7. Owner decisions still needed
1. Costume and headwear: undyed cotton, no headwear (current) or change.
2. Style: realistic (current) or stylised like the reference photo.
3. Historical clues: confirm rural UP c. 1910-1920 and ignore the 1919/Punjab code clues, or change the direction.
4. Replacement path: sculpt in Blender (free) or a paid tool (requires approval).
5. Curfew content: keep it for a later chapter or remove it from the daytime build.
