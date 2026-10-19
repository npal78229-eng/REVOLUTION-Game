"""
PROJECT REVOLUTION — Task 33 Audio Ingestion: Ladder Rung Creak & Dismount Foley
Imports SFX_Ladder_Rung_Creak and SFX_Ladder_Dismount into /Game/Audio/SFX/,
assigning them to SC_SFX_Foley and ATT_Voice_Proximity.
"""

import os
import unreal

def log_qa(msg):
    unreal.log_warning(f"[LADDER_AUDIO_IMPORT] {msg}")

def import_ladder_audio_assets():
    log_qa("================================================================================")
    log_qa("  PROJECT REVOLUTION — TASK 33 LADDER FOLEY AUDIO INGESTION & ROUTING")
    log_qa("================================================================================")

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    audio_dir = os.path.join(base_dir, "Art", "Audio", "SFX")

    editor_asset_lib = unreal.EditorAssetLibrary
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    sc_foley = editor_asset_lib.load_asset("/Game/Audio/SoundClasses/SC_Foley")
    if not sc_foley:
        sc_foley = editor_asset_lib.load_asset("/Game/Audio/SoundClasses/SC_SFX")
    assert sc_foley is not None, "Failed to load SoundClass SC_Foley!"

    att_voice = editor_asset_lib.load_asset("/Game/Audio/Attenuation/ATT_Voice_Proximity")
    if not att_voice:
        att_voice = editor_asset_lib.load_asset("/Game/Audio/Attenuation/ATT_SFX_Default")

    dest_dir = "/Game/Audio/SFX"
    if not editor_asset_lib.does_directory_exist(dest_dir):
        editor_asset_lib.make_directory(dest_dir)

    wav_files = ["SFX_Ladder_Rung_Creak.wav", "SFX_Ladder_Dismount.wav"]
    tasks = []
    for f in wav_files:
        asset_name = os.path.splitext(f)[0]
        asset_path = f"{dest_dir}/{asset_name}"
        if not editor_asset_lib.does_asset_exist(asset_path):
            file_path = os.path.join(audio_dir, f).replace("\\", "/")
            if not os.path.exists(file_path):
                log_qa(f"Error: {file_path} does not exist!")
                continue

            task = unreal.AssetImportTask()
            task.filename = file_path
            task.destination_path = dest_dir
            task.destination_name = asset_name
            task.replace_existing = True
            task.automated = True
            task.save = True
            tasks.append(task)

    if tasks:
        asset_tools.import_asset_tasks(tasks)
        log_qa(f"Imported {len(tasks)} SoundWave tasks into {dest_dir}.")

    for f in wav_files:
        asset_name = os.path.splitext(f)[0]
        asset_path = f"{dest_dir}/{asset_name}"
        sw = editor_asset_lib.load_asset(asset_path)
        if sw:
            sw.set_editor_property("sound_class_object", sc_foley)
            if att_voice:
                sw.set_editor_property("attenuation_settings", att_voice)
            sw.set_editor_property("looping", False)
            editor_asset_lib.save_asset(asset_path, only_if_is_dirty=False)
            log_qa(f"Configured SoundWave: {asset_path} (SoundClass={sc_foley.get_name()}, Looping=False)")
        else:
            log_qa(f"Warning: Failed to load imported SoundWave {asset_path}")

    log_qa("Task 33 ladder audio ingestion completed successfully.")

if __name__ == "__main__":
    import_ladder_audio_assets()
