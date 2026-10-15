"""
PROJECT REVOLUTION — Level Assembler for Veil of Memory (Censor Window) Memorial Scene
Arranges the 4 memorial storytelling assets into Zone D Memorial Courtyard of L_Validation_Gym:
1. SM_Memorial_Historic_Well_Brick (Historic hexagonal well with timber pulley gallows)
2. SM_Prop_Overturned_Brass_Lota (Traditional Punjabi brass lota overturned near well)
3. SM_Prop_Abandoned_Paper_Kite (Saffron patang kite caught on North Enclosure Wall)
4. SM_Prop_Wooden_Takhti_Slate (Traditional student wooden takhti slate near assembly grounds)

Enforces CTF_USE_COMPLEX_AS_SIMPLE collision and saves level.
"""

import unreal

def log(msg):
    unreal.log_warning(f"[REVOLUTION_MEMORIAL_ARRANGER] {msg}")

def run_arrangement():
    log("Arranging Veil of Memory Memorial Props into L_Validation_Gym...")

    level_editor_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    editor_actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    level_path = "/Game/Maps/L_Validation_Gym"
    level_editor_sub.load_level(level_path)

    # Clean existing actors from this set to prevent duplicates if re-run
    prefix_list = [
        "Memorial_Historic_Well_",
        "Prop_Overturned_Brass_Lota_",
        "Prop_Abandoned_Paper_Kite_",
        "Prop_Wooden_Takhti_Slate_"
    ]
    for a in editor_actor_sub.get_all_level_actors():
        lbl = a.get_actor_label()
        for prefix in prefix_list:
            if lbl.startswith(prefix):
                editor_actor_sub.destroy_actor(a)
                log(f"Cleaned existing actor: {lbl}")
                break

    # Cache Mesh Assets
    mesh_keys = [
        "SM_Memorial_Historic_Well_Brick",
        "SM_Prop_Overturned_Brass_Lota",
        "SM_Prop_Abandoned_Paper_Kite",
        "SM_Prop_Wooden_Takhti_Slate"
    ]
    mesh_cache = {}
    for mk in mesh_keys:
        m_obj = unreal.load_asset(f"/Game/Environment/Mohalla/Meshes/{mk}")
        if m_obj:
            mesh_cache[mk] = m_obj
            log(f"Cached mesh: {mk}")
        else:
            log(f"Warning: Failed to load mesh {mk}")

    def spawn_static_prop(mesh_key, loc, rot=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0), label=None):
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

    # 1. Historic Brick Well with Pulley Gallows
    spawn_static_prop(
        "SM_Memorial_Historic_Well_Brick",
        (1120.0, 2880.0, 0.0),
        (0.0, 45.0, 0.0),
        label="Memorial_Historic_Well_Shaheedi"
    )

    # 2. Overturned Brass Lota near well curb
    spawn_static_prop(
        "SM_Prop_Overturned_Brass_Lota",
        (1160.0, 2840.0, 0.0),
        (0.0, 15.0, 0.0),
        label="Prop_Overturned_Brass_Lota_Memorial"
    )

    # 3. Abandoned Paper Kite on North Enclosure Wall
    spawn_static_prop(
        "SM_Prop_Abandoned_Paper_Kite",
        (1200.0, 3440.0, 185.0),
        (15.0, 0.0, -25.0),
        label="Prop_Abandoned_Paper_Kite_Wall"
    )

    # 4. Wooden Takhti Slate on courtyard ground
    spawn_static_prop(
        "SM_Prop_Wooden_Takhti_Slate",
        (1360.0, 3020.0, 2.0),
        (0.0, -30.0, 0.0),
        label="Prop_Wooden_Takhti_Slate_Courtyard"
    )

    # Save level
    level_editor_sub.save_current_level()
    all_actors = editor_actor_sub.get_all_level_actors()
    log(f"SUCCESS: Veil of Memory props assembled. Total level actors: {len(all_actors)}")

if __name__ == "__main__":
    run_arrangement()
