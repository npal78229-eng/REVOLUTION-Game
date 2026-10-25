// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "InteractableInterface.h"
#include "RestitutionDropActor.generated.h"

class USceneComponent;
class UStaticMeshComponent;
class USphereComponent;
class USoundBase;
class ARevolutionCharacter;

/**
 * Interactive Restitution Cache / Reparation Drop Point for Community Trust ("Izzat & Vishwas")
 * Allows Kabir to make amends after causing collateral disturbance (e.g. breaking pottery or alerting patrols).
 * Leaving 2 copper annas or replacement tools restores community standing, converting Compromised to Neutral/Trusted
 * and unbolting locked bypass deorhi gates.
 */
UCLASS()
class REVOLUTION_API ARestitutionDropActor : public AActor, public IInteractableInterface
{
	GENERATED_BODY()

public:
	ARestitutionDropActor();

protected:
	virtual void BeginPlay() override;

public:
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* SceneRoot;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* PropMesh;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USphereComponent* InteractionTrigger;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|CommunityTrust")
	FName CommunityClusterID = FName(TEXT("Cluster_UBDC_CanalBasti"));

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|CommunityTrust")
	int32 RestitutionTrustBonus = 35;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|CommunityTrust")
	bool bHasBeenPaid = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|CommunityTrust")
	FText RestitutionPrompt;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|CommunityTrust")
	FText PaidPrompt;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* PaymentSound;

	// IInteractableInterface
	virtual void OnInteract_Implementation(ARevolutionCharacter* Interactor) override;
	virtual FText GetInteractionPrompt_Implementation() const override;
	virtual bool CanInteract_Implementation(const ARevolutionCharacter* Interactor) const override;

	UFUNCTION(BlueprintCallable, Category = "Revolution|CommunityTrust")
	void ResetRestitution();
};
