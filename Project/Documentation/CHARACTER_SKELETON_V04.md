# Kabir v04 - Skeleton (rig) status

## Done
- Blender armature Kabir_Armature: 21 bones, root -> pelvis -> spine_01..03 -> neck_01 -> head; clavicle, upperarm, lowerarm, hand (left and right); thigh, calf, foot (left and right). Names follow UE5 Mannequin style.
- Automatic weights bound to v04_Body, v04_Head, v04_Kurta, v04_Shorts (21 groups each).
- Pose test: upper arm L and thigh R bent; the mesh followed without tearing. Pose reset before export.
- Files: Art/Character/Kabir_v04/Kabir_v04_rig.fbx and Kabir_v04_rig.blend.
- Unreal: imported as skeletal mesh /Game/Characters/Kabir_v04_Rig/Kabir_v04_rig with its own skeleton Kabir_v04_rig_Skeleton. Height 144.2 cm.

## Not compatible yet (verified by design, not by bone list)
- The Mannequin skeleton (SK_Mannequin) has extra bones that this rig lacks: extra spine (spine_04, spine_05), twist bones, finger bones, ball_l/r, and others. Existing Mannequin animations cannot play on this rig directly.
- Bone list could not be read through the Unreal connection, so the exact missing list is not confirmed.

## Next
1. Add the missing Mannequin bones in Blender (spine_04/05, ball_l/r, finger chains) and re-bind weights, or
2. Create an IK Rig for both skeletons and use the IK Retargeter to play Mannequin animations on this rig.
3. Then test idle, walk, run and jump in a test level before touching BP_Kabir.

## Update 2026-10-12 - Mannequin bone names added
- Exported reference skeleton from SKM_Manny to Art/Character/Reference/SKM_Manny_reference.fbx and read its full list in Blender: 160 bones, including spine_04/05, neck_02, ball_l/r, finger chains (metacarpal and 01-03; thumb 01-03), twist/corrective bones, and ik_* control bones.
- Added 43 bones to Kabir_Armature (now 64 bones): spine_04, spine_05, neck_02, ball_l/r, and finger chains for both hands. Positions taken from reference offsets, scaled by 0.886 to match the 1.44 m figure.
- NOT added: twist, corrective and tricep/bicep bones; ik_* controls; weapon bones; clavicle_pec, latissimus, scapula bones. Animations that depend on these may not match.
- Weights re-bound (automatic) to all four meshes: 64 groups each.
- Pose test: upper arm, thigh and index finger bent; mesh followed.
- Files: Art/Character/Kabir_v04/Kabir_v04_rig.fbx and Kabir_v04_rig.blend (updated). Unreal: /Game/Characters/Kabir_v04_Rig/Kabir_v04_rig (64 bones; height 144.2 cm).
- Next: IK Rig for both skeletons and IK Retargeter, then test idle/walk/run/jump in the test level. Not yet done.

## Status 2026-10-12
- PAUSED. Retargeting work set aside to return to the performance investigation at the owner's request. Resume from the Next steps above.
