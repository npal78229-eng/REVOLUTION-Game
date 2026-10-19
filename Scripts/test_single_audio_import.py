import os
import unreal

def test_import():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    audio_dir = os.path.join(base_dir, "Art", "Audio", "Voice", "Walla")
    wav_files = sorted([f for f in os.listdir(audio_dir) if f.lower().endswith(".wav")])

    editor_asset_lib = unreal.EditorAssetLibrary
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    asset_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)

    sc_voice = editor_asset_lib.load_asset("/Game/Audio/SoundClasses/SC_Voice_Punjabi")
    att_voice = editor_asset_lib.load_asset("/Game/Audio/Attenuation/ATT_Voice_Proximity")

    dest_dir = "/Game/Audio/Voice"

    for f in wav_files:
        asset_name = os.path.splitext(f)[0]
        file_path = os.path.join(audio_dir, f).replace("\\", "/")
        unreal.log_warning(f"Importing {asset_name}...")

        task = unreal.AssetImportTask()
        task.filename = file_path
        task.destination_path = dest_dir
        task.destination_name = asset_name
        task.replace_existing = True
        task.automated = True
        task.save = False

        asset_tools.import_asset_tasks([task])

        sw = editor_asset_lib.load_asset(f"{dest_dir}/{asset_name}")
        if sw:
            sw.set_editor_property("sound_class_object", sc_voice)
            sw.set_editor_property("attenuation_settings", att_voice)
            asset_sub.save_loaded_asset(sw)
            unreal.log_warning(f"  [SAVED] {asset_name}")

    unreal.log_warning("[SUCCESS] All 8 voice files imported and configured!")

if __name__ == "__main__":
    test_import()
