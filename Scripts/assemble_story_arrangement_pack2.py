"""
PROJECT REVOLUTION — Level Assembler for Story Narrative Arrangement Pack 2
Loads L_Validation_Gym and arranges Pack 2 Blender storytelling assets:
1. Zone A Haveli Courtyard: Traditional Carved Shisham Grain Chest (SM_Prop_Haveli_Grain_Sandook) at (120, -120, 10)
2. Zone A Rooftop Terrace: Basant Fighter Kites & Glass Manja Spool (SM_Prop_Rooftop_Patang_Charkhi) at (20, 260, 408)
3. Zone D Grand Bazaar: Mandi Balance Scale with Brass Pans & Iron Weights (SM_Prop_Bazaar_Tarazu_Scale) at (180, 1720, 60)
4. Zone D Bazaar Curfew Checkpoint: Imperial Red Pillar Postbox (SM_Prop_Imperial_Postbox_GR) at (60, 2150, 10)
5. District C School Classroom 4B: Punjab 1919 Province Map Easel & Pointer (SM_Prop_School_Wall_Map_Easel) at (1100, 1920, 10)
"""

import unreal

def log(msg):
    unreal.log_warning(f"[REVOLUTION_STORY_ARRANGER_PACK2] {msg}")

def run_arrangement():
    log("Arranging Pack 2 storytelling assets according to narrative progression...")

    level_editor_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    editor_actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    level_path = "/Game/Maps/L_Validation_Gym"
    level_editor_sub.load_level(level_path)

    # Clean previous instances if present
    labels_to_clean = [
        "Story_Haveli_Grain_Sandook",
        "Story_Rooftop_Patang_Charkhi",
        "Story_Bazaar_Tarazu_Scale",
        "Story_Imperial_Postbox_GR",
        "Story_School_Wall_Map_Easel"
    ]
    for a in editor_actor_sub.get_all_level_actors():
        if a.get_actor_label() in labels_to_clean:
            editor_actor_sub.destroy_actor(a)
            log(f"Cleaned existing actor: {a.get_actor_label()}")

    # Cache Meshes
    mesh_keys = [
        "SM_Prop_Imperial_Postbox_GR",
        "SM_Prop_Bazaar_Tarazu_Scale",
        "SM_Prop_Rooftop_Patang_Charkhi",
        "SM_Prop_Haveli_Grain_Sandook",
        "SM_Prop_School_Wall_Map_Easel"
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

    # 1. Zone A Haveli Courtyard: Traditional Carved Shisham Grain & Dowry Chest
    spawn_story_prop(
        "SM_Prop_Haveli_Grain_Sandook",
        (120.0, -120.0, 10.0),
        rot=(0.0, 15.0, 0.0),
        scale=(1.0, 1.0, 1.0),
        label="Story_Haveli_Grain_Sandook"
    )

    # 2. Zone A Rooftop Terrace: Basant Fighter Kites & Glass Manja Spool
    spawn_story_prop(
        "SM_Prop_Rooftop_Patang_Charkhi",
        (20.0, 260.0, 408.0),
        rot=(0.0, 45.0, 0.0),
        scale=(1.0, 1.0, 1.0),
        label="Story_Rooftop_Patang_Charkhi"
    )

    # 3. Zone D Grand Bazaar: Mandi Balance Scale with Brass Pans & Iron Weights
    spawn_story_prop(
        "SM_Prop_Bazaar_Tarazu_Scale",
        (180.0, 1720.0, 60.0),
        rot=(0.0, -30.0, 0.0),
        scale=(1.0, 1.0, 1.0),
        label="Story_Bazaar_Tarazu_Scale"
    )

    # 4. Zone D Bazaar Curfew Checkpoint: Imperial Red Pillar Postbox (GR Cypher)
    spawn_story_prop(
        "SM_Prop_Imperial_Postbox_GR",
        (60.0, 2150.0, 10.0),
        rot=(0.0, 180.0, 0.0),
        scale=(1.0, 1.0, 1.0),
        label="Story_Imperial_Postbox_GR"
    )

    # 5. District C School Classroom 4B: Punjab 1919 Province Map Easel & Pointer
    spawn_story_prop(
        "SM_Prop_School_Wall_Map_Easel",
        (1100.0, 1920.0, 10.0),
        rot=(0.0, -45.0, 0.0),
        scale=(1.0, 1.0, 1.0),
        label="Story_School_Wall_Map_Easel"
    )

    # Save Level
    level_editor_sub.save_current_level()
    log("Saved L_Validation_Gym with Pack 2 Story Arrangement!")

if __name__ == "__main__":
    run_arrangement()
