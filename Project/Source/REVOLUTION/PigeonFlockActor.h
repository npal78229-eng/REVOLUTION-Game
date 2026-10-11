// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "PigeonFlockActor.generated.h"

class USceneComponent;
class UStaticMeshComponent;
class USoundBase;
class ARevolutionCharacter;

/**
 * Historical Haveli Rooftop Pigeon Flock (Kabootar)
 * Roosts along haveli brick parapets and cornices.
 * - Gentle ambient cooing when undisturbed.
 * - Startles into an explosive panic flight if Kabir sprints or approaches without crouching.
 * - Can be startled intentionally with clay marble pebbles to create acoustic diversions.
 * - Startled flock generates an acoustic disturbance alerting curfew patrol watchmen below.
 */
UCLASS()
class REVOLUTION_API APigeonFlockActor : public AActor
{
	GENERATED_BODY()

public:
	APigeonFlockActor();

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

public:
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* SceneRoot;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	TArray<UStaticMeshComponent*> BirdMeshes;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Stealth")
	float SprintSpookRadius = 300.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Stealth")
	float WalkSpookRadius = 180.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Stealth")
	float CrouchSpookRadius = 75.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Stealth")
	float AudibleAlertRadius = 1800.0f;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Stealth")
	bool bIsScatterTriggered = false;

	// Audio Assets
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* ScatterSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* CalmCooSound = nullptr;

	/** Manually or acoustically trigger the flock to take flight */
	UFUNCTION(BlueprintCallable, Category = "Revolution|Stealth")
	void TriggerScatterFlock();

	UFUNCTION(BlueprintPure, Category = "Revolution|Stealth")
	bool HasScattered() const { return bIsScatterTriggered; }

private:
	float CooTimer = 0.0f;
	float NextCooInterval = 12.0f;
	float ScatterFlightTimer = 0.0f;
	const float FlightDuration = 2.6f;

	TArray<FVector> BirdInitialOffsets;
	TArray<FVector> BirdFlightVelocities;
};
