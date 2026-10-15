# Performance Tests

Counted (2026-10-11, L_Mohalla_Home): 282 static mesh actors, ~37,800 LOD0 triangles, 4 lights (sun, sky light, 2 interior point lights) plus sky atmosphere and height fog. 292 actors total after later changes.
No gameplay errors in the PIE log for this level.
NOT measured: frame rate, GPU/CPU time, memory, shader compile, Lumen cost, packaged build. Hardware not identified.

## Play measurement (2026-10-12, L_Mohalla_Home, GTX 1650, 16 GB, 8 threads)
- Method: Python tick callback inside the Editor's Play-in-editor session, sampling delta time while walking.
- Result: about 8 fps average. UNRELIABLE: the Editor UI, Python callback and PIE overhead all inflate frame time. Do not use this as a game frame rate.
- stat unit / stat fps: sent to the Play session; values are shown in the viewport and could not be read through the connection.
- NEXT: measure in a standalone game build or with the game launched outside the Editor, then record average fps, 1% low, frame time, and GPU time, at a fixed camera position.

## Standalone measurement (2026-10-12, L_Mohalla_Home, 1280x720 windowed)
- Method: game launched outside the editor (UnrealEditor.exe -game, same project), with csvprofile recording FrameTime. Stopped after about 60 s. Profile: Saved/Profiling/CSV/Profile(20261013_190620).csv.
- Hardware: NVIDIA GeForce GTX 1650 (4 GB), 16 GB RAM, 8 logical cores.
- Results (3,735 frames): average frame 7.94 ms (about 126 fps); median 7.75 ms; 1% worst average 22.1 ms (about 45 fps); 13 frames over 16.7 ms (below 60 fps); 4 frames over 33 ms (worst 89.6 ms).
- Caveats: the character was not moved during the run (idle at the spawn point), so this is the light case. Stairs, crowds, and the watchman/dog AI were not stressed. Lumen and screen percentage 75 are as set in the project. Output resolution 1280x720; the target display is not set.
- Next: repeat with the player walking through the market and up the roof stairs, and at 1920x1080 to match a typical target. Confirm the 4 large hitches (possibly load time).

## Standalone walk test at 1920x1080 (2026-10-12)
- Same project, standalone (UnrealEditor.exe -game), 1920x1080 windowed, csvprofile FrameTime. Profile: Profile(20261013_190900).csv.
- Input: simulated key presses on the game window (Shift+W for 12 s, then A and D for 3 s each). The route was NOT chosen to reach the stairs or market; it walks in the street and houses area. Treat as a light-walking sample.
- Results (3,337 frames): average 7.88 ms (about 127 fps); median 7.73 ms; 1% low 16.2 ms (about 62 fps); 9 frames over 16.7 ms; 2 frames over 33 ms; worst 43.7 ms.
- Comparison: the earlier 1280x720 idle run had a 1% low of about 45 fps and 4 frames over 33 ms. The 1080p walking run had a better 1% low, so the earlier hitches were likely load time, not gameplay.
- Still NOT tested: the market (crowded props), roof stairs under load, watchman/dog AI active, and Lumen worst case. Recommend a second run with a route that visits those areas.

## Standalone route test at 1920x1080 (2026-10-12, second run)
- Input: simulated keys and mouse (north 4 s, mouse turn east, then Shift+W for 14 s). Route was an attempt toward the market; the actual path was NOT verified (no in-game position readout from a standalone build).
- Profile: Profile(20261013_191405).csv, 3,040 frames.
- Results: average 8.18 ms (about 122 fps); median 7.81 ms; 1% low 25.1 ms (about 40 fps); 28 frames over 16.7 ms; 3 frames over 33 ms; worst 88.2 ms.
- Interpretation: the heavier stretch of this run pulled the 1% low below 60 fps, so the market, houses, and street traffic are the likely cost. Cause not isolated.
- Still open: confirm the route with a position log, and find which area causes the 1% lows.

## Timeline analysis of the route run (2026-10-12, Profile 191405, 1920x1080)
- Method: rebuilt a timeline from cumulative FrameTime (no timestamps in the CSV). The route script started 14 s after launch, walked forward 4 s, turned, then ran east from about 19 s. Timing is approximate (about +/-2 s).
- Steady frame time was about 8 ms in every 2-second window (roughly 120 fps) across the whole run.
- Slow frames came in short spikes, not sustained load: 45.6 ms around 16-18 s (forward walk), 88.2 ms around 20-22 s (start of the run), and smaller spikes of 20-38 ms in the first 10 s.
- Interpretation: the 1% low is caused by hitches, most likely asset streaming or first-time shader and material compilation when new areas come into view, not by the level's steady cost. The first run through a new area is where the spikes happen.
- Not yet confirmed: the cause of the spikes. A second run that repeats the same route should show whether the spikes recur (first-visit cost) or not (warm-up cost).
