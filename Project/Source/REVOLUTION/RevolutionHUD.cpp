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

ARevolutionHUD::ARevolutionHUD()
{
	// Default historical palette
	ParchmentColor = FLinearColor(0.93f, 0.89f, 0.80f, 0.96f);
	AntiqueBrassColor = FLinearColor(0.82f, 0.65f, 0.28f, 1.0f);
	DarkInkColor = FLinearColor(0.12f, 0.10f, 0.08f, 1.0f);
	MutedSepiaColor = FLinearColor(0.42f, 0.35f, 0.26f, 1.0f);

	StaminaDisplayAlpha = 0.0f;
	ReticleFocusPulse = 0.0f;
}

void ARevolutionHUD::BeginPlay()
{
	Super::BeginPlay();

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

	if (Kabir->IsInspecting())
	{
		DrawInspectionModal(Kabir);
	}
	else
	{
		DrawCompass(Kabir);
		DrawReticle(Kabir);
		DrawInteractionPrompt(Kabir);
		DrawStaminaGauge(Kabir);
		DrawStealthAndDetection(Kabir);
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
}

void ARevolutionHUD::DrawStealthAndDetection(ARevolutionCharacter* Kabir)
{
	if (!bShowStealthIndicators || !Canvas || !Kabir) return;

	UFont* SmallFont = GEngine ? GEngine->GetSmallFont() : nullptr;

	// 1. Stance Concealment Badge (Lower Left)
	if (Kabir->bIsCrouched && SmallFont)
	{
		FString StanceText = TEXT("[ CROUCHED — CONCEALED ]");
		float StanceW = 0.0f, StanceH = 0.0f;
		GetTextSize(StanceText, StanceW, StanceH, SmallFont);

		float BadgeX = 36.0f;
		float BadgeY = Canvas->ClipY * 0.88f;

		DrawFramedBox(BadgeX, BadgeY, StanceW + 16.0f, StanceH + 8.0f, FLinearColor(0.06f, 0.05f, 0.04f, 0.70f), AntiqueBrassColor, 1.0f);
		DrawText(StanceText, AntiqueBrassColor, BadgeX + 8.0f, BadgeY + 4.0f, SmallFont);
	}

	// 2. Scan for active Watchman Detection
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
			float BannerY = 58.0f;

			DrawFramedBox(BannerX, BannerY, BannerW, BannerH, FLinearColor(0.12f, 0.02f, 0.02f, 0.85f), ThreatColor, 1.5f);
			DrawText(AlertText, FLinearColor(1.0f, 0.9f, 0.85f, 1.0f), BannerX + 16.0f, BannerY + 6.0f, SmallFont);
		}
	}
}
