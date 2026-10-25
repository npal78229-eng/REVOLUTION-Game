// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "InteractableInterface.h"
#include "HidingSpotActor.generated.h"

class UStaticMeshComponent;
class USceneComponent;
class ARevolutionCharacter;
class USoundBase;

/**
 * Environmental Stealth Concealment Spot (Jute Sack Stacks / Deorhi Alcove / Shadow Niche)
 * Allows 12-year-old scout Kabir to hide completely from colonial curfew patrols.
 * While inside, Kabir is 100% concealed from watchman perception cones and acoustic hearing.
 */
UCLASS()
class REVOLUTION_API AHidingSpotActor : public AActor, public IInteractableInterface
{
	GENERATED_BODY()

public:
	AHidingSpotActor();

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* SceneRoot;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* CoverMesh;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* HidingPoint;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* ExitPoint;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Concealment")
	FText SpotName = FText::FromString(TEXT("Jute Ration Sacks Cover"));

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Concealment")
	FText ConcealPrompt = FText::FromString(TEXT("Conceal in Shadows"));

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Concealment")
	FText ExitPrompt = FText::FromString(TEXT("Exit Cover"));

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Concealment")
	bool bIsOccupied = false;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Concealment")
	ARevolutionCharacter* Occupant = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* ClothRustleSound = nullptr;

	// IInteractableInterface Implementation
	virtual void OnInteract_Implementation(ARevolutionCharacter* Interactor) override;
	virtual FText GetInteractionPrompt_Implementation() const override;
	virtual bool CanInteract_Implementation(const ARevolutionCharacter* Interactor) const override;

	void EjectOccupant();
};
