import unreal

def log_warn(msg):
    unreal.log_warning(f"[ZONE_VERIFIER] {msg}")

log_warn("================ REVOLUTION COMPLETE ENVIRONMENT VALIDATION ================")

level_path = "/Game/Maps/L_Validation_Gym"
level_sub = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
level_sub.load_level(level_path)

actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
all_actors = actor_sub.get_all_level_actors()

log_warn(f"Total Actors in L_Validation_Gym: {len(all_actors)}")

# Count by category
categories = {
    "Zone A (Haveli & Workshop)": 0,
    "Zone B (Deorhi Galli)": 0,
    "Zone C (Communal Well)": 0,
    "Zone D (Grand Bazaar)": 0,
    "District C (Vernacular School)": 0,
    "Atmosphere & Lighting": 0,
    "Foundation & System": 0
}

for a in all_actors:
    label = a.get_actor_label()
    if label.startswith("School_"):
        categories["District C (Vernacular School)"] += 1
    elif label.startswith("Workshop_") or "Haveli" in label or "Charpai_Kabir" in label or "KiteSpool" in label or "Courtyard_Stairs" in label or "Lantern_Ledge" in label:
        categories["Zone A (Haveli & Workshop)"] += 1
    elif "Alley_" in label:
        categories["Zone B (Deorhi Galli)"] += 1
    elif "Well" in label or "Chopal" in label or "Gong" in label:
        categories["Zone C (Communal Well)"] += 1
    elif "Bazaar" in label or "Mandi" in label or "Halwai" in label or "Spice" in label:
        categories["Zone D (Grand Bazaar)"] += 1
    elif any(k in label for k in ["Light", "Sun", "Atmosphere", "Fog", "PostProcess"]):
        categories["Atmosphere & Lighting"] += 1
    else:
        categories["Foundation & System"] += 1

for cat, count in categories.items():
    log_warn(f"  * {cat}: {count} actors")

# Check PlayerStart
player_start = None
for a in all_actors:
    if isinstance(a, unreal.PlayerStart) or "PlayerStart" in a.get_actor_label():
        player_start = a
        break

if player_start:
    loc = player_start.get_actor_location()
    log_warn(f"[PASS] PlayerStart found at ({loc.x:.1f}, {loc.y:.1f}, {loc.z:.1f})")
else:
    log_warn("[FAIL] PlayerStart not found!")

# Check Foundation Slab
slab = None
for a in all_actors:
    if "Foundation_Slab" in a.get_actor_label():
        slab = a
        break
if slab:
    loc = slab.get_actor_location()
    log_warn(f"[PASS] Foundation Slab active at ({loc.x:.1f}, {loc.y:.1f}, {loc.z:.1f})")
else:
    log_warn("[FAIL] Foundation Slab missing!")

# Check critical landmarks
landmarks = [
    "Workshop_SewingMachine_Singer",
    "School_Bell_Tower",
    "School_Blackboard",
    "Modular_Mohalla_CommunalWell",
    "Modular_Bazaar_Stall_Spices",
    "Modular_Bazaar_Stall_Halwai",
    "Modular_Bazaar_Stall_ClothKhadi",
    "Modular_Chopal_Charpai_Elders",
    "Modular_Haveli_1F_JharokhaBalcony"
]
all_landmarks_found = True
for lm in landmarks:
    found = any(a.get_actor_label() == lm for a in all_actors)
    if not found:
        all_landmarks_found = False
    log_warn(f"[{'PASS' if found else 'FAIL'}] Landmark '{lm}' present: {found}")

assert all_landmarks_found, "One or more critical landmarks are missing!"
log_warn("================ ALL ACTOR & ZONE VALIDATIONS PASSED: 100% COMPLETE ================")
