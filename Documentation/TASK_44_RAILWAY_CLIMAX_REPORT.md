# TASK 44: Act V — North Western Railway Cutting, Signal Gantry & Locomotive Climax

**Milestone:** Phase 6.5.8 — Task 44  
**Project:** REVOLUTION (क्रांति) — Historical Action-Adventure (Punjab, 1919)  
**Engine:** Unreal Engine 5.5.4 LTS | Target Platform: Windows 64-bit  
**Status:** **100% COMPLETE & VALIDATED IN-ENGINE (TEST-30 PASSED, 0 ERRORS)**  
**Date:** October 24, 2026  

---

## 1. Executive Summary

**Act V: The North Western Railway Cutting & Cantonment Infiltration** serves as the narrative and gameplay climax of *REVOLUTION*. Having survived the tragic assembly at Jallianwala Bagh, navigated the desolate curfew-cordoned alleys of the walled city, and linked with the resistance press at the Bhatta brick kiln, protagonist Kabir reaches the northern military boundary of Amritsar.

Here, the monumental North Western Railway (NWR) broad-gauge tracks pass through an excavated stone-and-brick cutting that strictly separates the indigenous old city from the British military cantonment and Civil Lines. A British standard 4-6-0 steam locomotive (`Punjab Mail`) stands idling at the depot siding, venting steam and coal smoke across the tracks.

In **Task 44**, we built, integrated, and verified the complete climactic infrastructure:
1. **Broad-Gauge Steam Locomotive & Pressure Relief System:** British Indian 4-6-0 locomotive engine with boiler headlamp, RDR2-inspired curl-noise coal smoke plume, and interactive steam pressure relief valve that releases a blinding cloud of pressurized steam to break enemy line of sight.
2. **Colonial Semaphore Signal Gantry & Maintenance Ladder:** 6.5-meter lattice-steel signal tower spanning the rail corridor, complete with high-level amber/green signal optics and climbable vertical ladder.
3. **Cantonment Gate Sentry Picket & Guardhouse:** Sentry watchman checkpoint guarding the fortified rail crossing with high-power searchlight illumination.
4. **Civil Lines Administrative Bungalow & Martial Law Archive:** Doric veranda bungalow housing the confidential military telegraph station and martial law documentation cabinet.
5. **Act V Mission Progression Integration:** Full validation of Stages 26 through 29 culminating in the Golden Sunrise finale handoff.

```mermaid
flowchart TD
    subgraph Railway_Depot_Engineering ["Railway Infrastructure & Steam Dynamics"]
        A["Locomotive_Engine_PunjabMail_Depot (1000, 3900, 30)<br/>(British 4-6-0 broad-gauge steam engine on track bed)"]
        B["Locomotive_Steam_Pressure_Relief_Valve (1000, 3880, 90)<br/>(Interactive valve releasing LOS-breaking steam cloud)"]
        C["Smoke_Plume_Locomotive_PunjabMail (1000, 4120, 360)<br/>(RDR2-inspired curl-noise coal smokebox plume)"]
        D["Light_Locomotive_Headlamp_Beam (1000, 4180, 160)<br/>(14000 lm volumetric beam piercing night mist)"]
    end

    subgraph Signal_Gantry_Climb ["Traversal & Verticality"]
        E["Colonial_Railway_Signal_Gantry_Junction (1160, 3960, 0)<br/>(6.5m lattice steel semaphore gantry)"]
        F["Ladder_Signal_Gantry_Climb (1175, 3960, 0)<br/>(ALadderActor climbing to signal deck)"]
        G["Light_Railway_Signal_Amber & Green (1160, 3960, 650)<br/>(Colonial kerosene semaphore optics)"]
    end

    subgraph Cantonment_Infiltration ["Military Perimeter & Intelligence Target"]
        H["Cantonment_Guardhouse_Picket_NorthGate (650, 4220, 0)<br/>(Fortified whitewashed sandbag sentry post)"]
        I["NPC_Cantonment_Sentry_NorthGate (650, 4200, 10)<br/>(CurfewPatrolAI watchman guarding gate crossing)"]
        J["Civil_Lines_Clubhouse_Bungalow_HQ (900, 4800, 0)<br/>(Colonial administrative bungalow)"]
        K["Prop_Cantonment_Archive_Cabinet_Veranda (820, 4520, 60)<br/>(Martial law telegraph archives & dockets)"]
    end

    A --> B
    A --> C
    A --> D
    E --> F
    E --> G
    H --> I
    J --> K
    F -.-> J
```

---

## 2. Implemented Components & Architectural Details

### 2.1 The Punjab Mail Steam Locomotive & Steam Obscurity Cloak
* **Locomotive Mesh:** `SM_Locomotive_Engine_PunjabMail` (`Locomotive_Engine_PunjabMail_Depot` at $X=1000, Y=3900, Z=30$).
* **Volumetric Coal Smoke Plume:** `Smoke_Plume_Locomotive_PunjabMail` anchored at smokebox chimney ($Z=360$) with `MI_Smoke_Haveli_Chimney`. Features multi-octave curl noise turbulence representing heavy bituminous coal firing.
* **Locomotive Headlamp:** `Light_Locomotive_Headlamp_Beam` ($14000\text{ lm}$, warm incandescent $255, 230, 180$, volumetric scattering $2.5$) casting dynamic silhouettes down the rail corridor.
* **Interactive Steam Pressure Relief Valve:** `Locomotive_Steam_Pressure_Relief_Valve` (`ALocomotiveSteamValveActor`). When turned by the player, vents high-velocity pressurized boiler steam, breaking sentry line of sight.

### 2.2 Semaphore Signal Gantry & Vertical Traversal
* **Gantry Structure:** `Colonial_Railway_Signal_Gantry_Junction` (`SM_Colonial_Railway_Signal_Gantry` at $X=1160, Y=3960, Z=0$).
* **Signal Optics:** Dual kerosene semaphore lanterns:
  - `Light_Railway_Signal_Amber` ($1800\text{ lm}$, amber warning at $Z=650$).
  - `Light_Railway_Signal_Green` ($1200\text{ lm}$, clear route at $Z=580$).
* **Climbable Maintenance Ladder:** `Ladder_Signal_Gantry_Climb` (`ALadderActor`). Provides seamless vertical traversal up to the $6.5\text{m}$ elevated catwalk, allowing the player to bypass ground sentries.

### 2.3 Cantonment Guardhouse & Sentry Picket
* **Picket Fortification:** `Cantonment_Guardhouse_Picket_NorthGate` at $(650, 4220, 0)$ with stacked sandbags and whitewashed brick outpost.
* **Sentry AI:** `NPC_Cantonment_Sentry_NorthGate` (`ACurfewPatrolAI`) at $(650, 4200, 10)$ with dynamic detection cone and lantern inspection routine.
* **Sentry Searchlight:** `Light_Cantonment_NorthGate_Sentry` ($1800\text{ lm}$) mounted to the guardhouse eaves.

### 2.4 Civil Lines Headquarters Bungalow & Telegraph Station
* **Administrative Bungalow:** `Civil_Lines_Clubhouse_Bungalow_HQ` at $(900, 4800, 0)$ with classical Doric veranda columns and hipped tiled roof.
* **Martial Law Archive Cabinet:** `Prop_Cantonment_Archive_Cabinet_Veranda` at $(820, 4520, 60)$ housing the colonial telegraph records.
* **Telegraph Station Prop:** `Prop_Cantonment_Telegraph_Station` at $(835, 4515, 95)$ dressed with photogrammetry brass material.
* **Veranda Illumination:** `Light_Cantonment_Archive_Veranda` ($1500\text{ lm}$, warm $255, 210, 130$).

---

## 3. Automated In-Engine Verification Results

The automated headless test suite `Scripts/verify_act5_railway_climax.py` (`TEST-30`) executed via `UnrealEditor-Cmd.exe` against `/Game/Maps/L_Validation_Gym`:

| Subtest | Component / Verification Target | Expected Value / Criteria | Result |
| :--- | :--- | :--- | :--- |
| **Subtest 1** | Locomotive Engine & Steam Cloak Infrastructure | Engine, steam valve, smoke plume, and headlamp present | **PASS** |
| **Subtest 2** | Semaphore Signal Gantry & Climbable Ladder | Gantry tower, amber/green signals, ladder actor present | **PASS** |
| **Subtest 3** | Cantonment Gate Sentry Picket & Guardhouse | Picket outpost, sentry watchman AI, lantern present | **PASS** |
| **Subtest 4** | Civil Lines Headquarters & Telegraph Archive | Bungalow HQ, archive cabinet, telegraph prop, veranda light | **PASS** |
| **Subtest 5** | Act V Mission Progression Stages | Stages 26, 27, 28, 29 registered and valid | **PASS** |

**Summary Result:** **5 / 5 SUBTESTS PASSED (0 ERRORS)**  
JSON Evidence File: `Documentation/test30_act5_railway_climax_results.json`

---

## 4. Next Milestone: Task 45 (Master Gold Master Release & Full Packaging Certification)

With all narrative acts (Acts I through V), all 30 automated test suites, RDR2 volumetric smoke systems, and full level dressing completed, we proceed to **Task 45: Master Gold Master Release Build, Packaging & Final Project Certification**.
