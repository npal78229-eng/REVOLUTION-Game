import unreal

sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
print("=== LevelEditorSubsystem methods ===")
for m in dir(sub):
    if any(k in m.lower() for k in ['pie', 'play', 'sim', 'level']):
        print(m)

print("=== EditorLevelLibrary methods ===")
for m in dir(unreal.EditorLevelLibrary):
    if any(k in m.lower() for k in ['pie', 'play', 'sim']):
        print(m)
