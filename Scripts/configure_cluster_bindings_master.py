"""
PROJECT REVOLUTION — Task 39 Multi-District Cluster Architecture:
Assigns authentic canonical cluster IDs across all historical districts in L_Validation_Gym:
1. Cluster_KotGurdarshan_Bazaar:
   - Ram Lubhaya (Father, Haveli Courtyard)
   - Ghasita Bhishti (Communal Well)
   - Hira Halwai (Tea Stall)
   - Lala Karam Chand (Cloth Mandi)
   - Pandit Kashi Ram (School Headmaster)
   - Kartar Singh (Schoolmate Friend)
   - Munadi Town Crier & Bhai Sant Singh (Grand Bazaar Chowk)
   - Clinic Volunteer Elder (Medical Clinic)
   - Baisakhi Pilgrims & Fair Vendors
2. Cluster_Bhatta_BrickKiln:
   - Resistance Courier Liaison (Bull's Trench Kiln)
3. Cluster_UBDC_CanalBasti:
   - Kumhar Rahim (Potter's Courtyard)
   - Canal Bypass Gate, Terracotta Hazard, Restitution Bench
"""

import unreal

def configure_clusters():
    unreal.log_warning("=== REVOLUTION: Configuring Multi-District Community Trust Clusters ===")

    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)

    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    civ_class = unreal.load_class(None, "/Script/REVOLUTION.CivilianNPCActor")

    cluster_bazaar = unreal.Name("Cluster_KotGurdarshan_Bazaar")
    cluster_kiln = unreal.Name("Cluster_Bhatta_BrickKiln")
    cluster_canal = unreal.Name("Cluster_UBDC_CanalBasti")

    bazaar_labels = [
        "NPC_RamLubhaya_Father",
        "NPC_GhasitaBhishti_Water",
        "NPC_HiraHalwai_Chai",
        "NPC_LalaKaramChand_Cloth",
        "NPC_PanditKashiRam_Headmaster",
        "NPC_KartarSingh_Friend",
        "NPC_Munadi_TownCrier",
        "NPC_BhaiSantSingh_Elder",
        "NPC_BaisakhiPilgrim_Gurmukh",
        "NPC_FairVendor_Milkha",
        "NPC_Clinic_Volunteer_Elder"
    ]

    kiln_labels = [
        "NPC_Resistance_Courier_Liaison"
    ]

    canal_labels = [
        "NPC_Kumhar_Rahim"
    ]

    updated_count = 0
    for a in actor_sub.get_all_level_actors():
        if a.get_class() == civ_class:
            label = a.get_actor_label()
            if label in bazaar_labels:
                a.set_editor_property("community_cluster_id", cluster_bazaar)
                updated_count += 1
                unreal.log_warning(f"Bound '{label}' -> {cluster_bazaar}")
            elif label in kiln_labels:
                a.set_editor_property("community_cluster_id", cluster_kiln)
                updated_count += 1
                unreal.log_warning(f"Bound '{label}' -> {cluster_kiln}")
            elif label in canal_labels:
                a.set_editor_property("community_cluster_id", cluster_canal)
                updated_count += 1
                unreal.log_warning(f"Bound '{label}' -> {cluster_canal}")

    # Save level
    b_saved = level_sub.save_current_level()
    unreal.log_warning(f"Successfully configured {updated_count} civilian NPC cluster bindings. Level saved: {b_saved}")

if __name__ == "__main__":
    configure_clusters()
