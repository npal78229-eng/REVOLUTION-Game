import unreal

def test_spawn():
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)

    editor_actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    
    mesh = unreal.load_asset("/Game/Environment/Mohalla/Meshes/SM_Locomotive_Engine_PunjabMail")
    unreal.log_warning(f"Loaded mesh: {mesh}")

    actor = editor_actor_sub.spawn_actor_from_class(
        unreal.StaticMeshActor,
        unreal.Vector(1000.0, 3900.0, 30.0),
        unreal.Rotator(0.0, 90.0, 0.0)
    )
    unreal.log_warning(f"Spawned actor from class: {actor}")
    if actor:
        actor.static_mesh_component.set_static_mesh(mesh)
        actor.set_actor_label("Locomotive_Engine_PunjabMail_Depot")
        unreal.log_warning("Successfully set static mesh and label!")
        editor_actor_sub.destroy_actor(actor)
        unreal.log_warning("Successfully cleaned up test actor!")

if __name__ == "__main__":
    test_spawn()
