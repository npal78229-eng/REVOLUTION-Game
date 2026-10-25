import unreal
import json

def inspect_jallianwala_scene():
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)
    
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = actor_sub.get_all_level_actors()
    
    jallianwala_actors = []
    for a in actors:
        lbl = a.get_actor_label()
        loc = a.get_actor_location()
        if loc.y >= 2200:
            jallianwala_actors.append({
                "label": lbl,
                "class": a.get_class().get_name(),
                "location": {"x": loc.x, "y": loc.y, "z": loc.z}
            })
            
    out_path = r"C:\Users\npal7\PROJECT\REVOLUTION\Tests\jallianwala_scene_actors.json"
    with open(out_path, "w") as f:
        json.dump({
            "total_actors": len(actors),
            "actors_y_gte_2200": len(jallianwala_actors),
            "actors": sorted(jallianwala_actors, key=lambda x: x["location"]["y"])
        }, f, indent=2)
    unreal.log_warning(f"Saved inspection of {len(jallianwala_actors)} actors to {out_path}")

if __name__ == "__main__":
    inspect_jallianwala_scene()
