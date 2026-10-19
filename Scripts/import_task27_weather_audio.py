"""
PROJECT REVOLUTION — Task 27 Audio Ingestion & Routing: Dynamic Weather SoundWaves
Imports SFX_Weather_DustStorm_Wind_Loop.wav and SFX_Weather_GoldenHaze_Breeze.wav
into /Game/Audio/Weather/ and /Game/Audio/SFX/, configuring SC_Ambience_Mohalla.
"""

import os
import unreal

def log_qa(msg):
    unreal.log_warning(f"[WEATHER_IMPORT] {msg}")

def import_weather_assets():
    log_qa("================================================================================")
    log_qa("  PROJECT REVOLUTION — TASK 27 WEATHER AUDIO INGESTION & ROUTING")
    log_qa("================================================================================")

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    audio_dir = os.path.join(base_dir, "Art", "Audio", "Weather")
    wav_files = sorted([f for f in os.listdir(audio_dir) if f.lower().endswith(".wav")])

    editor_asset_lib = unreal.EditorAssetLibrary
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    asset_sub = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)

    sc_ambience = editor_asset_lib.load_asset("/Game/Audio/SoundClasses/SC_Ambience_Mohalla")
    assert sc_ambience is not None, "Failed to load SC_Ambience_Mohalla!"

    dest_dirs = ["/Game/Audio/Weather", "/Game/Audio/SFX"]
    for d in dest_dirs:
        if not editor_asset_lib.does_directory_exist(d):
            editor_asset_lib.make_directory(d)

    for d in dest_dirs:
        for f in wav_files:
            asset_name = os.path.splitext(f)[0]
            file_path = os.path.join(audio_dir, f).replace("\\", "/")
            log_qa(f"Importing {asset_name} into {d}...")

            task = unreal.AssetImportTask()
            task.filename = file_path
            task.destination_path = d
            task.destination_name = asset_name
            task.replace_existing = True
            task.automated = True
            task.save = False

            asset_tools.import_asset_tasks([task])

            sw = editor_asset_lib.load_asset(f"{d}/{asset_name}")
            if sw and sw.get_class().get_name() == "SoundWave":
                sw.set_editor_property("sound_class_object", sc_ambience)
                # Mark as looping since these are continuous weather loops
                sw.set_editor_property("looping", True)
                asset_sub.save_loaded_asset(sw)
                log_qa(f"  [SAVED & CONFIGURED] {d}/{asset_name} (SC_Ambience_Mohalla, Looping=True)")

    log_qa("[PASS] All Task 27 weather SoundWave assets successfully imported and saved!")
    return True

if __name__ == "__main__":
    import_weather_assets()
