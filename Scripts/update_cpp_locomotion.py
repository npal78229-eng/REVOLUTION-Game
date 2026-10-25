with open(r"C:\Users\npal7\PROJECT\REVOLUTION\Project\Source\REVOLUTION\RevolutionCharacter.cpp", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update material paths & unconditional assignment
old_mat_block = """\t\tstatic const TCHAR* V05MaterialPaths[] = {
\t\t\tTEXT("/Game/Characters/Kabir_v05/M_Kabir_Skin_PBR.M_Kabir_Skin_PBR"),
\t\t\tTEXT("/Game/Characters/Kabir_v05/M_Kabir_Eye_PBR.M_Kabir_Eye_PBR"),
\t\t\tTEXT("/Game/Characters/Kabir_v05/M_Hair.M_Hair"),
\t\t\tTEXT("/Game/Characters/Kabir_v05/M_Kabir_Khadi_PBR.M_Kabir_Khadi_PBR"),
\t\t\tTEXT("/Game/Characters/Kabir_v05/M_Kabir_Leather_PBR.M_Kabir_Leather_PBR")
\t\t};

\t\tfor (int32 MatIdx = 0; MatIdx < UE_ARRAY_COUNT(V05MaterialPaths); ++MatIdx)
\t\t{
\t\t\tif (GetMesh()->GetMaterial(MatIdx) == nullptr)
\t\t\t{
\t\t\t\tif (UMaterialInterface* Mat = LoadObject<UMaterialInterface>(nullptr, V05MaterialPaths[MatIdx]))
\t\t\t\t{
\t\t\t\t\tGetMesh()->SetMaterial(MatIdx, Mat);
\t\t\t\t\tUE_LOG(LogREVOLUTION, Display, TEXT("[KabirMaterials] Fallback applied slot %d: %s"), MatIdx, *Mat->GetName());
\t\t\t\t}
\t\t\t\telse
\t\t\t\t{
\t\t\t\t\tUE_LOG(LogREVOLUTION, Warning, TEXT("[KabirMaterials] Failed to load slot %d: %s"), MatIdx, V05MaterialPaths[MatIdx]);
\t\t\t\t}
\t\t\t}
\t\t}"""

new_mat_block = """\t\tstatic const TCHAR* V05MaterialPaths[] = {
\t\t\tTEXT("/Game/Characters/Kabir_v05/Materials/M_Kabir_Skin_Clean.M_Kabir_Skin_Clean"),
\t\t\tTEXT("/Game/Characters/Kabir_v05/Materials/M_Kabir_Eye_Clean.M_Kabir_Eye_Clean"),
\t\t\tTEXT("/Game/Characters/Kabir_v05/Materials/M_Kabir_Hair_Clean.M_Kabir_Hair_Clean"),
\t\t\tTEXT("/Game/Characters/Kabir_v05/Materials/M_Kabir_Khadi_Clean.M_Kabir_Khadi_Clean"),
\t\t\tTEXT("/Game/Characters/Kabir_v05/M_Kabir_Leather_PBR.M_Kabir_Leather_PBR")
\t\t};

\t\tfor (int32 MatIdx = 0; MatIdx < UE_ARRAY_COUNT(V05MaterialPaths); ++MatIdx)
\t\t{
\t\t\tif (UMaterialInterface* Mat = LoadObject<UMaterialInterface>(nullptr, V05MaterialPaths[MatIdx]))
\t\t\t{
\t\t\t\tGetMesh()->SetMaterial(MatIdx, Mat);
\t\t\t\tUE_LOG(LogREVOLUTION, Display, TEXT("[KabirMaterials] Applied clean PBR slot %d: %s"), MatIdx, *Mat->GetName());
\t\t\t}
\t\t\telse
\t\t\t{
\t\t\t\tUE_LOG(LogREVOLUTION, Warning, TEXT("[KabirMaterials] Failed to load slot %d: %s"), MatIdx, V05MaterialPaths[MatIdx]);
\t\t\t}
\t\t}"""

assert old_mat_block in code, "old_mat_block not found in code"
code = code.replace(old_mat_block, new_mat_block)

# 2. Update locomotion state machine with RDR2 stop momentum settle
old_anim_block = """\t// Native locomotion animation state switching for Kabir v05
\tif (USkeletalMeshComponent* MeshComp = GetMesh())
\t{
\t\tif (MeshComp->GetAnimationMode() == EAnimationMode::AnimationSingleNode)
\t\t{
\t\t\tconst float CurrentSpeed = GetVelocity().Size2D();
\t\t\tstatic UAnimSequence* CachedIdle = nullptr;
\t\t\tstatic UAnimSequence* CachedWalk = nullptr;
\t\t\tstatic UAnimSequence* CachedRun = nullptr;
\t\t\tif (!CachedIdle) CachedIdle = LoadObject<UAnimSequence>(nullptr, TEXT("/Game/Characters/Kabir_v05/Animations/Anim_Kabir_v05_Idle.Anim_Kabir_v05_Idle"));
\t\t\tif (!CachedWalk) CachedWalk = LoadObject<UAnimSequence>(nullptr, TEXT("/Game/Characters/Kabir_v05/Animations/Anim_Kabir_v05_Walk.Anim_Kabir_v05_Walk"));
\t\t\tif (!CachedRun) CachedRun = LoadObject<UAnimSequence>(nullptr, TEXT("/Game/Characters/Kabir_v05/Animations/Anim_Kabir_v05_Run.Anim_Kabir_v05_Run"));

\t\t\tUAnimSequence* TargetAnim = CachedIdle;
\t\t\tif (CurrentSpeed >= 240.0f && CachedRun)
\t\t\t{
\t\t\t\tTargetAnim = CachedRun;
\t\t\t}
\t\t\telse if (CurrentSpeed >= 15.0f && CachedWalk)
\t\t\t{
\t\t\t\tTargetAnim = CachedWalk;
\t\t\t}

\t\t\tstatic UAnimSequence* CurrentActiveAnim = nullptr;
\t\t\tif (TargetAnim && CurrentActiveAnim != TargetAnim)
\t\t\t{
\t\t\t\tCurrentActiveAnim = TargetAnim;
\t\t\t\tMeshComp->PlayAnimation(TargetAnim, true);
\t\t\t}
\t\t}
\t}"""

new_anim_block = """\t// Native locomotion animation state switching for Kabir v05 (RDR2 locomotion mechanics)
\tif (USkeletalMeshComponent* MeshComp = GetMesh())
\t{
\t\tif (MeshComp->GetAnimationMode() == EAnimationMode::AnimationSingleNode)
\t\t{
\t\t\tconst float CurrentSpeed = GetVelocity().Size2D();
\t\t\tstatic UAnimSequence* CachedIdle = nullptr;
\t\t\tstatic UAnimSequence* CachedWalk = nullptr;
\t\t\tstatic UAnimSequence* CachedRun = nullptr;
\t\t\tstatic UAnimSequence* CachedStop = nullptr;
\t\t\tif (!CachedIdle) CachedIdle = LoadObject<UAnimSequence>(nullptr, TEXT("/Game/Characters/Kabir_v05/Animations/Anim_Kabir_v05_Idle.Anim_Kabir_v05_Idle"));
\t\t\tif (!CachedWalk) CachedWalk = LoadObject<UAnimSequence>(nullptr, TEXT("/Game/Characters/Kabir_v05/Animations/Anim_Kabir_v05_Walk.Anim_Kabir_v05_Walk"));
\t\t\tif (!CachedRun) CachedRun = LoadObject<UAnimSequence>(nullptr, TEXT("/Game/Characters/Kabir_v05/Animations/Anim_Kabir_v05_Run.Anim_Kabir_v05_Run"));
\t\t\tif (!CachedStop) CachedStop = LoadObject<UAnimSequence>(nullptr, TEXT("/Game/Characters/Kabir_v05/Animations/Anim_Kabir_v05_Stop.Anim_Kabir_v05_Stop"));

\t\t\tstatic float StopRemainingTime = 0.0f;
\t\t\tstatic float PreviousSpeed = 0.0f;
\t\t\tstatic UAnimSequence* CurrentActiveAnim = nullptr;

\t\t\tUAnimSequence* TargetAnim = nullptr;
\t\t\tbool bLoop = true;

\t\t\tif (CurrentSpeed >= 240.0f && CachedRun)
\t\t\t{
\t\t\t\tTargetAnim = CachedRun;
\t\t\t\tbLoop = true;
\t\t\t\tStopRemainingTime = 0.0f;
\t\t\t}
\t\t\telse if (CurrentSpeed >= 15.0f && CachedWalk)
\t\t\t{
\t\t\t\tTargetAnim = CachedWalk;
\t\t\t\tbLoop = true;
\t\t\t\tStopRemainingTime = 0.0f;
\t\t\t}
\t\t\telse
\t\t\t{
\t\t\t\t// Speed < 15.0f: Check if we just stopped from locomotion (RDR2 momentum deceleration settle)
\t\t\t\tif (PreviousSpeed >= 35.0f && CachedStop && StopRemainingTime <= 0.0f && CurrentActiveAnim != CachedStop)
\t\t\t\t{
\t\t\t\t\tTargetAnim = CachedStop;
\t\t\t\t\tbLoop = false;
\t\t\t\t\tStopRemainingTime = 0.53f;
\t\t\t\t}
\t\t\t\telse if (StopRemainingTime > 0.0f)
\t\t\t\t{
\t\t\t\t\tStopRemainingTime -= DeltaTime;
\t\t\t\t\tif (StopRemainingTime <= 0.0f)
\t\t\t\t\t{
\t\t\t\t\t\tTargetAnim = CachedIdle;
\t\t\t\t\t\tbLoop = true;
\t\t\t\t\t}
\t\t\t\t}
\t\t\t\telse
\t\t\t\t{
\t\t\t\t\tTargetAnim = CachedIdle;
\t\t\t\t\tbLoop = true;
\t\t\t\t}
\t\t\t}

\t\t\tPreviousSpeed = CurrentSpeed;

\t\t\tif (TargetAnim && CurrentActiveAnim != TargetAnim)
\t\t\t{
\t\t\t\tCurrentActiveAnim = TargetAnim;
\t\t\t\tMeshComp->PlayAnimation(TargetAnim, bLoop);
\t\t\t}
\t\t}
\t}"""

assert old_anim_block in code, "old_anim_block not found in code"
code = code.replace(old_anim_block, new_anim_block)

with open(r"C:\Users\npal7\PROJECT\REVOLUTION\Project\Source\REVOLUTION\RevolutionCharacter.cpp", "w", encoding="utf-8") as f:
    f.write(code)

print("RevolutionCharacter.cpp successfully updated with clean materials and RDR2 locomotion logic!")
