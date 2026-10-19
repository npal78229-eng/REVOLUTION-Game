"""
PROJECT REVOLUTION — Task 25 Audio Ingestion & Routing: Baisakhi Dawn Epilogue
Imports SFX_Epilogue_BaisakhiDawn.wav into /Game/Audio/SFX/,
assigns it to SC_Ambience_Mohalla SoundClass, and verifies loading.
"""

import os
import unreal

def log_warn(msg):
    unreal.log_warning(f"[EPILOGUE_AUDIO_IMPORT] {msg}")

def import_epilogue_audio():
    log_warn("================================================================================")
    log_warn("  PROJECT REVOLUTION — TASK 25 EPILOGUE AUDIO INGESTION & ROUTING")
    log_warn("================================================================================")

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    wav_path = os.path.join(base_dir, "Art", "Audio", "SFX_Epilogue_BaisakhiDawn.wav").replace("\\", "/")
    assert os.path.exists(wav_path), f"Missing WAV file: {wav_path}"

    editor_asset_lib = unreal.EditorAssetLibrary
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    sc_ambience = editor_asset_lib.load_asset("/Game/Audio/SoundClasses/SC_Ambience_Mohalla")
    assert sc_ambience is not None, "Failed to load SC_Ambience_Mohalla!"

    dest_dir = "/Game/Audio/SFX"
    if not editor_asset_lib.does_directory_exist(dest_dir):
        editor_asset_lib.make_directory(dest_dir)

    task = unreal.AssetImportTask()
    task.filename = wav_path
    task.destination_path = dest_dir
    task.destination_name = "SFX_Epilogue_BaisakhiDawn"
    task.replace_existing = True
    task.automated = True
    task.save = True

    asset_tools.import_asset_tasks([task])
    log_warn(f"Imported SoundWave task to {dest_dir}/SFX_Epilogue_BaisakhiDawn")

    sound_asset = editor_asset_lib.load_asset(f"{dest_dir}/SFX_Epilogue_BaisakhiDawn")
    assert sound_asset is not None, "Failed to load imported SoundWave!"

    sound_asset.set_editor_property("sound_class_object", sc_ambience)
    unreal.get_editor_subsystem(unreal.EditorAssetSubsystem).save_loaded_asset(sound_asset)
    log_warn(f"[PASS] Successfully routed SFX_Epilogue_BaisakhiDawn to SoundClass: {sc_ambience.get_name()}")

if __name__ == "__main__":
    import_epilogue_audio()
