import unreal

def inspect():
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level("/Game/Maps/L_Validation_Gym")
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = actor_sub.get_all_level_actors()
    
    keywords = ["Locomotive", "Railway", "Signal", "Cantonment", "Civil_Lines"]
    matches = []
    for a in actors:
        lbl = a.get_actor_label()
        if any(k in lbl for k in keywords):
            loc = a.get_actor_location()
            matches.append(f"{lbl} at ({loc.x:.1f}, {loc.y:.1f}, {loc.z:.1f})")
            
    unreal.log_warning(f"=== FOUND {len(matches)} RAILWAY/CANTONMENT ACTORS ===")
    for m in matches:
        unreal.log_warning(f"  {m}")

if __name__ == "__main__":
    inspect()
