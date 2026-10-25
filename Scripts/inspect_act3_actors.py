import unreal
import json

def inspect_act3_actors():
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)
    
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = actor_sub.get_all_level_actors()
    
    act3_actors = []
    for a in actors:
        lbl = a.get_actor_label()
        loc = a.get_actor_location()
        if any(k in lbl.lower() for k in ["curfew", "searchlight", "stretcher", "clinic", "bunker", "lantern", "survivor"]):
            act3_actors.append({
                "label": lbl,
                "class": a.get_class().get_name(),
                "location": f"X={loc.x:.1f}, Y={loc.y:.1f}, Z={loc.z:.1f}"
            })
            
    out_path = r"C:\Users\npal7\PROJECT\REVOLUTION\Tests\act3_scene_actors.json"
    with open(out_path, "w") as f:
        json.dump({
            "count": len(act3_actors),
            "actors": act3_actors
        }, f, indent=2)
    unreal.log_warning(f"Saved {len(act3_actors)} Act III actors to {out_path}")

if __name__ == "__main__":
    inspect_act3_actors()
