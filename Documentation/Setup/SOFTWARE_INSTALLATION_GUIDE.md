# PROJECT REVOLUTION — Software Installation & Configuration Guide

**Date:** October 10, 2026  
**Auditor:** Senior Technical Director  
**Target Environment:** Windows 11 64-bit | Intel i5-10200H | 16 GB RAM | GTX 1650 (4 GB VRAM) | 151 GB Free NVMe  

---

## 1. Status of Environment Components

| Software Component | Target Version | Current Status | Action Performed / Required |
| :--- | :--- | :--- | :--- |
| **Epic Games Launcher** | Latest | **INSTALLED** | Verified at `C:\Program Files\Epic Games\Launcher`. |
| **Unreal Engine 5** | UE 5.4.4 LTS (or 5.5.x) | **MISSING** | **Requires User Approval & Action (Step 1 Below)**. |
| **Visual Studio 2022** | VS 2022 v17.8+ | **MISSING** | **Requires User Approval & Action (Step 2 Below)**. |
| **MSVC Compiler Toolset** | v143 (14.38.33130) | **MISSING** | Included in VS 2022 installation options. |
| **Windows SDK** | 10.0.22621.0 | **MISSING** | Included in VS 2022 installation options. |
| **Git** | 2.54.0 | **INSTALLED & VERIFIED** | Operational at `C:\Program Files\Git\cmd\git.exe`. |
| **Git LFS** | 3.7.1 | **INSTALLED & VERIFIED** | Operational at `C:\Program Files\Git\cmd\git-lfs.exe`. |
| **Blender 3D** | 5.2.1 LTS | **INSTALLED & CONFIGURED** | PATH configured; wrapper created at `Tools/blender.cmd`. Verified. |
| **Python** | 3.11.9 | **INSTALLED & VERIFIED** | Operational via `py.exe`. |
| **Disk Space Monitor** | Custom | **INSTALLED & VERIFIED** | Operational at `Tools/check_disk_space.ps1`. |
| **Snapshot Backup System** | Custom | **INSTALLED & VERIFIED** | Operational at `Tools/create_snapshot_backup.ps1`. |
| **UBT Compiler Tuning** | Custom XML | **CONFIGURED & VERIFIED** | Active at `%APPDATA%\Unreal Engine\UnrealBuildTool\BuildConfiguration.xml`. |

---

## 2. Step 1: Install Visual Studio 2022 Community (With C++ Workload)

### Official Download Link:
[https://visualstudio.microsoft.com/downloads/](https://visualstudio.microsoft.com/downloads/) (Select **Visual Studio Community 2022**)

### Disk Space Impact:
- Download size: ~2.5 – 3.5 GB
- Installed footprint: ~14 – 18 GB on Drive C:

### Step-by-Step Installation Instructions:
1. Download and run `VisualStudioSetup.exe`.
2. When the Visual Studio Installer opens, check the following **Workloads**:
   - `[X] Game development with C++`
   - `[X] Desktop development with C++`
3. In the right-hand panel (**Installation details**), expand **Game development with C++** and ensure these are checked:
   - `[X] MSVC v143 - VS 2022 C++ x64/x86 build tools (v14.38-17.8)` *(or latest stable v143)*
   - `[X] Windows 11 SDK (10.0.22621.0)` *(or 10.0.22000.0)*
   - `[X] Unreal Engine IDE support`
   - `[X] C++ profiling tools`
4. Click **Install**.
5. Once installation finishes, restart your PC if prompted.

---

## 3. Step 2: Install Unreal Engine 5.4.4 via Epic Games Launcher

### Prerequisite:
Epic Games Launcher is already installed on your PC at `C:\Program Files\Epic Games\Launcher`.

### Disk Space Impact:
- Default Full Install: ~65 GB download / ~100 GB installed (**Too large for our 151 GB drive!**)
- **Trimmed Install (Recommended):** **~30 GB download / ~45 GB installed**

### Step-by-Step Installation Instructions:
1. Open **Epic Games Launcher** from your Windows Start Menu.
2. Select the **Unreal Engine** tab on the left sidebar.
3. Click the **Library** tab at the top.
4. Next to **Engine Versions**, click the golden **`+`** icon to add an engine slot.
5. In the drop-down selector, choose **5.4.4** (or **5.5.x** if 5.4.4 is not listed).
6. Click **Install**.
7. **CRITICAL OPTIMIZATION STEP:** On the install dialog prompt, click **Options**:
   - Keep checked: `Core Components`, `Starter Content`, `Engine Source`.
   - **UNCHECK:** `Android` (saves ~15 GB)
   - **UNCHECK:** `iOS` (saves ~12 GB)
   - **UNCHECK:** `Linux` (saves ~10 GB)
   - **UNCHECK:** `Editor symbols for debugging` (saves ~35 GB; optional, can be added later if low-level engine crash disassembly is needed)
8. Confirm installation directory: `C:\Program Files\Epic Games\UE_5.4`.
9. Click **Apply / Install** to begin the download.

---

## 4. Post-Installation Verification Check

After completing the installations, running `Tools/check_disk_space.ps1` will verify your remaining storage, and Phase 5/6 will automatically verify the compiler, SDK, and engine registrations.
