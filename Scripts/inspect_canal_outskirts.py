import unreal
import json

def inspect_canal_outskirts():
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)
    
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = actor_sub.get_all_level_actors()
    
    canal_actors = []
    for a in actors:
        lbl = a.get_actor_label()
        loc = a.get_actor_location()
        if any(k in lbl.lower() for k in ["canal", "rahat", "persian", "aqueduct", "sluice", "kiln", "bhatta", "safehouse"]) or loc.x < -800:
            canal_actors.append({
                "label": lbl,
                "class": a.get_class().get_name(),
                "location": f"X={loc.x:.1f}, Y={loc.y:.1f}, Z={loc.z:.1f}"
            })
            
    out_path = r"C:\Users\npal7\PROJECT\REVOLUTION\Tests\act4_canal_actors.json"
    with open(out_path, "w") as f:
        json.dump({
            "count": len(canal_actors),
            "actors": canal_actors
        }, f, indent=2)
    unreal.log_warning(f"Saved {len(canal_actors)} Canal/Outskirts actors to {out_path}")

if __name__ == "__main__":
    inspect_canal_outskirts()
