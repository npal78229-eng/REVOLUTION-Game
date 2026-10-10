# PROJECT REVOLUTION — 3D Art & Asset Pipeline (Blender to Unreal Engine)

**Author:** Technical Artist & Unreal Engine Specialist  
**Tools:** Blender 5.2.1 LTS $\rightarrow$ Unreal Engine 5.4 / 5.5  
**Date:** October 10, 2026  

---

## 1. Asset Creation Pipeline Overview

```mermaid
flowchart LR
    Ref["Reference Gathering\n(Art/References)"] --> Model["Blender 5.2 Modeling\n(Art/Blender)"]
    Model --> Bake["Bake & UV Unpack\nCycles CUDA OptiX"]
    Bake --> Export["Export FBX/glTF\n(Art/Exports)"]
    Export --> UE["Import to UE5 Content\nNanite / Lumen Setup"]
    UE --> Log["Update AssetRegister.csv"]
```

---

## 2. Blender Modeling & Scene Conventions

1. **Units & Scale:**
   - Unit System: Metric
   - Length: Centimeters (1 Blender Unit = 1 Unreal Unit = 1 cm)
2. **Orientation:**
   - Forward: X-Forward / Y-Forward mapped to Unreal X-Forward (+X)
   - Up: +Z Up
3. **Pivots & Origin Points:**
   - Static Meshes: Pivot at ground base or natural connection point (0, 0, 0).
   - Modular Kits: Pivot snapped to grid corner (100cm / 50cm increments).

---

## 3. FBX Export Configuration (Blender 5.2)

When exporting static or skeletal meshes from Blender:
- Format: `FBX 2020` binary.
- Transform:
  - Apply Scalings: `FBX All`
  - Forward: `-Z Forward`
  - Up: `Y Up` *(matches standard Blender to UE transform conversion)*
  - Apply Transform: `Checked`
- Geometry:
  - Smoothing: `Face`
  - Tangent Space: `Checked` (for normal mapping)

---

## 4. Texture & Material Rules

1. **ORM Texture Packing (Mandatory):**
   - Channel R: Ambient Occlusion
   - Channel G: Roughness
   - Channel B: Metallic
   - Texture Compression in UE: `Masks (no sRGB)`
2. **Resolution Budgets:**
   - Hero Character / Primary Weapon: $2048 \times 2048$
   - Medium Environment Props (Rocks, Trees, Buildings): $1024 \times 1024$ or $2048 \times 2048$
   - Small Modular Props / Decals: $512 \times 512$
3. **Master Material Architecture:**
   - All assets instantiate material instances (`MI_...`) derived from `M_Master_PBR`.
   - No bespoke complex material graphs for standard props.
