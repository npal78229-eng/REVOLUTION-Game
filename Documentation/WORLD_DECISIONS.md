# PROJECT REVOLUTION — World Decisions & Architecture Records

**Author:** Creative Director & Senior Technical Director  
**Project Owner:** Creator (Final Authority on All Decisions)  
**Date Updated:** October 10, 2026  
**Status:** Approved by Project Owner  

---

## 1. Approved Creative & World Decisions

| Decision ID | Description | Approved Decision | Rationale & Owner Directive |
| :--- | :--- | :--- | :--- |
| **DEC-001** | Physical Workspace Isolation | `C:\Users\npal7\PROJECT\REVOLUTION` (Outside OneDrive) | Eliminates cloud sync file locking and compiler corruption. |
| **DEC-002** | Target Rendering Pipeline | Unreal Engine 5 with **Lumen Software Ray Tracing** | Prevents device loss crashes on GTX 1650 (4 GB VRAM) while enabling rich real-time GI. |
| **DEC-003** | Compilation Hardware Throttling | `MaxParallelActions: 4` in `BuildConfiguration.xml` | Prevents MSVC linker from exceeding 16 GB system RAM during parallel builds. |
| **DEC-004** | Source Control Baseline | Local Git + Git LFS pointer tracking | Manages binary `.uasset`, `.blend`, `.fbx` assets cleanly without repo bloat. |
| **DEC-005** | Production Staging Model | Staged Prototype $\rightarrow$ Playable Gym $\rightarrow$ Expanding Districts | Avoids building an enormous unvalidated world prematurely. |
| **DEC-006** | **Historical Setting & Region** | **Proposal 1: Central Punjab Plains (1919 – 1929)** | **Approved by Creator.** Crucible of India's freedom struggle; Jallianwala Bagh martial law through the rise of HSRA; ideal rooftop traversal and emotional cohesion. |
| **DEC-007** | **Setting Town Identity** | **Kot Gurdarshan (Fictional Town)** | **Approved by Creator.** Fictional town along the Lahore–Amritsar railway line preserves total narrative freedom while adhering strictly to authentic historical realities. |
| **DEC-008** | **Visual Direction Target** | **Red Dead Redemption 2 (RDR2) Aesthetic** | **Mandated by Creator.** Naturalistic lighting, volumetric atmosphere, heavy tactile material wear, dynamic weather (dust/mud/monsoon), cinematic framing, living NPC world. |
| **DEC-009** | **Protagonist Foundation** | **Kabir (Age 12 in 1919 $\rightarrow$ Age 21 in 1928)** | Family of master tailors / dyers; older WWI veteran uncle; multifaith Punjabi community; organic transformation through lived experience. |

---

## 2. Technical Strategy for RDR2 Visual Target on GTX 1650 (4 GB VRAM)

Achieving an RDR2-level grounded, tactile aesthetic on our hardware requires deliberate technical art direction:
1. **Material Realism over Polygon Sprawl:** RDR2's world feels real because of weathered surface details (chipped lime plaster, salt efflorescence on baked brick, mud splatters on carriage wheels, fabric fiber fraying). We will utilize **Detail Normal Maps**, **Macro-Variation Masks**, and **Channel-Packed ORM textures** rather than raw geometric excess.
2. **Volumetric Lighting & Atmosphere:** RDR2's iconic look relies heavily on sun shafts (*crepuscular rays*), morning dust, and smoke. We will use Unreal Engine's **Volumetric Fog with local exponential height fog volumes** and particle dust motes, tuned to medium grid resolution to maintain $\ge 30\text{ FPS}$.
3. **Dynamic Weather & Soil Interaction:** RDR2's mud and rain shaders will be achieved using vertex-painted puddle layers and material parameter collections (MPC) that drive wetness roughness values across the world during rain events.
4. **Cinematic Framing & Tone:** A naturalistic, non-stylized Academy-ratio depth-of-field, subtle lens dirt, and filmic ACES tonemapping.
