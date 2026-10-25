// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "InteractableInterface.h"
#include "CurfewGongActor.generated.h"

class UStaticMeshComponent;
class USoundBase;
class ARevolutionCharacter;

/**
 * Historical Municipal Curfew Bell / Gong (Chaukidar Curfew Ghanta)
 * Suspended above the outer deorhi gateway arch in Kot Gurdarshan, April 1919.
 * Historical Context & Gameplay Mechanics:
 * - Struck by colonial constables to toll the Section 144 night curfew (8:00 PM to 5:00 AM).
 * - Kabir can reach the elevated gateway platform and strike the gong with the hanging iron striker [E].
 * - Emits a deep, resonating acoustic toll that reverberates across the town (35m radius).
 * - Triggers an emergency sector-wide diversion: pulls all ACurfewPatrolAI watchmen toward the
 *   outer gateway arch, clearing the interior haveli alleys and rooftops for safe infiltration.
 */
UCLASS()
class REVOLUTION_API ACurfewGongActor : public AActor, public IInteractableInterface
{
	GENERATED_BODY()

public:
	ACurfewGongActor();

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* SceneRoot;

	/** Heavy timber gallows / suspension framework */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* TimberFrameMesh;

	/** Heavy cast-bronze circular gong disk */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* BronzeGongMesh;

	/** Wrought-iron striker mallet suspended on a leather cord */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* IronStrikerMesh;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Lore")
	FText GongTitle;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Lore", meta = (MultiLine = true))
	FText GongLore;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* GongTollSound = nullptr;

	/** Sector-wide audible range in cm (35 meters) */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Stealth")
	float SectorAlertRadius = 3500.0f;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|State")
	bool bHasBeenStruck = false;

	/** Strikes the municipal curfew gong, triggering a town-wide patrol diversion */
	UFUNCTION(BlueprintCallable, Category = "Revolution|Stealth")
	void StrikeGong(ARevolutionCharacter* Kabir);

	// IInteractableInterface Implementation
	virtual void OnInteract_Implementation(ARevolutionCharacter* Interactor) override;
	virtual FText GetInteractionPrompt_Implementation() const override;
	virtual bool CanInteract_Implementation(const ARevolutionCharacter* Interactor) const override;

protected:
	virtual void BeginPlay() override;
};
