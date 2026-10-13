# REVOLUTION - Initial Project Direction

Decisions below are from the owner (2026-10-12). Status of each item: CONFIRMED (verified in project), DECIDED (owner decision, not yet implemented), or OPEN.

## 1. Setting - DECIDED
Fictional rural North India inspired by Uttar Pradesh, circa 1910-1920.
Research status: partial. See HISTORICAL_REFERENCE_NOTES.md for sources and gaps. Not yet confirmed by an expert or primary source for the 1910s.

## 2. Capsule - DECIDED: keep 142 cm
CONFIRMED: capsule half height 71 cm (142 cm), radius 32 cm. Movement: step height 45 cm, walk 380 cm/s, jump 500. Doorway opening about 270 cm (door leaf). Camera boom 320 cm.
Movement still works with the current capsule (tested with the Mannequin mesh).

## 3. Foot offset - DONE, KEPT at -71
CONFIRMED by Play test: original -90 left the feet 16.85 cm below the floor; -71 places them 2.15 cm above it. Walking and jumping were unchanged. Original value recorded in FOOT_OFFSET_TEST.md.
Remaining: the 2.15 cm gap from the spawn height may need a small Player Start height fix (not changed).

## 4. Facial animation - OPEN (cannot be done yet)
CONFIRMED: SKM_Manny has 0 morph targets. The project has no facial setup.
UNVERIFIED: whether the Mannequin skeleton has any facial bones. The connection did not expose the bone list.
RECOMMENDATION: bone-based face is only possible if the new rig includes facial bones. Plan the rig with them from the start. Morph targets later for detailed expressions (they need to be authored in Blender and imported on the mesh).

## 5. Skeleton - OPEN, decision needed
CONFIRMED: Mannequin skeleton (SK_Mannequin) with ABP_Manny; animations are adult-proportioned Mannequin clips.
NOT TESTED: compatibility with any child-proportioned mesh (no such mesh exists yet).
Trade-offs:
- Reuse Mannequin skeleton: keeps all existing animations and ABP working; risks adult-proportion animations looking wrong on a child (limb ratios, foot placement), and the child mesh must be fitted to the Mannequin bones.
- New child skeleton: best fit for child proportions and possible facial bones; requires new animation retargeting, a new ABP, and rebuilding locomotion. More work and risk.
Recommendation: keep the Mannequin skeleton for the first mesh test. Only build a new skeleton if the child mesh fails the compatibility test (animations visibly wrong).

## 6. Hardware and performance - PARTLY CONFIRMED
CONFIRMED from this PC (via Windows): GPU NVIDIA GeForce GTX 1650 (4 GB VRAM), plus Intel UHD integrated graphics (1 GB); 16 GB RAM; 8 logical CPU cores.
CONFIRMED project settings (DefaultEngine.ini): Lumen dynamic global illumination and reflections enabled (method 1); hardware ray tracing off; screen percentage 75; texture pool 1800 MB; Nanite streaming pool 512.
ASSESSMENT: the GTX 1650 is an entry-level card. Lumen and 2K textures are workable but tight. "Scalable mid-range" should be tested on this machine first; if frame rate is poor, reduce Lumen quality or screen percentage rather than texture size.
NOT MEASURED: frame rate, GPU time, memory use in Play. Next step: measure with stat fps / stat unit in Play.
Protagonist texture start: 2K (2048) for face and head, 1K for body and clothing (per owner's 2K direction, body at 1K saves VRAM).

## 7. Budget - DECIDED
Free tools only. No paid plugins, assets or tools without owner approval. Blender is free. Antigravity status: the owner's tool; cost not verified.

## Protected items
No existing assets were deleted or overwritten. BP_Kabir mesh offset changed from -90 to -71 (original recorded). No other unrelated systems were changed.
