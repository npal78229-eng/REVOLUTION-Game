import unreal

skel_path = "/Game/Characters/Kabir_v06/SKM_Kabir_v06_Child_12_Skeleton"
skeleton = unreal.load_asset(skel_path)
fbx_path = "C:/Users/npal7/PROJECT/REVOLUTION/Art/Character/Kabir_v06/Animations/Anim_Kabir_v06_Idle.fbx"
dest_path = "/Game/Characters/Kabir_v06/Animations"

task = unreal.AssetImportTask()
task.filename = fbx_path
task.destination_path = dest_path
task.destination_name = "Anim_Kabir_v06_Idle"
task.replace_existing = True
task.automated = True
task.save = True

options = unreal.FbxImportUI()
options.automated_import_should_detect_type = False
options.mesh_type_to_import = unreal.FBXImportType.FBXIT_ANIMATION
options.import_mesh = False
options.import_as_skeletal = True
options.import_animations = True
options.skeleton = skeleton

task.options = options

asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
asset_tools.import_asset_tasks([task])

anim_asset = unreal.load_asset(f"{dest_path}/Anim_Kabir_v06_Idle")
if anim_asset:
    unreal.log_warning(f"SUCCESS: Loaded {anim_asset.get_name()}")
else:
    unreal.log_warning("FAILED to load imported animation.")
