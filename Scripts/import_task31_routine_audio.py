"""
PROJECT REVOLUTION — Task 31 Audio Ingestion & Routing: Civilian Routine Foley Loops
Imports the 6 synthesized occupational routine tracks into /Game/Audio/SFX/,
assigning them to SC_SFX_Foley / SC_Environment and ATT_Voice_Proximity attenuation.
"""

import os
import unreal

def log_qa(msg):
    unreal.log_warning(f"[ROUTINE_AUDIO_IMPORT] {msg}")

def import_routine_audio_assets():
    log_qa("================================================================================")
    log_qa("  PROJECT REVOLUTION — TASK 31 ROUTINE FOLEY AUDIO INGESTION & ROUTING")
    log_qa("================================================================================")

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    audio_dir = os.path.join(base_dir, "Art", "Audio", "SFX", "Routines")

    editor_asset_lib = unreal.EditorAssetLibrary
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    # Load SoundClass and Attenuation
    sc_foley = editor_asset_lib.load_asset("/Game/Audio/SoundClasses/SC_SFX_Foley")
    if not sc_foley:
        sc_foley = editor_asset_lib.load_asset("/Game/Audio/SoundClasses/SC_Voice_Punjabi")
    assert sc_foley is not None, "Failed to load SoundClass!"

    att_voice = editor_asset_lib.load_asset("/Game/Audio/Attenuation/ATT_Voice_Proximity")
    assert att_voice is not None, "Failed to load ATT_Voice_Proximity!"

    dest_dir = "/Game/Audio/SFX"
    if not editor_asset_lib.does_directory_exist(dest_dir):
        editor_asset_lib.make_directory(dest_dir)

    wav_files = [f for f in os.listdir(audio_dir) if f.lower().endswith(".wav")]
    log_qa(f"Found {len(wav_files)} routine foley WAV files in {audio_dir} to import.")

    tasks = []
    for f in wav_files:
        asset_name = os.path.splitext(f)[0]
        file_path = os.path.join(audio_dir, f).replace("\\", "/")

        task = unreal.AssetImportTask()
        task.filename = file_path
        task.destination_path = dest_dir
        task.destination_name = asset_name
        task.replace_existing = True
        task.automated = True
        task.save = True
        tasks.append(task)

    asset_tools.import_asset_tasks(tasks)
    log_qa(f"Imported {len(tasks)} SoundWave tasks into {dest_dir}.")

    # Configure SoundClass, Attenuation, and Looping
    for f in wav_files:
        asset_name = os.path.splitext(f)[0]
        asset_path = f"{dest_dir}/{asset_name}"
        sw = editor_asset_lib.load_asset(asset_path)
        if sw:
            sw.set_editor_property("sound_class_object", sc_foley)
            sw.set_editor_property("attenuation_settings", att_voice)
            sw.set_editor_property("looping", True)
            editor_asset_lib.save_asset(asset_path)
            log_qa(f"  [ROUTED] {asset_name} -> SoundClass: {sc_foley.get_name()}, Attenuation: {att_voice.get_name()}, Looping: True")

    log_qa("Task 31 Audio Ingestion & Routing 100% COMPLETE.")
    return True

if __name__ == "__main__":
    success = import_routine_audio_assets()
    import sys
    sys.exit(0 if success else 1)
