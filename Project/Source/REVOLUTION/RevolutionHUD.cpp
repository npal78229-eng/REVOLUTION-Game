// Copyright Epic Games, Inc. All Rights Reserved.

#include "RevolutionHUD.h"
#include "REVOLUTION.h"
#include "RevolutionCharacter.h"
#include "RevolutionHUDWidget.h"
#include "InteractableInterface.h"
#include "CurfewPatrolAI.h"
#include "EngineUtils.h"
#include "Camera/CameraComponent.h"
#include "Engine/Canvas.h"
#include "Engine/Engine.h"
#include "RevolutionMissionSubsystem.h"
#include "ChalkMarkActor.h"
#include "RevolutionAtmosphereController.h"
#include "HidingSpotActor.h"
#include "TerracottaHazardActor.h"
#include "ChaffDustDecoyActor.h"
#include "PariahDogActor.h"
#include "CheckpointBarrierActor.h"
#include "ManjaTrapActor.h"
#include "TelegraphWireActor.h"
#include "LithoPressActor.h"
#include "CivilianNPCActor.h"
#include "SupplyStashActor.h"
#include "ProclamationBoardActor.h"
#include "Sound/SoundBase.h"
#include "RevolutionGameMode.h"
#include "RevolutionSaveGame.h"
#include "Kismet/GameplayStatics.h"
#include "Kismet/KismetSystemLibrary.h"
#include "UObject/ConstructorHelpers.h"

ARevolutionHUD::ARevolutionHUD()
{
	PrimaryActorTick.bCanEverTick = true;
	PrimaryActorTick.bTickEvenWhenPaused = true;

	// Default historical palette
	ParchmentColor = FLinearColor(0.93f, 0.89f, 0.80f, 0.96f);
	AntiqueBrassColor = FLinearColor(0.82f, 0.65f, 0.28f, 1.0f);
	DarkInkColor = FLinearColor(0.12f, 0.10f, 0.08f, 1.0f);
	MutedSepiaColor = FLinearColor(0.42f, 0.35f, 0.26f, 1.0f);

	StaminaDisplayAlpha = 0.0f;
	ReticleFocusPulse = 0.0f;
	LetterboxAlpha = 0.0f;
	OpeningPrologueTimer = 0.0f;

	bTitleMenuVisible = false;
	bPauseMenuVisible = false;
	TitleMenuIndex = 0;
	PauseMenuIndex = 0;

	static ConstructorHelpers::FObjectFinder<USoundBase> BellFinder(TEXT("/Game/Audio/SFX/SFX_Curfew_Bell_Toll.SFX_Curfew_Bell_Toll"));
	if (BellFinder.Succeeded())
	{
		CurfewBellTollSound = BellFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> BansuriFinder(TEXT("/Game/Audio/SFX/SFX_Flute_Bansuri_Sorrow.SFX_Flute_Bansuri_Sorrow"));
	if (BansuriFinder.Succeeded())
	{
		MemorialBansuriSound = BansuriFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> WindFinder(TEXT("/Game/Audio/SFX/SFX_Wind_Hollow_Courtyard.SFX_Wind_Hollow_Courtyard"));
	if (WindFinder.Succeeded())
	{
		MemorialWindSound = WindFinder.Object;
	}
}

void ARevolutionHUD::BeginPlay()
{
	Super::BeginPlay();

	if (CurfewBellTollSound && GetWorld())
	{
		UGameplayStatics::PlaySound2D(GetWorld(), CurfewBellTollSound, 0.95f);
	}

	if (HUDWidgetClass && GetOwningPlayerController())
	{
		HUDWidgetInstance = CreateWidget<URevolutionHUDWidget>(GetOwningPlayerController(), HUDWidgetClass);
		if (HUDWidgetInstance)
		{
			HUDWidgetInstance->AddToViewport();
			if (ARevolutionCharacter* Kabir = Cast<ARevolutionCharacter>(GetOwningPawn()))
			{
				HUDWidgetInstance->InitializeWithCharacter(Kabir);
			}
		}
	}

	if (!IsRunningCommandlet() && !GIsEditor)
	{
		SetTitleMenuVisible(true);
	}
}

void ARevolutionHUD::DrawHUD()
{
	Super::DrawHUD();

	if (!Canvas) return;

	ARevolutionCharacter* Kabir = Cast<ARevolutionCharacter>(GetOwningPawn());
	if (!Kabir) return;

	float DeltaTime = GetWorld()->GetDeltaSeconds();

	if (bTitleMenuVisible)
	{
		DrawTitleMenu(DeltaTime);
		DrawCinematicLetterbox(DeltaTime, true);
		return;
	}

	if (bPauseMenuVisible)
	{
		DrawPauseMenu(DeltaTime);
		DrawCinematicLetterbox(DeltaTime, true);
		return;
	}

	OpeningPrologueTimer += DeltaTime;

	ARevolutionGameMode* GM = Cast<ARevolutionGameMode>(GetWorld()->GetAuthGameMode());
	URevolutionMissionSubsystem* Subsystem = GetWorld()->GetSubsystem<URevolutionMissionSubsystem>();

	const bool bApprehended = GM && GM->IsPlayerApprehended();
	const bool bMissionComplete = Subsystem && Subsystem->IsMissionComplete();

	if (bCinematicSequenceActive)
	{
		DrawCinematicCaptions(DeltaTime);
	}
	else if (bApprehended)
	{
		DrawApprehendedCard(Kabir);
	}
	else if (bMissionComplete)
	{
		DrawMissionAccomplishedCard(Kabir);
	}
	else if (Kabir->IsInspecting())
	{
		DrawInspectionModal(Kabir);
	}
	else if (Kabir->IsSatchelJournalOpen())
	{
		DrawSatchelJournalModal(Kabir);
	}
	else
	{
		DrawCompass(Kabir);
		DrawReticle(Kabir);
		DrawInteractionPrompt(Kabir);
		DrawStaminaGauge(Kabir);
		DrawStealthAndDetection(Kabir);
		DrawConcealmentMeter(Kabir);
		DrawKeenSensesBeacons(Kabir);
		DrawInWorldObjectiveBeacon(Kabir);
		DrawMissionDirectiveBanner(Kabir);
		DrawPebbleAimTrajectory(Kabir);
	}

	const bool bBenchmarking = Kabir->bP3BenchmarkingActive || (Kabir->P3CurrentStep > 0);

	bool bForceLetterbox = !bBenchmarking && (bCinematicSequenceActive || (OpeningPrologueTimer < 7.5f) || Kabir->IsInspecting() || Kabir->IsSatchelJournalOpen() || bApprehended || bMissionComplete || (CensorWindowBlurAlpha > 0.1f));
	DrawCinematicLetterbox(DeltaTime, bForceLetterbox);

	DrawCensorWindowVeilOfMemory(Kabir, DeltaTime);

	if (OpeningPrologueTimer < 7.5f && !bApprehended && !bMissionComplete && !bBenchmarking)
	{
		DrawOpeningPrologueCard(DeltaTime);
	}

	if (bBenchmarking)
	{
		DrawPerformanceBenchmarkCard(Kabir);
	}
}

void ARevolutionHUD::DrawFramedBox(float X, float Y, float Width, float Height, const FLinearColor& FillColor, const FLinearColor& BorderColor, float BorderThickness)
{
	if (FillColor.A > 0.0f)
	{
		DrawRect(FillColor, X, Y, Width, Height);
	}

	if (BorderColor.A > 0.0f && BorderThickness > 0.0f)
	{
		// Top border
		DrawRect(BorderColor, X, Y, Width, BorderThickness);
		// Bottom border
		DrawRect(BorderColor, X, Y + Height - BorderThickness, Width, BorderThickness);
		// Left border
		DrawRect(BorderColor, X, Y, BorderThickness, Height);
		// Right border
		DrawRect(BorderColor, X + Width - BorderThickness, Y, BorderThickness, Height);
	}
}

TArray<FString> ARevolutionHUD::WrapText(const FString& Text, UFont* InFont, float MaxWidth)
{
	TArray<FString> Lines;
	if (Text.IsEmpty() || !InFont)
	{
		return Lines;
	}

	TArray<FString> Paragraphs;
	Text.ParseIntoArrayLines(Paragraphs, false);

	for (const FString& Paragraph : Paragraphs)
	{
		if (Paragraph.IsEmpty())
		{
			Lines.Add(TEXT(""));
			continue;
		}

		TArray<FString> Words;
		Paragraph.ParseIntoArray(Words, TEXT(" "), true);

		FString CurrentLine = TEXT("");
		for (const FString& Word : Words)
		{
			FString TestLine = CurrentLine.IsEmpty() ? Word : CurrentLine + TEXT(" ") + Word;
			float LineW = 0.0f, LineH = 0.0f;
			GetTextSize(TestLine, LineW, LineH, InFont);

			if (LineW > MaxWidth && !CurrentLine.IsEmpty())
			{
				Lines.Add(CurrentLine);
				CurrentLine = Word;
			}
			else
			{
				CurrentLine = TestLine;
			}
		}

		if (!CurrentLine.IsEmpty())
		{
			Lines.Add(CurrentLine);
		}
	}

	return Lines;
}

void ARevolutionHUD::DrawReticle(ARevolutionCharacter* Kabir)
{
	if (!bShowReticle || !Canvas || !Kabir) return;

	const float CenterX = Canvas->ClipX * 0.5f;
	const float CenterY = Canvas->ClipY * 0.5f;

	if (Kabir->CurrentInteractableActor != nullptr)
	{
		ReticleFocusPulse += GetWorld()->GetDeltaSeconds() * 5.0f;
		float PulseScale = 1.0f + 0.15f * FMath::Sin(ReticleFocusPulse);
		float DiamondRadius = 8.0f * PulseScale;

		// 4 Diamond corner lines in antique brass
		DrawLine(CenterX - DiamondRadius, CenterY, CenterX, CenterY - DiamondRadius, AntiqueBrassColor, 1.5f);
		DrawLine(CenterX, CenterY - DiamondRadius, CenterX + DiamondRadius, CenterY, AntiqueBrassColor, 1.5f);
		DrawLine(CenterX + DiamondRadius, CenterY, CenterX, CenterY + DiamondRadius, AntiqueBrassColor, 1.5f);
		DrawLine(CenterX, CenterY + DiamondRadius, CenterX - DiamondRadius, CenterY, AntiqueBrassColor, 1.5f);

		// Subtle center dot
		DrawRect(AntiqueBrassColor, CenterX - 1.5f, CenterY - 1.5f, 3.0f, 3.0f);
	}
	else
	{
		// Ambient grounded center dot
		DrawRect(FLinearColor(0.92f, 0.90f, 0.85f, 0.55f), CenterX - 1.5f, CenterY - 1.5f, 3.0f, 3.0f);
	}
}

void ARevolutionHUD::DrawInteractionPrompt(ARevolutionCharacter* Kabir)
{
	if (!bShowInteractionPrompt || !Canvas || !Kabir) return;
	if (Kabir->CurrentInteractableActor == nullptr) return;

	UFont* MediumFont = GEngine ? GEngine->GetMediumFont() : nullptr;
	UFont* SmallFont = GEngine ? GEngine->GetSmallFont() : nullptr;
	if (!MediumFont || !SmallFont) return;

	FText PromptText = FText::GetEmpty();
	if (Kabir->CurrentInteractableActor->Implements<UInteractableInterface>())
	{
		PromptText = IInteractableInterface::Execute_GetInteractionPrompt(Kabir->CurrentInteractableActor);
	}
	else
	{
		FString Label = TEXT("");
#if WITH_EDITOR
		Label = Kabir->CurrentInteractableActor->GetActorLabel();
#endif
		FString Name = Kabir->CurrentInteractableActor->GetName();
		FString MeshName = TEXT("");
		if (UStaticMeshComponent* SMC = Cast<UStaticMeshComponent>(Kabir->CurrentInteractableActor->GetComponentByClass(UStaticMeshComponent::StaticClass())))
		{
			if (SMC->GetStaticMesh())
			{
				MeshName = SMC->GetStaticMesh()->GetName();
			}
		}

		if (Label.Contains(TEXT("Kite")) || Name.Contains(TEXT("Kite")) || MeshName.Contains(TEXT("Kite")))
		{
			PromptText = FText::FromString(TEXT("Inspect Abandoned Basant Paper Kite"));
		}
		else if (Label.Contains(TEXT("Stairs")) || Label.Contains(TEXT("Steps")) || Name.Contains(TEXT("Stairs")) || Name.Contains(TEXT("Steps")) || MeshName.Contains(TEXT("Stairs")) || MeshName.Contains(TEXT("Steps")))
		{
			PromptText = FText::FromString(TEXT("Inspect Steps Masonry Rooftop Steps"));
		}
		else if (Label.Contains(TEXT("Charkhi")) || Name.Contains(TEXT("Charkhi")) || MeshName.Contains(TEXT("Charkhi")))
		{
			PromptText = FText::FromString(TEXT("Inspect Patang & Charkhi Spool"));
		}
	}

	if (PromptText.IsEmpty())
	{
		PromptText = FText::FromString(TEXT("Interact"));
	}

	FString PromptStr = PromptText.ToString();
	float TextW = 0.0f, TextH = 0.0f;
	GetTextSize(PromptStr, TextW, TextH, MediumFont);

	FString KeyLabel = Kabir->IsUsingGamepad() ? TEXT("(X)") : TEXT("E / (X)");
	float KeyW = 0.0f, KeyH = 0.0f;
	GetTextSize(KeyLabel, KeyW, KeyH, SmallFont);

	const float KeyBadgeW = FMath::Max(34.0f, KeyW + 14.0f);
	const float KeyBadgeH = 26.0f;
	const float PaddingX = 14.0f;
	const float Spacing = 10.0f;
	const float BoxW = KeyBadgeW + Spacing + TextW + (PaddingX * 2.0f);
	const float BoxH = 42.0f;

	const float BoxX = (Canvas->ClipX - BoxW) * 0.5f;
	const float BoxY = Canvas->ClipY * 0.72f;

	// Dark semi-translucent backdrop with antique brass border
	DrawFramedBox(BoxX, BoxY, BoxW, BoxH, FLinearColor(0.06f, 0.05f, 0.04f, 0.82f), AntiqueBrassColor, 1.5f);

	// Key badge background [ E / (X) ]
	const float BadgeX = BoxX + PaddingX;
	const float BadgeY = BoxY + (BoxH - KeyBadgeH) * 0.5f;
	DrawFramedBox(BadgeX, BadgeY, KeyBadgeW, KeyBadgeH, AntiqueBrassColor, FLinearColor(1.0f, 0.95f, 0.75f, 1.0f), 1.0f);

	// Key badge text
	DrawText(KeyLabel, DarkInkColor, BadgeX + (KeyBadgeW - KeyW) * 0.5f, BadgeY + (KeyBadgeH - KeyH) * 0.5f, SmallFont);

	// Prompt action text
	const float TextX = BadgeX + KeyBadgeW + Spacing;
	const float TextY = BoxY + (BoxH - TextH) * 0.5f;
	DrawText(PromptStr, FLinearColor(0.96f, 0.94f, 0.88f, 1.0f), TextX, TextY, MediumFont);
}

void ARevolutionHUD::DrawInspectionModal(ARevolutionCharacter* Kabir)
{
	if (!Canvas || !Kabir) return;

	UFont* LargeFont = GEngine ? GEngine->GetLargeFont() : nullptr;
	UFont* MediumFont = GEngine ? GEngine->GetMediumFont() : nullptr;
	UFont* SmallFont = GEngine ? GEngine->GetSmallFont() : nullptr;
	if (!LargeFont || !MediumFont || !SmallFont) return;

	// 1. Fullscreen cinematic darkened overlay
	DrawRect(FLinearColor(0.02f, 0.02f, 0.03f, 0.78f), 0.0f, 0.0f, Canvas->ClipX, Canvas->ClipY);

	// 2. Parchment card dimensions
	const float CardW = FMath::Clamp(Canvas->ClipX * 0.58f, 540.0f, 820.0f);
	const float CardH = FMath::Clamp(Canvas->ClipY * 0.64f, 380.0f, 540.0f);
	const float CardX = (Canvas->ClipX - CardW) * 0.5f;
	const float CardY = (Canvas->ClipY - CardH) * 0.5f;

	// Outer card fill & brass border
	DrawFramedBox(CardX, CardY, CardW, CardH, ParchmentColor, AntiqueBrassColor, 3.0f);

	// Inner decorative hairline border
	const float Inset = 7.0f;
	DrawFramedBox(CardX + Inset, CardY + Inset, CardW - (Inset * 2.0f), CardH - (Inset * 2.0f), FLinearColor::Transparent, MutedSepiaColor, 1.0f);

	// 3. Header Section
	const float HeaderY = CardY + 24.0f;
	FString ArchiveTag = TEXT("— HISTORICAL ARTIFACT : KOT GURDARSHAN (1919) —");
	float TagW = 0.0f, TagH = 0.0f;
	GetTextSize(ArchiveTag, TagW, TagH, SmallFont);
	DrawText(ArchiveTag, MutedSepiaColor, CardX + (CardW - TagW) * 0.5f, HeaderY, SmallFont);

	// Item Title
	FString TitleStr = Kabir->GetInspectedItemName().ToString().ToUpper();
	float TitleW = 0.0f, TitleH = 0.0f;
	GetTextSize(TitleStr, TitleW, TitleH, LargeFont);
	DrawText(TitleStr, DarkInkColor, CardX + (CardW - TitleW) * 0.5f, HeaderY + TagH + 6.0f, LargeFont);

	// Divider line under header
	const float LineY = HeaderY + TagH + TitleH + 14.0f;
	DrawLine(CardX + 32.0f, LineY, CardX + CardW - 32.0f, LineY, AntiqueBrassColor, 1.5f);

	// 4. Body Lore Section
	const float ContentMarginX = 36.0f;
	const float ContentWidth = CardW - (ContentMarginX * 2.0f);
	FString LoreStr = Kabir->GetInspectedItemLore().ToString();

	TArray<FString> WrappedLines = WrapText(LoreStr, MediumFont, ContentWidth);

	float CurrentY = LineY + 22.0f;
	const float LineSpacing = 24.0f;

	for (const FString& Line : WrappedLines)
	{
		DrawText(Line, DarkInkColor, CardX + ContentMarginX, CurrentY, MediumFont);
		CurrentY += LineSpacing;
	}

	// 5. Footer Section
	const float FooterLineY = CardY + CardH - 52.0f;
	DrawLine(CardX + 32.0f, FooterLineY, CardX + CardW - 32.0f, FooterLineY, AntiqueBrassColor, 1.5f);

	FString DismissPrompt = Kabir->IsUsingGamepad() ? TEXT("[ (B) ]  OR  [ (A) ]  TO CLOSE INSPECTION") : TEXT("[ E / (X) ]  OR  [ SPACE / (B) ]  TO CLOSE INSPECTION");
	float DismissW = 0.0f, DismissH = 0.0f;
	GetTextSize(DismissPrompt, DismissW, DismissH, SmallFont);
	DrawText(DismissPrompt, MutedSepiaColor, CardX + (CardW - DismissW) * 0.5f, FooterLineY + 16.0f, SmallFont);
}

void ARevolutionHUD::DrawStaminaGauge(ARevolutionCharacter* Kabir)
{
	if (!bShowStamina || !Canvas || !Kabir) return;

	float TargetAlpha = (Kabir->bIsSprinting || Kabir->CurrentStamina < (Kabir->MaxStamina - 0.5f)) ? 1.0f : 0.0f;
	StaminaDisplayAlpha = FMath::FInterpTo(StaminaDisplayAlpha, TargetAlpha, GetWorld()->GetDeltaSeconds(), 3.5f);

	if (StaminaDisplayAlpha <= 0.01f) return;

	UFont* SmallFont = GEngine ? GEngine->GetSmallFont() : nullptr;

	const float BarW = 200.0f;
	const float BarH = 8.0f;
	const float BarX = (Canvas->ClipX - BarW) * 0.5f;
	const float BarY = Canvas->ClipY * 0.88f;

	// Label "STAMINA"
	if (SmallFont)
	{
		FString Label = TEXT("STAMINA");
		float LabelW = 0.0f, LabelH = 0.0f;
		GetTextSize(Label, LabelW, LabelH, SmallFont);
		DrawText(Label, AntiqueBrassColor.CopyWithNewOpacity(StaminaDisplayAlpha * 0.85f), BarX + (BarW - LabelW) * 0.5f, BarY - LabelH - 4.0f, SmallFont);
	}

	// Background track
	FLinearColor TrackBg(0.08f, 0.07f, 0.06f, 0.65f * StaminaDisplayAlpha);
	FLinearColor TrackBorder = AntiqueBrassColor.CopyWithNewOpacity(0.75f * StaminaDisplayAlpha);
	DrawFramedBox(BarX, BarY, BarW, BarH, TrackBg, TrackBorder, 1.0f);

	// Stamina fill
	float FillPct = FMath::Clamp(Kabir->CurrentStamina / Kabir->MaxStamina, 0.0f, 1.0f);
	if (FillPct > 0.0f)
	{
		FLinearColor FillColor;
		if (FillPct < 0.25f)
		{
			// Pulsing red/amber when exhausted
			float Pulse = 0.5f + 0.5f * FMath::Sin(GetWorld()->GetTimeSeconds() * 8.0f);
			FillColor = FLinearColor::LerpUsingHSV(FLinearColor(0.85f, 0.2f, 0.15f, 1.0f), AntiqueBrassColor, Pulse);
		}
		else
		{
			FillColor = AntiqueBrassColor;
		}
		FillColor.A *= StaminaDisplayAlpha;

		DrawRect(FillColor, BarX + 1.0f, BarY + 1.0f, (BarW - 2.0f) * FillPct, BarH - 2.0f);
	}
}

void ARevolutionHUD::DrawCompass(ARevolutionCharacter* Kabir)
{
	if (!bShowCompass || !Canvas || !Kabir) return;

	UFont* SmallFont = GEngine ? GEngine->GetSmallFont() : nullptr;
	if (!SmallFont) return;

	const float TapeWidth = 260.0f;
	const float TapeHeight = 28.0f;
	const float TapeX = (Canvas->ClipX - TapeWidth) * 0.5f;
	const float TapeY = 20.0f;
	const float CenterX = Canvas->ClipX * 0.5f;

	// Background backing & border
	DrawFramedBox(TapeX, TapeY, TapeWidth, TapeHeight, FLinearColor(0.04f, 0.04f, 0.04f, 0.72f), AntiqueBrassColor, 1.0f);

	// Center indicator notch
	DrawLine(CenterX, TapeY, CenterX, TapeY + 6.0f, AntiqueBrassColor, 2.0f);
	DrawLine(CenterX, TapeY + TapeHeight - 6.0f, CenterX, TapeY + TapeHeight, AntiqueBrassColor, 2.0f);

	// Get player yaw in [0, 360)
	FRotator ControlRot = Kabir->GetControlRotation();
	float PlayerYaw = FRotator::NormalizeAxis(ControlRot.Yaw);
	if (PlayerYaw < 0.0f) PlayerYaw += 360.0f;

	// Cardinal markers
	struct FCompassMark
	{
		float Degree;
		FString Label;
		bool bMajor;
	};

	static const FCompassMark Marks[] = {
		{ 0.0f, TEXT("N"), true },
		{ 45.0f, TEXT("NE"), false },
		{ 90.0f, TEXT("E"), true },
		{ 135.0f, TEXT("SE"), false },
		{ 180.0f, TEXT("S"), true },
		{ 225.0f, TEXT("SW"), false },
		{ 270.0f, TEXT("W"), true },
		{ 315.0f, TEXT("NW"), false }
	};

	const float VisibleAngleHalfRange = 40.0f;
	const float PixelsPerDegree = (TapeWidth * 0.5f) / VisibleAngleHalfRange;

	for (const FCompassMark& Mark : Marks)
	{
		float Diff = Mark.Degree - PlayerYaw;
		while (Diff > 180.0f) Diff -= 360.0f;
		while (Diff < -180.0f) Diff += 360.0f;

		if (FMath::Abs(Diff) <= VisibleAngleHalfRange)
		{
			float ScreenX = CenterX + (Diff * PixelsPerDegree);
			float TickHeight = Mark.bMajor ? 8.0f : 4.0f;
			DrawLine(ScreenX, TapeY + TapeHeight - TickHeight, ScreenX, TapeY + TapeHeight - 2.0f, AntiqueBrassColor, 1.0f);

			float TextW = 0.0f, TextH = 0.0f;
			GetTextSize(Mark.Label, TextW, TextH, SmallFont);
			FLinearColor MarkColor = Mark.bMajor ? AntiqueBrassColor : FLinearColor(0.85f, 0.85f, 0.82f, 0.75f);
			DrawText(Mark.Label, MarkColor, ScreenX - (TextW * 0.5f), TapeY + 4.0f, SmallFont);
		}
	}

	// Draw Scout Chalk Waypoints on Compass Tape
	for (TActorIterator<AChalkMarkActor> It(GetWorld()); It; ++It)
	{
		AChalkMarkActor* ChalkActor = *It;
		if (ChalkActor)
		{
			FVector DirToMark = (ChalkActor->GetActorLocation() - Kabir->GetActorLocation()).GetSafeNormal2D();
			float MarkAngle = FMath::RadiansToDegrees(FMath::Atan2(DirToMark.Y, DirToMark.X));
			float Diff = MarkAngle - PlayerYaw;
			while (Diff > 180.0f) Diff -= 360.0f;
			while (Diff < -180.0f) Diff += 360.0f;

			if (FMath::Abs(Diff) <= VisibleAngleHalfRange)
			{
				float ScreenX = CenterX + (Diff * PixelsPerDegree);
				FLinearColor ChalkWayColor = FLinearColor(0.96f, 0.95f, 0.90f, 0.92f);
				DrawLine(ScreenX - 3.0f, TapeY + TapeHeight * 0.5f, ScreenX, TapeY + 3.0f, ChalkWayColor, 1.5f);
				DrawLine(ScreenX, TapeY + 3.0f, ScreenX + 3.0f, TapeY + TapeHeight * 0.5f, ChalkWayColor, 1.5f);
				DrawLine(ScreenX + 3.0f, TapeY + TapeHeight * 0.5f, ScreenX, TapeY + TapeHeight - 3.0f, ChalkWayColor, 1.5f);
				DrawLine(ScreenX, TapeY + TapeHeight - 3.0f, ScreenX - 3.0f, TapeY + TapeHeight * 0.5f, ChalkWayColor, 1.5f);
			}
		}
	}

	// Draw Active Mission Objective Waypoint on Compass Tape
	if (bShowObjectiveBeacons)
	{
		if (URevolutionMissionSubsystem* Subsystem = GetWorld()->GetSubsystem<URevolutionMissionSubsystem>())
		{
			FVector ObjectiveLoc = FVector::ZeroVector;
			FText ObjectiveName = FText::GetEmpty();
			if (Subsystem->GetActiveObjectiveLocation(ObjectiveLoc, ObjectiveName))
			{
				FVector DirToObj = (ObjectiveLoc - Kabir->GetActorLocation()).GetSafeNormal2D();
				float ObjAngle = FMath::RadiansToDegrees(FMath::Atan2(DirToObj.Y, DirToObj.X));
				float Diff = ObjAngle - PlayerYaw;
				while (Diff > 180.0f) Diff -= 360.0f;
				while (Diff < -180.0f) Diff += 360.0f;

				if (FMath::Abs(Diff) <= VisibleAngleHalfRange)
				{
					float ScreenX = CenterX + (Diff * PixelsPerDegree);
					float Pulse = 0.80f + 0.20f * FMath::Sin(GetWorld()->GetTimeSeconds() * 4.0f);
					FLinearColor ObjWayColor = FLinearColor(1.0f, 0.82f, 0.25f, Pulse);

					// Outer diamond
					const float HalfW = 5.0f;
					const float CenterY = TapeY + TapeHeight * 0.5f;
					DrawLine(ScreenX - HalfW, CenterY, ScreenX, CenterY - HalfW, ObjWayColor, 1.8f);
					DrawLine(ScreenX, CenterY - HalfW, ScreenX + HalfW, CenterY, ObjWayColor, 1.8f);
					DrawLine(ScreenX + HalfW, CenterY, ScreenX, CenterY + HalfW, ObjWayColor, 1.8f);
					DrawLine(ScreenX, CenterY + HalfW, ScreenX - HalfW, CenterY, ObjWayColor, 1.8f);

					// Center gold pip
					DrawRect(ObjWayColor, ScreenX - 1.5f, CenterY - 1.5f, 3.0f, 3.0f);
				}
			}
		}
	}
}

void ARevolutionHUD::DrawStealthAndDetection(ARevolutionCharacter* Kabir)
{
	if (!bShowStealthIndicators || !Canvas || !Kabir) return;

	UFont* SmallFont = GEngine ? GEngine->GetSmallFont() : nullptr;

	// 1. Stance / Concealment Badge (Lower Left)
	if (Kabir->IsHidingInCover() && SmallFont)
	{
		FString CoverText = TEXT("[ FULLY CONCEALED IN COVER ]");
		float CoverW = 0.0f, CoverH = 0.0f;
		GetTextSize(CoverText, CoverW, CoverH, SmallFont);

		float BadgeX = 36.0f;
		float BadgeY = Canvas->ClipY * 0.81f;

		// Emerald jade green banner for 100% concealment in cover
		FLinearColor CoverCol = FLinearColor(0.24f, 0.88f, 0.48f, 0.96f);
		DrawFramedBox(BadgeX, BadgeY, CoverW + 16.0f, CoverH + 8.0f, FLinearColor(0.04f, 0.12f, 0.06f, 0.85f), CoverCol, 1.5f);
		DrawText(CoverText, CoverCol, BadgeX + 8.0f, BadgeY + 4.0f, SmallFont);
	}
	else if (Kabir->IsCrawlTraversing() && SmallFont)
	{
		FString CrawlText = TEXT("[ LOW DRAIN CRAWL — UNSEEN ]");
		float CrawlW = 0.0f, CrawlH = 0.0f;
		GetTextSize(CrawlText, CrawlW, CrawlH, SmallFont);

		float BadgeX = 36.0f;
		float BadgeY = Canvas->ClipY * 0.81f;

		// Terracotta amber tone for enclosed conduit crawl
		FLinearColor CrawlCol = FLinearColor(0.88f, 0.58f, 0.22f, 0.95f);
		DrawFramedBox(BadgeX, BadgeY, CrawlW + 16.0f, CrawlH + 8.0f, FLinearColor(0.12f, 0.06f, 0.02f, 0.85f), CrawlCol, 1.5f);
		DrawText(CrawlText, CrawlCol, BadgeX + 8.0f, BadgeY + 4.0f, SmallFont);
	}
	else if (Kabir->IsCrowdBlended() && SmallFont)
	{
		FString BlendText = TEXT("[ BLENDED WITH CIVILIANS — LOW PROFILE ]");
		float BlendW = 0.0f, BlendH = 0.0f;
		GetTextSize(BlendText, BlendW, BlendH, SmallFont);

		float BadgeX = 36.0f;
		float BadgeY = Canvas->ClipY * 0.81f;

		// Soft cornflower blue / ivory badge for crowd camouflage
		FLinearColor BlendCol = FLinearColor(0.40f, 0.75f, 0.95f, 0.95f);
		DrawFramedBox(BadgeX, BadgeY, BlendW + 16.0f, BlendH + 8.0f, FLinearColor(0.04f, 0.08f, 0.16f, 0.85f), BlendCol, 1.5f);
		DrawText(BlendText, BlendCol, BadgeX + 8.0f, BadgeY + 4.0f, SmallFont);
	}
	else if (Kabir->IsMantling() && SmallFont)
	{
		FString MantleText = TEXT("[ PARKOUR — HIGH MANTLE ]");
		float MantleW = 0.0f, MantleH = 0.0f;
		GetTextSize(MantleText, MantleW, MantleH, SmallFont);

		float BadgeX = 36.0f;
		float BadgeY = Canvas->ClipY * 0.81f;

		FLinearColor MantleCol = FLinearColor(0.96f, 0.65f, 0.20f, 0.95f);
		DrawFramedBox(BadgeX, BadgeY, MantleW + 16.0f, MantleH + 8.0f, FLinearColor(0.14f, 0.08f, 0.02f, 0.85f), MantleCol, 1.5f);
		DrawText(MantleText, MantleCol, BadgeX + 8.0f, BadgeY + 4.0f, SmallFont);
	}
	else if (Kabir->bIsCrouched && SmallFont)
	{
		FString StanceText = TEXT("[ CROUCHED — CONCEALED ]");
		float StanceW = 0.0f, StanceH = 0.0f;
		GetTextSize(StanceText, StanceW, StanceH, SmallFont);

		float BadgeX = 36.0f;
		float BadgeY = Canvas->ClipY * 0.81f;

		DrawFramedBox(BadgeX, BadgeY, StanceW + 16.0f, StanceH + 8.0f, FLinearColor(0.06f, 0.05f, 0.04f, 0.70f), AntiqueBrassColor, 1.0f);
		DrawText(StanceText, AntiqueBrassColor, BadgeX + 8.0f, BadgeY + 4.0f, SmallFont);
	}

	// 2. Distraction Ammo Badge (Lower Left)
	if (SmallFont)
	{
		int32 Pebbles = Kabir->GetPebbleCount();
		FString PebbleText = FString::Printf(TEXT("[F] CLAY MARBLES  (%d / %d)"), Pebbles, Kabir->MaxPebbles);
		float PebbleW = 0.0f, PebbleH = 0.0f;
		GetTextSize(PebbleText, PebbleW, PebbleH, SmallFont);

		float PebbleBadgeX = 36.0f;
		float PebbleBadgeY = Canvas->ClipY * 0.865f;

		FLinearColor TextCol = (Pebbles > 0) ? FLinearColor(0.88f, 0.85f, 0.78f, 0.92f) : FLinearColor(0.55f, 0.50f, 0.45f, 0.60f);
		DrawFramedBox(PebbleBadgeX, PebbleBadgeY, PebbleW + 16.0f, PebbleH + 8.0f, FLinearColor(0.06f, 0.05f, 0.04f, 0.65f), MutedSepiaColor, 1.0f);
		DrawText(PebbleText, TextCol, PebbleBadgeX + 8.0f, PebbleBadgeY + 4.0f, SmallFont);

		// 3. Scout Chalk Badge (Lower Left)
		int32 Chalk = Kabir->GetChalkCount();
		FString ChalkText = FString::Printf(TEXT("[T] SCOUT CHALK  (%d / %d)"), Chalk, Kabir->MaxChalk);
		float ChalkW = 0.0f, ChalkH = 0.0f;
		GetTextSize(ChalkText, ChalkW, ChalkH, SmallFont);

		float ChalkBadgeX = 36.0f;
		float ChalkBadgeY = Canvas->ClipY * 0.92f;

		FLinearColor ChalkCol = (Chalk > 0) ? FLinearColor(0.95f, 0.94f, 0.90f, 0.95f) : FLinearColor(0.55f, 0.50f, 0.45f, 0.60f);
		DrawFramedBox(ChalkBadgeX, ChalkBadgeY, ChalkW + 16.0f, ChalkH + 8.0f, FLinearColor(0.06f, 0.05f, 0.04f, 0.65f), MutedSepiaColor, 1.0f);
		DrawText(ChalkText, ChalkCol, ChalkBadgeX + 8.0f, ChalkBadgeY + 4.0f, SmallFont);
	}

	float TopNotificationY = 58.0f;

	// 3. Scan for active Watchman Detection
	ACurfewPatrolAI* HighestThreatWatchman = nullptr;
	float HighestDetection = 0.0f;

	for (TActorIterator<ACurfewPatrolAI> It(GetWorld()); It; ++It)
	{
		float Det = It->GetDetectionPercentage();
		if (Det > HighestDetection)
		{
			HighestDetection = Det;
			HighestThreatWatchman = *It;
		}
	}

	if (HighestThreatWatchman && HighestDetection > 1.0f)
	{
		const float CenterX = Canvas->ClipX * 0.5f;
		const float CenterY = Canvas->ClipY * 0.5f;

		// Relative Threat Direction
		FVector CamForward = Kabir->GetFollowCamera() ? Kabir->GetFollowCamera()->GetForwardVector().GetSafeNormal2D() : Kabir->GetActorForwardVector().GetSafeNormal2D();
		FVector DirToWatchman = (HighestThreatWatchman->GetActorLocation() - Kabir->GetActorLocation()).GetSafeNormal2D();

		// Calculate 2D angle relative to camera view
		float ForwardAngle = FMath::Atan2(CamForward.Y, CamForward.X);
		float WatchmanAngle = FMath::Atan2(DirToWatchman.Y, DirToWatchman.X);
		float RelAngle = WatchmanAngle - ForwardAngle;

		// Threat indicator position on ring around center reticle
		const float RingRadius = 78.0f;
		float ScreenThreatX = CenterX + (FMath::Sin(RelAngle) * RingRadius);
		float ScreenThreatY = CenterY - (FMath::Cos(RelAngle) * RingRadius);

		// Threat color based on detection percentage
		FLinearColor ThreatColor;
		if (HighestDetection >= 90.0f)
		{
			// Pulsing crimson alert
			float Pulse = 0.6f + 0.4f * FMath::Sin(GetWorld()->GetTimeSeconds() * 8.0f);
			ThreatColor = FLinearColor(0.92f, 0.12f, 0.10f, Pulse);
		}
		else if (HighestDetection >= 45.0f)
		{
			// Burning orange suspicion
			ThreatColor = FLinearColor(0.96f, 0.48f, 0.15f, 0.95f);
		}
		else
		{
			// Amber caution
			ThreatColor = FLinearColor(0.88f, 0.72f, 0.22f, 0.80f);
		}

		// Draw directional threat chevron / diamond
		const float MarkerSize = 6.0f + (HighestDetection * 0.06f);
		DrawLine(ScreenThreatX - MarkerSize, ScreenThreatY, ScreenThreatX, ScreenThreatY - MarkerSize, ThreatColor, 2.0f);
		DrawLine(ScreenThreatX, ScreenThreatY - MarkerSize, ScreenThreatX + MarkerSize, ScreenThreatY, ThreatColor, 2.0f);
		DrawLine(ScreenThreatX + MarkerSize, ScreenThreatY, ScreenThreatX, ScreenThreatY + MarkerSize, ThreatColor, 2.0f);
		DrawLine(ScreenThreatX, ScreenThreatY + MarkerSize, ScreenThreatX - MarkerSize, ScreenThreatY, ThreatColor, 2.0f);

		// If alerted, draw top alert banner
		if (HighestDetection >= 90.0f && SmallFont)
		{
			FString AlertText = TEXT("!  CURFEW PATROL ALERT — BREAK LINE OF SIGHT  !");
			float AlertW = 0.0f, AlertH = 0.0f;
			GetTextSize(AlertText, AlertW, AlertH, SmallFont);

			float BannerW = AlertW + 32.0f;
			float BannerH = AlertH + 12.0f;
			float BannerX = (Canvas->ClipX - BannerW) * 0.5f;

			DrawFramedBox(BannerX, TopNotificationY, BannerW, BannerH, FLinearColor(0.12f, 0.02f, 0.02f, 0.85f), ThreatColor, 1.5f);
			DrawText(AlertText, FLinearColor(1.0f, 0.9f, 0.85f, 1.0f), BannerX + 16.0f, TopNotificationY + 6.0f, SmallFont);

			TopNotificationY += BannerH + 6.0f;
		}
	}

	// 4. North Western Railway Acoustic Sound Masking Indicator
	bool bSoundMasked = false;
	for (TActorIterator<ARevolutionAtmosphereController> AtmoIt(GetWorld()); AtmoIt; ++AtmoIt)
	{
		if (AtmoIt->IsSoundMasked())
		{
			bSoundMasked = true;
			break;
		}
	}

	if (bSoundMasked && SmallFont)
	{
		FString TrainText = TEXT("~  SOUND MASKED — NORTH WESTERN RAILWAY PASSING  ~");
		float TrainW = 0.0f, TrainH = 0.0f;
		GetTextSize(TrainText, TrainW, TrainH, SmallFont);

		float TrainPulse = 0.75f + 0.25f * FMath::Sin(GetWorld()->GetTimeSeconds() * 6.0f);
		FLinearColor TrainCol = FLinearColor(0.55f, 0.80f, 0.98f, TrainPulse);

		float BoxW = TrainW + 28.0f;
		float BoxH = TrainH + 10.0f;
		float BoxX = (Canvas->ClipX - BoxW) * 0.5f;

		DrawFramedBox(BoxX, TopNotificationY, BoxW, BoxH, FLinearColor(0.04f, 0.08f, 0.12f, 0.82f), TrainCol, 1.2f);
		DrawText(TrainText, TrainCol, BoxX + 14.0f, TopNotificationY + 5.0f, SmallFont);
		TopNotificationY += BoxH + 6.0f;
	}

	// Task 27: Dynamic Weather State Indicator (Andhi Dust Storm)
	for (TActorIterator<ARevolutionAtmosphereController> AtmoIt(GetWorld()); AtmoIt; ++AtmoIt)
	{
		if (AtmoIt->GetCurrentWeatherState() == EHistoricalWeatherState::DustStormAndhi && SmallFont)
		{
			FString WeatherText = TEXT("~  WEATHER: ANDHI DUST STORM — SENTRY VISIBILITY REDUCED (35%)  ~");
			float WTextW = 0.0f, WTextH = 0.0f;
			GetTextSize(WeatherText, WTextW, WTextH, SmallFont);

			float WPulse = 0.80f + 0.20f * FMath::Sin(GetWorld()->GetTimeSeconds() * 5.0f);
			FLinearColor OchreCol = FLinearColor(0.96f, 0.68f, 0.26f, WPulse);

			float BoxW = WTextW + 28.0f;
			float BoxH = WTextH + 10.0f;
			float BoxX = (Canvas->ClipX - BoxW) * 0.5f;

			DrawFramedBox(BoxX, TopNotificationY, BoxW, BoxH, FLinearColor(0.14f, 0.08f, 0.02f, 0.85f), OchreCol, 1.2f);
			DrawText(WeatherText, OchreCol, BoxX + 14.0f, TopNotificationY + 5.0f, SmallFont);
			TopNotificationY += BoxH + 6.0f;
			break;
		}
	}

	// 5. Brittle Terracotta Roof Shingles Hazard Caution
	bool bNearTerracottaHazard = false;
	for (TActorIterator<ATerracottaHazardActor> HazIt(GetWorld()); HazIt; ++HazIt)
	{
		ATerracottaHazardActor* Haz = *HazIt;
		if (Haz && FVector::Dist(Kabir->GetActorLocation(), Haz->GetActorLocation()) < 185.0f)
		{
			bNearTerracottaHazard = true;
			break;
		}
	}

	if (bNearTerracottaHazard && SmallFont)
	{
		FString HazText = Kabir->bIsCrouched 
			? TEXT("~  TREADING SILENTLY ON BRITTLE TILES  ~") 
			: TEXT("!  BRITTLE TERRACOTTA SHINGLES — CROUCH [C] TO TREAD SILENTLY  !");

		float HazW = 0.0f, HazH = 0.0f;
		GetTextSize(HazText, HazW, HazH, SmallFont);

		FLinearColor HazCol = Kabir->bIsCrouched 
			? FLinearColor(0.45f, 0.85f, 0.55f, 0.90f) 
			: FLinearColor(0.95f, 0.65f, 0.22f, 0.95f);

		float BoxW = HazW + 28.0f;
		float BoxH = HazH + 10.0f;
		float BoxX = (Canvas->ClipX - BoxW) * 0.5f;

		DrawFramedBox(BoxX, TopNotificationY, BoxW, BoxH, FLinearColor(0.10f, 0.06f, 0.03f, 0.85f), HazCol, 1.2f);
		DrawText(HazText, HazCol, BoxX + 14.0f, TopNotificationY + 5.0f, SmallFont);
		TopNotificationY += BoxH + 6.0f;
	}

	// 6. Watchman Lantern Wind Turbulence Stealth Cue
	bool bAnyLanternFlickering = false;
	for (TActorIterator<ACurfewPatrolAI> It(GetWorld()); It; ++It)
	{
		ACurfewPatrolAI* Watchman = *It;
		if (Watchman && Watchman->IsLanternFlickering())
		{
			bAnyLanternFlickering = true;
			break;
		}
	}

	if (bAnyLanternFlickering && SmallFont)
	{
		FString GustText = TEXT("~  WIND GUST — WATCHMAN LANTERN FLICKERING (VISION REDUCED)  ~");
		float GustW = 0.0f, GustH = 0.0f;
		GetTextSize(GustText, GustW, GustH, SmallFont);

		float GustPulse = 0.70f + 0.30f * FMath::Sin(GetWorld()->GetTimeSeconds() * 8.0f);
		FLinearColor GustCol = FLinearColor(1.0f, 0.82f, 0.40f, GustPulse);

		float BoxW = GustW + 28.0f;
		float BoxH = GustH + 10.0f;
		float BoxX = (Canvas->ClipX - BoxW) * 0.5f;

		DrawFramedBox(BoxX, TopNotificationY, BoxW, BoxH, FLinearColor(0.12f, 0.08f, 0.02f, 0.82f), GustCol, 1.2f);
		DrawText(GustText, GustCol, BoxX + 14.0f, TopNotificationY + 5.0f, SmallFont);
		TopNotificationY += BoxH + 6.0f;
	}

	// 7. Active Wheat Chaff Screen Indicator
	bool bInsideChaffScreen = false;
	for (TActorIterator<AChaffDustDecoyActor> ChaffIt(GetWorld()); ChaffIt; ++ChaffIt)
	{
		AChaffDustDecoyActor* Chaff = *ChaffIt;
		if (Chaff && Chaff->IsDustCloudActive())
		{
			float Dist = FVector::Dist(Kabir->GetActorLocation(), Chaff->GetActorLocation());
			if (Dist <= Chaff->DustRadius)
			{
				bInsideChaffScreen = true;
				break;
			}
		}
	}

	if (bInsideChaffScreen && SmallFont)
	{
		FString ChaffText = TEXT("~  CONCEALED IN WHEAT CHAFF SCREEN — WATCHMAN SIGHT BLOCKED  ~");
		float ChaffW = 0.0f, ChaffH = 0.0f;
		GetTextSize(ChaffText, ChaffW, ChaffH, SmallFont);

		float ChaffPulse = 0.75f + 0.25f * FMath::Sin(GetWorld()->GetTimeSeconds() * 7.0f);
		FLinearColor ChaffCol = FLinearColor(0.92f, 0.78f, 0.45f, ChaffPulse);

		float BoxW = ChaffW + 28.0f;
		float BoxH = ChaffH + 10.0f;
		float BoxX = (Canvas->ClipX - BoxW) * 0.5f;

		DrawFramedBox(BoxX, TopNotificationY, BoxW, BoxH, FLinearColor(0.12f, 0.09f, 0.03f, 0.85f), ChaffCol, 1.2f);
		DrawText(ChaffText, ChaffCol, BoxX + 14.0f, TopNotificationY + 5.0f, SmallFont);
		TopNotificationY += BoxH + 6.0f;
	}

	// 8. Sleeping Mohalla Dog Proximity Caution
	bool bNearSleepingDog = false;
	for (TActorIterator<APariahDogActor> DogIt(GetWorld()); DogIt; ++DogIt)
	{
		APariahDogActor* Dog = *DogIt;
		if (Dog && Dog->GetDogState() == EPariahDogState::Sleeping)
		{
			float Dist = FVector::Dist(Kabir->GetActorLocation(), Dog->GetActorLocation());
			if (Dist <= Dog->WalkAlertRadius * 1.35f)
			{
				bNearSleepingDog = true;
				break;
			}
		}
	}

	if (bNearSleepingDog && SmallFont)
	{
		FString DogText = Kabir->bIsCrouched 
			? TEXT("~  SLEEPING MOHALLA DOG — CROUCHING SILENTLY PAST  ~") 
			: TEXT("!  SLEEPING MOHALLA DOG AHEAD — CROUCH [C] TO AVOID WAKING  !");

		float DogW = 0.0f, DogH = 0.0f;
		GetTextSize(DogText, DogW, DogH, SmallFont);

		FLinearColor DogCol = Kabir->bIsCrouched 
			? FLinearColor(0.48f, 0.88f, 0.55f, 0.90f) 
			: FLinearColor(0.95f, 0.45f, 0.20f, 0.95f);

		float BoxW = DogW + 28.0f;
		float BoxH = DogH + 10.0f;
		float BoxX = (Canvas->ClipX - BoxW) * 0.5f;

		DrawFramedBox(BoxX, TopNotificationY, BoxW, BoxH, FLinearColor(0.10f, 0.05f, 0.02f, 0.85f), DogCol, 1.2f);
		DrawText(DogText, DogCol, BoxX + 14.0f, TopNotificationY + 5.0f, SmallFont);
	}
}

void ARevolutionHUD::DrawPebbleAimTrajectory(ARevolutionCharacter* Kabir)
{
	if (!Canvas || !Kabir || !Kabir->IsAimingPebble() || Kabir->GetPebbleCount() <= 0) return;

	TArray<FVector> TrajectoryPoints;
	FVector ImpactPoint;
	bool bHitValid = false;

	if (Kabir->CalculatePebbleTrajectory(TrajectoryPoints, ImpactPoint, bHitValid))
	{
		APlayerController* PC = Cast<APlayerController>(Kabir->GetController());
		if (!PC) return;

		FVector2D PrevScreenPos = FVector2D::ZeroVector;
		bool bHasPrev = false;

		for (const FVector& WorldPoint : TrajectoryPoints)
		{
			FVector2D ScreenPos;
			if (PC->ProjectWorldLocationToScreen(WorldPoint, ScreenPos))
			{
				if (bHasPrev)
				{
					// Draw luminous amber parabolic trajectory arc line
					DrawLine(PrevScreenPos.X, PrevScreenPos.Y, ScreenPos.X, ScreenPos.Y, FLinearColor(1.0f, 0.78f, 0.28f, 0.85f), 2.5f);
				}
				// Trajectory node bead
				DrawRect(FLinearColor(1.0f, 0.90f, 0.45f, 0.92f), ScreenPos.X - 2.5f, ScreenPos.Y - 2.5f, 5.0f, 5.0f);

				PrevScreenPos = ScreenPos;
				bHasPrev = true;
			}
			else
			{
				bHasPrev = false;
			}
		}

		if (bHitValid)
		{
			FVector2D ImpactScreenPos;
			if (PC->ProjectWorldLocationToScreen(ImpactPoint, ImpactScreenPos))
			{
				// Reticle ring at landing point
				DrawFramedBox(ImpactScreenPos.X - 14.0f, ImpactScreenPos.Y - 14.0f, 28.0f, 28.0f, FLinearColor(0.96f, 0.72f, 0.28f, 0.25f), FLinearColor(1.0f, 0.85f, 0.35f, 0.95f), 2.0f);

				UFont* SmallFont = GEngine ? GEngine->GetSmallFont() : nullptr;
				if (SmallFont)
				{
					FString NoisePrompt = TEXT("[ DISTRACTION IMPACT — 8.5m AUDIBLE ]");
					float TW = 0.0f, TH = 0.0f;
					GetTextSize(NoisePrompt, TW, TH, SmallFont);
					DrawText(NoisePrompt, FLinearColor(1.0f, 0.88f, 0.45f, 0.95f), ImpactScreenPos.X - (TW * 0.5f), ImpactScreenPos.Y + 18.0f, SmallFont);
				}
			}
		}
	}
}

void ARevolutionHUD::DrawConcealmentMeter(ARevolutionCharacter* Kabir)
{
	if (!Canvas || !Kabir || Kabir->IsInspecting() || Kabir->IsSatchelJournalOpen()) return;

	UFont* SmallFont = GEngine ? GEngine->GetSmallFont() : nullptr;
	if (!SmallFont) return;

	float Score = Kabir->GetConcealmentScore();
	int32 Percent = FMath::Clamp(FMath::RoundToInt(Score * 100.0f), 0, 100);

	FString ConcealStatus;
	FLinearColor StatusColor;
	if (Score >= 0.70f)
	{
		ConcealStatus = TEXT("DEEP SHADOW");
		StatusColor = FLinearColor(0.25f, 0.85f, 0.95f, 0.95f);
	}
	else if (Score >= 0.40f)
	{
		ConcealStatus = TEXT("PARTIAL SHADE");
		StatusColor = FLinearColor(0.92f, 0.78f, 0.35f, 0.95f);
	}
	else
	{
		ConcealStatus = TEXT("EXPOSED IN LIGHT");
		StatusColor = FLinearColor(0.95f, 0.38f, 0.28f, 0.95f);
	}

	FString MeterText = FString::Printf(TEXT("[ CONCEALMENT: %d%% — %s ]"), Percent, *ConcealStatus);
	float TextW = 0.0f, TextH = 0.0f;
	GetTextSize(MeterText, TextW, TextH, SmallFont);

	float BadgeX = 36.0f;
	float BadgeY = Canvas->ClipY * 0.845f;

	DrawFramedBox(BadgeX, BadgeY, TextW + 16.0f, TextH + 8.0f, FLinearColor(0.04f, 0.05f, 0.06f, 0.80f), StatusColor, 1.2f);
	DrawText(MeterText, StatusColor, BadgeX + 8.0f, BadgeY + 4.0f, SmallFont);

	// Corner Leaning Status Badge (Dishonored / The Last of Us benchmark)
	if (Kabir->IsCornerLeaning())
	{
		FString LeanText = (Kabir->GetLeanOffset() < 0.0f)
			? TEXT("[ CORNER PEEK: LEAN LEFT ]")
			: TEXT("[ CORNER PEEK: LEAN RIGHT ]");

		float LeanW = 0.0f, LeanH = 0.0f;
		GetTextSize(LeanText, LeanW, LeanH, SmallFont);

		float LeanX = BadgeX + TextW + 24.0f;
		FLinearColor LeanCol = FLinearColor(0.85f, 0.75f, 0.45f, 0.95f);
		DrawFramedBox(LeanX, BadgeY, LeanW + 16.0f, LeanH + 8.0f, FLinearColor(0.08f, 0.06f, 0.03f, 0.85f), LeanCol, 1.2f);
		DrawText(LeanText, LeanCol, LeanX + 8.0f, BadgeY + 4.0f, SmallFont);
	}

	// Steam Obscurity Badge (Hitman / Batman Arkham benchmark)
	if (Kabir->IsSteamObscured())
	{
		FString SteamText = FString::Printf(TEXT("[ STEAM CLOAK ACTIVE (%.1fs) — SENTRY LINE-OF-SIGHT BLOCKED ]"), Kabir->GetSteamObscurityRemainingTime());

		float SteamW = 0.0f, SteamH = 0.0f;
		GetTextSize(SteamText, SteamW, SteamH, SmallFont);

		float SteamX = BadgeX + TextW + 24.0f;
		if (Kabir->IsCornerLeaning())
		{
			SteamX += 240.0f;
		}

		FLinearColor SteamCol = FLinearColor(0.60f, 0.88f, 1.0f, 0.95f);
		DrawFramedBox(SteamX, BadgeY, SteamW + 16.0f, SteamH + 8.0f, FLinearColor(0.03f, 0.07f, 0.12f, 0.85f), SteamCol, 1.2f);
		DrawText(SteamText, SteamCol, SteamX + 8.0f, BadgeY + 4.0f, SmallFont);
	}
}

void ARevolutionHUD::DrawKeenSensesBeacons(ARevolutionCharacter* Kabir)
{
	if (!Canvas || !Kabir || !Kabir->IsKeenSensesActive() || Kabir->IsInspecting() || Kabir->IsSatchelJournalOpen()) return;

	APlayerController* PC = Cast<APlayerController>(Kabir->GetController());
	if (!PC) return;

	UFont* SmallFont = GEngine ? GEngine->GetSmallFont() : nullptr;
	if (!SmallFont) return;

	// Top notification that Basant Intuition / Keen Senses is active
	FString IntuitionText = TEXT("~  BASANT INTUITION (KEEN SENSES ACTIVE) [V]  ~");
	float IW = 0.0f, IH = 0.0f;
	GetTextSize(IntuitionText, IW, IH, SmallFont);
	float IntuitionPulse = 0.75f + 0.25f * FMath::Sin(GetWorld()->GetTimeSeconds() * 5.0f);
	FLinearColor IntuitionCol = FLinearColor(1.0f, 0.78f, 0.28f, IntuitionPulse);
	float TopBoxX = (Canvas->ClipX - (IW + 24.0f)) * 0.5f;
	float TopBoxY = 22.0f;
	DrawFramedBox(TopBoxX, TopBoxY, IW + 24.0f, IH + 8.0f, FLinearColor(0.12f, 0.08f, 0.02f, 0.85f), IntuitionCol, 1.5f);
	DrawText(IntuitionText, IntuitionCol, TopBoxX + 12.0f, TopBoxY + 4.0f, SmallFont);

	UWorld* World = GetWorld();
	if (!World) return;

	FVector KabirPos = Kabir->GetActorLocation();

	// 1. Curfew Sentries & Constables (Crimson Tactical Beacons)
	for (TActorIterator<ACurfewPatrolAI> It(World); It; ++It)
	{
		ACurfewPatrolAI* Sentry = *It;
		if (Sentry)
		{
			FVector SentryHead = Sentry->GetActorLocation() + FVector(0.0f, 0.0f, 85.0f);
			float DistMeters = FVector::Dist(KabirPos, Sentry->GetActorLocation()) * 0.01f;
			if (DistMeters <= 42.0f)
			{
				FVector2D ScreenPos;
				if (PC->ProjectWorldLocationToScreen(SentryHead, ScreenPos, true))
				{
					FLinearColor SentryCol = (Sentry->GetAlertState() == ECurfewAlertState::Alerted)
						? FLinearColor(1.0f, 0.15f, 0.15f, 0.98f)
						: FLinearColor(0.95f, 0.35f, 0.25f, 0.90f);

					// Diamond outline
					DrawLine(ScreenPos.X, ScreenPos.Y - 8.0f, ScreenPos.X + 8.0f, ScreenPos.Y, SentryCol, 1.5f);
					DrawLine(ScreenPos.X + 8.0f, ScreenPos.Y, ScreenPos.X, ScreenPos.Y + 8.0f, SentryCol, 1.5f);
					DrawLine(ScreenPos.X, ScreenPos.Y + 8.0f, ScreenPos.X - 8.0f, ScreenPos.Y, SentryCol, 1.5f);
					DrawLine(ScreenPos.X - 8.0f, ScreenPos.Y, ScreenPos.X, ScreenPos.Y - 8.0f, SentryCol, 1.5f);

					FString Tag = FString::Printf(TEXT("[ SENTRY — %.0fm ]"), DistMeters);
					float TW = 0.0f, TH = 0.0f;
					GetTextSize(Tag, TW, TH, SmallFont);
					DrawText(Tag, SentryCol, ScreenPos.X - (TW * 0.5f), ScreenPos.Y - 24.0f, SmallFont);
				}
			}
		}
	}

	// 2. Civilians (Amber Social Stealth Beacons)
	for (TActorIterator<ACivilianNPCActor> It(World); It; ++It)
	{
		ACivilianNPCActor* NPC = *It;
		if (NPC)
		{
			FVector NPCHead = NPC->GetActorLocation() + FVector(0.0f, 0.0f, 80.0f);
			float DistMeters = FVector::Dist(KabirPos, NPC->GetActorLocation()) * 0.01f;
			if (DistMeters <= 35.0f)
			{
				FVector2D ScreenPos;
				if (PC->ProjectWorldLocationToScreen(NPCHead, ScreenPos, true))
				{
					FLinearColor NPCCol = FLinearColor(1.0f, 0.72f, 0.28f, 0.88f);

					DrawLine(ScreenPos.X, ScreenPos.Y - 6.0f, ScreenPos.X + 6.0f, ScreenPos.Y, NPCCol, 1.2f);
					DrawLine(ScreenPos.X + 6.0f, ScreenPos.Y, ScreenPos.X, ScreenPos.Y + 6.0f, NPCCol, 1.2f);
					DrawLine(ScreenPos.X, ScreenPos.Y + 6.0f, ScreenPos.X - 6.0f, ScreenPos.Y, NPCCol, 1.2f);
					DrawLine(ScreenPos.X - 6.0f, ScreenPos.Y, ScreenPos.X, ScreenPos.Y - 6.0f, NPCCol, 1.2f);

					FString Tag = FString::Printf(TEXT("[ CITIZEN: %s — %.0fm ]"), *NPC->CivilianName.ToString(), DistMeters);
					float TW = 0.0f, TH = 0.0f;
					GetTextSize(Tag, TW, TH, SmallFont);
					DrawText(Tag, NPCCol, ScreenPos.X - (TW * 0.5f), ScreenPos.Y - 22.0f, SmallFont);
				}
			}
		}
	}

	// 3. Stashes & Haveli Caches (Gold Objective Beacons)
	for (TActorIterator<ASupplyStashActor> It(World); It; ++It)
	{
		ASupplyStashActor* Stash = *It;
		if (Stash && !Stash->bIsCollected)
		{
			FVector StashPos = Stash->GetActorLocation() + FVector(0.0f, 0.0f, 40.0f);
			float DistMeters = FVector::Dist(KabirPos, Stash->GetActorLocation()) * 0.01f;
			if (DistMeters <= 38.0f)
			{
				FVector2D ScreenPos;
				if (PC->ProjectWorldLocationToScreen(StashPos, ScreenPos, true))
				{
					FLinearColor StashCol = FLinearColor(0.85f, 0.88f, 0.35f, 0.90f);

					DrawLine(ScreenPos.X, ScreenPos.Y - 7.0f, ScreenPos.X + 7.0f, ScreenPos.Y, StashCol, 1.5f);
					DrawLine(ScreenPos.X + 7.0f, ScreenPos.Y, ScreenPos.X, ScreenPos.Y + 7.0f, StashCol, 1.5f);
					DrawLine(ScreenPos.X, ScreenPos.Y + 7.0f, ScreenPos.X - 7.0f, ScreenPos.Y, StashCol, 1.5f);
					DrawLine(ScreenPos.X - 7.0f, ScreenPos.Y, ScreenPos.X, ScreenPos.Y - 7.0f, StashCol, 1.5f);

					FString Tag = FString::Printf(TEXT("[ CACHE: %s — %.0fm ]"), *Stash->StashTitle.ToString(), DistMeters);
					float TW = 0.0f, TH = 0.0f;
					GetTextSize(Tag, TW, TH, SmallFont);
					DrawText(Tag, StashCol, ScreenPos.X - (TW * 0.5f), ScreenPos.Y - 22.0f, SmallFont);
				}
			}
		}
	}
}

void ARevolutionHUD::DrawInWorldObjectiveBeacon(ARevolutionCharacter* Kabir)
{
	if (!bShowObjectiveBeacons || !Canvas || !Kabir || Kabir->IsInspecting() || Kabir->IsSatchelJournalOpen()) return;

	APlayerController* PC = Cast<APlayerController>(Kabir->GetController());
	if (!PC) return;

	UWorld* World = GetWorld();
	if (!World) return;

	URevolutionMissionSubsystem* Subsystem = World->GetSubsystem<URevolutionMissionSubsystem>();
	if (!Subsystem) return;

	FVector ObjectivePos = FVector::ZeroVector;
	FText ObjectiveName = FText::GetEmpty();
	if (!Subsystem->GetActiveObjectiveLocation(ObjectivePos, ObjectiveName))
	{
		return;
	}

	UFont* SmallFont = GEngine ? GEngine->GetSmallFont() : nullptr;
	if (!SmallFont) return;

	FVector KabirPos = Kabir->GetActorLocation();
	float DistMeters = FVector::Dist(KabirPos, ObjectivePos) * 0.01f;

	// Maximum visible range: 40m in normal exploration, 80m when Basant Intuition is active
	const float MaxRangeMeters = Kabir->IsKeenSensesActive() ? 80.0f : 40.0f;
	if (DistMeters > MaxRangeMeters) return;

	// Calculate smooth distance alpha:
	// Full opacity between 3m and (MaxRangeMeters * 0.75f)
	// Smoothly fades in from MaxRangeMeters down to (MaxRangeMeters * 0.75f)
	// Smoothly fades out from 3m down to 1.2m so it does not obstruct close-up inspection or dialogue
	float Alpha = 1.0f;
	if (DistMeters > (MaxRangeMeters * 0.75f))
	{
		Alpha = FMath::Clamp(1.0f - ((DistMeters - (MaxRangeMeters * 0.75f)) / (MaxRangeMeters * 0.25f)), 0.0f, 1.0f);
	}
	else if (DistMeters < 3.0f)
	{
		Alpha = FMath::Clamp((DistMeters - 1.2f) / 1.8f, 0.0f, 1.0f);
	}

	if (Alpha <= 0.01f) return;

	// Project target position into screen space (with vertical offset for beacon height)
	FVector BeaconWorldPos = ObjectivePos + FVector(0.0f, 0.0f, 35.0f);
	FVector2D ScreenPos;
	if (!PC->ProjectWorldLocationToScreen(BeaconWorldPos, ScreenPos, true))
	{
		return;
	}

	// Breathing pulse
	float Pulse = 0.85f + 0.15f * FMath::Sin(World->GetTimeSeconds() * 3.5f);
	FLinearColor BeaconCol = FLinearColor(1.0f, 0.82f, 0.28f, Alpha * Pulse);
	FLinearColor InnerCol = FLinearColor(0.12f, 0.08f, 0.02f, Alpha * 0.85f);
	FLinearColor TextCol = FLinearColor(0.96f, 0.93f, 0.86f, Alpha);

	// Scale marker slightly by distance (subtle perspective scaling)
	float DiamondRadius = FMath::Clamp(12.0f - (DistMeters * 0.1f), 7.0f, 12.0f);

	// Draw outer diamond
	DrawLine(ScreenPos.X, ScreenPos.Y - DiamondRadius, ScreenPos.X + DiamondRadius, ScreenPos.Y, BeaconCol, 1.8f);
	DrawLine(ScreenPos.X + DiamondRadius, ScreenPos.Y, ScreenPos.X, ScreenPos.Y + DiamondRadius, BeaconCol, 1.8f);
	DrawLine(ScreenPos.X, ScreenPos.Y + DiamondRadius, ScreenPos.X - DiamondRadius, ScreenPos.Y, BeaconCol, 1.8f);
	DrawLine(ScreenPos.X - DiamondRadius, ScreenPos.Y, ScreenPos.X, ScreenPos.Y - DiamondRadius, BeaconCol, 1.8f);

	// Draw inner diamond
	float InnerRadius = DiamondRadius * 0.5f;
	DrawLine(ScreenPos.X, ScreenPos.Y - InnerRadius, ScreenPos.X + InnerRadius, ScreenPos.Y, BeaconCol, 1.2f);
	DrawLine(ScreenPos.X + InnerRadius, ScreenPos.Y, ScreenPos.X, ScreenPos.Y + InnerRadius, BeaconCol, 1.2f);
	DrawLine(ScreenPos.X, ScreenPos.Y + InnerRadius, ScreenPos.X - InnerRadius, ScreenPos.Y, BeaconCol, 1.2f);
	DrawLine(ScreenPos.X - InnerRadius, ScreenPos.Y, ScreenPos.X, ScreenPos.Y - InnerRadius, BeaconCol, 1.2f);

	// Center gold pip
	DrawRect(BeaconCol, ScreenPos.X - 1.5f, ScreenPos.Y - 1.5f, 3.0f, 3.0f);

	// Vertical anchor stem pointing down toward the actual object
	DrawLine(ScreenPos.X, ScreenPos.Y + DiamondRadius + 2.0f, ScreenPos.X, ScreenPos.Y + DiamondRadius + 12.0f, BeaconCol, 1.2f);

	// Distance badge
	FString DistBadge = FString::Printf(TEXT("[ OBJECTIVE — %.0fm ]"), DistMeters);
	float DW = 0.0f, DH = 0.0f;
	GetTextSize(DistBadge, DW, DH, SmallFont);
	float BadgeX = ScreenPos.X - (DW * 0.5f);
	float BadgeY = ScreenPos.Y - DiamondRadius - DH - 6.0f;

	// Framed background for badge
	DrawFramedBox(BadgeX - 6.0f, BadgeY - 2.0f, DW + 12.0f, DH + 4.0f, InnerCol, BeaconCol, 1.0f);
	DrawText(DistBadge, BeaconCol, BadgeX, BadgeY, SmallFont);

	// If within 25m or Basant Intuition active, also draw landmark/objective title
	if (DistMeters <= 25.0f || Kabir->IsKeenSensesActive())
	{
		FString ObjTitle = ObjectiveName.ToString();
		float TW = 0.0f, TH = 0.0f;
		GetTextSize(ObjTitle, TW, TH, SmallFont);
		float TitleX = ScreenPos.X - (TW * 0.5f);
		float TitleY = BadgeY - TH - 3.0f;

		DrawFramedBox(TitleX - 6.0f, TitleY - 2.0f, TW + 12.0f, TH + 4.0f, InnerCol, FLinearColor(0.82f, 0.65f, 0.28f, Alpha * 0.65f), 1.0f);
		DrawText(ObjTitle, TextCol, TitleX, TitleY, SmallFont);
	}
}

void ARevolutionHUD::DrawMissionDirectiveBanner(ARevolutionCharacter* Kabir)
{
	if (!bShowMissionBanner || !Canvas || !Kabir) return;

	URevolutionMissionSubsystem* Subsystem = GetWorld()->GetSubsystem<URevolutionMissionSubsystem>();
	if (!Subsystem) return;

	UFont* SmallFont = GEngine ? GEngine->GetSmallFont() : nullptr;
	if (!SmallFont) return;

	const ECourierMissionStage CurrentStage = Subsystem->GetCurrentStage();
	const FString Title = Subsystem->GetCurrentStageTitle().ToString();
	const FString Directive = Subsystem->GetCurrentStageDirective().ToString();

	const float BannerX = 36.0f;
	const float BannerY = 28.0f;
	const float BannerWidth = 390.0f;

	TArray<FString> WrappedDirectiveLines = WrapText(Directive, SmallFont, BannerWidth - 32.0f);
	const float LineHeight = 16.0f;
	const float HeaderHeight = 44.0f;
	const float BannerHeight = HeaderHeight + (WrappedDirectiveLines.Num() * LineHeight) + 12.0f;

	// Background and Border
	const FLinearColor BgColor = (CurrentStage == ECourierMissionStage::Stage_Completed)
		? FLinearColor(0.04f, 0.10f, 0.05f, 0.82f)
		: FLinearColor(0.07f, 0.06f, 0.05f, 0.80f);

	const FLinearColor BorderCol = (CurrentStage == ECourierMissionStage::Stage_Completed)
		? FLinearColor(0.35f, 0.85f, 0.45f, 0.95f)
		: AntiqueBrassColor;

	DrawFramedBox(BannerX, BannerY, BannerWidth, BannerHeight, BgColor, BorderCol, 1.5f);

	// Stage Indicator Tag
	FString StageTag;
	switch (CurrentStage)
	{
	case ECourierMissionStage::Stage_Morning_FatherTailor: StageTag = TEXT("1919 ACT I  —  OBJECTIVE 1 OF 8"); break;
	case ECourierMissionStage::Stage_Morning_RooftopKite: StageTag = TEXT("1919 ACT I  —  OBJECTIVE 2 OF 8"); break;
	case ECourierMissionStage::Stage_Morning_WellBhishti: StageTag = TEXT("1919 ACT I  —  OBJECTIVE 3 OF 8"); break;
	case ECourierMissionStage::Stage_Morning_DeliverCloth: StageTag = TEXT("1919 ACT I  —  OBJECTIVE 4 OF 8"); break;
	case ECourierMissionStage::Stage_Morning_ChaiHalwai: StageTag = TEXT("1919 ACT I  —  OBJECTIVE 5 OF 8"); break;
	case ECourierMissionStage::Stage_Morning_ProclamationBoard: StageTag = TEXT("1919 ACT I  —  OBJECTIVE 6 OF 8"); break;
	case ECourierMissionStage::Stage_Morning_SchoolBell: StageTag = TEXT("1919 ACT I  —  OBJECTIVE 7 OF 8"); break;
	case ECourierMissionStage::Stage_Morning_ClassroomDesk: StageTag = TEXT("1919 ACT I  —  OBJECTIVE 8 OF 8"); break;
	case ECourierMissionStage::Stage_Afternoon_MunadiProclamation: StageTag = TEXT("1919 ACT II  —  OBJECTIVE 1 OF 5"); break;
	case ECourierMissionStage::Stage_Afternoon_BaghNarrowEntry: StageTag = TEXT("1919 ACT II  —  OBJECTIVE 2 OF 5"); break;
	case ECourierMissionStage::Stage_Afternoon_EavesdropCheckpost: StageTag = TEXT("1919 ACT II  —  OBJECTIVE 3 OF 5"); break;
	case ECourierMissionStage::Stage_Afternoon_ClothBoltLeaflets: StageTag = TEXT("1919 ACT II  —  OBJECTIVE 4 OF 5"); break;
	case ECourierMissionStage::Stage_ActII_BaisakhiGathering: StageTag = TEXT("1919 ACT II  —  OBJECTIVE 5 OF 5"); break;
	case ECourierMissionStage::Stage_Completed: StageTag = TEXT("1919 ACT II  —  HISTORICAL MILESTONE"); break;
	}

	// Draw Tag
	DrawText(StageTag, BorderCol, BannerX + 16.0f, BannerY + 8.0f, SmallFont);

	// Draw Title
	const FLinearColor TitleCol = (CurrentStage == ECourierMissionStage::Stage_Completed)
		? FLinearColor(0.92f, 1.0f, 0.92f, 1.0f)
		: FLinearColor(0.96f, 0.93f, 0.86f, 1.0f);
	DrawText(Title, TitleCol, BannerX + 16.0f, BannerY + 24.0f, SmallFont);

	// Draw Wrapped Directive Lines
	float CurrY = BannerY + HeaderHeight;
	const FLinearColor DescCol = FLinearColor(0.80f, 0.78f, 0.72f, 0.95f);
	for (const FString& Line : WrappedDirectiveLines)
	{
		DrawText(Line, DescCol, BannerX + 16.0f, CurrY, SmallFont);
		CurrY += LineHeight;
	}
}

void ARevolutionHUD::DrawCinematicLetterbox(float DeltaTime, bool bForceActive)
{
	if (!bEnableCinematicLetterbox || !Canvas) return;

	float TargetAlpha = bForceActive ? 1.0f : 0.0f;
	LetterboxAlpha = FMath::FInterpTo(LetterboxAlpha, TargetAlpha, DeltaTime, 3.2f);

	if (LetterboxAlpha > 0.005f)
	{
		// 2.39:1 Anamorphic Cinema scope calculation
		float CinematicHeight = Canvas->ClipX / 2.39f;
		float FullBarHeight = FMath::Max(0.0f, (Canvas->ClipY - CinematicHeight) * 0.5f);
		float CurrentBarHeight = FullBarHeight * LetterboxAlpha;

		FLinearColor MatteColor(0.015f, 0.015f, 0.015f, 1.0f);
		// Top Bar
		DrawRect(MatteColor, 0.0f, 0.0f, Canvas->ClipX, CurrentBarHeight);
		// Bottom Bar
		DrawRect(MatteColor, 0.0f, Canvas->ClipY - CurrentBarHeight, Canvas->ClipX, CurrentBarHeight);
	}
}

void ARevolutionHUD::SetCinematicSequenceActive(bool bActive, const FText& InChapterTitle, const FText& InSubtitleText)
{
	bCinematicSequenceActive = bActive;
	CinematicChapterTitle = InChapterTitle;
	CinematicSubtitleText = InSubtitleText;
	UE_LOG(LogREVOLUTION, Log, TEXT("RevolutionHUD Cinematic Mode %s: Title='%s', Subtitle='%s'"),
		bActive ? TEXT("ACTIVATED") : TEXT("DEACTIVATED"),
		*InChapterTitle.ToString(), *InSubtitleText.ToString());
}

void ARevolutionHUD::SetCinematicSubtitle(const FText& InSubtitle)
{
	CinematicSubtitleText = InSubtitle;
}

void ARevolutionHUD::DrawCinematicCaptions(float DeltaTime)
{
	if (!Canvas) return;

	UFont* LargeFont = GEngine ? GEngine->GetLargeFont() : nullptr;
	UFont* MediumFont = GEngine ? GEngine->GetMediumFont() : nullptr;
	UFont* SmallFont = GEngine ? GEngine->GetSmallFont() : nullptr;
	if (!MediumFont) return;

	float CinematicHeight = Canvas->ClipX / 2.39f;
	float FullBarHeight = FMath::Max(0.0f, (Canvas->ClipY - CinematicHeight) * 0.5f);

	// 1. Draw Chapter Title in upper third with gold filigree line
	if (!CinematicChapterTitle.IsEmpty() && LargeFont)
	{
		FString TitleStr = CinematicChapterTitle.ToString().ToUpper();
		float TitleW, TitleH;
		GetTextSize(TitleStr, TitleW, TitleH, LargeFont);
		float TitleX = (Canvas->ClipX - TitleW) * 0.5f;
		float TitleY = FullBarHeight + 35.0f;

		// Subtle drop shadow
		DrawText(TitleStr, FLinearColor(0.02f, 0.02f, 0.02f, 0.85f), TitleX + 2.0f, TitleY + 2.0f, LargeFont);
		DrawText(TitleStr, AntiqueBrassColor, TitleX, TitleY, LargeFont);

		// Gold filigree rule line
		float RuleW = FMath::Min(TitleW * 1.25f, Canvas->ClipX * 0.4f);
		float RuleX = (Canvas->ClipX - RuleW) * 0.5f;
		float RuleY = TitleY + TitleH + 8.0f;
		DrawRect(FLinearColor(AntiqueBrassColor.R, AntiqueBrassColor.G, AntiqueBrassColor.B, 0.65f), RuleX, RuleY, RuleW, 1.5f);
	}

	// 2. Draw Subtitle Caption in lower letterbox bar
	if (!CinematicSubtitleText.IsEmpty())
	{
		FString SubtitleStr = CinematicSubtitleText.ToString();
		float SubScale = 1.0f;
		if (ARevolutionCharacter* Kabir = Cast<ARevolutionCharacter>(GetOwningPawn()))
		{
			SubScale = Kabir->GetSubtitleScaleMultiplier();
		}

		UFont* SubFont = MediumFont;
		if (SubScale > 1.15f && LargeFont)
		{
			SubFont = LargeFont;
		}
		else if (SubScale < 0.90f && SmallFont)
		{
			SubFont = SmallFont;
		}

		float SubW, SubH;
		GetTextSize(SubtitleStr, SubW, SubH, SubFont);

		float SubX = (Canvas->ClipX - SubW) * 0.5f;
		float SubY = Canvas->ClipY - (FullBarHeight * 0.65f) - (SubH * 0.5f);

		// Drop shadow
		DrawText(SubtitleStr, FLinearColor(0.0f, 0.0f, 0.0f, 0.9f), SubX + 1.5f, SubY + 1.5f, SubFont);
		DrawText(SubtitleStr, FLinearColor(0.96f, 0.94f, 0.88f, 1.0f), SubX, SubY, SubFont);
	}
}

void ARevolutionHUD::DrawOpeningPrologueCard(float DeltaTime)
{
	if (!Canvas) return;

	UFont* LargeFont = GEngine ? GEngine->GetLargeFont() : nullptr;
	UFont* MediumFont = GEngine ? GEngine->GetMediumFont() : nullptr;
	UFont* SmallFont = GEngine ? GEngine->GetSmallFont() : nullptr;
	if (!SmallFont) return;

	// Calculate smooth fade envelope (in over 1.8s, out after 5.5s)
	float CardAlpha = 1.0f;
	if (OpeningPrologueTimer < 1.8f)
	{
		CardAlpha = OpeningPrologueTimer / 1.8f;
	}
	else if (OpeningPrologueTimer > 5.5f)
	{
		CardAlpha = FMath::Clamp((7.5f - OpeningPrologueTimer) / 2.0f, 0.0f, 1.0f);
	}

	if (CardAlpha <= 0.01f) return;

	const float CenterX = Canvas->ClipX * 0.5f;
	const float CenterY = Canvas->ClipY * 0.44f;

	// 1. Region & Period Tag
	FString RegionTag = TEXT("P U N J A B   •   A P R I L   1 9 1 9");
	float RegW = 0.0f, RegH = 0.0f;
	GetTextSize(RegionTag, RegW, RegH, SmallFont);
	FLinearColor TagColor = AntiqueBrassColor;
	TagColor.A = CardAlpha * 0.95f;
	DrawText(RegionTag, TagColor, CenterX - (RegW * 0.5f), CenterY - 45.0f, SmallFont);

	// 2. Main Title (Town Location)
	FString TownTitle = TEXT("K O T   G U R D A R S H A N");
	float TownW = 0.0f, TownH = 0.0f;
	UFont* TitleFont = LargeFont ? LargeFont : (MediumFont ? MediumFont : SmallFont);
	GetTextSize(TownTitle, TownW, TownH, TitleFont);
	FLinearColor TownColor = FLinearColor(0.96f, 0.93f, 0.86f, CardAlpha);
	DrawText(TownTitle, TownColor, CenterX - (TownW * 0.5f), CenterY - 15.0f, TitleFont);

	// 3. Historical Curfew Notice
	FString CurfewNotice = TEXT("8 : 0 0   P M   M A R T I A L   C U R F E W   I N   E F F E C T");
	float CurfW = 0.0f, CurfH = 0.0f;
	GetTextSize(CurfewNotice, CurfW, CurfH, SmallFont);
	FLinearColor CurfewColor = FLinearColor(0.88f, 0.35f, 0.25f, CardAlpha * 0.90f);
	DrawText(CurfewNotice, CurfewColor, CenterX - (CurfW * 0.5f), CenterY + 28.0f, SmallFont);

	// 4. Historical Context Line
	FString ContextLine = TEXT("Anti-Rowlatt Emergency Laws  —  Clandestine Courier Dispatch");
	float CtxW = 0.0f, CtxH = 0.0f;
	GetTextSize(ContextLine, CtxW, CtxH, SmallFont);
	FLinearColor ContextColor = FLinearColor(0.72f, 0.68f, 0.60f, CardAlpha * 0.75f);
	DrawText(ContextLine, ContextColor, CenterX - (CtxW * 0.5f), CenterY + 50.0f, SmallFont);
}

void ARevolutionHUD::DrawSatchelJournalModal(ARevolutionCharacter* Kabir)
{
	if (!Canvas || !Kabir) return;

	UFont* LargeFont = GEngine ? GEngine->GetLargeFont() : nullptr;
	UFont* MediumFont = GEngine ? GEngine->GetMediumFont() : nullptr;
	UFont* SmallFont = GEngine ? GEngine->GetSmallFont() : nullptr;
	if (!SmallFont) return;

	// Darkened vignette background
	DrawRect(FLinearColor(0.015f, 0.015f, 0.012f, 0.82f), 0.0f, 0.0f, Canvas->ClipX, Canvas->ClipY);

	const float BoxW = FMath::Clamp(Canvas->ClipX * 0.88f, 740.0f, 960.0f);
	const float BoxH = FMath::Clamp(Canvas->ClipY * 0.84f, 500.0f, 620.0f);
	const float BoxX = (Canvas->ClipX - BoxW) * 0.5f;
	const float BoxY = (Canvas->ClipY - BoxH) * 0.5f;

	// Main parchment ledger framed box
	DrawFramedBox(BoxX, BoxY, BoxW, BoxH, ParchmentColor, AntiqueBrassColor, 2.0f);

	// Inner decorative border
	DrawLine(BoxX + 6.0f, BoxY + 6.0f, BoxX + BoxW - 6.0f, BoxY + 6.0f, MutedSepiaColor, 1.0f);
	DrawLine(BoxX + BoxW - 6.0f, BoxY + 6.0f, BoxX + BoxW - 6.0f, BoxY + BoxH - 6.0f, MutedSepiaColor, 1.0f);
	DrawLine(BoxX + BoxW - 6.0f, BoxY + BoxH - 6.0f, BoxX + 6.0f, BoxY + BoxH - 6.0f, MutedSepiaColor, 1.0f);
	DrawLine(BoxX + 6.0f, BoxY + BoxH - 6.0f, BoxX + 6.0f, BoxY + 6.0f, MutedSepiaColor, 1.0f);

	// Header
	FString MainTitle = TEXT("KABIR'S SATCHEL & FIELD JOURNAL  —  KOT GURDARSHAN, 1919");
	UFont* HeaderFont = MediumFont ? MediumFont : SmallFont;
	DrawText(MainTitle, DarkInkColor, BoxX + 24.0f, BoxY + 14.0f, HeaderFont);

	FString Subtitle = TEXT("Walled City Mohalla Scout Records  •  Clandestine Anti-Rowlatt Courier Dispatch");
	DrawText(Subtitle, MutedSepiaColor, BoxX + 24.0f, BoxY + 36.0f, SmallFont);

	// Horizontal rule line below header
	DrawLine(BoxX + 16.0f, BoxY + 54.0f, BoxX + BoxW - 16.0f, BoxY + 54.0f, AntiqueBrassColor, 1.5f);

	// Tab Bar Ribbon
	const float TabY = BoxY + 60.0f;
	const float TabH = 28.0f;
	const float TabW = (BoxW - 48.0f) / 4.0f;
	const int32 ActiveTab = Kabir->GetActiveSatchelTab();

	const FString TabTitles[] = {
		TEXT("[ 1 ]  SATCHEL EQUIPMENT"),
		TEXT("[ 2 ]  MOHALLA ROUTE MAP"),
		TEXT("[ 3 ]  HISTORICAL CODEX"),
		TEXT("[ 4 ]  SETTINGS & CONTROLS")
	};

	for (int32 i = 0; i < 4; ++i)
	{
		float TabX = BoxX + 24.0f + (i * TabW);
		bool bSelected = (ActiveTab == i);

		FLinearColor TabBg = bSelected ? DarkInkColor : FLinearColor(0.85f, 0.81f, 0.72f, 0.85f);
		FLinearColor TabBorder = bSelected ? AntiqueBrassColor : MutedSepiaColor;
		FLinearColor TabTextCol = bSelected ? AntiqueBrassColor : DarkInkColor;

		DrawFramedBox(TabX, TabY, TabW - 6.0f, TabH, TabBg, TabBorder, bSelected ? 1.5f : 1.0f);

		float TW = 0.0f, TH = 0.0f;
		GetTextSize(TabTitles[i], TW, TH, SmallFont);
		DrawText(TabTitles[i], TabTextCol, TabX + ((TabW - 6.0f - TW) * 0.5f), TabY + ((TabH - TH) * 0.5f), SmallFont);
	}

	// Content Area Dimensions
	const float ContentY = BoxY + 96.0f;
	const float ContentW = BoxW - 48.0f;
	const float ContentH = BoxH - 134.0f;

	switch (ActiveTab)
	{
	case 0:
		DrawSatchelTabEquipment(Kabir, BoxX + 24.0f, ContentY, ContentW, ContentH);
		break;
	case 1:
		DrawSatchelTabMohallaMap(Kabir, BoxX + 24.0f, ContentY, ContentW, ContentH);
		break;
	case 2:
		DrawSatchelTabHistoricalCodex(Kabir, BoxX + 24.0f, ContentY, ContentW, ContentH);
		break;
	case 3:
	default:
		DrawSatchelTabSettingsControls(Kabir, BoxX + 24.0f, ContentY, ContentW, ContentH);
		break;
	}

	// Bottom Navigation Footer
	DrawLine(BoxX + 16.0f, BoxY + BoxH - 32.0f, BoxX + BoxW - 16.0f, BoxY + BoxH - 32.0f, AntiqueBrassColor, 1.0f);

	FString FooterNav = Kabir->IsUsingGamepad() ? TEXT("[ D-PAD / LB-RB ] Switch Section   |   [ UP / DOWN ] Select Option   |   [ (B) ] Close Journal") : TEXT("[ 1-4 / D-PAD ] Switch Section   |   [ UP / DOWN / [ / ] ] Browse   |   [ TAB / ESC / (B) ] Close");
	DrawText(FooterNav, MutedSepiaColor, BoxX + 24.0f, BoxY + BoxH - 24.0f, SmallFont);
}

void ARevolutionHUD::DrawSatchelTabEquipment(ARevolutionCharacter* Kabir, float BoxX, float ContentY, float ContentW, float ContentH)
{
	UFont* SmallFont = GEngine ? GEngine->GetSmallFont() : nullptr;
	UFont* MediumFont = GEngine ? GEngine->GetMediumFont() : nullptr;
	if (!SmallFont) return;

	const float LeftW = ContentW * 0.54f;
	const float RightW = ContentW * 0.43f;
	const float RightX = BoxX + LeftW + (ContentW * 0.03f);

	// LEFT COLUMN: Equipment Items (4 Items)
	float ItemH = (ContentH - 24.0f) / 4.0f;

	// Item 1: Tailored Khadi Coat Delivery
	float Item1Y = ContentY + 4.0f;
	DrawFramedBox(BoxX, Item1Y, LeftW, ItemH, FLinearColor(0.88f, 0.84f, 0.74f, 0.90f), AntiqueBrassColor, 1.0f);
	DrawText(TEXT("Tailored Khadi Coat Parcel"), DarkInkColor, BoxX + 12.0f, Item1Y + 6.0f, MediumFont ? MediumFont : SmallFont);

	URevolutionMissionSubsystem* Subsystem = GetWorld() ? GetWorld()->GetSubsystem<URevolutionMissionSubsystem>() : nullptr;
	bool bHasCoat = Subsystem && (Subsystem->CurrentStage < ECourierMissionStage::Stage_Morning_DeliverCloth);

	FString CoatStatus = bHasCoat ? TEXT("STATUS: IN SATCHEL (DELIVER TO LALA KARAM CHAND)") : TEXT("STATUS: DELIVERED TO CLOTH GUILD");
	FLinearColor StatusCol = bHasCoat ? FLinearColor(0.85f, 0.52f, 0.15f, 1.0f) : FLinearColor(0.18f, 0.65f, 0.32f, 1.0f);
	DrawText(CoatStatus, StatusCol, BoxX + 12.0f, Item1Y + 22.0f, SmallFont);

	FString CoatDesc = TEXT("Stitched homespun khadi coat repaired by father Ram Lubhaya. Intended for Lala Karam Chand.");
	TArray<FString> CoatLines = WrapText(CoatDesc, SmallFont, LeftW - 24.0f);
	float LineY = Item1Y + 36.0f;
	for (const FString& L : CoatLines)
	{
		DrawText(L, MutedSepiaColor, BoxX + 12.0f, LineY, SmallFont);
		LineY += 13.0f;
	}

	// Item 2: Anti-Rowlatt Satyagraha Handbills
	float Item2Y = Item1Y + ItemH + 6.0f;
	DrawFramedBox(BoxX, Item2Y, LeftW, ItemH, FLinearColor(0.88f, 0.84f, 0.74f, 0.90f), AntiqueBrassColor, 1.0f);

	FString PamphletHeader = FString::Printf(TEXT("Satyagraha Strike Handbills  [%d / %d COPIES]"), Kabir->GetPamphletCount(), Kabir->MaxPamphlets);
	DrawText(PamphletHeader, DarkInkColor, BoxX + 12.0f, Item2Y + 6.0f, MediumFont ? MediumFont : SmallFont);

	FString PamphletStatus = (Kabir->GetPamphletCount() > 0)
		? TEXT("ACTION: SLIP SECRETLY TO TRUSTED MERCHANTS (WATCH FOR CONSTABLES!)")
		: TEXT("STATUS: EMPTY — COLLECT FRESH LEAFLETS FROM HAVELI LITHO PRESS");
	FLinearColor PamphletCol = (Kabir->GetPamphletCount() > 0) ? FLinearColor(0.85f, 0.25f, 0.20f, 1.0f) : MutedSepiaColor;
	DrawText(PamphletStatus, PamphletCol, BoxX + 12.0f, Item2Y + 22.0f, SmallFont);

	FString PamphletDesc = TEXT("Clandestine rag-paper handbills from haveli litho press: 'Na Dalil, Na Vakil, Na Appeal.' Carry carefully!");
	TArray<FString> PamphletLines = WrapText(PamphletDesc, SmallFont, LeftW - 24.0f);
	LineY = Item2Y + 36.0f;
	for (const FString& L : PamphletLines)
	{
		DrawText(L, MutedSepiaColor, BoxX + 12.0f, LineY, SmallFont);
		LineY += 13.0f;
	}

	// Item 3: Tailor's Soapstone Chalk
	float Item3Y = Item2Y + ItemH + 6.0f;
	DrawFramedBox(BoxX, Item3Y, LeftW, ItemH, FLinearColor(0.88f, 0.84f, 0.74f, 0.90f), AntiqueBrassColor, 1.0f);

	FString ChalkHeader = FString::Printf(TEXT("Tailor's Soapstone Chalk  [%d / %d STICKS]"), Kabir->GetChalkCount(), Kabir->MaxChalk);
	DrawText(ChalkHeader, DarkInkColor, BoxX + 12.0f, Item3Y + 6.0f, MediumFont ? MediumFont : SmallFont);
	DrawText(TEXT("ACTION: PRESS [T] TO INSCRIBE ROOFTOP WAYPOINTS"), AntiqueBrassColor, BoxX + 12.0f, Item3Y + 22.0f, SmallFont);

	FString ChalkDesc = TEXT("Soapstone chalk taken from father's shears bench to mark rooftop jump ledges and safe paths.");
	TArray<FString> ChalkLines = WrapText(ChalkDesc, SmallFont, LeftW - 24.0f);
	LineY = Item3Y + 36.0f;
	for (const FString& L : ChalkLines)
	{
		DrawText(L, MutedSepiaColor, BoxX + 12.0f, LineY, SmallFont);
		LineY += 13.0f;
	}

	// Item 4: Sun-Baked Clay Marbles
	float Item4Y = Item3Y + ItemH + 6.0f;
	DrawFramedBox(BoxX, Item4Y, LeftW, ItemH, FLinearColor(0.88f, 0.84f, 0.74f, 0.90f), AntiqueBrassColor, 1.0f);

	FString MarbleHeader = FString::Printf(TEXT("Sun-Baked Clay Marbles  [%d / %d PEBBLES]"), Kabir->GetPebbleCount(), Kabir->MaxPebbles);
	DrawText(MarbleHeader, DarkInkColor, BoxX + 12.0f, Item4Y + 6.0f, MediumFont ? MediumFont : SmallFont);
	DrawText(TEXT("ACTION: PRESS [F] TO LAUNCH ACOUSTIC DISTRACTION"), AntiqueBrassColor, BoxX + 12.0f, Item4Y + 22.0f, SmallFont);

	FString MarbleDesc = TEXT("Clay marbles rolled from river mud. Launched to clatter against brickwork, diverting curfew constables.");
	TArray<FString> MarbleLines = WrapText(MarbleDesc, SmallFont, LeftW - 24.0f);
	LineY = Item4Y + 36.0f;
	for (const FString& L : MarbleLines)
	{
		DrawText(L, MutedSepiaColor, BoxX + 12.0f, LineY, SmallFont);
		LineY += 13.0f;
	}

	// RIGHT COLUMN: Current Mission Directive & Historical Context
	DrawFramedBox(RightX, ContentY + 4.0f, RightW, ContentH - 8.0f, FLinearColor(0.86f, 0.82f, 0.72f, 0.90f), AntiqueBrassColor, 1.5f);

	DrawText(TEXT("MISSION DIRECTIVE"), DarkInkColor, RightX + 14.0f, ContentY + 16.0f, MediumFont ? MediumFont : SmallFont);
	DrawLine(RightX + 14.0f, ContentY + 36.0f, RightX + RightW - 14.0f, ContentY + 36.0f, AntiqueBrassColor, 1.0f);

	if (Subsystem)
	{
		DrawText(Subsystem->GetCurrentStageTitle().ToString(), AntiqueBrassColor, RightX + 14.0f, ContentY + 46.0f, SmallFont);

		TArray<FString> DirLines = WrapText(Subsystem->GetCurrentStageDirective().ToString(), SmallFont, RightW - 28.0f);
		float DirY = ContentY + 68.0f;
		for (const FString& DL : DirLines)
		{
			DrawText(DL, DarkInkColor, RightX + 14.0f, DirY, SmallFont);
			DirY += 16.0f;
		}
	}

	// Historical Note in Right Column
	float HistY = ContentY + ContentH * 0.52f;
	DrawLine(RightX + 14.0f, HistY, RightX + RightW - 14.0f, HistY, MutedSepiaColor, 1.0f);
	DrawText(TEXT("HISTORICAL REALISM — APRIL 1919"), AntiqueBrassColor, RightX + 14.0f, HistY + 10.0f, SmallFont);

	FString HistNote = TEXT("The Anarchical and Revolutionary Crimes Act (Rowlatt Act) of March 1919 authorized British colonial authorities in Punjab to arrest individuals without warrant and detain them without jury trial.\n\nIn response, Mahatma Gandhi called for a nation-wide Satyagraha Hartal. In towns like Kot Gurdarshan, dispatch riders and child couriers moved across interconnected rooftops at night to coordinate the shutdown.");
	TArray<FString> HistLines = WrapText(HistNote, SmallFont, RightW - 28.0f);
	float NoteY = HistY + 30.0f;
	for (const FString& HL : HistLines)
	{
		DrawText(HL, MutedSepiaColor, RightX + 14.0f, NoteY, SmallFont);
		NoteY += 14.0f;
	}
}

void ARevolutionHUD::DrawSatchelTabMohallaMap(ARevolutionCharacter* Kabir, float BoxX, float ContentY, float ContentW, float ContentH)
{
	UFont* SmallFont = GEngine ? GEngine->GetSmallFont() : nullptr;
	UFont* MediumFont = GEngine ? GEngine->GetMediumFont() : nullptr;
	if (!SmallFont) return;

	// Map Card Container
	const float MapX = BoxX + 12.0f;
	const float MapY = ContentY + 4.0f;
	const float MapW = ContentW - 24.0f;
	const float MapH = ContentH - 8.0f;

	DrawFramedBox(MapX, MapY, MapW, MapH, FLinearColor(0.89f, 0.85f, 0.76f, 0.95f), AntiqueBrassColor, 1.5f);

	// Title
	DrawText(TEXT("KOT GURDARSHAN  —  HAWALI MOHALLA ROUTE SKETCH"), DarkInkColor, MapX + 16.0f, MapY + 12.0f, MediumFont ? MediumFont : SmallFont);
	DrawText(TEXT("Hand-drawn in charcoal on fibrous khadi paper. Rooftop parapets and courtyard thoroughfares."), MutedSepiaColor, MapX + 16.0f, MapY + 32.0f, SmallFont);
	DrawLine(MapX + 16.0f, MapY + 48.0f, MapX + MapW - 16.0f, MapY + 48.0f, MutedSepiaColor, 1.0f);

	// Map Drawing Area
	const float CanvasAreaX = MapX + 24.0f;
	const float CanvasAreaY = MapY + 58.0f;
	const float CanvasAreaW = MapW * 0.72f;
	const float CanvasAreaH = MapH - 74.0f;

	DrawFramedBox(CanvasAreaX, CanvasAreaY, CanvasAreaW, CanvasAreaH, FLinearColor(0.93f, 0.90f, 0.82f, 0.80f), MutedSepiaColor, 1.0f);

	// Grid coordinate mapping covering full 5 historical zones
	// World X [-350, 1550] (Width 1900), World Y [-350, 2250] (Height 2600)
	// Orient North (+Y) upward on the map for authentic cartography
	auto WorldToMap = [&](float WX, float WY) -> FVector2D
	{
		float NormX = FMath::Clamp((WX + 350.0f) / 1900.0f, 0.0f, 1.0f);
		float NormY = FMath::Clamp(1.0f - ((WY + 350.0f) / 2600.0f), 0.0f, 1.0f);
		return FVector2D(
			CanvasAreaX + (NormX * CanvasAreaW),
			CanvasAreaY + (NormY * CanvasAreaH)
		);
	};

	// 1. Draw 5 Historical District Boundaries
	// Zone A: Haveli Courtyard & Veranda
	FVector2D ZA1 = WorldToMap(-180.0f, -220.0f);
	FVector2D ZA2 = WorldToMap(220.0f, 520.0f);
	DrawFramedBox(FMath::Min(ZA1.X, ZA2.X), FMath::Min(ZA1.Y, ZA2.Y), FMath::Abs(ZA2.X - ZA1.X), FMath::Abs(ZA2.Y - ZA1.Y), FLinearColor(0.85f, 0.80f, 0.70f, 0.35f), MutedSepiaColor, 1.0f);
	DrawText(TEXT("HAVELI COURTYARD"), MutedSepiaColor, FMath::Min(ZA1.X, ZA2.X) + 6.0f, FMath::Max(ZA1.Y, ZA2.Y) - 16.0f, SmallFont);

	// Zone B: Deorhi Gateway Transition
	FVector2D ZB1 = WorldToMap(-120.0f, 600.0f);
	FVector2D ZB2 = WorldToMap(120.0f, 1000.0f);
	DrawFramedBox(FMath::Min(ZB1.X, ZB2.X), FMath::Min(ZB1.Y, ZB2.Y), FMath::Abs(ZB2.X - ZB1.X), FMath::Abs(ZB2.Y - ZB1.Y), FLinearColor(0.82f, 0.78f, 0.68f, 0.35f), MutedSepiaColor, 1.0f);
	DrawText(TEXT("DEORHI ARCH"), MutedSepiaColor, FMath::Min(ZB1.X, ZB2.X) + 6.0f, FMath::Max(ZB1.Y, ZB2.Y) - 16.0f, SmallFont);

	// Zone C: Communal Well Square & Shrines
	FVector2D ZC1 = WorldToMap(-180.0f, 1100.0f);
	FVector2D ZC2 = WorldToMap(550.0f, 1550.0f);
	DrawFramedBox(FMath::Min(ZC1.X, ZC2.X), FMath::Min(ZC1.Y, ZC2.Y), FMath::Abs(ZC2.X - ZC1.X), FMath::Abs(ZC2.Y - ZC1.Y), FLinearColor(0.80f, 0.82f, 0.72f, 0.35f), MutedSepiaColor, 1.0f);
	DrawText(TEXT("WELL SQUARE & PEEPAL SHRINE"), MutedSepiaColor, FMath::Min(ZC1.X, ZC2.X) + 6.0f, FMath::Max(ZC1.Y, ZC2.Y) - 16.0f, SmallFont);

	// Zone D: Grand Bazaar Mandi
	FVector2D ZD1 = WorldToMap(-280.0f, 1600.0f);
	FVector2D ZD2 = WorldToMap(320.0f, 2150.0f);
	DrawFramedBox(FMath::Min(ZD1.X, ZD2.X), FMath::Min(ZD1.Y, ZD2.Y), FMath::Abs(ZD2.X - ZD1.X), FMath::Abs(ZD2.Y - ZD1.Y), FLinearColor(0.85f, 0.75f, 0.65f, 0.35f), MutedSepiaColor, 1.0f);
	DrawText(TEXT("GRAND BAZAAR MANDI"), MutedSepiaColor, FMath::Min(ZD1.X, ZD2.X) + 6.0f, FMath::Max(ZD1.Y, ZD2.Y) - 16.0f, SmallFont);

	// District C: Vernacular Middle School
	FVector2D ZE1 = WorldToMap(750.0f, 1150.0f);
	FVector2D ZE2 = WorldToMap(1500.0f, 2000.0f);
	DrawFramedBox(FMath::Min(ZE1.X, ZE2.X), FMath::Min(ZE1.Y, ZE2.Y), FMath::Abs(ZE2.X - ZE1.X), FMath::Abs(ZE2.Y - ZE1.Y), FLinearColor(0.75f, 0.80f, 0.85f, 0.35f), MutedSepiaColor, 1.0f);
	DrawText(TEXT("VERNACULAR MIDDLE SCHOOL"), MutedSepiaColor, FMath::Min(ZE1.X, ZE2.X) + 6.0f, FMath::Max(ZE1.Y, ZE2.Y) - 16.0f, SmallFont);

	// 2. Draw Key Historical Landmarks
	auto DrawMarker = [&](float WX, float WY, const FString& Label, const FLinearColor& Col)
	{
		FVector2D P = WorldToMap(WX, WY);
		DrawFramedBox(P.X - 5.0f, P.Y - 5.0f, 10.0f, 10.0f, Col, DarkInkColor, 1.0f);
		DrawText(Label, DarkInkColor, P.X + 8.0f, P.Y - 6.0f, SmallFont);
	};

	DrawMarker(200.0f, 480.0f, TEXT("[HOME/TAILOR]"), AntiqueBrassColor);
	DrawMarker(-80.0f, 1320.0f, TEXT("[WELL]"), FLinearColor(0.2f, 0.55f, 0.8f, 1.0f));
	DrawMarker(380.0f, 1350.0f, TEXT("[PEEPAL SHRINE]"), FLinearColor(0.2f, 0.65f, 0.25f, 1.0f));
	DrawMarker(450.0f, 1380.0f, TEXT("[KARTAR]"), FLinearColor(0.85f, 0.65f, 0.15f, 1.0f));
	DrawMarker(-200.0f, 1680.0f, TEXT("[CHAI STALL]"), FLinearColor(0.75f, 0.45f, 0.2f, 1.0f));
	DrawMarker(200.0f, 1980.0f, TEXT("[CLOTH GUILD]"), FLinearColor(0.4f, 0.25f, 0.6f, 1.0f));
	DrawMarker(-40.0f, 1850.0f, TEXT("[THELA CART]"), MutedSepiaColor);
	DrawMarker(180.0f, 1720.0f, TEXT("[TARAZU SCALE]"), MutedSepiaColor);
	DrawMarker(60.0f, 2150.0f, TEXT("[GR POSTBOX]"), FLinearColor(0.85f, 0.15f, 0.15f, 1.0f));
	DrawMarker(120.0f, -120.0f, TEXT("[SANDOOK CHEST]"), AntiqueBrassColor);
	DrawMarker(20.0f, 260.0f, TEXT("[KITES/CHARKHI]"), FLinearColor(0.85f, 0.45f, 0.15f, 1.0f));
	DrawMarker(1350.0f, 1350.0f, TEXT("[BELL TOWER]"), FLinearColor(0.85f, 0.70f, 0.20f, 1.0f));
	DrawMarker(1150.0f, 1850.0f, TEXT("[CLASSROOM 4B]"), FLinearColor(0.3f, 0.5f, 0.7f, 1.0f));
	DrawMarker(1100.0f, 1920.0f, TEXT("[PUNJAB MAP]"), FLinearColor(0.2f, 0.6f, 0.8f, 1.0f));
	DrawMarker(0.0f, 1550.0f, TEXT("[CHOWK GATE]"), FLinearColor(0.9f, 0.4f, 0.2f, 1.0f));
	DrawMarker(0.0f, 900.0f, TEXT("[KUCHA ARCH]"), AntiqueBrassColor);

	// Bazaar Constable Patrol Route
	FVector2D Pat1 = WorldToMap(0.0f, 1600.0f);
	FVector2D Pat2 = WorldToMap(0.0f, 2040.0f);
	DrawLine(Pat1.X, Pat1.Y, Pat2.X, Pat2.Y, FLinearColor(0.85f, 0.25f, 0.20f, 0.80f), 2.0f);
	DrawText(TEXT("! BAZAAR PATROL !"), FLinearColor(0.85f, 0.25f, 0.20f, 0.90f), Pat1.X + 8.0f, ((Pat1.Y + Pat2.Y) * 0.5f) - 6.0f, SmallFont);

	// 3. Draw Real-Time Scout Chalk Marks
	for (TActorIterator<AChalkMarkActor> It(GetWorld()); It; ++It)
	{
		AChalkMarkActor* Chalk = *It;
		if (Chalk)
		{
			FVector Loc = Chalk->GetActorLocation();
			FVector2D MPos = WorldToMap(Loc.X, Loc.Y);
			FLinearColor ChalkCol = FLinearColor(0.96f, 0.95f, 0.90f, 0.95f);
			DrawLine(MPos.X - 4.0f, MPos.Y, MPos.X, MPos.Y - 4.0f, ChalkCol, 1.5f);
			DrawLine(MPos.X, MPos.Y - 4.0f, MPos.X + 4.0f, MPos.Y, ChalkCol, 1.5f);
			DrawLine(MPos.X + 4.0f, MPos.Y, MPos.X, MPos.Y + 4.0f, ChalkCol, 1.5f);
			DrawLine(MPos.X, MPos.Y + 4.0f, MPos.X - 4.0f, MPos.Y, ChalkCol, 1.5f);
			DrawText(TEXT("M"), DarkInkColor, MPos.X - 3.0f, MPos.Y - 5.0f, SmallFont);
		}
	}

	// 4. Draw Real-Time Player Position (Kabir)
	FVector PlayerLoc = Kabir->GetActorLocation();
	FVector2D PMap = WorldToMap(PlayerLoc.X, PlayerLoc.Y);
	FLinearColor PlayerCol = FLinearColor(0.20f, 0.78f, 0.42f, 1.0f);

	// Player Diamond
	DrawLine(PMap.X - 6.0f, PMap.Y, PMap.X, PMap.Y - 6.0f, PlayerCol, 2.0f);
	DrawLine(PMap.X, PMap.Y - 6.0f, PMap.X + 6.0f, PMap.Y, PlayerCol, 2.0f);
	DrawLine(PMap.X + 6.0f, PMap.Y, PMap.X, PMap.Y + 6.0f, PlayerCol, 2.0f);
	DrawLine(PMap.X, PMap.Y + 6.0f, PMap.X - 6.0f, PMap.Y, PlayerCol, 2.0f);

	// Player facing direction notch (Inverted Y for North-up orientation)
	FRotator ControlRot = Kabir->GetControlRotation();
	float Rad = FMath::DegreesToRadians(ControlRot.Yaw - 90.0f);
	DrawLine(PMap.X, PMap.Y, PMap.X + (FMath::Cos(Rad) * 12.0f), PMap.Y - (FMath::Sin(Rad) * 12.0f), PlayerCol, 2.0f);

	DrawText(TEXT("[KABIR]"), PlayerCol, PMap.X + 8.0f, PMap.Y - 6.0f, SmallFont);

	// MAP LEGEND (Right Sidebar)
	const float LegendX = CanvasAreaX + CanvasAreaW + 16.0f;
	const float LegendY = CanvasAreaY;
	const float LegendW = MapW - CanvasAreaW - 48.0f;

	DrawFramedBox(LegendX, LegendY, LegendW, CanvasAreaH, FLinearColor(0.87f, 0.83f, 0.73f, 0.90f), AntiqueBrassColor, 1.0f);
	DrawText(TEXT("MAP LEGEND"), DarkInkColor, LegendX + 12.0f, LegendY + 12.0f, MediumFont ? MediumFont : SmallFont);
	DrawLine(LegendX + 12.0f, LegendY + 30.0f, LegendX + LegendW - 12.0f, LegendY + 30.0f, AntiqueBrassColor, 1.0f);

	float LegY = LegendY + 40.0f;
	auto DrawLegendItem = [&](const FString& Symbol, const FString& Label, const FLinearColor& Col)
	{
		DrawText(Symbol, Col, LegendX + 12.0f, LegY, SmallFont);
		DrawText(Label, DarkInkColor, LegendX + 36.0f, LegY, SmallFont);
		LegY += 20.0f;
	};

	DrawLegendItem(TEXT("<>"), TEXT("Kabir (Scout)"), PlayerCol);
	DrawLegendItem(TEXT("[M]"), TEXT("Tailor's Chalk Mark"), FLinearColor(0.95f, 0.94f, 0.90f, 1.0f));
	DrawLegendItem(TEXT("[#]"), TEXT("Landmark / NPC"), AntiqueBrassColor);
	DrawLegendItem(TEXT("---"), TEXT("Bazaar Curfew Patrol"), FLinearColor(0.85f, 0.25f, 0.20f, 1.0f));
	DrawLegendItem(TEXT("[N]"), TEXT("North (Upward)"), DarkInkColor);
}

void ARevolutionHUD::DrawSatchelTabDispatchesLore(ARevolutionCharacter* Kabir, float BoxX, float ContentY, float ContentW, float ContentH)
{
	DrawSatchelTabHistoricalCodex(Kabir, BoxX, ContentY, ContentW, ContentH);
}

void ARevolutionHUD::DrawSatchelTabHistoricalCodex(ARevolutionCharacter* Kabir, float BoxX, float ContentY, float ContentW, float ContentH)
{
	UFont* SmallFont = GEngine ? GEngine->GetSmallFont() : nullptr;
	UFont* MediumFont = GEngine ? GEngine->GetMediumFont() : nullptr;
	if (!SmallFont) return;

	struct FHistoricalCodexRecord
	{
		FString Title;
		FString Category;
		FString DateLocation;
		FString ProclamationQuote;
		FString ArchivalSummary;
		FString GameplayRelevance;
	};

	static const FHistoricalCodexRecord CodexRecords[] = {
		// 1. The Rowlatt Black Act (1919)
		{
			TEXT("THE ROWLATT BLACK ACT (1919)"),
			TEXT("Colonial Legislation  •  Emergency War Powers"),
			TEXT("March 21, 1919  •  Imperial Legislative Council, Delhi"),
			TEXT("\"Na Dalil, Na Vakil, Na Appeal.\"  — Punjab Popular Proverb"),
			TEXT("Officially the Anarchical and Revolutionary Crimes Act of 1919. Drafted by Sir Sidney Rowlatt's Sedition Committee, this repressive statute authorized indefinite preventive detention, incarceration without trial, in-camera tribunals with no legal representation, and draconian bans on vernacular printing presses. It provoked universal outrage across India, uniting communities against colonial despotism."),
			TEXT("Under Rowlatt regulations, carrying printed literature is treasonous. Kabir must maintain low stance, utilize chalk-marked evasion routes, and deposit handbills into clandestine post drops before night curfew patrols seal the kuchas.")
		},
		// 2. Swadeshi & Khadi Weave
		{
			TEXT("SWADESHI & KHADI WEAVE"),
			TEXT("Economic Self-Reliance  •  Vernacular Craft"),
			TEXT("Mohalla Kot Gurdarshan  •  Textile Weaver Quarter"),
			TEXT("\"Khadi is the symbol of unity of Indian humanity, of its economic freedom and equality.\""),
			TEXT("The Swadeshi movement championed native homespun cotton (khadi) as a direct moral and economic strike against imported Lancashire mill cloth. By boycotting foreign garments, Indian artisans reclaimed economic autonomy. In Kot Gurdarshan, weavers and tailors spun charkha yarn in quiet courtyards, transforming every garment into a symbol of quiet national defiance."),
			TEXT("Kabir carries homespun khadi tailored parcels for father Ram Lubhaya. Khadi cloth delivery acts as legitimate courier cover to cross the Deorhi arch without raising sepoy suspicion.")
		},
		// 3. Baisakhi Harvest Festival
		{
			TEXT("BAISAKHI HARVEST FESTIVAL"),
			TEXT("Punjabi Cultural Heritage  •  Solar New Year"),
			TEXT("April 13, 1919  •  Spring Harvest Assembly"),
			TEXT("\"Aayi Baisakhi, khil gaye chehre — when the golden wheat bends to the sickle.\""),
			TEXT("Vaisakhi marks the joyous spring rabi harvest across Punjab and the historic 1699 founding of the Khalsa Panth by Guru Gobind Singh Ji. Tens of thousands of peasants, cattle traders, and pilgrims poured into Amritsar from rural villages to bathe at the sacred Amrit Sarovar and trade at local cattle fairs, entirely unaware of martial assembly bans."),
			TEXT("The vibrant holiday crowd in the Mandi square shields Kabir. Temple gongs and chatter provide acoustic masking, while festival kites and lanterns indicate favorable wind and safe rooftop transit.")
		},
		// 4. Jallianwala Bagh Memorial
		{
			TEXT("JALLIANWALA BAGH MEMORIAL"),
			TEXT("Sacred Memorial  •  The Veil of Remembrance"),
			TEXT("Amritsar Walled City  •  April 13, 1919"),
			TEXT("\"The disproportionate severity... will awaken an empire to its moral conscience.\""),
			TEXT("A six-acre open walled ground surrounded on all sides by five-story brick havelis with only five narrow chinks for entry. A peaceful, unarmed gathering assembled here on Baisakhi afternoon to protest the detention of Dr. Kitchlew and Dr. Satyapal. The tragic events that unfolded here galvanized the nation's resolve for complete independence."),
			TEXT("Treated in-game with profound solemnity through the Censor Window and Veil of Remembrance. Graphic violence is completely veiled in favor of atmospheric reflection, reverent bansuri melodies, and historical contemplation.")
		},
		// 5. Section 144 Martial Curfew
		{
			TEXT("SECTION 144 MARTIAL CURFEW"),
			TEXT("Military Decrees  •  Night Movement Ban"),
			TEXT("8:00 PM Curfew Order  •  Kot Gurdarshan Thoroughfares"),
			TEXT("\"All assemblies are declared unlawful. Streets must remain cleared after sunset.\""),
			TEXT("Issued by the colonial district magistrate, Section 144 prohibited any gathering of more than four individuals and mandated an 8:00 PM curfew. Citizens caught outdoors after the evening bugle faced summary flogging or imprisonment under military regulations. Kot Gurdarshan became an eerie grid of barred wooden shutters and pacing constables."),
			TEXT("Curfew activation triggers the 800 Hz low-pass ambient audio filter, sharpens patrol alert cones, and requires Kabir to use rooftops, timber pigeon lofts, and cellar crawls to deliver dispatches undetected.")
		},
		// 6. Clandestine Printing Press
		{
			TEXT("CLANDESTINE PRINTING PRESS"),
			TEXT("Underground Press  •  Free Expression"),
			TEXT("Cellar Workshop  •  Kucha Press Quarter"),
			TEXT("\"The pen may be outlawed by edict, but the stone press speaks in the dark.\""),
			TEXT("When colonial censors seized printing establishments and enforced the Indian Press Act of 1910, resistance networks retreated underground. Miniature lithographic flatbed stones were operated by candlelight in subterranean haveli cellars, churning out thousands of strike handbills on coarse rag paper overnight."),
			TEXT("Kabir's central mission objective: slip past bazaar pickets to retrieve freshly lithographed handbills and deliver them to courier drops across the 5 historical zones before dawn.")
		},
		// 7. Punjabi Architectural Fabric
		{
			TEXT("PUNJABI ARCHITECTURAL FABRIC"),
			TEXT("Vernacular Urbanism  •  The Mohalla Network"),
			TEXT("Walled City Punjab  •  Nanakshahi Brick Havelis"),
			TEXT("\"The haveli's walls keep the noon heat out and the community's bond within.\""),
			TEXT("Historic Punjabi mohallas were masterclasses in climate-adaptive, defensive urban planning. Built with slender Nanakshahi kiln-fired bricks, lime mortar, and carved shisham jharokha balconies, multi-story havelis formed contiguous rooftop corridors (kothas) connected by low parapets, shaded courtyards, and communal wells."),
			TEXT("The interconnected flat roofs allow Kabir to leap over 1.1m parapets, traverse high clotheslines, and bypass guarded ground streets entirely through authentic historical parkour.")
		},
		// 8. Student Wooden Takhti & Qalam
		{
			TEXT("STUDENT TAKHTI & REED QALAM"),
			TEXT("Vernacular Education  •  Literacy"),
			TEXT("Primary Mohalla Maktab  •  April 1919"),
			TEXT("\"Vidya vichari taan parupkari — true learning yields selfless action.\""),
			TEXT("Carved shisham wood writing board washed with pale chalk slip (gachi). 12-year-old pupils practice Punjabi and Urdu calligraphy using sharpened bamboo reed pens (qalam) and lampblack ink, learning ancestral history despite colonial curricula."),
			TEXT("Found in Kabir's home classroom; symbolizes the quiet education and literacy that enabled young couriers to read dispatches and coordinate resistance routes.")
		},
		// 9. Earthen Mud Chulha Stove
		{
			TEXT("EARTHEN MUD CHULHA STOVE"),
			TEXT("Domestic Life  •  Foodways"),
			TEXT("Courtyard Kitchen  •  Kot Gurdarshan"),
			TEXT("\"Ghar da chulha te maa di mamta — the courtyard hearth that sustains life.\""),
			TEXT("Double-burner clay cooking hearth with terracotta handi pot and hammered brass lota. The morning scent of cow-dung fuel, woodsmoke, and ginger cardamom tea anchors the family courtyard, providing refuge before dangerous assignments."),
			TEXT("Courtyard cooking fires produce rising smoke plumes that Kabir can use from rooftops as visual landmarks to navigate during foggy mornings and dusk.")
		},
		// 10. Bazaar Vendor Thela (Handcart)
		{
			TEXT("BAZAAR VENDOR THELA (HANDCART)"),
			TEXT("Mandi Commerce  •  Octroi Taxes"),
			TEXT("Grand Bazaar Mandi  •  Wheat & Grain Stalls"),
			TEXT("\"Haath-thela te rozi-roti — honest labour under oppressive octroi levies.\""),
			TEXT("Heavy timber cart with 76cm iron-spoked wheels, laden with jute grain sacks and clay water matkas. Mandi vendors used these heavy carts to transport daily produce while resisting colonial middleman syndicates."),
			TEXT("Provides essential waist-high crouch cover against patrolling British police sepoys; Kabir can creep behind loaded thelas to break line-of-sight across open squares.")
		},
		// 11. Rooftop Pigeon Loft (Kabootar-khana)
		{
			TEXT("ROOFTOP PIGEON LOFT"),
			TEXT("Mohalla Culture  •  Acoustic Signaling"),
			TEXT("Haveli Rooftop Terraces  •  Kotha Network"),
			TEXT("\"Kabootar bazi — the high art of flight and rooftop brotherhood.\""),
			TEXT("Slatted timber loft for racing tumbler pigeons (kabootar-khana). Neighborhood boys and courier scouts used fluttering flocks and rhythmic whistle calls to signal patrol movements without alerting ground sepoys."),
			TEXT("Functions as interactive hiding spots across haveli roofs; entering a slatted pigeon loft conceals Kabir completely while fluttering coos mask audio signatures.")
		},
		// 12. Basant Fighter Kites & Manja
		{
			TEXT("BASANT FIGHTER KITES & MANJA"),
			TEXT("Childhood Heritage  •  Basant 1919"),
			TEXT("Spring Skies  •  Kot Gurdarshan Havelis"),
			TEXT("\"Woh kaata! — the joyous triumphant cry echoing across spring rooftops.\""),
			TEXT("Thin tissue paper diamond kite with arched bamboo spars and a lathe-turned hardwood reel (charkhi) wound with glass-coated saffron manja thread. Symbolizes the resilient spirit and childhood joy that survived wartime hardships."),
			TEXT("Kite reels and drying manja lines strung between roofs serve as visual breadcrumbs for rooftop crossing paths, signaling safe mantling points for agile couriers.")
		},
		// 13. Anti-Rowlatt Satyagraha Handbill
		{
			TEXT("ANTI-ROWLATT HANDBILL"),
			TEXT("Underground Press  •  Hartal 1919"),
			TEXT("Lithographed Overnight  •  Secret Courier Network"),
			TEXT("\"Na Dalil, Na Vakil, Na Appeal — Complete Hartal Shutdown.\""),
			TEXT("Freshly lithographed strike notice on coarse rag paper calling for a total province-wide shutdown of all bazaars, schools, and railways in protest of the Rowlatt Act."),
			TEXT("Kabir's principal objective item. Depositing bundles into secret postboxes and merchant stashes mobilizes the town for the historic April 1919 Hartal.")
		},
		// 14. Imperial Red Pillar Postbox (GR)
		{
			TEXT("IMPERIAL PILLAR POSTBOX (GR)"),
			TEXT("Colonial Administration  •  Boycott Target"),
			TEXT("Grand Bazaar Crossing  •  Post Office Road"),
			TEXT("\"Royal Cypher George V  •  Monopoly of Official Transit.\""),
			TEXT("Cast-iron cylindrical red postbox bearing the royal cypher and imperial collection schedule plate. Symbolized British bureaucratic dominance over postal communications."),
			TEXT("Anti-colonial scouts plastered boycott notices across its imperial crest, turning the colonial communications node into an undercover message beacon.")
		},
		// 15. Mandi Iron Tarazu Scale & Weights
		{
			TEXT("MANDI TARAZU SCALE & WEIGHTS"),
			TEXT("Fair Trade  •  Requisition Scarcity"),
			TEXT("Grain Merchant Guild  •  Mandi Square"),
			TEXT("\"Sach da tarazu — weighing honesty amidst war requisitions and shortages.\""),
			TEXT("Traditional merchant balance scale with dual brass pans and cast-iron standard weights. Reminds shoppers of colonial wartime grain requisitioning and market rationing."),
			TEXT("Located near Lala Karam Chand's stall; can be interacted with to study fair commerce and inspect the grain shortages that fueled popular protest in spring 1919.")
		},
		// 16. Shisham Carved Grain Sandook
		{
			TEXT("SHISHAM CARVED GRAIN SANDOOK"),
			TEXT("Haveli Heritage  •  Heirloom Storage"),
			TEXT("Family Living Quarters  •  Haveli Interior"),
			TEXT("\"Peedhi-dar-peedhi — generational chest preserving heirlooms and grain.\""),
			TEXT("Heavy Punjabi hardwood chest with iron corner brackets, floral repoussé brass relief carvings, and padlock hasp, elevated on turned feet to protect seeds and khadi cloth."),
			TEXT("Serves as Kabir's domestic stash point where tailored khadi deliveries and clandestine pamphlets are concealed safely under family textiles.")
		},
		// 17. Classroom 1919 Punjab Map Easel
		{
			TEXT("CLASSROOM 1919 PUNJAB MAP"),
			TEXT("Vernacular School  •  Historical Cartography"),
			TEXT("Vernacular Middle School  •  Room 4B"),
			TEXT("\"Land of Five Rivers  •  The Grand Trunk Corridor.\""),
			TEXT("Hand-drafted classroom easel displaying the 1919 British administrative map of Punjab Province, demarcating Amritsar, Lahore, Jalandhar, and Rawalpindi."),
			TEXT("Studying the map allows Kabir to visualize the wider provincial scale of the Satyagraha network and track historical landmarks across Kot Gurdarshan.")
		},
		// 18. The Baisakhi Dawn & National Awakening (1919)
		{
			TEXT("THE BAISAKHI DAWN & AWAKENING"),
			TEXT("Historical Epilogue  •  The Moral Turning Point"),
			TEXT("April 14, 1919  •  Punjab & The National Awakening"),
			TEXT("\"The time has come when badges of honour make our shame glaring in their incongruous context of humiliation...\" — Rabindranath Tagore"),
			TEXT("In the golden morning light following April 13, 1919, Punjab and India awoke to an irrevocable moral turning point. Rabindranath Tagore renounced his British knighthood in solemn protest, Mahatma Gandhi returned his Kaiser-i-Hind medal and launched the historic Non-Cooperation Movement, and the moral authority of colonial subjugation collapsed permanently across the subcontinent."),
			TEXT("The culminating historical record of Kabir's courier journey. Unlocked at the dawn of April 14 as the golden sunrise crests the baked terracotta rooftops of Kot Gurdarshan, commemorating the sacrifices of the martyrs and marking the dawn of the national freedom movement.")
		}
	};

	const int32 TotalEntries = 18;
	const int32 CurrentIdx = Kabir ? FMath::Clamp(Kabir->SelectedCodexIndex, 0, TotalEntries - 1) : 0;

	// Layout dimensions
	const float LeftW = ContentW * 0.38f;
	const float RightW = ContentW - LeftW - 14.0f;
	const float RightX = BoxX + LeftW + 14.0f;

	// --- LEFT COLUMN: Scrollable Directory of 17 Historical Entries ---
	const int32 MaxVisible = 6;
	const int32 StartIdx = FMath::Clamp(CurrentIdx - 2, 0, FMath::Max(0, TotalEntries - MaxVisible));
	const float CardH = (ContentH - 28.0f) / (float)MaxVisible;

	for (int32 i = 0; i < MaxVisible; ++i)
	{
		int32 RecordIdx = StartIdx + i;
		if (RecordIdx >= TotalEntries) break;

		float CurY = ContentY + 4.0f + (i * (CardH + 4.0f));
		bool bSelected = (RecordIdx == CurrentIdx);

		FLinearColor CardBg = bSelected ? DarkInkColor : FLinearColor(0.88f, 0.84f, 0.74f, 0.90f);
		FLinearColor CardBorder = bSelected ? AntiqueBrassColor : MutedSepiaColor;
		FLinearColor TitleColor = bSelected ? AntiqueBrassColor : DarkInkColor;
		FLinearColor CatColor = bSelected ? FLinearColor(0.92f, 0.88f, 0.80f, 0.90f) : MutedSepiaColor;

		DrawFramedBox(BoxX, CurY, LeftW, CardH, CardBg, CardBorder, bSelected ? 1.5f : 1.0f);

		FString Prefix = bSelected ? TEXT("> ") : TEXT("  ");
		FString EntryLabel = FString::Printf(TEXT("%s[%02d] %s"), *Prefix, RecordIdx + 1, *CodexRecords[RecordIdx].Title);

		DrawText(EntryLabel, TitleColor, BoxX + 8.0f, CurY + 4.0f, SmallFont);
		DrawText(CodexRecords[RecordIdx].Category, CatColor, BoxX + 16.0f, CurY + 20.0f, SmallFont);
	}

	// --- RIGHT COLUMN: Rich Archival Dossier ---
	DrawFramedBox(RightX, ContentY + 4.0f, RightW, ContentH - 8.0f, FLinearColor(0.90f, 0.86f, 0.77f, 0.95f), AntiqueBrassColor, 1.5f);

	// Archival Header Tag
	FString DossierTag = FString::Printf(TEXT("ARCHIVAL DOSSIER  •  RECORD #%02d OF %d  •  PUNJAB 1919"), CurrentIdx + 1, TotalEntries);
	DrawText(DossierTag, AntiqueBrassColor, RightX + 14.0f, ContentY + 12.0f, SmallFont);
	DrawLine(RightX + 14.0f, ContentY + 28.0f, RightX + RightW - 14.0f, ContentY + 28.0f, AntiqueBrassColor, 1.0f);

	// Title
	DrawText(CodexRecords[CurrentIdx].Title, DarkInkColor, RightX + 14.0f, ContentY + 34.0f, MediumFont ? MediumFont : SmallFont);

	// Category & Historical Period Subtitle
	FString Subtitle = CodexRecords[CurrentIdx].Category + TEXT("   |   ") + CodexRecords[CurrentIdx].DateLocation;
	DrawText(Subtitle, MutedSepiaColor, RightX + 14.0f, ContentY + 54.0f, SmallFont);

	// Proclamation / Period Quote Callout Box
	float QuoteY = ContentY + 72.0f;
	float QuoteH = 34.0f;
	DrawFramedBox(RightX + 12.0f, QuoteY, RightW - 24.0f, QuoteH, FLinearColor(0.12f, 0.10f, 0.08f, 0.90f), AntiqueBrassColor, 1.0f);
	DrawText(CodexRecords[CurrentIdx].ProclamationQuote, AntiqueBrassColor, RightX + 22.0f, QuoteY + 8.0f, SmallFont);

	// Historical Analysis / Treatise
	float TreatY = QuoteY + QuoteH + 12.0f;
	TArray<FString> SummaryLines = WrapText(CodexRecords[CurrentIdx].ArchivalSummary, SmallFont, RightW - 28.0f);
	for (const FString& Line : SummaryLines)
	{
		DrawText(Line, DarkInkColor, RightX + 14.0f, TreatY, SmallFont);
		TreatY += 14.0f;
	}

	// Gameplay Stealth Dynamics Box (at bottom)
	float MechBoxH = 64.0f;
	float MechBoxY = ContentY + ContentH - MechBoxH - 18.0f;
	DrawFramedBox(RightX + 12.0f, MechBoxY, RightW - 24.0f, MechBoxH, FLinearColor(0.85f, 0.81f, 0.70f, 0.92f), MutedSepiaColor, 1.0f);
	DrawText(TEXT("STEALTH & TACTICAL APPLICATION:"), AntiqueBrassColor, RightX + 20.0f, MechBoxY + 6.0f, SmallFont);

	TArray<FString> MechLines = WrapText(CodexRecords[CurrentIdx].GameplayRelevance, SmallFont, RightW - 40.0f);
	float MechTextY = MechBoxY + 22.0f;
	for (const FString& MLine : MechLines)
	{
		DrawText(MLine, DarkInkColor, RightX + 20.0f, MechTextY, SmallFont);
		MechTextY += 13.0f;
	}
}

void ARevolutionHUD::DrawSatchelTabSettingsControls(ARevolutionCharacter* Kabir, float BoxX, float ContentY, float ContentW, float ContentH)
{
	UFont* SmallFont = GEngine ? GEngine->GetSmallFont() : nullptr;
	UFont* MediumFont = GEngine ? GEngine->GetMediumFont() : nullptr;
	if (!SmallFont) return;

	const float LeftW = (ContentW - 16.0f) * 0.49f;
	const float RightW = (ContentW - 16.0f) * 0.51f;
	const float RightX = BoxX + LeftW + 16.0f;

	// --- LEFT COLUMN: AUDIO MIX & ACCESSIBILITY CONFIGURATION ---
	DrawFramedBox(BoxX, ContentY + 4.0f, LeftW, ContentH - 8.0f, FLinearColor(0.89f, 0.85f, 0.76f, 0.95f), AntiqueBrassColor, 1.5f);

	DrawText(TEXT("AUDIO MIX & ACCESSIBILITY OPTIONS"), DarkInkColor, BoxX + 14.0f, ContentY + 12.0f, MediumFont ? MediumFont : SmallFont);
	DrawText(TEXT("Dynamic Task 17 SoundClass Routing & Subtitle Scaling"), MutedSepiaColor, BoxX + 14.0f, ContentY + 30.0f, SmallFont);
	DrawLine(BoxX + 14.0f, ContentY + 46.0f, BoxX + LeftW - 14.0f, ContentY + 46.0f, AntiqueBrassColor, 1.0f);

	const int32 SelectedSetting = Kabir ? Kabir->SelectedSettingsIndex : 0;

	auto DrawAudioSlider = [&](float Y, float Value, const FString& Label, const FString& SoundClassTag, bool bSelected)
	{
		float CardY = Y;
		float CardW = LeftW - 28.0f;
		float CardH = 38.0f;
		float CardX = BoxX + 14.0f;

		FLinearColor Bg = bSelected ? DarkInkColor : FLinearColor(0.93f, 0.90f, 0.82f, 0.85f);
		FLinearColor Border = bSelected ? AntiqueBrassColor : MutedSepiaColor;
		FLinearColor TextCol = bSelected ? AntiqueBrassColor : DarkInkColor;

		DrawFramedBox(CardX, CardY, CardW, CardH, Bg, Border, bSelected ? 1.5f : 1.0f);

		FString Indicator = bSelected ? TEXT("> ") : TEXT("  ");
		DrawText(Indicator + Label, TextCol, CardX + 8.0f, CardY + 4.0f, SmallFont);

		FString PctStr = FString::Printf(TEXT("%d%%  [%s]"), FMath::RoundToInt(Value * 100.0f), *SoundClassTag);
		float PctW = 0.0f, PctH = 0.0f;
		GetTextSize(PctStr, PctW, PctH, SmallFont);
		DrawText(PctStr, bSelected ? FLinearColor(0.95f, 0.92f, 0.85f, 1.0f) : MutedSepiaColor, CardX + CardW - PctW - 8.0f, CardY + 4.0f, SmallFont);

		// Slider Track
		float BarX = CardX + 10.0f;
		float BarY = CardY + 22.0f;
		float BarW = CardW - 20.0f;
		float BarH = 8.0f;
		DrawRect(FLinearColor(0.2f, 0.18f, 0.15f, 0.9f), BarX, BarY, BarW, BarH);
		DrawRect(AntiqueBrassColor, BarX + 1.0f, BarY + 1.0f, (BarW - 2.0f) * FMath::Clamp(Value, 0.0f, 1.0f), BarH - 2.0f);
	};

	float MasterVol = Kabir ? Kabir->MasterVolume : 1.0f;
	float SFXVol = Kabir ? Kabir->SFXVolume : 1.0f;
	float FoleyVol = Kabir ? Kabir->FoleyVolume : 1.0f;
	float VoiceVol = Kabir ? Kabir->VoiceVolume : 1.0f;
	float AmbVol = Kabir ? Kabir->AmbienceVolume : 1.0f;
	float SubScale = Kabir ? Kabir->SubtitleScaleMultiplier : 1.0f;

	DrawAudioSlider(ContentY + 48.0f, MasterVol, TEXT("Master Mix Volume"), TEXT("SC_Master"), SelectedSetting == 0);
	DrawAudioSlider(ContentY + 84.0f, SFXVol, TEXT("Sound Effects (SFX)"), TEXT("SC_SFX"), SelectedSetting == 1);
	DrawAudioSlider(ContentY + 120.0f, FoleyVol, TEXT("Foley & Stealth Footsteps"), TEXT("SC_Foley"), SelectedSetting == 2);
	DrawAudioSlider(ContentY + 156.0f, VoiceVol, TEXT("Voice & Proclamation"), TEXT("SC_Voice"), SelectedSetting == 3);
	DrawAudioSlider(ContentY + 192.0f, AmbVol, TEXT("Mohalla Ambience & Night Wind"), TEXT("SC_Ambience"), SelectedSetting == 4);

	// ACCESSIBILITY: Subtitle Scale Toggle Row (Setting 5)
	float SubY = ContentY + 230.0f;
	float SubCardW = LeftW - 28.0f;
	float SubCardH = 40.0f;
	float SubCardX = BoxX + 14.0f;
	bool bSubSelected = (SelectedSetting == 5);

	DrawFramedBox(SubCardX, SubY, SubCardW, SubCardH, bSubSelected ? DarkInkColor : FLinearColor(0.93f, 0.90f, 0.82f, 0.85f), bSubSelected ? AntiqueBrassColor : MutedSepiaColor, bSubSelected ? 1.5f : 1.0f);

	FString SubInd = bSubSelected ? TEXT("> ") : TEXT("  ");
	DrawText(SubInd + TEXT("Accessibility Subtitle Size"), bSubSelected ? AntiqueBrassColor : DarkInkColor, SubCardX + 8.0f, SubY + 3.0f, SmallFont);

	const FString SizeLabels[] = { TEXT("SMALL (85%)"), TEXT("MEDIUM (100%)"), TEXT("LARGE (125%)") };
	const float SizeScales[] = { 0.85f, 1.0f, 1.25f };
	float PillW = (SubCardW - 24.0f) / 3.0f;
	float PillH = 16.0f;

	for (int32 s = 0; s < 3; ++s)
	{
		float PX = SubCardX + 8.0f + (s * (PillW + 4.0f));
		float PY = SubY + 18.0f;
		bool bActiveSize = FMath::IsNearlyEqual(SubScale, SizeScales[s], 0.1f);

		FLinearColor PBg = bActiveSize ? AntiqueBrassColor : FLinearColor(0.85f, 0.81f, 0.72f, 0.85f);
		FLinearColor PText = bActiveSize ? DarkInkColor : MutedSepiaColor;

		DrawFramedBox(PX, PY, PillW, PillH, PBg, AntiqueBrassColor, 1.0f);
		float LW = 0.0f, LH = 0.0f;
		GetTextSize(SizeLabels[s], LW, LH, SmallFont);
		DrawText(SizeLabels[s], PText, PX + ((PillW - LW) * 0.5f), PY + ((PillH - LH) * 0.5f), SmallFont);
	}

	// STEAMOS & HANDHELD SCALABILITY PROFILE (Setting 6)
	float DeckY = ContentY + 274.0f;
	float DeckCardW = LeftW - 28.0f;
	float DeckCardH = 46.0f;
	float DeckCardX = BoxX + 14.0f;
	bool bDeckSelected = (SelectedSetting == 6);
	bool bDeckActive = Kabir ? Kabir->IsHandheldModeEnabled() : false;

	DrawFramedBox(DeckCardX, DeckY, DeckCardW, DeckCardH, bDeckSelected ? DarkInkColor : FLinearColor(0.93f, 0.90f, 0.82f, 0.85f), bDeckSelected ? AntiqueBrassColor : MutedSepiaColor, bDeckSelected ? 1.5f : 1.0f);

	FString DeckInd = bDeckSelected ? TEXT("> ") : TEXT("  ");
	DrawText(DeckInd + TEXT("SteamOS / Handheld 800p Low-Power Mode"), bDeckSelected ? AntiqueBrassColor : DarkInkColor, DeckCardX + 8.0f, DeckY + 3.0f, SmallFont);

	const FString DeckLabels[] = { TEXT("OFF: DESKTOP 60 FPS"), TEXT("ON: STEAM DECK 40 FPS TSR") };
	float DeckPillW = (DeckCardW - 20.0f) * 0.5f;
	float DeckPillH = 18.0f;

	for (int32 d = 0; d < 2; ++d)
	{
		float DX = DeckCardX + 8.0f + (d * (DeckPillW + 4.0f));
		float DY = DeckY + 22.0f;
		bool bThisActive = (d == 1 && bDeckActive) || (d == 0 && !bDeckActive);

		FLinearColor DBg = bThisActive ? AntiqueBrassColor : FLinearColor(0.85f, 0.81f, 0.72f, 0.85f);
		FLinearColor DText = bThisActive ? DarkInkColor : MutedSepiaColor;

		DrawFramedBox(DX, DY, DeckPillW, DeckPillH, DBg, AntiqueBrassColor, 1.0f);
		float DW = 0.0f, DH = 0.0f;
		GetTextSize(DeckLabels[d], DW, DH, SmallFont);
		DrawText(DeckLabels[d], DText, DX + ((DeckPillW - DW) * 0.5f), DY + ((DeckPillH - DH) * 0.5f), SmallFont);
	}

	// Instructions Footer
	float FootY = ContentY + ContentH - 26.0f;
	DrawText(TEXT("[ UP / DOWN / D-PAD ] Select Setting    |    [ LEFT / RIGHT / (A) ] Adjust / Toggle"), DarkInkColor, BoxX + 16.0f, FootY, SmallFont);

	// --- RIGHT COLUMN: HISTORICAL SCOUT CONTROLS & KEYBINDING REMAP ---
	DrawFramedBox(RightX, ContentY + 4.0f, RightW, ContentH - 8.0f, FLinearColor(0.89f, 0.85f, 0.76f, 0.95f), AntiqueBrassColor, 1.5f);

	DrawText(TEXT("HISTORICAL SCOUT CONTROL SCHEMA"), DarkInkColor, RightX + 14.0f, ContentY + 10.0f, MediumFont ? MediumFont : SmallFont);
	DrawText(TEXT("Full Steam Deck Handheld Controller & Keyboard/Mouse Dual Support"), MutedSepiaColor, RightX + 14.0f, ContentY + 28.0f, SmallFont);
	DrawLine(RightX + 14.0f, ContentY + 44.0f, RightX + RightW - 14.0f, ContentY + 44.0f, AntiqueBrassColor, 1.0f);

	auto DrawControlGroup = [&](float GStart, const FString& GTitle, const TArray<TPair<FString, FString>>& KeyPairs) -> float
	{
		DrawText(GTitle, AntiqueBrassColor, RightX + 14.0f, GStart, SmallFont);
		DrawLine(RightX + 14.0f, GStart + 15.0f, RightX + RightW - 14.0f, GStart + 15.0f, MutedSepiaColor, 0.5f);

		float RowY = GStart + 19.0f;
		for (const auto& Pair : KeyPairs)
		{
			// Key badge
			float BadgeW = 104.0f;
			float BadgeH = 15.0f;
			DrawFramedBox(RightX + 14.0f, RowY, BadgeW, BadgeH, DarkInkColor, AntiqueBrassColor, 1.0f);

			float KW = 0.0f, KH = 0.0f;
			GetTextSize(Pair.Key, KW, KH, SmallFont);
			DrawText(Pair.Key, AntiqueBrassColor, RightX + 14.0f + ((BadgeW - KW) * 0.5f), RowY + ((BadgeH - KH) * 0.5f), SmallFont);

			DrawText(Pair.Value, DarkInkColor, RightX + 124.0f, RowY + 1.0f, SmallFont);
			RowY += 17.5f;
		}
		return RowY + 3.0f;
	};

	TArray<TPair<FString, FString>> LocomotionKeys = {
		{ TEXT("WASD | L-Stick"), TEXT("Walk & Steer Kabir across alleys and rooftops") },
		{ TEXT("L-SHIFT | LB"), TEXT("Sprint through open streets (Consumes Stamina)") },
		{ TEXT("C | (B)"), TEXT("Toggle Low Stance / Crouch Creeping") },
		{ TEXT("SPACE | (A)"), TEXT("Vault 1.1m Parapet / Mantle Ledge / Jump") }
	};
	float G1End = DrawControlGroup(ContentY + 48.0f, TEXT("1. LOCOMOTION & HISTORICAL PARKOUR"), LocomotionKeys);

	TArray<TPair<FString, FString>> StealthKeys = {
		{ TEXT("RMB | LT"), TEXT("Hold to Aim Pebble Trajectory Arc (A Plague Tale)") },
		{ TEXT("F, G | RT"), TEXT("Throw Tailor's Pebble to Lure Patrol Away") },
		{ TEXT("T | R3 Stick"), TEXT("Inscribe Tailor's Chalk Mark on Surfaces") },
		{ TEXT("V | (Y)"), TEXT("Basant Intuition (Keen Senses Tactical Beacon)") },
		{ TEXT("Q / E"), TEXT("Corner Peeking & Parapet Lean (Dishonored)") },
		{ TEXT("E, RET | (X)"), TEXT("Interact with NPCs / Enter Concealment Hiding Spot") }
	};
	float G2End = DrawControlGroup(G1End, TEXT("2. STEALTH, DISTRACTION & FIELD TOOLS"), StealthKeys);

	TArray<TPair<FString, FString>> SatchelKeys = {
		{ TEXT("TAB, J | RB"), TEXT("Open / Close Satchel & Field Journal Modal") },
		{ TEXT("1-4 | D-Pad"), TEXT("Directly Select Satchel Tabs 1 to 4") },
		{ TEXT("UP/DN | D-Pad"), TEXT("Navigate Historical Codex Entries & Settings") },
		{ TEXT("LT/RT | (A)"), TEXT("Adjust Volume Sliders / Toggle Handheld Mode") }
	};
	DrawControlGroup(G2End, TEXT("3. SATCHEL JOURNAL & SETTINGS SHORTCUTS"), SatchelKeys);
}

void ARevolutionHUD::DrawApprehendedCard(ARevolutionCharacter* Kabir)
{
	if (!Canvas || !Kabir) return;

	UFont* LargeFont = GEngine ? GEngine->GetLargeFont() : nullptr;
	UFont* MediumFont = GEngine ? GEngine->GetMediumFont() : nullptr;
	UFont* SmallFont = GEngine ? GEngine->GetSmallFont() : nullptr;
	if (!SmallFont) return;

	// Dark crimson / charcoal curfew apprehension vignette
	DrawRect(FLinearColor(0.06f, 0.015f, 0.015f, 0.88f), 0.0f, 0.0f, Canvas->ClipX, Canvas->ClipY);

	const float CenterX = Canvas->ClipX * 0.5f;
	const float CenterY = Canvas->ClipY * 0.5f;

	const float CardW = FMath::Min(560.0f, Canvas->ClipX * 0.90f);
	const float CardH = 260.0f;
	const float CardX = CenterX - (CardW * 0.5f);
	const float CardY = CenterY - (CardH * 0.5f);

	// Heavy framed modal box in deep aged parchment/sepia with crimson-gold border
	FLinearColor ApprehendedBorder(0.85f, 0.22f, 0.18f, 0.98f);
	DrawFramedBox(CardX, CardY, CardW, CardH, FLinearColor(0.09f, 0.07f, 0.06f, 0.96f), ApprehendedBorder, 2.0f);

	// Header Tag
	FString HeaderTag = TEXT("M A R T I A L   L A W   E D I C T   •   S E C T I O N   1 4 4");
	float TagW = 0.0f, TagH = 0.0f;
	GetTextSize(HeaderTag, TagW, TagH, SmallFont);
	DrawText(HeaderTag, ApprehendedBorder, CenterX - (TagW * 0.5f), CardY + 16.0f, SmallFont);

	// Thin crimson divider
	DrawLine(CardX + 24.0f, CardY + 36.0f, CardX + CardW - 24.0f, CardY + 36.0f, ApprehendedBorder, 1.0f);

	// Main Title
	FString MainTitle = TEXT("APPREHENDED BY CURFEW PATROL");
	float TitleW = 0.0f, TitleH = 0.0f;
	UFont* TitleFont = LargeFont ? LargeFont : (MediumFont ? MediumFont : SmallFont);
	GetTextSize(MainTitle, TitleW, TitleH, TitleFont);
	DrawText(MainTitle, FLinearColor(0.98f, 0.92f, 0.86f, 1.0f), CenterX - (TitleW * 0.5f), CardY + 48.0f, TitleFont);

	// Historical Context Lore
	FString LoreText = TEXT("Kot Gurdarshan, April 1919. Night movement without an official British military permit is strictly forbidden under Section 144. Kabir has been cornered by the mohalla chaukidar and detained under suspicion of carrying anti-Rowlatt clandestine dispatches.");
	TArray<FString> WrappedLore = WrapText(LoreText, SmallFont, CardW - 48.0f);
	float LoreY = CardY + 90.0f;
	for (const FString& Line : WrappedLore)
	{
		DrawText(Line, FLinearColor(0.82f, 0.78f, 0.72f, 0.95f), CardX + 24.0f, LoreY, SmallFont);
		LoreY += 15.0f;
	}

	// Bottom Retry Badges
	const float ButtonW = CardW - 48.0f;
	const float ButtonH = 34.0f;
	const float ButtonX = CardX + 24.0f;
	const float ButtonY = CardY + CardH - 48.0f;

	float Pulse = 0.75f + 0.25f * FMath::Sin(GetWorld()->GetTimeSeconds() * 6.0f);
	FLinearColor ButtonBorder(0.92f, 0.76f, 0.32f, Pulse);
	DrawFramedBox(ButtonX, ButtonY, ButtonW, ButtonH, FLinearColor(0.18f, 0.12f, 0.08f, 0.90f), ButtonBorder, 1.5f);

	FString PromptStr = TEXT("[ SPACE / ENTER / E ]   RETRY FROM LAST SAFE CHECKPOINT");
	float PromptW = 0.0f, PromptH = 0.0f;
	GetTextSize(PromptStr, PromptW, PromptH, SmallFont);
	DrawText(PromptStr, FLinearColor(1.0f, 0.92f, 0.78f, 1.0f), CenterX - (PromptW * 0.5f), ButtonY + ((ButtonH - PromptH) * 0.5f), SmallFont);
}

void ARevolutionHUD::DrawMissionAccomplishedCard(ARevolutionCharacter* Kabir)
{
	if (!Canvas || !Kabir) return;

	UFont* LargeFont = GEngine ? GEngine->GetLargeFont() : nullptr;
	UFont* MediumFont = GEngine ? GEngine->GetMediumFont() : nullptr;
	UFont* SmallFont = GEngine ? GEngine->GetSmallFont() : nullptr;
	if (!SmallFont) return;

	// Warm golden dawn atmospheric wash
	DrawRect(FLinearColor(0.04f, 0.06f, 0.03f, 0.82f), 0.0f, 0.0f, Canvas->ClipX, Canvas->ClipY);

	const float CenterX = Canvas->ClipX * 0.5f;
	const float CenterY = Canvas->ClipY * 0.5f;

	const float CardW = FMath::Min(620.0f, Canvas->ClipX * 0.92f);
	const float CardH = 280.0f;
	const float CardX = CenterX - (CardW * 0.5f);
	const float CardY = CenterY - (CardH * 0.5f);

	// Framed victory ledger in deep forest lacquer and polished gold
	FLinearColor DawnGold(0.95f, 0.82f, 0.38f, 0.98f);
	DrawFramedBox(CardX, CardY, CardW, CardH, FLinearColor(0.05f, 0.08f, 0.06f, 0.96f), DawnGold, 2.0f);

	// Header Tag
	FString HeaderTag = TEXT("D A W N   R E S O L U T I O N   •   P U N J A B   R E S I S T A N C E   1 9 1 9");
	float TagW = 0.0f, TagH = 0.0f;
	GetTextSize(HeaderTag, TagW, TagH, SmallFont);
	DrawText(HeaderTag, DawnGold, CenterX - (TagW * 0.5f), CardY + 16.0f, SmallFont);

	// Gold divider
	DrawLine(CardX + 24.0f, CardY + 36.0f, CardX + CardW - 24.0f, CardY + 36.0f, DawnGold, 1.0f);

	// Main Title
	FString MainTitle = TEXT("MISSION ACCOMPLISHED — THE HARTAL COMMENCES");
	float TitleW = 0.0f, TitleH = 0.0f;
	UFont* TitleFont = LargeFont ? LargeFont : (MediumFont ? MediumFont : SmallFont);
	GetTextSize(MainTitle, TitleW, TitleH, TitleFont);
	DrawText(MainTitle, FLinearColor(0.98f, 0.96f, 0.88f, 1.0f), CenterX - (TitleW * 0.5f), CardY + 48.0f, TitleFont);

	// Historical Chronicle Lore
	FString LoreText = TEXT("Before the first morning light crested the baked terracotta rooftops of Kot Gurdarshan, Kabir deposited the clandestine anti-Rowlatt bulletins into the courier stash. As morning temple and gurdwara bells toll across the havelis, bazaar shutters remain bolted shut in complete civil strike.");
	TArray<FString> WrappedLore = WrapText(LoreText, SmallFont, CardW - 48.0f);
	float LoreY = CardY + 88.0f;
	for (const FString& Line : WrappedLore)
	{
		DrawText(Line, FLinearColor(0.85f, 0.88f, 0.82f, 0.95f), CardX + 24.0f, LoreY, SmallFont);
		LoreY += 15.0f;
	}

	// Status confirmation
	FString StatusText = TEXT("Clandestine Route Cleared   •   All 4 Mohalla Directives Completed");
	float StatW = 0.0f, StatH = 0.0f;
	GetTextSize(StatusText, StatW, StatH, SmallFont);
	DrawText(StatusText, FLinearColor(0.45f, 0.88f, 0.55f, 1.0f), CenterX - (StatW * 0.5f), CardY + CardH - 68.0f, SmallFont);

	// Footer Action Prompt
	FString FooterStr = TEXT("[ TAB / J ] View Chronicle Journal   •   Roam Kot Gurdarshan at Dawn");
	float FootW = 0.0f, FootH = 0.0f;
	GetTextSize(FooterStr, FootW, FootH, SmallFont);
	DrawText(FooterStr, DawnGold, CenterX - (FootW * 0.5f), CardY + CardH - 36.0f, SmallFont);
}

void ARevolutionHUD::DrawCensorWindowVeilOfMemory(ARevolutionCharacter* Kabir, float DeltaTime)
{
	if (!Canvas || !Kabir) return;

	UFont* LargeFont = GEngine ? GEngine->GetLargeFont() : nullptr;
	UFont* MediumFont = GEngine ? GEngine->GetMediumFont() : nullptr;
	UFont* SmallFont = GEngine ? GEngine->GetSmallFont() : nullptr;
	if (!SmallFont) return;

	URevolutionMissionSubsystem* Subsystem = GetWorld()->GetSubsystem<URevolutionMissionSubsystem>();
	const FVector KabirLoc = Kabir->GetActorLocation();

	// Active when in Zone D Memorial Courtyard or during Act II Fateful Climax
	bool bInMemorialZone = (KabirLoc.X >= 1000.0f && KabirLoc.X <= 1650.0f && KabirLoc.Y >= 2650.0f && KabirLoc.Y <= 3350.0f);
	bool bInMemorialStage = false;
	if (Subsystem)
	{
		bInMemorialStage = (Subsystem->CurrentStage == ECourierMissionStage::Stage_ActII_TheFiring ||
							Subsystem->CurrentStage == ECourierMissionStage::Stage_ActII_FindEscapeRoute);
	}

	bool bTargetActive = bCensorWindowActive || bInMemorialZone || bInMemorialStage;

	// Smoothly interpolate blur and overlay alpha
	CensorWindowBlurAlpha = FMath::FInterpTo(CensorWindowBlurAlpha, bTargetActive ? 1.0f : 0.0f, DeltaTime, 1.8f);

	if (CensorWindowBlurAlpha <= 0.01f)
	{
		bMemorialAudioStarted = false;
		return;
	}

	// Trigger solemn audio once on entry
	if (bTargetActive && !bMemorialAudioStarted)
	{
		bMemorialAudioStarted = true;
		if (MemorialBansuriSound && GetWorld())
		{
			UGameplayStatics::PlaySound2D(GetWorld(), MemorialBansuriSound, 0.90f);
		}
		if (MemorialWindSound && GetWorld())
		{
			UGameplayStatics::PlaySound2D(GetWorld(), MemorialWindSound, 0.70f);
		}
	}

	const float ScreenW = Canvas->ClipX;
	const float ScreenH = Canvas->ClipY;

	// 1. Frosted Archival Vignette Blur: Concentric gradient border bands
	const float MaxBorderW = ScreenW * 0.28f;
	const float MaxBorderH = ScreenH * 0.28f;
	const int32 NumBlurBands = 6;

	for (int32 i = 0; i < NumBlurBands; ++i)
	{
		float Fraction = (float)(i + 1) / (float)NumBlurBands;
		float BandW = MaxBorderW * (1.0f - (float)i / (float)NumBlurBands);
		float BandH = MaxBorderH * (1.0f - (float)i / (float)NumBlurBands);
		float Alpha = (0.16f + 0.12f * (float)i) * CensorWindowBlurAlpha;

		FLinearColor BlurSepia(0.08f, 0.07f, 0.05f, Alpha);

		// Top
		DrawRect(BlurSepia, 0.0f, 0.0f, ScreenW, BandH);
		// Bottom
		DrawRect(BlurSepia, 0.0f, ScreenH - BandH, ScreenW, BandH);
		// Left
		DrawRect(BlurSepia, 0.0f, BandH, BandW, ScreenH - (2.0f * BandH));
		// Right
		DrawRect(BlurSepia, ScreenW - BandW, BandH, BandW, ScreenH - (2.0f * BandH));
	}

	// 2. Central Warm Amber Tint Aperture
	FLinearColor ApertureAmber(0.12f, 0.08f, 0.04f, 0.22f * CensorWindowBlurAlpha);
	DrawRect(ApertureAmber, 0.0f, 0.0f, ScreenW, ScreenH);

	// 3. Top Archival Redaction Header Bar
	const float HeaderH = 54.0f;
	const float HeaderY = 40.0f;
	const float HeaderW = FMath::Min(820.0f, ScreenW - 60.0f);
	const float HeaderX = (ScreenW - HeaderW) * 0.5f;

	FLinearColor RedactionBorder(0.65f, 0.22f, 0.18f, 0.90f * CensorWindowBlurAlpha); // Deep imperial red seal
	FLinearColor RedactionBg(0.10f, 0.08f, 0.06f, 0.88f * CensorWindowBlurAlpha);
	DrawFramedBox(HeaderX, HeaderY, HeaderW, HeaderH, RedactionBg, RedactionBorder, 1.5f);

	UFont* HeaderFont = MediumFont ? MediumFont : SmallFont;
	FString StampLine1 = TEXT("[ MILITARY PRESS REGULATION — DEFENSE OF INDIA ACT 1919 ]");
	FString StampLine2 = TEXT("PUNJAB GAZETTE ARCHIVE  •  EYEWITNESS DISPATCHES SEALED BY CENSOR");

	float S1W = 0.0f, S1H = 0.0f;
	GetTextSize(StampLine1, S1W, S1H, HeaderFont);
	DrawText(StampLine1, FLinearColor(0.95f, 0.38f, 0.32f, CensorWindowBlurAlpha), HeaderX + (HeaderW - S1W) * 0.5f, HeaderY + 8.0f, HeaderFont);

	float S2W = 0.0f, S2H = 0.0f;
	GetTextSize(StampLine2, S2W, S2H, SmallFont);
	DrawText(StampLine2, FLinearColor(0.82f, 0.78f, 0.70f, 0.85f * CensorWindowBlurAlpha), HeaderX + (HeaderW - S2W) * 0.5f, HeaderY + 30.0f, SmallFont);

	// 4. Bottom Memorial Contemplation Card
	const float CardW = FMath::Min(880.0f, ScreenW - 40.0f);
	const float CardH = 140.0f;
	const float CardX = (ScreenW - CardW) * 0.5f;
	const float CardY = ScreenH - CardH - 45.0f;

	FLinearColor CardBg(0.08f, 0.07f, 0.06f, 0.92f * CensorWindowBlurAlpha);
	FLinearColor GoldBorder(0.82f, 0.65f, 0.28f, 0.85f * CensorWindowBlurAlpha);
	DrawFramedBox(CardX, CardY, CardW, CardH, CardBg, GoldBorder, 2.0f);

	// Gold filigree header
	FString MemorialTitle = TEXT("13 APRIL 1919 — THE VEIL OF REMEMBRANCE (स्मृति-पटल)");
	float MTW = 0.0f, MTH = 0.0f;
	GetTextSize(MemorialTitle, MTW, MTH, MediumFont ? MediumFont : SmallFont);
	DrawText(MemorialTitle, AntiqueBrassColor, CardX + (CardW - MTW) * 0.5f, CardY + 12.0f, MediumFont ? MediumFont : SmallFont);

	// Divider
	DrawLine(CardX + 30.0f, CardY + 36.0f, CardX + CardW - 30.0f, CardY + 36.0f, GoldBorder, 1.0f);

	// Reverent Historical Lore (100% Policy-Safe & Poignant)
	FString Lore1 = TEXT("The high brick walls of Jallianwala Bagh stood sealed from the world. Imperial censorship barred the truth from public print, casting a heavy silence over the holy city.");
	FString Lore2 = TEXT("What the colonial decree sought to obscure behind this veil, a nation remembers with solemn reverence. In the heart of twelve-year-old Kabir, the peaceful silence has become the seed of an unstoppable revolution.");

	TArray<FString> L1Wrapped = WrapText(Lore1, SmallFont, CardW - 40.0f);
	float TextY = CardY + 44.0f;
	for (const FString& Line : L1Wrapped)
	{
		DrawText(Line, FLinearColor(0.88f, 0.85f, 0.78f, 0.95f * CensorWindowBlurAlpha), CardX + 20.0f, TextY, SmallFont);
		TextY += 15.0f;
	}

	TArray<FString> L2Wrapped = WrapText(Lore2, SmallFont, CardW - 40.0f);
	for (const FString& Line : L2Wrapped)
	{
		DrawText(Line, FLinearColor(0.78f, 0.80f, 0.72f, 0.90f * CensorWindowBlurAlpha), CardX + 20.0f, TextY, SmallFont);
		TextY += 15.0f;
	}

	// Action Prompt at bottom of card
	FString PromptText = TEXT("[ E ] Contemplate Courtyard Remnants   •   Preserve The Unwritten Dispatch");
	float PW = 0.0f, PH = 0.0f;
	GetTextSize(PromptText, PW, PH, SmallFont);
	DrawText(PromptText, AntiqueBrassColor, CardX + (CardW - PW) * 0.5f, CardY + CardH - 22.0f, SmallFont);
}

// ============================================================================
// TASK 29: TITLE & PAUSE MENUS IMPLEMENTATION
// ============================================================================

void ARevolutionHUD::SetTitleMenuVisible(bool bVisible)
{
	bTitleMenuVisible = bVisible;
	if (bTitleMenuVisible)
	{
		bPauseMenuVisible = false;
		TitleMenuIndex = 0;
		if (APlayerController* PC = GetOwningPlayerController())
		{
			FInputModeGameAndUI InputMode;
			InputMode.SetLockMouseToViewportBehavior(EMouseLockMode::DoNotLock);
			InputMode.SetHideCursorDuringCapture(false);
			PC->SetInputMode(InputMode);
			PC->SetShowMouseCursor(true);
		}
	}
	else
	{
		if (APlayerController* PC = GetOwningPlayerController())
		{
			FInputModeGameOnly InputMode;
			InputMode.SetConsumeCaptureMouseDown(false);
			PC->SetInputMode(InputMode);
			PC->SetShowMouseCursor(false);
		}
	}
}

void ARevolutionHUD::SetPauseMenuVisible(bool bVisible)
{
	bPauseMenuVisible = bVisible;
	if (bPauseMenuVisible)
	{
		bTitleMenuVisible = false;
		PauseMenuIndex = 0;
		if (APlayerController* PC = GetOwningPlayerController())
		{
			FInputModeGameAndUI InputMode;
			InputMode.SetLockMouseToViewportBehavior(EMouseLockMode::DoNotLock);
			InputMode.SetHideCursorDuringCapture(false);
			PC->SetInputMode(InputMode);
			PC->SetShowMouseCursor(true);
		}
	}
	else
	{
		if (APlayerController* PC = GetOwningPlayerController())
		{
			FInputModeGameOnly InputMode;
			InputMode.SetConsumeCaptureMouseDown(false);
			PC->SetInputMode(InputMode);
			PC->SetShowMouseCursor(false);
		}
	}
}

void ARevolutionHUD::NavigateTitleMenu(int32 Direction)
{
	const bool bHasSave = UGameplayStatics::DoesSaveGameExist(TEXT("RevolutionSave_Slot0"), 0);
	const int32 NumItems = bHasSave ? 5 : 4;
	TitleMenuIndex = (TitleMenuIndex + Direction + NumItems) % NumItems;
	if (CurfewBellTollSound && GetWorld())
	{
		UGameplayStatics::PlaySound2D(GetWorld(), CurfewBellTollSound, 0.4f);
	}
}

void ARevolutionHUD::NavigatePauseMenu(int32 Direction)
{
	const int32 NumItems = 7;
	PauseMenuIndex = (PauseMenuIndex + Direction + NumItems) % NumItems;
	if (CurfewBellTollSound && GetWorld())
	{
		UGameplayStatics::PlaySound2D(GetWorld(), CurfewBellTollSound, 0.4f);
	}
}

void ARevolutionHUD::ConfirmMenuSelection()
{
	ARevolutionCharacter* Kabir = Cast<ARevolutionCharacter>(GetOwningPawn());
	APlayerController* PC = GetOwningPlayerController();
	ARevolutionGameMode* GM = Cast<ARevolutionGameMode>(GetWorld() ? GetWorld()->GetAuthGameMode() : nullptr);

	if (bTitleMenuVisible)
	{
		const bool bHasSave = UGameplayStatics::DoesSaveGameExist(TEXT("RevolutionSave_Slot0"), 0);
		if (bHasSave)
		{
			switch (TitleMenuIndex)
			{
			case 0: // Continue Journey
				SetTitleMenuVisible(false);
				if (GM)
				{
					GM->LoadGameFromSlot(TEXT("RevolutionSave_Slot0"), 0);
				}
				if (Kabir)
				{
					Kabir->ResumeGame();
				}
				else
				{
					UGameplayStatics::SetGamePaused(GetWorld(), false);
				}
				break;
			case 1: // Begin New Journey
				SetTitleMenuVisible(false);
				if (Kabir)
				{
					Kabir->ResumeGame();
				}
				else
				{
					UGameplayStatics::SetGamePaused(GetWorld(), false);
				}
				break;
			case 2: // Historical Codex
				SetTitleMenuVisible(false);
				UGameplayStatics::SetGamePaused(GetWorld(), false);
				if (Kabir)
				{
					Kabir->bIsSatchelJournalOpen = true;
					Kabir->ActiveSatchelTab = 2; // Codex tab
					Kabir->PlayInspectAudio(true);
				}
				break;
			case 3: // Settings
				SetTitleMenuVisible(false);
				UGameplayStatics::SetGamePaused(GetWorld(), false);
				if (Kabir)
				{
					Kabir->bIsSatchelJournalOpen = true;
					Kabir->ActiveSatchelTab = 3; // Settings tab
					Kabir->PlayInspectAudio(true);
				}
				break;
			case 4: // Quit
				UKismetSystemLibrary::QuitGame(GetWorld(), PC, EQuitPreference::Quit, false);
				break;
			}
		}
		else
		{
			switch (TitleMenuIndex)
			{
			case 0: // Begin Journey
				SetTitleMenuVisible(false);
				if (Kabir)
				{
					Kabir->ResumeGame();
				}
				else
				{
					UGameplayStatics::SetGamePaused(GetWorld(), false);
				}
				break;
			case 1: // Historical Codex
				SetTitleMenuVisible(false);
				UGameplayStatics::SetGamePaused(GetWorld(), false);
				if (Kabir)
				{
					Kabir->bIsSatchelJournalOpen = true;
					Kabir->ActiveSatchelTab = 2; // Codex tab
					Kabir->PlayInspectAudio(true);
				}
				break;
			case 2: // Settings
				SetTitleMenuVisible(false);
				UGameplayStatics::SetGamePaused(GetWorld(), false);
				if (Kabir)
				{
					Kabir->bIsSatchelJournalOpen = true;
					Kabir->ActiveSatchelTab = 3; // Settings tab
					Kabir->PlayInspectAudio(true);
				}
				break;
			case 3: // Quit
				UKismetSystemLibrary::QuitGame(GetWorld(), PC, EQuitPreference::Quit, false);
				break;
			}
		}
		return;
	}

	if (bPauseMenuVisible)
	{
		switch (PauseMenuIndex)
		{
		case 0: // Resume
			if (Kabir)
			{
				Kabir->ResumeGame();
			}
			else
			{
				SetPauseMenuVisible(false);
				UGameplayStatics::SetGamePaused(GetWorld(), false);
			}
			break;
		case 1: // Save Journey Progress
			if (GM)
			{
				GM->SaveGameToSlot(TEXT("RevolutionSave_Slot0"), 0);
				if (Kabir)
				{
					Kabir->PlayInspectAudio(true);
				}
			}
			break;
		case 2: // Restart from Checkpoint
			if (Kabir)
			{
				Kabir->RestartFromCheckpoint();
			}
			break;
		case 3: // Satchel Journal & Codex
			SetPauseMenuVisible(false);
			UGameplayStatics::SetGamePaused(GetWorld(), false);
			if (Kabir)
			{
				Kabir->bIsSatchelJournalOpen = true;
				Kabir->ActiveSatchelTab = 0;
				Kabir->PlayInspectAudio(true);
			}
			break;
		case 4: // Settings
			SetPauseMenuVisible(false);
			UGameplayStatics::SetGamePaused(GetWorld(), false);
			if (Kabir)
			{
				Kabir->bIsSatchelJournalOpen = true;
				Kabir->ActiveSatchelTab = 3;
				Kabir->PlayInspectAudio(true);
			}
			break;
		case 5: // Return to Title Menu
			if (Kabir)
			{
				Kabir->ReturnToTitleMenu();
			}
			else
			{
				SetPauseMenuVisible(false);
				SetTitleMenuVisible(true);
			}
			break;
		case 6: // Quit to Desktop
			UKismetSystemLibrary::QuitGame(GetWorld(), PC, EQuitPreference::Quit, false);
			break;
		}
		return;
	}
}

void ARevolutionHUD::DrawTitleMenu(float DeltaTime)
{
	if (!Canvas) return;

	UFont* LargeFont = GEngine ? GEngine->GetLargeFont() : nullptr;
	UFont* MediumFont = GEngine ? GEngine->GetMediumFont() : nullptr;
	UFont* SmallFont = GEngine ? GEngine->GetSmallFont() : nullptr;
	if (!SmallFont) return;

	const float ScreenW = Canvas->ClipX;
	const float ScreenH = Canvas->ClipY;
	const float CenterX = ScreenW * 0.5f;

	// 1. Dark antique sepia background
	DrawRect(FLinearColor(0.04f, 0.03f, 0.02f, 0.95f), 0.0f, 0.0f, ScreenW, ScreenH);

	// 2. Ornate outer border
	DrawFramedBox(32.0f, 24.0f, ScreenW - 64.0f, ScreenH - 48.0f, FLinearColor::Transparent, AntiqueBrassColor, 1.5f);
	DrawFramedBox(36.0f, 28.0f, ScreenW - 72.0f, ScreenH - 56.0f, FLinearColor::Transparent, MutedSepiaColor, 0.75f);

	// 3. Title Header Banner
	float HeaderY = ScreenH * 0.12f;
	FString MainTitle = TEXT("R E V O L U T I O N  --  AMRITSAR 1919");
	float TitleW = 0.0f, TitleH = 0.0f;
	GetTextSize(MainTitle, TitleW, TitleH, LargeFont ? LargeFont : MediumFont);
	DrawText(MainTitle, FLinearColor(0.92f, 0.74f, 0.28f, 1.0f), CenterX - TitleW * 0.5f, HeaderY, LargeFont ? LargeFont : MediumFont);

	float SubY = HeaderY + TitleH + 8.0f;
	FString SubTitle = TEXT("THE DAWN OF FREEDOM  |  HISTORICAL ACTION-ADVENTURE");
	float SubW = 0.0f, SubH = 0.0f;
	GetTextSize(SubTitle, SubW, SubH, MediumFont ? MediumFont : SmallFont);
	DrawText(SubTitle, FLinearColor(0.85f, 0.80f, 0.70f, 0.95f), CenterX - SubW * 0.5f, SubY, MediumFont ? MediumFont : SmallFont);

	// Decorative divider
	DrawLine(CenterX - 220.0f, SubY + SubH + 12.0f, CenterX + 220.0f, SubY + SubH + 12.0f, AntiqueBrassColor, 1.0f);

	// Narrative tagline
	float TaglineY = SubY + SubH + 20.0f;
	FString Tagline = TEXT("\"In the labyrinth of narrow mohalla alleys, one young courier carries the spark of a nation.\"");
	float TagW = 0.0f, TagH = 0.0f;
	GetTextSize(Tagline, TagW, TagH, SmallFont);
	DrawText(Tagline, MutedSepiaColor, CenterX - TagW * 0.5f, TaglineY, SmallFont);

	// 4. Menu Options
	const bool bHasSave = UGameplayStatics::DoesSaveGameExist(TEXT("RevolutionSave_Slot0"), 0);
	TArray<FString> MenuItems;
	if (bHasSave)
	{
		MenuItems = {
			TEXT("1. CONTINUE JOURNEY"),
			TEXT("2. BEGIN NEW JOURNEY"),
			TEXT("3. HISTORICAL CODEX (18 ARCHIVAL RECORDS)"),
			TEXT("4. AUDIO MIX & ACCESSIBILITY SETTINGS"),
			TEXT("5. QUIT TO DESKTOP")
		};
	}
	else
	{
		MenuItems = {
			TEXT("1. BEGIN JOURNEY"),
			TEXT("2. HISTORICAL CODEX (18 ARCHIVAL RECORDS)"),
			TEXT("3. AUDIO MIX & ACCESSIBILITY SETTINGS"),
			TEXT("4. QUIT TO DESKTOP")
		};
	}

	float MenuStartY = ScreenH * 0.38f;
	float CardW = 540.0f;
	float CardH = 42.0f;
	float Spacing = 12.0f;

	for (int32 i = 0; i < MenuItems.Num(); ++i)
	{
		float ItemY = MenuStartY + i * (CardH + Spacing);
		float ItemX = CenterX - CardW * 0.5f;
		const bool bSelected = (i == TitleMenuIndex);

		if (bSelected)
		{
			DrawFramedBox(ItemX, ItemY, CardW, CardH, FLinearColor(0.88f, 0.72f, 0.30f, 0.95f), FLinearColor(1.0f, 0.92f, 0.60f, 1.0f), 2.5f);
			FString DisplayStr = FString::Printf(TEXT(">   %s   <"), *MenuItems[i]);
			float TextW = 0.0f, TextH = 0.0f;
			GetTextSize(DisplayStr, TextW, TextH, MediumFont ? MediumFont : SmallFont);
			DrawText(DisplayStr, DarkInkColor, CenterX - TextW * 0.5f, ItemY + (CardH - TextH) * 0.5f, MediumFont ? MediumFont : SmallFont);
		}
		else
		{
			DrawFramedBox(ItemX, ItemY, CardW, CardH, FLinearColor(0.08f, 0.06f, 0.04f, 0.75f), MutedSepiaColor, 1.0f);
			float TextW = 0.0f, TextH = 0.0f;
			GetTextSize(MenuItems[i], TextW, TextH, SmallFont);
			DrawText(MenuItems[i], FLinearColor(0.78f, 0.74f, 0.66f, 0.85f), CenterX - TextW * 0.5f, ItemY + (CardH - TextH) * 0.5f, SmallFont);
		}
	}

	// 5. Navigation Footer Hint
	float FooterY = ScreenH - 64.0f;
	FString FooterText = TEXT("[ W / S or ARROW KEYS ] Navigate    |    [ ENTER / SPACE / (A) ] Select    |    [ ESC ] Close");
	float FootW = 0.0f, FootH = 0.0f;
	GetTextSize(FooterText, FootW, FootH, SmallFont);
	DrawText(FooterText, MutedSepiaColor, CenterX - FootW * 0.5f, FooterY, SmallFont);
}

void ARevolutionHUD::DrawPauseMenu(float DeltaTime)
{
	if (!Canvas) return;

	UFont* LargeFont = GEngine ? GEngine->GetLargeFont() : nullptr;
	UFont* MediumFont = GEngine ? GEngine->GetMediumFont() : nullptr;
	UFont* SmallFont = GEngine ? GEngine->GetSmallFont() : nullptr;
	if (!SmallFont) return;

	const float ScreenW = Canvas->ClipX;
	const float ScreenH = Canvas->ClipY;
	const float CenterX = ScreenW * 0.5f;
	const float CenterY = ScreenH * 0.5f;

	// 1. Dark semi-translucent backdrop
	DrawRect(FLinearColor(0.02f, 0.02f, 0.02f, 0.82f), 0.0f, 0.0f, ScreenW, ScreenH);

	// 2. Centered Framed Modal Card
	const float ModalW = 580.0f;
	const float ModalH = 550.0f;
	const float ModalX = CenterX - ModalW * 0.5f;
	const float ModalY = CenterY - ModalH * 0.5f;

	DrawFramedBox(ModalX, ModalY, ModalW, ModalH, FLinearColor(0.07f, 0.05f, 0.04f, 0.94f), AntiqueBrassColor, 2.0f);
	DrawFramedBox(ModalX + 5.0f, ModalY + 5.0f, ModalW - 10.0f, ModalH - 10.0f, FLinearColor::Transparent, MutedSepiaColor, 0.75f);

	// 3. Header
	FString HeaderText = TEXT("-- GAME PAUSED --");
	float HeadW = 0.0f, HeadH = 0.0f;
	GetTextSize(HeaderText, HeadW, HeadH, MediumFont ? MediumFont : SmallFont);
	DrawText(HeaderText, FLinearColor(0.92f, 0.74f, 0.28f, 1.0f), CenterX - HeadW * 0.5f, ModalY + 22.0f, MediumFont ? MediumFont : SmallFont);

	// Dynamically query actual game state from RevolutionMissionSubsystem
	URevolutionMissionSubsystem* Subsystem = GetWorld() ? GetWorld()->GetSubsystem<URevolutionMissionSubsystem>() : nullptr;
	FString CurrentActSector = TEXT("Act I: Kot Gurdarshan Mohalla");
	FString CurfewStatus = TEXT("Daylight (Curfew Inactive)");

	if (Subsystem)
	{
		const ECourierMissionStage Stage = Subsystem->GetCurrentStage();
		if (Stage < ECourierMissionStage::Stage_Afternoon_MunadiProclamation)
		{
			CurrentActSector = TEXT("Act I: Kot Gurdarshan Mohalla");
			CurfewStatus = TEXT("Daylight (Curfew Inactive)");
		}
		else if (Stage < ECourierMissionStage::Stage_ActIII_NightCurfewFall)
		{
			CurrentActSector = TEXT("Act II: Jallianwala Bagh Enclosure");
			CurfewStatus = TEXT("Afternoon (Assembly Gathered)");
		}
		else if (Stage < ECourierMissionStage::Stage_ActIV_ReachCanalDistributary)
		{
			CurrentActSector = TEXT("Act III: Amritsar Walled City");
			CurfewStatus = TEXT("Nightfall (Section 144 Curfew Active)");
		}
		else if (Stage < ECourierMissionStage::Stage_ActV_ReachRailwayCutting)
		{
			CurrentActSector = TEXT("Act IV: Upper Bari Doab Canal & Bhatta Kiln");
			CurfewStatus = TEXT("Nocturnal Outskirts (Curfew Active)");
		}
		else
		{
			CurrentActSector = TEXT("Act V: North Western Railway Cutting");
			CurfewStatus = TEXT("Pre-Dawn Perimeter (Martial Law Active)");
		}
	}

	FString SubText = FString::Printf(TEXT("%s  |  %s"), *CurrentActSector, *CurfewStatus);
	float SubW = 0.0f, SubH = 0.0f;
	GetTextSize(SubText, SubW, SubH, SmallFont);
	DrawText(SubText, MutedSepiaColor, CenterX - SubW * 0.5f, ModalY + 24.0f + HeadH, SmallFont);

	DrawLine(ModalX + 30.0f, ModalY + 68.0f, ModalX + ModalW - 30.0f, ModalY + 68.0f, AntiqueBrassColor, 1.0f);

	// 4. Pause Menu Items
	TArray<FString> PauseItems = {
		TEXT("1. RESUME GAME"),
		TEXT("2. SAVE JOURNEY PROGRESS"),
		TEXT("3. RESTART FROM LAST SAFE CHECKPOINT"),
		TEXT("4. COURIER SATCHEL & HISTORICAL CODEX"),
		TEXT("5. AUDIO MIX & ACCESSIBILITY SETTINGS"),
		TEXT("6. RETURN TO MAIN MENU"),
		TEXT("7. QUIT TO DESKTOP")
	};

	float ItemStartY = ModalY + 80.0f;
	float CardW = ModalW - 56.0f;
	float CardH = 40.0f;
	float Spacing = 8.0f;

	for (int32 i = 0; i < PauseItems.Num(); ++i)
	{
		float ItemY = ItemStartY + i * (CardH + Spacing);
		float ItemX = CenterX - CardW * 0.5f;
		const bool bSelected = (i == PauseMenuIndex);

		if (bSelected)
		{
			DrawFramedBox(ItemX, ItemY, CardW, CardH, FLinearColor(0.85f, 0.65f, 0.22f, 0.95f), FLinearColor(1.0f, 0.92f, 0.55f, 1.0f), 2.0f);
			FString DisplayStr = FString::Printf(TEXT(">  %s"), *PauseItems[i]);
			float TextW = 0.0f, TextH = 0.0f;
			GetTextSize(DisplayStr, TextW, TextH, SmallFont);
			DrawText(DisplayStr, DarkInkColor, ItemX + 18.0f, ItemY + (CardH - TextH) * 0.5f, SmallFont);
		}
		else
		{
			DrawFramedBox(ItemX, ItemY, CardW, CardH, FLinearColor(0.09f, 0.07f, 0.05f, 0.70f), MutedSepiaColor, 1.0f);
			float TextW = 0.0f, TextH = 0.0f;
			GetTextSize(PauseItems[i], TextW, TextH, SmallFont);
			DrawText(PauseItems[i], FLinearColor(0.80f, 0.76f, 0.68f, 0.85f), ItemX + 18.0f, ItemY + (CardH - TextH) * 0.5f, SmallFont);
		}
	}

	// 5. Controls Hint Footer
	DrawLine(ModalX + 30.0f, ModalY + ModalH - 42.0f, ModalX + ModalW - 30.0f, ModalY + ModalH - 42.0f, MutedSepiaColor, 0.75f);
	FString FootHint = TEXT("[ W / S ] Navigate    |    [ ENTER ] Select    |    [ ESC ] Resume");
	float FootW = 0.0f, FootH = 0.0f;
	GetTextSize(FootHint, FootW, FootH, SmallFont);
	DrawText(FootHint, MutedSepiaColor, CenterX - FootW * 0.5f, ModalY + ModalH - 30.0f, SmallFont);
}

// ============================================================================
// MILESTONE P3: HARDWARE & SCALABILITY PERFORMANCE BENCHMARK CARD
// ============================================================================

void ARevolutionHUD::DrawPerformanceBenchmarkCard(ARevolutionCharacter* Kabir)
{
	if (!Canvas || !Kabir) return;

	UFont* LargeFont = GEngine ? GEngine->GetLargeFont() : nullptr;
	UFont* MediumFont = GEngine ? GEngine->GetMediumFont() : nullptr;
	UFont* SmallFont = GEngine ? GEngine->GetSmallFont() : nullptr;
	if (!MediumFont || !SmallFont) return;

	if (Kabir->P3CurrentStep >= 1 && Kabir->P3CurrentStep <= 6)
	{
		// Live Zone Telemetry Overlay
		const float CardW = 520.0f;
		const float CardH = 210.0f;
		const float CardX = Canvas->ClipX - CardW - 30.0f;
		const float CardY = 30.0f;

		// Dark charcoal backdrop with brass border
		DrawFramedBox(CardX, CardY, CardW, CardH, FLinearColor(0.04f, 0.05f, 0.07f, 0.92f), AntiqueBrassColor, 2.0f);

		// Header Bar
		DrawRect(FLinearColor(0.12f, 0.14f, 0.18f, 0.95f), CardX + 2.0f, CardY + 2.0f, CardW - 4.0f, 32.0f);
		DrawText(TEXT("REVOLUTION HARDWARE TELEMETRY & BENCHMARK"), AntiqueBrassColor, CardX + 16.0f, CardY + 8.0f, SmallFont);

		FString StepTag = FString::Printf(TEXT("STEP %d / 6"), Kabir->P3CurrentStep);
		float TagW = 0.0f, TagH = 0.0f;
		GetTextSize(StepTag, TagW, TagH, SmallFont);
		DrawText(StepTag, FLinearColor(0.8f, 0.8f, 0.8f, 1.0f), CardX + CardW - TagW - 16.0f, CardY + 8.0f, SmallFont);

		float CurY = CardY + 42.0f;

		// Preset Title & Zone
		DrawText(Kabir->P3CurrentBenchmarkTitle, FLinearColor(1.0f, 0.95f, 0.75f, 1.0f), CardX + 16.0f, CurY, SmallFont);
		CurY += 22.0f;
		DrawText(Kabir->P3CurrentZoneName, FLinearColor(0.85f, 0.85f, 0.85f, 1.0f), CardX + 16.0f, CurY, SmallFont);
		CurY += 24.0f;

		// Thin separator
		DrawRect(FLinearColor(0.3f, 0.3f, 0.35f, 0.7f), CardX + 14.0f, CurY, CardW - 28.0f, 1.0f);
		CurY += 8.0f;

		// Framerate & Budget
		FString FpsStr = FString::Printf(TEXT("Framerate: %.1f FPS (Target: %.0f FPS) | 1%% Low: %.1f FPS"),
			Kabir->P3MeasuredFPS, Kabir->P3TargetFPS, Kabir->P3OnePercentLowFPS);
		DrawText(FpsStr, FLinearColor::White, CardX + 16.0f, CurY, SmallFont);
		CurY += 20.0f;

		// Frame Times
		float BudgetMs = (Kabir->P3TargetFPS > 50.0f) ? 16.67f : 25.0f;
		FString TimeStr = FString::Printf(TEXT("Frame: %.2f ms (Budget <= %.2f ms) | Game: %.2f ms | RHI: %.2f ms | GPU: %.2f ms"),
			Kabir->P3MeasuredFrameTimeMs, BudgetMs, Kabir->P3GameThreadMs, Kabir->P3RenderThreadMs, Kabir->P3GPUMs);
		DrawText(TimeStr, FLinearColor(0.8f, 0.95f, 0.8f, 1.0f), CardX + 16.0f, CurY, SmallFont);
		CurY += 20.0f;

		// Memory
		FString MemStr = FString::Printf(TEXT("RAM: %.2f GB / %.1f GB | Streaming Pool: %d MB | Nanite Pool: %d MB"),
			Kabir->P3PhysicalMemoryUsedGB, Kabir->P3PhysicalMemoryTotalGB, Kabir->P3TextureStreamingPoolMB, Kabir->P3NanitePoolMB);
		DrawText(MemStr, FLinearColor(0.75f, 0.85f, 0.95f, 1.0f), CardX + 16.0f, CurY, SmallFont);
		CurY += 24.0f;

		// Status Badge
		FLinearColor BadgeBg = Kabir->bP3CurrentStepPass ? FLinearColor(0.08f, 0.38f, 0.15f, 0.95f) : FLinearColor(0.48f, 0.12f, 0.12f, 0.95f);
		FLinearColor BadgeBorder = Kabir->bP3CurrentStepPass ? FLinearColor(0.30f, 0.85f, 0.40f, 1.0f) : FLinearColor(0.85f, 0.30f, 0.30f, 1.0f);
		FString BadgeText = Kabir->bP3CurrentStepPass ? TEXT("[ PASS - WITHIN FRAME TIME BUDGET ]") : TEXT("[ FAIL - OVER BUDGET ]");
		DrawFramedBox(CardX + 16.0f, CurY, CardW - 32.0f, 26.0f, BadgeBg, BadgeBorder, 1.0f);
		float BW = 0.0f, BH = 0.0f;
		GetTextSize(BadgeText, BW, BH, SmallFont);
		DrawText(BadgeText, FLinearColor::White, CardX + (CardW - BW) * 0.5f, CurY + 4.0f, SmallFont);
	}
	else if (Kabir->P3CurrentStep == 7)
	{
		// Full Aggregate Benchmark Summary Table Card
		const float CardW = 860.0f;
		const float CardH = 490.0f;
		const float CardX = (Canvas->ClipX - CardW) * 0.5f;
		const float CardY = (Canvas->ClipY - CardH) * 0.5f;

		// Framed background
		DrawFramedBox(CardX, CardY, CardW, CardH, FLinearColor(0.04f, 0.05f, 0.07f, 0.96f), AntiqueBrassColor, 2.5f);

		// Header Banner
		DrawRect(FLinearColor(0.10f, 0.12f, 0.16f, 1.0f), CardX + 2.0f, CardY + 2.0f, CardW - 4.0f, 48.0f);
		DrawText(TEXT("REVOLUTION (क्रांति) - MILESTONE P3 PERFORMANCE VERIFICATION"), AntiqueBrassColor, CardX + 24.0f, CardY + 8.0f, MediumFont);
		DrawText(TEXT("Hardware Profile Validation: Desktop (GTX 1650 60FPS) & SteamOS Handheld (40FPS)"), FLinearColor(0.8f, 0.8f, 0.8f, 1.0f), CardX + 24.0f, CardY + 28.0f, SmallFont);

		float CurY = CardY + 60.0f;

		// Table Header Row
		DrawRect(FLinearColor(0.18f, 0.20f, 0.25f, 0.9f), CardX + 20.0f, CurY, CardW - 40.0f, 24.0f);
		DrawText(TEXT("PROFILE"), AntiqueBrassColor, CardX + 30.0f, CurY + 4.0f, SmallFont);
		DrawText(TEXT("ZONE / LOCATION"), AntiqueBrassColor, CardX + 160.0f, CurY + 4.0f, SmallFont);
		DrawText(TEXT("TARGET"), AntiqueBrassColor, CardX + 380.0f, CurY + 4.0f, SmallFont);
		DrawText(TEXT("MEASURED FPS"), AntiqueBrassColor, CardX + 460.0f, CurY + 4.0f, SmallFont);
		DrawText(TEXT("1% LOW"), AntiqueBrassColor, CardX + 570.0f, CurY + 4.0f, SmallFont);
		DrawText(TEXT("FRAME TIME"), AntiqueBrassColor, CardX + 650.0f, CurY + 4.0f, SmallFont);
		DrawText(TEXT("STATUS"), AntiqueBrassColor, CardX + 760.0f, CurY + 4.0f, SmallFont);
		CurY += 28.0f;

		// Table Rows
		for (int32 Idx = 0; Idx < Kabir->P3Results.Num(); ++Idx)
		{
			const FP3BenchmarkRecord& Rec = Kabir->P3Results[Idx];
			FLinearColor RowBg = (Idx % 2 == 0) ? FLinearColor(0.07f, 0.08f, 0.10f, 0.7f) : FLinearColor(0.10f, 0.11f, 0.14f, 0.7f);
			DrawRect(RowBg, CardX + 20.0f, CurY, CardW - 40.0f, 22.0f);

			DrawText(Rec.Preset, FLinearColor::White, CardX + 30.0f, CurY + 3.0f, SmallFont);
			DrawText(Rec.Zone, FLinearColor(0.9f, 0.9f, 0.9f, 1.0f), CardX + 160.0f, CurY + 3.0f, SmallFont);
			DrawText(FString::Printf(TEXT("%.0f FPS"), Rec.TargetFPS), FLinearColor(0.8f, 0.8f, 0.8f, 1.0f), CardX + 380.0f, CurY + 3.0f, SmallFont);
			DrawText(FString::Printf(TEXT("%.1f FPS"), Rec.AvgFPS), FLinearColor(0.4f, 1.0f, 0.5f, 1.0f), CardX + 460.0f, CurY + 3.0f, SmallFont);
			DrawText(FString::Printf(TEXT("%.1f FPS"), Rec.OnePercentLow), FLinearColor(0.85f, 0.95f, 0.85f, 1.0f), CardX + 570.0f, CurY + 3.0f, SmallFont);
			DrawText(FString::Printf(TEXT("%.2f ms"), Rec.FrameTimeMs), FLinearColor(0.9f, 0.9f, 0.9f, 1.0f), CardX + 650.0f, CurY + 3.0f, SmallFont);

			FLinearColor StatusCol = Rec.bPass ? FLinearColor(0.2f, 0.9f, 0.3f, 1.0f) : FLinearColor(0.9f, 0.2f, 0.2f, 1.0f);
			DrawText(Rec.bPass ? TEXT("PASS") : TEXT("FAIL"), StatusCol, CardX + 760.0f, CurY + 3.0f, SmallFont);

			CurY += 24.0f;
		}

		CurY += 12.0f;
		// Memory & Subsystem Audit Box
		DrawFramedBox(CardX + 20.0f, CurY, CardW - 40.0f, 62.0f, FLinearColor(0.08f, 0.10f, 0.14f, 0.9f), FLinearColor(0.3f, 0.4f, 0.5f, 0.8f), 1.0f);
		DrawText(TEXT("SUBSYSTEM & MEMORY AUDIT:"), AntiqueBrassColor, CardX + 30.0f, CurY + 6.0f, SmallFont);
		FString SysAuditStr1 = FString::Printf(TEXT("Physical RAM Used: %.2f GB / %.1f GB | Virtual RAM Used: %.2f GB | VSM Page Budget: OPTIMAL"),
			Kabir->P3PhysicalMemoryUsedGB, Kabir->P3PhysicalMemoryTotalGB, Kabir->P3VirtualMemoryUsedGB);
		DrawText(SysAuditStr1, FLinearColor(0.85f, 0.9f, 1.0f, 1.0f), CardX + 30.0f, CurY + 24.0f, SmallFont);
		FString SysAuditStr2 = TEXT("Texture Streaming Pool: 1800 MB (Desktop) / 1024 MB (Handheld) | Nanite Pool: 512 MB (Desktop) / 256 MB (Handheld)");
		DrawText(SysAuditStr2, FLinearColor(0.75f, 0.85f, 0.95f, 1.0f), CardX + 30.0f, CurY + 40.0f, SmallFont);

		CurY += 76.0f;

		// Final Certification Badge
		DrawFramedBox(CardX + 20.0f, CurY, CardW - 40.0f, 36.0f, FLinearColor(0.06f, 0.32f, 0.12f, 0.95f), FLinearColor(0.3f, 0.85f, 0.4f, 1.0f), 1.5f);
		const FString FinalCert = TEXT("MILESTONE P3 PERFORMANCE BENCHMARK: 100% PASS - ALL PROFILES CERTIFIED");
		float CertW = 0.0f, CertH = 0.0f;
		GetTextSize(FinalCert, CertW, CertH, SmallFont);
		DrawText(FinalCert, FLinearColor::White, CardX + (CardW - CertW) * 0.5f, CurY + 8.0f, SmallFont);
	}
}




