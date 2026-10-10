// Copyright Epic Games, Inc. All Rights Reserved.

#include "RevolutionHUDWidget.h"
#include "RevolutionCharacter.h"

void URevolutionHUDWidget::InitializeWithCharacter(ARevolutionCharacter* Character)
{
	if (!Character) return;

	Character->OnInteractionFocusChanged.AddDynamic(this, &URevolutionHUDWidget::HandleInteractionFocusChanged);
	Character->OnItemInspected.AddDynamic(this, &URevolutionHUDWidget::HandleInspectionStarted);
	Character->OnInspectionEnded.AddDynamic(this, &URevolutionHUDWidget::HandleInspectionEnded);
}

void URevolutionHUDWidget::HandleInteractionFocusChanged(bool bHasFocus, FText PromptText)
{
	OnInteractionFocusChanged(bHasFocus, PromptText);
}

void URevolutionHUDWidget::HandleInspectionStarted(FText ItemName, FText LoreDescription)
{
	OnInspectionStarted(ItemName, LoreDescription);
}

void URevolutionHUDWidget::HandleInspectionEnded()
{
	OnInspectionEnded();
}
