"""
PROJECT REVOLUTION — Task 39 Scene Assembly:
Act IV Potter's Courtyard & Canal Bypass Encounter (Upper Bari Doab Canal Basti)
Assembles:
1. NPC_Kumhar_Rahim (Village Potter, ACivilianNPCActor, Cluster_UBDC_CanalBasti)
2. Door_CanalBypass_Gate (Aqueduct Bypass Wicket, ADoorDeorhiActor, Cluster_UBDC_CanalBasti)
3. Hazard_Terracotta_PotterYard (Brittle drying earthenware, ATerracottaHazardActor)
4. Artisan Courtyard Dressing (Charpai rope bed, jute clay sacks, chulha stove, hurricane lantern)
5. Warm period amber lighting (Light_Potter_Courtyard)
"""

import unreal

def assemble_potter_courtyard():
    unreal.log_warning("=== REVOLUTION: Assembling Act IV Potter's Courtyard & Community Trust Encounter ===")

    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)

    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    existing_actors = {a.get_actor_label(): a for a in actor_sub.get_all_level_actors()}

    cluster_id = unreal.Name("Cluster_UBDC_CanalBasti")

    # 1. Spawn or Update NPC_Kumhar_Rahim
    civ_class = unreal.load_class(None, "/Script/REVOLUTION.CivilianNPCActor")
    assert civ_class is not None, "CivilianNPCActor class missing!"

    rahim_label = "NPC_Kumhar_Rahim"
    rahim_loc = unreal.Vector(-1020.0, 2180.0, 0.0)
    rahim_rot = unreal.Rotator(0.0, -45.0, 0.0)

    if rahim_label in existing_actors:
        npc_rahim = existing_actors[rahim_label]
        npc_rahim.set_actor_location(rahim_loc, False, True)
        npc_rahim.set_actor_rotation(rahim_rot, True)
        unreal.log_warning(f"Updated existing NPC: {rahim_label}")
    else:
        npc_rahim = actor_sub.spawn_actor_from_class(civ_class, rahim_loc, rahim_rot)
        npc_rahim.set_actor_label(rahim_label)
        existing_actors[rahim_label] = npc_rahim
        unreal.log_warning(f"Spawned new NPC: {rahim_label}")

    npc_rahim.set_editor_property("community_cluster_id", cluster_id)
    npc_rahim.configure_occupation(unreal.CivilianOccupation.BHISHTI_WATER_CARRIER)
    npc_rahim.set_editor_property("civilian_name", unreal.Text("Kumhar Rahim"))
    npc_rahim.set_editor_property("profession_title", unreal.Text("Village Potter (Kumhar)"))
    npc_rahim.set_editor_property(
        "historical_lore",
        unreal.Text(
            "An artisan whose family has turned terracotta clay on the Upper Bari Doab Canal for generations. "
            "Under April 1919 martial law, the colonial administration has threatened collective punishment against any agrarian "
            "village that harbors anti-Rowlatt couriers. Rahim wishes Kabir well in his heart, but fears for his children's lives."
        )
    )

    potter_voice = unreal.load_asset("/Game/Audio/Voice/SFX_Voice_Doabi_KumharPotter_Bark")
    if potter_voice:
        npc_rahim.set_editor_property("interaction_voice_sound", potter_voice)
        npc_rahim.set_editor_property("ambient_bark_voice_sound", potter_voice)
        unreal.log_warning("Bound SFX_Voice_Doabi_KumharPotter_Bark to NPC_Kumhar_Rahim")

    # 2. Spawn or Update Door_CanalBypass_Gate
    door_class = unreal.load_class(None, "/Script/REVOLUTION.DoorDeorhiActor")
    assert door_class is not None, "DoorDeorhiActor class missing!"

    gate_label = "Door_CanalBypass_Gate"
    gate_loc = unreal.Vector(-980.0, 2220.0, 0.0)
    gate_rot = unreal.Rotator(0.0, 90.0, 0.0)

    if gate_label in existing_actors:
        door_gate = existing_actors[gate_label]
        door_gate.set_actor_location(gate_loc, False, True)
        door_gate.set_actor_rotation(gate_rot, True)
        unreal.log_warning(f"Updated existing Door: {gate_label}")
    else:
        door_gate = actor_sub.spawn_actor_from_class(door_class, gate_loc, gate_rot)
        door_gate.set_actor_label(gate_label)
        existing_actors[gate_label] = door_gate
        unreal.log_warning(f"Spawned new Door: {gate_label}")

    door_gate.set_editor_property("community_cluster_id", cluster_id)
    door_gate.set_editor_property("door_name", unreal.Text("Canal Aqueduct Bypass Wicket"))

    # 3. Spawn or Update Hazard_Terracotta_PotterYard
    hazard_class = unreal.load_class(None, "/Script/REVOLUTION.TerracottaHazardActor")
    assert hazard_class is not None, "TerracottaHazardActor class missing!"

    hazard_label = "Hazard_Terracotta_PotterYard"
    hazard_loc = unreal.Vector(-1040.0, 2150.0, 15.0)
    hazard_rot = unreal.Rotator(0.0, 0.0, 0.0)

    if hazard_label in existing_actors:
        hazard_act = existing_actors[hazard_label]
        hazard_act.set_actor_location(hazard_loc, False, True)
        unreal.log_warning(f"Updated existing Hazard: {hazard_label}")
    else:
        hazard_act = actor_sub.spawn_actor_from_class(hazard_class, hazard_loc, hazard_rot)
        hazard_act.set_actor_label(hazard_label)
        existing_actors[hazard_label] = hazard_act
        unreal.log_warning(f"Spawned new Hazard: {hazard_label}")

    hazard_act.set_editor_property("community_cluster_id", cluster_id)
    hazard_act.set_editor_property("hazard_name", unreal.Text("Drying Terracotta Water Pots (Matka & Kulhad)"))
    hazard_act.set_editor_property("trust_penalty_on_crunch", -20)

    # 4. Spawn or Update Restitution_Drop_PotterBench
    restitution_class = unreal.load_class(None, "/Script/REVOLUTION.RestitutionDropActor")
    assert restitution_class is not None, "RestitutionDropActor class missing!"

    restitution_label = "Restitution_Drop_PotterBench"
    restitution_loc = unreal.Vector(-1030.0, 2190.0, 35.0)
    restitution_rot = unreal.Rotator(0.0, 0.0, 0.0)

    if restitution_label in existing_actors:
        rest_act = existing_actors[restitution_label]
        rest_act.set_actor_location(restitution_loc, False, True)
        unreal.log_warning(f"Updated existing Restitution Actor: {restitution_label}")
    else:
        rest_act = actor_sub.spawn_actor_from_class(restitution_class, restitution_loc, restitution_rot)
        rest_act.set_actor_label(restitution_label)
        existing_actors[restitution_label] = rest_act
        unreal.log_warning(f"Spawned new Restitution Actor: {restitution_label}")

    rest_act.set_editor_property("community_cluster_id", cluster_id)
    rest_act.set_editor_property("restitution_trust_bonus", 35)

    # 5. Courtyard Dressing Props
    mesh_charpai = unreal.load_asset("/Game/Environment/Mohalla/Meshes/SM_Prop_Charpai_RopeBed")
    mesh_sacks = unreal.load_asset("/Game/Environment/Mohalla/Meshes/SM_Prop_GrainSack_Jute_01")
    mesh_chulha = unreal.load_asset("/Game/Environment/Mohalla/Meshes/SM_Prop_Courtyard_Chulha_Stove")
    mesh_mashk = unreal.load_asset("/Game/Environment/Mohalla/Meshes/SM_Prop_Bhishti_Mashk")
    mesh_lantern = unreal.load_asset("/Game/Environment/Mohalla/Meshes/SM_Prop_HurricaneLantern")
    mat_brass = unreal.load_asset("/Game/Environment/Mohalla/Materials/MI_HammeredBrass_Photogrammetry")

    def spawn_or_update_mesh(label, mesh, loc, rot=unreal.Rotator(0,0,0), scale=unreal.Vector(1,1,1), mat=None):
        if label in existing_actors:
            act = existing_actors[label]
            act.set_actor_location(loc, False, True)
            act.set_actor_rotation(rot, True)
            act.set_actor_scale3d(scale)
            unreal.log_warning(f"Updated prop: {label}")
        else:
            act = actor_sub.spawn_actor_from_class(unreal.StaticMeshActor, loc, rot)
            act.set_actor_label(label)
            act.set_actor_scale3d(scale)
            existing_actors[label] = act
            unreal.log_warning(f"Spawned prop: {label}")

        sm_comp = act.get_component_by_class(unreal.StaticMeshComponent)
        if sm_comp and mesh:
            sm_comp.set_static_mesh(mesh)
            if mat:
                sm_comp.set_material(0, mat)
        return act

    # Potter's Charpai Rope Bed
    spawn_or_update_mesh(
        "Prop_Potter_Charpai",
        mesh_charpai,
        unreal.Vector(-1060.0, 2210.0, 0.0),
        unreal.Rotator(0.0, 15.0, 0.0),
        unreal.Vector(1.0, 1.0, 1.0)
    )

    # Clay & Sediment Jute Sacks
    spawn_or_update_mesh(
        "Prop_Potter_ClaySacks",
        mesh_sacks,
        unreal.Vector(-1005.0, 2190.0, 0.0),
        unreal.Rotator(0.0, -30.0, 0.0),
        unreal.Vector(1.1, 1.1, 1.1)
    )

    # Courtyard Terracotta Firing Chulha
    spawn_or_update_mesh(
        "Prop_Potter_EarthenStove",
        mesh_chulha,
        unreal.Vector(-1045.0, 2220.0, 0.0),
        unreal.Rotator(0.0, 45.0, 0.0),
        unreal.Vector(1.0, 1.0, 1.0)
    )

    # Water Carrier Leather Mashk (for moistening clay)
    spawn_or_update_mesh(
        "Prop_Potter_WaterMashk",
        mesh_mashk,
        unreal.Vector(-1015.0, 2170.0, 0.0),
        unreal.Rotator(0.0, 60.0, 0.0),
        unreal.Vector(1.0, 1.0, 1.0)
    )

    # Hurricane Lantern on timber post
    spawn_or_update_mesh(
        "Prop_Potter_Courtyard_Lantern",
        mesh_lantern,
        unreal.Vector(-1020.0, 2180.0, 75.0),
        unreal.Rotator(0.0, 0.0, 0.0),
        unreal.Vector(0.85, 0.85, 0.85),
        mat_brass
    )

    # Warm amber courtyard point light
    def spawn_or_update_point_light(label, loc, color, intensity, radius):
        if label in existing_actors:
            act = existing_actors[label]
            act.set_actor_location(loc, False, True)
            unreal.log_warning(f"Updated light: {label}")
        else:
            act = actor_sub.spawn_actor_from_class(unreal.PointLight, loc, unreal.Rotator(0,0,0))
            act.set_actor_label(label)
            existing_actors[label] = act
            unreal.log_warning(f"Spawned light: {label}")

        light_comp = act.get_component_by_class(unreal.PointLightComponent)
        if light_comp:
            light_comp.set_editor_property("light_color", color)
            light_comp.set_editor_property("intensity", intensity)
            light_comp.set_editor_property("attenuation_radius", radius)
            light_comp.set_editor_property("cast_shadows", True)
        return act

    spawn_or_update_point_light(
        "Light_Potter_Courtyard",
        unreal.Vector(-1020.0, 2180.0, 105.0),
        unreal.Color(255, 175, 90, 255),
        1100.0,
        350.0
    )

    # 5. Save Level Package
    level_sub.save_current_level()
    unreal.log_warning("=== Potter's Courtyard Scene Successfully Assembled and Level Saved! ===")

if __name__ == "__main__":
    assemble_potter_courtyard()
