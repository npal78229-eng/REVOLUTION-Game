# PROJECT REVOLUTION — Source Control Setup & Operations Guide

**System:** Git + Git LFS (Large File Storage)  
**Host Git Version:** 2.54.0.windows.1 | Git LFS: 3.7.1  
**Project Path:** `C:\Users\npal7\PROJECT\REVOLUTION`  
**Classification:** Development Safety & Architecture  

---

## 1. Source Control Architecture

Unreal Engine projects consist of two fundamentally different file types:
1. **Text Files:** C++ source (`.cpp`, `.h`), build rules (`.Build.cs`, `.Target.cs`), configuration files (`.ini`), and documentation (`.md`, `.csv`). These are managed by native Git delta compression.
2. **Binary Assets:** Unreal asset files (`.uasset`, `.umap`), 3D models (`.blend`, `.fbx`), textures (`.png`, `.tga`), and audio (`.wav`). These CANNOT be merged and will bloat git history if stored in delta trees. These are managed exclusively via **Git LFS** pointers.

---

## 2. Source Control Safety Rules

1. **Never Commit Generated Folders:**
   - `Intermediate/`, `Saved/`, `DerivedDataCache/`, `Binaries/`, `.vs/`, `Build/`, `Backups/`.
   - The root `.gitignore` enforces this rule automatically.
2. **Always Lock Binary Assets in Multi-User Environments:**
   - Because `.uasset` files cannot be merged via text diffs, when collaborating with multiple developers, use `git lfs lock <asset-path>`.
3. **Never Push to Remote Repositories Without Authorization:**
   - The repository operates in local-only mode by default. No remote origin is configured until explicitly directed by the Project Owner.
4. **Credential Protection:**
   - Never stage API keys, credentials, license keys, or private tokens.

---

## 3. Daily Developer Commands

### Check Working Tree Status:
```bash
git status
```

### Stage New Changes:
```bash
git add <path-to-file>
```

### Commit Structured Changes:
```bash
git commit -m "feat(gameplay): implement stamina consumption for sprint"
```

### Verify LFS Tracked Files:
```bash
git lfs ls-files
```
