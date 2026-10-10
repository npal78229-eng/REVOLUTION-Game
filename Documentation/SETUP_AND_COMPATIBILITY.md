# PROJECT REVOLUTION — Setup & Toolchain Compatibility Matrix

**Document Purpose:** Official verification and compatibility baseline for Project REVOLUTION (AAA Open-World Game).  
**Date Checked:** October 10, 2026  
**Status:** Verified against official Epic Games, Microsoft, and Blender documentation.

---

## 1. Selected Engine Target

### Primary Recommendation: **Unreal Engine 5.4.4** (or **Unreal Engine 5.5.x**)
- **Rationale:** 
  - Unreal Engine 5.4 is the mature, battle-tested Long-Term Support baseline with broad Fab / Marketplace plugin compatibility, optimized Nanite rendering, and production-tested World Partition.
  - Unreal Engine 5.5 provides bleeding-edge PCG and Megalights improvements.
  - For Project REVOLUTION on a GTX 1650 (4 GB VRAM) and 16 GB RAM, **UE 5.4.4** provides the highest stability and lowest memory volatility.

---

## 2. Toolchain Compatibility Matrix

| Component | Official Requirement (UE 5.4 / 5.5) | Host Machine Detected | Compatibility Status | Verification Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Operating System** | Windows 10 64-bit (v1909+) or Windows 11 64-bit | Windows 11 Home (Build 26200, 64-bit) | **VERIFIED COMPATIBLE** | Supported natively by UnrealBuildTool and DirectX 12 Agility SDK. |
| **IDE** | Visual Studio 2022 (v17.8 or later recommended) | *Not yet installed* (VS Code present) | **ACTION REQUIRED (PHASE 4)** | Community, Professional, or Build Tools 2022 required for C++ development. |
| **MSVC Compiler Toolset** | **MSVC v143** — Version **14.38.33130** (v14.38-17.8)<br>*(Older: min 14.34; Newer MSVC versions >14.38 require explicit v14.38 component)* | *Not yet installed* | **ACTION REQUIRED (PHASE 4)** | Must install `MSVC v143 - VS 2022 C++ x64/x86 build tools (v14.38-17.8)` via Visual Studio Installer. |
| **Windows SDK** | Minimum: `10.0.19041.0` (UE 5.4)<br>Minimum: `10.0.22000.0` (UE 5.5)<br>Recommended: `10.0.22621.0` | *Not yet installed* | **ACTION REQUIRED (PHASE 4)** | Included via Visual Studio C++ Game Development workload. |
| **GPU & Graphics Driver** | DirectX 12 (SM 6.6+), NVIDIA Driver $\ge$ 526.47 | NVIDIA GeForce GTX 1650 (4 GB VRAM), Driver 592.00 | **VERIFIED COMPATIBLE** | Driver 592.00 exceeds requirements. Note: Software Lumen will be used due to GTX 1650 hardware limits. |
| **Git Version Control** | Git 2.30+ | Git 2.54.0.windows.1 | **VERIFIED COMPATIBLE** | Operational at `C:\Program Files\Git\cmd\git.exe`. |
| **Git Large File Storage** | Git LFS 3.0+ | Git LFS 3.7.1 | **VERIFIED COMPATIBLE** | Operational at `C:\Program Files\Git\cmd\git-lfs.exe`. |
| **3D DCC Tool** | Blender 3.6 LTS, 4.x, or 5.x with FBX 2020 / USD | Blender 5.2 | **VERIFIED COMPATIBLE** | Installed at `C:\Program Files\Blender Foundation\Blender 5.2`. Compatible with FBX and OpenUSD import pipelines. |
| **Scripting Automation** | Python 3.9 – 3.11 | Python 3.11.9 (via `py.exe`) | **VERIFIED COMPATIBLE** | Operational via Windows Python launcher. |
| **Epic Games Launcher** | Latest Launcher release | Installed (`C:\Program Files\Epic Games\Launcher`) | **VERIFIED COMPATIBLE** | Ready to install UE 5.4/5.5 engine binaries. |

---

## 3. Required Visual Studio 2022 Components Detail

To prevent compilation failures and linker crashes when generating or building the Unreal C++ project, the Visual Studio 2022 installation **must** include the following exact workloads and individual components:

### Primary Workload:
- **Game development with C++** (`Microsoft.VisualStudio.Workload.NativeGame`)
- **Desktop development with C++** (`Microsoft.VisualStudio.Workload.NativeDesktop`)

### Critical Individual Components:
1. `MSVC v143 - VS 2022 C++ x64/x86 build tools (v14.38-17.8)` (Exact compiler version expected by UE 5.4 / 5.5).
2. `Windows 11 SDK (10.0.22621.0)` or `Windows 10 SDK (10.0.20348.0)`.
3. `C++ core desktop features`.
4. `Unreal Engine IDE support` (`Microsoft.VisualStudio.Component.VC.UnrealEngine`).
5. `C++ profiling tools` (for performance benchmarking).

---

## 4. Hardware Scalability & Engine Configuration Rules

Given the host hardware baseline (GTX 1650 4 GB VRAM, 16 GB RAM, 4C/8T CPU), the following configuration rules are strictly defined for the engine:

1. **Lumen Global Illumination:**
   - Setting: `Lumen Software Ray Tracing` (Global Distance Fields & Mesh Distance Fields).
   - Prohibited: `Hardware Ray Tracing` (unsupported on GTX 1650).
2. **Nanite Virtualized Geometry:**
   - Enabled for static landscape and architectural meshes.
   - Streaming memory pool: Constrained to prevent VRAM overcommit.
3. **Shadow Filtering:**
   - Cascaded shadow maps or Virtual Shadow Maps with optimized resolution cache (`r.Shadow.Virtual.Cache.MaxPageAge 32`).
4. **Editor Screen Percentage:**
   - Default viewport: `75%` with TSR (Temporal Super Resolution) upscaling.
5. **Compilation Worker Cap (`BuildConfiguration.xml`):**
   - Max parallel actions: `4` (matches physical core count and fits within 16 GB RAM envelope during linking).

---

## 5. Official Source URLs & References

- **Unreal Engine Hardware and Software Specifications:**  
  URL: [https://dev.epicgames.com/documentation/en-us/unreal-engine/hardware-and-software-specifications-for-unreal-engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/hardware-and-software-specifications-for-unreal-engine)  
  *Verified: October 10, 2026*
- **Setting Up Visual Studio for Unreal Engine:**  
  URL: [https://dev.epicgames.com/documentation/en-us/unreal-engine/setting-up-visual-studio-for-unreal-engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/setting-up-visual-studio-for-unreal-engine)  
  *Verified: October 10, 2026*
- **Unreal Engine Git & Source Control Documentation:**  
  URL: [https://dev.epicgames.com/documentation/en-us/unreal-engine/using-source-control-in-unreal-engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-source-control-in-unreal-engine)  
  *Verified: October 10, 2026*
- **Git Large File Storage (LFS) Documentation:**  
  URL: [https://git-lfs.com/](https://git-lfs.com/)  
  *Verified: October 10, 2026*
- **Blender to Unreal Engine Interoperability Documentation:**  
  URL: [https://docs.blender.org/manual/en/latest/addons/import_export/scene_fbx.html](https://docs.blender.org/manual/en/latest/addons/import_export/scene_fbx.html)  
  *Verified: October 10, 2026*
