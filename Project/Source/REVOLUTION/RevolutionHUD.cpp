// Copyright Epic Games, Inc. All Rights Reserved.

#include "RevolutionHUD.h"
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
#include "ProclamationBoardActor.h"
#include "Sound/SoundBase.h"
#include "RevolutionGameMode.h"
#include "Kismet/GameplayStatics.h"
#include "UObject/ConstructorHelpers.h"

ARevolutionHUD::ARevolutionHUD()
{
	// Default historical palette
	ParchmentColor = FLinearColor(0.93f, 0.89f, 0.80f, 0.96f);
	AntiqueBrassColor = FLinearColor(0.82f, 0.65f, 0.28f, 1.0f);
	DarkInkColor = FLinearColor(0.12f, 0.10f, 0.08f, 1.0f);
	MutedSepiaColor = FLinearColor(0.42f, 0.35f, 0.26f, 1.0f);

	StaminaDisplayAlpha = 0.0f;
	ReticleFocusPulse = 0.0f;
	LetterboxAlpha = 0.0f;
	OpeningPrologueTimer = 0.0f;

	static ConstructorHelpers::FObjectFinder<USoundBase> BellFinder(TEXT("/Game/Audio/SFX/SFX_Curfew_Bell_Toll.SFX_Curfew_Bell_Toll"));
	if (BellFinder.Succeeded())
	{
		CurfewBellTollSound = BellFinder.Object;
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
}

void ARevolutionHUD::DrawHUD()
{
	Super::DrawHUD();

	if (!Canvas) return;

	ARevolutionCharacter* Kabir = Cast<ARevolutionCharacter>(GetOwningPawn());
	if (!Kabir) return;

	float DeltaTime = GetWorld()->GetDeltaSeconds();
	OpeningPrologueTimer += DeltaTime;

	ARevolutionGameMode* GM = Cast<ARevolutionGameMode>(GetWorld()->GetAuthGameMode());
	URevolutionMissionSubsystem* Subsystem = GetWorld()->GetSubsystem<URevolutionMissionSubsystem>();

	const bool bApprehended = GM && GM->IsPlayerApprehended();
	const bool bMissionComplete = Subsystem && Subsystem->IsMissionComplete();

	if (bApprehended)
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
		DrawMissionDirectiveBanner(Kabir);
	}

	bool bForceLetterbox = (OpeningPrologueTimer < 7.5f) || Kabir->IsInspecting() || Kabir->IsSatchelJournalOpen() || bApprehended || bMissionComplete;
	DrawCinematicLetterbox(DeltaTime, bForceLetterbox);

	if (OpeningPrologueTimer < 7.5f && !bApprehended && !bMissionComplete)
	{
		DrawOpeningPrologueCard(DeltaTime);
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
	if (PromptText.IsEmpty())
	{
		PromptText = FText::FromString(TEXT("Interact"));
	}

	FString PromptStr = PromptText.ToString();
	float TextW = 0.0f, TextH = 0.0f;
	GetTextSize(PromptStr, TextW, TextH, MediumFont);

	const float KeyBadgeW = 34.0f;
	const float KeyBadgeH = 26.0f;
	const float PaddingX = 14.0f;
	const float Spacing = 10.0f;
	const float BoxW = KeyBadgeW + Spacing + TextW + (PaddingX * 2.0f);
	const float BoxH = 42.0f;

	const float BoxX = (Canvas->ClipX - BoxW) * 0.5f;
	const float BoxY = Canvas->ClipY * 0.72f;

	// Dark semi-translucent backdrop with antique brass border
	DrawFramedBox(BoxX, BoxY, BoxW, BoxH, FLinearColor(0.06f, 0.05f, 0.04f, 0.82f), AntiqueBrassColor, 1.5f);

	// Key badge background [ E ]
	const float BadgeX = BoxX + PaddingX;
	const float BadgeY = BoxY + (BoxH - KeyBadgeH) * 0.5f;
	DrawFramedBox(BadgeX, BadgeY, KeyBadgeW, KeyBadgeH, AntiqueBrassColor, FLinearColor(1.0f, 0.95f, 0.75f, 1.0f), 1.0f);

	// Key badge text "E"
	float KeyW = 0.0f, KeyH = 0.0f;
	GetTextSize(TEXT("E"), KeyW, KeyH, SmallFont);
	DrawText(TEXT("E"), DarkInkColor, BadgeX + (KeyBadgeW - KeyW) * 0.5f, BadgeY + (KeyBadgeH - KeyH) * 0.5f, SmallFont);

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

	FString DismissPrompt = TEXT("[ E ]  OR  [ SPACE ]  TO CLOSE INSPECTION");
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
	case ECourierMissionStage::Stage_Completed: StageTag = TEXT("1919 ACT I PROLOGUE  —  ACCOMPLISHED"); break;
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
	const float TabW = (BoxW - 48.0f) / 3.0f;
	const int32 ActiveTab = Kabir->GetActiveSatchelTab();

	const FString TabTitles[] = {
		TEXT("[ 1 ]  SATCHEL EQUIPMENT"),
		TEXT("[ 2 ]  MOHALLA ROUTE MAP"),
		TEXT("[ 3 ]  DISPATCHES & LORE")
	};

	for (int32 i = 0; i < 3; ++i)
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
	default:
		DrawSatchelTabDispatchesLore(Kabir, BoxX + 24.0f, ContentY, ContentW, ContentH);
		break;
	}

	// Bottom Navigation Footer
	DrawLine(BoxX + 16.0f, BoxY + BoxH - 32.0f, BoxX + BoxW - 16.0f, BoxY + BoxH - 32.0f, AntiqueBrassColor, 1.0f);

	FString FooterNav = TEXT("[ 1 / 2 / 3 ] Switch Section     |     [ TAB / J / E / ESC ] Close Satchel");
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

	// LEFT COLUMN: Equipment Items
	// Item 1: Tailored Khadi Coat Delivery
	float Item1Y = ContentY + 4.0f;
	float ItemH = (ContentH - 20.0f) / 3.0f;

	DrawFramedBox(BoxX, Item1Y, LeftW, ItemH, FLinearColor(0.88f, 0.84f, 0.74f, 0.90f), AntiqueBrassColor, 1.0f);
	DrawText(TEXT("Tailored Khadi Coat Parcel"), DarkInkColor, BoxX + 12.0f, Item1Y + 8.0f, MediumFont ? MediumFont : SmallFont);

	URevolutionMissionSubsystem* Subsystem = GetWorld() ? GetWorld()->GetSubsystem<URevolutionMissionSubsystem>() : nullptr;
	bool bHasCoat = Subsystem && (Subsystem->CurrentStage < ECourierMissionStage::Stage_Morning_DeliverCloth);

	FString CoatStatus = bHasCoat ? TEXT("STATUS: IN SATCHEL (DELIVER TO LALA KARAM CHAND)") : TEXT("STATUS: DELIVERED TO CLOTH GUILD");
	FLinearColor StatusCol = bHasCoat ? FLinearColor(0.85f, 0.52f, 0.15f, 1.0f) : FLinearColor(0.18f, 0.65f, 0.32f, 1.0f);
	DrawText(CoatStatus, StatusCol, BoxX + 12.0f, Item1Y + 28.0f, SmallFont);

	FString CoatDesc = TEXT("A finely stitched homespun khadi coat repaired by father Ram Lubhaya on the veranda Singer sewing machine. Intended for Lala Karam Chand in the Grand Bazaar.");
	TArray<FString> CoatLines = WrapText(CoatDesc, SmallFont, LeftW - 24.0f);
	float LineY = Item1Y + 48.0f;
	for (const FString& L : CoatLines)
	{
		DrawText(L, MutedSepiaColor, BoxX + 12.0f, LineY, SmallFont);
		LineY += 14.0f;
	}

	// Item 2: Tailor's Soapstone Chalk
	float Item2Y = Item1Y + ItemH + 6.0f;
	DrawFramedBox(BoxX, Item2Y, LeftW, ItemH, FLinearColor(0.88f, 0.84f, 0.74f, 0.90f), AntiqueBrassColor, 1.0f);

	FString ChalkHeader = FString::Printf(TEXT("Tailor's Soapstone Chalk  [%d / %d STICKS]"), Kabir->GetChalkCount(), Kabir->MaxChalk);
	DrawText(ChalkHeader, DarkInkColor, BoxX + 12.0f, Item2Y + 8.0f, MediumFont ? MediumFont : SmallFont);
	DrawText(TEXT("ACTION: PRESS [T] TO INSCRIBE ROOFTOP WAYPOINTS"), AntiqueBrassColor, BoxX + 12.0f, Item2Y + 28.0f, SmallFont);

	FString ChalkDesc = TEXT("Smooth white soapstone chalk taken from Kabir's father's tailoring shears bench. Used to mark rooftop jump ledges and safe escape paths with visible compass waypoints.");
	TArray<FString> ChalkLines = WrapText(ChalkDesc, SmallFont, LeftW - 24.0f);
	LineY = Item2Y + 48.0f;
	for (const FString& L : ChalkLines)
	{
		DrawText(L, MutedSepiaColor, BoxX + 12.0f, LineY, SmallFont);
		LineY += 14.0f;
	}

	// Item 3: Sun-Baked Clay Marbles
	float Item3Y = Item2Y + ItemH + 6.0f;
	DrawFramedBox(BoxX, Item3Y, LeftW, ItemH, FLinearColor(0.88f, 0.84f, 0.74f, 0.90f), AntiqueBrassColor, 1.0f);

	FString MarbleHeader = FString::Printf(TEXT("Sun-Baked Clay Marbles  [%d / %d PEBBLES]"), Kabir->GetPebbleCount(), Kabir->MaxPebbles);
	DrawText(MarbleHeader, DarkInkColor, BoxX + 12.0f, Item3Y + 8.0f, MediumFont ? MediumFont : SmallFont);
	DrawText(TEXT("ACTION: PRESS [F] TO LAUNCH ACOUSTIC DISTRACTION"), AntiqueBrassColor, BoxX + 12.0f, Item3Y + 28.0f, SmallFont);

	FString MarbleDesc = TEXT("Clay marbles rolled from Ravi river mud. Launched to clatter against brickwork, diverting curfew constables or scattering rooftop pigeons to mask clandestine movements.");
	TArray<FString> MarbleLines = WrapText(MarbleDesc, SmallFont, LeftW - 24.0f);
	LineY = Item3Y + 48.0f;
	for (const FString& L : MarbleLines)
	{
		DrawText(L, MutedSepiaColor, BoxX + 12.0f, LineY, SmallFont);
		LineY += 14.0f;
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

	// Grid coordinate mapping: World X [-240, 240] -> Screen X, World Y [-280, 280] -> Screen Y
	auto WorldToMap = [&](float WX, float WY) -> FVector2D
	{
		float NormX = (WX + 240.0f) / 480.0f;
		float NormY = (WY + 280.0f) / 560.0f;
		return FVector2D(
			CanvasAreaX + (NormX * CanvasAreaW),
			CanvasAreaY + (NormY * CanvasAreaH)
		);
	};

	// 1. Draw Architectural Structures on Map
	// Courtyard Boundary
	FVector2D C1 = WorldToMap(-120.0f, -140.0f);
	FVector2D C2 = WorldToMap(140.0f, 160.0f);
	DrawFramedBox(C1.X, C1.Y, C2.X - C1.X, C2.Y - C1.Y, FLinearColor(0.85f, 0.80f, 0.70f, 0.35f), MutedSepiaColor, 1.0f);
	DrawText(TEXT("HAVELI COURTYARD"), MutedSepiaColor, C1.X + 8.0f, C1.Y + 8.0f, SmallFont);

	// Deorhi Gateway (South)
	FVector2D DPos = WorldToMap(-20.0f, -240.0f);
	DrawFramedBox(DPos.X - 18.0f, DPos.Y - 6.0f, 36.0f, 12.0f, DarkInkColor, AntiqueBrassColor, 1.0f);
	DrawText(TEXT("[DEORHI GATE]"), DarkInkColor, DPos.X - 32.0f, DPos.Y + 8.0f, SmallFont);

	// Rooftop Parapet (North)
	FVector2D PPos = WorldToMap(0.0f, 240.0f);
	DrawFramedBox(PPos.X - 45.0f, PPos.Y - 6.0f, 90.0f, 12.0f, FLinearColor(0.4f, 0.3f, 0.2f, 0.6f), AntiqueBrassColor, 1.0f);
	DrawText(TEXT("[ROOFTOP PARAPET & PIGEONS]"), DarkInkColor, PPos.X - 60.0f, PPos.Y - 20.0f, SmallFont);

	// Jharokha Balcony (West)
	FVector2D JPos = WorldToMap(-190.0f, -60.0f);
	DrawFramedBox(JPos.X - 14.0f, JPos.Y - 14.0f, 28.0f, 28.0f, FLinearColor(0.2f, 0.45f, 0.3f, 0.5f), AntiqueBrassColor, 1.0f);
	DrawText(TEXT("[COURIER STASH]"), DarkInkColor, JPos.X - 35.0f, JPos.Y + 16.0f, SmallFont);

	// Low Drain Conduit (West wall)
	FVector2D DrainPos = WorldToMap(-120.0f, 90.0f);
	DrawFramedBox(DrainPos.X - 12.0f, DrainPos.Y - 6.0f, 24.0f, 12.0f, FLinearColor(0.88f, 0.55f, 0.2f, 0.8f), DarkInkColor, 1.0f);
	DrawText(TEXT("[MORI DRAIN]"), DarkInkColor, DrainPos.X - 28.0f, DrainPos.Y + 8.0f, SmallFont);

	// Outer Alley Curfew Patrol Route (South)
	FVector2D A1 = WorldToMap(-220.0f, -240.0f);
	FVector2D A2 = WorldToMap(220.0f, -240.0f);
	DrawLine(A1.X, A1.Y, A2.X, A2.Y, FLinearColor(0.85f, 0.25f, 0.20f, 0.65f), 2.0f);
	DrawText(TEXT("!  CURFEW PATROL ROUTE  !"), FLinearColor(0.85f, 0.25f, 0.20f, 0.85f), A1.X + 20.0f, A1.Y - 16.0f, SmallFont);

	// Clandestine Litho Press (North-East Alcove)
	FVector2D LithoPos = WorldToMap(115.0f, 185.0f);
	DrawFramedBox(LithoPos.X - 10.0f, LithoPos.Y - 6.0f, 20.0f, 12.0f, FLinearColor(0.2f, 0.35f, 0.55f, 0.8f), DarkInkColor, 1.0f);
	DrawText(TEXT("[LITHO PRESS]"), DarkInkColor, LithoPos.X - 30.0f, LithoPos.Y + 8.0f, SmallFont);

	// Colonial Checkpoint Barricade (Far South Gate)
	FVector2D BarPos = WorldToMap(-20.0f, -270.0f);
	DrawFramedBox(BarPos.X - 16.0f, BarPos.Y - 4.0f, 32.0f, 8.0f, FLinearColor(0.85f, 0.15f, 0.15f, 0.9f), DarkInkColor, 1.0f);
	DrawText(TEXT("[CHECKPOINT]"), FLinearColor(0.85f, 0.15f, 0.15f, 1.0f), BarPos.X - 32.0f, BarPos.Y + 6.0f, SmallFont);

	// Telegraph Wire Sabotage Post (Rooftop North-East)
	FVector2D WirePos = WorldToMap(60.0f, 240.0f);
	DrawFramedBox(WirePos.X - 8.0f, WirePos.Y - 8.0f, 16.0f, 16.0f, FLinearColor(0.7f, 0.6f, 0.2f, 0.85f), DarkInkColor, 1.0f);
	DrawText(TEXT("[TELEGRAPH]"), DarkInkColor, WirePos.X - 28.0f, WirePos.Y - 14.0f, SmallFont);

	// Sleeping Mohalla Dog (Alley South-West)
	FVector2D DogPos = WorldToMap(-155.0f, -40.0f);
	DrawFramedBox(DogPos.X - 8.0f, DogPos.Y - 6.0f, 16.0f, 12.0f, FLinearColor(0.6f, 0.45f, 0.3f, 0.8f), DarkInkColor, 1.0f);
	DrawText(TEXT("[STRAY DOG]"), DarkInkColor, DogPos.X - 25.0f, DogPos.Y + 8.0f, SmallFont);

	// Wheat Chaff Decoy Screen (Courtyard East)
	FVector2D ChaffPos = WorldToMap(85.0f, 60.0f);
	DrawFramedBox(ChaffPos.X - 8.0f, ChaffPos.Y - 6.0f, 16.0f, 12.0f, FLinearColor(0.88f, 0.78f, 0.4f, 0.8f), DarkInkColor, 1.0f);
	DrawText(TEXT("[CHAFF SCREEN]"), DarkInkColor, ChaffPos.X - 32.0f, ChaffPos.Y + 8.0f, SmallFont);

	// 2. Draw Real-Time Scout Chalk Marks
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

	// 3. Draw Real-Time Player Position (Kabir)
	FVector PlayerLoc = Kabir->GetActorLocation();
	FVector2D PMap = WorldToMap(PlayerLoc.X, PlayerLoc.Y);
	FLinearColor PlayerCol = FLinearColor(0.20f, 0.78f, 0.42f, 1.0f);

	// Player Diamond
	DrawLine(PMap.X - 6.0f, PMap.Y, PMap.X, PMap.Y - 6.0f, PlayerCol, 2.0f);
	DrawLine(PMap.X, PMap.Y - 6.0f, PMap.X + 6.0f, PMap.Y, PlayerCol, 2.0f);
	DrawLine(PMap.X + 6.0f, PMap.Y, PMap.X, PMap.Y + 6.0f, PlayerCol, 2.0f);
	DrawLine(PMap.X, PMap.Y + 6.0f, PMap.X - 6.0f, PMap.Y, PlayerCol, 2.0f);

	// Player facing direction notch
	FRotator ControlRot = Kabir->GetControlRotation();
	float Rad = FMath::DegreesToRadians(ControlRot.Yaw - 90.0f);
	DrawLine(PMap.X, PMap.Y, PMap.X + (FMath::Cos(Rad) * 12.0f), PMap.Y + (FMath::Sin(Rad) * 12.0f), PlayerCol, 2.0f);

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
		LegY += 22.0f;
	};

	DrawLegendItem(TEXT("<>"), TEXT("Kabir (Scout)"), PlayerCol);
	DrawLegendItem(TEXT("[M]"), TEXT("Tailor's Chalk Mark"), FLinearColor(0.95f, 0.94f, 0.90f, 1.0f));
	DrawLegendItem(TEXT("[#]"), TEXT("Deorhi Gate & Kundi"), AntiqueBrassColor);
	DrawLegendItem(TEXT("[S]"), TEXT("Courier Stash Box"), FLinearColor(0.2f, 0.65f, 0.3f, 1.0f));
	DrawLegendItem(TEXT("[D]"), TEXT("Haveli Drain Crawl"), FLinearColor(0.88f, 0.55f, 0.2f, 1.0f));
	DrawLegendItem(TEXT("[P]"), TEXT("Rooftop Parapet"), MutedSepiaColor);
	DrawLegendItem(TEXT("---"), TEXT("Curfew Patrol Alley"), FLinearColor(0.85f, 0.25f, 0.20f, 1.0f));
}

void ARevolutionHUD::DrawSatchelTabDispatchesLore(ARevolutionCharacter* Kabir, float BoxX, float ContentY, float ContentW, float ContentH)
{
	UFont* SmallFont = GEngine ? GEngine->GetSmallFont() : nullptr;
	UFont* MediumFont = GEngine ? GEngine->GetMediumFont() : nullptr;
	if (!SmallFont) return;

	// Two-column layout for discovered historical artifacts
	const float ColW = (ContentW - 16.0f) * 0.5f;
	const float Col1X = BoxX;
	const float Col2X = BoxX + ColW + 16.0f;

	struct FLoreEntry
	{
		FString Title;
		FString Category;
		FString Description;
	};

	static const FLoreEntry Entries[] = {
		{
			TEXT("Dietz No. 2 Hurricane Lantern"),
			TEXT("Colonial Lighting  •  Cold-Blast Draft"),
			TEXT("Tinplate kerosene lantern used by Punjab night chaukidars. Burns kerosene distributed under colonial wartime quotas.")
		},
		{
			TEXT("Woven Moonj Charpai"),
			TEXT("Traditional Artisan Furniture"),
			TEXT("Daybed woven from twisted moonj river-grass rope over shisham hardwood rails. The social anchor of Punjabi haveli courtyards.")
		},
		{
			TEXT("Terracotta Chai Kulhad"),
			TEXT("Pottery  •  Bazaar Culture"),
			TEXT("Disposable unglazed clay cup hand-thrown by town kumhars. Imparts an authentic earthy aroma (saundhi khushboo) to boiled tea.")
		},
		{
			TEXT("Burlap Jute Ration Sack"),
			TEXT("Imperial Wartime Procurement"),
			TEXT("Heavy burlap sacks stamped with imperial seals. Requisitioned wheat intended for Mesopotamia, leaving Punjab bazaars inflated.")
		},
		{
			TEXT("Hardwood Kite Charkhi"),
			TEXT("Basant Festival  •  Signaling"),
			TEXT("Hardwood kite spool with glass-coated manja line. Young rooftop scouts used colored kites to signal across railway tracks.")
		},
		{
			TEXT("Aged Teak Deorhi Gateway"),
			TEXT("Haveli Architecture  •  Iron Kundi"),
			TEXT("Massive double doors forged from aged Burma teak with wrought-iron slide bolts, separating public alleys from private sanctuary.")
		},
		{
			TEXT("Carved Teak Jharokha"),
			TEXT("Walled City Balcony"),
			TEXT("Overhanging timber lattice balcony allowing residents and scouts to observe British garrison movements without being seen.")
		},
		{
			TEXT("Haveli Storm-Drain Arch"),
			TEXT("Runoff Conduit  •  Mori Traversal"),
			TEXT("Low brick conduit running through boundary walls. Allows 12-year-old Kabir to crawl on hands and knees to evade colonial watchmen.")
		}
	};

	const float CardH = (ContentH - 24.0f) / 4.0f;

	for (int32 i = 0; i < 8; ++i)
	{
		float CurX = (i < 4) ? Col1X : Col2X;
		float CurY = ContentY + 4.0f + ((i % 4) * (CardH + 6.0f));

		DrawFramedBox(CurX, CurY, ColW, CardH, FLinearColor(0.88f, 0.84f, 0.74f, 0.90f), AntiqueBrassColor, 1.0f);

		DrawText(Entries[i].Title, DarkInkColor, CurX + 10.0f, CurY + 6.0f, MediumFont ? MediumFont : SmallFont);
		DrawText(Entries[i].Category, AntiqueBrassColor, CurX + 10.0f, CurY + 24.0f, SmallFont);

		TArray<FString> Wrapped = WrapText(Entries[i].Description, SmallFont, ColW - 20.0f);
		float TextY = CurY + 42.0f;
		for (const FString& Line : Wrapped)
		{
			DrawText(Line, MutedSepiaColor, CurX + 10.0f, TextY, SmallFont);
			TextY += 13.0f;
		}
	}
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



