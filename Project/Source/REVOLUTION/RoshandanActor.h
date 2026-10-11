// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "InteractableInterface.h"
#include "RoshandanActor.generated.h"

class UBoxComponent;
class UStaticMeshComponent;
class USoundBase;
class ARevolutionCharacter;

/**
 * Historical Haveli Rooftop Roshandan (Lightwell / Ventilation Shaft)
 * A framed opening in the rooftop terrace floor with iron lattice grates, looking down into the courtyard.
 * Tactical Stealth Gameplay:
 * - Kabir can look down to survey courtyard watchman movements from the safety of the roof.
 * - Interaction [E] allows dropping a clay marble down the shaft into the courtyard below.
 * - Produces an acoustic disturbance on the ground floor, luring watchmen into the courtyard
 *   without Kabir needing to descend from the rooftops.
 */
UCLASS()
class REVOLUTION_API ARoshandanActor : public AActor, public IInteractableInterface
{
	GENERATED_BODY()

public:
	ARoshandanActor();

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* SceneRoot;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UBoxComponent* InteractionBox;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* ShaftCurbMesh;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* IronGrilleMesh;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Roshandan")
	FText RoshandanName = FText::FromString(TEXT("Haveli Roshandan (Rooftop Lightwell)"));

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Roshandan")
	FVector DropTargetLocation = FVector(30.0f, 60.0f, 15.0f); // Courtyard floor target

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Roshandan")
	float AcousticAlertRadius = 850.0f; // 8.5m noise radius on courtyard floor

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Roshandan")
	float DropCooldown = 3.5f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* PebbleDropSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* GroundImpactSound = nullptr;

	// IInteractableInterface Implementation
	virtual void OnInteract_Implementation(ARevolutionCharacter* Interactor) override;
	virtual FText GetInteractionPrompt_Implementation() const override;
	virtual bool CanInteract_Implementation(const ARevolutionCharacter* Interactor) const override;

protected:
	virtual void BeginPlay() override;

private:
	float LastDropTime = -10.0f;
};
