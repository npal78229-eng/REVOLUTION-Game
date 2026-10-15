# Kabir - Character Model v04

Saved: Documents/Blender/Kabir_v04/Kabir_v04.blend (scene Kabir_v04).

## Changes from v02/v03
- Kurta and shorts are now fitted shells carved from the body itself (about 1.2 cm thick, smoothed), so they sit on the body instead of floating as separate blocks.
- Body and head smoothed with subdivision (from v03).
- Head keeps the expression shape keys from v02 (Smile, Brows_Up).

## Still not satisfactory
- Body, face, hands and feet are still primitive-based and mannequin-like. Clothing is shell-based, with no folds or fabric shape.
- Hairline and face are basic. No sculpted features.

## Next
- Sculpting by a person or a free base-body tool, as in CHARACTER_MODEL_V03.md. Keep v04 as the layout reference.

## Fit pass (2026-10-12)
- Kurta and shorts are shrink-wrapped to the body surface (outside, 1.2 cm and 1.0 cm offset), then thickened and smoothed. File re-saved at Documents/Blender/Kabir_v04/Kabir_v04.blend.
- Shorts edge is a little lumpy at the hips; the body is still primitive-based.

## Export and Unreal import (2026-10-12)
- Shorts smoothed (Relax modifier, factor 0.6, 10 iterations). Blender file re-saved to Art/Character/Kabir_v04/Kabir_v04.blend and Documents/Blender/Kabir_v04/Kabir_v04.blend.
- FBX exported to Art/Character/Kabir_v04/Kabir_v04.fbx and imported to /Game/Characters/Kabir_v04/ as four static meshes (v04_Body, v04_Head, v04_Kurta, v04_Shorts). Not merged this time.
- Heights in Unreal: body 0.1..144.3 cm; kurta 63.6..111.4 cm; shorts 64.1..81.6 cm. Figure height 144.2 cm.
- Test level L_Character_Test_v02 shows the four v04 parts at the origin.
- Playable BP_Kabir is still SKM_Manny. Not changed.
- Still open: merging or keeping the four meshes, skeleton and rig, and any decision to replace the playable character.
