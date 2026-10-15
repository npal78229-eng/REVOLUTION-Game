import unreal

def log(msg):
    unreal.log_warning(f"[CHECK_HOME_ACTORS] {msg}")

level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
level_sub.load_level("/Game/Maps/L_Mohalla_Home")

actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
all_actors = actor_sub.get_all_level_actors()

required_npcs = [
    "NPC_RamLubhaya_Father",
    "NPC_GhasitaBhishti_Water",
    "NPC_HiraHalwai_Chai",
    "NPC_LalaKaramChand_Cloth",
    "NPC_PanditKashiRam_Headmaster",
    "NPC_KartarSingh_Friend",
    "NPC_Constable_Gurdial"
]

missing_npcs = []
for npc in required_npcs:
    found = any(a.get_actor_label() == npc for a in all_actors)
    log(f"NPC '{npc}': {'FOUND' if found else 'MISSING'}")
    if not found:
        missing_npcs.append(npc)

required_landmarks = [
    "Workshop_SewingMachine_Singer",
    "Foliage_PeepalTree_Shrine",
    "Prop_Tulsi_Pedestal",
    "Prop_ClothRolls_Manchester",
    "School_Bell_Tower",
    "School_Blackboard",
    "Story_Courtyard_Chulha_Stove",
    "Story_School_Takhti_Slate",
    "Story_Rooftop_Pigeon_Coop",
    "Story_Bazaar_Cart_Thela",
    "Story_Peepal_Pamphlet_Stack",
    "Story_Litho_Pamphlet_Stack",
    "Story_Haveli_Grain_Sandook",
    "Story_Rooftop_Patang_Charkhi",
    "Story_Bazaar_Tarazu_Scale",
    "Story_Imperial_Postbox_GR",
    "Story_School_Wall_Map_Easel",
    "Arch_Monumental_Chowk_Gate",
    "Arch_Overhead_Kucha_HaveliExit",
    "Street_Lamp_Post_BazaarChowk",
    "Bazaar_Canopy_Khadi_NorthWest",
    "Street_Drain_Gutter_DeorhiWest",
    "Town_Faseel_NorthWall_West",
    "Checkpoint_Picket_Barrier_NorthGate",
    "Haveli_Facade_3Story_BazaarWest",
    "Story_Litho_Press_Flatbed_Vault",
    "SupplyStash_Litho_Press",
    "Mohalla_Pyaoo_Water_Shelter_Chowk"
]

missing_lms = []
for lm in required_landmarks:
    found = any(a.get_actor_label() == lm for a in all_actors)
    log(f"Landmark '{lm}': {'FOUND' if found else 'MISSING'}")
    if not found:
        missing_lms.append(lm)

log(f"Summary in L_Mohalla_Home: Missing NPCs={len(missing_npcs)}, Missing Landmarks={len(missing_lms)}")
