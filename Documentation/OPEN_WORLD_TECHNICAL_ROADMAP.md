# PROJECT REVOLUTION — Open-World Technical Roadmap & Subsystem Staging

**Author:** Senior Technical Director  
**Scope:** Progressive system introduction, performance risks, and open-world architectural staging  
**Date:** October 10, 2026  

---

## 1. Feature Staging: Prototype vs Full Production

To prevent scope creep and memory exhaustion on the GTX 1650 (4 GB VRAM) / 16 GB RAM hardware baseline, open-world features are staged across progressive development cycles:

| Subsystem | Included in First Prototype? | Deferred to Later Stages? | Rationale & Hardware Justification |
| :--- | :---: | :---: | :--- |
| **Enhanced Input** | **YES** | No | Core foundation for responsive gameplay across Keyboard/Mouse and Gamepad. |
| **Lumen Software Ray Tracing** | **YES** | No | Real-time global illumination with zero reliance on dedicated hardware RT cores. |
| **Nanite Virtualized Geometry** | **YES** | No | Static environment meshes benefit immediately from automatic LOD streaming. |
| **One File Per Actor (OFPA)** | **YES** | No | Essential source control hygiene; eliminates level file merge conflicts. |
| **World Partition (512m Cells)** | **YES** | No | Required to keep memory usage under 12 GB during world editing. |
| **Virtual Shadow Maps (VSM)** | **YES (Optimized)** | No | VSM with cached page ages (`MaxPageAge 32`) balances visual fidelity and VRAM. |
| **Data Layers** | **YES** | No | Segregates landscape, foliage, and actors for targeted editing. |
| **Gameplay Ability System (GAS)** | **YES (Base)** | Extensions | Base attributes (Health, Stamina) set up early to prevent later refactors. |
| **AI Perception & Navigation** | No | **YES** | Initial milestone requires character movement validation before NPC logic. |
| **Motion Matching** | No | **YES** | High memory footprint for motion databases; standard state machines suffice for prototype. |
| **Hierarchical LOD (HLOD)** | No | **YES** | Requires built-out world vistas; premature in a single gym test level. |
| **Full Landscape Deformation** | No | **YES** | Initial test level will use modular geometry before streaming large terrain heightmaps. |
| **Persistent Save/Load System** | No | **YES** | Serialization architecture implemented once core actor data types are stabilized. |

---

## 2. Open-World Subsystem Architecture Deep-Dive

### 2.1 World Partition & One File Per Actor (OFPA)
- **Grid Configuration:** Default 512m streaming cell size.
- **Loading Strategy:** Cells stream in dynamically based on player location. In the editor, only the active authoring region is loaded via the World Partition editor window.
- **Benefits:** Minimizes memory footprint on 16 GB RAM and prevents giant multi-gigabyte `.umap` files in Git LFS.

### 2.2 Data Layers Architecture
The open world is partitioned into four primary layers:
1. `DL_Terrain`: Heightmap, basic landscape materials, rivers.
2. `DL_Architecture`: Static modular structures, roads, ruins.
3. `DL_Foliage`: Trees, bushes, grass scatter (managed via PCG / Procedural Content Generation).
4. `DL_Encounters`: Spawners, enemy AI camps, interactive quest triggers.

Tech artists can work on `DL_Architecture` with `DL_Foliage` completely unloaded, saving ~2 GB of editor RAM.

### 2.3 Nanite & Lumen Performance Budgets
- **Nanite:**
  - Used for opaque static meshes with high triangular density.
  - Excluded from: Two-sided vegetation with complex masking (leaves use standard LOD cards).
- **Lumen:**
  - Global illumination via Mesh Distance Fields (MDF).
  - Software reflections with screen-space fallback.
  - Light update rate throttled in editor to conserve GPU cycles.

### 2.4 Streaming Budgets & Profiling
- **Texture Streaming Pool:** Capped at $1800\text{ MB}$.
- **Mesh Streaming Pool:** Capped at $512\text{ MB}$.
- **Target Frame Time:** $\le 33.3\text{ ms}$ (30 FPS minimum) in editor at 75% resolution.
