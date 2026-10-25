// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "InteractableInterface.h"
#include "CommunityTrustTypes.h"
#include "DoorDeorhiActor.generated.h"

class UStaticMeshComponent;
class USceneComponent;
class ARevolutionCharacter;
class ACurfewPatrolAI;
class USoundBase;

/**
 * Interactive 1919 Haveli Deorhi Gateway Door with Wrought-Iron Slide-Bolt (Kundi)
 * Allows Kabir to:
 * - Slide iron bolt (unbolt/bolt)
 * - Push heavy teak door open with wooden hinge creak
 * - Slam and bolt the door behind him while pursued to barricade against colonial watchmen
 * - AI watchman pounds on bolted door with bamboo lathi, creating distraction & delay
 */
UCLASS()
class REVOLUTION_API ADoorDeorhiActor : public AActor, public IInteractableInterface
{
	GENERATED_BODY()

public:
	ADoorDeorhiActor();

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

public:
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* SceneRoot;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* DoorHinge;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* DoorMesh;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* FrameMesh;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Door")
	bool bIsBolted = true;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Door")
	bool bIsOpen = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Door")
	float MaxOpenAngle = 105.0f; // degrees

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Door")
	float SwingSpeed = 160.0f; // degrees per second

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Door")
	FText DoorName = FText::FromString(TEXT("Aged Teak Deorhi Gateway"));

	// Audio assets
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* LatchSlideSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* DoorCreakSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* DoorSlamSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* LathiBangSound = nullptr;

	// IInteractableInterface
	virtual void OnInteract_Implementation(ARevolutionCharacter* Interactor) override;
	virtual FText GetInteractionPrompt_Implementation() const override;
	virtual bool CanInteract_Implementation(const ARevolutionCharacter* Interactor) const override;

	/** Returns true if the given location is on the interior courtyard side where the bolt kundi is mounted */
	UFUNCTION(BlueprintPure, Category = "Revolution|Door")
	bool IsOnInteriorLatchSide(const FVector& Location) const;

	/** Toggle open / close state */
	UFUNCTION(BlueprintCallable, Category = "Revolution|Door")
	void SetDoorOpen(bool bOpen);

	/** Toggle bolt lock state */
	UFUNCTION(BlueprintCallable, Category = "Revolution|Door")
	void SetBolted(bool bBolted);

	/** Triggered when an AI watchman pursues player to this closed bolted door */
	UFUNCTION(BlueprintCallable, Category = "Revolution|Door")
	void WatchmanBangOnDoor(ACurfewPatrolAI* Watchman);

	UFUNCTION(BlueprintPure, Category = "Revolution|Door")
	bool IsDoorBolted() const { return bIsBolted; }

	UFUNCTION(BlueprintPure, Category = "Revolution|Door")
	bool IsDoorOpen() const { return bIsOpen; }

	// --- COMMUNITY TRUST INTEGRATION ---
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|CommunityTrust")
	FName CommunityClusterID = FName(TEXT("Cluster_UBDC_CanalBasti"));

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|CommunityTrust")
	bool bLockWhenCompromised = true;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|CommunityTrust")
	bool bUnlockWhenTrusted = true;

	UFUNCTION(BlueprintCallable, Category = "Revolution|CommunityTrust")
	void ApplyCommunityStance(ECommunityStance Stance);

private:
	float CurrentYaw = 0.0f;
	float TargetYaw = 0.0f;
	bool bIsSwinging = false;
	float LastBangTime = -10.0f;
};
