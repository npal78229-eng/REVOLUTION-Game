"""
Check BlueprintEditorLibrary methods
"""
import unreal

methods = [m for m in dir(unreal.BlueprintEditorLibrary) if not m.startswith('_')]
unreal.log_warning(f"BlueprintEditorLibrary methods: {methods}")
