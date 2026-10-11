// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "InteractableInterface.h"
#include "CheckpointBarrierActor.generated.h"

class UStaticMeshComponent;
class UPointLightComponent;
class USoundBase;
class ARevolutionCharacter;

/**
 * Historical Colonial Police Checkpoint Barricade (Naka Bandi)
 * Placed at the bazaar thoroughfare boundary in Kot Gurdarshan, April 1919.
 * Visual & Narrative Grounding:
 * - Wooden X-trestles with wire coils blocking the main road towards the railway junction.
 * - Crimson storm lantern (Lal Batti) signaling strict Section 144 martial lockdown.
 * - Reinforces the stealth puzzle: the streets are impassable, compelling Kabir to infiltrate
 *   via haveli rooftops, roshandan lightwells, and low drain crawlways.
 */
UCLASS()
class REVOLUTION_API ACheckpointBarrierActor : public AActor, public IInteractableInterface
{
	GENERATED_BODY()

public:
	ACheckpointBarrierActor();

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* SceneRoot;

	/** Heavy horizontal timber barricade beam */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* BarrierCrossbarMesh;

	/** Left diagonal support post */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* PostLeftMesh;

	/** Right diagonal support post */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* PostRightMesh;

	/** Barbed wire coil obstruction */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* WireMesh;

	/** Hanging red storm hurricane lantern */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* RedLanternMesh;

	/** Crimson warning point light */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UPointLightComponent* RedLanternLight;

	/** Imperial military warning plaque */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* WarningPlaqueMesh;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Lore")
	FText BarrierTitle;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Lore", meta = (MultiLine = true))
	FText BarrierLore;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* LanternCreakSound = nullptr;

	// IInteractableInterface Implementation
	virtual void OnInteract_Implementation(ARevolutionCharacter* Interactor) override;
	virtual FText GetInteractionPrompt_Implementation() const override;
	virtual bool CanInteract_Implementation(const ARevolutionCharacter* Interactor) const override;

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

private:
	float LightPulseTimer = 0.0f;
};
