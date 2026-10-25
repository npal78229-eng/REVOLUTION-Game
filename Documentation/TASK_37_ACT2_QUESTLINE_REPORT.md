# TASK 37 / PHASE 6.5.2: ACT II QUESTLINE — "THE RUMORS OF BAISAKHI" REPORT

**Project:** REVOLUTION (क्रांति) — 1919 Punjab Historical Narrative Stealth Open-World Experience  
**Engine Baseline:** Unreal Engine 5.5.4 LTS | Target Hardware: NVIDIA GeForce GTX 1650 (4GB VRAM)  
**Verification Date:** October 19, 2026  
**Status:** **100% COMPLETE & CERTIFIED (TEST-23 PASSED, 23/23 CI SUITES)**  

---

## 1. Executive Summary

Task 37 deepens the historical stealth and narrative core of Act II (**"The Gathering Storm"**), advancing Kabir's journey from witnessing Nikka Ram's Munadi proclamation at Grand Bazaar Chowk into an undercover investigation through Amritsar's tense, curfew-patrolled mohallas:
- **Colonial Checkpost Eavesdropping Mechanic:**
  - Engineered stealth eavesdropping requirement (`bRequireStealthForInteraction`). Kabir must crouch, blend into crowd clusters, or remain under shadow concealment (score $> 0.25$) to eavesdrop on Imperial Police constables discussing General Dyer's 9th Gurkha and 54th Sikhs troop movements from Ram Bagh headquarters.
  - Accompanied by cloth rustle concealment feedback (`SFX_Conceal_Cloth_Rustle`).
- **Secret Meeting Leaflet Retrieval:**
  - Implemented contraband leaflet recovery from Lala Karam Chand's Swadeshi khadi cloth rolls (`SM_Prop_ClothRolls_Manchester`) at the textile mandi.
  - Trigger awards $+2$ Satyagraha rally handbills directly into Kabir's satchel inventory via `AwardPamphletsOnTrigger`, accompanied by crisp paper handling foley (`SFX_Pamphlet_Retrieve`).
- **Curfew Infiltration Route to Jallianwala Bagh:**
  - Dynamic route guidance directing Kabir through narrow back-alleys avoiding Constable Gurdial's curfew patrol zone toward the locked north choke-point $(900, 2250, 50)$ and onward into the Bagh assembly.
- **Mission Subsystem Architecture Expansion:**
  - Extended `ECourierMissionStage` with `Stage_Afternoon_EavesdropCheckpost` and `Stage_Afternoon_ClothBoltLeaflets`.
  - Authoritative compass waypoints and diamond objective beacons seamlessly track each phase in 3D world space.
- **Gym Level Assembly & Automated QA:**
  - Assembled `Trigger_Eavesdrop_Checkpost` and `Trigger_ClothBolt_Leaflets` into `/Game/Maps/L_Validation_Gym.umap` (231 level actors).
  - Authored headless verification suite `Scripts/verify_act2_questline.py` (`TEST-23`), passing 6/6 subtests with 0 errors.

---

## 2. Architecture & Implementation Breakdown

### 2.1 C++ Objective Trigger Actor (`ObjectiveTriggerActor.h` & `.cpp`)

1. **Stealth Verification Logic:**
   - Added `bRequireStealthForInteraction` (default `false`).
   - In `CanInteract_Implementation(APawn* Interactor)`:
     ```cpp
     if (bRequireStealthForInteraction)
     {
         ARevolutionCharacter* RevChar = Cast<ARevolutionCharacter>(Interactor);
         if (RevChar)
         {
             const bool bIsCrouched = RevChar->bIsCrouched;
             const bool bIsCrowdBlended = RevChar->IsCrowdBlended();
             const float ShadowConcealment = RevChar->GetShadowConcealmentScore();
             if (!bIsCrouched && !bIsCrowdBlended && ShadowConcealment < 0.25f)
             {
                 return false; // Player is standing in broad daylight; eavesdropping blocked
             }
         }
     }
     ```
2. **Satchel Leaflet Award System:**
   - Added `AwardPamphletsOnTrigger` (default `0`).
   - In `OnInteract_Implementation(APawn* Interactor)`:
     ```cpp
     if (AwardPamphletsOnTrigger > 0)
     {
         ARevolutionCharacter* RevChar = Cast<ARevolutionCharacter>(Interactor);
         if (RevChar)
         {
             RevChar->AddPamphlets(AwardPamphletsOnTrigger);
         }
     }
     ```

---

### 2.2 Mission Subsystem & Sequential Questline (`RevolutionMissionSubsystem.h` & `.cpp`)

1. **Enum Expansion (`ECourierMissionStage`):**
   ```cpp
   Stage_Afternoon_MunadiProclamation, // Step 9: Proclamation drum
   Stage_Afternoon_BaghNarrowEntry,     // Step 10: Choke-point discovery
   Stage_Afternoon_EavesdropCheckpost,  // Step 11: Listen to constable rumors
   Stage_Afternoon_ClothBoltLeaflets,   // Step 12: Retrieve hidden leaflets
   Stage_Act_II_BaisakhiGathering,     // Step 13: Enter garden gathering
   ```

2. **Stage Progression & Directives:**
   - `Stage_Afternoon_EavesdropCheckpost`:
     - English: *"Eavesdrop on the colonial police post behind the sandbag barricade."*
     - Majhi Punjabi: *"ਰੇਤ ਦੇ ਬੋਰਿਆਂ ਦੇ ਉਹਲੇ ਪੁਲਿਸ ਚੌਕੀ ਦੀ ਗੱਲਬਾਤ ਚੋਰੀ-ਛਿਪੇ ਸੁਣੋ।"*
   - `Stage_Afternoon_ClothBoltLeaflets`:
     - English: *"Retrieve the hidden Satyagraha rally handbills from Lala Karam Chand's khadi cloth bolts."*
     - Majhi Punjabi: *"ਲਾਲਾ ਕਰਮ ਚੰਦ ਦੇ ਖੱਦਰ ਦੇ ਥਾਨਾਂ 'ਚੋਂ ਸਤਿਆਗ੍ਰਹਿ ਦੇ ਪਰਚੇ ਕੱਢੋ।"*

3. **In-World Waypoints & Compass Ribbon:**
   - `Stage_Afternoon_EavesdropCheckpost`: $(-40.0, 2080.0, 50.0)$ (`"Colonial Checkpost Eavesdropping Post"`)
   - `Stage_Afternoon_ClothBoltLeaflets`: $(210.0, 1960.0, 50.0)$ (`"Lala Karam Chand's Cloth Bolt Stash"`)
   - `Stage_Act_II_BaisakhiGathering`: $(1450.0, 3100.0, 50.0)$ (`"Baisakhi Assembly Pandal"`)

---

### 2.3 Level Assembly & Dynamic Fallbacks (`RevolutionGameMode.cpp`)

- `ARevolutionGameMode::SpawnDefaultMohallaProps()` dynamically instantiates:
  - `Trigger_Eavesdrop_Checkpost`: Spawned at $(-40, 2080, 50)$, `bRequireStealthForInteraction = true`, `TriggerSound = SFX_Conceal_Cloth_Rustle`.
  - `Trigger_ClothBolt_Leaflets`: Spawned at $(210, 1960, 50)$, mesh `SM_Prop_ClothRolls_Manchester`, `AwardPamphletsOnTrigger = 2`, `TriggerSound = SFX_Pamphlet_Retrieve`.
- Both actors are permanently saved into `/Game/Maps/L_Validation_Gym.umap` (231 total actors).

---

## 3. Automated QA Verification (`TEST-23`)

The dedicated automated test suite `Scripts/verify_act2_questline.py` was executed via Unreal Editor Commandlet:

| Subtest | Verification Scope | Status | Result Detail |
|---|---|:---:|---|
| **Subtest 1** | Level Assembly of Act II Objective Triggers | **PASS** | `Trigger_Eavesdrop_Checkpost` and `Trigger_ClothBolt_Leaflets` present; 231 actors validated |
| **Subtest 2** | Checkpost Eavesdropping & Stealth Requirement | **PASS** | Stage=10, `bRequireStealthForInteraction=True`, `SFX_Conceal_Cloth_Rustle` verified |
| **Subtest 3** | Textile Mandi Cloth Stash & Satchel Increment | **PASS** | Stage=11, `AwardPamphletsOnTrigger=2`, `SM_Prop_ClothRolls_Manchester`, `SFX_Pamphlet_Retrieve` |
| **Subtest 4** | Mission Subsystem Sequential Act II Progression | **PASS** | Verified progression: Munadi -> Bagh Entry -> Eavesdrop -> Cloth Bolts -> Gathering |
| **Subtest 5** | Objective Coordinates & Compass Waypoints | **PASS** | Accurate 3D coordinates across all 5 Act II stages |
| **Subtest 6** | Curfew Route, Sentry AI & Soundscapes | **PASS** | Patrol AI, sandbag barricades, and 6 foley/crowd sound cues verified |

**Overall Result:** **ALL 6 SUBTESTS PASSED — 0 ERRORS (Commandlet runtime: 0.50s).**

---

## 4. Master CI Verification Matrix (23/23 Passing)

All 23 automated test suites in the Master CI Harness pass with 100% success:
- `TEST-01` to `TEST-22`: 100% PASS (Zero regression).
- `TEST-23`: Act II Questline: "The Rumors of Baisakhi" & Checkpost Eavesdropping — **PASS**.
