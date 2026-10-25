with open(r"C:\Users\npal7\PROJECT\REVOLUTION\Project\Source\REVOLUTION\RevolutionCharacter.cpp", "r", encoding="utf-8") as f:
    code = f.read()

target = """\t\t\t\tFTimerHandle QAShotTimer;
\t\t\t\tWorld->GetTimerManager().SetTimer(QAShotTimer, [this]()
\t\t\t\t{
\t\t\t\t\t// Position Kabir in open sunlit courtyard facing the camera
\t\t\t\t\tSetActorLocation(FVector(360.0f, -20.0f, 90.0f), false, nullptr, ETeleportType::TeleportPhysics);
\t\t\t\t\tSetActorRotation(FRotator(0.0f, 0.0f, 0.0f), ETeleportType::TeleportPhysics);
\t\t\t\t\tif (APlayerController* PC = Cast<APlayerController>(GetController()))
\t\t\t\t\t{
\t\t\t\t\t\tPC->SetControlRotation(FRotator(-6.0f, 175.0f, 0.0f));
\t\t\t\t\t}
\t\t\t\t\tif (CameraBoom)
\t\t\t\t\t{
\t\t\t\t\t\tCameraBoom->bDoCollisionTest = false;
\t\t\t\t\t\tCameraBoom->TargetArmLength = 220.0f;
\t\t\t\t\t\tCameraBoom->SocketOffset = FVector(0.0f, 25.0f, 25.0f);
\t\t\t\t\t}"""

replacement = """\t\t\t\tFTimerHandle QAShotTimer;
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

assert target in code, "target not found"
code = code.replace(target, replacement)

with open(r"C:\Users\npal7\PROJECT\REVOLUTION\Project\Source\REVOLUTION\RevolutionCharacter.cpp", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated QAShotTimer with sunlit rooftop position!")
