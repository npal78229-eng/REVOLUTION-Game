import unreal

def log(msg):
    unreal.log_warning(f"[INSPECT_INPUT] {msg}")

imc = unreal.EditorAssetLibrary.load_asset("/Game/Characters/Kabir/Input/IMC_Default")
if not imc:
    log("Failed to load /Game/Characters/Kabir/Input/IMC_Default")
else:
    log(f"Loaded IMC: {imc.get_name()}")
    mappings = imc.get_editor_property("mappings")
    log(f"Mappings count: {len(mappings)}")
    for m in mappings:
        action = m.get_editor_property("action")
        key = m.get_editor_property("key")
        act_name = action.get_name() if action else "None"
        key_name = key.get_editor_property("key_name") if key else "None"
        modifiers = m.get_editor_property("modifiers")
        mod_names = [mod.get_class().get_name() for mod in modifiers]
        log(f"  Mapping: Action={act_name}, Key={key_name}, Modifiers={mod_names}")
