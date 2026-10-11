// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "InteractableInterface.h"
#include "CrawlSpaceActor.generated.h"

class USceneComponent;
class UStaticMeshComponent;
class ARevolutionCharacter;
class USoundBase;

/**
 * Historical Haveli Low Drain / Conduit Crawlway (Mori / Parnala Arch)
 * Allows 12-year-old scout Kabir (1.42m height) to crawl on hands and knees through
 * narrow drainage arches (<80cm height) through thick masonry walls.
 * Adult colonial watchmen (1.80m+) cannot fit, making this a vital asymmetric stealth route.
 */
UCLASS()
class REVOLUTION_API ACrawlSpaceActor : public AActor, public IInteractableInterface
{
	GENERATED_BODY()

public:
	ACrawlSpaceActor();

public:
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* SceneRoot;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* ConduitMesh;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* PointA; // Courtyard / Interior Threshold

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* PointB; // Street Alley / Exterior Threshold

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Traversal")
	float CrawlDuration = 1.6f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Traversal")
	FText DrainName = FText::FromString(TEXT("Haveli Storm-Drain Arch"));

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Traversal")
	FText CrawlPrompt = FText::FromString(TEXT("Squeeze Through Drain Conduit"));

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* ScrapeSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* EmergeSound = nullptr;

	// IInteractableInterface
	virtual void OnInteract_Implementation(ARevolutionCharacter* Interactor) override;
	virtual FText GetInteractionPrompt_Implementation() const override;
	virtual bool CanInteract_Implementation(const ARevolutionCharacter* Interactor) const override;

	/** Gets the opposite exit point relative to the interactor's position */
	void GetCrawlEndpoints(const FVector& InteractorLoc, FVector& OutStart, FVector& OutEnd) const;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Traversal")
	bool bIsTraversing = false;

	void FinishTraversal();
};
