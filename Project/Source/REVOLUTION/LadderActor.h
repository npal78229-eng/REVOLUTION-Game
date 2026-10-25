// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "InteractableInterface.h"
#include "LadderActor.generated.h"

class USceneComponent;
class UStaticMeshComponent;
class UBoxComponent;
class ARevolutionCharacter;
class USoundBase;

/**
 * Historical Timber / Bamboo Makeshift Traversal Ladder
 * Connects the ground floor courtyard (Z = 0) to the Haveli first-floor terrace (Z = 400).
 * Implements IInteractableInterface for contextual climbing and descending.
 */
UCLASS()
class REVOLUTION_API ALadderActor : public AActor, public IInteractableInterface
{
	GENERATED_BODY()

public:
	ALadderActor();

protected:
	virtual void BeginPlay() override;

public:
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* SceneRoot;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* LadderMesh;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UBoxComponent* InteractionTrigger;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* BottomMountPoint;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* TopDismountPoint;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Traversal")
	float ClimbDuration = 1.8f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Traversal")
	FText LadderName = FText::FromString(TEXT("Haveli Courtyard Timber Ladder"));

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Traversal")
	FText AscendPrompt = FText::FromString(TEXT("Climb Timber Ladder to Terrace"));

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Traversal")
	FText DescendPrompt = FText::FromString(TEXT("Descend Ladder to Courtyard"));

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* ClimbSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* DismountSound = nullptr;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Traversal")
	bool bIsTraversing = false;

	// IInteractableInterface
	virtual void OnInteract_Implementation(ARevolutionCharacter* Interactor) override;
	virtual FText GetInteractionPrompt_Implementation() const override;
	virtual bool CanInteract_Implementation(const ARevolutionCharacter* Interactor) const override;

	/** Determines whether the given location is closer to bottom or top */
	UFUNCTION(BlueprintPure, Category = "Revolution|Traversal")
	bool IsCloserToBottom(const FVector& InteractorLoc) const;

	void FinishTraversal();
};
