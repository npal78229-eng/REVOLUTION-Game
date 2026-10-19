"""
PROJECT REVOLUTION — Task 26 Audio Ingestion & Routing: Multi-Dialect Punjabi Voice Assets
Imports the 8 synthesized Punjabi walla voice tracks into /Game/Audio/Voice/ and /Game/Audio/SFX/,
assigning them to SC_Voice_Punjabi and ATT_Voice_Proximity attenuation.
"""

import os
import unreal

def log_qa(msg):
    unreal.log_warning(f"[VOICE_WALLA_IMPORT] {msg}")

def import_walla_voice_assets():
    log_qa("================================================================================")
    log_qa("  PROJECT REVOLUTION — TASK 26 MULTI-DIALECT VOICE INGESTION & ROUTING")
    log_qa("================================================================================")

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    audio_dir = os.path.join(base_dir, "Art", "Audio", "Voice", "Walla")

    editor_asset_lib = unreal.EditorAssetLibrary
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    # Load SoundClass and Attenuation
    sc_voice = editor_asset_lib.load_asset("/Game/Audio/SoundClasses/SC_Voice_Punjabi")
    assert sc_voice is not None, "Failed to load SC_Voice_Punjabi!"
    att_voice = editor_asset_lib.load_asset("/Game/Audio/Attenuation/ATT_Voice_Proximity")
    assert att_voice is not None, "Failed to load ATT_Voice_Proximity!"

    dest_dirs = ["/Game/Audio/Voice", "/Game/Audio/SFX"]
    for d in dest_dirs:
        if not editor_asset_lib.does_directory_exist(d):
            editor_asset_lib.make_directory(d)

    wav_files = [f for f in os.listdir(audio_dir) if f.lower().endswith(".wav")]
    log_qa(f"Found {len(wav_files)} multi-dialect voice WAV files in {audio_dir} to import.")

    tasks = []
    for d in dest_dirs:
        for f in wav_files:
            asset_name = os.path.splitext(f)[0]
            file_path = os.path.join(audio_dir, f).replace("\\", "/")

            task = unreal.AssetImportTask()
            task.filename = file_path
            task.destination_path = d
            task.destination_name = asset_name
            task.replace_existing = True
            task.automated = True
            task.save = True
            tasks.append(task)

    asset_tools.import_asset_tasks(tasks)
    log_qa(f"Imported {len(tasks)} SoundWave tasks across {dest_dirs}.")

    # Configure SoundClass and Attenuation for all imported voice assets
    configured_count = 0
    for d in dest_dirs:
        for f in wav_files:
            asset_name = os.path.splitext(f)[0]
            asset_path = f"{d}/{asset_name}"
            sw = editor_asset_lib.load_asset(asset_path)
            if sw and sw.get_class().get_name() == "SoundWave":
                sw.set_editor_property("sound_class_object", sc_voice)
                sw.set_editor_property("attenuation_settings", att_voice)
                editor_asset_lib.save_loaded_asset(sw)
                configured_count += 1

    log_qa(f"[PASS] Successfully configured SoundClass (SC_Voice_Punjabi) and Attenuation (ATT_Voice_Proximity) on {configured_count} voice assets.")
    editor_asset_lib.save_directory("/Game/Audio", only_if_is_dirty=True, recursive=True)
    return True

if __name__ == "__main__":
    import_walla_voice_assets()
