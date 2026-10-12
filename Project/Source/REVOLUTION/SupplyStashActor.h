// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "InteractableInterface.h"
#include "SupplyStashActor.generated.h"

class UStaticMeshComponent;
class USoundBase;
class ARevolutionCharacter;

UENUM(BlueprintType)
enum class ESupplyStashType : uint8
{
	Pebbles UMETA(DisplayName = "Clay Marbles & River Pebbles"),
	Chalk UMETA(DisplayName = "Tailor's Chalk Slabs (Kharri Mitti)"),
	Pamphlets UMETA(DisplayName = "Anti-Rowlatt Strike Handbills (Satyagraha)")
};

/**
 * Historical Mohalla Equipment Supply Stash
 * Tactile scavenger caches scattered across haveli courtyards and terraces.
 * Enables 12-year-old Kabir to replenish clay marbles and tailor's chalk during curfew infiltration.
 */
UCLASS()
class REVOLUTION_API ASupplyStashActor : public AActor, public IInteractableInterface
{
	GENERATED_BODY()

public:
	ASupplyStashActor();

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* SceneRoot;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* StashMesh;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Supply")
	ESupplyStashType StashType = ESupplyStashType::Pebbles;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Supply")
	int32 ReplenishAmount = 2;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Supply")
	FText StashTitle = FText::FromString(TEXT("Clay Marble Stash"));

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Supply", meta = (MultiLine = true))
	FText LoreDescription = FText::FromString(TEXT("Smooth earthen marbles and river stones gathered along canal distributaries. Used by young scouts to lure night watchmen through acoustic decoys."));

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Supply")
	bool bIsCollected = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* PickupSound = nullptr;

	// IInteractableInterface Implementation
	virtual void OnInteract_Implementation(ARevolutionCharacter* Interactor) override;
	virtual FText GetInteractionPrompt_Implementation() const override;
	virtual bool CanInteract_Implementation(const ARevolutionCharacter* Interactor) const override;

protected:
	virtual void BeginPlay() override;
};
