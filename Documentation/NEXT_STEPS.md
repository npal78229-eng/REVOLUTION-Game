# PROJECT REVOLUTION — Next Development Steps
## Concrete Tasks & Dependency Roadmap for Phase 4 & Phase 5

**Classification:** Immediate Development Action Plan  
**Target Horizon:** Next 3 Milestones  
**Date:** October 12, 2026  

---

## 1. Top Concrete Development Tasks

```mermaid
flowchart LR
    Task0["Task 0: District C Middle School\n• Modular brick classroom\n• Iron bell tower & desks\n[STATUS: COMPLETED & VALIDATED]"]
    
    Task1["Task 1: Living Civilian NPC & Foliage System\n• 5 Punjabi historical archetypes\n• Sacred Peepal & Tulsi shrines\n• Proximity barks & Satchel lore\n[STATUS: COMPLETED & VALIDATED]"]
    
    Task2["Task 2: Act I Story Narrative Questline\n• 'The Morning Courier'\n• Deliver tailored coat to merchant\n• Buy chai & ring school bell\n[STATUS: COMPLETED & VALIDATED]"]

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

### Task 1: Living Civilian NPC & Foliage System [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE**
- **Implemented Components:**
  - Dedicated C++ class `ACivilianNPCActor` implementing `IInteractableInterface`.
  - 5 authentic historical archetypes with unique lore, perspectives, and visual accessories:
    1. *Ram Lubhaya (Master Tailor / Kabir's Father):* Working Singer sewing machine on family veranda $(200, 480, 88)$.
    2. *Ghasita Bhishti (Traditional Water-Carrier):* Carrying leather goatskin *mashk* by the communal well $(-80, 1320, 88)$.
    3. *Hira Halwai (Tea Stall Owner):* Serving steaming cardamom chai kulhads at the Grand Bazaar stall $(-200, 1680, 88)$.
    4. *Lala Karam Chand (Cloth Merchant):* Managing Manchester & Swadeshi khadi bolts at the mandi stall $(200, 1980, 88)$.
    5. *Pandit Kashi Ram (School Headmaster):* Teaching and overseeing the schoolyard iron bell tower $(1350, 1420, 88)$.
  - Historical Foliage & Nature:
    - *Sacred Peepal Tree with Chabutra Shrine* (`SM_Foliage_PeepalTree_Shrine`) at $(380, 1350, 0)$ in Zone C.
    - *Courtyard Sacred Tulsi Planter Pedestal* (`SM_Prop_Tulsi_Pedestal`) at $(120, 80, 0)$ in Zone A.
  - Natural player tracking (smooth head/torso turn toward Kabir within 2.8m).
  - Ambient proximity barks and multi-line interactive dialogues displayed via Kabir's inspection modal.

---

### Task 2: Implement Act I Exploratory Quest — "The Morning Courier" [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE**
- **Implemented Components:**
  - Expanded `RevolutionMissionSubsystem` with full 8-stage Act I narrative loop:
    1. `Stage_Morning_FatherTailor`: Converse with master tailor Ram Lubhaya on the veranda.
    2. `Stage_Morning_RooftopKite`: Climb courtyard stairs, inspect Basant fighter kite, and survey mohalla rooftops.
    3. `Stage_Morning_WellBhishti`: Descend through Deorhi gateway, meet Ghasita Bhishti at communal well square.
    4. `Stage_Morning_DeliverCloth`: Enter Grand Bazaar, hand over tailored khadi coat to Lala Karam Chand.
    5. `Stage_Morning_ChaiHalwai`: Drink hot cardamom chai kulhad at Hira Halwai's stall; hear Rowlatt Act unrest rumors.
    6. `Stage_Morning_ProclamationBoard`: Inspect/deface Section 144 martial law curfew order on proclamation board.
    7. `Stage_Morning_SchoolBell`: Enter Vernacular Middle School courtyard and toll central wrought-iron bell (`SFX_Dawn_Temple_Bell`).
    8. `Stage_Morning_ClassroomDesk`: Take assigned pupil desk in Classroom 4B; complete Act I prologue (`SFX_Dawn_Gong_Complete`).
  - Integrated audio feedback triggers (`UGameplayStatics::PlaySoundAtLocation`) for bell tolling and objective fanfare.
  - In-game HUD objective tracker with Satchel Journal inventory tab tracking the Tailored Khadi Coat Parcel.
  - Validated with automated headless test suite `Scripts/verify_act1_questline.py` across all 114 level actors with 100% PASS rate.

---

## 2. Phase 5 Roadmap: Colonial Authority & Gathering Storm

```mermaid
flowchart LR
    Task3["Task 3: Colonial Constable Patrol AI\n• British Imperial Police & Indian Constables\n• Lantern line-of-sight & suspicion meter\n• Mohalla curfew enforcement"]
    
    Task4["Task 4: Underground Pamphlet Drop\n• Anti-Rowlatt Act leaflets\n• Rooftop dead-drops & pigeon coops\n• Dr. Saifuddin Kitchlew rallying network"]
    
    Task5["Task 5: The Road to Jallianwala Bagh\n• Baisakhi festival crowd simulation\n• Historic town square boundary expansion\n• April 13, 1919 historical culmination"]

    Task3 --> Task4
    Task4 --> Task5
```

### Task 3: Colonial Constable Patrol & Schoolmate Friend System [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE**
- **Implemented Components:**
  - `NPC_KartarSingh_Friend`: 12-year-old childhood schoolmate with custom kite spool prop, youthful scaling (0.72x), friendly banter, and dialogue at $(450, 1380, 88)$.
  - `NPC_Constable_Gurdial`: Punjab Imperial Police Constable actively patrolling Grand Bazaar between $(0, 1600, 88)$ and $(0, 2040, 88)$ with 3 waypoints and line-of-sight perception.
  - Total level actors expanded to 116 in `L_Validation_Gym.umap` (100% PASS on automated verification suite `Scripts/verify_act1_questline.py`).

---

### Task 4: Underground Pamphlet Drop & Secret Printing Network [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE**
- **Implemented Components:**
  - `ARevolutionCharacter`: Added contraband inventory `PamphletCount` (capacity 5), `AddPamphlets(Amount)`, and `DeliverPamphlets(Amount)`.
  - `ASupplyStashActor`: Extended with `ESupplyStashType::Pamphlets` ("Anti-Rowlatt Strike Handbills"), interactive prompts, and authentic rag-paper foley sound (`SFX_Pamphlet_Retrieve`).
  - `ACivilianNPCActor`: Integrated clandestine drop-off logic in `OnInteract_Implementation`. Interacting with Lala Karam Chand or Hira Halwai while carrying handbills stealthily delivers a leaflet (`DeliverPamphlets(1)`), triggering dedicated dialogue acknowledgement and gratitude.
  - `ACurfewPatrolAI`: Heightened suspicion mechanic in `CanSeePlayer`—carrying contraband handbills increases watchman visual detection rate by 30% (`StanceMultiplier *= 1.30f`).
  - `ARevolutionHUD`: Expanded Tab 1 (Satchel Equipment) with a dedicated 4th card displaying Satyagraha Strike Handbill inventory count, mission actions, and historical excerpts ("Na Dalil, Na Vakil, Na Appeal").
  - Automated verification suite `Scripts/verify_act1_questline.py` updated and passed with 100% SUCCESS across all 146 level actors.

---

### Task 5: The Road to Jallianwala Bagh — Baisakhi Gathering & General Dyer's Proclamation [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE**
- **Implemented Components:**
  - 5 authentic 3D monumental & period assets generated in Blender 5.2 LTS and dual-exported to `Art/Exports/`, `Art/PROJECT/`, and `PROJECT/`:
    1. `SM_Munadi_Proclamation_Drum`: Nagara kettle-drum on teak tripod stand with drum beaters, rim lacing, and British martial law proclamation parchment scroll.
    2. `SM_Baisakhi_Garland_Archway`: Grand festive portal spanning 4.2m with cascading marigold garlands (*Genda Phool*) and mango leaf festoons (*Toran*).
    3. `SM_Jallianwala_Narrow_Gateway`: Historic 2.2m claustrophobic corridor entrance flanked by 5m Lahori brick haveli walls and iron security wicket grille.
    4. `SM_Prop_Wheat_Sheaves_Cart`: Punjabi bullock harvest cart (*Bail Gadi*) with 1.3m spoked wheels and piled golden Baisakhi wheat sheaves.
    5. `SM_Baisakhi_Mela_Sweet_Stall`: Festive halwai market platform with hammered brass platters, golden jalebis, laddus, and paper bunting.
  - Ingested into `/Game/Environment/Mohalla/Meshes/` with complex collision and authentic PBR materials (`M_LahoriBrick_PBR`, `M_AgedTeak_PBR`, `M_ClothSaffron_PBR`, etc.).
  - Placed into active master level `L_Validation_Gym.umap` via automated assembler (`assemble_task5_baisakhi_gathering.py`), expanding total level actors to **165**.
  - Synthesized and ingested authentic 16-bit 44.1kHz audio assets:
    - `SFX_Munadi_Drum.uasset` (Nagara proclamation drum roll and resonant proclamation strikes).
    - `SFX_Baisakhi_Crowd_Murmur.uasset` (Festive gathering crowd swells with low-frequency murmurs).
  - C++ Mission & GameMode Expansion:
    - Extended `ECourierMissionStage` with 3 new Act II stages: `Stage_Afternoon_MunadiProclamation`, `Stage_Afternoon_BaghNarrowEntry`, `Stage_ActII_BaisakhiGathering`.
    - Integrated audio synchronization triggers and interactive historical inspection lore cards.
    - Added runtime dynamic trigger instantiation in `RevolutionGameMode::BeginPlay()`.
    - Recompiled `UnrealEditor-REVOLUTION.dll` (Exit code 0).
  - Validated with automated test suite `Scripts/verify_act1_questline.py` across all 165 actors, 7 NPCs, and 33 landmarks with **100% PASS** rate.

---

### Task 6: The Enclosed Garden of Jallianwala Bagh — Memorial Well, Enclosure Walls & British Troop Picket [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE**
- **Implemented Components:**
  - 5 authentic 3D monumental & historical assets generated in Blender 5.2 LTS and dual-exported to `Art/Exports/`, `Art/PROJECT/`, and `PROJECT/`:
    1. `SM_Jallianwala_Shahidi_Kua_Well`: Historic Martyrs' Well with octagonal masonry plinth, circular deep stone shaft, turned teak posts, protective hipped terracotta canopy, and iron pulley wheel.
    2. `SM_Jallianwala_Enclosure_Wall`: 4.5m tall blind Lahori brick haveli wall modules with pilaster buttresses, stepped cornices, and zero ground openings.
    3. `SM_Jallianwala_Raised_Bank`: 1.2m elevated tactical earthen/brick mound positioned inside the corridor mouth where General Dyer deployed his 50 riflemen.
    4. `SM_British_Armored_Car_Obstacle`: 1919 Austin/Crossley British armored vehicle with riveted armor hull, twin Vickers machine gun turret, and slotted driver visor blocked outside the 2.2m narrow gate.
    5. `SM_Jallianwala_Baisakhi_Pandal`: Woven white khadi platform dais with Persian carpet runner, masnad cotton bolsters, speech podium, and striped shamiana canopy.
  - Ingested into `/Game/Environment/Mohalla/Meshes/` with complex collision and period PBR materials (`M_LahoriBrick_PBR`, `M_AgedTeak_PBR`, `M_WroughtIron_PBR`, `M_DirtRoad_PBR`, `M_ClothSaffron_PBR`).
  - Placed 8 structures into active master level `L_Validation_Gym.umap` via automated assembler (`assemble_task6_jallianwala_garden.py`), expanding total level actors to **173**.
  - Synthesized and ingested authentic 16-bit 44.1kHz audio:
    - `SFX_Crowd_Rally_Speech.uasset` (Distant orator addressing the assembly with vocal formant peaks & sympathetic crowd murmurs).
    - `SFX_Military_Boot_March.uasset` (Cadence of heavy iron-hobnailed British military infantry boots stamping in unison).
  - C++ Mission & GameMode Updates:
    - Extended `RevolutionMissionSubsystem` with audio synchronization for rally speech and approaching boots.
    - Added runtime dynamic trigger spawning in `RevolutionGameMode::BeginPlay()` for the Martyrs' Well (`Trigger_Shahidi_Kua_Well`) and Assembly Dais (`Trigger_Jallianwala_Pandal`) with modal historical lore cards.
    - Compiled `UnrealEditor-REVOLUTION.dll` (Exit code 0).
  - Automated Verification:
    - Passed with **100% SUCCESS** in `verify_act1_questline.py` across **173 actors, 7 NPCs, and 41 landmarks**.

---

### Task 7: The Fateful Afternoon of April 13, 1919 — Crowd Panic Debris, Bugle Sound & Escape Traversal [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE**
- **Implemented Components:**
  - 4 authentic 3D historical & gameplay traversal assets modeled in Blender 5.2 LTS and dual-exported to `Art/Exports/`, `Art/PROJECT/`, and `PROJECT/`:
    1. `SM_Prop_Fallen_Turban_Shoes_Scatter`: Ground debris scatter capturing discarded pagris (saffron & white uncoiled turban wraps), 3 pairs of Punjabi curved-toe leather juttis, broken bamboo cane umbrellas, brass lotas, and shattered terracotta pottery.
    2. `SM_Jallianwala_Crumbling_Wall_Breach`: 4.4m wide x 1.75m high breached haveli brick wall section featuring climbable stepped brick talus ramp on the garden side (Z = 0.0 to 0.75m), placing the 1.75m fractured coping rim within 1.0m of Kabir's feet to allow parkour vault traversal into the rear alleyways.
    3. `SM_Prop_Bullet_Pocked_Brick_Slab`: Iconic 2.8m x 3.2m Lahori brick memorial wall section with indented bullet impact crater chips and white painted plaster marking frames as preserved at the national memorial.
    4. `SM_Prop_Makeshift_Timber_Ladder`: 3.6m tall rough-hewn bamboo/sal timber ladder with 10 cross rungs and hemp rope lashings leaned at 72 degrees against the north boundary wall.
  - Ingested into `/Game/Environment/Mohalla/Meshes/` with `CTF_USE_COMPLEX_AS_SIMPLE` collision and authentic PBR materials (`M_LahoriBrick_PBR`, `M_AgedTeak_PBR`, `M_ClothSaffron_PBR`, `M_Clay_PBR`, etc.).
  - Placed 6 structures into active master level `L_Validation_Gym.umap` via automated assembler (`assemble_task7_stampede_and_breach.py`), expanding total level actors to **179**.
  - Synthesized and ingested authentic 16-bit 44.1kHz audio:
    - `SFX_Bugle_Call_Charge.uasset` (British military bugle call fanfare in harmonic series C4-E4-G4-C5 signalling the firing order).
    - `SFX_Crowd_Panic_Scream.uasset` (Sudden stampede, vocal shouts/screams, frantic footfalls, and surging reverberations echoing off high enclosure walls).
  - C++ Gameplay & Mission System Expansion:
    - Extended `ECourierMissionStage` with Act II Climax stages:
      - `Stage_ActII_TheFiring` (Step 12: General Dyer orders fire; bugle call and rifle volleys).
      - `Stage_ActII_FindEscapeRoute` (Step 13: Panic in the enclosure; stampede debris navigation).
      - `Stage_ActII_VaultWallBreach` (Step 14: Vault the 1.8m crumbling wall breach).
      - `Stage_Completed` (Step 15: Act II Finale: Escape from Jallianwala Bagh).
    - Added runtime objective triggers in `RevolutionGameMode::BeginPlay()`:
      - `Trigger_TheFiring` at $(1250, 2800, 50)$ with bugle SFX.
      - `Trigger_FindEscape` at $(950, 3100, 50)$ with panic SFX.
      - `Trigger_VaultBreach` at $(680, 3320, 50)$ with completion fanfare.
    - Successfully recompiled `UnrealEditor-REVOLUTION.dll` (Exit code 0).
  - Automated Verification:
    - Headless verification suite `Scripts/verify_act1_questline.py` passed with **100% SUCCESS** across **179 actors, 7 NPCs, 47 landmarks, and 15 narrative stages**.

---

---

### Task 8: Act III — The Fateful Dusk & The Amritsar Curfew [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE**
- **Implemented Components:**
  - 4 authentic 3D historical & gameplay environment assets modeled in Blender 5.2 LTS and dual-exported to `Art/Exports/`, `Art/PROJECT/`, and `PROJECT/`:
    1. `SM_Prop_Searchlight_Tripod_Imperial`: Colonial carbon-arc searchlight with swivel collar, elevation yoke fork, exhaust vent hood, and heavy timber tripod with iron shoe spikes.
    2. `SM_Prop_Curfew_Notice_Martial_Law`: Walled city timber tripod easel displaying General Dyer's inflexible 8:00 PM shoot-on-sight curfew decree.
    3. `SM_Prop_Makeshift_Stretcher_Charpai`: Emergency survivor stretcher constructed with longitudinal bamboo carrying poles, cross braces, and torn cotton bandages.
    4. `SM_Checkpoint_Sandbag_Sentry_Bunker`: Fortified curved sandbag revetment with heavy timber shoring posts, firing embrasures, and corrugated iron roof.
  - Ingested into `/Game/Environment/Mohalla/Meshes/` with `CTF_USE_COMPLEX_AS_SIMPLE` collision.
  - Placed 5 curfew structures into `L_Validation_Gym.umap` via `assemble_task8_curfew_and_searchlight.py`, expanding level actors to **184**.
  - Synthesized and ingested authentic 16-bit 44.1kHz audio:
    - `SFX_Night_Cricket_Ambience.uasset` (High-frequency cricket bursts, hollow haveli canyon drafts, and distant mourning).
    - `SFX_Police_Whistle_Curfew.uasset` (Piercing Acme double-trill British colonial police curfew whistle).
  - C++ Mission & GameMode Updates:
    - Extended `ECourierMissionStage` with Act III stages: `Stage_ActIII_NightCurfewFall`, `Stage_ActIII_EvadeSearchlightPicket`, `Stage_ActIII_AidWoundedSurvivors`, and `Stage_ActIII_Completed`.
    - Spawning dynamic runtime triggers in `RevolutionGameMode::BeginPlay()` (`CurfewNoticeTrigger`, `SearchlightPicketTrigger`, `SecretStretcherClinicTrigger`) with modal historical lore cards.
  - Automated Verification:
    - `Scripts/verify_act1_questline.py` passed with **100% SUCCESS** across 184 actors, 7 NPCs, and 52 landmarks.

---

### Task 9: Act IV — The Rural Outskirts & Upper Bari Doab Canal Network [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE**
- **Implemented Components:**
  - 4 authentic monumental & industrial 3D assets modeled in Blender 5.2 LTS and dual-exported to `Art/Exports/`, `Art/PROJECT/`, and `PROJECT/`:
    1. `SM_Canal_Distributary_Aqueduct_Stone`: Historic Upper Bari Doab masonry canal distributary culvert with channel bed, brick revetments, stone coping, iron lift gate sheet with gear racks, twin handwheels, and inspection catwalk.
    2. `SM_Persian_Wheel_Rahat_Timber`: Indigenous Punjabi Persian wheel water lifter with 3.0m vertical wooden drive wheel, 8 turned terracotta *tind* water pots on continuous chain loops, horizontal spur cog gear, bullock draught beam, and timber flume trough.
    3. `SM_Brick_Kiln_Chimney_Bhatta`: Traditional Bull's trench brick kiln with 7.5m tall conical brick chimney, stepped corbel crown rim, arched draft flue intake portal, and drying hacks of green clay and red Lahori bricks.
    4. `SM_Prop_Clandestine_Safehouse_Crate_Cache`: Underground resistance supply cache with 3 stenciled teak shipping crates, printing ink canisters, vintage roadster bicycle frame, and draped weathered burlap tarpaulin.
  - Ingested into `/Game/Environment/Mohalla/Meshes/` with `CTF_USE_COMPLEX_AS_SIMPLE` collision.
  - Placed 4 structures into Zone F Western Outskirts of `L_Validation_Gym.umap` via `assemble_task9_outskirts_and_canal.py`.
  - Synthesized and ingested authentic 16-bit 44.1kHz audio: `SFX_Canal_Water_Flow_Gentle.uasset` and `SFX_Persian_Wheel_Rahat_Creak.uasset`.

---

### Task 9.5: The Veil of Memory — Archival Censor Window & Protagonist Architecture [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE**
- **Implemented Components:**
  - **Archival Censor Window & Cinematic Vignette (Policy-Compliant AAA Storytelling):**
    - Implemented `DrawCensorWindowVeilOfMemory(Kabir, DeltaTime)` in `ARevolutionHUD` (`RevolutionHUD.h/.cpp`).
    - Concentric frosted Gaussian vignette borders fading screen edges into deep sepia/charcoal tones.
    - Imperial Press Censorship Header Stamp: `[MILITARY PRESS REGULATION — DEFENSE OF INDIA ACT 1919]`.
    - Poignant Memorial Contemplation Card: Reflecting on the unbroken silence of Jallianwala Bagh without any graphic violence, allowing the player's imagination to honor the gravity of the event.
    - Interactive prompt: `[E] Contemplate Courtyard Remnants • Preserve The Unwritten Dispatch`.
  - **Remembrance Audio Soundscapes:**
    - `SFX_Flute_Bansuri_Sorrow.wav`: Haunting wooden bamboo flute melody in Raag Bhairavi (the raga of quiet grief, remembrance, and dawn).
    - `SFX_Wind_Hollow_Courtyard.wav`: Somber Punjabi evening wind echoing through empty brick archways.
    - Ingested into `/Game/Audio/SFX/` and played dynamically upon entering the memorial zone.
  - **4 Memorial Environmental 3D Storytelling Assets:**
    - Modeled in Blender 5.2 LTS and dual-exported to `Art/Exports/`, `Art/PROJECT/`, and `C:/Users/npal7/PROJECT/PROJECT/`:
      1. `SM_Memorial_Historic_Well_Brick`: Hexagonal Lahori brick well with timber pulley gallows, wrought-iron axle, and stone coping.
      2. `SM_Prop_Overturned_Brass_Lota`: Traditional Punjabi hammered brass water urn lying on its side with water reflection.
      3. `SM_Prop_Abandoned_Paper_Kite`: Diamond saffron bamboo-and-paper patang kite caught high on the brick enclosure wall.
      4. `SM_Prop_Wooden_Takhti_Slate`: Traditional student wooden writing slate with carved handle, chalk inscription, and brass inkpot.
    - Ingested with `CTF_USE_COMPLEX_AS_SIMPLE` collision and assembled into Zone D Memorial Courtyard of `L_Validation_Gym.umap` via `assemble_veil_of_memory_scene.py`.
    - Total Level Actors expanded to **192**.
  - **Protagonist Character (Kabir) Redesign:**
    - Built comprehensive 12-year-old character generation script `Scripts/build_kabir_complete_hero.py` in Blender 5.2 LTS.
    - Continuous anatomical head loop cage with sculpted facial features: nose bridge, nostrils, eyelids, juvenile lips (cupid's bow upper lip, full lower lip), rounded chin, natural ears.
    - Saffron patka (turban) headdress with wrapped crown, topknot *juda* bun, and flowing nape ties.
    - Khadi kurta with Nehru collar, 3 carved wooden buttons, side slits (*chaks*), cotton pajama pants, leather juttis, and leather courier satchel with brass buckle.
    - Rigged with full humanoid armature hierarchy parented with deformation modifiers.
    - Exported rigged FBX and rendered studio presentations (`Kabir_Protagonist_AAA_Portrait.png`, `Kabir_Protagonist_AAA_Hero.png`, `Kabir_Protagonist_AAA_Profile.png`) to `Art/PROJECT/` and `C:/Users/npal7/PROJECT/PROJECT/`.
  - **Automated Verification:**
    - `Scripts/verify_act1_questline.py` passed with **100% SUCCESS** across **192 actors, 7 NPCs, 60 landmarks, and all 23 narrative stages**.

---

---

### Task 10: Layer 4 — Railway Junction & Colonial Civil Lines [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE**
- **Implemented Components:**
  - **4 Monumental Colonial Railway 3D Assets:** Modeled in Blender 5.2 LTS and dual-exported to `Art/Exports/`, `Art/PROJECT/`, and `C:/Users/npal7/PROJECT/PROJECT/`:
    1. `SM_Railway_Brick_Overpass_Arch`: Monumental 8.0m span British colonial arch overpass with corbel courses and heavy stone coping.
    2. `SM_Railway_Tracks_Ballast_Bed_4m`: Indian 5ft 6in broad-gauge steel dual rails, creosote-treated timber sleepers, and angled stone ballast bedding.
    3. `SM_Colonial_Railway_Signal_Gantry`: 6.5m lattice structural iron semaphore signal tower with maintenance ladder, railed platform, and red/white semaphore arm.
    4. `SM_Civil_Lines_Club_Perimeter_Railing`: Segregated perimeter security palisade with spearhead finials, horizontal rails, and brick end pilasters.
  - **Level Assembly:** Placed across the northern boundary of `L_Validation_Gym.umap` at $(900, 3900, 0)$ through $(1100, 4200, 0)$ via `assemble_task10_railway_and_civil_lines.py`. Total level actors expanded to **199**.
  - **Atmospheric Audio:** Synthesized and ingested `SFX_Steam_Locomotive_Idling.uasset` and `SFX_Railway_Signal_Bell.uasset`.
  - **C++ Narrative Progression:** Extended `ECourierMissionStage` across 27 distinct story stages from Act I through Act V finale (`Stage_ActV_ReachRailwayCutting`, `Stage_ActV_ClimbSignalGantry`, `Stage_ActV_CrossCivilLinesPalisade`, `Stage_Completed`).

---

### Task 11: AAA Benchmark Mechanics Synthesis (Assassin's Creed, A Plague Tale, Dishonored) [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE**
- **Synthesized Proven Gameplay Mechanisms:**
  1. **Dynamic High Mantling & Parkour Traversal (Assassin's Creed / Uncharted):**
     - Low Vault (50cm – 125cm): Smooth horizontal clearing of low parapets, carts, and sandbag pickets.
     - High Mantle (125cm – 215cm): Athletic two-handed ledge pull-up onto haveli walls, brick compound perimeters, railway embankments, and aqueduct catwalks with S-curve cubic root interpolation (`bIsMantling`).
  2. **Social Stealth & Civilian Crowd Blending (Assassin's Creed / Hitman):**
     - When walking calmly within 3.2m of mohalla citizens or bazaar shopkeepers, Kabir enters `bIsCrowdBlended` mode.
     - Curfew patrol watchmen and British constables suffer an **80% reduction in detection rate** (`StanceMultiplier *= 0.20f`).
     - Real-time HUD badge displays `[ BLENDED WITH CIVILIANS — LOW PROFILE ]`.
  3. **Predictive Pebble Aim Trajectory & Acoustic Distraction (A Plague Tale: Innocence / The Last of Us):**
     - Holding Right Mouse Button (`RMB`) projects a real-time parabolic ballistic arc on screen with gravity compensation ($g = -1127\text{ cm/s}^2$).
     - Renders luminous amber trajectory arc nodes and an impact target reticle highlighting the exact point of surface strike.
     - Displays `[ DISTRACTION IMPACT — 8.5m AUDIBLE ]` beacon to pinpoint diversion zones and lure curfew sentries away from critical gates.
  4. **Automated Verification:**
     - Headless automated regression suite `Scripts/verify_act1_questline.py` passed with **100% SUCCESS** across 199 level actors, 7 narrative NPCs, 64 landmarks, and all 27 story stages.

---

### Task 12: Layer 5 Historical Dynamic Atmosphere & Extended AAA Stealth Synthesis [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE**
- **5-Phase Historical Dynamic Atmosphere System:**
  - Expanded `ARevolutionAtmosphereController` to continuously drive 5 chronological atmospheric lighting & weather phases matching the narrative acts:
    1. **Morning Dawn (Act I):** 3200K warm sunrise, pitch -15°, yaw 75°, intensity 14.0, soft golden mist ($0.012\text{ density}$), morning temple bell chimes.
    2. **Baisakhi Festival Midday (Act II):** 5200K high spring sun, pitch -62°, yaw 165°, intensity 28.0, crisp visibility in bustling chowks ($0.004\text{ density}$).
    3. **Curfew Martial Law Night (Act III):** 8500K sharp moonlight, pitch -68°, yaw 40°, intensity 2.2, dense smog ($0.040\text{ density}$), British curfew whistle echoes.
    4. **Canal Distributary Night (Act IV):** 6500K river moonlight, pitch -48°, yaw 25°, intensity 3.2, heavy ground fog rolling off water canals ($0.058\text{ density}$).
    5. **Golden Sunrise Finale (Act V):** 2850K golden dawn triumph break, pitch -6.5°, yaw 85°, intensity 22.0, radiant morning haze ($0.018\text{ density}$).
  - Seamless interpolation across Sun/Moon rotation, intensity, temperature, SkyLight color, and Exponential Height Fog inscattering.
  - Spawned persistent `AtmosphereController_Historical` actor into `L_Validation_Gym.umap`, expanding total level actors to **200**.
- **Synthesized AAA Benchmark Stealth Mechanisms:**
  1. **Corner Peeking & Lean Mechanic (Dishonored / The Last of Us):**
     - Leaning left (`Q`) and right (`E`) dynamically offsets camera boom by $\pm 48\text{ cm}$ laterally and tilts roll by $\pm 5^\circ$.
     - When leaning around haveli wall corners, Kabir exposes only a subtle silhouette, reducing enemy visual detection rate to **0.35x**.
     - Real-time HUD badge displays `[ CORNER PEEK: LEAN LEFT / RIGHT ]`.
  2. **Environmental Shadow Concealment Rating (Thief / Splinter Cell / Dishonored):**
     - Calculates Kabir's dynamic luminance exposure in real time against nearby sentry lanterns and deep haveli shade.
     - Curfew sentry detection speed is dampened by up to **75%** when Kabir is cloaked in deep shadow (`ShadowDampening = 1.0f - 0.75f * ConcealmentScore`).
     - Real-time HUD badge displays `[ CONCEALMENT: %d%% — DEEP SHADOW / PARTIAL SHADE / EXPOSED ]`.
  3. **Keen Senses / Basant Intuition (Assassin's Creed Eagle Vision / Hitman Instinct):**
     - Toggled with `V` key (`ToggleKeenSenses()`).
     - Projects world-space tactical awareness beacons on screen:
       - Curfew Sentries & Constables (Crimson diamond beacons with distance meters).
       - Civilians & Allies (Warm amber social stealth markers).
       - Resistance Caches, Stashes & Water Pumps (Luminous golden icons).
- **Protagonist Hero Mesh PBR Materials:**
  - Assigned authentic historical materials across all 10 material slots of `/Game/Characters/Kabir_AAA/SK_Kabir_Protagonist_AAA`: skin, wooden buttons, eyes, dark hair, khadi kurta, cotton pajama, saffron patka, aged leather satchel, and brass buckle.
- **Automated Master Regression:**
  - `Scripts/verify_act1_questline.py` passed with **100% SUCCESS (Exit Code 0)** across **200 level actors, 7 narrative NPCs, 64 historic landmarks, and 27 story milestones**.

---

### Task 13: Layer 4 & 5 Climax — The Locomotive Depot & Colonial Civil Lines Cantonment [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE**
- **Implemented Components:**
  - **4 Monumental 3D Environment & Traversal Assets:** Modeled in Blender 5.2 LTS and dual-exported to `Art/Exports/`, `Art/PROJECT/`, and `C:/Users/npal7/PROJECT/PROJECT/`:
    1. `SM_Locomotive_Engine_PunjabMail` (334 KB): Authentic British 4-6-0 broad-gauge steam locomotive with cylindrical boiler, brass bands, smokebox, driver's cab, coupling rods, and 6ft driving wheels.
    2. `SM_Civil_Lines_Clubhouse_Bungalow` (150 KB): Classical colonial administrative bungalow with raised stone plinth, 6 Tuscan veranda columns, sash windows, and hipped zinc roof.
    3. `SM_Cantonment_Guardhouse_Picket` (111 KB): Whitewashed brick sentry post with rifle embrasures, curved sandbag revetment, and 6.2m flagpole.
    4. `SM_Prop_Cantonment_Archive_Cabinet` (109 KB): Teak filing cabinet with wire mesh doors, curfew dispatches, and brass handles.
  - **Atmospheric & Narrative Foley Audio:** Synthesized 16-bit 44.1kHz audio and ingested into `/Game/Audio/SFX/`:
    - `SFX_Telegraph_Chirp_Ticker.uasset`: High-frequency rhythmic brass telegraph sounder decoding imperial telegrams.
    - `SFX_Locomotive_Steam_Hiss.uasset`: High-pressure steam boiler relief valve hissing across the railway cutting.
  - **Level Assembly (`assemble_task13_cantonment.py`):**
    - Placed all 4 monumental structures beyond the railway palisade in `L_Validation_Gym.umap`:
      - `Locomotive_Engine_PunjabMail_Depot` on the broad-gauge tracks at $(1000, 3900, 30)$.
      - `Cantonment_Guardhouse_Picket_NorthGate` guarding the Civil Lines gateway at $(650, 4220, 0)$.
      - `Civil_Lines_Clubhouse_Bungalow_HQ` at $(900, 4800, 0)$ as the Act V climax headquarters.
      - `Prop_Cantonment_Archive_Cabinet_Veranda` on the clubhouse veranda at $(820, 4520, 60)$.
    - Saved level package, expanding total level actors to **204**.
  - **Automated Regression Verification Suite:**
    - Updated `Scripts/verify_act1_questline.py` to assert the 4 new Cantonment landmarks.
    - Executed in-engine with **100% SUCCESS (0 errors)** across **204 actors, 7 narrative NPCs, 68 landmarks, and 27 story milestones**.

---

### Task 14: Act V Climax — Locomotive Steam Distraction & Clandestine Dispatch Infiltration [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE**
- **Implemented Components:**
  - **Dedicated C++ Class `ALocomotiveSteamValveActor`:**
    - Interactive high-pressure relief valve mounted on `SM_Locomotive_Engine_PunjabMail` at $(1000, 3880, 90)$.
    - Releases high-pressure steam hiss (`SFX_Locomotive_Steam_Hiss`), cloaking Kabir with steam obscurity (`bIsSteamObscured`) for 14.0 seconds.
    - Emits a 28-meter acoustic distraction wave calling nearby sentries to investigate (`InvestigateSoundLocation`).
    - Placed persistently into `L_Validation_Gym.umap` via `assemble_task14_steam_valve.py`, expanding total level actors to **205**.
  - **AAA Benchmark Steam Obscurity Stealth Synthesis (*Hitman* / *Batman: Arkham*):**
    - Extended `ARevolutionCharacter` with `bIsSteamObscured`, `SteamObscurityRemainingTime`, and `TriggerSteamObscurity(Duration)`.
    - Integrated line-of-sight obstruction in `ACurfewPatrolAI::CanSeePlayer`: when Kabir is steam-obscured, sentry visual detection is completely broken (`return false`).
    - Extended `ARevolutionHUD` with a luminous cyan steam status badge: `[ STEAM CLOAK ACTIVE (%.1fs) — SENTRY LINE-OF-SIGHT BLOCKED ]`.
  - **Cantonment Gate Sentinel & Veranda Archive Infiltration:**
    - Spawning `Cantonment_Sentry_Picket` (`ACurfewPatrolAI`) at $(650, 4220, 10)$ with 3 waypoints guarding the Civil Lines gateway.
    - Interactive dispatch trigger on `SM_Prop_Cantonment_Archive_Cabinet` at $(820, 4520, 75)$ playing `SFX_Telegraph_Chirp_Ticker.uasset`.
    - Triggers the 2850K `GoldenSunrise` finale in `ARevolutionAtmosphereController`, completing the full 5-act narrative arc.
  - **Automated Master Regression:**
    - `Scripts/verify_act1_questline.py` passed with **100% SUCCESS (0 errors)** across **205 level actors, 7 narrative NPCs, 69 historic landmarks, and 27 story milestones**.

---

### Task 15: Master Play-In-Editor (PIE) Validation, Packaging & Release Readiness [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE**
- **Implemented Components:**
  - **Full End-to-End Story Walkthrough Simulation (`Scripts/verify_pie_master_walkthrough.py`):**
    - Headless PIE simulation executing across all 205 actors in `/Game/Maps/L_Validation_Gym`.
    - Validates Kabir's core locomotion, crouch postures, corner peeking/dynamic lean, Keen Senses / Basant Intuition, pebble aiming distraction, tailor's chalk marking, and locomotive steam cloak.
    - Automated sequential verification through all **27 story milestones** (Act I through Act V finale) and 5 dynamic atmosphere transitions (MorningDawn -> BaisakhiMidday -> CurfewNight -> CanalNight -> GoldenSunrise).
    - Executed with **100% SUCCESS (0 errors)**.
  - **NVIDIA GeForce GTX 1650 Hardware Performance & Frame Budget Audit (`Scripts/profile_gtx1650_performance.py`):**
    - Certified Software Lumen (`r.Lumen.HardwareRayTracing=0`), TSR 75% screen percentage (`r.ScreenPercentage=75`), 1800MB texture streaming pool, 512MB Nanite pool, and 32-frame VSM page age.
    - Total estimated peak VRAM allocation modeled at **3412.0 MB** within the 3500 MB budget (88 MB safety headroom).
    - Total bottleneck frame time modeled at **21.40 ms (~46.7 FPS)**, comfortably beating the $\le 33.33\text{ ms}$ (30 FPS) target.
    - Documented in [`Documentation/GTX1650_PERFORMANCE_AUDIT.md`](file:///C:/Users/npal7/PROJECT/REVOLUTION/Documentation/GTX1650_PERFORMANCE_AUDIT.md).
  - **Automated Standalone Win64 Release Packaging (`Scripts/package_windows_release.ps1`):**
    - Automated `RunUAT.bat BuildCookRun` pipeline compiling `REVOLUTION.exe`, cooking 638 packages with Zen/IoStore compression, staging, and archiving.
    - Output archived cleanly to [`Build/Development/Windows/`](file:///C:/Users/npal7/PROJECT/REVOLUTION/Build/Development/Windows/REVOLUTION.exe) (`REVOLUTION.exe`, `REVOLUTION-Windows.ucas`, `REVOLUTION-Windows.utoc`, `REVOLUTION-Windows.pak`).
    - Build and cooking succeeded in **18.2 minutes** with `ExitCode=0 (Success)`.

---

## 3. Phase 6 Roadmap: Polish, Audio Mastering & Cinematic Refinement

```mermaid
flowchart LR
    Task16["Task 16: Cinematic Camera Sequences\n• Level Sequence Cutscenes for Munadi & Golden Sunrise\n• Smooth letterbox cinematic transitions"]
    
    Task17["Task 17: Audio Mix & Sound Class Routing\n• Ambient Punjabi Foley & Soundscape Bus\n• Dynamic Low-Pass Curfew Filter\n• Voice Bark Spatialization"]
    
    Task18["Task 18: Quality-of-Life & Visual Polish\n• Extended Keybinding Remapping Menu\n• Historical Glossary Codex UI\n• Accessibility Subtitle Controls"]

    Task16 --> Task17
    Task17 --> Task18
```

### Task 16: Cinematic Camera Sequences & Dynamic Transitions [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE**
- **Implemented Components:**
  - **Level Sequence Cutscenes (`/Game/Cinematics/`):**
    - `LS_Munadi_Proclamation`: 150 frames (5.0s @ 30 FPS) establishing General Dyer's curfew proclamation across the historic Faseel archway.
    - `LS_Golden_Sunrise_Finale`: 180 frames (6.0s @ 30 FPS) framing the dawn resolution over the Punjab Mail locomotive depot and Civil Lines bungalow.
  - **C++ Cinematic Director Actor (`ARevolutionCinematicDirectorActor`):**
    - `PlayCinematicCutscene(Sequence, ChapterTitle, Subtitle, BlendInTime)`: seamlessly triggers sequence playback with `SetViewTargetWithBlend()`, eases into cinematic camera framing, disables player control inputs, and broadcasts `OnCinematicCompleted`.
    - `StopCinematicCutscene(BlendOutTime)`: returns view target smoothly back to player pawn and restores gameplay controls.
    - `UpdateSubtitle(Subtitle)`: dynamically updates lower-third ivory captions mid-cutscene.
    - Integrated persistently as `CinematicDirector_Master` in `/Game/Maps/L_Validation_Gym` (expanding total level actors to **206**).
  - **ARevolutionHUD Cinematic Mode:**
    - `bCinematicSequenceActive`: triggers widescreen anamorphic 2.39:1 letterbox matte.
    - Upper-third antique brass chapter title cards with gold filigree divider rules (`CinematicChapterTitle`).
    - Lower-third ivory period subtitles with dark drop shadows (`CinematicSubtitleText`).
  - **Automated Verification:**
    - `Scripts/verify_cinematic_sequences.py`: 100% PASS (0 errors).
    - `Scripts/verify_act1_questline.py`: 100% PASS (0 errors across 206 actors).
    - `Scripts/verify_pie_master_walkthrough.py`: 100% PASS (0 errors across 206 actors, 27 milestones).

---

### Task 17: Audio Mix & Sound Class Routing [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE**
- **Implemented Components:**
  - **Sound Class Hierarchy (`/Game/Audio/SoundClasses/`):**
    - `SC_Master`: Root Master Bus (Volume: 1.0, LPF: 20000 Hz).
    - `SC_SFX`: Mechanical sounds, weapons, alarms, telegraph (Parent: `SC_Master`, Volume: 1.0).
    - `SC_Foley`: Tactile movement, footsteps, cloth rustle, pebble throw (Parent: `SC_SFX`, Volume: 1.0).
    - `SC_Voice_Punjabi`: Punjabi civilian dialogues, crowd murmurs, watchman shouts (Parent: `SC_Master`, Volume: 1.0).
    - `SC_Ambience_Mohalla`: Environmental soundscapes, wind, crickets, canal water (Parent: `SC_Master`, Volume: 0.85).
  - **3D Spatialized Sound Attenuations (`/Game/Audio/Attenuation/`):**
    - `ATT_Voice_Proximity`: Natural human voice falloff (18.0m radius, 4.0m inner sphere).
    - `ATT_Foley_Localized`: Intimate footstep and interaction falloff (12.0m radius, 2.0m inner sphere).
    - `ATT_Monumental_Mechanical`: Heavy locomotive and industrial kiln falloff (45.0m radius, 8.0m inner sphere).
  - **Sound Mixes & Dynamic Curfew Filter (`/Game/Audio/SoundMixes/`):**
    - `SMix_Default`: Baseline audio balance.
    - `SMix_Curfew_Night`: Dynamic Low-Pass Curfew Filter:
      - `SC_Ambience_Mohalla`: LPF at 800 Hz, volume dampened to 0.45 (muffling distant town life under martial law).
      - `SC_Voice_Punjabi`: LPF at 1200 Hz, volume dampened to 0.35 (enforced street curfew stillness).
      - `SC_Foley`: Volume boosted to 1.30 (heightened sensory stealth perception for Kabir).
      - `SC_SFX`: Volume boosted to 1.15 (sentry whistles, searchlight hum, boiler release).
    - `SMix_Cinematic`: Cutscene dialogue ducking:
      - `SC_Voice_Punjabi`: Volume boosted to 1.35.
      - `SC_Ambience_Mohalla`: Volume dampened to 0.30.
      - `SC_SFX`: Volume dampened to 0.55.
      - `SC_Foley`: Volume dampened to 0.60.
  - **100% SoundWave Asset Coverage:**
    - Routed all 42 individual sound waves in `/Game/Audio/SFX/` to designated SoundClasses:
      - `SC_Voice_Punjabi`: 4 assets
      - `SC_Ambience_Mohalla`: 7 assets
      - `SC_Foley`: 13 assets
      - `SC_SFX`: 18 assets
  - **C++ Dynamic SoundMix Integration:**
    - `ARevolutionAtmosphereController`: Automatically pushes `SMix_Curfew_Night` when transitioning to `CurfewNight` and restores `SMix_Default` for daytime/sunrise phases.
    - `ARevolutionCinematicDirectorActor`: Pushes `SMix_Cinematic` during cutscenes and restores gameplay mix upon completion.
  - **Automated Verification:**
    - `Scripts/verify_audio_mix.py`: 100% PASS (0 errors).
    - `Scripts/verify_cinematic_sequences.py`: 100% PASS (0 errors).
    - `Scripts/verify_act1_questline.py`: 100% PASS (0 errors across 206 actors).
    - `Scripts/verify_pie_master_walkthrough.py`: 100% PASS (0 errors across 206 actors, 27 milestones).

---

### Task 18: Quality-of-Life, Historical Glossary Codex UI & Keybinding Remap [NEXT]
- **Target Objectives:**
  1. Author In-Game Historical Glossary Codex UI accessible via Satchel Journal tab (detailed archival background on Rowlatt Act, Khadi movement, Baisakhi festival, Jallianwala Bagh, and Section 144 martial law).
  2. Implement Enhanced Input runtime keybinding remapping and accessibility subtitle configuration.
  3. Validate through automated test suite `Scripts/verify_qol_and_codex.py`.



