import unreal

def check_assets():
    armored_car = unreal.load_asset("/Game/Environment/Mohalla/Meshes/SM_British_Armored_Car_Obstacle")
    raised_bank = unreal.load_asset("/Game/Environment/Mohalla/Meshes/SM_Jallianwala_Raised_Bank")
    breach = unreal.load_asset("/Game/Environment/Mohalla/Meshes/SM_Jallianwala_Crumbling_Wall_Breach")
    bullet_wall = unreal.load_asset("/Game/Environment/Mohalla/Meshes/SM_Prop_Bullet_Pocked_Brick_Slab")
    scatter = unreal.load_asset("/Game/Environment/Mohalla/Meshes/SM_Prop_Fallen_Turban_Shoes_Scatter")
    
    print("SM_British_Armored_Car_Obstacle:", armored_car is not None)
    print("SM_Jallianwala_Raised_Bank:", raised_bank is not None)
    print("SM_Jallianwala_Crumbling_Wall_Breach:", breach is not None)
    print("SM_Prop_Bullet_Pocked_Brick_Slab:", bullet_wall is not None)
    print("SM_Prop_Fallen_Turban_Shoes_Scatter:", scatter is not None)
    
    mat_muzzle = unreal.load_asset("/Game/VFX/Smoke/Materials/MI_Smoke_Gunpowder_Muzzle")
    print("MI_Smoke_Gunpowder_Muzzle:", mat_muzzle is not None)
    
    bugle_sound = unreal.load_asset("/Game/Audio/SFX/SFX_Bugle_Call_Charge")
    panic_sound = unreal.load_asset("/Game/Audio/SFX/SFX_Crowd_Panic_Scream")
    print("SFX_Bugle_Call_Charge:", bugle_sound is not None)
    print("SFX_Crowd_Panic_Scream:", panic_sound is not None)

if __name__ == "__main__":
    check_assets()
