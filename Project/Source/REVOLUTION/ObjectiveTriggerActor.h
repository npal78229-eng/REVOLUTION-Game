// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "InteractableInterface.h"
#include "RevolutionMissionSubsystem.h"
#include "ObjectiveTriggerActor.generated.h"

class UStaticMeshComponent;
class ARevolutionCharacter;

/**
 * Interactive Courier Drop & Collection Point for Clandestine Missions
 * Implements IInteractableInterface to progress URevolutionMissionSubsystem.
 */
UCLASS()
class REVOLUTION_API AObjectiveTriggerActor : public AActor, public IInteractableInterface
{
	GENERATED_BODY()

public:
	AObjectiveTriggerActor();

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* SceneRoot;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* MeshComponent;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Mission")
	ECourierMissionStage RequiredMissionStage = ECourierMissionStage::Stage_RetrievePamphlets;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Mission")
	FText InteractionPrompt = FText::FromString(TEXT("Retrieve Leaflets"));

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Mission")
	FText ItemTitle = FText::FromString(TEXT("Anti-Rowlatt Pamphlet Dispatch"));

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Mission", meta = (MultiLine = true))
	FText HistoricalLoreUponInteraction = FText::FromString(TEXT("Underground lithographed bulletins calling for a town-wide Hartal (general shutdown) in protest against wartime emergency laws."));

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Mission")
	bool bHasBeenTriggered = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Mission")
	bool bHideMeshOnTrigger = false;

	// IInteractableInterface Implementation
	virtual void OnInteract_Implementation(ARevolutionCharacter* Interactor) override;
	virtual FText GetInteractionPrompt_Implementation() const override;
	virtual bool CanInteract_Implementation(const ARevolutionCharacter* Interactor) const override;
};
