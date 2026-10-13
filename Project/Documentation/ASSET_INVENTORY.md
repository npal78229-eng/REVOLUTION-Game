# Asset Inventory

## Reused (existing, /Game/Environment/Mohalla/Meshes)
Wall (plain/window/doorway 4x4 m), Floor_Ceiling_Slab_4x4m, Roof_Parapet_4m_A, Door_Deorhi_Teak_01, Market_Stall_Wood_Awning, Mohalla_Well_Stone, Shop_Shutter_Foldable, Prop_ShopSign_Wood, Prop_SpiceBasket_Woven, Prop_GrainSack_Jute_01, Prop_ClayChaiCup_Kulhad, Prop_Charpai_RopeBed, Prop_HurricaneLantern, Prop_Kite_Spool_Charkhi. Not yet placed: Balcony_Jharokha_Wood_A, Roof_Stairs_Masonry_01.
All low-poly (12-290 tris) with convex collision (complex-as-simple); Nanite off.

## Materials
Rebuilt (were empty): M_LahoriBrick_PBR, M_AgedTeak_PBR, M_WroughtIron_PBR, M_Clay_PBR.
New flat-colour placeholders: M_DirtRoad_PBR, M_FieldGrass_PBR, M_PlasterOchre_PBR, M_Foliage_PBR, M_Bark_PBR, M_ClothSaffron_PBR, M_ClothIndigo_PBR.
Some meshes reference M_Terracotta_PBR / M_JuteRope_PBR, which do not exist.

## New project assets
/Game/Characters/Kabir/BP_Kabir; /Game/Blueprints/BP_RevolutionGameMode; /Game/Blueprints/BP_Mohalla_Daytime_GameMode; /Game/Maps/L_Mohalla_Home; input actions IA_Sprint, IA_Crouch, IA_Interact (+ keys in IMC_Default).
6 InspectableProp actors in the family home (placeholder descriptions).

## Placeholders (engine primitives)
Trees, low table, water pot, blackboard, pillars, cloth bolts, fields, boundary hedges.

## Added 2026-10-12 (later)
- FamilyHome_Jharokha_Balcony (SM_Balcony_Jharokha_Wood_A) above the front door of the family home, protruding toward the street.
- FamilyHome_Roof_Stairs (SM_Roof_Stairs_Masonry_01) in the gap between the family home and the west neighbour, at (-1600, 930).
- CHARACTER_DESIGN.md created (Kabir brief, placeholder).

## Roof access (2026-10-12)
- RoofStairs_Step_00..09: Cube primitives, M_LahoriBrick_PBR. Placeholder geometry, not final stair art.
- RoofStairs_Guard_Parapet: SM_Roof_Parapet_4m_A.
- Removed (actor only): FamilyHome_Roof_Stairs, FamilyHome_ParaL_0.
- Unused asset kept: SM_Roof_Stairs_Masonry_01 (not placed).
