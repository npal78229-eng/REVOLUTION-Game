# Kabir - Character Model v02 (Blender, separate asset)

Status: second build, approved direction applied (realistic-leaning child, no headwear, undyed cotton kurta and undyed cotton shorts, no weapons or gold accessories). Still a preview. Not imported into Unreal yet. BP_Kabir still uses SKM_Manny. Nothing in the project was overwritten.

## Files
- Art/Character/Kabir_v02/Kabir_v02.blend (only the v02 scene, collection Kabir_v02)
- Art/Character/Kabir_v02/Kabir_v02.fbx (49 mesh parts, no skeleton, applied scale, 1 unit = 1 m, forward -Y, up Z)
- v01 files are unchanged on disk: Art/Character/Kabir_v01/

## Design applied
- Child proportions, 1.44 m tall (target 140-150 cm; capsule is 142 cm, so about 2 cm over).
- Head about 1:6 of height, narrow child jaw, eyes set on the face, short cropped hair, small nose and lips, ears.
- Costume: undyed cotton kurta (cream-tan) and short cotton shorts (undyed, earthy tone). Bare feet with toes.
- No headwear, no weapons, no gold accessories (as approved).

## Face
- Shape keys on the head: Basis, Smile, Brows_Up. Eyes and irises are separate meshes (no eyelid geometry yet).
- Nose and lips are small sculpted bumps, not detailed sculpting.

## Not done (Milestone 2 quality still open)
- Procedural primitives, not sculpted. Hands are simplified (palm and five finger tubes). Feet simplified.
- Hair is a single cap shell; no strands or hairline detail.
- No UVs or textures (flat material colours only). No retopology.
- No skeleton or rig; no facial bones. No eyelids or mouth geometry beyond the bumps.
- Not tested in Unreal yet.

## Known issues found during build (fixed)
- Name clash with v01 objects: v02 parts were initially renamed with .001 suffixes; fixed. Old v02 head duplicate removed.
- Nose displacement was in wrong units and buried the eyes; head rebuilt.

## Unreal import and scale check (2026-10-12)
- Imported Kabir_v02.fbx into /Game/Characters/Kabir_v02/ as 49 static meshes (one per part). Materials imported. Textures not imported (none).
- Unreal units confirmed: 1 m in Blender = 100 cm in Unreal.
- Head centre at 131 cm, top at 142.5 cm. Feet at 0.1 cm. Assembled figure height 144.2 cm (capsule 142 cm), width 45 cm with arms, depth 28 cm.
- Test level created: /Game/Maps/L_Character_Test_v02 with all 49 parts placed at the origin (pivots preserved). Used only for checking scale and assembly. The playable level L_Mohalla_Home and BP_Kabir are untouched; BP_Kabir still uses SKM_Manny.
- Still open: convert to one skeletal mesh (needs skeleton), decide whether to replace SKM_Manny, and test movement with the new mesh. Combining the 49 parts into one mesh is recommended before rigging.

## Combined single mesh (2026-10-12)
- Blender: parts joined into two objects, Kabir_Body (all parts except head) and Kabir_Head (carries Basis/Smile/Brows_Up shape keys). Re-exported Kabir_v02.fbx and Kabir_v02.blend.
- Unreal: re-imported as one static mesh /Game/Characters/Kabir_v02/Kabir_Body. Height 144.2 cm, 25,552 triangles at LOD0, 6 material slots (names carry _001 suffix from the earlier duplicate material names; cosmetic).
- Shape keys (Smile, Brows_Up) are NOT carried into Unreal: static meshes do not hold morph targets. They need a skeletal mesh import to survive.
- Test level L_Character_Test_v02 now places this single mesh.
- Still open: skeleton and rig (required before walking/jumping), skeletal import for morph targets, material cleanup, then decide on swapping SKM_Manny.

## Viewable copy in Blender (2026-10-12)
- Separate folder for viewing in Blender: C:\Users\npal7\Documents\Blender\Kabir_v02\Kabir_v02.blend (scene Kabir_v02, objects Kabir_Body and Kabir_Head, shape keys on the head).
- Project copy (same content) remains in Art/Character/Kabir_v02/.
