with open(r"C:\Users\npal7\PROJECT\REVOLUTION\Project\Source\REVOLUTION\RevolutionCharacter.cpp", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add header include
include_target = '#include "LadderActor.h"\n'
include_replacement = '#include "LadderActor.h"\n#include "RevolutionAtmosphereController.h"\n'
if '#include "RevolutionAtmosphereController.h"' not in code:
    assert include_target in code, "include_target not found"
    code = code.replace(include_target, include_replacement)

# 2. Update QAShotTimer
shot_target = """\t\t\t\tFTimerHandle QAShotTimer;
\t\t\t\tWorld->GetTimerManager().SetTimer(QAShotTimer, [this]()
\t\t\t\t{
\t\t\t\t\t// Position Kabir on open sunlit rooftop terrace in full Punjab daylight
\t\t\t\t\tSetActorLocation(FVector(360.0f, 220.0f, 485.0f), false, nullptr, ETeleportType::TeleportPhysics);
\t\t\t\t\tSetActorRotation(FRotator(0.0f, 90.0f, 0.0f), ETeleportType::TeleportPhysics);
\t\t\t\t\tif (APlayerController* PC = Cast<APlayerController>(GetController()))
\t\t\t\t\t{
\t\t\t\t\t\tPC->SetControlRotation(FRotator(-4.0f, -80.0f, 0.0f));
\t\t\t\t\t}
\t\t\t\t\tif (CameraBoom)
\t\t\t\t\t{
\t\t\t\t\t\tCameraBoom->bDoCollisionTest = false;
\t\t\t\t\t\tCameraBoom->TargetArmLength = 210.0f;
\t\t\t\t\t\tCameraBoom->SocketOffset = FVector(0.0f, 25.0f, 25.0f);
\t\t\t\t\t}"""

shot_replacement = """\t\t\t\tFTimerHandle QAShotTimer;
\t\t\t\tWorld->GetTimerManager().SetTimer(QAShotTimer, [this]()
\t\t\t\t{
\t\t\t\t\t// Bathe world in bright 28-lux Punjab Baisakhi festival midday spring sunlight
\t\t\t\t\tfor (TActorIterator<ARevolutionAtmosphereController> It(GetWorld()); It; ++It)
\t\t\t\t\t{
\t\t\t\t\t\tIt->SetAtmospherePhase(EHistoricalAtmospherePhase::BaisakhiMidday, 0.0f);
\t\t\t\t\t}

\t\t\t\t\t// Position Kabir on open sunlit rooftop terrace in full Punjab daylight
\t\t\t\t\tSetActorLocation(FVector(360.0f, 220.0f, 485.0f), false, nullptr, ETeleportType::TeleportPhysics);
\t\t\t\t\tSetActorRotation(FRotator(0.0f, -90.0f, 0.0f), ETeleportType::TeleportPhysics);
\t\t\t\t\tif (APlayerController* PC = Cast<APlayerController>(GetController()))
\t\t\t\t\t{
\t\t\t\t\t\tPC->SetControlRotation(FRotator(-6.0f, 80.0f, 0.0f));
\t\t\t\t\t}
\t\t\t\t\tif (CameraBoom)
\t\t\t\t\t{
\t\t\t\t\t\tCameraBoom->bDoCollisionTest = false;
\t\t\t\t\t\tCameraBoom->TargetArmLength = 190.0f;
\t\t\t\t\t\tCameraBoom->SocketOffset = FVector(0.0f, 20.0f, 20.0f);
\t\t\t\t\t}"""

assert shot_target in code, "shot_target not found"
code = code.replace(shot_target, shot_replacement)

with open(r"C:\Users\npal7\PROJECT\REVOLUTION\Project\Source\REVOLUTION\RevolutionCharacter.cpp", "w", encoding="utf-8") as f:
    f.write(code)

print("RevolutionCharacter.cpp successfully updated with BaisakhiMidday sunlight!")
