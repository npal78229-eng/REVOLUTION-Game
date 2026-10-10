"""
PROJECT REVOLUTION — AUDIO INGESTION SCRIPT
Imports synthesized 16-bit 44.1kHz PCM WAV files into /Game/Audio/SFX as USoundWave assets.
"""

import os
import unreal

def import_audio():
    audio_dir = "C:/Users/npal7/PROJECT/REVOLUTION/Art/Audio"
    dest_path = "/Game/Audio/SFX"
    
    asset_subsystem = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    if not asset_subsystem.does_directory_exist(dest_path):
        asset_subsystem.make_directory(dest_path)
        
    wav_files = [f for f in os.listdir(audio_dir) if f.lower().endswith(".wav")]
    unreal.log(f"[AUDIO] Found {len(wav_files)} WAV files to import from {audio_dir}")
    
    tasks = []
    for f in wav_files:
        asset_name = os.path.splitext(f)[0]
        file_path = os.path.join(audio_dir, f).replace("\\", "/")
        
        task = unreal.AssetImportTask()
        task.filename = file_path
        task.destination_path = dest_path
        task.destination_name = asset_name
        task.replace_existing = True
        task.automated = True
        task.save = True
        tasks.append(task)
        
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    asset_tools.import_asset_tasks(tasks)
    
    unreal.EditorAssetLibrary.save_directory("/Game/Audio", only_if_is_dirty=True, recursive=True)
    unreal.log(f"[AUDIO] Successfully imported {len(tasks)} sound waves into {dest_path}")

if __name__ == "__main__":
    import_audio()
