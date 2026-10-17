"""
PROJECT REVOLUTION — Task 21: Assemble Civilian Voice Audio on Level Actors
Binds the localized Punjabi voice sound assets and attenuation settings
to all 6 Civilian NPCs and the Curfew Patrol AI / Constable in /Game/Maps/L_Validation_Gym.
"""

import unreal

def log_warn(msg):
    unreal.log_warning(f"[VOICE_ASSEMBLER] {msg}")

def main():
    log_warn("================================================================================")
    log_warn("  PROJECT REVOLUTION — TASK 21 LEVEL ACTOR VOICE AUDIO BINDING")
    log_warn("================================================================================")

    editor_asset_lib = unreal.EditorAssetLibrary
    level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    map_path = "/Game/Maps/L_Validation_Gym"
    log_warn(f"Loading map: {map_path}...")
    level_sub.load_level(map_path)

    att_voice = editor_asset_lib.load_asset("/Game/Audio/Attenuation/ATT_Voice_Proximity")
    assert att_voice is not None, "Failed to load ATT_Voice_Proximity!"

    # Voice mappings for civilian archetypes (enum int or name)
    voice_map = {
        0: { # FatherTailor
            "dialogue": "/Game/Audio/Voice/SFX_Voice_RamLubhaya_Dialogue",
            "bark": "/Game/Audio/Voice/SFX_Voice_RamLubhaya_Bark"
        },
        1: { # HalwaiChaiVendor
            "dialogue": "/Game/Audio/Voice/SFX_Voice_HiraHalwai_Dialogue",
            "bark": "/Game/Audio/Voice/SFX_Voice_HiraHalwai_Bark"
        },
        2: { # BhishtiWaterCarrier
            "dialogue": "/Game/Audio/Voice/SFX_Voice_Ghasita_Dialogue",
            "bark": "/Game/Audio/Voice/SFX_Voice_Ghasita_Bark"
        },
        3: { # SchoolHeadmaster
            "dialogue": "/Game/Audio/Voice/SFX_Voice_PanditKashiRam_Dialogue",
            "bark": "/Game/Audio/Voice/SFX_Voice_PanditKashiRam_Bark"
        },
        4: { # ClothMerchant
            "dialogue": "/Game/Audio/Voice/SFX_Voice_LalaKaramChand_Dialogue",
            "bark": "/Game/Audio/Voice/SFX_Voice_LalaKaramChand_Bark"
        },
        5: { # SchoolFriendKartar
            "dialogue": "/Game/Audio/Voice/SFX_Voice_KartarSingh_Dialogue",
            "bark": "/Game/Audio/Voice/SFX_Voice_KartarSingh_Bark"
        }
    }

    all_actors = actor_sub.get_all_level_actors()
    civilian_count = 0
    patrol_count = 0

    constable_curfew = editor_asset_lib.load_asset("/Game/Audio/Voice/SFX_Voice_ConstableGurdial_Curfew")
    constable_suspicion = editor_asset_lib.load_asset("/Game/Audio/Voice/SFX_Voice_ConstableGurdial_Suspicion")

    for actor in all_actors:
        cname = actor.get_class().get_name()

        if cname == "CivilianNPCActor":
            occ = actor.get_editor_property("occupation")
            # Enum can be int or Enum object
            occ_idx = occ if isinstance(occ, int) else occ.value if hasattr(occ, "value") else int(occ)
            
            cfg = voice_map.get(occ_idx)
            if cfg:
                dlg_asset = editor_asset_lib.load_asset(cfg["dialogue"])
                bark_asset = editor_asset_lib.load_asset(cfg["bark"])
                
                actor.set_editor_property("interaction_voice_sound", dlg_asset)
                actor.set_editor_property("ambient_bark_voice_sound", bark_asset)
                actor.set_editor_property("voice_attenuation", att_voice)
                
                actor_label = actor.get_actor_label()
                civilian_name = str(actor.get_editor_property("civilian_name"))
                log_warn(f"[BOUND CIVILIAN] '{actor_label}' ({civilian_name}) -> Dialogue: {cfg['dialogue']}, Bark: {cfg['bark']}")
                civilian_count += 1

        elif cname == "CurfewPatrolAI":
            actor.set_editor_property("curfew_voice_proclamation_sound", constable_curfew)
            actor.set_editor_property("suspicious_voice_sound", constable_suspicion)
            actor.set_editor_property("voice_attenuation", att_voice)
            
            actor_label = actor.get_actor_label()
            log_warn(f"[BOUND PATROL] '{actor_label}' -> Curfew Proclamation & Suspicion voice tracks")
            patrol_count += 1

    log_warn(f"Total bound: {civilian_count} civilian NPCs, {patrol_count} curfew patrol sentries.")
    assert civilian_count >= 6, f"Expected at least 6 civilian NPCs, found {civilian_count}!"
    assert patrol_count >= 1, f"Expected at least 1 curfew patrol sentry, found {patrol_count}!"

    # Save level map
    saved = level_sub.save_current_level()
    log_warn(f"Level map saved successfully: {saved}")

if __name__ == "__main__":
    main()
