// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "InteractableInterface.h"
#include "TelegraphWireActor.generated.h"

class UStaticMeshComponent;
class USoundBase;
class ARevolutionCharacter;

/**
 * Historical British Indian Telegraph Pole & Copper Line Sabotage Post
 * Mounted along haveli rooftop terraces in Kot Gurdarshan, April 1919.
 * Historical Context & Gameplay Mechanics:
 * - The colonial administration relied on overhead military telegraph lines to coordinate
 *   railway troop movements and dispatch arrest orders from the Lahore Cantonment.
 * - During the April 1919 Rowlatt Hartals, nationalist couriers systematically cut these wires (Taar Katna).
 * - Kabir can climb to the rooftop utility cross-arm and snip the copper wire using tailor shears [E].
 * - Cutting the wire isolates the local police post from imperial reinforcements and completes
 *   a major tactical milestone in Kabir's field journal.
 */
UCLASS()
class REVOLUTION_API ATelegraphWireActor : public AActor, public IInteractableInterface
{
	GENERATED_BODY()

public:
	ATelegraphWireActor();

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* SceneRoot;

	/** Weathered timber utility post */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* UtilityPoleMesh;

	/** Horizontal wooden insulator crossarm */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* CrossarmMesh;

	/** Left porcelain bell insulator */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* InsulatorLeftMesh;

	/** Right porcelain bell insulator */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* InsulatorRightMesh;

	/** Active taut copper military telegraph wire */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* TelegraphWireMesh;

	/** Severed loose hanging wire coil (visible once cut) */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* SeveredWireMesh;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|State")
	bool bIsWireCut = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* WireCutSound = nullptr;

	/** Snips the imperial military telegraph wire */
	UFUNCTION(BlueprintCallable, Category = "Revolution|Stealth")
	void CutTelegraphLine(ARevolutionCharacter* Kabir);

	// IInteractableInterface Implementation
	virtual void OnInteract_Implementation(ARevolutionCharacter* Interactor) override;
	virtual FText GetInteractionPrompt_Implementation() const override;
	virtual bool CanInteract_Implementation(const ARevolutionCharacter* Interactor) const override;

protected:
	virtual void BeginPlay() override;
};
