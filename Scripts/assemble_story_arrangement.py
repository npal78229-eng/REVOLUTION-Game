"""
PROJECT REVOLUTION — Level Assembler for Story Narrative Arrangement
Loads L_Validation_Gym and arranges newly created Blender storytelling assets:
1. Zone A Haveli Courtyard: Earthen Mud Cooking Stove (SM_Prop_Courtyard_Chulha_Stove) at (60, -80, 10)
2. Zone A Veranda Charpai: Student Wooden Writing Slate (SM_Prop_School_Takhti_Slate) at (160, 140, 25)
3. Zone A Rooftop Terrace: Wooden Pigeon Coop (SM_Prop_Pigeon_Coop_KabootarKhana) at (-60, 240, 410)
4. Zone D Grand Bazaar: Wooden Market Handcart (SM_Prop_Bazaar_Cart_Thela) at (-40, 1850, 88)
5. Zone C Sacred Peepal Shrine: Secret Anti-Rowlatt Pamphlet Stack (SM_Prop_Pamphlet_Stack_Rowlatt) at (410, 1370, 30)
6. Zone A Litho Workshop: Secret Anti-Rowlatt Pamphlet Stack at (120, 195, 60)
"""

import unreal

def log(msg):
    unreal.log_warning(f"[REVOLUTION_STORY_ARRANGER] {msg}")

def run_arrangement():
    log("Arranging storytelling assets according to narrative progression...")

    level_editor_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    editor_actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    level_path = "/Game/Maps/L_Validation_Gym"
    level_editor_sub.load_level(level_path)

    # Clean previous instances if present
    labels_to_clean = [
        "Story_Courtyard_Chulha_Stove",
        "Story_School_Takhti_Slate",
        "Story_Rooftop_Pigeon_Coop",
        "Story_Bazaar_Cart_Thela",
        "Story_Peepal_Pamphlet_Stack",
        "Story_Litho_Pamphlet_Stack"
    ]
    for a in editor_actor_sub.get_all_level_actors():
        if a.get_actor_label() in labels_to_clean:
            editor_actor_sub.destroy_actor(a)
            log(f"Cleaned existing actor: {a.get_actor_label()}")

    # Cache Meshes
    mesh_keys = [
        "SM_Prop_School_Takhti_Slate",
        "SM_Prop_Bazaar_Cart_Thela",
        "SM_Prop_Courtyard_Chulha_Stove",
        "SM_Prop_Pigeon_Coop_KabootarKhana",
        "SM_Prop_Pamphlet_Stack_Rowlatt"
    ]
    mesh_cache = {}
    for mk in mesh_keys:
        m_obj = unreal.load_asset(f"/Game/Environment/Mohalla/Meshes/{mk}")
        if m_obj:
            mesh_cache[mk] = m_obj
            log(f"Cached mesh: {mk}")
        else:
            log(f"Warning: Failed to load mesh {mk}")

    def spawn_story_prop(mesh_key, loc, rot=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0), label=None):
        if mesh_key not in mesh_cache:
            log(f"Error: {mesh_key} not in cache")
            return None
        m_obj = mesh_cache[mesh_key]
        actor = unreal.EditorLevelLibrary.spawn_actor_from_object(
            m_obj,
            unreal.Vector(loc[0], loc[1], loc[2]),
            unreal.Rotator(rot[0], rot[1], rot[2])
        )
        if actor:
            actor.set_actor_scale3d(unreal.Vector(scale[0], scale[1], scale[2]))
            if label:
                actor.set_actor_label(label)
            sm_comp = actor.get_component_by_class(unreal.StaticMeshComponent)
            if sm_comp:
                sm_comp.set_collision_profile_name("BlockAll")
                sm_comp.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)
                sm_comp.set_mobility(unreal.ComponentMobility.STATIC)
            log(f"Spawned {label} at {loc}")
        return actor

    # 1. Zone A Haveli Courtyard: Earthen Mud Cooking Stove (Mitti da Chulha)
    spawn_story_prop(
        "SM_Prop_Courtyard_Chulha_Stove",
        (60.0, -80.0, 10.0),
        rot=(0.0, 45.0, 0.0),
        scale=(1.0, 1.0, 1.0),
        label="Story_Courtyard_Chulha_Stove"
    )

    # 2. Zone A Veranda: Kabir's Wooden Writing Slate (Takhti) on charpai
    spawn_story_prop(
        "SM_Prop_School_Takhti_Slate",
        (160.0, 140.0, 25.0),
        rot=(15.0, -25.0, 0.0),
        scale=(1.0, 1.0, 1.0),
        label="Story_School_Takhti_Slate"
    )

    # 3. Zone A Rooftop Terrace: Wooden Pigeon Coop (Kabootar-khana)
    spawn_story_prop(
        "SM_Prop_Pigeon_Coop_KabootarKhana",
        (-60.0, 240.0, 410.0),
        rot=(0.0, 90.0, 0.0),
        scale=(1.0, 1.0, 1.0),
        label="Story_Rooftop_Pigeon_Coop"
    )

    # 4. Zone D Grand Bazaar: Wooden Market Handcart (Thela)
    spawn_story_prop(
        "SM_Prop_Bazaar_Cart_Thela",
        (-40.0, 1850.0, 88.0),
        rot=(0.0, 15.0, 0.0),
        scale=(1.0, 1.0, 1.0),
        label="Story_Bazaar_Cart_Thela"
    )

    # 5. Zone C Sacred Peepal Tree Shrine: Clandestine Anti-Rowlatt Pamphlet Stack
    spawn_story_prop(
        "SM_Prop_Pamphlet_Stack_Rowlatt",
        (410.0, 1370.0, 30.0),
        rot=(0.0, -35.0, 0.0),
        scale=(1.0, 1.0, 1.0),
        label="Story_Peepal_Pamphlet_Stack"
    )

    # 6. Zone A Litho Workshop: Clandestine Anti-Rowlatt Pamphlet Stack
    spawn_story_prop(
        "SM_Prop_Pamphlet_Stack_Rowlatt",
        (120.0, 195.0, 60.0),
        rot=(0.0, 0.0, 0.0),
        scale=(1.0, 1.0, 1.0),
        label="Story_Litho_Pamphlet_Stack"
    )

    # Save level and dirty packages
    level_editor_sub.save_current_level()
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(False, True)
    unreal.EditorAssetLibrary.save_directory("/Game", only_if_is_dirty=True, recursive=True)
    log("=== Narrative Story Arrangement Complete & Saved Successfully ===")

if __name__ == "__main__":
    run_arrangement()
