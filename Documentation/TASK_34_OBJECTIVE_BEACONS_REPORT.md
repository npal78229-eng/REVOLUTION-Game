# PROJECT REVOLUTION — Task 34 Completion Report
## Seamless Act I In-World Objective Beacons & Mohalla Compass Waypoint Indicators

**Document ID:** `TASK-34-REPORT`  
**Milestone:** Phase 6.4.2 — In-World Objective Beacons & Compass Indicators  
**Engine Version:** Unreal Engine 5.5.4 LTS  
**Target Hardware Baseline:** NVIDIA GeForce GTX 1650 (4GB VRAM) / 1080p 30+ FPS  
**Date:** October 19, 2026  
**Status:** **100% COMPLETE & VERIFIED IN-ENGINE (TEST-20 PASSED, 20/20 MASTER CI PASSING, 0 ERRORS)**  

---

## 1. Executive Summary

Task 34 achieves **Phase 6.4.2** of the Post-Audit Master Development Plan, resolving key navigational friction in Kot Gurdarshan by introducing grounded, period-authentic in-world objective beacons and mohalla compass waypoints for Kabir's historical 1919 Act I courier journey.

Prior to Task 34, objectives were communicated solely via a 2D parchment banner in the top-left HUD (`DrawMissionDirectiveBanner`) and chalk scout marks on walls (`AChalkMarkActor`). Navigating through dense, winding Lahori brick mohalla alleys between the family haveli, the communal well, the Grand Bazaar, and the Vernacular Middle School lacked intuitive visual alignment without resorting to immersion-breaking modern mini-maps.

Task 34 seamlessly resolves this by:
1. Enhancing `URevolutionMissionSubsystem` with `GetActiveObjectiveLocation(FVector& OutLocation, FText& OutObjectiveName)`, dynamically resolving 3D coordinates and authentic landmark titles across all 8 Act I story stages and Acts II–V historical milestones.
2. Implementing `ARevolutionHUD::DrawInWorldObjectiveBeacon` using dynamic world-to-screen projection (`ProjectWorldLocationToScreen`), displaying an antique brass/gold diamond marker with subtle breathing pulse, perspective distance tag (`[ OBJECTIVE — 18m ]`), landmark header, and vertical anchor stem.
3. Implementing distance-dependent alpha attenuation that feathers in at 40m (or 80m during Basant Intuition / Keen Senses) and smoothly fades out below 3.0m down to 1.2m, completely preventing visual clutter during close-up dialogue and inspection.
4. Projecting the active objective bearing onto the mohalla top compass ribbon (`DrawCompass`) as an antique brass diamond waypoint with center gold pip whenever facing within the $\pm 40^\circ$ FOV.
5. Authoring automated headless test suite `Scripts/verify_objective_beacons.py` (`TEST-20`), validating 100% of subtests across all Act I stages and projection mathematics with `Success - 0 error(s)`.
6. Expanding the Master Continuous Integration test harness (`run_all_tests.py` and `run_all_tests.ps1`) to 20 suites: **100% PASS (20/20 SUITES PASSED) in 5.9 minutes**.

---

## 2. Technical Architecture & System Implementation

### 2.1 C++ Mission Subsystem Query Architecture (`URevolutionMissionSubsystem`)
In `Source/Revolution/RevolutionMissionSubsystem.h` and `.cpp`:
- Declared and implemented `bool GetActiveObjectiveLocation(FVector& OutLocation, FText& OutObjectiveName) const`:
  - **Dynamic Actor Resolution:** Queries active in-world instances first:
    - `AObjectiveTriggerActor`: checks matching `RequiredMissionStage` and `!bHasBeenTriggered`.
    - `ACivilianNPCActor`: checks matching `Occupation` (`FatherTailor`, `BhishtiWaterCarrier`, `ClothMerchant`, `HalwaiChaiVendor`) and returns `Civ->GetActorLocation() + FVector(0, 0, 90.0f)`.
    - Specific named level actors: `Haveli_Rooftop_Basant_Kite`, `Story_Curfew_Notice_Martial_Law_Chowk`, `School_Bell_Tower`, and `Story_School_Takhti_Slate`.
  - **Canonical Coordinates Fallback:** Ensures 100% deterministic fallback for every stage across Acts I–V even if an actor is culled or streaming.
  - **Completion State:** Returns `false` when `CurrentStage == ECourierMissionStage::Stage_Completed`.

### 2.2 In-World Tactical Objective Beacon (`ARevolutionHUD::DrawInWorldObjectiveBeacon`)
In `Source/Revolution/RevolutionHUD.h` and `.cpp`:
- Configured via `UPROPERTY(EditAnywhere, BlueprintReadWrite) bool bShowObjectiveBeacons = true`.
- **Dynamic 3D Projection:** Calls `PC->ProjectWorldLocationToScreen(ObjectivePos + FVector(0, 0, 35.0f), ScreenPos, true)`.
- **Range & Visibility Envelope:**
  - Standard exploration: $40\text{ m}$ visibility envelope.
  - Basant Intuition (Keen Senses, `V` key): extended $80\text{ m}$ envelope.
- **Dual Alpha Attenuation:**
  - Far-field feathering: smoothly interpolates alpha from $1.0$ down to $0.0$ between $30\text{ m}$ and $40\text{ m}$ ($60\text{ m}$ and $80\text{ m}$ with Keen Senses).
  - Near-field decluttering: smoothly drops alpha from $1.0$ down to $0.0$ between $3.0\text{ m}$ and $1.2\text{ m}$, ensuring clean framing for NPC dialogue and tactile inspection.
- **Grounded Visual Styling:**
  - Antique brass outer diamond: $(X \pm r, Y)$ and $(X, Y \pm r)$ with subtle perspective radius scaling ($7\text{ px} \dots 12\text{ px}$).
  - Inner concentric diamond with center gold pip.
  - Vertical anchor stem ($10\text{ px}$) pointing down to the physical prop/character.
  - Breathing pulse: $0.85 + 0.15 \times \sin(3.5 t)$.
  - Framed parchment badge with antique brass border showing `[ OBJECTIVE — 18m ]`.
  - Landmark title badge displayed within $25\text{ m}$ or during Basant Intuition.

### 2.3 Mohalla Compass Ribbon Waypoint Projection (`ARevolutionHUD::DrawCompass`)
- Dynamically queries `Subsystem->GetActiveObjectiveLocation(ObjectiveLoc, ObjectiveName)`.
- Calculates 2D planar direction vector and heading bearing:
  $$\Delta\theta = \text{atan2}(Y_{\text{obj}} - Y_{\text{player}}, X_{\text{obj}} - X_{\text{player}}) - \text{Yaw}_{\text{player}}$$
- Normalizes bearing delta to $[-180^\circ, 180^\circ]$.
- When within the compass ribbon visible half-range ($\pm 40^\circ$):
  - Computes ribbon screen X coordinate:
    $$\text{ScreenX} = \text{CenterX} + (\Delta\theta \times \text{PixelsPerDegree})$$
  - Renders a pulsing antique gold diamond waypoint ($5\text{ px}$ radius) with center pip directly on the top compass tape.

---

## 3. Act I Story Stage Objective Mappings

| Stage | Mission Objective | Target Actor / Anchor | 3D World Location | Landmark Title Displayed |
|---|---|---|---|---|
| **Stage 1** | Father's Tailor Dispatch | `NPC_RamLubhaya_Father` / Veranda | $(480.0, 500.0, 88.0)$ | *"Ram Lubhaya's Tailor Shop"* |
| **Stage 2** | Rooftop Basant Kite Survey | `Haveli_Rooftop_Basant_Kite` / Ledge | $(380.0, 200.0, 480.0)$ | *"Haveli Rooftop Basant Kite"* |
| **Stage 3** | Mohalla Well & Bhishti | `NPC_GhasitaBhishti_Water` / Well | $(-80.0, 1320.0, 88.0)$ | *"Ghasita Bhishti (Mohalla Well)"* |
| **Stage 4** | Grand Bazaar Cloth Guild | `NPC_LalaKaramChand_Cloth` / Mandi | $(200.0, 1980.0, 88.0)$ | *"Lala Karam Chand (Cloth Merchant)"* |
| **Stage 5** | Halwai Tea Stall Rumors | `NPC_HiraHalwai_Chai` / Tea Stall | $(-200.0, 1680.0, 88.0)$ | *"Hira Halwai's Tea Stall"* |
| **Stage 6** | Colonial Proclamation Notice | `Story_Curfew_Notice_Martial_Law_Chowk` | $(-80.0, 1850.0, 50.0)$ | *"Section 144 Proclamation Board"* |
| **Stage 7** | Ring Middle School Bell | `School_Bell_Tower` / Courtyard | $(1350.0, 1350.0, 60.0)$ | *"Vernacular Middle School Bell"* |
| **Stage 8** | Classroom 4B Student Desk | `Classroom 4B Desk` / `Story_School_Takhti_Slate` | $(1150.0, 1850.0, 35.0)$ | *"Classroom 4B Student Desk"* |

---

## 4. Verification & Quality Assurance (TEST-20)

### 4.1 Subtest Results Breakdown
Automated headless QA suite `Scripts/verify_objective_beacons.py` executed via `UnrealEditor-Cmd.exe`:

```
================================================================================
  PROJECT REVOLUTION — TASK 34 OBJECTIVE BEACONS & COMPASS WAYPOINTS QA (TEST-20)
================================================================================
Loaded gym level: /Game/Maps/L_Validation_Gym (228 actors)
--- Subtest 1: Verifying Mission Subsystem Objective Query Reflection ---
[PASS] Subsystem reflection verified: get_active_objective_location is present.
--- Subtest 2: Verifying All 8 Act I Mission Stages Objective Targets ---
Stage Stage 1: Father Ram Lubhaya Tailor Dispatch:
  Target: 'Ram Lubhaya's Tailor Shop' at (480.0, 500.0, 88.0)
Stage Stage 2: Rooftop Basant Kite:
  Target: 'Haveli Rooftop Basant Kite' at (380.0, 200.0, 480.0)
Stage Stage 3: Mohalla Well & Bhishti Ghasita:
  Target: 'Ghasita Bhishti (Mohalla Well)' at (-80.0, 1320.0, 88.0)
Stage Stage 4: Grand Bazaar Lala Karam Chand Cloth Guild:
  Target: 'Lala Karam Chand (Cloth Merchant)' at (200.0, 1980.0, 88.0)
Stage Stage 5: Halwai Tea Stall Rumors:
  Target: 'Hira Halwai's Tea Stall' at (-200.0, 1680.0, 88.0)
Stage Stage 6: Colonial Proclamation Notice:
  Target: 'Section 144 Proclamation Board' at (-80.0, 1850.0, 50.0)
Stage Stage 7: Ring Middle School Bell:
  Target: 'Vernacular Middle School Bell' at (1350.0, 1350.0, 60.0)
Stage Stage 8: Classroom 4B Student Desk:
  Target: 'Classroom 4B Student Desk' at (1150.0, 1850.0, 35.0)
[PASS] All 8 Act I story stages resolved authoritative 3D positions & landmark names.
--- Subtest 3: Verifying Completed Journey Returns None (False) ---
[PASS] Stage_Completed correctly returned None (terminal objective state).
--- Subtest 4: Verifying Acts II-V Milestone Coordinates ---
  Milestone STAGE_AFTERNOON_MUNADI_PROCLAMATION -> 'Munadi Proclamation Drum' at (80.0, 1920.0, 50.0)
  Milestone STAGE_AFTERNOON_BAGH_NARROW_ENTRY -> 'Jallianwala Bagh Choke-Point' at (900.0, 2250.0, 50.0)
  Milestone STAGE_ACT_II_THE_FIRING -> 'The Firing Line' at (1250.0, 2800.0, 50.0)
  Milestone STAGE_ACT_III_NIGHT_CURFEW_FALL -> 'Central Chowk Curfew Notice' at (-80.0, 1850.0, 50.0)
  Milestone STAGE_ACT_IV_REACH_CANAL_DISTRIBUTARY -> 'Canal Sluice Regulator' at (-950.0, 2200.0, 50.0)
  Milestone STAGE_ACT_V_CLIMB_SIGNAL_GANTRY -> 'Semaphore Signal Gantry' at (1160.0, 3960.0, 50.0)
[PASS] Acts II-V milestone objectives successfully verified.
--- Subtest 5: Verifying Spatial Alpha & Range Calculation Logic ---
[PASS] Distance alpha scaling, smooth close-up fadeout, and Basant Intuition range extension verified.
--- Subtest 6: Verifying Compass Ribbon Bearing Projection Math ---
[PASS] Compass ribbon bearing angle normalization and viewport projection math verified.
--- Subtest 7: Verifying ARevolutionHUD Configuration ---
[PASS] ARevolutionHUD bShowObjectiveBeacons defaults to True.
================================================================================
  ALL SUBTESTS PASSED (7/7) — TASK 34 OBJECTIVE BEACONS CERTIFIED
================================================================================
Success - 0 error(s)
```

---

## 5. Master CI Harness 20-Suite Certification

Following integration of `TEST-20` into `Scripts/run_all_tests.py` and `Scripts/run_all_tests.ps1`, the entire 20-suite automated test matrix executed:

```
================================================================================
  PROJECT REVOLUTION — MASTER CI VERIFICATION SUMMARY REPORT
================================================================================
ID         STATUS   DURATION   TEST SUITE NAME
--------------------------------------------------------------------------------
TEST-01    PASS     17.35s     Quality-of-Life, Satchel Modal & Historical Codex
TEST-02    PASS     17.92s     Audio Mix, SoundClass Hierarchy & Dynamic Curfew Filter
TEST-03    PASS     17.58s     Cinematic Camera Sequences & C++ Director Actor
TEST-04    PASS     24.69s     Act I Narrative Story Questline & Landmarks (205 Actors)
TEST-05    PASS     17.14s     Master PIE & Story Simulation (27 Milestones across Acts I-V)
TEST-06    PASS     0.11s      Standalone Build Cook, IoStore Packaging & GTX 1650 Budget
TEST-07    PASS     18.95s     Civilian Dialogue Voice Localization & Ambient Proximity Audio
TEST-08    PASS     18.22s     Pedestrian Reaction, Dynamic Stumble & Curiosity System
TEST-09    PASS     17.80s     SteamOS & Handheld Proton Scalability Profile & Controller Mappings
TEST-10    PASS     20.54s     Advanced Photogrammetry Texturing & Material Architecture
TEST-11    PASS     17.67s     Historical Narrative Epilogue, Codex 18th Record & Cinematic Director
TEST-12    PASS     21.62s     Multi-Dialect Punjabi Voice Recording Expansion & Bazaar Walla System
TEST-13    PASS     17.38s     Dynamic Time-of-Day Weather States, Andhi Dust Storm & Volumetric Fog
TEST-14    PASS     17.31s     Curfew Sentry AI Collision Resolution & 3-Waypoint Patrol Routine
TEST-15    PASS     17.64s     Frontend Title Screen, Pause Menu System & Checkpoint Restart Loop
TEST-16    PASS     17.73s     Persistent Disk Save/Load System (USaveGame) & Continue Journey Loop
TEST-17    PASS     17.35s     Procedural Skeletal Idle Animations, Occupational Routine Life & Heritage Attire
TEST-18    PASS     17.56s     Haveli Ground Floor Domestic Dressing & Village Exploration Boundaries
TEST-19    PASS     22.07s     Rooftop Traversal, Vertical Ladder Traversal & Mantling Feedback
TEST-20    PASS     17.63s     Seamless Act I In-World Objective Beacons & Mohalla Compass Waypoints
--------------------------------------------------------------------------------
================================================================================
  OVERALL RESULT: 100% PASS (20/20 SUITES PASSED) in 5.9 minutes!
  PROJECT REVOLUTION IS CERTIFIED GOLD MASTER READY!
================================================================================
```

---

## 6. Files Created or Modified

1. `Project/Source/Revolution/RevolutionMissionSubsystem.h`:
   - Declared `GetActiveObjectiveLocation(FVector& OutLocation, FText& OutObjectiveName) const`.
2. `Project/Source/Revolution/RevolutionMissionSubsystem.cpp`:
   - Included `EngineUtils.h`, `CivilianNPCActor.h`, and `ObjectiveTriggerActor.h`.
   - Implemented `GetActiveObjectiveLocation` with dynamic actor queries and canonical coordinate fallbacks.
3. `Project/Source/Revolution/RevolutionHUD.h`:
   - Declared `DrawInWorldObjectiveBeacon(ARevolutionCharacter* Kabir)`.
   - Declared `UPROPERTY(EditAnywhere, BlueprintReadWrite) bool bShowObjectiveBeacons = true`.
4. `Project/Source/Revolution/RevolutionHUD.cpp`:
   - Called `DrawInWorldObjectiveBeacon(Kabir)` in `DrawHUD()`.
   - Implemented `DrawCompass` active mission objective waypoint projection onto the compass tape ribbon.
   - Implemented `DrawInWorldObjectiveBeacon` with perspective scaling, breathing pulse, distance badge, and near/far alpha feathering.
5. `Scripts/verify_objective_beacons.py`:
   - Headless test suite (`TEST-20`) validating 8 Act I stages, later act milestones, distance alpha math, compass ribbon offset math, and HUD CDO properties.
6. `Scripts/run_all_tests.py` & `Scripts/run_all_tests.ps1`:
   - Registered `TEST-20` into master regression matrix.
7. `Documentation/TASK_34_OBJECTIVE_BEACONS_REPORT.md`:
   - Comprehensive technical completion and verification report.
