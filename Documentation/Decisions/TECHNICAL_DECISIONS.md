# PROJECT REVOLUTION — Technical Architecture Decision Records (ADR)

**Lead:** Senior Technical Director  
**Date:** October 10, 2026  
**Status:** Approved Baseline  

---

## ADR-001: Local Drive Isolation (Decoupling from OneDrive)
- **Status:** **Accepted**
- **Context:** The active user workspace is located in `OneDrive\PROJECT\project1`. Unreal Engine projects generate hundreds of thousands of transient files during C++ compilation, DDC shader caching, and asset cooks.
- **Decision:** Place Project REVOLUTION strictly in `C:\Users\npal7\PROJECT\REVOLUTION` outside OneDrive.
- **Consequences:** Eliminates file-lock contention during compilation, stops runaway cloud bandwidth usage, and ensures peak NVMe SSD throughput.

---

## ADR-002: Rendering Mode — Lumen Software Ray Tracing
- **Status:** **Accepted**
- **Context:** The development GPU is an NVIDIA GeForce GTX 1650 (4 GB VRAM), which lacks hardware ray tracing (RT) cores.
- **Decision:** Enforce Lumen Software Ray Tracing using Mesh Distance Fields and Global Distance Fields. Disable Hardware Ray Tracing across all engine configurations.
- **Consequences:** Stable real-time global illumination without device-loss GPU crashes (`DXGI_ERROR_DEVICE_REMOVED`), fitting within the 4 GB VRAM budget.

---

## ADR-003: Compiler Parallelism Cap (`MaxParallelActions: 4`)
- **Status:** **Accepted**
- **Context:** The CPU is an Intel Core i5-10200H (4 Cores / 8 Threads) with 16 GB of system RAM. Unconstrained parallel compilation in MSVC spawns 8 or more `cl.exe` / `link.exe` processes, which consume 12–16 GB RAM and force the OS to page to disk.
- **Decision:** Lock `MaxParallelActions` to 4 in `%APPDATA%\Unreal Engine\UnrealBuildTool\BuildConfiguration.xml`.
- **Consequences:** Smooth background compilation, zero RAM starvation, and an unhindered operating system.

---

## ADR-004: Version Control Architecture (Local Git + Git LFS)
- **Status:** **Accepted**
- **Context:** Large binary assets (`.uasset`, `.umap`, `.blend`, `.fbx`, `.png`) would bloat Git repository size if committed as text deltas.
- **Decision:** Integrate Git LFS for binary formats with an official Unreal `.gitignore` and `.gitattributes`. Maintain repository in local-only mode until a private cloud remote is authorized.
- **Consequences:** Lean repository history, fast checkout times, and full protection of source assets.

---

## ADR-005: Staged Subsystem Introduction
- **Status:** **Accepted**
- **Context:** Attempting to build a full open world before verifying basic character locomotion, C++ compilation, and packaging leads to technical debt.
- **Decision:** Stage development from Milestone 0 (Environment) $\rightarrow$ Milestone 1 (Playable Gym) $\rightarrow$ Milestone 2 (Locomotion/Input) $\rightarrow$ Milestone 3 (World Partitioning).
- **Consequences:** Verifiable, small increments where every component is tested and proven before building the next layer.
