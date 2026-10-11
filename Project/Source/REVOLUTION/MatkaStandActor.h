// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "InteractableInterface.h"
#include "MatkaStandActor.generated.h"

class UStaticMeshComponent;
class USoundBase;
class ARevolutionCharacter;

/**
 * Historical Earthen Water Pot Stand (Matka / Ghara Stand)
 * Traditional Punjabi courtyard drinking station in Kot Gurdarshan, April 1919.
 * Tactile Gameplay Mechanics:
 * - Large porous clay pots filled with cool well-water steeped with fragrant vetiver root (khus).
 * - Drinking from the brass ladle [E] instantly replenishes Kabir's stamina to 100% and quenches exertion.
 * - Kabir can tip the brass ladle into the pot to create a rhythmic water splash decoy,
 *   diverting curfew watchmen to investigate the courtyard water station.
 */
UCLASS()
class REVOLUTION_API AMatkaStandActor : public AActor, public IInteractableInterface
{
	GENERATED_BODY()

public:
	AMatkaStandActor();

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* SceneRoot;

	/** Carved teak tripod stand holding the clay pot */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* TripodStandMesh;

	/** Porous terracotta water pot (Ghara / Matka) */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* ClayMatkaMesh;

	/** Brass drinking ladle with long handle (Katori / Chamach) */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* BrassLadleMesh;

	/** Cool well-water surface inside the pot */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* WaterSurfaceMesh;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Lore")
	FText StandTitle;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Lore", meta = (MultiLine = true))
	FText StandLore;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* DrinkSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* WaterSplashSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Stealth")
	float DecoyAlertRadius = 850.0f;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|State")
	bool bHasDrunkRecently = false;

	/** Drinks cool well water, restoring Kabir's stamina to maximum */
	UFUNCTION(BlueprintCallable, Category = "Revolution|Interaction")
	void DrinkWater(ARevolutionCharacter* Kabir);

	/** Splashes water with the ladle to create an acoustic distraction */
	UFUNCTION(BlueprintCallable, Category = "Revolution|Stealth")
	void TriggerWaterDecoy();

	// IInteractableInterface Implementation
	virtual void OnInteract_Implementation(ARevolutionCharacter* Interactor) override;
	virtual FText GetInteractionPrompt_Implementation() const override;
	virtual bool CanInteract_Implementation(const ARevolutionCharacter* Interactor) const override;

protected:
	virtual void BeginPlay() override;
};
