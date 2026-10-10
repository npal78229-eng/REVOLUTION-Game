# PROJECT REVOLUTION — World Map Layout & Spatial Design

**World Setting:** Kot Gurdarshan, Central Punjab (1919 – 1929)  
**Total Region Footprint:** $\approx 1.5\text{ km} \times 1.2\text{ km}$ ($1.8\text{ km}^2$ total open-world space)  
**Initial Prototype Footprint:** $100\text{ m} \times 100\text{ m}$ (District A: Family Mohalla & Courtyard)  
**World Streaming Architecture:** Unreal Engine 5 World Partition (512m Grid Cells)  
**Author:** Lead World Designer & Level Designer  
**Date:** October 10, 2026  

---

## 1. High-Level Spatial Layout & Geographic Flow

```mermaid
flowchart TD
    subgraph West["West Enclave (British Imperial Power)"]
        CivilLines["District F: Civil Lines\n(Bungalows, District Court, Club)"]
        Cantonment["Military Cantonment\n(Infantry Barracks, Drill Field)"]
    end

    subgraph Barrier["The Iron & Stone Dividing Line"]
        Tracks["District E: North Western Railway Tracks & Freight Yard"]
        Overpass["The Red-Brick Railway Overpass & Checkpoint"]
    end

    subgraph East["East Enclave (Walled Native Town)"]
        Mohalla["District A: Mohalla Darzian\n(Family Courtyard & Rooftops)"]
        Bazaar["District B: Grand Bazaar & Grain Mandi"]
        School["District C: Vernacular Middle School"]
    end

    subgraph NorthEast["North-East Countryside & Margins"]
        Canal["District D: Canal Colony & Wheat/Mustard Fields"]
        Kilns["The Brick Kilns & Lock Gates"]
        Ghats["District G: Old Caravanserai & Riverside Margins"]
    end

    CivilLines <--> Overpass
    Cantonment <--> Overpass
    Overpass <--> Tracks
    Tracks <--> Bazaar
    Mohalla <--> Bazaar
    Bazaar <--> School
    Mohalla <--> Canal
    Canal <--> Kilns
    Canal <--> Ghats
```

---

## 2. Landmark Visual Beacons & Lines of Sight

In our environmental design philosophy, open-world navigation relies on visible physical landmarks rather than cluttered mini-map icons. Kot Gurdarshan features five primary visual beacons visible across rooftops and avenues:

| Beacon ID | Landmark Name | Height | District Location | Visual & Narrative Purpose |
| :--- | :--- | :---: | :--- | :--- |
| **LND-01** | **The Railway Station Clock Tower** | $28\text{ m}$ | District E (Junction) | Cast-iron red-brick Victorian tower; chiming bell announces curfew and train arrivals. Visible across all native rooftops. |
| **LND-02** | **The Grand Peepal & Temple Spire** | $22\text{ m}$ | District A (Old Town) | Ancient sprawling sacred tree beside a white lime-shikhara temple; anchor for Kabir's home neighborhood. |
| **LND-03** | **St. Andrew's Garrison Church Spire** | $32\text{ m}$ | District F (Cantonment) | Gothic sandstone spire towering over the British enclave; signals the forbidden European zone. |
| **LND-04** | **Imperial Brick Kiln Chimney** | $35\text{ m}$ | District D (Countryside) | Solitary brick smokestack belching black coal plumes into orange sunset skies; orienting beacon in the countryside. |
| **LND-05** | **The Ruined Caravanserai Mughal Gateway** | $18\text{ m}$ | District G (Outer Margins) | Massive crumbling 17th-century brick archway swallowed by banyan roots; marks the clandestine rebel printer refuge. |

---

## 3. Scale, Distance & Travel Times (12-Year-Old Protagonist)

Movement speeds calibrated for a 12-year-old boy:
- Normal Walking Pace: $3.8\text{ km/h}$ ($\approx 1.05\text{ m/s}$)
- Running / Rooftop Dash: $10.5\text{ km/h}$ ($\approx 2.9\text{ m/s}$)

```mermaid
flowchart LR
    Home["Home (Mohalla)"] -- "180 m\n(1.7 min walk)" --> Bazaar["Grand Bazaar"]
    Bazaar -- "220 m\n(2.1 min walk)" --> School["Vernacular School"]
    Bazaar -- "250 m\n(2.4 min walk)" --> Station["Railway Station"]
    Station -- "320 m\n(3.0 min walk)" --> Courts["District Court (Civil Lines)"]
    Home -- "400 m\n(3.8 min walk)" --> Canal["Canal Lock #7"]
    Home -- "1150 m\n(11.0 min walk)" --> Cantonment["British Garrison Barracks"]
```

---

## 4. Security Tiers & Environmental Access Zones

```mermaid
flowchart TD
    Zone1["Zone 1: Safe Domestic Zones\n(Family Courtyard, Rooftops, Temple Chopal)\n• Unrestricted access\n• Warm ambient acoustics\n• No police patrols"]
    Zone2["Zone 2: Public Commercial Zones\n(Grand Bazaar, Grain Mandi, School Ground)\n• Normal civilian access\n• Occasional Indian constables with lathis\n• Eavesdropping opportunities"]
    Zone3["Zone 3: Tense Monitored Zones\n(Railway Platforms, Goods Yard, Canal Road)\n• Armed police presence\n• Identity checks after dusk\n• Require stealth, tickets, or errands"]
    Zone4["Zone 4: High-Security Restricted Zones\n(Civil Lines at Night, Kotwali Lockup, European Club)\n• Prohibited for Indian civilians without official passes\n• Immediate trespass alert / arrest\n• Stealth infiltration only"]

    Zone1 --> Zone2 --> Zone3 --> Zone4
```

---

## 5. Staged Worldbuilding Rollout Plan

To ensure rigorous quality and prevent unvalidated asset bloat, the world will expand across four controlled stages:

```mermaid
flowchart TD
    S1["Stage 1: The Initial Prototype Gym (Current Target)\n• Footprint: 100m x 100m\n• Family Courtyard + 3 Adjoining Rooftops + Narrow Mohalla Alley\n• Validates: Grounded lighting, brick materials, rooftop traversal, domestic audio"]
    S2["Stage 2: The Core Walled Town\n• Footprint: 400m x 400m\n• Adds: Grand Bazaar, Grain Mandi, Vernacular School, Akhara"]
    S3["Stage 3: The Industrial & Rural Fringe\n• Footprint: 800m x 600m\n• Adds: Railway Station, Freight Yards, Upper Bari Doab Canal, Mustard Fields"]
    S4["Stage 4: The Full Open World\n• Footprint: 1.5km x 1.2km\n• Adds: British Civil Lines, District Court, Cantonment, Outer Ruined Serai"]

    S1 --> S2 --> S3 --> S4
```
