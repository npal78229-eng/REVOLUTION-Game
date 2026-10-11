# PROJECT REVOLUTION — Environment Asset Inventory

**Classification:** Technical Asset Registry  
**Project:** REVOLUTION (Unreal Engine 5.5, MSVC 14.44 / C++20)  
**Last Updated:** October 11, 2026  
**Status:** All Listed Assets Verified on Disk and In-Engine

---

## 1. Modular Architectural Meshes (`Content/Environment/Mohalla/Meshes/`)

| Asset Name | Polycount | Collision Mode | Assigned Materials | Status |
| :--- | :--- | :--- | :--- | :--- |
| `SM_Wall_Brick_4x4m_A` | ~48 tris | `CTF_USE_COMPLEX_AS_SIMPLE` | `M_LahoriBrick_PBR`, `M_LimePlaster_PBR` | In-Use (Haveli walls, alleyways, bazaar backings) |
| `SM_Wall_Brick_Doorway_4x4m` | ~84 tris | `CTF_USE_COMPLEX_AS_SIMPLE` | `M_LahoriBrick_PBR` | In-Use (Haveli entrance, shopfront openings) |
| `SM_Wall_Brick_Window_4x4m` | ~96 tris | `CTF_USE_COMPLEX_AS_SIMPLE` | `M_LahoriBrick_PBR` | In-Use (Haveli living rooms, alley facades) |
| `SM_Floor_Ceiling_Slab_4x4m` | ~12 tris | `CTF_USE_COMPLEX_AS_SIMPLE` | `M_LahoriBrick_PBR`, `M_LimePlaster_PBR` | In-Use (Rooftop terraces, 1F floor slabs) |
| `SM_Roof_Parapet_4m_A` | ~24 tris | `CTF_USE_COMPLEX_AS_SIMPLE` | `M_LahoriBrick_PBR` | In-Use (1.1m vaultable rooftop boundaries) |
| `SM_Roof_Stairs_Masonry_01` | ~96 tris | `CTF_USE_COMPLEX_AS_SIMPLE` | `M_LahoriBrick_PBR` | In-Use (Courtyard staircase ascending 4m) |
| `SM_Door_Deorhi_Teak_01` | ~120 tris | `CTF_USE_COMPLEX_AS_SIMPLE` | `M_AgedTeak_PBR` | In-Use (Haveli gateway double doors) |
| `SM_Shop_Shutter_Foldable` | ~88 tris | `CTF_USE_COMPLEX_AS_SIMPLE` | `M_AgedTeak_PBR`, `M_WroughtIron_PBR` | In-Use (Closed bazaar shopfronts, curfew shutters) |
| `SM_Balcony_Jharokha_Wood_A` | ~340 tris | `CTF_USE_COMPLEX_AS_SIMPLE` | `M_AgedTeak_PBR` | In-Use (Upper-story overhang balconies) |
| `SM_Mohalla_Well_Stone` | ~410 tris | `CTF_USE_COMPLEX_AS_SIMPLE` | `M_LahoriBrick_PBR`, `M_AgedTeak_PBR`, `M_WroughtIron_PBR` | In-Use (Communal well, social center of District A) |
| `SM_Market_Stall_Wood_Awning` | ~168 tris | `CTF_USE_COMPLEX_AS_SIMPLE` | `M_AgedTeak_PBR`, `M_Clay_PBR` | In-Use (Spice stall, Halwai tea stall, cloth stall) |

---

## 2. Historical Dressing & Interactive Props (`Content/Environment/Mohalla/Meshes/`)

| Asset Name | C++ Actor Binding | Material | Physical Purpose | Status |
| :--- | :--- | :--- | :--- | :--- |
| `SM_Prop_Charpai_RopeBed` | `AInspectableProp` | `M_AgedTeak_PBR` | Woven moonj daybed for domestic courtyards and chopal. | In-Use |
| `SM_Prop_HurricaneLantern` | `AInspectableProp` | `M_WroughtIron_PBR` | Dietz No. 2 cold-blast tin lantern used by night watchmen. | In-Use |
| `SM_Prop_GrainSack_Jute_01` | `AInspectableProp` | `M_Clay_PBR` | Requisitioned burlap wheat sacks with British excise stamps. | In-Use |
| `SM_Prop_ClayChaiCup_Kulhad` | `AInspectableProp` | `M_Clay_PBR` | Unglazed terracotta tea cup made by local bazaar Kumhars. | In-Use |
| `SM_Prop_Kite_Spool_Charkhi` | `AInspectableProp` | `M_AgedTeak_PBR` | Polished hardwood kite spool strung with glass-coated line. | In-Use |
| `SM_Prop_SpiceBasket_Woven` | `AInspectableProp` | `M_Clay_PBR` | Cane basket filled with turmeric (*haldi*) and red chili. | In-Use |
| `SM_Prop_ShopSign_Wood` | `AInspectableProp` | `M_AgedTeak_PBR` | Hanging wooden merchant plaque with iron mounting brackets. | In-Use |
| `SM_School_Desk_Bench_Wood` | `AInspectableProp` | `M_AgedTeak_PBR` | Two-seater varnished Sheesham student desk bench with slate groove. | In-Use (Classroom 4B) |
| `SM_School_Blackboard_Easel` | `AInspectableProp` | `M_AgedTeak_PBR`, `M_WroughtIron_PBR` | Large timber-framed slate easel blackboard for teacher instruction. | In-Use (Classroom 4B) |
| `SM_School_Bell_Tower_Iron` | `AInspectableProp` | `M_WroughtIron_PBR`, `M_AgedTeak_PBR` | 4-post wrought iron school bell gantry with suspended brass bell. | In-Use (Schoolyard Center) |
| `SM_Prop_SewingMachine_Singer` | `AInspectableProp` | `M_WroughtIron_PBR`, `M_AgedTeak_PBR` | Authentic 1919 cast-iron Singer treadle sewing machine with foot pedal. | In-Use (Father's Veranda) |

---

## 3. PBR Master Materials (`Content/Environment/Mohalla/Materials/`)

| Material Name | Base Color (sRGB) | Roughness | Metallic | Historic Application |
| :--- | :--- | :--- | :--- | :--- |
| `M_LahoriBrick_PBR` | `(0.55, 0.22, 0.15)` | 0.85 | 0.00 | Porous kiln-baked red alluvial clay bricks, courtyard paving. |
| `M_AgedTeak_PBR` | `(0.25, 0.16, 0.09)` | 0.65 | 0.00 | Dark oiled Sheesham and teak timber, doors, charpais, jharokhas. |
| `M_WroughtIron_PBR` | `(0.12, 0.12, 0.13)` | 0.40 | 0.85 | Blacksmith iron bars, well pulley, lantern frames, door studs. |
| `M_Clay_PBR` | `(0.60, 0.35, 0.20)` | 0.90 | 0.00 | Unglazed terracotta pottery, kulhads, burlap sacks, canvas awning. |

---

## 4. Gameplay & Traversal C++ Actors (`Source/REVOLUTION/`)

| C++ Class | Base Class | Primary Responsibility | Level Instances |
| :--- | :--- | :--- | :--- |
| `ARevolutionCharacter` | `ACharacter` | Kabir player pawn (locomotion, stamina, vaulting, crouching, inspection, audio). | Spawned by GameMode at `PlayerStart` |
| `ARevolutionGameMode` | `AGameModeBase` | Game framework coordinator; manages HUD, props, and mission subsystem. | Configured in `DefaultEngine.ini` |
| `ARevolutionHUD` | `AHUD` | Draws period HUD interface with historical typography and warm gold accents. | Spawned by GameMode |
| `AInspectableProp` | `AActor` | Interactive object with 3D highlight, prompt, and historical lore card. | 22 dynamically spawned + 12 placed |
| `ACurfewPatrolAI` | `ACharacter` | British colonial Chaukidar with lantern and realistic waypoint patrol loop. | 1 active patrol in District A |
| `AMatkaStandActor` | `AActor` | Chilled earthen water vessel providing 100% stamina recovery and sound distraction. | 1 in family courtyard |
| `ACurfewGongActor` | `AActor` | Municipal 35m curfew gong providing sector-wide patrol diversion. | 1 in communal well square |
| `AHidingSpotActor` | `AActor` | Shadow alcoves and grain sack concealment spots. | 2 in alleyway and mandi |
| `ACrawlSpaceActor` | `AActor` | 80cm foundation breach crawlway traversal. | 1 connecting alley to bazaar |
| `ATerracottaHazardActor`| `AActor` | Fragile unbaked pottery hazards that crunch underfoot and alert AI. | 2 in domestic storage corners |

---

## 5. Source Asset Repositories

- **Blender 5.2 Projects:**
  - `Art/Blender/KIT_Punjabi_Mohalla.blend` (Master modular architecture kit)
  - `Art/Blender/Courtyard_Rooftop_Gym_Scene.blend` (Assembled courtyard prototype)
- **FBX Export Directory:**
  - `Art/Exports/` (23 modular FBX files ready for automated headless ingestion)
- **Engine Maps:**
  - `Project/Content/Maps/L_Validation_Gym.umap` (The playable 105-piece vertical slice across 5 zones)
