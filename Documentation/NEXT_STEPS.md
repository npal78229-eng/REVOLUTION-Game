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

### Task 18: Quality-of-Life, Historical Glossary Codex UI & Keybinding Remap [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE**
- **Implemented Components:**
  - **Tactile Satchel Journal 4-Tab Architecture (`ARevolutionHUD` & `ARevolutionCharacter`):**
    - `[ 1 ] SATCHEL EQUIPMENT`: Real-time inventory status (Tailored Khadi Coat Parcel, Tailor's Chalk Marks, Clay Pebbles, Clandestine Pamphlets).
    - `[ 2 ] MOHALLA ROUTE MAP`: Hand-drawn khadi parchment cartography of Kot Gurdarshan with real-time scout positions, dynamic chalk marks, curfew patrol route indicators, and 5 historical zones.
    - `[ 3 ] HISTORICAL CODEX`: Complete 17-entry period archival knowledge base featuring master-detail directory, archival records, primary source excerpts, and tactical gameplay applications.
    - `[ 4 ] SETTINGS & CONTROLS`: Dynamic audio volume sliders, accessibility subtitle scaling toggles, and comprehensive keyboard/mouse input schema.
  - **17-Record Archival Historical Codex Knowledge Base:**
    - *7 Core Period Historical Treatises:*
      1. `The Rowlatt Black Act (1919)` (Colonial emergency powers, indefinite detention, "Na Dalil, Na Vakil, Na Appeal").
      2. `Swadeshi & Khadi Weave` (Economic autonomy, hand-spun cotton, indigenous trade resistance).
      3. `Baisakhi Harvest Festival` (Solar new year, Khalsa Panth founding, rural pilgrim assemblies).
      4. `Jallianwala Bagh Memorial` (Solemn memory, non-violent assembly, the Veil of Remembrance).
      5. `Section 144 Martial Curfew` (8:00 PM curfew edict, searchlight sentries, unlawful assembly bans).
      6. `Clandestine Printing Press` (Subterranean lithographic stones, strike handbills, freedom of expression).
      7. `Punjabi Architectural Fabric` (Nanakshahi brick havelis, shaded kuchas, interconnected kotha rooftops).
    - *10 Discovered Material Culture Artifacts:*
      - Student Takhti & Reed Qalam, Earthen Mud Chulha Stove, Bazaar Vendor Thela Handcart, Rooftop Pigeon Loft (Kabootar-khana), Basant Fighter Kites & Manja, Anti-Rowlatt Satyagraha Handbill, Imperial Red Pillar Postbox (GR), Mandi Iron Tarazu Scale & Weights, Shisham Carved Grain Sandook, Classroom 1919 Punjab Map Easel.
    - *Interactive Navigation:* `SelectNextCodexEntry()`, `SelectPrevCodexEntry()`, bound to `[ / ]` and `UP / DOWN` arrow keys with active selection highlight.
  - **Quality-of-Life, Accessibility & Audio Configuration:**
    - Dynamic SoundClass volume sliders: `MasterVolume`, `SFXVolume`, `FoleyVolume`, `VoiceVolume`, `AmbienceVolume` adjusting audio mix dynamically in real time via `UGameplayStatics::SetSoundMixClassOverride`.
    - Accessibility Subtitle Size toggles: `SMALL (0.85x)`, `MEDIUM (1.0x)`, `LARGE (1.25x)` via `SubtitleScaleMultiplier`, scaling cinematic ivory captions dynamically.
    - Direct keybindings: `1 / 2 / 3 / 4` for instantaneous tab selection, `UP / DOWN / LEFT / RIGHT` for intuitive settings and codex browsing.
  - **Automated Verification & Master Regression:**
    - `Scripts/verify_qol_and_codex.py`: 100% PASS (0 errors, 0 warnings).
    - `Scripts/verify_audio_mix.py`: 100% PASS (0 errors across 5 SoundClasses, 3 Mixes, 42 SoundWaves).
    - `Scripts/verify_cinematic_sequences.py`: 100% PASS (0 errors across Level Sequences and Director Actor).
    - `Scripts/verify_act1_questline.py`: 100% PASS (0 errors across 206 actors, 7 NPCs, 69 landmarks).
    - `Scripts/verify_pie_master_walkthrough.py`: 100% PASS (0 errors across 206 actors, 27 milestones).

---

### Task 19: Standalone Build Cook & Distribution Package Validation [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE**
- **Implemented Components:**
  - **Full Asset Cooking & IoStore Packaging Pipeline (`RunUAT.bat BuildCookRun`):**
    - Executed clean BuildCookRun process for Windows 64-bit (`Development` client configuration).
    - Cooked and indexed **648 project packages**, serialized into Zen/IoStore container archives (`global.ucas`, `global.utoc`, `REVOLUTION-Windows.pak`, `REVOLUTION-Windows.ucas`, `REVOLUTION-Windows.utoc`).
    - Staged and archived standalone distribution to `Build/Development/Windows/` in **3.19 minutes** with `ExitCode=0 (Success)`.
  - **Standalone Package Architecture:**
    - Root Launcher Executable: `Build/Development/Windows/REVOLUTION.exe` (168,448 bytes).
    - Win64 Target Executable: `Build/Development/Windows/REVOLUTION/Binaries/Win64/REVOLUTION.exe` (283.1 MB).
    - Total Packaged Distribution Size: **885.5 MB** ($\ll 20\text{ GB}$ distribution ceiling).
    - Total Container Archives: **171.1 MB** with Oodle compression (36.51% ratio).
  - **GTX 1650 Hardware Budget Compliance:**
    - Modeled Peak VRAM Allocation: **3412.0 MB / 3500.0 MB** (88.0 MB safety headroom).
    - Modeled Frametime: **21.40 ms (~46.7 FPS)**, exceeding the $\le 33.33\text{ ms}$ ($\ge 30\text{ FPS}$) target bar.
  - **Automated Verification:**
    - `Scripts/verify_standalone_package.py`: 100% PASS (0 errors, 0 warnings).

---

### Task 20: Master Continuous Integration (CI) Test Harness & Gold Master Readiness [COMPLETED]
- **Status:** **100% COMPLETE & CERTIFIED GOLD MASTER READY**
- **Implemented Components:**
  - **Unified Master Test Harness (`Scripts/run_all_tests.ps1` / `Scripts/run_all_tests.py`):**
    - Executes all 6 QA verification suites in sequence:
      1. `TEST-01`: `verify_qol_and_codex.py` (27.38s, PASS)
      2. `TEST-02`: `verify_audio_mix.py` (24.18s, PASS)
      3. `TEST-03`: `verify_cinematic_sequences.py` (23.19s, PASS)
      4. `TEST-04`: `verify_act1_questline.py` (23.21s, PASS across 206 actors, 7 NPCs, 69 landmarks)
      5. `TEST-05`: `verify_pie_master_walkthrough.py` (23.20s, PASS across 27 story milestones, Acts I–V)
      6. `TEST-06`: `verify_standalone_package.py` (1.03s, PASS across IoStore containers & GTX 1650 budget)
    - Total execution time: **2.04 minutes** with **100% PASS (0 errors, 0 warnings)**.
  - **Comprehensive Gold Master Release Report (`Documentation/GOLD_MASTER_RELEASE_REPORT.md`):**
    - Formally documents full engine architecture, 27 narrative stages, AAA stealth mechanics, audio hierarchy, GTX 1650 hardware profiling ($\le 3500\text{ MB}$ VRAM, $46.7\text{ FPS}$), standalone IoStore packaging (885.5 MB), and full CI test harness audit tables.
  - **Synchronized Git Repository:**
    - Full version control tracking with commit history and GitHub remote synchronization on `origin/main`.

---

### Task 21: Authentic Punjabi Civilian Dialogue Localization & Ambient Proximity Voice System [COMPLETED]
- **Status:** **100% COMPLETE & CERTIFIED IN-ENGINE**
- **Implemented Components:**
  - **Procedural Acoustic Formant Synthesis (`Scripts/generate_civilian_voice_audio.py`):**
    - Synthesized 14 authentic 16-bit 44.1kHz vocal tracks across character age/archetype profiles with formant resonators (F1, F2, F3) and pitch contours:
      1. `SFX_Voice_RamLubhaya_Bark` & `SFX_Voice_RamLubhaya_Dialogue` (Father Ram Lubhaya, ~114 Hz)
      2. `SFX_Voice_Ghasita_Bark` & `SFX_Voice_Ghasita_Dialogue` (Bhishti Ghasita, ~132 Hz with vocal vibrato)
      3. `SFX_Voice_HiraHalwai_Bark` & `SFX_Voice_HiraHalwai_Dialogue` (Hira Halwai, ~152 Hz bazaar vendor call)
      4. `SFX_Voice_LalaKaramChand_Bark` & `SFX_Voice_LalaKaramChand_Dialogue` (Lala Karam Chand, ~122 Hz merchant tone)
      5. `SFX_Voice_PanditKashiRam_Bark` & `SFX_Voice_PanditKashiRam_Dialogue` (Headmaster Pandit Kashi Ram, ~138 Hz)
      6. `SFX_Voice_KartarSingh_Bark` & `SFX_Voice_KartarSingh_Dialogue` (Kartar Singh, ~228 Hz 12-year-old friend)
      7. `SFX_Voice_ConstableGurdial_Curfew` & `SFX_Voice_ConstableGurdial_Suspicion` (Constable Gurdial Singh, ~102 Hz)
  - **Unreal Audio Routing (`Scripts/import_civilian_voice_audio.py`):**
    - Ingested all 14 voice assets into `/Game/Audio/Voice/` and `/Game/Audio/SFX/` as `SoundWave` assets.
    - 100% routed to `SC_Voice_Punjabi` SoundClass and `ATT_Voice_Proximity` 3D spatialized attenuation.
  - **C++ Gameplay Audio Integration:**
    - `ACivilianNPCActor`: Added `InteractionVoiceSound`, `AmbientBarkVoiceSound`, and `VoiceAttenuation`. Automatically loads archetype voice assets in `ConfigureOccupation()`, plays localized dialogue on `OnInteract_Implementation()`, and plays ambient barks on `OnProximityBeginOverlap()`.
    - `ACurfewPatrolAI`: Added `CurfewVoiceProclamationSound`, `SuspiciousVoiceSound`, and `VoiceAttenuation`. Plays stern suspicion query on investigating state and curfew command on alert state.
  - **Level Map Scene Assembly (`Scripts/assemble_civilian_voice_actors.py`):**
    - Bound all 6 civilian NPCs and curfew patrol constable in `/Game/Maps/L_Validation_Gym` with localized voice assets.
  - **Automated QA Verification Suite (`Scripts/verify_civilian_voice_localization.py`):**
    - Executed with **100% PASS (0 errors)** across all 14 voice sound waves, 6 civilian NPCs, and patrol sentries.

---

### Task 22: Dynamic Non-Lethal Pedestrian Reaction & Crowd Stumble System [COMPLETED]
- **Status:** **100% COMPLETE & CERTIFIED IN-ENGINE**
- **Implemented Components:**
  - **Dynamic C++ Reaction State Machine (`ECivilianReactionState`):**
    - `Idle`: Default resting or artisan work posture.
    - `FacingPlayer`: Natural proximity orientation when Kabir approaches gently.
    - `Stumbling`: Procedural spring-damped balance loss and recovery when bumped into by sprinting player.
    - `CuriousInvestigating`: Gaze orientation toward distraction impacts (pebble clatters) without raising alarm.
  - **Procedural Spring-Damped Balance Recovery Physics:**
    - Procedural pitch/roll mesh lean and translation offset away from impact direction.
    - Non-violent collision sweep pushback preserving historical dignity and zero health damage.
    - Momentum damping: `ARevolutionCharacter::HandleCivilianCollision` naturally absorbs Kabir's high-speed sprint momentum upon colliding with adult pedestrians.
  - **Contextual Vocal Reactions & Synthesis:**
    - Synthesized 5 authentic Punjabi pedestrian reaction SoundWaves:
      1. `SFX_Voice_Civilian_Stumble_01` (Adult male exclamation "Ohe! Sambhal ke!")
      2. `SFX_Voice_Civilian_Stumble_02` (Bazaar vendor sharp reaction "Arrey dhyan naal!")
      3. `SFX_Voice_Civilian_Stumble_03` (Youth friend startled reaction "Oye Kabir!")
      4. `SFX_Voice_Civilian_Curiosity_01` (Adult inquisitive murmur "Ki diggeya uthe?")
      5. `SFX_Voice_Civilian_Curiosity_02` (Vendor curious whisper "Aawaz kithon aayi?")
    - Total sound assets expanded to **61 SoundWaves** (100% routed to `SC_Voice_Punjabi`, `SC_SFX`, `SC_Foley`, `SC_Ambience_Mohalla`).
  - **Acoustic Distraction Dispatch (`PebbleProjectile.cpp`):**
    - On pebble impact, nearby `ACivilianNPCActor` instances within 750cm enter `CuriousInvestigating` state.
    - Zero curfew alarm escalation: Military constables remain unalerted, enabling authentic public stealth diversion.
  - **Master 8-Suite Continuous Integration Harness (`Scripts/run_all_tests.ps1`):**
    - Integrated `TEST-08` (`verify_pedestrian_reactions.py`) into the unified harness.
    - Executed all 8 suites in sequence in **3.33 minutes** with **100% PASS (0 errors, 0 warnings)**.

---

### Task 23: SteamOS & Handheld Proton Scalability Profile [COMPLETED]
- **Status:** **100% COMPLETE & CERTIFIED IN-ENGINE**
- **Implemented Components:**
  - **Steam Deck & Linux Device Profiles (`Project/Config/DefaultDeviceProfiles.ini`):**
    - Authoring `[SteamDeck DeviceProfile]` and `[SteamDeckLinux DeviceProfile]` targeting native 800p (1280x800, 16:10).
    - Dynamic resolution scaling (TSR 66%–85% target window: 844x528 internal to 1088x680 internal upscaled).
    - 40 FPS / 25.0ms sweet spot frametime budget (`t.MaxFPS=40`, `r.DynamicRes.FrameTimeBudget=25.0`).
    - Handheld unified LPDDR5 memory budget (`r.Nanite.Streaming.PoolSize=256`, `r.Streaming.PoolSize=1024`).
    - Low-overhead Lumen Software Ray Tracing settings (`DownsampleFactor=16`, `VirtualShadowMaps LODBias=1.0`).
  - **Tiered Handheld Scalability Settings (`Project/Config/DefaultScalability.ini`):**
    - Authoring ECVF-compliant scalability tiers across Anti-Aliasing (TSR Quality), Shadows (Virtual Shadow Maps physical pages), Global Illumination (Lumen Diffuse Indirect), Reflections, and Foliage density.
  - **Complete Gamepad & Controller Mapping Architecture (`Project/Config/DefaultInput.ini`):**
    - Full Gamepad Axis Mappings: `MoveForward` (Gamepad_LeftY), `MoveRight` (Gamepad_LeftX), `Turn` (Gamepad_RightX), `LookUp` (Gamepad_RightY).
    - Full Gamepad Action Mappings:
      - `Jump`: `Gamepad_FaceButton_Bottom` (A / Cross)
      - `Sprint`: `Gamepad_LeftShoulder` (LB / L1)
      - `Crouch`: `Gamepad_FaceButton_Right` (B / Circle)
      - `Interact`: `Gamepad_FaceButton_Left` (X / Square)
      - `AimPebble`: `Gamepad_LeftTrigger` (LT / L2)
      - `ThrowPebble`: `Gamepad_RightTrigger` (RT / R2)
      - `ToggleJournal`: `Gamepad_RightShoulder` (RB / R1)
      - `KeenSenses`: `Gamepad_FaceButton_Top` (Y / Triangle)
      - `DrawChalk`: `Gamepad_RightThumbstick` (R3)
      - `Menu Navigation`: `Gamepad_DPad_Up / Down / Left / Right`
      - `Codex Direct`: `Gamepad_Special_Left` (Back / View)
      - `Settings Direct`: `Gamepad_Special_Right` (Start / Menu)
  - **C++ Engine Architecture (`ARevolutionCharacter` & `ARevolutionHUD`):**
    - Direct Gamepad key and axis bindings in `ARevolutionCharacter::SetupPlayerInputComponent`.
    - Active input tracking: `bIsUsingGamepad` dynamically detects controller vs keyboard/mouse usage.
    - Handheld Mode Setting: Added Setting 6 to Satchel Tab 4 (`bHandheldSteamOSMode`, `ToggleHandheldMode`, `ApplyHandheldScalability`).
    - Dual HUD Prompts & Glyphs: Contextual interact prompt shows `[E / (X)]`, inspection modal shows `[ (B) ] / [ (A) ]`, Satchel Journal footer shows D-pad / LB-RB hints, and Tab 4 renders full dual Keyboard/Gamepad schema badges.
  - **Dedicated QA Test Suite (`Scripts/verify_steamos_handheld_profile.py`):**
    - Automated suite verifying device profiles, scalability settings, input mappings, C++ class reflection, and handheld hardware envelope simulation (1280x800 native, TSR 66%–85%, $\le 2800\text{ MB}$ unified VRAM allocation, 3.51 hours battery life on 40Wh battery at 11.4W total system draw).
  - **Master 9-Suite Continuous Integration Harness (`Scripts/run_all_tests.ps1` & `Scripts/run_all_tests.py`):**
    - Integrated `TEST-09` into the unified CI harness.

---

### Task 24: Advanced Photogrammetry Texturing & Heritage Material Architecture [COMPLETED]
- **Status:** **100% COMPLETE & CERTIFIED IN-ENGINE**
- **Implemented Components:**
  - **Procedural PBR Photogrammetry Texture Generation (`Scripts/generate_photogrammetry_textures.py`):**
    - Built a high-performance, zero-dependency pure Python PNG generator (`struct` + `zlib`) generating 12 1024x1024 32-bit RGBA PBR texture maps dual-exported to `Art/Textures/` and `Art/PROJECT/Textures/`:
      1. *Nanakshahi Brickwork (`T_NanakshahiBrick_BC`, `_N`, `_ORM`):* Traditional slim Punjabi kiln-fired terracotta brick masonry with coarse lime-surkhi mortar pointing, historical micro-pitting, and authentic surface roughness.
      2. *Carved Shisham Timber (`T_CarvedShisham_BC`, `_N`, `_ORM`):* Dense North Indian rosewood (*Dalbergia sissoo*) featuring authentic 8-petal acanthus floral reliefs, chisel tool marks, natural grain striations, and hand-rubbed mustard oil sheen.
      3. *Hammered Brass Metalwork (`T_HammeredBrass_BC`, `_N`, `_ORM`):* Hand-peened brass (*pittal*) with spherical ball-peen hammer dimpling, edge-wear metallic highlights, and oxidized dark patina in crevices.
      4. *Woven Jute Twine & Burlap (`T_WovenJute_BC`, `_N`, `_ORM`):* Handspun organic jute cordage in tight plain-weave burlap canvas, featuring fiber slub irregularities, tactile micro-displacement, and fibrous roughness.
  - **Automated Unreal Ingestion & Material Architecture (`Scripts/import_and_build_photogrammetry_materials.py`):**
    - Seamless headless ingestion of all 12 texture assets into `/Game/Environment/Mohalla/Textures/`.
    - Proper texture compression settings (`TC_DEFAULT` for BaseColor with `sRGB=True`; `TC_NORMALMAP` for Normal with `sRGB=False` & `TEXTUREGROUP_WORLD_NORMAL_MAP`; `TC_MASKS` for ORM with `sRGB=False`).
    - Automated construction and compilation of Master Material `M_Master_Heritage_PBR` with full parameter wiring (BaseColorMap -> Base Color, NormalMap -> Normal, ORMMap R -> Ambient Occlusion, G -> Roughness, B -> Metallic).
    - Automated creation and parameterization of 4 Material Instances (`MI_NanakshahiBrick_Photogrammetry`, `MI_CarvedShisham_Photogrammetry`, `MI_HammeredBrass_Photogrammetry`, `MI_WovenJute_Photogrammetry`).
    - Batch assignment of photogrammetry material instances across 15 landmark static mesh slots in `/Game/Environment/Mohalla/Meshes/`:
      - 7 Brick structures (`SM_Wall_Brick_4x4m_A`, `SM_Wall_Brick_Doorway_4x4m`, `SM_Wall_Brick_Window_4x4m`, `SM_Floor_Ceiling_Slab_4x4m`, `SM_Roof_Parapet_4m_A`, `SM_Memorial_Historic_Well_Brick`, `SM_Railway_Brick_Overpass_Arch`)
      - 4 Timber meshes (`SM_Door_Deorhi_Teak_01`, `SM_Prop_Haveli_Grain_Sandook`, `SM_School_Desk_Bench_Wood`, `SM_School_Blackboard_Easel`)
      - 2 Brass props (`SM_Prop_Overturned_Brass_Lota`, `SM_Prop_Bazaar_Tarazu_Scale`)
      - 2 Jute props (`SM_Prop_GrainSack_Jute_01`, `SM_Prop_Charpai_RopeBed`)
  - **Automated QA Verification Suite (`Scripts/verify_photogrammetry_materials.py` / `TEST-10`):**
    - Validates 12/12 texture assets, master material class integrity, 4/4 material instance parentage & texture parameter overrides, 15/15 mesh slot assignments, and hardware texture memory streaming budgets.
    - Verified total streaming footprint of 16.0 MB, consuming only 0.89% of the GTX 1650 pool (1800 MB) and 1.56% of the Steam Deck pool (1024 MB).
  - **Master 10-Suite Continuous Integration Harness (`Scripts/run_all_tests.ps1` & `Scripts/run_all_tests.py`):**
    - Expanded unified CI harness to 10 automated test suites, achieving 100% PASS across all 10 suites in 3.55 minutes.

---

### Task 25: Historical Narrative Epilogue — "The Baisakhi Dawn" [COMPLETED]
- **Status:** **100% COMPLETE & CERTIFIED IN-ENGINE**
- **Implemented Components:**
  - **18th Archival Historical Codex Record (`RevolutionHUD.cpp` & `RevolutionCharacter.cpp`):**
    - Authored period archival record `THE BAISAKHI DAWN & AWAKENING` in Satchel Journal Tab 3.
    - Historical treaty on Rabindranath Tagore renouncing his British Knighthood (31 May 1919) and Mahatma Gandhi launching the Non-Cooperation Movement (1920) for *Purna Swaraj*.
    - Updated navigation modulo to 18 (`Index % 18`) in `SelectNextCodexEntry()` and `SelectPrevCodexEntry()`.
  - **Cinematic Director Epilogue Method (`ARevolutionCinematicDirectorActor`):**
    - Added `PlayBaisakhiDawnEpilogue()` UFUNCTION triggering `LS_Golden_Sunrise_Finale` sequence with letterboxing and captions.
  - **Period Epilogue Soundscape:**
    - Synthesized 4.2s 16-bit 44.1kHz audio (`SFX_Epilogue_BaisakhiDawn.wav`) featuring D-tanpura drone, Raag Bhairav bansuri overtones, and brass temple bells.
    - Ingested into `/Game/Audio/SFX/SFX_Epilogue_BaisakhiDawn` routed to `SC_Ambience_Mohalla`.
  - **Master Continuous Integration (CI) Test Harness Integration:**
    - Authored `Scripts/verify_task25_epilogue.py` (`TEST-11`), passing with 0 errors across all 205 actors.
    - Integrated `TEST-11` into `Scripts/run_all_tests.py` and `Scripts/run_all_tests.ps1`.

---

---

### Task 26: Multi-Dialect Punjabi Voice Recording Expansion & Bazaar Walla System [COMPLETED]
- **Status:** **100% COMPLETE & CERTIFIED IN-ENGINE**
- **Implemented Components:**
  - **8 Multi-Dialect Punjabi Vocal Vendor & Crowd Walla Tracks:**
    - Synthesized across Majhi (Amritsar/Lahore) and Doabi (Jalandhar/Hoshiarpur) vernacular.
    - Ingested as 16-bit 44.1kHz SoundWave assets into `/Game/Audio/Voice/` and 100% routed to `SC_Voice_Punjabi` and `ATT_Voice_Proximity`.
  - **Autonomous C++ Actor `ARevolutionBazaarWallaActor`:**
    - Features organic asynchronous calling intervals (12.0s–25.0s), natural pitch randomization ($\pm 3\%$), and martial law curfew silencing (`SetCurfewSilenced`).
  - **Master Level Scene Integration (`L_Validation_Gym.umap`):**
    - Placed 4 authentic Bazaar Walla vendor actors across Grand Bazaar and Mandi, expanding total level actors to **209**.
  - **Master Continuous Integration (CI) Harness Integration:**
    - Authored `Scripts/verify_task26_multidialect_walla.py` (`TEST-12`), passing with 0 errors across all 209 actors.
    - Integrated `TEST-12` into `Scripts/run_all_tests.py` and `Scripts/run_all_tests.ps1`.

---

---

### Task 27: Dynamic Time-of-Day Weather States, Andhi Dust Storm & Volumetric Fog [COMPLETED]
- **Status:** **100% COMPLETE & CERTIFIED IN-ENGINE**
- **Implemented Components:**
  - **Dynamic Weather State Machine (`ARevolutionAtmosphereController`):**
    - `EHistoricalWeatherState` enum (`ClearSky`, `GoldenHaze`, `DustStormAndhi`, `CurfewSmog`).
    - Volumetric fog and inscattering parameter interpolation: extinction scale ($2.4\times$), scattering distribution ($0.75$), wind intensity ($0.85$), and ochre terracotta inscattering hue.
    - UFUNCTION reflection: `GetWeatherVisibilityMultiplier()` ($0.65\times$ during storms), `IsWeatherSoundMasked()`, `SetWeatherState()`, and `TriggerDustStorm(Duration)`.
  - **Sentry AI Perception Modulation (`CurfewPatrolAI.cpp`):**
    - Sentry visual perception reduced by $35\%$ during *Andhi* dust storms.
    - Acoustic masking active during storms, preventing footstep detection.
  - **Diegetic HUD Weather Advantage Banner (`RevolutionHUD.cpp`):**
    - Ochre notification banner displayed during active dust storms informing the player of sensory advantages.
  - **Period-Accurate Atmospheric Soundscape:**
    - Synthesized and ingested loopable 16-bit 44.1kHz audio assets: `SFX_Weather_DustStorm_Wind_Loop` and `SFX_Weather_GoldenHaze_Breeze` assigned to `SC_Ambience_Mohalla`.
  - **Master Continuous Integration (CI) Harness Integration:**
    - Authored `Scripts/verify_task27_weather_states.py` (`TEST-13`), passing with 0 errors.
    - Master CI test harness (`run_all_tests.py` and `run_all_tests.ps1`) expanded to 13 suites, passing 100% (13/13 suites in 3.47 minutes).

---

### Task 28: Curfew Sentry AI Collision Resolution & Patrol Path Restoration [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE (0 ERRORS)**
- **Implemented Components:**
  - **Communal Well Geometry Normalization:** Reset `Modular_Mohalla_CommunalWell` (`StaticMeshActor_49`) from `Pitch = 22.5°` tilt to `FRotator(0.0f, 0.0f, 0.0f)`, pulling the wellhead flush with the courtyard stone foundation and retracting its complex collision boundary.
  - **Sentry Spawn Orientation & Upright Restoral:** Restored `NPC_Constable_Gurdial` (`CurfewPatrolAI_0`) from inverted capsule `FRotator(90.0f, 0.0f, 180.0f)` to upright `FRotator(0.0f, 90.0f, 0.0f)` facing $+Y$ down the Grand Bazaar corridor at $(40.0, 1680.0, 88.0)$.
  - **Guaranteed Physical Clearance:** Verified $343.87\text{ cm}$ ($> 3.4\text{ meters}$) clearance between sentry capsule and communal wellhead, preventing any spawn clipping or navigation mesh obstruction.
  - **Multi-Waypoint Patrol Routine:** Configured 3 sequential patrol waypoints along the Grand Bazaar:
    - `Waypoint[0]`: $(40.0, 1680.0, 88.0)$ (Bazaar Wellhead)
    - `Waypoint[1]`: $(40.0, 1850.0, 88.0)$ (Spicemarket Stall)
    - `Waypoint[2]`: $(40.0, 2040.0, 88.0)$ (Cantonment Checkpoint Archway)
  - **C++ Defensive Runtime Guard (`CurfewPatrolAI.cpp`):** Implemented automatic upright yaw-only snapping on `BeginPlay()`, clamping any inadvertent pitch/roll angles to zero.
  - **Python Socket Configuration Hardening (`DefaultEngine.ini`):** Set `bRemoteExecution=False` under `PythonScriptPluginSettings`, eliminating multicast socket binding errors in commandlet execution.
  - **Master Continuous Integration (CI) Harness Integration:**
    - Authored `Scripts/verify_curfew_patrol.py` (`TEST-14`), passing 100% with `Success - 0 error(s)` and exit code 0.
    - Master CI test harness (`run_all_tests.py` and `run_all_tests.ps1`) expanded to 14 suites.

---

### Task 29: In-Engine Title & Main Menu, Pause System, and Front-End Navigation Loop [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE (0 ERRORS)**
- **Implemented Components:**
  - **Historical Period Title Screen (`ARevolutionHUD::DrawTitleMenu`):**
    - Rendered full-screen antique sepia backdrop with ornamental double borders in antique brass (`#D1A647`) and muted sepia.
    - Multilingual typography: `REVOLUTION (क्रांति / ਕ੍ਰਾਂਤੀ)` and *"Amritsar, April 1919 — The Dawn of Freedom"*.
    - 4 interactive menu selections: `Begin Journey`, `Historical Codex`, `Settings`, and `Quit to Desktop`.
  - **In-Game Pause System (`ARevolutionHUD::DrawPauseMenu` & `ARevolutionCharacter::TogglePauseMenu`):**
    - `Escape` key and Gamepad `Special_Right` dynamically pause world tick (`UGameplayStatics::SetGamePaused`), unlock mouse cursor, and display a centered framed parchment card.
    - 6 interactive options: `Resume Game`, `Restart from Last Safe Checkpoint`, `Satchel Journal & Codex`, `Audio & Accessibility Settings`, `Return to Main Menu`, and `Quit to Desktop`.
  - **Safe Checkpoint Restart Loop:**
    - Seamlessly resets velocity and respawns Kabir at the last safe checkpoint location via `ARevolutionGameMode::RespawnPlayerAtCheckpoint()`.
  - **Pause-Aware Input Bindings:**
    - Menu navigation keys (`Up`, `Down`, `Enter`, `Escape`, `SpaceBar`, and Gamepad D-Pad/FaceButtons) configured with `.bExecuteWhenPaused = true` for responsive UI manipulation while world physics are halted.
  - **Master Continuous Integration (CI) Harness Integration:**
    - Authored `Scripts/verify_frontend_menus.py` (`TEST-15`), passing 100% with `Success - 0 error(s)` and exit code 0.
    - Master CI test harness (`run_all_tests.py` and `run_all_tests.ps1`) expanded to 15 suites.

---

---

### Task 30: Persistent Disk Save/Load System (`USaveGame`), Game State Serialization & Continue Journey Loop [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE (0 ERRORS)**
- **Implemented Components:**
  - **`URevolutionSaveGame` C++ Class:** Inherits from `USaveGame` with 19 serialized properties capturing narrative progress (Acts I–V), player location and rotation, stamina, satchel inventory (pamphlets, pebbles, chalk), discovered codex index, checkpoint transform, audio volumes, and SteamOS mode.
  - **`ARevolutionGameMode` Disk IO:** Authoritative methods `SaveGameToSlot()`, `LoadGameFromSlot()`, `DoesSaveGameExist()`, and `DeleteSaveSlot()` handling disk reads/writes to `Saved/SaveGames/RevolutionSave_Slot0.sav`.
  - **`URevolutionMissionSubsystem` Direct Stage Restoration:** Implemented `SetMissionStage()` for immediate narrative state deserialization and HUD banner broadcasting.
  - **Dynamic Title Menu Navigation:** Automatically detects existing save files on startup and surfaces `[ 1. CONTINUE JOURNEY (यात्रा जारी रखें) ]` along with `[ 2. BEGIN NEW JOURNEY ]`.
  - **In-Game Pause Menu Saving:** Added `[ 2. SAVE JOURNEY PROGRESS (प्रगति सहेजें) ]` with parchment audio feedback.
  - **Master Continuous Integration (CI) Harness Integration:**
    - Authored `Scripts/verify_save_load_system.py` (`TEST-16`), passing 100% with `Success - 0 error(s)` and exit code 0.
    - Master CI test harness (`run_all_tests.py` and `run_all_tests.ps1`) expanded to 16 suites.

---

### Task 31: Procedural Skeletal Idle Animations, Occupational Routine Life & Heritage Attire [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE (0 ERRORS)**
- **Implemented Components:**
  - **Procedural Respiration System (`CivilianNPCActor.cpp`):**
    - Sinusoidal human respiratory chest/shoulder movement ($Z \pm 1.25\text{ cm}$, pitch/roll $\pm 0.35^\circ$) calibrated to resting respiration ($15\text{ breaths/min}$, $0.25\text{ Hz}$).
  - **Archetype-Specific Occupational Micro-Gestures & Prop Dynamics:**
    - *Ram Lubhaya:* $5.0\text{ Hz}$ cast-iron Singer sewing machine treadle vibration & periodic forward seam inspection lean.
    - *Hira Halwai:* $0.8\text{ Hz}$ circular brass ladle tea stirring motion and rhythmic torso swaying.
    - *Ghasita Bhishti:* Asymmetric shoulder load tilt ($+1.8^\circ$), gentle weight shifts, and goatskin *mashk* slosh roll.
    - *Lala Karam Chand:* Horizontal fabric weave scanning ($\pm 2.5^\circ$ yaw) and downward inspection pitch dip.
    - *Pandit Kashi Ram:* Scholarly upright posture with thoughtful nods every 7 seconds.
    - *Kartar Singh:* Skyward gaze looking up at flying Basant fighter kites ($+12^\circ \pm 4^\circ$) and continuous spinning of the wooden *charkhi* kite spool.
  - **Culturally Researched Heritage Attire PBR Material Ingestion:**
    - Replaced all default mannequin gray materials (`MI_Manny_01`, `MI_Manny_02`) with authentic PBR textiles: `M_ClothUndyedCotton_PBR` (khadi), `M_ClothSaffron_PBR` (kesari), `M_ClothIndigo_PBR` (indigo), and `M_AgedTeak_PBR` (aged leather/salwar).
  - **Continuous 3D Spatialized Routine Foley Soundscape:**
    - Ingested 6 loopable 16-bit 44.1kHz audio assets: `SFX_Routine_SewingMachine_Loop`, `SFX_Routine_ChaiStir_Loop`, `SFX_Routine_MashkWater_Loop`, `SFX_Routine_ClothMerchant_Loop`, `SFX_Routine_Schoolmaster_Loop`, and `SFX_Routine_KartarKite_Loop` attached via `RoutineAudioComp` and attenuated with `ATT_Voice_Proximity`.
  - **Stumble Precedence Guard:** Physical sprint collisions cleanly suspend routine kinesics, spring-damping the NPC through balance recovery before smoothly resuming daily life.
  - **Master Continuous Integration (CI) Harness Integration:**
    - Authored `Scripts/verify_civilian_routines.py` (`TEST-17`), passing 100% with `Success - 0 error(s)` and exit code 0.
    - Master CI test harness (`run_all_tests.py` and `run_all_tests.ps1`) expanded to 17 suites: **100% PASS (17/17 SUITES PASSED) in 5.3 minutes**.

---

## 4. Overall Project Lifecycle & Milestone Status

All 32 planned milestones across Phases 1 through 5, Gold Master certification, and Post-Gold Master expansions/fixes (Tasks 0 through 31) have been fully implemented, validated in-engine with automated headless test suites, and certified with 0 errors:

- **Tasks 0–20:** Phases 1–5 Gold Master Development & Release Readiness (**100% COMPLETE & CERTIFIED**)
- **Task 21:** Authentic Punjabi Civilian Dialogue Localization & Ambient Proximity Voice System (**100% COMPLETE & CERTIFIED**)
- **Task 22:** Dynamic Non-Lethal Pedestrian Reaction & Crowd Stumble System (**100% COMPLETE & CERTIFIED**)
- **Task 23:** SteamOS & Handheld Proton Scalability Profile (**100% COMPLETE & CERTIFIED**)
- **Task 24:** Advanced Photogrammetry Texturing & Heritage Material Architecture (**100% COMPLETE & CERTIFIED**)
- **Task 25:** Historical Narrative Epilogue — "The Baisakhi Dawn" (**100% COMPLETE & CERTIFIED**)
- **Task 26:** Multi-Dialect Punjabi Voice Recording Expansion & Bazaar Walla System (**100% COMPLETE & CERTIFIED**)
- **Task 27:** Dynamic Time-of-Day Weather States, Andhi Dust Storm & Volumetric Fog (**100% COMPLETE & CERTIFIED**)
- **Task 28:** Curfew Sentry AI Collision Resolution & Patrol Path Restoration (**100% COMPLETE & CERTIFIED**)
- **Task 29:** In-Engine Title & Main Menu, Pause System, and Front-End Navigation Loop (**100% COMPLETE & CERTIFIED**)
- **Task 30:** Persistent Disk Save/Load System (`USaveGame`), Game State Serialization & Continue Journey Loop (**100% COMPLETE & CERTIFIED**)
- **Task 31:** Procedural Skeletal Idle Animations, Occupational Routine Life & Heritage Attire (**100% COMPLETE & CERTIFIED**)

**Current Roadmap Status:** **ALL 32 MILESTONES (0–31) ARE 100% COMPLETE, INTEGRATED, AND CERTIFIED IN-ENGINE (17/17 CI SUITES PASSING).**

---

### Task 32: Haveli Ground Floor Domestic Dressing & Village Exploration Boundaries [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE (0 ERRORS)**
- **Implemented Components:**
  - **Haveli Ground Floor Domestic Dressing (9 Period Elements):**
    - *Haveli_GF_Charpai_Veranda:* Authentic woven jute rope daybed (`SM_Prop_Charpai_RopeBed`) on the family veranda with photogrammetry woven jute texturing (`MI_WovenJute_Photogrammetry`).
    - *Haveli_GF_Brass_Lota_Hearth:* Traditional hammered brass *lota* (`SM_Prop_Overturned_Brass_Lota` with `MI_HammeredBrass_Photogrammetry`) and baked clay *kulhads* (`SM_Prop_ClayChaiCup_Kulhad` with `M_Clay_PBR`) beside the mud *chulha* cooking stove.
    - *Haveli_GF_GrainSack_Jute_01 & 02:* Stacked natural jute grain sacks (`SM_Prop_GrainSack_Jute_01`) and a woven spice/flour basket (`SM_Prop_SpiceBasket_Woven`) flanking the large carved grain *sandook*.
    - *Haveli_GF_Takhta_Shutter_TailorShop:* Foldable aged teak *takhta* shop shutters (`SM_Shop_Shutter_Foldable` with `M_AgedTeak_PBR`) and khadi/muslin cloth rolls (`SM_Prop_ClothRolls_Manchester` with `M_ClothUndyedCotton_PBR`) on the cutting bench.
    - *Haveli_GF_HurricaneLantern_Niche:* Hurricane lantern (`SM_Prop_HurricaneLantern` with `MI_HammeredBrass_Photogrammetry`) resting on an architectural brick niche.
  - **Village Exploration Perimeter Boundaries (6 Physical Enclosures):**
    - *Boundary_Wall_South_HaveliCenter:* Solid Lahori brick wall module (`SM_Wall_Brick_4x4m_A`) at $(0, -600, 0)$ bridging the rear haveli walls.
    - *Boundary_Wall_West_DeorhiGap:* Massive stone town rampart (`SM_Wall_Town_Faseel_Rampart`) at $(-650, 350, 0)$ enclosing the western alleyway perimeter.
    - *Boundary_Wall_East_MohallaAlley:* Town rampart module (`SM_Wall_Town_Faseel_Rampart`) at $(650, 850, 0)$ sealing the eastern perimeter toward the school grounds.
    - *Boundary_Barrier_NorthGate_West & East:* Sandbag and timber picket barriers (`SM_Checkpoint_Picket_Sandbag_Barrier`) flanking the checkpoint at $Y = 2150$.
    - *Boundary_Wall_North_CantonmentSeal:* Full-height brick barrier (`SM_Wall_Brick_4x4m_A` scaled $1.5\times$ $Z$) at $(0, 2250, 0)$ preventing player fall-out beyond the military checkpoint.
  - **Master Continuous Integration (CI) Harness Integration:**
    - Authored `Scripts/verify_haveli_boundaries.py` (`TEST-18`), passing 100% with `Success - 0 error(s)` and exit code 0.
    - Master CI test harness (`run_all_tests.py` and `run_all_tests.ps1`) expanded to 18 suites: **100% PASS (18/18 SUITES PASSED) in 4.97 minutes**.

---

## 4. Overall Project Lifecycle & Milestone Status

All 33 planned milestones across Phases 1 through 5, Gold Master certification, and Post-Gold Master expansions/fixes (Tasks 0 through 32) have been fully implemented, validated in-engine with automated headless test suites, and certified with 0 errors:

- **Tasks 0–20:** Phases 1–5 Gold Master Development & Release Readiness (**100% COMPLETE & CERTIFIED**)
- **Task 21:** Authentic Punjabi Civilian Dialogue Localization & Ambient Proximity Voice System (**100% COMPLETE & CERTIFIED**)
- **Task 22:** Dynamic Non-Lethal Pedestrian Reaction & Crowd Stumble System (**100% COMPLETE & CERTIFIED**)
- **Task 23:** SteamOS & Handheld Proton Scalability Profile (**100% COMPLETE & CERTIFIED**)
- **Task 24:** Advanced Photogrammetry Texturing & Heritage Material Architecture (**100% COMPLETE & CERTIFIED**)
- **Task 25:** Historical Narrative Epilogue — "The Baisakhi Dawn" (**100% COMPLETE & CERTIFIED**)
- **Task 26:** Multi-Dialect Punjabi Voice Recording Expansion & Bazaar Walla System (**100% COMPLETE & CERTIFIED**)
- **Task 27:** Dynamic Time-of-Day Weather States, Andhi Dust Storm & Volumetric Fog (**100% COMPLETE & CERTIFIED**)
- **Task 28:** Curfew Sentry AI Collision Resolution & Patrol Path Restoration (**100% COMPLETE & CERTIFIED**)
- **Task 29:** In-Engine Title & Main Menu, Pause System, and Front-End Navigation Loop (**100% COMPLETE & CERTIFIED**)
- **Task 30:** Persistent Disk Save/Load System (`USaveGame`), Game State Serialization & Continue Journey Loop (**100% COMPLETE & CERTIFIED**)
- **Task 31:** Procedural Skeletal Idle Animations, Occupational Routine Life & Heritage Attire (**100% COMPLETE & CERTIFIED**)
- **Task 32:** Haveli Ground Floor Domestic Dressing & Village Exploration Boundaries (**100% COMPLETE & CERTIFIED**)
- **Task 33:** Rooftop Traversal, Vertical Ladder Traversal & Mantling Feedback (**100% COMPLETE & CERTIFIED**)

**Current Roadmap Status:** **ALL 34 MILESTONES (0–33) ARE 100% COMPLETE, INTEGRATED, AND CERTIFIED IN-ENGINE (19/19 CI SUITES PASSING, 0 ERRORS).**

---

### Task 34: Seamless Act I In-World Objective Beacons & Mohalla Compass Indicators [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE (0 ERRORS)**
- **Implemented Components:**
  - **C++ Mission Subsystem Query Architecture (`URevolutionMissionSubsystem`):**
    - Added `GetActiveObjectiveLocation(FVector& OutLocation, FText& OutObjectiveName) const` dynamically querying in-world `AObjectiveTriggerActor`, `ACivilianNPCActor`, and named level actors (`Haveli_Rooftop_Basant_Kite`, `School_Bell_Tower`, etc.), with canonical coordinate fallbacks across all 8 Act I stages and later act milestones.
    - Terminal state detection: correctly returns `false` (in C++) / `None` (in Python) upon `Stage_Completed`.
  - **In-World Tactical Objective Beacon (`ARevolutionHUD::DrawInWorldObjectiveBeacon`):**
    - Dynamic 3D world-to-screen projection (`ProjectWorldLocationToScreen`) rendering an antique brass/gold diamond marker with breathing pulse ($0.85 + 0.15 \times \sin(3.5t)$), center gold pip, and vertical anchor stem pointing to the target.
    - Dual distance alpha attenuation: visible within 40m (extended to 80m during Basant Intuition / Keen Senses), with near-field feathering fading out below 3.0m down to 1.2m to prevent UI clutter during close-up dialogue/inspection.
    - Contextual badge display: renders `[ OBJECTIVE — 18m ]` with landmark title badge within 25m.
  - **Mohalla Compass Ribbon Waypoint Projection (`ARevolutionHUD::DrawCompass`):**
    - Projects active objective bearing onto the top compass ribbon as a pulsing antique gold diamond waypoint whenever within the $\pm 40^\circ$ FOV.
  - **Master Continuous Integration (CI) Harness Integration:**
    - Authored `Scripts/verify_objective_beacons.py` (`TEST-20`), passing 100% with `Success - 0 error(s)` and exit code 0.
    - Master CI test harness (`run_all_tests.py` and `run_all_tests.ps1`) expanded to 20 suites: **100% PASS (20/20 SUITES PASSED) in 5.9 minutes**.

---

## 4. Overall Project Lifecycle & Milestone Status

All 35 planned milestones across Phases 1 through 5, Gold Master certification, and Post-Gold Master expansions/fixes (Tasks 0 through 34) have been fully implemented, validated in-engine with automated headless test suites, and certified with 0 errors:

- **Tasks 0–20:** Phases 1–5 Gold Master Development & Release Readiness (**100% COMPLETE & CERTIFIED**)
- **Task 21:** Authentic Punjabi Civilian Dialogue Localization & Ambient Proximity Voice System (**100% COMPLETE & CERTIFIED**)
- **Task 22:** Dynamic Non-Lethal Pedestrian Reaction & Crowd Stumble System (**100% COMPLETE & CERTIFIED**)
- **Task 23:** SteamOS & Handheld Proton Scalability Profile (**100% COMPLETE & CERTIFIED**)
- **Task 24:** Advanced Photogrammetry Texturing & Heritage Material Architecture (**100% COMPLETE & CERTIFIED**)
- **Task 25:** Historical Narrative Epilogue — "The Baisakhi Dawn" (**100% COMPLETE & CERTIFIED**)
- **Task 26:** Multi-Dialect Punjabi Voice Recording Expansion & Bazaar Walla System (**100% COMPLETE & CERTIFIED**)
- **Task 27:** Dynamic Time-of-Day Weather States, Andhi Dust Storm & Volumetric Fog (**100% COMPLETE & CERTIFIED**)
- **Task 28:** Curfew Sentry AI Collision Resolution & Patrol Path Restoration (**100% COMPLETE & CERTIFIED**)
- **Task 29:** In-Engine Title & Main Menu, Pause System, and Front-End Navigation Loop (**100% COMPLETE & CERTIFIED**)
- **Task 30:** Persistent Disk Save/Load System (`USaveGame`), Game State Serialization & Continue Journey Loop (**100% COMPLETE & CERTIFIED**)
- **Task 31:** Procedural Skeletal Idle Animations, Occupational Routine Life & Heritage Attire (**100% COMPLETE & CERTIFIED**)
- **Task 32:** Haveli Ground Floor Domestic Dressing & Village Exploration Boundaries (**100% COMPLETE & CERTIFIED**)
- **Task 33:** Rooftop Traversal, Vertical Ladder Traversal & Mantling Feedback (**100% COMPLETE & CERTIFIED**)
- **Task 34:** Seamless Act I In-World Objective Beacons & Mohalla Compass Indicators (**100% COMPLETE & CERTIFIED**)
- **Task 35:** Act I Finale to Act II Cinematic Handoff & Munadi Proclamation Sequence (**100% COMPLETE & CERTIFIED**)
- **Task 36:** Grand Bazaar Chowk Munadi Crowd Clatter & Dynamic Dialogue System (**100% COMPLETE & CERTIFIED**)
- **Task 37:** Act II Questline — "The Rumors of Baisakhi" & Checkpost Eavesdropping (**100% COMPLETE & CERTIFIED**)
- **Task 38:** Baisakhi Fair Ground Atmosphere & Gathering Expansion (**100% COMPLETE & CERTIFIED**)
- **Task 39:** RDR2-Inspired Volumetric Smoke, Curl Noise Flow & Atmospheric Optics System (**100% COMPLETE & CERTIFIED**)
- **Task 40:** Act II Climax — The Massacre of Jallianwala Bagh & The Firing Line (**100% COMPLETE & CERTIFIED**)
- **Task 41:** Act III — The Desolate Night & Clandestine Medical Evacuation (**100% COMPLETE & CERTIFIED**)
- **Task 42:** Act IV — The Rural Outskirts & Upper Bari Doab Canal Feeder Network (**100% COMPLETE & CERTIFIED**)

**Current Roadmap Status:** **ALL 43 MILESTONES (0–42) ARE 100% COMPLETE, INTEGRATED, AND CERTIFIED IN-ENGINE (28/28 CI SUITES PASSING, 0 ERRORS).**

---

### 37. Task 37: Act II Questline — "The Rumors of Baisakhi" & Checkpost Eavesdropping [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE (TEST-23 PASSED, 0 ERRORS)**
- **Implemented Components:**
  - **Colonial Checkpost Eavesdropping Mechanic:**
    - C++ property `bRequireStealthForInteraction` in `AObjectiveTriggerActor`. Requires Kabir to be crouched, crowd-blended, or in shadow concealment (score $> 0.25$) to eavesdrop behind sandbags at $(-40, 2080, 50)$.
    - Foley audio cue: `SFX_Conceal_Cloth_Rustle`.
  - **Secret Meeting Leaflet Retrieval:**
    - Contraband satchel increment `AwardPamphletsOnTrigger = 2` from Lala Karam Chand's khadi cloth bolts (`SM_Prop_ClothRolls_Manchester`) at $(210, 1960, 50)$ at the textile mandi.
    - Tactile handling audio cue: `SFX_Pamphlet_Retrieve`.
  - **Curfew Infiltration Route & Sentry AI:**
    - Back-alley stealth path avoiding Constable Gurdial's patrol radius towards northern choke-point $(900, 2250, 50)$.
  - **Mission Subsystem Expansion:**
    - Extended `ECourierMissionStage` with `Stage_Afternoon_EavesdropCheckpost` and `Stage_Afternoon_ClothBoltLeaflets`.
    - Authentic Majhi Punjabi and English directives and 3D compass waypoint positions.
  - **Level Assembly & Zero-Regression QA:**
    - Placed and saved both triggers in `L_Validation_Gym.umap` (231 total actors).
    - Headless verification suite `Scripts/verify_act2_questline.py` (`TEST-23`) passing 6/6 subtests with 0 errors.
    - Master CI harness expanded to 23 automated suites.

---

### 38. Task 38: Baisakhi Fair Ground Atmosphere & Gathering Expansion [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE (TEST-24 PASSED, 0 ERRORS)**
- **Implemented Components:**
  - **Two New Grounded Historical Civilian Archetypes:**
    - `BaisakhiPilgrim` (Bhai Gurmukh Singh, Peasant Farmer from Tarn Taran): Sacred saffron turban (`M_ClothSaffron_PBR`), undyed khadi kurta (`M_ClothUndyedCotton_PBR`), attached jute grain sack prop (`SM_Prop_GrainSack_Jute_01`), crowd-scanning micro-gestures.
    - `FairVendor` (Chacha Milkha, Baisakhi Mela Sweet & Toy Vendor): Saffron kurta, indigo lower, spinning pinwheel toy spool (`SM_Prop_Kite_Spool_Charkhi`), vocal hawker gestures.
  - **Festival Market Dressing & Historical Landmark Assembly:**
    - Assembled `Prop_Baisakhi_Mela_Sweet_Stall` at $(1020, 2440, 0)$ and `Prop_Baisakhi_Garland_Archway` at $(950, 2350, 0)$.
    - Placed `Trigger_Baisakhi_Pandal` at $(1450, 3100, 50)$ and `Trigger_Shahidi_Kua` at $(1200, 2950, 50)$ persistently in `L_Validation_Gym.umap` (237 total actors).
  - **Dynamic Stage-Aware Dialogue & Historical Lore:**
    - Act I joyous harvest snan and spinning pinwheels transitioning to Act II emergency warnings of Dyer's armored cars unable to fit through the 2.2-meter alleyway mouth.
  - **Mission Subsystem Integration:**
    - Interacting with Bhai Gurmukh Singh or the Pandal Dais trigger at $(1450, 3100, 50)$ advances mission stage to `Stage_ActII_TheFiring` at $(1250, 2800, 50)$.
  - **Automated QA Verification Suite:**
    - Authored `Scripts/verify_baisakhi_fairground.py` (`TEST-24`), certifying 6/6 subtests with 0 errors.
    - Master CI harness expanded to 24 test suites.

---

### 39. Task 39: RDR2-Inspired Volumetric Smoke, Curl Noise Flow & Atmospheric Optics System [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE (TEST-25 PASSED, 0 ERRORS)**
- **Implemented Components:**
  - **RDR2 RAGE Engine Binary Decompilation & Introspection:**
    - Analyzed `C:\Program Files\Red Dead Redemption 2\RDR2.exe` using REA and PE symbol introspection.
    - Reverse-engineered `ptxu_PyroclasticVolume` (bounding sphere clustering), `ptxu_Noise_m_curlNoiseStrengthKFP` (divergence-free vorticity), `SunScatteringLUTTex` (Mie forward scattering "silver lining"), and `ptxu_UvDistortion` (screen-space refraction).
  - **Procedural PBR Textures Synthesized:**
    - `T_Smoke_Pyroclastic_Puff.tga` (512x512, 32-bit): 6-lobed spherical Gaussian billows with fBm perturbation and radial normal map vectors.
    - `T_Smoke_CurlNoise_Flow.tga` (512x512, 32-bit): Mathematical finite-difference curl noise flow map driving dynamic UV advection.
  - **Master Materials & Material Instances:**
    - `M_RDR2_Pyroclastic_Smoke.uasset`: Translucent Unlit master material with Depth Fade (`DepthFadeDistance = 75`), dual-band curl noise panner advection, and Fresnel forward Mie scattering rim.
    - `M_RDR2_HeatHaze.uasset`: Screen-space refraction index ($1.0 + 0.045 \cdot (\text{FlowNoise} - 0.5)$) with fast upward convection and distance falloff.
    - 4 production material instances: `MI_Smoke_Chulha_Campfire`, `MI_Smoke_Haveli_Chimney`, `MI_Smoke_Gunpowder_Muzzle`, and `MI_Smoke_Locomotive_Steam`.
  - **C++ Gameplay & Actor Integration:**
    - Updated `ALocomotiveSteamValveActor` with dynamic `SteamPlumeMesh` configured with `MI_Smoke_Locomotive_Steam`, procedurally scaling from 1.0 to 4.5 over 14 seconds when vented to provide sentry line-of-sight stealth obscurity.
    - Level placement in `L_Validation_Gym.umap`: `BP_Chulha_Fireplace_RDR2`, `Light_Chulha_Flame_Bounce`, `HeatHaze_Chulha`, `Smoke_Plume_Chulha`, `BP_Haveli_Rooftop_Chimney_RDR2`, `Smoke_Plume_Rooftop_Chimney`, and `Locomotive_Steam_Pressure_Relief_Valve`.
  - **Automated Verification:**
    - In-engine test `Scripts/verify_rdr2_smoke_integration.py` (`TEST-25`) passed with **100% SUCCESS (0 errors)** across 7 actors, 6 materials, and 2 textures.
    - Story simulation `verify_pie_master_walkthrough.py` validated all 29 narrative stages with 0 errors.
    - Master CI harness expanded to 25 automated suites.
    - Comprehensive report artifact: `RDR2_SMOKE_ANALYSIS_AND_INTEGRATION_REPORT.md`.

---

### 40. Task 40: Act II Climax — The Massacre of Jallianwala Bagh & The Firing Line [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE (TEST-26 PASSED, 0 ERRORS)**
- **Implemented Components:**
  - **Colonial Armored Car Blockade:** Placed `British_Armored_Car_Obstacle_North` and `South` (`SM_British_Armored_Car_Obstacle`) blocking the 2.2m narrow entrance corridor outside the Faseel archway.
  - **Raised Bank Tactical Firing Line:** Deployed 4 ranked riflemen pickets (`Picket_Rifleman_Alpha..Delta`) and `Officer_GeneralDyer_Command` on `SM_Jallianwala_Raised_Bank` ($Z = 120$).
  - **Volumetric Gunpowder Muzzle Plumes (RDR2 Inspired):** 3 dynamic smoke plume actors (`Gunsmoke_Plume_RaisedBank_01..03`) using `MI_Smoke_Gunpowder_Muzzle` producing a thick, rolling sulfurous haze across the firing line.
  - **Memorial Bullet-Pocked Walls & Scatter Debris:** Positioned `Jallianwala_Bullet_Pocked_Wall_East_02` and `North`, plus panic debris scatters (`Prop_Fallen_Turban_Scatter_WellApproach` and `BreachApproach`).
  - **Parkour Wall Breach Escape Traversal:** Fully functional athletic mantle vault over the 1.75m crumbling brick talus at `Jallianwala_Crumbling_Wall_Breach_West` $(650, 3350, 0)$.
  - **Automated Verification:** Authored and validated `Scripts/verify_act2_climax_firing_line.py` (`TEST-26`), passing 7/7 subtests with 0 errors. Story simulation `verify_pie_master_walkthrough.py` re-validated all 29 stages. CI harness expanded to 26 suites.
  - Comprehensive documentation in `Documentation/TASK_40_ACT2_CLIMAX_FIRING_LINE_REPORT.md`.

---

### 41. Task 41: Act III — The Desolate Night & Clandestine Medical Evacuation [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE (TEST-27 PASSED, 0 ERRORS)**
- **Implemented Components:**
  - **Clandestine Medical Safehouse Clinic:** Placed dual bamboo charpai stretchers (`Story_Makeshift_Stretcher_Alley` & `Makeshift_Stretcher_Charpai_Clinic_02`), medical supply cache, rolled khadi cotton bandages, hurricane lantern, and volunteer elder NPC (`NPC_Clinic_Volunteer_Elder`) at $(-120, 950, 0)$.
  - **Imperial Searchlight Picket & Sandbag Bunker:** Positioned `Light_Searchlight_CarbonArc_Beam` casting cool carbon-arc beam ($16000\text{ lm}$, volumetric scattering $3.5$) and `NPC_Curfew_Sentry_Bunker` at $(0, 2260, 0)$.
  - **Curfew Notice Station:** Positioned `Story_Curfew_Notice_Martial_Law_Chowk` with dedicated overhead niche lantern at $(-80, 1850, 0)$.
  - **Automated Verification:** `Scripts/verify_act3_medical_evacuation.py` (`TEST-27`) certified 5/5 subtests with 0 errors. Documented in `Documentation/TASK_41_DESOLATE_NIGHT_CLINIC_REPORT.md`.

---

### 42. Task 42: Act IV — The Rural Outskirts & Upper Bari Doab Canal Feeder Network [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE (TEST-28 PASSED, 0 ERRORS)**
- **Implemented Components:**
  - **Masonry Canal Aqueduct Sluice Gate:** Dressed sandstone piers, cast-iron lift sheets, catwalk, lantern, and 3D localized sound actor `Audio_Canal_Water_Flow` with `SFX_Canal_Water_Flow_Gentle` at $(-950, 2200, 0)$.
  - **Timber Persian Wheel (Rahat) Machinery:** 3.0m wooden wheel, terracotta water pots, timber flume, lantern, and 3D localized sound actor `Audio_Persian_Wheel_Creak` with `SFX_Persian_Wheel_Rahat_Creak` at $(-1150, 2050, 0)$.
  - **Agrarian Field Dressing:** Placed `Prop_Wheat_Harvest_BullockCart_Canal` (`SM_Prop_Wheat_Sheaves_Cart`) providing crouch cover along canal banks.
  - **Automated Verification:** `Scripts/verify_act4_canal_outskirts.py` (`TEST-28`) certified 5/5 subtests with 0 errors. Documented in `Documentation/TASK_42_CANAL_OUTSKIRTS_REPORT.md`.

---

### 43. Task 43: Act IV Climax — The Bhatta Brick Kiln Resistance Infiltration & Underground Press [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE (TEST-29 PASSED, 0 ERRORS)**
- **Implemented Components:**
  - **Bull's Trench Conical Chimney:** 7.5m tapered brick stack (`Industrial_Brick_Kiln_Bhatta_Chimney`) at $(-1250, 2650, 0)$.
  - **RDR2-Inspired Industrial Smoke Plume:** Anchored at chimney crown ($Z = 780$) with `MI_Smoke_Haveli_Chimney` and curl-noise draft velocity advection.
  - **Subterranean Flue Fire Glow:** `Light_Bhatta_Kiln_Flue_Glow` ($2200\text{ lm}$, ember orange, radius $480\text{ cm}$) radiating warmth through kiln vents.
  - **Underground Lithographic Press & Supply Cache:** `Story_Clandestine_Safehouse_Supply_Cache`, khadi handbill bundles, brass work lantern, and task light at $(-1180, 2520, 0)$.
  - **Resistance Courier Contact NPC:** `NPC_Resistance_Courier_Liaison` positioned at $(-1200, 2540, 88)$.
  - **Automated Verification:** `Scripts/verify_act4_climax_brick_kiln.py` (`TEST-29`) passed 5/5 subtests with 0 errors. Documented in `Documentation/TASK_43_BRICK_KILN_PRESS_REPORT.md`.

---

### 44. Task 44: Act V — North Western Railway Cutting, Signal Gantry & Locomotive Climax [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE (TEST-30 PASSED, 0 ERRORS)**
- **Implemented Components:**
  - **Broad-Gauge Steam Locomotive & Steam Valve:** British Indian 4-6-0 locomotive `Locomotive_Engine_PunjabMail_Depot` at $(1000, 3900, 30)$, interactive steam obscurity valve `Locomotive_Steam_Pressure_Relief_Valve`, RDR2 curl-noise smokestack plume `Smoke_Plume_Locomotive_PunjabMail`, and high-powered boiler headlamp ($14000\text{ lm}$).
  - **Lattice-Steel Semaphore Signal Gantry & Ladder:** `Colonial_Railway_Signal_Gantry_Junction` at $(1160, 3960, 0)$, dual kerosene amber/green signals, and `Ladder_Signal_Gantry_Climb` (`ALadderActor`) climbing to the $6.5\text{m}$ catwalk deck.
  - **Cantonment Gate Sentry Picket:** `Cantonment_Guardhouse_Picket_NorthGate`, watchman `NPC_Cantonment_Sentry_NorthGate` (`CurfewPatrolAI`), and gate searchlight at $(650, 4200, 10)$.
  - **Civil Lines Bungalow HQ & Martial Law Archive:** Doric veranda bungalow `Civil_Lines_Clubhouse_Bungalow_HQ`, telegraph station, confidential archive cabinet, and veranda lighting at $(820, 4520, 60)$.
  - **Automated Verification:** `Scripts/verify_act5_railway_climax.py` (`TEST-30`) passed 5/5 subtests with 0 errors. Documented in `Documentation/TASK_44_RAILWAY_CLIMAX_REPORT.md`.

---

### 45. Task 45: Master Gold Master Release Build, Packaging & Final Certification [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE (ALL 30 TEST SUITES PASSED, BUILD SUCCESSFUL)**
- **Implemented Components:**
  - **Master PIE Narrative Simulation:** `verify_pie_master_walkthrough.py` re-verified all 29 story stages, audio triggers, historical dignity standards, and character mechanics with 100% success and 0 errors.
  - **Full CI Test Harness:** All 30 regression test suites (`TEST-01` through `TEST-30`) registered and passing across both Python (`run_all_tests.py`) and PowerShell (`run_all_tests.ps1`) runners.
  - **Automated Release Packaging:** Executed `package_windows_release.ps1` via `RunUAT.bat BuildCookRun` compiling C++20 binaries, cooking `/Game/Maps/L_Validation_Gym` (289 actors), and archiving standalone distribution to `Build/Development/Windows/`.
  - **Standalone Package Audit:** `verify_standalone_package.py` verified launcher binary, Win64 target executable, all 5 IoStore/pak containers ($932.6\text{ MB}$ package), and NVIDIA GeForce GTX 1650 hardware budget compliance ($3412\text{ MB}$ VRAM, $46.7\text{ FPS}$).
  - **Final Release Certification:** Comprehensive sign-off authored in `Documentation/GOLD_MASTER_FINAL_RELEASE_REPORT.md`.

---

## 5. Master Project Completion Status & Roadmap Reconciliation

```
================================================================================
  PROJECT REVOLUTION (क्रांति) — ROADMAP & PHASE SUMMARY RECONCILIATION
================================================================================
  Phase 1: Foundation, C++ Architecture & Core Mechanics   -> Tasks 0-4
  Phase 2: World Building, Mohalla & Vernacular School     -> Tasks 5-9
  Phase 3: Colonial Boundaries & Cantonment Infrastructure  -> Tasks 10-14
  Phase 4: Full Narrative Arc, Audio Mix & QoL Codex       -> Tasks 15-24
  Phase 5A: Epilogue, Audio Walla & Core Systems Expansion -> Tasks 25-31
  Phase 5B: Mohalla World Dressing, Rooftops & Act Handoff -> Tasks 32-38
  Phase 5C: Atmospheric Optics & Dual Task 39 Scope        -> Task 39 (Smoke & Community Trust)
  Phase 6: Climax Environments & Story Progression         -> Tasks 40-44
  Phase 7: Packaging, Candidate Builds & Verification     -> Task 45
  Phase 8: Kabir v05 Locomotion Suite & PBR Overhaul       -> Task 46
  Phase 9: Runtime Defect Remediation & Shipping Release   -> Audit Report (AUDIT-REV-2026-FINAL)
  Phase 10: End-to-End QA Traversal & Production Hardening -> Task 47 (TEST-32 to TEST-36) [COMPLETED]
  Phase 11: Kabir v06 Lineup & Pehchan-Talashi Mechanics  -> Tasks 48-49 (TEST-37 to TEST-39) [COMPLETED]
================================================================================
```

### Roadmap Reconciliations & Task ID Conflict Record

> [!NOTE] Phase Summary Task Omission Resolution (Tasks 26–38)
> In previous phase summary tables, the table jumped directly from Phase 4 (Tasks 15–24) to Phase 5 ("Task 25 & 39–40"), omitting Tasks 26 through 38 from the phase breakdown despite individual task descriptions and verification suites being documented in detail in Section 4. The reconciled phase breakdown above explicitly accounts for all tasks:
> - **Tasks 26–31 (Phase 5A):** Multi-Dialect Punjabi Walla, Dynamic Weather States, Curfew Sentry AI, Frontend Menus, Disk Persistence (`USaveGame`), and Skeletal Routine Animations.
> - **Tasks 32–38 (Phase 5B):** Haveli Ground Floor Dressing, Rooftop Traversal & Mantling, Objective Beacons & Compass, Act I to Act II Handoff, Chowk Munadi Crowd Clatter, Act II Eavesdropping, and Baisakhi Fair Ground Expansion.

> [!IMPORTANT] Dual Task 39 Mapping Conflict Documentation
> Two separate major systems were historically assigned ID `Task 39` across project reports and test suites. Rather than renumbering established project artifacts, both mappings are preserved and documented here:
> 1. **Task 39A (Volumetric Smoke & Atmospheric Optics):**
>    - Primary Document: `Documentation/RDR2_SMOKE_ANALYSIS_AND_INTEGRATION_REPORT.md`
>    - CI Test: `TEST-25` (`Scripts/verify_rdr2_smoke_integration.py`)
>    - Implemented Scope: 4-phase curl noise volumetric smoke, optical Mie/Rayleigh extinction, and locomotive chimney heat haze.
> 2. **Task 39B (Community-Trust System 'Izzat & Vishwas'):**
>    - Primary Document: `Documentation/TASK_39_COMMUNITY_TRUST_REPORT.md`
>    - CI Test: `TEST-31` (`Scripts/verify_community_trust.py`)
>    - Implemented Scope: Localized reputation clusters (`UCommunityTrustSubsystem`), Deorhi door auto-bolting, civilian reaction barks, and persistent disk serialization via `URevolutionSaveGame`.
















---

### 46. Task 46: Kabir v05 RDR2-Inspired Locomotion Suite, Euphoria Posture & Punjabi Bronze PBR Overhaul [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE (31/31 CI SUITES PASSED, 0 ERRORS)**
- **Implemented Components:**
  - **RDR2-Inspired Locomotion Suite:**
    - `Anim_Kabir_v05_Idle` (120f / 4.0s): Asymmetric weight shift (pelvis shifted 0.8 cm over right leg), 4-second sinusoidal respiration wave, curfew sentry observation head micro-glances (frame 35 left, frame 85 right, seamless loop).
    - `Anim_Kabir_v05_Walk` (30f / 1.0s): Authentic 12-year-old child cadence (2 steps/sec / 120 BPM), pelvic vertical bobbing (-1.2 cm strike, +1.0 cm pass), Trendelenburg hip roll (3.0 deg), torso counter-twist (3.5 deg), phase-locked arm swings.
    - `Anim_Kabir_v05_Run` (20f / 0.67s): 9-degree forward athletic lean, high knee drive (flexion +65 deg), bent arm pumping (60 deg elbow bend, +-32 deg swing), vertical flight bounce.
    - `Anim_Kabir_v05_Stop` (16f / 0.53s): RDR2 momentum deceleration settle where lead foot plants, pelvis and spine absorb forward inertia and settle into idle base.
  - **Blender Armature Symmetry Matrix:**
    - Resolved edit mode bone roll asymmetry on `upperarm_l` vs `upperarm_r`, achieving exact mirror symmetry with 25-degree pitch, 60-degree hang, and 5-degree forearm bend, keeping hands skimming outer thighs naturally without torso clipping.
  - **Vertex Weight Forensics & Fixes:**
    - Stripped spurious 55%-75% root bone vertex weights on `v05_Kabir_Sandals`, transferring clean weights from foot bones via DataTransfer modifier.
    - Removed calf, forearm, and thumb weights on `v05_Kabir_Satchel`, normalizing strictly to pelvis and spine bones.
  - **Authentic Historical Punjab PBR Materials:**
    - Skin: Authentic North Indian Punjabi bronze complexion (`#B37F56` / `[117, 55, 23]`) with `MSM_DEFAULT_LIT` standard PBR shading.
    - Eyes: Warm dark brown eyes with cornea specularity.
    - Hair: Deep espresso hair (`#1A1412`).
    - Attire: Authentic handloom cream khadi weave (`#E8DEC8` / `#D0BC96`) with blue shorts and saddle brown leather satchel/sandals (`#593926`).
    - Enabled `used_with_skeletal_mesh = True` across all 5 master materials, resolving both the flat grey clay fallback and subsurface blowout under key lights.
  - **Full Automated CI Verification & Standalone Win64 Packaging:**
    - In-engine standalone `-game` validation screenshot captured in Haveli deorhi foyer: `v05_InEngine_PlayableKabir.png`.
    - Executed all 31 automated regression test suites via `Scripts/run_all_tests.py`: **100% PASS (31/31 SUITES PASSED) in 8.92 minutes** with 0 errors.
    - Packaged standalone distribution via `RunUAT.bat BuildCookRun` to `Build/Development/Windows/REVOLUTION.exe` with Zen/IoStore compression (932.9 MB package, 100% PASS on `verify_standalone_package.py`).

---

### 47. Task 47: End-to-End Interactive QA Playthrough Bot & 29-Stage Telemetry Verification [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE (32/32 CI SUITES PASSED, 0 ERRORS)**
- **Implemented Components:**
  - **End-to-End Interactive Playthrough Bot (`Scripts/verify_e2e_interactive_playthrough.py` / `TEST-32`):**
    - Spawns/references protagonist Kabir at the Haveli courtyard start location `(0.0, 220.0, 75.0)` in master level `L_Validation_Gym.umap` (298 actors).
    - Traverses all 29 sequential story milestones from Act I through Act V finale without skipping or deadlock.
    - Continuous physical capsule collision sweeps (`sweep=True`) across 10 intermediate segments per waypoint, verifying zero collision blocks along pedestrian walking paths.
    - Supports vertical ladder traversal (Courtyard to 1F Terrace, Signal Gantry) and parkour mantle vaults (Wall breach) into landing decks.
    - Simulates stealth crouch posture (`b_is_crouched = True`) when approaching the colonial checkpost eavesdropping station.
    - Triggers `OnInteract()` on each target NPC and objective trigger, advancing `URevolutionMissionSubsystem` state machine.
    - Verifies synchronized dynamic atmosphere transitions across all 5 historical acts:
      - Act I: `MorningDawn` (3200K, Steps 1–8)
      - Act II: `BaisakhiMidday` (5200K, Steps 9–17)
      - Act III: `CurfewNight` (8500K, Steps 18–21)
      - Act IV: `CanalNight` (6500K, Steps 22–25)
      - Act V: `GoldenSunrise` (2850K, Steps 26–29)
    - Confirms `is_mission_complete() == True` upon reaching Stage 29.
    - Total physical exploration distance recorded: **205.5 meters**.
  - **Playthrough Telemetry Serialization:**
    - Structured telemetry output saved to `Documentation/E2E_PLAYTHROUGH_TELEMETRY.json` with per-stage coordinates, segment distances, cumulative distances, simulated durations, and atmosphere phases.
  - **Master CI Test Harness Upgrade:**
    - Registered `TEST-32` in `Scripts/run_all_tests.py` and `Scripts/run_all_tests.ps1`.
    - Executed all 32 automated regression test suites: **100% PASS (32/32 SUITES PASSED) in 11.21 minutes** with 0 errors.

---

### 48. Task 48: Kabir v06 Heritage Character Lineup, 16 Animation Sequences & Cinematic Showcase [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE (TEST-37 & TEST-38 PASSED, 0 ERRORS)**
- **Implemented Components:**
  - **3 Life-Stage Hero Skeletal Meshes:**
    - `SKM_Kabir_v06_Child_12` (12-year-old child protagonist, height 128 cm, khadi kurta and blue shorts).
    - `SKM_Kabir_v06_Teen_16` (16-year-old youth, height 155 cm, pajama and bandi vest).
    - `SKM_Kabir_v06_Adult_25` (25-year-old revolutionary, height 178 cm, full dhoti kurta and angavastram).
  - **8 PBR Heritage Materials:**
    - `M_Kabir_v06_Skin`, `M_Kabir_v06_Eye`, `M_Kabir_v06_Hair`, `M_Kabir_v06_Khadi_Cream`, `M_Kabir_v06_Khadi_Pajama`, `M_Kabir_v06_Angavastram`, `M_Kabir_v06_Leather`, `M_Kabir_v06_Brass`.
  - **16 Custom Animation Sequences (`/Game/Characters/Kabir_v06/Animations/`):**
    - Locomotion: Idle, Walk, Run, Stop, Crouch Idle, Crouch Walk.
    - Combat & Weapons: Weapon Pickup, Weapon Draw, Weapon Aim, Weapon Shoot, Weapon Holster.
    - Traversal & Agility: Jump, Climb Ladder, Mantle.
    - Diegetic Interaction: Satchel Open, Curfew Listen.
  - **3 Playable Character Blueprints:** `BP_Kabir_v06_Child_12`, `BP_Kabir_v06_Teen_16`, `BP_Kabir_v06_Adult_25`.
  - **Dedicated Showcase Map:** `L_Kabir_v06_Showcase.umap` (303 level actors, 3 life-stage hero lineup, Master CineCamera).
  - **Automated Verification:** `TEST-37` (`verify_kabir_v06_full_suite.py`) and `TEST-38` (`verify_kabir_v06_showcase_level.py`) passed 100% with 0 errors.

---

### 49. Task 49: "Pehchan & Talashi" Colonial Interrogation System & Persian Wheel Labor [COMPLETED]
- **Status:** **100% COMPLETE & VALIDATED IN-ENGINE (TEST-39 PASSED, 5/5 SUBTESTS, 0 ERRORS)**
- **Implemented Components:**
  - **APersianWheelActor Flume Labor & Manual Reparation:**
    - Interactive Persian wheel (`Rural_Persian_Wheel_Rahat_Canal`) connected to `Cluster_UBDC_CanalBasti`.
    - Pushing the timber draught beam clears irrigation flumes to Kumhar Rahim's potter pits, granting `+35` community trust bonus, elevating cluster stance from Compromised to Neutral, and unbolting deorhi barricades (`Door_CanalBypass_Gate`).
  - **Pehchan & Talashi Sentry Interrogation State Machine:**
    - Sentry initiates `ChallengerHalt` under Section 144 martial curfew ("Thahar! Kaun hai wahan?").
    - Frisk inspection transitions to `SatchelSearch` (2.5s examination).
    - If satchel contains 0 contraband: Sentry issues `CleanPass` and returns to unaware patrol.
    - If satchel contains banned pamphlets: Sentry escalates to `Alerted`, sounds whistle, and registers `Incident_ContrabandSeizedByCurfew` with -30 trust penalty.
    - Community Vouch Protection: If local cluster is `Trusted` and a civilian NPC is nearby, civilian delivers protective vouch bark ("Daroga sahib, he is with us!"), defusing search into `CleanPass`.
    - Interrogation Evasion Flight: If Kabir flees outside confrontation radius during halt/search, sentry triggers immediate pursuit alarm.
  - **Automated Verification:** `TEST-39` (`verify_pehchan_talashi.py`) passed all 5/5 subtests with 100% QA certification. Documented in `Tests/TASK_38_PEHCHAN_TALASHI_VERIFICATION.json`.
