// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "InteractableInterface.h"
#include "ChaffDustDecoyActor.generated.h"

class UStaticMeshComponent;
class USphereComponent;
class USoundBase;
class ARevolutionCharacter;

/**
 * Historical Harvest Wheat Chaff & Winnowing Scoop Decoy (Bhoosa & Chhaj)
 * Placed in haveli courtyard storage corners in Kot Gurdarshan, April 1919.
 * Tactile Realism & Gameplay Mechanics:
 * - Following the spring Baisakhi rabi harvest, courtyards stored grain and finely crushed wheat chaff.
 * - Kabir can shake the winnowing scoop [E] or hit it with a clay marble to release a billowing
 *   chaff dust screen (2.8m radius) for 7.5 seconds.
 * - The particulate cloud completely breaks line-of-sight for ACurfewPatrolAI watchmen and induces
 *   a coughing pause if a watchman wanders into the cloud.
 */
UCLASS()
class REVOLUTION_API AChaffDustDecoyActor : public AActor, public IInteractableInterface
{
	GENERATED_BODY()

public:
	AChaffDustDecoyActor();

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* SceneRoot;

	/** Jute sack containing harvested wheat chaff */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* BurlapSackMesh;

	/** Woven bamboo/reed winnowing scoop (Chhaj) tilted against the wall */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* WinnowingScoopMesh;

	/** Billowing particulate chaff dust cloud volume */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* DustCloudMesh;

	/** Dust cloud obscuration radius sphere */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USphereComponent* DustSphere;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|State")
	bool bIsDischarged = false;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|State")
	bool bIsDustActive = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Parameters")
	float DustRadius = 280.0f; // 2.8m visual obscuration zone

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Parameters")
	float DustDuration = 7.5f; // Seconds before chaff settles on the ground

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* DustReleaseSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* WatchmanCoughSound = nullptr;

	/** Releases the wheat chaff particulate screen */
	UFUNCTION(BlueprintCallable, Category = "Revolution|Stealth")
	void TriggerChaffDust();

	UFUNCTION(BlueprintPure, Category = "Revolution|Stealth")
	bool IsDustCloudActive() const { return bIsDustActive; }

	// IInteractableInterface Implementation
	virtual void OnInteract_Implementation(ARevolutionCharacter* Interactor) override;
	virtual FText GetInteractionPrompt_Implementation() const override;
	virtual bool CanInteract_Implementation(const ARevolutionCharacter* Interactor) const override;

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

private:
	float DustTimer = 0.0f;
	float CloudScaleProgress = 0.0f;
};
