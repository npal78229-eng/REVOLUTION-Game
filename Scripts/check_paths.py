import unreal

def check_paths():
    assets = [
        "/Game/Environment/Mohalla/Meshes/SM_British_Armored_Car_Obstacle",
        "/Game/Environment/Mohalla/Meshes/SM_Jallianwala_Raised_Bank",
        "/Game/Environment/Mohalla/Meshes/SM_Jallianwala_Crumbling_Wall_Breach",
        "/Game/Environment/Mohalla/Meshes/SM_Prop_Bullet_Pocked_Brick_Slab",
        "/Game/Environment/Mohalla/Meshes/SM_Prop_Fallen_Turban_Shoes_Scatter",
        "/Game/VFX/Smoke/Materials/MI_Smoke_Gunpowder_Muzzle",
        "/Game/VFX/Smoke/Materials/M_RDR2_Pyroclastic_Smoke",
        "/Game/Audio/SFX/SFX_Bugle_Call_Charge",
        "/Game/Audio/SFX/SFX_Crowd_Panic_Scream"
    ]
    for p in assets:
        a = unreal.load_asset(p)
        unreal.log_warning(f"Path {p}: {'LOADED OK' if a else 'FAILED'}")

if __name__ == "__main__":
    check_paths()
