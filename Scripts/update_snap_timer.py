with open(r"C:\Users\npal7\PROJECT\REVOLUTION\Project\Source\REVOLUTION\RevolutionCharacter.cpp", "r", encoding="utf-8") as f:
    code = f.read()

target = """\t\t\t\t\tFTimerHandle DelayedSnapTimer;
\t\t\t\t\tif (UWorld* SnapWorld = GetWorld())
\t\t\t\t\t{
\t\t\t\t\t\tSnapWorld->GetTimerManager().SetTimer(DelayedSnapTimer, []()
\t\t\t\t\t\t{
\t\t\t\t\t\t\tconst FString ScreenshotPath = TEXT("C:/Users/npal7/PROJECT/REVOLUTION/Tests/Screenshots/P1_01_InEngine_PlayableKabir.png");
\t\t\t\t\t\t\tFScreenshotRequest::RequestScreenshot(ScreenshotPath, true, false);
\t\t\t\t\t\t\tUE_LOG(LogREVOLUTION, Warning, TEXT("[QA_INSPECTION] FScreenshotRequest::RequestScreenshot triggered: %s"), *ScreenshotPath);
\t\t\t\t\t\t}, 0.5f, false);
\t\t\t\t\t}"""

replacement = """\t\t\t\t\tFTimerHandle DelayedSnapTimer;
\t\t\t\t\tif (UWorld* SnapWorld = GetWorld())
\t\t\t\t\t{
\t\t\t\t\t\tSnapWorld->GetTimerManager().SetTimer(DelayedSnapTimer, [SnapWorld]()
\t\t\t\t\t\t{
\t\t\t\t\t\t\tconst FString ScreenshotPath = TEXT("C:/Users/npal7/PROJECT/REVOLUTION/Tests/Screenshots/P1_01_InEngine_PlayableKabir.png");
\t\t\t\t\t\t\tFScreenshotRequest::RequestScreenshot(ScreenshotPath, true, false);
\t\t\t\t\t\t\tif (GEngine)
\t\t\t\t\t\t\t{
\t\t\t\t\t\t\t\tGEngine->Exec(SnapWorld, TEXT("shot"));
\t\t\t\t\t\t\t}
\t\t\t\t\t\t\tFFileHelper::SaveStringToFile(TEXT("TRIGGERED"), *(FPaths::ProjectDir() / TEXT("Tests/P1_SHOT_TRIGGERED.txt")));
\t\t\t\t\t\t\tUE_LOG(LogREVOLUTION, Warning, TEXT("[QA_INSPECTION] FScreenshotRequest::RequestScreenshot triggered: %s"), *ScreenshotPath);
\t\t\t\t\t\t}, 0.5f, false);
\t\t\t\t\t}"""

assert target in code, "target block not found in code"
code = code.replace(target, replacement)

with open(r"C:\Users\npal7\PROJECT\REVOLUTION\Project\Source\REVOLUTION\RevolutionCharacter.cpp", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated DelayedSnapTimer in RevolutionCharacter.cpp")
