"""
PROJECT REVOLUTION — Level Assembler for Task 26: Multi-Dialect Bazaar Crowd Walla
Places 4 authentic ARevolutionBazaarWallaActor instances into L_Validation_Gym.umap
representing Majhi and Doabi street vendors and hawkers.
"""

import unreal

def log_arranger(msg):
    unreal.log_warning(f"[BAZAAR_WALLA_ASSEMBLER] {msg}")

def run_arrangement():
    log_arranger("================================================================================")
    log_arranger("  PROJECT REVOLUTION — TASK 26 BAZAAR WALLA SCENE ASSEMBLY")
    log_arranger("================================================================================")

    level_editor_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    editor_actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    editor_asset_lib = unreal.EditorAssetLibrary

    level_path = "/Game/Maps/L_Validation_Gym"
    level_editor_sub.load_level(level_path)

    # 1. Load C++ class
    walla_class = unreal.load_class(None, "/Script/REVOLUTION.RevolutionBazaarWallaActor")
    assert walla_class is not None, "ERROR: Could not load ARevolutionBazaarWallaActor class!"

    # 2. Load attenuation
    att_voice = editor_asset_lib.load_asset("/Game/Audio/Attenuation/ATT_Voice_Proximity")
    assert att_voice is not None, "ERROR: Could not load ATT_Voice_Proximity!"

    # Clean existing walla actors if re-run
    walla_labels = [
        "BazaarWalla_Majhi_Sabzi",
        "BazaarWalla_Doabi_Kulfi",
        "BazaarWalla_Majhi_Hawker",
        "BazaarWalla_Doabi_Mazdoor"
    ]
    for a in editor_actor_sub.get_all_level_actors():
        if a.get_actor_label() in walla_labels:
            editor_actor_sub.destroy_actor(a)
            log_arranger(f"Cleaned existing actor: {a.get_actor_label()}")

    vendors = [
        {
            "label": "BazaarWalla_Majhi_Sabzi",
            "loc": unreal.Vector(50.0, 1550.0, 88.0),
            "rot": unreal.Rotator(0.0, 45.0, 0.0),
            "title": "Sabzi-Walla (Majhi Vegetable Vendor)",
            "phrase": "Taaza saag te gobi lai lo ji! Majhe da taaza saal!",
            "translation": "Buy fresh greens and cauliflower! Fresh from the Majha soil!",
            "sound": "/Game/Audio/Voice/SFX_Voice_Majhi_SabziWalla_Bark",
            "dialect": 0 # Majhi
        },
        {
            "label": "BazaarWalla_Doabi_Kulfi",
            "loc": unreal.Vector(-150.0, 1850.0, 88.0),
            "rot": unreal.Rotator(0.0, 135.0, 0.0),
            "title": "Kulfi-Walla (Doabi Sweet Vendor)",
            "phrase": "Thandi kulfi pista-badam! Aao bai kulfi khao!",
            "translation": "Cold pistachio and almond kulfi! Come, children, taste the sweet cream!",
            "sound": "/Game/Audio/Voice/SFX_Voice_Doabi_KulfiWalla_Bark",
            "dialect": 1 # Doabi
        },
        {
            "label": "BazaarWalla_Majhi_Hawker",
            "loc": unreal.Vector(250.0, 2100.0, 88.0),
            "rot": unreal.Rotator(0.0, 90.0, 0.0),
            "title": "Patrika Hawker (Majhi Gazette Seller)",
            "phrase": "Waqt di aawaz! Akhbar padho! Rowlatt Act di khabar!",
            "translation": "The voice of the times! Read the gazette! Breaking news on the Rowlatt Act!",
            "sound": "/Game/Audio/Voice/SFX_Voice_Majhi_PatrikaHawker_Bark",
            "dialect": 0 # Majhi
        },
        {
            "label": "BazaarWalla_Doabi_Mazdoor",
            "loc": unreal.Vector(-50.0, 1200.0, 88.0),
            "rot": unreal.Rotator(0.0, 0.0, 0.0),
            "title": "Quli Mazdoor (Doabi Heavy Porter)",
            "phrase": "Bacha ke ji bacha ke! Bhari gathri hai, raah chaddo!",
            "translation": "Watch out, please! Heavy load on my head, clear the way!",
            "sound": "/Game/Audio/Voice/SFX_Voice_Doabi_MazdoorPorter_Bark",
            "dialect": 1 # Doabi
        }
    ]

    for v in vendors:
        actor = editor_actor_sub.spawn_actor_from_class(walla_class, v["loc"], v["rot"])
        assert actor is not None, f"Failed to spawn actor: {v['label']}"
        actor.set_actor_label(v["label"])

        sound_asset = editor_asset_lib.load_asset(v["sound"])
        assert sound_asset is not None, f"Failed to load SoundWave: {v['sound']}"

        actor.set_editor_property("vendor_title", unreal.Text(v["title"]))
        actor.set_editor_property("punjabi_phrase", unreal.Text(v["phrase"]))
        actor.set_editor_property("english_translation", unreal.Text(v["translation"]))
        actor.set_editor_property("primary_walla_sound", sound_asset)
        actor.set_editor_property("voice_attenuation", att_voice)
        if hasattr(unreal, "PunjabiDialect"):
            dialect_val = unreal.PunjabiDialect.MAJHI if v["dialect"] == 0 else unreal.PunjabiDialect.DOABI
            actor.set_editor_property("dialect", dialect_val)

        log_arranger(f"  [SPAWNED & CONFIGURED] {v['label']} at {v['loc']}")

    level_editor_sub.save_current_level()
    all_actors = editor_actor_sub.get_all_level_actors()
    log_arranger(f"[PASS] Successfully assembled 4 Bazaar Walla actors. Total level actors: {len(all_actors)}")
    return True

if __name__ == "__main__":
    run_arrangement()
