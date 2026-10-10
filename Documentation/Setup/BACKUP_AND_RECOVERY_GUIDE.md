# PROJECT REVOLUTION — Backup & Disaster Recovery Guide

**Document Version:** 1.0.0  
**Classification:** Development Safety & Infrastructure  
**Author:** Senior Technical Director  

---

## 1. Backup Strategy Overview

Project REVOLUTION utilizes a three-tier safety and backup strategy to ensure zero data loss across years of development:

1. **Tier 1: Local Source Control (Git + Git LFS)**
   - Tracks all source code, configurations, technical documentation, scripts, and production assets.
   - Every commit represents an immutable point-in-time state.
2. **Tier 2: Automated Snapshot Archives (`Tools/create_snapshot_backup.ps1`)**
   - Lightweight zipped snapshots created before major milestones, engine upgrades, or risky refactors.
   - Excludes heavy transient directories (`Intermediate/`, `Saved/`, `DerivedDataCache/`, `Binaries/`).
   - Stored in `C:\Users\npal7\PROJECT\REVOLUTION\Backups/`.
3. **Tier 3: External / Secondary Drive Cold Storage (Recommended User Step)**
   - Periodically copying `Backups/` and the project repository to an external USB NVMe SSD or offline backup drive.

---

## 2. Performing a Project Snapshot Backup

Run the automated script from PowerShell:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File "C:\Users\npal7\PROJECT\REVOLUTION\Tools\create_snapshot_backup.ps1" -Label "BeforeEngineUpgrade"
```

The script will:
1. Stage all critical files (`Source/`, `Config/`, `Documentation/`, `Design/`, `Scripts/`, `Tools/`, `SourceControl/`, and `.uproject`).
2. Filter out all volatile cache files.
3. Generate a compressed zip named `REVOLUTION_Snapshot_YYYYMMDD_HHMMSS_<Label>.zip` in `Backups/`.
4. Report output file size and verification status.

---

## 3. Disaster Recovery Procedures

### Scenario A: Corrupted Intermediate or Cache Files
If the Unreal Editor fails to launch, crashes during startup, or exhibits strange compilation errors:
1. Close Unreal Editor and Visual Studio.
2. Delete the following generated folders inside `Project/`:
   - `Project/Intermediate/`
   - `Project/DerivedDataCache/`
   - `Project/.vs/`
3. Right-click `Project/REVOLUTION.uproject` and select **Generate Visual Studio project files**.
4. Rebuild the project in Visual Studio.
5. Launch the editor. The DDC cache will cleanly regenerate.

### Scenario B: Accidental File Deletion or Broken C++ Code
1. Use Git to inspect the delta:
   ```bash
   git status
   git diff
   ```
2. Revert uncommitted changes:
   ```bash
   git checkout -- <file-path>
   ```
3. Or restore from the latest snapshot archive in `Backups/` by extracting it to a temporary staging folder.

### Scenario C: Complete System Reinstall or Disk Failure
1. Reinstall Visual Studio 2022 and Unreal Engine 5 according to [`Documentation/Setup/SOFTWARE_INSTALLATION_GUIDE.md`](file:///C:/Users/npal7/PROJECT/REVOLUTION/Documentation/Setup/SOFTWARE_INSTALLATION_GUIDE.md).
2. Restore the project from external backup or Git clone.
3. Run `git lfs pull` to retrieve all binary assets.
4. Regenerate project files and build.
