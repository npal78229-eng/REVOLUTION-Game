# Character Design Review - Phase 1, Milestone 1 (Claude's part)

Status: AWAITING APPROVAL. Per the plan, no Blender modelling (Milestone 2) until the face, proportions and clothing are approved.

## 1. Reference images supplied by the owner
Image A - head topology and shape-key reference (Blender 2.7x scene with a head, eyes, ear and two shape keys "Key 1" and "Key 2").
- Useful: shows a face built with separate shape keys for expressions (mouth and cheek regions highlighted). This is the approach we need for facial animation later (morph targets).
- Caution: the file is an existing model, and its source and licence are not known. Use it only as a technique reference. Do not copy or reuse its mesh without checking the licence.
- Not a child head: proportions look adult-to-teen, with a long neck.

Image B - three-view concept art (front, three-quarter, back) of a stylised child with a turban, blue scarf, layered blue outfit, gold trims, bamboo staff, sword hilt, and bare feet.
- Useful: clear silhouette, child proportions in a stylised way, readable colour blocking.
- Conflicts with the project brief (verified against PROJECT_DIRECTION.md):
  a. Style: chibi, very large head and eyes. The brief asks for believable child proportions, not cartoon.
  b. Costume: a fantasy-warrior look (weapons, gold bracers, layered wraps). The brief asks for an ordinary boy and realistic everyday clothing for rural UP c. 1910-1920.
  c. Headwear: a turban is tied to particular communities and religions. It has not been decided for this character. This needs your decision, not a default from me.
  d. Accessories: gold trims, a bamboo staff and sword are not part of an ordinary childhood. They would also conflict with the "Not yet added: colonial signage/uniforms" rule only in spirit; they are not historically grounded for this setting.

## 2. Technical requirements (Claude)
- Scale: 1 unit = 1 m. Target standing height 140-150 cm. Current capsule is 142 cm (keep unless you approve a change). A chibi head ratio (about 1:3) would make the character far shorter than the capsule. Recommended ratio for a 12-year-old: head about 1:5.5 to 1:6.
- Skeleton: reuse the Mannequin skeleton only for a first compatibility test. Proportions in the concept (short legs, big head) will not fit Mannequin animations well. Expect a new skeleton or a retarget step, and budget for it.
- Facial: close-up cinematics need shape keys (morph targets) for mouth, brows and eyes, plus eye bones. Image A's shape-key setup is the right kind of approach.
- Polygon budget: suggested LOD0 25k-35k tris for the face-and-body hero, LOD1 about 12k, LOD2 about 5k (see CHARACTER_TECHNICAL_SPEC.md). Stylised concept art does not change this budget.
- Gameplay camera: about 320 cm from the character at 90 degrees FOV, so the head is roughly 1/3 of screen height. Hands, feet and face detail matter less at gameplay distance and more in cutscenes.
- Turban or large hair volumes add polygons and cloth-collision work. Pick one and budget for it.

## 3. Decisions needed before Milestone 2
1. Headwear: no headwear (default recommendation), cap, or turban. If a turban, which community/style, and it must be historically and culturally checked.
2. Proportions and style: realistic-leaning child (recommended), or stylised like Image B.
3. Costume: undyed cotton kurta and shorts (or dhoti) as in CHARACTER_MODEL_V01, or a more colourful costume like Image B. Weapons and gold accessories: excluded by default.
4. Approve the face direction: age 12, skin tone, eye and hair direction. Reference images are not to be copied.

## 4. Existing model
Kabir_v01 (procedural primitives, see CHARACTER_MODEL_V01.md) is a placeholder for layout and scale checks only. It does NOT satisfy Milestone 2 (sculpted face and body, historical clothing, refined hands, feet, hair). Milestone 2 starts from the approved direction above.
