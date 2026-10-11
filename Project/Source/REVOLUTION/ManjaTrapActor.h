// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "InteractableInterface.h"
#include "ManjaTrapActor.generated.h"

class UStaticMeshComponent;
class UBoxComponent;
class USoundBase;
class ARevolutionCharacter;

/**
 * Historical Basant Kite String Hazard (Glass-Coated Manja Line)
 * Strung between rooftop terrace parapets in Kot Gurdarshan, April 1919.
 * Tactile Stealth Dynamics:
 * - Walking upright or sprinting into the taut glass-coated string snags Kabir's vest,
 *   causing a sharp twang that alerts the curfew watchman patrolling below.
 * - Approaching while crouched allows Kabir to safely slip underneath.
 * - Kabir can carefully cut and collect the strong cotton twine [E], permanently disarming the hazard.
 */
UCLASS()
class REVOLUTION_API AManjaTrapActor : public AActor, public IInteractableInterface
{
	GENERATED_BODY()

public:
	AManjaTrapActor();

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* SceneRoot;

	/** Left anchor post / masonry finial */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* PostLeftMesh;

	/** Right anchor post / masonry finial */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* PostRightMesh;

	/** Taut glass-coated manja kite thread */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* StringLineMesh;

	/** Discarded wooden kite spool (Charkhi) lying near the post */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* SpoolMesh;

	/** Snag detection trigger box */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UBoxComponent* SnagTrigger;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|State")
	bool bIsDisarmed = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Detection")
	float AlertRadiusWatchman = 800.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* StringSnapSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* CollectTwineSound = nullptr;

	UFUNCTION()
	void OnOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);

	/** Carefully disarms and retrieves the glass-coated cord */
	UFUNCTION(BlueprintCallable, Category = "Revolution|Stealth")
	void DisarmTrap(ARevolutionCharacter* Kabir);

	// IInteractableInterface Implementation
	virtual void OnInteract_Implementation(ARevolutionCharacter* Interactor) override;
	virtual FText GetInteractionPrompt_Implementation() const override;
	virtual bool CanInteract_Implementation(const ARevolutionCharacter* Interactor) const override;

protected:
	virtual void BeginPlay() override;
};
