import json
import unreal

def main():
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level("/Game/Maps/L_Validation_Gym")

    actors = actor_sub.get_all_level_actors()
    data = {
        "civilians": [],
        "doors": [],
        "hazards": [],
        "restitutions": []
    }

    civ_class = unreal.load_class(None, "/Script/REVOLUTION.CivilianNPCActor")
    door_class = unreal.load_class(None, "/Script/REVOLUTION.DoorDeorhiActor")
    hazard_class = unreal.load_class(None, "/Script/REVOLUTION.TerracottaHazardActor")
    restitution_class = unreal.load_class(None, "/Script/REVOLUTION.RestitutionDropActor")

    for a in actors:
        label = a.get_actor_label()
        loc = f"({a.get_actor_location().x:.0f}, {a.get_actor_location().y:.0f}, {a.get_actor_location().z:.0f})"
        
        if a.get_class() == civ_class:
            cluster = str(a.get_editor_property("community_cluster_id"))
            data["civilians"].append({"label": label, "cluster": cluster, "loc": loc})
        elif a.get_class() == door_class:
            cluster = str(a.get_editor_property("community_cluster_id"))
            bolted = a.is_door_bolted()
            data["doors"].append({"label": label, "cluster": cluster, "bolted": bolted, "loc": loc})
        elif a.get_class() == hazard_class:
            cluster = str(a.get_editor_property("community_cluster_id"))
            data["hazards"].append({"label": label, "cluster": cluster, "loc": loc})
        elif a.get_class() == restitution_class:
            cluster = str(a.get_editor_property("community_cluster_id"))
            paid = a.get_editor_property("has_been_paid")
            data["restitutions"].append({"label": label, "cluster": cluster, "paid": paid, "loc": loc})

    out_file = "C:/Users/npal7/PROJECT/REVOLUTION/Tests/cluster_actors_audit.json"
    with open(out_file, "w") as f:
        json.dump(data, f, indent=2)

    unreal.log_warning(f"Saved cluster audit: {len(data['civilians'])} civs, {len(data['doors'])} doors, {len(data['hazards'])} hazards, {len(data['restitutions'])} restitutions to {out_file}")

if __name__ == "__main__":
    main()
