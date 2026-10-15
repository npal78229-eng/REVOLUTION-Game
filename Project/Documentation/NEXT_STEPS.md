# Next Steps

1. Confirm region/year (code hints: Punjab, 1919/1920s) and update HISTORICAL_REFERENCE_NOTES.md.
2. Play `L_Mohalla_Home`: check it looks right, keyboard input works, and the Inspect prompt/panel appears at the family-home props.
3. Fix visual issues found; place Balcony_Jharokha and Roof_Stairs; add street/alley detail; replace placeholder primitives; profile performance.

## Update 2026-10-12 (later)
- Check in Play: balcony placement, stairs connection, collisions near the doorway.
- Assign costume materials to Kabir (indigo kurta, undyed dhoti) once the period is confirmed.
- Confirm region/year with the owner.

## Update 2026-10-12 (stairs)
- Roof stairs (SM_Roof_Stairs_Masonry_01) are blocked and not climbable as placed. Owner to choose: decorative, ramp, or steps. See FOOT_OFFSET_TEST.md.

## Update 2026-10-12 (roof stairs done)
- Roof access tested in Play: climb, roof crossing, return, and descent all pass in scripted tests. Owner to confirm by playing.
- Next: replace brick cube steps with proper stair art if desired; check camera and visuals; then the performance measurement in a standalone build (still required).

## Retexture to-do (owner feedback 2026-10-12)
- Owner says the roof stairs look good for a preview, but the texture is weak. Retexture later: replace the plain M_LahoriBrick_PBR cube steps with proper stone or brick masonry textures. Geometry stays as it is.
- Owner has accepted the current layout for now.
