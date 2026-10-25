# TASK 36 / PHASE 6.5.1: GRAND BAZAAR CHOWK MUNADI CROWD CLATTER & DYNAMIC DIALOGUE SYSTEM REPORT

**Project:** REVOLUTION (क्रांति) — 1919 Punjab Historical Narrative Stealth Open-World Experience  
**Engine Baseline:** Unreal Engine 5.5.4 LTS | Target Hardware: NVIDIA GeForce GTX 1650 (4GB VRAM)  
**Verification Date:** October 19, 2026  
**Status:** **100% COMPLETE & CERTIFIED (TEST-22 PASSED)**  

---

## 1. Executive Summary

Task 36 expands the central hub of Kot Gurdarshan—**Grand Bazaar Chowk**—into a living, culturally authentic, and dynamically responsive crowd scene reacting in real-time to General Dyer's proclamation of martial law:
- Added two brand new culturally grounded civilian archetypes:
  1. **Nikka Ram (`MunadiTownCrier`)**: The municipal town crier and dafli drummer of Amritsar, beating the nagara drum and reading the emergency Section 144 martial law proclamation.
  2. **Bhai Sant Singh (`ProtestElder`)**: A revered shopkeeper and community elder of Kot Gurdarshan, counselling non-violent restraint, courage, and communal unity during the Act II crisis.
- Engineered a **dynamic stage-aware dialogue and bark subsystem** (`SetDialogueModeForStage` and `HandleMissionDirectiveChanged`) allowing all existing and new mohalla civilians to dynamically transition their ambient barks and multi-line dialogues between peaceful morning errands (Act I) and the martial law curfew emergency (Act II).
- Implemented authentic procedural idle animations (dafli drumbeat arm rhythms and elder dignified sways), PBR heritage attire (saffron and undyed khadi cotton), and prop attachments (`SM_Munadi_Proclamation_Drum` and `SM_Prop_Pamphlet_Stack_Rowlatt`).
- Assembled authentic period crowd audio clatter (`SFX_Baisakhi_Crowd_Murmur` and `SFX_Crowd_Rally_Speech`) across the Bazaar Chowk.
- Certified via dedicated automated QA test suite `Scripts/verify_chowk_munadi_crowd.py` (`TEST-22`) with 6/6 passing subtests.

---

## 2. Architecture & Implementation Breakdown

### 2.1 C++ Civilian NPC System Expansion (`CivilianNPCActor.h` & `.cpp`)

1. **New Occupations in `ECivilianOccupation`:**
   - `MunadiTownCrier` (Nikka Ram, Amritsar Town Crier / Drummer)
   - `ProtestElder` (Bhai Sant Singh, Community Elder / Shopkeeper)

2. **Stage-Aware Dialogue Switching Architecture:**
   - Added `ActIIBarks` and `ActIIDialogues` arrays to `ACivilianNPCActor`.
   - Added `bIsInActIIMode` state flag and accessor `IsInActIIMode() const`.
   - Added `SetDialogueModeForStage(ECourierMissionStage NewStage)`:
     ```cpp
     const bool bShouldBeActII = (NewStage >= ECourierMissionStage::Stage_Afternoon_MunadiProclamation &&
                                  NewStage <= ECourierMissionStage::Stage_ActII_Completed);
     if (bIsInActIIMode != bShouldBeActII)
     {
         bIsInActIIMode = bShouldBeActII;
         CurrentDialogueIndex = 0;
     }
     ```
   - Bound `HandleMissionDirectiveChanged` to `URevolutionMissionSubsystem::OnMissionDirectiveChanged` in `BeginPlay()`, providing seamless automatic dialogue state switching when mission directives change.

3. **Dialogue Progression & Bark Selection:**
   - `AdvanceConversation()` and `GetCurrentDialogue()` dynamically select from `ActIIDialogues` when `bIsInActIIMode` is active, cycling smoothly through emergency dialogue lines.
   - `OnProximityBeginOverlap()` selects emergency barks from `ActIIBarks` when in Act II mode.

4. **Procedural Micro-Gestures (`Tick()`):**
   - **Nikka Ram (`MunadiTownCrier`)**: Sinusoidal rhythm simulating dafli drumstick strikes on the proclamation drum at 4.0 Hz with subtle chest pitch heave.
   - **Bhai Sant Singh (`ProtestElder`)**: Gentle contemplative yaw sway (0.25 Hz) with periodic dignified nodding motions (6.0s cycle).

5. **Heritage Attire PBR Materials (`ApplyHeritageAttireMaterials()`):**
   - **Nikka Ram**: Saffron kurta (`M_ClothSaffron_PBR`) in Slot 0, undyed cotton dhoti (`M_ClothUndyedCotton_PBR`) in Slot 1, saffron turban (`M_ClothSaffron_PBR`).
   - **Bhai Sant Singh**: All undyed khadi cotton (`M_ClothUndyedCotton_PBR`) in Slots 0 and 1, matching undyed cotton turban.

6. **Prop Attachment Mesh Configuration:**
   - `MunadiTownCrier`: `SM_Munadi_Proclamation_Drum` scaled to $(0.35, 0.35, 0.35)$ at local offset $(25, 0, -20)$.
   - `ProtestElder`: `SM_Prop_Pamphlet_Stack_Rowlatt` scaled to $(0.55, 0.55, 0.55)$ at local offset $(20, 15, -30)$.

---

### 2.2 Mission Subsystem & Objective Tracking (`RevolutionMissionSubsystem.cpp`)

- Updated `GetActiveObjectiveLocation` during `Stage_Afternoon_MunadiProclamation`:
  - Automatically queries the world for an active `ACivilianNPCActor` with `Occupation == ECivilianOccupation::MunadiTownCrier`.
  - Points compass ribbon and in-world diamond beacon directly to Nikka Ram at Grand Bazaar Chowk $(60, 1920, 10)$.
  - Fallback coordinates gracefully resolve to the Chowk Proclamation Drum Stand at $(80, 1920, 50)$.
- In `OnInteract_Implementation`: interacting with Nikka Ram during `Stage_Afternoon_MunadiProclamation` advances mission stage to `Stage_Afternoon_BaghNarrowEntry`, seamlessly updating the objective beacon to $(900, 2250, 50)$ (`"Jallianwala Bagh Choke-Point"`).

---

### 2.3 Level Assembly & Map Placement (`L_Validation_Gym.umap`)

- **Assembled Chowk Crowd NPCs:**
  - `NPC_Munadi_TownCrier`: Positioned at $(60.0, 1920.0, 88.0)$, Yaw $30.0^\circ$.
  - `NPC_BhaiSantSingh_Elder`: Positioned at $(140.0, 1860.0, 88.0)$, Yaw $120.0^\circ$.
- Saved permanently into `L_Validation_Gym.umap` (Total actors expanded to 230; total civilian NPCs expanded from 6 to 8).
- `RevolutionGameMode.cpp` includes fallback spawning logic ensuring both characters are dynamically instantiated if level lacks them.

---

## 3. Automated QA Suite (`Scripts/verify_chowk_munadi_crowd.py` / `TEST-22`)

The dedicated automated test suite executes 6 comprehensive subtests in headless editor commandlet mode:

| Subtest | Validation Target | Status |
| :--- | :--- | :---: |
| **Subtest 1** | Chowk Crowd Level Placement & Assembly in `L_Validation_Gym` (8 Civilian NPCs) | **PASS** |
| **Subtest 2** | Archetype Defaults, Props, Audio Loops, Heritage Attire & Routine Animation | **PASS** |
| **Subtest 3** | Dynamic Stage-Aware Dialogue Switching (Act I vs Act II Emergency Mode) | **PASS** |
| **Subtest 4** | Active Objective Resolution to Nikka Ram at Bazaar Chowk | **PASS** |
| **Subtest 5** | Mission Stage Advance to Bagh Narrow Entry at $(900, 2250, 50)$ | **PASS** |
| **Subtest 6** | Assembled Crowd Audio Clatter Packages (`SFX_Baisakhi_Crowd_Murmur`, `SFX_Crowd_Rally_Speech`) | **PASS** |

---

## 4. Master CI Regression Matrix (22 Suites Total)

```
================================================================================
  PROJECT REVOLUTION — MASTER CI TEST HARNESS EXECUTION SUMMARY
================================================================================
  TEST-01: Asset Structure Validation                          -> PASS
  TEST-02: Level Geometry & Actor Assembly Verification        -> PASS
  TEST-03: Material Interface & Texture Wiring QA              -> PASS
  TEST-04: Audio Mix & Sound Attenuation Verification          -> PASS
  TEST-05: Animation Blueprint & Retargeting Validation        -> PASS
  TEST-06: Enhanced Locomotion & Input System Integrity        -> PASS
  TEST-07: Core Gameplay Loop & Dynamic Objective Verification -> PASS
  TEST-08: Curfew & Detection AI Verification                  -> PASS
  TEST-09: Cinematic Sequences Verification                    -> PASS
  TEST-10: Quality of Life & Codex Verification                -> PASS
  TEST-11: Historical Epilogue Verification                    -> PASS
  TEST-12: Multi-Dialect Punjabi Voice Recording Expansion     -> PASS
  TEST-13: Dynamic Time-of-Day Weather States & Fog            -> PASS
  TEST-14: Curfew Sentry AI Collision Resolution               -> PASS
  TEST-15: Frontend Title Screen & Pause Menu System           -> PASS
  TEST-16: Persistent Disk Save/Load System (USaveGame)        -> PASS
  TEST-17: Procedural Skeletal Idle Animations & Routine Life  -> PASS
  TEST-18: Haveli Domestic Dressing & Boundaries               -> PASS
  TEST-19: Rooftop Traversal & Ladder Climbing System          -> PASS
  TEST-20: Seamless Act I In-World Objective Beacons           -> PASS
  TEST-21: Act I to Act II Cinematic Handoff Sequence          -> PASS
  TEST-22: Grand Bazaar Chowk Munadi Crowd & Dynamic Dialogue  -> PASS
================================================================================
  TOTAL SUITES: 22 | PASSED: 22 | FAILED: 0 | PASS RATE: 100.0%
================================================================================
```

---

## 5. Artifact & Source Deliverables

1. **C++ Source Files:**
   - [`CivilianNPCActor.h`](file:///C:/Users/npal7/PROJECT/REVOLUTION/Project/Source/REVOLUTION/CivilianNPCActor.h)
   - [`CivilianNPCActor.cpp`](file:///C:/Users/npal7/PROJECT/REVOLUTION/Project/Source/REVOLUTION/CivilianNPCActor.cpp)
   - [`RevolutionMissionSubsystem.cpp`](file:///C:/Users/npal7/PROJECT/REVOLUTION/Project/Source/REVOLUTION/RevolutionMissionSubsystem.cpp)
   - [`RevolutionGameMode.cpp`](file:///C:/Users/npal7/PROJECT/REVOLUTION/Project/Source/REVOLUTION/RevolutionGameMode.cpp)
2. **QA Test Suites & CI Harness:**
   - [`verify_chowk_munadi_crowd.py`](file:///C:/Users/npal7/PROJECT/REVOLUTION/Scripts/verify_chowk_munadi_crowd.py) (`TEST-22`)
   - [`run_all_tests.py`](file:///C:/Users/npal7/PROJECT/REVOLUTION/Scripts/run_all_tests.py)
   - [`run_all_tests.ps1`](file:///C:/Users/npal7/PROJECT/REVOLUTION/Scripts/run_all_tests.ps1)
3. **Map Asset:**
   - `/Game/Maps/L_Validation_Gym.umap` (230 actors, 8 civilian NPCs)
