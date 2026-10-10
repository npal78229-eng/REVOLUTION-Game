// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/HUD.h"
#include "RevolutionHUD.generated.h"

class ARevolutionCharacter;
class URevolutionHUDWidget;

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

	/** Helper to draw a framed card with outer/inner borders */
	void DrawFramedBox(float X, float Y, float Width, float Height, const FLinearColor& FillColor, const FLinearColor& BorderColor, float BorderThickness = 2.0f);

	/** Helper to wrap text into lines */
	TArray<FString> WrapText(const FString& Text, UFont* InFont, float MaxWidth);

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
	FLinearColor ParchmentColor = FLinearColor(0.93f, 0.89f, 0.80f, 0.96f);

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|UI")
	FLinearColor AntiqueBrassColor = FLinearColor(0.82f, 0.65f, 0.28f, 1.0f);

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|UI")
	FLinearColor DarkInkColor = FLinearColor(0.12f, 0.10f, 0.08f, 1.0f);

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|UI")
	FLinearColor MutedSepiaColor = FLinearColor(0.42f, 0.35f, 0.26f, 1.0f);

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|UI")
	TSubclassOf<URevolutionHUDWidget> HUDWidgetClass;

	UPROPERTY(Transient, BlueprintReadOnly, Category = "Revolution|UI")
	URevolutionHUDWidget* HUDWidgetInstance = nullptr;

private:
	float StaminaDisplayAlpha = 0.0f;
	float ReticleFocusPulse = 0.0f;
};
