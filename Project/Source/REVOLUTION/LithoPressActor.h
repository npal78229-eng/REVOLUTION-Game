// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "InteractableInterface.h"
#include "LithoPressActor.generated.h"

class UStaticMeshComponent;
class USoundBase;
class ARevolutionCharacter;

/**
 * Historical Clandestine Lithographic Hand Press (Pathar di Chhapakhana)
 * Concealed in haveli cellar workshops and back rooms during the April 1919 martial curfew in Punjab.
 * Tactical Gameplay Mechanics:
 * - Origin of the anti-Rowlatt leaflets and general strike (Hartal) notices.
 * - Kabir can inspect the heavy Bavarian limestone flatbed press to study clandestine vernacular printmaking.
 * - Operating the iron roller and scraper crank yields fresh anti-Rowlatt handbills and replenishes
 *   tailor's chalk / marble supplies from the secret workshop cache.
 */
UCLASS()
class REVOLUTION_API ALithoPressActor : public AActor, public IInteractableInterface
{
	GENERATED_BODY()

public:
	ALithoPressActor();

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* SceneRoot;

	/** Heavy timber workbench plinth */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* TimberTableMesh;

	/** Polished Bavarian limestone lithography flatbed slab */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* LithoStoneMesh;

	/** Heavy cast-iron scraper and roller assembly */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* RollerAssemblyMesh;

	/** Ink grinding slate with brayer roller and oil ink pots */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* InkPaletteMesh;

	/** Stack of freshly inked anti-Rowlatt pamphlets drying on blotting paper */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* LeafletStackMesh;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Lore")
	FText PressTitle;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Lore", meta = (MultiLine = true))
	FText PressLore;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|State")
	bool bHasBeenOperated = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* PressOperateSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* LeafletRetrieveSound = nullptr;

	/** Pulls fresh strike handbills from the litho stone and replenishes courier supplies */
	UFUNCTION(BlueprintCallable, Category = "Revolution|Interaction")
	void OperatePress(ARevolutionCharacter* Kabir);

	// IInteractableInterface Implementation
	virtual void OnInteract_Implementation(ARevolutionCharacter* Interactor) override;
	virtual FText GetInteractionPrompt_Implementation() const override;
	virtual bool CanInteract_Implementation(const ARevolutionCharacter* Interactor) const override;

protected:
	virtual void BeginPlay() override;
};
