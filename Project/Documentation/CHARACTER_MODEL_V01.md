# Kabir - Character Model v01 (Blender, separate asset)

Status: first build of a new child character, separate from the Unreal Manny placeholder. Not imported into Unreal yet. The current BP_Kabir still uses SKM_Manny. Nothing in the project was overwritten.

## Files
- Blender scene file: Art/Character/Kabir_v01/Kabir_v01.blend (contains only the character scene, collection Kabir_v01).
- FBX export: Art/Character/Kabir_v01/Kabir_v01.fbx (27 mesh parts, mesh only, no skeleton; applied scale, 1 unit = 1 m, forward -Y, up Z, face -Y).
- The Blender session also has an unrelated open file (Prop_Tailor_SewingMachine.blend) with a sewing workstation scene. It was not modified.

## What it is
- Child proportions, about 1.44 m tall (measured bounding box, feet at z 0 to head top 1.45 m). Target was 140-150 cm. Capsule is 142 cm, so the model is about 2 cm taller than the capsule. Acceptable for a preview; adjust if the capsule is kept at 142 cm.
- Head is large relative to body (child proportion), narrow chest, long legs relative to torso.
- Costume: undyed cotton kurta (cream-tan) over the torso, indigo half-pants at the hips and upper thighs, leather chappals.
- Face: simple eyes and ears only. No facial rig, no mouth or brows, no morph targets.
- Hands: simple mitten shapes. Hair: a single shell over the head.

## What it is NOT
- Procedural primitives (spheres, cylinders, cubes), not sculpted or retopologised. Not game-quality. Owner said quality is not the priority for now.
- No skeleton or rig; no animation; no UVs or textures (flat materials only).
- Not tested in Unreal (no skinning, no collision, no scale check in engine).

## Next steps for this asset
1. Import Kabir_v01.fbx into Unreal under a new folder (e.g. /Game/Characters/Kabir_v01/) without touching SKM_Manny or BP_Kabir.
2. Add a skeleton or retarget to SK_Mannequin (test compatibility as in CHARACTER_TECHNICAL_SPEC.md).
3. Test scale against the 142 cm capsule and the doorway (about 270 cm), then decide whether to swap BP_Kabir's mesh.
