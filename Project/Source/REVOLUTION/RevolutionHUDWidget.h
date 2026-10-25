// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "RevolutionHUDWidget.generated.h"

class ARevolutionCharacter;

/**
 * Base UMG Widget class for REVOLUTION HUD
 * Exposes Blueprint events for designers to bind to UI animations and rich widgets.
 */
UCLASS()
class REVOLUTION_API URevolutionHUDWidget : public UUserWidget
{
	GENERATED_BODY()

public:
	UFUNCTION(BlueprintImplementableEvent, Category = "Revolution|HUD")
	void OnInteractionFocusChanged(bool bHasFocus, const FText& PromptText);

	UFUNCTION(BlueprintImplementableEvent, Category = "Revolution|HUD")
	void OnInspectionStarted(const FText& ItemName, const FText& LoreDescription);

	UFUNCTION(BlueprintImplementableEvent, Category = "Revolution|HUD")
	void OnInspectionEnded();

	UFUNCTION(BlueprintImplementableEvent, Category = "Revolution|HUD")
	void OnStaminaUpdated(float CurrentStamina, float MaxStamina, bool bIsSprinting);

	UFUNCTION(BlueprintCallable, Category = "Revolution|HUD")
	void InitializeWithCharacter(ARevolutionCharacter* Character);

protected:
	UFUNCTION()
	void HandleInteractionFocusChanged(bool bHasFocus, FText PromptText);

	UFUNCTION()
	void HandleInspectionStarted(FText ItemName, FText LoreDescription);

	UFUNCTION()
	void HandleInspectionEnded();
};
