# PROJECT REVOLUTION

**AAA Open-World Game Development Foundation**  
**Engine:** Unreal Engine 5 (Target: UE 5.4.x / 5.5.x)  
**Primary Language:** C++ & Gameplay Framework Blueprints  
**Content Creation:** Blender 5.2  
**Target Hardware Baseline:** Intel Core i5 (4C/8T), 16 GB RAM, NVIDIA GTX 1650 (4 GB VRAM), NVMe SSD  

---

## 1. Directory Structure

```text
REVOLUTION/
├── Project/            # Unreal Engine project root (.uproject, Source, Config, Content)
├── SourceControl/      # Git LFS locks, hooks, and version control configurations
├── Tools/              # Custom developer utilities, packaging scripts, and cache cleanups
├── Scripts/            # Automation scripts, build helpers, and CI automation
├── Documentation/      # Engineering & technical documentation
│   ├── Architecture/   # Subsystem architecture specifications
│   ├── Setup/          # Environment & toolchain setup guides
│   ├── Decisions/      # Architecture Decision Records (ADRs)
│   └── Research/       # Benchmarks, plugin evaluations, and engine notes
├── Design/             # Game design, production roadmap, and asset tracking
│   ├── GameDesignDocument.md
│   ├── TechnicalRoadmap.md
│   └── AssetRegister.csv
├── Art/                # Source art creation files before Unreal Engine import
│   ├── Blender/        # .blend source files and scene assemblies
│   ├── References/     # Concept art, photographic reference boards
│   └── Exports/        # Exported .fbx, .gltf, .png, .exr ready for ingestion
├── Build/              # Packaged build binaries and intermediate test artifacts (not tracked in VCS)
├── Tests/              # Functional test maps, automation scripts, and unit tests
├── Logs/               # Editor runtime logs, crash dumps, and profiling sessions
└── Backups/            # Milestone snapshots and critical configuration archives
```

---

## 2. Key Technical Guidelines

1. **Storage Isolation:** This project resides in `C:\Users\npal7\PROJECT\REVOLUTION` strictly outside OneDrive to eliminate cloud file locks and cache synchronization delays.
2. **Version Control Hygiene:** Generated engine directories (`Intermediate/`, `Saved/`, `DerivedDataCache/`, `.vs/`, `Binaries/`) are excluded from source control.
3. **Renderer & Scalability:** Software Ray Tracing (Lumen Software mode) is enforced to ensure consistent performance on 4 GB VRAM discrete GPUs.

---

## 3. Documentation Quick Links
- [Hardware & Environment Audit](file:///C:/Users/npal7/PROJECT/REVOLUTION/Documentation/REVOLUTION_HARDWARE_AND_ENVIRONMENT_REPORT.md)
- [Game Design Document](file:///C:/Users/npal7/PROJECT/REVOLUTION/Design/GameDesignDocument.md)
- [Technical Roadmap](file:///C:/Users/npal7/PROJECT/REVOLUTION/Design/TechnicalRoadmap.md)
- [Asset Register](file:///C:/Users/npal7/PROJECT/REVOLUTION/Design/AssetRegister.csv)
