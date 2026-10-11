# PROJECT REVOLUTION — Next Development Steps
## Concrete Tasks & Dependency Roadmap for Phase 4

**Classification:** Immediate Development Action Plan  
**Target Horizon:** Next 3 Milestones  
**Date:** October 11, 2026  

---

## 1. Top 3 Concrete Development Tasks

```mermaid
flowchart LR
    Task0["Task 0: Vernacular Middle School (District C)\n• Modular colonial brick classroom\n• Veranda archways & iron bell tower\n• Desks, benches & blackboard\n[STATUS: COMPLETED & VALIDATED]"]
    
    Task1["Task 1: Living Civilian NPC System\n• Punjabi artisan & vendor routines\n• Ambient crowd audio loops\n• Water-carrier Bhishti & Halwai tea maker\n[STATUS: IMMEDIATE NEXT]"]
    
    Task2["Task 2: Early Story Narrative Mission Slice\n• Act I Quest: 'The Morning Courier'\n• Deliver tailored coat & buy chai kulhads\n• First encounter with Rowlatt Act proclamation\n[STATUS: READY FOR WIRING]"]

    Task0 --> Task1
    Task1 --> Task2
```

---

### Task 0: Construct District C — The Vernacular Middle School [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE**
- **Implemented Components:**
  - Gateway Archway & bilingual Vernacular School plaque (`SM_School_Signboard`).
  - Schoolyard Central Iron Bell Tower (`SM_School_Bell_Tower_Iron`) at $(1350, 1350, 0)$.
  - Classroom 4B Brick Compound with entrance doorway, arched windows, and solid walkable roof slabs at $Z = 400\text{ cm}$.
  - Classroom Interior: Dual student desk benches (`SM_School_Desk_Bench_Wood`), timber-framed slate blackboard (`SM_School_Blackboard_Easel`), and evening literacy lantern.
  - Family Workshop: Singer sewing machine (`SM_Prop_SewingMachine_Singer`), tailor charpai, and chai kulhad at $(200, 520, 0)$.

---

### Task 2: Implement Ambient Civilian NPCs & Daily Life Routines
- **Objective:** Populate Mohalla Darzian and Grand Bazaar with a small number of believable, historically grounded Punjabi townspeople.
- **Components:**
  - 4 foundational NPC archetypes:
    1. *The Halwai Tea Maker:* Boiling chai and pouring into clay kulhads at the Zone D stall.
    2. *The Water-Carrier (Bhishti):* Carrying leather goatskin water bag (*mashk*) near the communal well.
    3. *Kabir's Father (Darzi):* Working the foot-pedal sewing machine on the family veranda.
    4. *The Cloth Merchant:* Arguing prices over stacks of Manchester cotton.
  - Idle animation state machines and historical Urdu/Punjabi voice bark triggers.
- **Dependencies:**
  - Skeletal mesh mannequin rig binding.
  - Dialogue subsystem and NPC interaction trigger volumes.

---

### Task 3: Implement Act I Exploratory Quest — "The Morning Courier"
- **Objective:** Create the first playable story mission validating the entire journey from home to market.
- **Mission Flow:**
  1. Kabir wakes in the family courtyard; father asks him to take a repaired coat to the cloth merchant in the Grand Bazaar.
  2. Kabir climbs the stairs to the rooftop to check on his Basant fighter kite.
  3. Kabir vaults the roof parapet or descends to the Deorhi gateway, walks past the communal well, and enters the bazaar.
  4. Delivers the coat, overhears rumors about curfew sirens at the tea stall, and inspects the new colonial proclamation posted on the municipal board.
- **Dependencies:**
  - Tasks 1 & 2.
  - Quest objective triggers (`ObjectiveTriggerActor.cpp`).
