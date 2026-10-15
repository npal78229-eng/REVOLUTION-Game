// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "InteractableInterface.h"
#include "LocomotiveSteamValveActor.generated.h"

class UStaticMeshComponent;
class USoundBase;
class ARevolutionCharacter;

/**
 * Historical British Broad-Gauge Steam Locomotive Boiler Valve
 * Allows Kabir to release high-pressure boiler steam, creating a blinding vapor cloud
 * that cloaks him from sentry line-of-sight and lures colonial pickets to investigate.
 * Synthesizes AAA benchmark mechanics from Hitman and Batman: Arkham.
 */
UCLASS()
class REVOLUTION_API ALocomotiveSteamValveActor : public AActor, public IInteractableInterface
{
	GENERATED_BODY()

public:
	ALocomotiveSteamValveActor();

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* SceneRoot;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* ValveMesh;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Lore")
	FText ValveTitle;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Lore", meta = (MultiLine = true))
	FText ValveLore;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* SteamHissSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Stealth")
	float SteamObscurityDuration = 14.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Stealth")
	float DistractionRadius = 2800.0f;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|State")
	bool bHasBeenVented = false;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|State")
	float VentCooldownTimer = 0.0f;

	// IInteractableInterface Implementation
	virtual void OnInteract_Implementation(ARevolutionCharacter* Interactor) override;
	virtual FText GetInteractionPrompt_Implementation() const override;
	virtual bool CanInteract_Implementation(const ARevolutionCharacter* Interactor) const override;

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;
};
