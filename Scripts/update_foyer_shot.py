with open(r"C:\Users\npal7\PROJECT\REVOLUTION\Project\Source\REVOLUTION\RevolutionCharacter.cpp", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Include PointLightComponent
inc_target = '#include "Components/SkeletalMeshComponent.h"\n'
inc_repl = '#include "Components/SkeletalMeshComponent.h"\n#include "Components/PointLightComponent.h"\n'
if '#include "Components/PointLightComponent.h"' not in code:
    assert inc_target in code, "inc_target not found"
    code = code.replace(inc_target, inc_repl)

# 2. Update QAShotTimer
shot_target = """\t\t\t\tFTimerHandle QAShotTimer;
\t\t\t\tWorld->GetTimerManager().SetTimer(QAShotTimer, [this]()
\t\t\t\t{
\t\t\t\t\t// Bathe world in bright 28-lux Punjab Baisakhi festival midday spring sunlight
\t\t\t\t\tfor (TActorIterator<ARevolutionAtmosphereController> It(GetWorld()); It; ++It)
\t\t\t\t\t{
\t\t\t\t\t\tIt->SetAtmospherePhase(EHistoricalAtmospherePhase::BaisakhiMidday, 0.0f);
\t\t\t\t\t}

\t\t\t\t\t// Position Kabir on open sunlit rooftop terrace facing camera (same verified open vista as P3_02)
\t\t\t\t\tSetActorLocation(FVector(360.0f, 220.0f, 475.0f), false, nullptr, ETeleportType::TeleportPhysics);
\t\t\t\t\tSetActorRotation(FRotator(0.0f, -115.0f, 0.0f), ETeleportType::TeleportPhysics);
\t\t\t\t\tif (APlayerController* PC = Cast<APlayerController>(GetController()))
\t\t\t\t\t{
\t\t\t\t\t\tPC->SetControlRotation(FRotator(2.0f, 65.0f, 0.0f));
\t\t\t\t\t}
\t\t\t\t\tif (CameraBoom)
\t\t\t\t\t{
\t\t\t\t\t\tCameraBoom->bDoCollisionTest = false;
\t\t\t\t\t\tCameraBoom->TargetArmLength = 190.0f;
\t\t\t\t\t\tCameraBoom->SocketOffset = FVector(0.0f, 20.0f, 25.0f);
\t\t\t\t\t}"""

shot_repl = """\t\t\t\tFTimerHandle QAShotTimer;
\t\t\t\tWorld->GetTimerManager().SetTimer(QAShotTimer, [this]()
\t\t\t\t{
\t\t\t\t\t// Position Kabir in Haveli foyer facing the camera
\t\t\t\t\tSetActorLocation(FVector(0.0f, 220.0f, 75.0f), false, nullptr, ETeleportType::TeleportPhysics);
\t\t\t\t\tSetActorRotation(FRotator(0.0f, -90.0f, 0.0f), ETeleportType::TeleportPhysics);
\t\t\t\t\tif (APlayerController* PC = Cast<APlayerController>(GetController()))
\t\t\t\t\t{
\t\t\t\t\t\tPC->SetControlRotation(FRotator(-4.0f, 90.0f, 0.0f));
\t\t\t\t\t}
\t\t\t\t\tif (CameraBoom)
\t\t\t\t\t{
\t\t\t\t\t\tCameraBoom->bDoCollisionTest = false;
\t\t\t\t\t\tCameraBoom->TargetArmLength = 180.0f;
\t\t\t\t\t\tCameraBoom->SocketOffset = FVector(0.0f, 0.0f, 25.0f);
\t\t\t\t\t}

\t\t\t\t\t// Hero fill light for clear material & posture inspection
\t\t\t\t\tif (UPointLightComponent* HeroLight = NewObject<UPointLightComponent>(this, TEXT("QA_HeroLight")))
\t\t\t\t\t{
\t\t\t\t\t\tHeroLight->RegisterComponentWithWorld(GetWorld());
\t\t\t\t\t\tHeroLight->SetWorldLocation(FVector(0.0f, 100.0f, 140.0f));
\t\t\t\t\t\tHeroLight->SetIntensity(12000.0f);
\t\t\t\t\t\tHeroLight->SetLightColor(FLinearColor(1.0f, 0.94f, 0.85f, 1.0f));
\t\t\t\t\t\tHeroLight->SetAttenuationRadius(800.0f);
\t\t\t\t\t}"""

assert shot_target in code, "shot_target not found"
code = code.replace(shot_target, shot_repl)

with open(r"C:\Users\npal7\PROJECT\REVOLUTION\Project\Source\REVOLUTION\RevolutionCharacter.cpp", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated RevolutionCharacter.cpp with foyer hero shot and point light!")
