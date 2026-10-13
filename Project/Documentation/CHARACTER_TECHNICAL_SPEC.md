# CHARACTER TECHNICAL SPEC - Protagonist (Kabir)

Project: REVOLUTION. Engine: Unreal Engine 5.5.4 (verified). Level: /Game/Maps/L_Mohalla_Home.
Status: specification only. No replacement character has been built. Nothing in the project was deleted or overwritten.

## 1. Existing character (verified in project)

| Item | Value | Status |
|---|---|---|
| Player Blueprint | /Game/Characters/Kabir/BP_Kabir, parent C++ class RevolutionCharacter | verified |
| Game Mode used by level | BP_Mohalla_Daytime_GameMode (pawn BP_Kabir) | verified |
| Original Game Mode | BP_RevolutionGameMode (C++ RevolutionGameMode, runs curfew-night scenario) | verified, not used by L_Mohalla_Home |
| Skeletal mesh | SKM_Manny (Mannequin asset, default UE sample) | verified |
| Skeleton | SK_Mannequin | verified |
| Animation Blueprint | ABP_Manny | verified |
| Mesh component | relative location Z -90, yaw -90, uniform scale 0.78 | verified |
| Materials | slot M_torso -> MI_Manny_02; slot M_HeadLegs -> MI_Manny_01 (Mannequin default textures T_Manny_01/02) | verified |
| Capsule | radius 32 cm, half height 71 cm (about 142 cm tall) | verified |
| Mesh bounds (unscaled) | about 111 x 42 x 181 cm -> about 141 cm tall after 0.78 scale | verified |
| Walk speed | 380 cm/s; crouched 300 cm/s | verified |
| Jump velocity | 500 | verified |
| Acceleration / braking | 2048 / 2000 | verified |
| Air control | 0.35 | verified |
| Max step height | 45 cm | verified |
| Camera | spring arm 320 cm, pawn-controlled rotation, follow camera FOV 90 | verified |
| Input | IA_Move, IA_Look, IA_Jump, IA_Sprint, IA_Crouch, IA_Interact in IMC_Default | verified |
| Animations present | BS_MM_WalkRun, MM_Idle, MM_Walk_Fwd, MM_Run_Fwd, MM_Walk_InPlace, MM_Jump, MM_Fall_Loop, MM_Land, MM_T_Pose, unarmed MF_* sequences | verified (asset list) |
| Facial animation / morph targets | none found in this asset list | verified absence in list only |

## 2. Problems with the current character

1. **Adult proportions scaled down.** Manny is an adult mannequin shrunk to 78%. This is exactly what the brief rejects: child proportions (head-to-body ratio, limb length, shoulder width) are not modelled.
2. **Generic mannequin look.** Default Mannequin textures and no costume.
3. **Probable foot offset mismatch (UNVERIFIED visually).** The mesh is offset -90 cm while the capsule bottom is at -71 cm. Because the scale 0.78 is not applied to the offset, the feet may sit about 19 cm below the capsule bottom, i.e., about 17 cm into the ground at the spawn height. This should be checked in Play before changing anything. Suggested fix, pending approval: set the mesh Z offset to about -71.
4. **No facial setup.** No morph targets or facial rig are in the project, so cinematic close-ups are not supported.
5. **Movement and camera values are template defaults** (Mannequin-style), not tuned for a child.

## 3. Identity decisions

Verified from the project:
- Protagonist name: Kabir (asset and input naming). Preserved.
- Input and character naming indicates a boy, but no age is set in code.

From the brief (to be used for design):
- Age: 12.
- Ordinary family background, curious, quiet determination.
- Everyday historically appropriate clothing (not yet defined).
- Realistic, grounded, not an adult scaled down, generic mannequin, fantasy warrior, or cartoon.

UNCONFIRMED (approval needed):
- Region and years. Project code mentions "1919 Mohalla" and an inspectable text mentions "1920s Punjab". Not confirmed by the owner.
- Final face and costume details. Antigravity should design these from the approved direction.
- Whether the character must match the environment's Lahori/Punjab-style assets.

## 4. Blender requirements (for Antigravity)

### A. Model
- Child proportions for a 12-year-old: total height target about 140-150 cm (must match the capsule; see Section 5). Head about 1/6 to 1/6.5 of height. Longer legs relative to torso than an adult, smaller hands and feet, narrower shoulders.
- Full body, plus close-up facial detail for cinematics (eyes, eyelids, mouth, brows, nose, ears).
- Hands with five fingers, feet with toes, clearly visible ears.
- Hair: simple, low-count strands or card hair; no high-poly strand groom for gameplay.
- Clothing: fitted to the body; no separate cloth simulation in the game asset.
- Real-time budget: suggested LOD0 about 25,000-35,000 triangles for a close-up cinematic protagonist, with LOD1 about 12,000 and LOD2 about 5,000. These are starting targets, not mandatory limits. Confirm against the target hardware before locking.

### B. Rigging
- Reuse the existing SK_Mannequin skeleton only if the proportions of the new mesh are close enough that the existing animations do not look wrong. Because a child has different limb ratios, a new skeleton retargeted from the Mannequin is the likelier path. Test first.
- Keep standard UE5 Mannequin bone names (pelvis, spine_01..05, neck_01, head, clavicle_l/r, upperarm_l/r, lowerarm_l/r, hand_l/r, finger bones, thigh_l/r, calf_l/r, foot_l/r, ball_l/r) so the retarget and existing ABP keep working.
- Facial bones or morph targets: required for cinematic close-ups; not present in the project now. Decide the facial approach before modelling (bones vs morphs).
- Risks: changing the skeleton breaks ABP_Manny and any Retarget Assets until they are rebuilt; keep the new skeleton as a separate asset.

### C. Materials and textures
- Material slots: skin, hair, eyes, clothing (top, bottom), footwear. Keep to 4-6 slots.
- Skin: PBR base colour, normal, roughness, optional subsurface mask.
- Hair: alpha card texture or simple PBR.
- Cloth: PBR base colour, normal, roughness.
- Texture resolutions: 2048 for face and head, 1024 for body and clothing, 512 for small details. Confirm against VRAM budget.
- Unreal compatibility: use standard UE5 PBR nodes; avoid exotic shading models; do not depend on removed nodes.

### D. Export and import
- Format: FBX (preferred for skeletal mesh and animation), with Blender's Y-up / forward settings matched to UE: Apply Scale, Forward -Y, Up Z in the exporter.
- Scale: model in metres in Blender matching UE centimetres after import (1 Blender unit = 1 m); apply all transforms before export; the final UE scale should be 1.0 with the mesh in cm.
- Orientation: character faces -Y in UE (matching the existing Manny convention) with origin at the feet.
- Normals and tangents: export with tangents from the source, and import with Mikktspace. Smooth normals on the body and face.
- Skeleton: one root bone at origin; no extra root transforms.
- Naming: Character_Kabir_v01_LOD0.fbx, _LOD1.fbx, _LOD2.fbx; textures Kabir_Skin_BC_2k.png etc.
- Folder in UE: /Game/Characters/Kabir/Mesh/ (new), keeping BP_Kabir and the input assets where they are.

### E. Performance
- Gameplay camera distance is about 320 cm behind the character with a 90 degree FOV (verified). Cinematics will be closer.
- Use LOD0 for cinematics and gameplay near range; LOD1 for mid range; LOD2 beyond.
- Avoid high-resolution textures on clothing and hair cards.
- Use one shared material with instances instead of many unique materials.

## 5. Capsule and scale requirements (must be decided before modelling)

The character capsule is 142 cm tall. A 12-year-old is roughly 140-150 cm. Two options:
1. Keep the 142 cm capsule and model the child at about 140 cm standing (recommended; least change).
2. Change the capsule and camera. This affects movement, stairs (max step height 45 cm), doorways (door opening about 270 cm) and camera boom distance (320 cm). Changing it requires owner approval.

## 6. Validation checklist (for when the new model exists)

| # | Check | Type |
|---|---|---|
| 1 | Character scale matches capsule (feet at capsule bottom, head within capsule) | Automated (bounds) + visual |
| 2 | Child proportions read correctly in front/side views | Visual |
| 3 | Face and body proportions in close-up | Visual |
| 4 | Materials and textures render with correct colours in Lumen daytime | Visual |
| 5 | Skeleton compatibility (bones named as spec, retarget to ABP) | Automated (bone name check) |
| 6 | Animation deformation at shoulders, hips, knees, elbows | Visual |
| 7 | Clothing intersections (no clipping at neck, shoulders, waist, knees) | Visual |
| 8 | Capsule collision: walks through the doorway (270 cm), up 45 cm steps, no snagging | Gameplay test (PIE) |
| 9 | Idle, walk, run, jump, land, fall animations play correctly | Gameplay test |
| 10 | Frame rate and triangle count at gameplay distance | Performance test |
| 11 | Integration into L_Mohalla_Home without breaking inspect/input | Gameplay test |

Automated: scale, bounds, bone names, material slot count, triangle count, import warnings.
Needs visual or gameplay testing: all others.
No test in this list has passed yet; the replacement character does not exist.

## 7. Known uncertainties and decisions needing owner approval

1. Region and years (affects costume and architecture). Hints: Punjab, 1919/1920s. UNCONFIRMED.
2. Capsule size: keep 142 cm (recommended) or change it.
3. Whether to fix the mesh offset (-90 -> about -71) after confirming in Play. NOT changed yet.
4. Facial approach: bones or morph targets.
5. Whether to reuse the Mannequin skeleton or build a new one.
6. Target hardware (affects LOD and texture sizes).
7. Final character visual design (Antigravity, with approval).
8. Whether any paid tools or assets are allowed.


## Update 2026-10-12 (owner decisions applied)
- Capsule: kept at 142 cm.
- Foot offset: changed BP_Kabir mesh Z from -90 to -71 after a Play test (feet from -16.85 cm to +2.15 cm relative to the floor; walking and jump unchanged). Original -90 recorded in FOOT_OFFSET_TEST.md.
- Facial: SKM_Manny has 0 morph targets. Facial bones unverified. Bone-based face needs facial bones in the new rig.
- Skeleton: keep Mannequin skeleton for the first mesh test; new skeleton only if compatibility fails. Trade-offs in PROJECT_DIRECTION.md.
- Hardware: GTX 1650 (4 GB), 16 GB RAM. Start protagonist at 2K (face/head), 1K (body/clothing). Measure in Play before finalising LODs.
- Budget: free tools only.
See PROJECT_DIRECTION.md for the full status of each decision.
