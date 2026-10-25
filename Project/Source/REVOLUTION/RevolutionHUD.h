// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/HUD.h"
#include "RevolutionHUD.generated.h"

class ARevolutionCharacter;
class URevolutionHUDWidget;
class USoundBase;

/**
 * Historical Cinematic HUD for REVOLUTION
 * Provides tactile, grounded period UI elements:
 * - Minimalist crosshair & contextual interact reticle
 * - Dynamic interaction prompt badge ([E] Action)
 * - Historical Inspection Lore Modal (Parchment card with gold borders, period typography, dismiss prompt)
 * - Dynamic stamina indicator (smooth fade in/out antique brass meter)
 * - Mohalla compass orientation ticker
 */
UCLASS()
class REVOLUTION_API ARevolutionHUD : public AHUD
{
	GENERATED_BODY()

public:
	ARevolutionHUD();

	virtual void DrawHUD() override;

protected:
	virtual void BeginPlay() override;

	/** Draw the minimal focus reticle */
	void DrawReticle(ARevolutionCharacter* Kabir);

	/** Draw the contextual interaction prompt */
	void DrawInteractionPrompt(ARevolutionCharacter* Kabir);

	/** Draw the full historical inspection modal */
	void DrawInspectionModal(ARevolutionCharacter* Kabir);

	/** Draw dynamic stamina meter */
	void DrawStaminaGauge(ARevolutionCharacter* Kabir);

	/** Draw top compass orientation ribbon */
	void DrawCompass(ARevolutionCharacter* Kabir);

	/** Draw stealth suspicion indicator and threat direction arc */
	void DrawStealthAndDetection(ARevolutionCharacter* Kabir);

	/** Draw predictive parabolic pebble aim trajectory and impact beacon (A Plague Tale benchmark) */
	void DrawPebbleAimTrajectory(ARevolutionCharacter* Kabir);

	/** Draw Keen Senses tactical beacons (Assassin's Creed / Hitman benchmark) */
	void DrawKeenSensesBeacons(ARevolutionCharacter* Kabir);

	/** Draw tactile in-world objective beacon and distance indicator */
	void DrawInWorldObjectiveBeacon(ARevolutionCharacter* Kabir);

	/** Draw Environmental Shadow Concealment meter (Thief / Dishonored benchmark) */
	void DrawConcealmentMeter(ARevolutionCharacter* Kabir);

	/** Draw clandestine courier mission directive banner */
	void DrawMissionDirectiveBanner(ARevolutionCharacter* Kabir);

	/** Draw anamorphic 2.39:1 letterbox bars */
	void DrawCinematicLetterbox(float DeltaTime, bool bForceActive);

	/** Draw historical prologue title sequence */
	void DrawOpeningPrologueCard(float DeltaTime);

	/** Draw tactile courier satchel & field journal modal */
	void DrawSatchelJournalModal(ARevolutionCharacter* Kabir);
	void DrawSatchelTabEquipment(ARevolutionCharacter* Kabir, float BoxX, float ContentY, float ContentW, float ContentH);
	void DrawSatchelTabMohallaMap(ARevolutionCharacter* Kabir, float BoxX, float ContentY, float ContentW, float ContentH);
	void DrawSatchelTabDispatchesLore(ARevolutionCharacter* Kabir, float BoxX, float ContentY, float ContentW, float ContentH);
	void DrawSatchelTabHistoricalCodex(ARevolutionCharacter* Kabir, float BoxX, float ContentY, float ContentW, float ContentH);
	void DrawSatchelTabSettingsControls(ARevolutionCharacter* Kabir, float BoxX, float ContentY, float ContentW, float ContentH);

	/** Draw Section 144 martial law curfew apprehension modal card */
	void DrawApprehendedCard(ARevolutionCharacter* Kabir);

	/** Draw dawn mission accomplished & town-wide Hartal chronicle modal card */
	void DrawMissionAccomplishedCard(ARevolutionCharacter* Kabir);

	/** Draw the stylized Censor Window & Veil of Memory archival presentation */
	void DrawCensorWindowVeilOfMemory(ARevolutionCharacter* Kabir, float DeltaTime);

	/** Draw cinematic cutscene chapter titles and subtitle captions */
	void DrawCinematicCaptions(float DeltaTime);

	/** Helper to draw a framed card with outer/inner borders */
	void DrawFramedBox(float X, float Y, float Width, float Height, const FLinearColor& FillColor, const FLinearColor& BorderColor, float BorderThickness = 2.0f);

	/** Helper to wrap text into lines */
	TArray<FString> WrapText(const FString& Text, UFont* InFont, float MaxWidth);

	/** Draw Milestone P3 Hardware Performance & Telemetry Benchmark Card */
	void DrawPerformanceBenchmarkCard(ARevolutionCharacter* Kabir);

public:
	UPROPERTY(VisibleAnywhere, BlueprintReadWrite, Category = "Revolution|Cinematic")
	bool bCinematicSequenceActive = false;

	UPROPERTY(VisibleAnywhere, BlueprintReadWrite, Category = "Revolution|Cinematic")
	FText CinematicSubtitleText;

	UPROPERTY(VisibleAnywhere, BlueprintReadWrite, Category = "Revolution|Cinematic")
	FText CinematicChapterTitle;

	UFUNCTION(BlueprintCallable, Category = "Revolution|Cinematic")
	void SetCinematicSequenceActive(bool bActive, const FText& InChapterTitle = FText::GetEmpty(), const FText& InSubtitleText = FText::GetEmpty());

	UFUNCTION(BlueprintCallable, Category = "Revolution|Cinematic")
	void SetCinematicSubtitle(const FText& InSubtitle);

	// --- TASK 29: TITLE & PAUSE MENUS ---
	UPROPERTY(VisibleAnywhere, BlueprintReadWrite, Category = "Revolution|UI")
	bool bTitleMenuVisible = false;

	UPROPERTY(VisibleAnywhere, BlueprintReadWrite, Category = "Revolution|UI")
	bool bPauseMenuVisible = false;

	UPROPERTY(VisibleAnywhere, BlueprintReadWrite, Category = "Revolution|UI")
	int32 TitleMenuIndex = 0;

	UPROPERTY(VisibleAnywhere, BlueprintReadWrite, Category = "Revolution|UI")
	int32 PauseMenuIndex = 0;

	UFUNCTION(BlueprintCallable, Category = "Revolution|UI")
	void SetTitleMenuVisible(bool bVisible);

	UFUNCTION(BlueprintPure, Category = "Revolution|UI")
	bool IsTitleMenuVisible() const { return bTitleMenuVisible; }

	UFUNCTION(BlueprintCallable, Category = "Revolution|UI")
	void SetPauseMenuVisible(bool bVisible);

	UFUNCTION(BlueprintPure, Category = "Revolution|UI")
	bool IsPauseMenuVisible() const { return bPauseMenuVisible; }

	UFUNCTION(BlueprintCallable, Category = "Revolution|UI")
	void NavigateTitleMenu(int32 Direction);

	UFUNCTION(BlueprintCallable, Category = "Revolution|UI")
	void NavigatePauseMenu(int32 Direction);

	UFUNCTION(BlueprintCallable, Category = "Revolution|UI")
	void ConfirmMenuSelection();

protected:
	void DrawTitleMenu(float DeltaTime);
	void DrawPauseMenu(float DeltaTime);

public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|UI")
	bool bShowReticle = true;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|UI")
	bool bShowCompass = true;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|UI")
	bool bShowStamina = true;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|UI")
	bool bShowInteractionPrompt = true;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|UI")
	bool bShowStealthIndicators = true;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|UI")
	bool bShowMissionBanner = true;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|UI")
	bool bShowObjectiveBeacons = true;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|UI")
	FLinearColor ParchmentColor = FLinearColor(0.93f, 0.89f, 0.80f, 0.96f);

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|UI")
	FLinearColor AntiqueBrassColor = FLinearColor(0.82f, 0.65f, 0.28f, 1.0f);

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|UI")
	FLinearColor DarkInkColor = FLinearColor(0.12f, 0.10f, 0.08f, 1.0f);

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|UI")
	FLinearColor MutedSepiaColor = FLinearColor(0.42f, 0.35f, 0.26f, 1.0f);

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|UI")
	TSubclassOf<URevolutionHUDWidget> HUDWidgetClass;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|UI")
	bool bEnableCinematicLetterbox = true;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* CurfewBellTollSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* MemorialBansuriSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* MemorialWindSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|UI")
	bool bCensorWindowActive = false;

	UPROPERTY(Transient, BlueprintReadOnly, Category = "Revolution|UI")
	URevolutionHUDWidget* HUDWidgetInstance = nullptr;

private:
	float StaminaDisplayAlpha = 0.0f;
	float ReticleFocusPulse = 0.0f;
	float LetterboxAlpha = 0.0f;
	float OpeningPrologueTimer = 0.0f;
	float CensorWindowBlurAlpha = 0.0f;
	bool bMemorialAudioStarted = false;
};
