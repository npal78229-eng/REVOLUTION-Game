// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "InteractableInterface.generated.h"

class ARevolutionCharacter;

UINTERFACE(MinimalAPI, Blueprintable)
class UInteractableInterface : public UInterface
{
	GENERATED_BODY()
};

class REVOLUTION_API IInteractableInterface
{
	GENERATED_BODY()

public:
	/** Called when Kabir triggers interaction on this actor */
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "Revolution|Interaction")
	void OnInteract(ARevolutionCharacter* Interactor);

	/** Returns contextual prompt text (e.g. "Inspect Newspaper", "Open Door") */
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "Revolution|Interaction")
	FText GetInteractionPrompt() const;

	/** Determines if actor can currently be interacted with */
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "Revolution|Interaction")
	bool CanInteract(const ARevolutionCharacter* Interactor) const;
};
