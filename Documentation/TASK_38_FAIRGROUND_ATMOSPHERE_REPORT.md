# TASK 38 / PHASE 6.5.3: BAISAKHI FAIR GROUND ATMOSPHERE & GATHERING EXPANSION REPORT

**Project:** REVOLUTION (क्रांति) — 1919 Punjab Historical Narrative Stealth Open-World Experience  
**Engine Baseline:** Unreal Engine 5.5.4 LTS | Target Hardware: NVIDIA GeForce GTX 1650 (4GB VRAM)  
**Verification Date:** October 19, 2026  
**Status:** **100% COMPLETE & CERTIFIED (TEST-24 PASSED, 24/24 CI SUITES)**  

---

## 1. Executive Summary

Task 38 breathes historical life and emotional depth into the approach and outer perimeter of **Jallianwala Bagh** on the afternoon of **April 13, 1919**, capturing the vibrant cultural festival of Baisakhi before the tragedy:
- **Two New Grounded Historical Civilian Archetypes:**
  1. **Bhai Gurmukh Singh (`BaisakhiPilgrim`)**: A peasant farmer who traveled twenty miles by bullock cart from Tarn Taran with his family for the sacred Baisakhi dip (*snan*) at Sri Harmandir Sahib and the annual cattle fair. Unaware of the colonial district magistrate's proclamation or Section 144 martial law, he restfully waits in Jallianwala Bagh with thousands of fellow pilgrims.
  2. **Chacha Milkha (`FairVendor`)**: A beloved Punjab mela toy and sweet vendor selling spinning paper pinwheels (*firkiyan*), brass camel bells, and hot jalebis outside the garden gateway. He witnesses the arrival of British military lorries and shares crucial historical intelligence regarding General Dyer's armored cars getting stuck at the 2.2-meter alleyway mouth.
- **Authentic Heritage Attire, Props & Procedural Micro-Gestures:**
  - *Bhai Gurmukh Singh*: Sacred Baisakhi saffron turban (`M_ClothSaffron_PBR`), undyed khadi kurta (`M_ClothUndyedCotton_PBR`), aged teak dhoti (`M_AgedTeak_PBR`), attached jute grain sack prop (`SM_Prop_GrainSack_Jute_01`), and rhythmic crowd-scanning micro-gestures.
  - *Chacha Milkha*: Saffron kurta (`M_ClothSaffron_PBR`), indigo cotton lower (`M_ClothIndigo_PBR`), saffron turban (`M_ClothSaffron_PBR`), attached spinning pinwheel toy spool (`SM_Prop_Kite_Spool_Charkhi`), and hawker body gestures.
- **Festival Market Dressing & Historical Landmark Assembly:**
  - Assembled `Prop_Baisakhi_Mela_Sweet_Stall` at $(1020, 2440, 0)$ and `Prop_Baisakhi_Garland_Archway` at $(950, 2350, 0)$.
  - Placed persistent objective triggers in `L_Validation_Gym.umap` (237 actors):
    - `Trigger_Baisakhi_Pandal`: The Peaceful Baisakhi Assembly Dais at $(1450, 3100, 50)$ for `Stage_ActII_BaisakhiGathering`.
    - `Trigger_Shahidi_Kua`: The Martyrs' Well memorial site at $(1200, 2950, 50)$.
- **Dynamic Stage-Aware Dialogue Subsystem:**
  - Transition from Act I joyous festival chatter (wheat harvest, holy snan, spinning toys) to Act II emergency warnings (General Dyer's blocked armored cars, Gurkha riflemen marching inside on foot).
- **Master CI & Automated Verification:**
  - Certified via `Scripts/verify_baisakhi_fairground.py` (`TEST-24`) passing 6/6 subtests with 0 errors.
  - Master CI Harness expanded to 24 test suites with 100% pass rate.

---

## 2. Architecture & Implementation Breakdown

### 2.1 C++ Civilian NPC System Expansion ([`CivilianNPCActor.h`](file:///C:/Users/npal7/PROJECT/REVOLUTION/Project/Source/REVOLUTION/CivilianNPCActor.h) & [`.cpp`](file:///C:/Users/npal7/PROJECT/REVOLUTION/Project/Source/REVOLUTION/CivilianNPCActor.cpp))

1. **Enum Expansion (`ECivilianOccupation`):**
   ```cpp
   BaisakhiPilgrim, // Bhai Gurmukh Singh (Baisakhi Pilgrim / Rural Farmer)
   FairVendor       // Chacha Milkha (Baisakhi Fair Vendor / Toy & Sweet Seller)
   ```

2. **Heritage Attire PBR Assignment (`ApplyHeritageAttireMaterials()`):**
   - `BaisakhiPilgrim`: Slot 0 = `M_ClothUndyedCotton_PBR`, Slot 1 = `M_AgedTeak_PBR`, Turban = `M_ClothSaffron_PBR`.
   - `FairVendor`: Slot 0 = `M_ClothSaffron_PBR`, Slot 1 = `M_ClothIndigo_PBR`, Turban = `M_ClothSaffron_PBR`.

3. **Prop Attachments & Local Offsets:**
   - `BaisakhiPilgrim`: `SM_Prop_GrainSack_Jute_01` scaled to $(0.6, 0.6, 0.6)$ at $(20, 15, -40)$.
   - `FairVendor`: `SM_Prop_Kite_Spool_Charkhi` scaled to $(0.45, 0.45, 0.45)$ at $(22, 12, -15)$ with continuous procedural yaw spinning ($140^\circ/\text{s}$).

4. **Procedural Micro-Gestures (`Tick()`):**
   - `BaisakhiPilgrim`: 0.18 Hz yaw scanning ($\pm 2.8^\circ$) simulating calm contemplation of the gathered crowd, with 0.35 Hz breathing pitch rhythm.
   - `FairVendor`: Continuous prop yaw rotation ($140^\circ/\text{s}$) with 1.2 Hz vocal hawker chest heave and sway.

---

### 2.2 Game Mode & Dynamic Spawning ([`RevolutionGameMode.cpp`](file:///C:/Users/npal7/PROJECT/REVOLUTION/Project/Source/REVOLUTION/RevolutionGameMode.cpp))

- Expanded `CiviliansToSpawn` with:
  - `Bhai Gurmukh Singh`: $(1380, 3050, 10)$, rotation $(0, -60, 0)$.
  - `Chacha Milkha`: $(1050, 2400, 10)$, rotation $(0, 45, 0)$.
- In `SpawnDefaultMohallaProps()` fallback:
  - Scans active world for missing civilian archetypes and automatically instantiates missing NPCs to ensure all 10 civilian archetypes exist simultaneously.

---

### 2.3 Mission Subsystem Integration ([`RevolutionMissionSubsystem.cpp`](file:///C:/Users/npal7/PROJECT/REVOLUTION/Project/Source/REVOLUTION/RevolutionMissionSubsystem.cpp))

- During `Stage_ActII_BaisakhiGathering`:
  - Interacting with `Bhai Gurmukh Singh` or the `Trigger_Baisakhi_Pandal` dais advances the mission stage to `Stage_ActII_TheFiring`.
  - Next objective beacon seamlessly shifts to $(1250, 2800, 50)$ (`"The Firing Line"`).

---

## 3. Automated QA Verification (`TEST-24`)

The dedicated automated test suite [`verify_baisakhi_fairground.py`](file:///C:/Users/npal7/PROJECT/REVOLUTION/Scripts/verify_baisakhi_fairground.py) was executed via Unreal Editor Commandlet:

| Subtest | Verification Scope | Status | Result Detail |
|---|---|:---:|---|
| **Subtest 1** | Level Assembly of Fairground NPCs & Dressing | **PASS** | `NPC_BaisakhiPilgrim_Gurmukh`, `NPC_FairVendor_Milkha`, and festival stalls placed; 10 civilians verified |
| **Subtest 2** | Archetype Defaults, Props, Audio & Attire | **PASS** | Props, routine loops (`SFX_Baisakhi_Crowd_Murmur`, `SFX_Routine_ChaiStir_Loop`), and PBR attire verified |
| **Subtest 3** | Dynamic Stage-Aware Dialogue & Historical Lore | **PASS** | Act I harvest lore & Act II armored car passage constraint dialogue verified |
| **Subtest 4** | Assembly Pandal & Shahidi Kua Triggers | **PASS** | Pandal Dais at $(1450, 3100, 50)$ and Shahidi Kua at $(1200, 2950, 50)$ verified |
| **Subtest 5** | Mission Subsystem Progression to Gathering | **PASS** | Seamless stage progression from Gathering to The Firing Line at $(1250, 2800, 50)$ |
| **Subtest 6** | Fairground Audio Architecture & Population | **PASS** | 5 audio assets verified, 10 unique civilian occupations in scene, 237 total actors (< 260 budget) |

**Overall Result:** **ALL 6 SUBTESTS PASSED — 0 ERRORS (Commandlet runtime: 0.72s).**

---

## 4. Master CI Verification Matrix (24/24 Passing)

All 24 automated test suites in the Master CI Harness pass with 100% success:
- `TEST-01` to `TEST-23`: 100% PASS (Zero regression).
- `TEST-24`: Baisakhi Fair Ground Atmosphere & Gathering Expansion — **PASS**.
