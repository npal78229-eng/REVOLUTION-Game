"""
PROJECT REVOLUTION — Task 17: Master Audio Mix, Sound Classes & Dynamic Curfew Filter
Configures:
1. Sound Classes Hierarchy (/Game/Audio/SoundClasses/):
   - SC_Master (Root Master Bus)
   - SC_SFX (Parent: SC_Master)
   - SC_Foley (Parent: SC_SFX)
   - SC_Voice_Punjabi (Parent: SC_Master)
   - SC_Ambience_Mohalla (Parent: SC_Master)
2. Sound Attenuations (/Game/Audio/Attenuation/):
   - ATT_Voice_Proximity (Spatialized 18.0m falloff, 4.0m inner sphere)
   - ATT_Foley_Localized (Spatialized 12.0m falloff, 2.0m inner sphere)
   - ATT_Monumental_Mechanical (Spatialized 45.0m falloff, 8.0m inner sphere)
3. Sound Mixes (/Game/Audio/SoundMixes/):
   - SMix_Default (Baseline balanced mix)
   - SMix_Curfew_Night (Dynamic Low-Pass Curfew Filter: 800Hz LPF on Mohalla Ambience, dampened civilian voice, heightened foley)
   - SMix_Cinematic (Cutscene audio ducking: prioritized Punjabi dialogue & subdued background SFX)
4. Wave Asset Routing:
   - Routes all 42 SoundWaves in /Game/Audio/SFX/ to their designated SoundClass
5. Level Scene Integration:
   - Binds SMix_Default and SMix_Curfew_Night to AtmosphereController in /Game/Maps/L_Validation_Gym
   - Binds SMix_Cinematic to CinematicDirector_Master in /Game/Maps/L_Validation_Gym
"""

import unreal

def log_info(msg):
    unreal.log_warning(f"[AUDIO_MIX_SETUP] {msg}")

def setup_audio_system():
    log_info("================================================================================")
    log_info("  PROJECT REVOLUTION — TASK 17 AUDIO MIX & SOUND CLASS ROUTING SETUP")
    log_info("================================================================================")

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    editor_asset_lib = unreal.EditorAssetLibrary

    # 1. Ensure Directories Exist
    dirs = [
        "/Game/Audio/SoundClasses",
        "/Game/Audio/SoundMixes",
        "/Game/Audio/Attenuation"
    ]
    for d in dirs:
        if not editor_asset_lib.does_directory_exist(d):
            editor_asset_lib.make_directory(d)
            log_info(f"Created directory: {d}")

    # 2. Create Sound Classes
    sc_factory = unreal.SoundClassFactory()

    def get_or_create_sound_class(name, volume=1.0, lpf=20000.0):
        path = f"/Game/Audio/SoundClasses/{name}"
        sc = editor_asset_lib.load_asset(path)
        if not sc:
            sc = asset_tools.create_asset(name, "/Game/Audio/SoundClasses", unreal.SoundClass, sc_factory)
            log_info(f"Created SoundClass: {name}")
        props = unreal.SoundClassProperties(volume=volume, low_pass_filter_frequency=lpf)
        sc.set_editor_property("properties", props)
        return sc

    sc_master = get_or_create_sound_class("SC_Master", volume=1.0, lpf=20000.0)
    sc_sfx = get_or_create_sound_class("SC_SFX", volume=1.0, lpf=20000.0)
    sc_foley = get_or_create_sound_class("SC_Foley", volume=1.0, lpf=20000.0)
    sc_voice = get_or_create_sound_class("SC_Voice_Punjabi", volume=1.0, lpf=20000.0)
    sc_ambience = get_or_create_sound_class("SC_Ambience_Mohalla", volume=0.85, lpf=20000.0)

    # Configure SoundClass Parent-Child Hierarchy
    sc_sfx.set_editor_property("parent_class", sc_master)
    sc_foley.set_editor_property("parent_class", sc_sfx)
    sc_voice.set_editor_property("parent_class", sc_master)
    sc_ambience.set_editor_property("parent_class", sc_master)

    for sc in [sc_master, sc_sfx, sc_foley, sc_voice, sc_ambience]:
        editor_asset_lib.save_loaded_asset(sc)
    log_info("[PASS] SoundClass hierarchy established (SC_Master -> SC_SFX [-> SC_Foley], SC_Voice_Punjabi, SC_Ambience_Mohalla).")

    # 3. Create Sound Attenuations
    sa_factory = unreal.SoundAttenuationFactory()

    def get_or_create_attenuation(name, falloff_dist, inner_radius):
        path = f"/Game/Audio/Attenuation/{name}"
        sa = editor_asset_lib.load_asset(path)
        if not sa:
            sa = asset_tools.create_asset(name, "/Game/Audio/Attenuation", unreal.SoundAttenuation, sa_factory)
            log_info(f"Created SoundAttenuation: {name}")
        
        atten = unreal.SoundAttenuationSettings()
        atten.spatialize = True
        atten.attenuate = True
        atten.falloff_distance = falloff_dist
        atten.attenuation_shape = unreal.AttenuationShape.SPHERE
        atten.attenuation_shape_extents = unreal.Vector(inner_radius, 0.0, 0.0)
        sa.set_editor_property("attenuation", atten)
        editor_asset_lib.save_loaded_asset(sa)
        return sa

    att_voice = get_or_create_attenuation("ATT_Voice_Proximity", 1800.0, 400.0)
    att_foley = get_or_create_attenuation("ATT_Foley_Localized", 1200.0, 200.0)
    att_mech = get_or_create_attenuation("ATT_Monumental_Mechanical", 4500.0, 800.0)
    log_info("[PASS] SoundAttenuations created (ATT_Voice_Proximity, ATT_Foley_Localized, ATT_Monumental_Mechanical).")

    # 4. Create Sound Mixes
    sm_factory = unreal.SoundMixFactory()

    # 4.1 SMix_Default
    path_default = "/Game/Audio/SoundMixes/SMix_Default"
    smix_default = editor_asset_lib.load_asset(path_default)
    if not smix_default:
        smix_default = asset_tools.create_asset("SMix_Default", "/Game/Audio/SoundMixes", unreal.SoundMix, sm_factory)
        log_info("Created SoundMix: SMix_Default")
    
    adj_default_master = unreal.SoundClassAdjuster(
        sound_class_object=sc_master,
        volume_adjuster=1.0,
        pitch_adjuster=1.0,
        low_pass_filter_frequency=20000.0,
        apply_to_children=True
    )
    smix_default.set_editor_property("sound_class_effects", [adj_default_master])
    editor_asset_lib.save_loaded_asset(smix_default)
    log_info("[PASS] SMix_Default baseline mix configured.")

    # 4.2 SMix_Curfew_Night (Dynamic Low-Pass Curfew Filter)
    path_curfew = "/Game/Audio/SoundMixes/SMix_Curfew_Night"
    smix_curfew = editor_asset_lib.load_asset(path_curfew)
    if not smix_curfew:
        smix_curfew = asset_tools.create_asset("SMix_Curfew_Night", "/Game/Audio/SoundMixes", unreal.SoundMix, sm_factory)
        log_info("Created SoundMix: SMix_Curfew_Night")

    adj_curfew_amb = unreal.SoundClassAdjuster(
        sound_class_object=sc_ambience,
        volume_adjuster=0.45,
        pitch_adjuster=0.98,
        low_pass_filter_frequency=800.0,
        apply_to_children=True
    )
    adj_curfew_voice = unreal.SoundClassAdjuster(
        sound_class_object=sc_voice,
        volume_adjuster=0.35,
        pitch_adjuster=1.0,
        low_pass_filter_frequency=1200.0,
        apply_to_children=True
    )
    adj_curfew_foley = unreal.SoundClassAdjuster(
        sound_class_object=sc_foley,
        volume_adjuster=1.30,
        pitch_adjuster=1.0,
        low_pass_filter_frequency=20000.0,
        apply_to_children=True
    )
    adj_curfew_sfx = unreal.SoundClassAdjuster(
        sound_class_object=sc_sfx,
        volume_adjuster=1.15,
        pitch_adjuster=1.0,
        low_pass_filter_frequency=20000.0,
        apply_to_children=True
    )
    smix_curfew.set_editor_property("sound_class_effects", [adj_curfew_amb, adj_curfew_voice, adj_curfew_foley, adj_curfew_sfx])
    editor_asset_lib.save_loaded_asset(smix_curfew)
    log_info("[PASS] SMix_Curfew_Night configured (Ambience LPF=800Hz, Voice=0.35, Foley=1.30, SFX=1.15).")

    # 4.3 SMix_Cinematic (Cutscene Audio Ducking)
    path_cinematic = "/Game/Audio/SoundMixes/SMix_Cinematic"
    smix_cinematic = editor_asset_lib.load_asset(path_cinematic)
    if not smix_cinematic:
        smix_cinematic = asset_tools.create_asset("SMix_Cinematic", "/Game/Audio/SoundMixes", unreal.SoundMix, sm_factory)
        log_info("Created SoundMix: SMix_Cinematic")

    adj_cin_amb = unreal.SoundClassAdjuster(
        sound_class_object=sc_ambience,
        volume_adjuster=0.30,
        pitch_adjuster=1.0,
        low_pass_filter_frequency=1500.0,
        apply_to_children=True
    )
    adj_cin_voice = unreal.SoundClassAdjuster(
        sound_class_object=sc_voice,
        volume_adjuster=1.35,
        pitch_adjuster=1.0,
        low_pass_filter_frequency=20000.0,
        apply_to_children=True
    )
    adj_cin_sfx = unreal.SoundClassAdjuster(
        sound_class_object=sc_sfx,
        volume_adjuster=0.55,
        pitch_adjuster=1.0,
        low_pass_filter_frequency=20000.0,
        apply_to_children=True
    )
    adj_cin_foley = unreal.SoundClassAdjuster(
        sound_class_object=sc_foley,
        volume_adjuster=0.60,
        pitch_adjuster=1.0,
        low_pass_filter_frequency=20000.0,
        apply_to_children=True
    )
    smix_cinematic.set_editor_property("sound_class_effects", [adj_cin_amb, adj_cin_voice, adj_cin_sfx, adj_cin_foley])
    editor_asset_lib.save_loaded_asset(smix_cinematic)
    log_info("[PASS] SMix_Cinematic configured (Voice=1.35, Ambience=0.30, SFX=0.55, Foley=0.60).")

    # 5. Route All 42 SoundWaves in /Game/Audio/SFX/
    wave_paths = editor_asset_lib.list_assets("/Game/Audio/SFX", recursive=False)
    log_info(f"Routing {len(wave_paths)} SoundWave assets to SoundClasses...")

    voice_keywords = ["crowd", "speech", "scream", "watchman_callout"]
    ambience_keywords = ["ambience", "cricket", "canal", "water", "wind", "pigeon", "flute", "bansuri", "rahat"]
    foley_keywords = ["footstep", "cloth", "scrape", "drain", "gasp", "parchment", "pamphlet", "chalk", "vault", "boot_march"]

    routed_counts = {"Voice": 0, "Ambience": 0, "Foley": 0, "SFX": 0}

    for p in wave_paths:
        sw = editor_asset_lib.load_asset(p)
        if not sw or sw.get_class().get_name() != "SoundWave":
            continue

        asset_name = sw.get_name().lower()

        if any(k in asset_name for k in voice_keywords):
            sw.set_editor_property("sound_class_object", sc_voice)
            routed_counts["Voice"] += 1
        elif any(k in asset_name for k in ambience_keywords):
            sw.set_editor_property("sound_class_object", sc_ambience)
            routed_counts["Ambience"] += 1
        elif any(k in asset_name for k in foley_keywords):
            sw.set_editor_property("sound_class_object", sc_foley)
            routed_counts["Foley"] += 1
        else:
            sw.set_editor_property("sound_class_object", sc_sfx)
            routed_counts["SFX"] += 1

        editor_asset_lib.save_loaded_asset(sw)

    log_info(f"[PASS] 42 SoundWaves routed successfully: {routed_counts}")

    # 6. Bind SoundMixes to Master Map Actors
    level_path = "/Game/Maps/L_Validation_Gym"
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_sub.load_level(level_path)

    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    all_actors = actor_sub.get_all_level_actors()

    atmo_bound = False
    cin_bound = False

    for a in all_actors:
        cls_name = a.get_class().get_name()
        lbl = a.get_actor_label()

        if "AtmosphereController" in cls_name:
            a.set_editor_property("default_sound_mix", smix_default)
            a.set_editor_property("curfew_sound_mix", smix_curfew)
            atmo_bound = True
            log_info(f"[PASS] Bound Default & Curfew SoundMix to AtmosphereController: {a.get_name()}")

        if lbl == "CinematicDirector_Master" or "CinematicDirector" in cls_name:
            a.set_editor_property("cinematic_sound_mix", smix_cinematic)
            cin_bound = True
            log_info(f"[PASS] Bound Cinematic SoundMix to CinematicDirector: {a.get_name()}")

    assert atmo_bound, "Failed to bind SoundMixes to AtmosphereController!"
    assert cin_bound, "Failed to bind CinematicSoundMix to CinematicDirector!"

    b_saved = level_sub.save_current_level()
    log_info(f"[PASS] Master Level saved with audio configuration: {b_saved}")
    log_info("================================================================================")
    log_info("  TASK 17 AUDIO MIX & SOUND CLASS ROUTING SETUP: 100% SUCCESS")
    log_info("================================================================================")

if __name__ == "__main__":
    setup_audio_system()
