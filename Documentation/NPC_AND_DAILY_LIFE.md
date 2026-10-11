# PROJECT REVOLUTION — NPCs, Social Strata & Living World Systems

**Target Engine:** Unreal Engine 5 (AI State Trees, Mass Entity Crowd Baseline)  
**Setting:** Kot Gurdarshan, Central Punjab (1919 – 1929)  
**Design Philosophy:** Grounded Living World Simulation (Scalable for Small Team & 16 GB RAM)  
**Author:** Lead Systems Designer & Narrative Designer  
**Date:** October 10, 2026  

---

## 1. Social Strata & Competing Perspectives

Kot Gurdarshan is not a monolithic cartoon. Indian society under the Raj was intensely complex, divided by economic interests, risk tolerance, caste, and ideology. The town's residents reflect six distinct worldviews:

```mermaid
flowchart TD
    subgraph Perspectives["Societal Spectrum in Kot Gurdarshan"]
        L["1. Imperial Loyalists & Titled Landlords\n(Khan Bahadurs, Rai Bahadurs, military contractors)\n• Prioritize status, British pensions, imperial trade"]
        M["2. Prudent Moderates & Merchants\n(Master Ramlal, grain traders, clerks)\n• Fear martial law; prioritize family feeding and business survival"]
        R["3. Non-Violent Reformers & Satyagrahis\n(Congress volunteers, lawyers, khadi spinners)\n• Boycott British cloth, hold peaceful prayer rallies, court arrest"]
        Y["4. Radical Youth & Revolutionary Underground\n(Students, railway mechanics like Devraj, secret press)\n• Demand Purna Swaraj (Total Independence); operate underground"]
        C["5. Subordinate Indian Colonial Police\n(Constables, Kotwal Mir Afzal)\n• Torn between municipal paychecks and the shame of striking neighbors"]
        B["6. British Imperial Hierarchy\n(Officers, railway overseers, civil magistrates)\n• Enforce imperial sovereignty; view Indian self-rule with racial contempt"]
    end
```

---

## 2. Diurnal Cycles & NPC Schedules

In an authentic living world, characters do not stand idle waiting for player interaction. The town shifts across five realistic daily phases:

```mermaid
timeline
    title Daily Life Schedule in Kot Gurdarshan
    04:30 - 07:00 : Dawn (Brahma Muhurta) : Temple bells, Azaan, sweeping courtyards, fetching well water, milk delivery
    07:00 - 13:00 : Morning Commercial Rush : School starts, bazaar shutters open, grain weighing at Mandi, railway departures
    13:00 - 16:00 : Midday Afternoon Slump : Blinding heat, shopkeepers nap on charpais, silent alleys, dogs in shade
    16:00 - 19:30 : Evening Resurgence : School releases, wrestling in akhara, frying samosas, lighting kerosene lamps
    19:30 - 04:30 : Night & Curfew : Police boots on brick, chowkidar calls, locked gates, secret rooftop couriers
```

### Phase Details:
1. **Dawn (4:30 AM – 7:00 AM):** 
   - Low mist. Sound of sweeping broom bristles on brick. Earthenware water pots clinking at the mohalla well. Kabir's mother Parvati lighting the clay stove (*chulha*). Smoke rising straight into cold morning air.
2. **Morning Rush (7:00 AM – 1:00 PM):**
   - The street wakes. Wooden shutters clatter up. Kabir walks to school with his brass tiffin box. Bullock carts laden with golden wheat enter from the canal road. Tongas clatter toward the railway station.
3. **Midday Slump (1:00 PM – 4:00 PM):**
   - 42°C summer heat. Streets empty. Cotton curtains (*chicks*) lowered across shopfronts. Crows caw lazily from parapets. Ideal window for covert traversal when street witnesses are minimal.
4. **Evening Resurgence (4:00 PM – 7:30 PM):**
   - The bazaar hums with life. Halwai frying sizzling sweet jalebis. Young men training in the mud wrestling pit (*akhara*). Elders gathered at the chopal smoking hookahs and discussing Lahore newspapers.
5. **Night & Curfew (7:30 PM – 4:30 AM):**
   - In 1919 (Act I), the curfew siren sounds from the clock tower. Heavy wooden mohalla gates are bolted shut. British mounted patrols and Indian constables with brass-tipped lathis march through empty streets. Lanterns in civilian homes are extinguished. Underground couriers operate across the dark rooftops.

---

## 3. Scalable Technical Architecture for NPC Simulation (16 GB RAM Budget)

To prevent GPU/CPU bottlenecking on our Intel i5-10200H (4 cores) and 16 GB RAM, NPC simulation is stratified into a **Three-Tier Density Architecture**:

```mermaid
flowchart TD
    T1["Tier 1: High-Fidelity Story & Companion NPCs (Count: 5 - 12)\n• Full Unreal Engine State Tree AI\n• Contextual voice dialogue & facial blendshapes\n• Persistent memory of player actions\n• (Kabir's family, close friends, key police antagonists)"]
    T2["Tier 2: Ambient Interactive Citizens (Count: 20 - 35)\n• Lightweight behavioral state machines (Work, Eat, Converse, Flee)\n• Proximity-triggered greeting bark dialogue\n• React to curfew sirens, gunfire, and player sprint collisions"]
    T3["Tier 3: Distant Background Crowd & Audio Illusion (Count: 40 - 60)\n• Low-poly instanced static meshes with simple vertex animation\n• Spline-based path following along bazaar lanes\n• Rich 3D binaural spatialized audio creates the sensation of hundreds of residents"]

    T1 --> T2 --> T3
```

---

## 4. Implemented Historical Archetypes (`ACivilianNPCActor`)

In Phase 4, five foundational Punjabi characters were implemented in C++ (`ACivilianNPCActor`) and placed into `L_Validation_Gym.umap`:

| Archetype Name | Historical Profession & Role | Map Location | In-Engine Accessory | Primary Lore & Perspective |
| :--- | :--- | :--- | :--- | :--- |
| **Ram Lubhaya** | Master Tailor / Kabir's Father | Zone A Veranda $(200, 480, 88)$ | `SM_Prop_SewingMachine_Singer` | Traumatized by the loss of his brother in the Great War; urges caution while resisting imperial taxation. |
| **Ghasita Bhishti** | Traditional Water-Carrier | Zone C Well Square $(-80, 1320, 88)$ | `SM_Prop_Bhishti_Mashk` | Generational Muslim water-carrier; embodies the shared community solidarity of pre-partition Punjab. |
| **Hira Halwai** | Chai & Jalebi Stall Owner | Zone D Grand Bazaar $(-200, 1680, 88)$ | `SM_Prop_ClayChaiCup_Kulhad` | Outspoken bazaar merchant whose samovar is the center of local political debate and police warnings. |
| **Lala Karam Chand** | Textile Merchant | Zone D Mandi Street $(200, 1980, 88)$ | `SM_Prop_ClothRolls_Manchester` | Torn between unsold British Manchester cotton inventory and the rising moral tide of Swadeshi boycott. |
| **Pandit Kashi Ram** | Vernacular Middle School Headmaster | District C Schoolyard $(1350, 1420, 88)$ | `SM_School_Blackboard_Easel` | Scholar who teaches that critical inquiry and universal literacy are the ultimate weapons of independence. |

Each character features:
- **Proximity Awareness:** Smoothly rotates toward Kabir when he walks within $2.8\text{ meters}$.
- **Ambient Historical Barks:** Spoken/subtitled lines in authentic Punjab English with local cultural terms (*Hartal*, *Mashk*, *Puttar*, *Chai*, *Manchester*, *Rowlatt Act*).
- **Direct Interaction:** Interacting with 'E' brings up multi-line dialogues and records historical discoveries in Kabir's Satchel Journal.

