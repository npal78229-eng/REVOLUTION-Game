import unreal

world = unreal.EditorLevelLibrary.get_editor_world()
actors = unreal.EditorActorSubsystem().get_all_level_actors()

target = None
for a in actors:
    if a.get_name() == "StaticMeshActor_200" or a.get_actor_label() == "StaticMeshActor_200":
        target = a
        break

if target:
    unreal.log_warning(f"Found StaticMeshActor_200: {target.get_actor_label()} ({target.get_name()})")
    unreal.log_warning(f"  Class: {target.get_class().get_name()}")
    unreal.log_warning(f"  Location: {target.get_actor_location()}")
    unreal.log_warning(f"  Rotation: {target.get_actor_rotation()}")
    smc = target.get_component_by_class(unreal.StaticMeshComponent)
    if smc:
        mesh = smc.get_editor_property("static_mesh")
        mesh_name = mesh.get_name() if mesh else "None"
        unreal.log_warning(f"  StaticMesh: {mesh_name} ({mesh.get_path_name() if mesh else ''})")
        unreal.log_warning(f"  CollisionProfileName: {smc.get_collision_profile_name()}")
        unreal.log_warning(f"  CollisionEnabled: {smc.get_collision_enabled()}")
        bounds = target.get_actor_bounds(False)
        unreal.log_warning(f"  Bounds: Origin={bounds[0]}, BoxExtent={bounds[1]}")
else:
    unreal.log_warning("StaticMeshActor_200 not found by name, listing actors near (118, 1795):")
    for a in actors:
        loc = a.get_actor_location()
        dist = ((loc.x - 118)**2 + (loc.y - 1795)**2)**0.5
        if dist < 200:
            unreal.log_warning(f"  Near actor: {a.get_actor_label()} ({a.get_name()}) at {loc}")

# Also fix the 4 Kabir clean materials
materials_to_fix = [
    "/Game/Characters/Kabir_v05/Materials/M_Kabir_Skin_Clean",
    "/Game/Characters/Kabir_v05/Materials/M_Kabir_Eye_Clean",
    "/Game/Characters/Kabir_v05/Materials/M_Kabir_Hair_Clean",
    "/Game/Characters/Kabir_v05/Materials/M_Kabir_Khadi_Clean",
    "/Game/Characters/Kabir_v05/M_Hair",
    "/Game/Characters/Kabir_v05/M_Kabir_Skin_PBR",
    "/Game/Characters/Kabir_v05/M_Kabir_Eye_PBR",
    "/Game/Characters/Kabir_v05/M_Kabir_Khadi_PBR",
    "/Game/Characters/Kabir_v05/M_Kabir_Leather_PBR"
]

editor_asset_lib = unreal.EditorAssetLibrary()
for mat_path in materials_to_fix:
    mat = unreal.EditorAssetLibrary.load_asset(mat_path)
    if mat and isinstance(mat, unreal.Material):
        cur_flag = mat.get_editor_property("used_with_skeletal_mesh")
        unreal.log_warning(f"Material {mat_path}: used_with_skeletal_mesh was {cur_flag}")
        if not cur_flag:
            mat.set_editor_property("used_with_skeletal_mesh", True)
            unreal.MaterialEditingLibrary.recompile_material(mat)
            editor_asset_lib.save_loaded_asset(mat)
            unreal.log_warning(f"  -> FIXED & SAVED: {mat_path}")
