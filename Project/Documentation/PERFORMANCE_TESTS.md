# Performance Tests

Counted (2026-10-11, L_Mohalla_Home): 282 static mesh actors, ~37,800 LOD0 triangles, 4 lights (sun, sky light, 2 interior point lights) plus sky atmosphere and height fog. 292 actors total after later changes.
No gameplay errors in the PIE log for this level.
NOT measured: frame rate, GPU/CPU time, memory, shader compile, Lumen cost, packaged build. Hardware not identified.

## Play measurement (2026-10-12, L_Mohalla_Home, GTX 1650, 16 GB, 8 threads)
- Method: Python tick callback inside the Editor's Play-in-editor session, sampling delta time while walking.
- Result: about 8 fps average. UNRELIABLE: the Editor UI, Python callback and PIE overhead all inflate frame time. Do not use this as a game frame rate.
- stat unit / stat fps: sent to the Play session; values are shown in the viewport and could not be read through the connection.
- NEXT: measure in a standalone game build or with the game launched outside the Editor, then record average fps, 1% low, frame time, and GPU time, at a fixed camera position.
