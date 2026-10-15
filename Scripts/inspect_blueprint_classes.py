import unreal

def log(msg):
    unreal.log_warning(f"[INSPECT_BP] {msg}")

log("================ INSPECTING BLUEPRINT CLASSES ================")

# 1. Inspect BP_Mohalla_Daytime_GameMode
gm_asset = unreal.EditorAssetLibrary.load_asset("/Game/Blueprints/BP_Mohalla_Daytime_GameMode")
if gm_asset:
    log(f"Loaded GM Asset: {gm_asset.get_name()} ({gm_asset.get_class().get_name()})")
    gm_cdo = unreal.get_default_object(gm_asset.generated_class())
    if gm_cdo:
        log(f"GM CDO DefaultPawnClass: {gm_cdo.get_editor_property('default_pawn_class')}")
        log(f"GM CDO HUDClass: {gm_cdo.get_editor_property('hud_class')}")
        log(f"GM CDO PlayerControllerClass: {gm_cdo.get_editor_property('player_controller_class')}")
else:
    log("Failed to load /Game/Blueprints/BP_Mohalla_Daytime_GameMode")

# 2. Inspect BP_Kabir
kabir_asset = unreal.EditorAssetLibrary.load_asset("/Game/Characters/Kabir/BP_Kabir")
if kabir_asset:
    log(f"Loaded Kabir Asset: {kabir_asset.get_name()} ({kabir_asset.get_class().get_name()})")
    kabir_cdo = unreal.get_default_object(kabir_asset.generated_class())
    if kabir_cdo:
        try:
            log(f"Kabir CDO DefaultMappingContext: {kabir_cdo.get_editor_property('default_mapping_context')}")
            log(f"Kabir CDO MoveAction: {kabir_cdo.get_editor_property('move_action')}")
            log(f"Kabir CDO LookAction: {kabir_cdo.get_editor_property('look_action')}")
            log(f"Kabir CDO JumpAction: {kabir_cdo.get_editor_property('jump_action')}")
            log(f"Kabir CDO SprintAction: {kabir_cdo.get_editor_property('sprint_action')}")
            log(f"Kabir CDO WalkSpeed: {kabir_cdo.get_editor_property('walk_speed')}")
        except Exception as e:
            log(f"Error reading Kabir CDO properties: {e}")
else:
    log("Failed to load /Game/Characters/Kabir/BP_Kabir")

# 3. Check C++ ARevolutionCharacter CDO
char_cdo = unreal.get_default_object(unreal.RevolutionCharacter)
if char_cdo:
    log(f"RevolutionCharacter CDO DefaultMappingContext: {char_cdo.get_editor_property('default_mapping_context')}")
    log(f"RevolutionCharacter CDO MoveAction: {char_cdo.get_editor_property('move_action')}")

log("================ INSPECTION COMPLETE ================")
