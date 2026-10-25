// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "InteractableInterface.h"
#include "PariahDogActor.generated.h"

class UStaticMeshComponent;
class USphereComponent;
class USoundBase;
class ARevolutionCharacter;

UENUM(BlueprintType)
enum class EPariahDogState : uint8
{
	Sleeping UMETA(DisplayName = "Sleeping"),
	Disturbed UMETA(DisplayName = "Disturbed (Growling)"),
	Barking UMETA(DisplayName = "Barking (Alerting Watchmen)"),
	Distracted UMETA(DisplayName = "Distracted (Decoy)"),
	Pacified UMETA(DisplayName = "Pacified (Soothed)")
};

/**
 * Historical Mohalla Pariah Dog (Desi Kutta) Vigilance Decoy & Stealth Hazard
 * Resting in alleyway shadows of Kot Gurdarshan during 1919 curfew.
 * Tactile Stealth Dynamics:
 * - Upright walking within 2.5m or sprinting within 5.5m startles the dog into barking.
 * - Loud barking draws ACurfewPatrolAI watchmen directly to investigate the alleyway disturbance.
 * - Kabir can crouch-sneak past silently within 70cm without waking the sleeping dog.
 * - Throwing a clay marble/pebble nearby distracts the dog, turning its attention away.
 * - Kabir can approach crouched to softly soothe/shush [E] the dog into deep pacified sleep.
 */
UCLASS()
class REVOLUTION_API APariahDogActor : public AActor, public IInteractableInterface
{
	GENERATED_BODY()

public:
	APariahDogActor();

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* SceneRoot;

	/** Worn burlap rag / straw bedding in alley doorway */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* BeddingMatMesh;

	/** Sleeping curled dog torso */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* DogBodyMesh;

	/** Dog head and muzzle (animates/rotates when alert, barking, or distracted) */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* DogHeadMesh;

	/** Awareness trigger sphere */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USphereComponent* VigilanceSphere;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|State")
	EPariahDogState CurrentState = EPariahDogState::Sleeping;

	/** Radius in cm within which upright walking startles the dog */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Detection")
	float WalkAlertRadius = 250.0f;

	/** Radius in cm within which sprinting footsteps immediately wake the dog into barking */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Detection")
	float SprintAlertRadius = 550.0f;

	/** Radius in cm within which dog bark summons colonial patrol watchmen */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Detection")
	float WatchmanAlertRadius = 1400.0f;

	/** Radius in cm for clay marble distraction impact */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Detection")
	float PebbleHearingRadius = 500.0f;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|State")
	bool bIsPacified = false;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|State")
	bool bIsDistracted = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* BarkSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* GrowlSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* SootheSound = nullptr;

	/** Distracts dog with pebble impact */
	UFUNCTION(BlueprintCallable, Category = "Revolution|Stealth")
	void DistractWithPebble(const FVector& DecoyLocation);

	/** Softly soothes dog when approached while crouching */
	UFUNCTION(BlueprintCallable, Category = "Revolution|Stealth")
	void SootheDog(ARevolutionCharacter* Kabir);

	UFUNCTION(BlueprintPure, Category = "Revolution|State")
	EPariahDogState GetDogState() const { return CurrentState; }

	// IInteractableInterface Implementation
	virtual void OnInteract_Implementation(ARevolutionCharacter* Interactor) override;
	virtual FText GetInteractionPrompt_Implementation() const override;
	virtual bool CanInteract_Implementation(const ARevolutionCharacter* Interactor) const override;

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

	void TriggerBarkAlert();
	void AlertNearbyWatchmen();

private:
	float DisturbedTimer = 0.0f;
	float BarkTimer = 0.0f;
	float DistractionTimer = 0.0f;
	float BarkCooldownTimer = 0.0f;
	FVector DecoyTargetLocation;
};
