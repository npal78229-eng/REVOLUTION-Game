// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "InteractableInterface.h"
#include "ProclamationBoardActor.generated.h"

class UStaticMeshComponent;
class USoundBase;
class ARevolutionCharacter;

/**
 * Historical British Imperial Curfew Proclamation Board (Section 144 Edict)
 * Posted on haveli deorhi entrance walls in April 1919 Kot Gurdarshan.
 * Tactical Resistance Mechanics:
 * - Kabir can read [E] the colonial martial decree issued by the District Magistrate.
 * - If carrying tailor's chalk, Kabir can deface the edict with a resistance strike mark,
 *   provoking colonial watchmen who pause in shock to examine the defaced imperial decree.
 */
UCLASS()
class REVOLUTION_API AProclamationBoardActor : public AActor, public IInteractableInterface
{
	GENERATED_BODY()

public:
	AProclamationBoardActor();

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* SceneRoot;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* BoardFrameMesh;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* ParchmentNoticeMesh;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* ChalkDefaceMesh;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Lore")
	FText ProclamationTitle;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Lore", meta = (MultiLine = true))
	FText ProclamationBody;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Resistance")
	bool bIsDefaced = false;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Resistance")
	bool bHasBeenInvestigatedByWatchman = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* ChalkDefaceSound = nullptr;

	/** Defaces the imperial notice with tailor's chalk */
	UFUNCTION(BlueprintCallable, Category = "Revolution|Resistance")
	void DefaceNoticeWithChalk(ARevolutionCharacter* Kabir);

	// IInteractableInterface Implementation
	virtual void OnInteract_Implementation(ARevolutionCharacter* Interactor) override;
	virtual FText GetInteractionPrompt_Implementation() const override;
	virtual bool CanInteract_Implementation(const ARevolutionCharacter* Interactor) const override;

protected:
	virtual void BeginPlay() override;
};
