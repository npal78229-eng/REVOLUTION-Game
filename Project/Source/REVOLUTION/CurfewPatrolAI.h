// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "CurfewPatrolAI.generated.h"

class UPointLightComponent;
class USpotLightComponent;
class UStaticMeshComponent;
class ARevolutionCharacter;
class USoundBase;

UENUM(BlueprintType)
enum class ECurfewAlertState : uint8
{
	Unaware UMETA(DisplayName = "Unaware (Patrolling)"),
	Suspicious UMETA(DisplayName = "Suspicious (Investigating)"),
	Searching UMETA(DisplayName = "Searching (Alerted Area)"),
	Alerted UMETA(DisplayName = "Alerted (Curfew Challenge)")
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnWatchmanAlertChanged, ECurfewAlertState, NewState, float, DetectionPercentage);

/**
 * Historical British-Era Watchman (Chaukidar / Colonial Constable)
 * Patrols the streets of Kot Gurdarshan during 1919 martial curfew with a hurricane lantern.
 * Features:
 * - Line-of-sight cone perception with obstruction check (broken by 1.1m rooftop parapet / walls)
 * - Dynamic detection meter based on Kabir's stance (crouched in shadow vs standing vs sprinting)
 * - Warm 3200K kerosene lantern with real-time dynamic lighting
 * - Multi-waypoint patrol routine with search pauses
 * - Curfew confrontation and alert signaling
 */
UCLASS()
class REVOLUTION_API ACurfewPatrolAI : public ACharacter
{
	GENERATED_BODY()

public:
	ACurfewPatrolAI();

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

public:
	// --- PATROL CONFIGURATION ---
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Patrol")
	TArray<FVector> PatrolWaypoints;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Patrol")
	float PatrolWalkSpeed = 160.0f; // Slow, deliberate night patrol

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Patrol")
	float AlertChaseSpeed = 360.0f; // Brisk curfew pursuit

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Patrol")
	float WaypointAcceptanceRadius = 80.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Patrol")
	float WaypointWaitDuration = 3.0f; // Seconds to look around at each corner

	// --- PERCEPTION & CONCEALMENT PARAMETERS ---
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Perception")
	float SightRadius = 1400.0f; // 14 meters vision range

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Perception")
	float PeripheralVisionAngle = 80.0f; // Half-angle FOV cone (total 160 degrees)

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Perception")
	float HearingRadius = 850.0f; // Audible detection for sprinting steps

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Perception")
	float DetectionMeter = 0.0f; // 0.0 to 100.0

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Perception")
	float DetectionFillRate = 45.0f; // Per second when clearly visible

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Perception")
	float SuspicionDecayRate = 18.0f; // Per second when Kabir breaks line of sight

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Perception")
	ECurfewAlertState AlertState = ECurfewAlertState::Unaware;

	UPROPERTY(BlueprintAssignable, Category = "Revolution|Perception")
	FOnWatchmanAlertChanged OnWatchmanAlertChanged;

	// --- COMPONENTS ---
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Components")
	UStaticMeshComponent* LanternMesh;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Components")
	UPointLightComponent* LanternLight;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Components")
	USpotLightComponent* LanternBeam;

	// --- AUDIO & VOICE LINES ---
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* WatchmanCalloutSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* WatchmanWhistleSound = nullptr;

	// --- LORE & DESIGNATION ---
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Dialogue")
	FText WatchmanTitle;

	UFUNCTION(BlueprintCallable, Category = "Revolution|Perception")
	bool CanSeePlayer(ARevolutionCharacter* TargetPlayer, float& OutPerceptionIntensity);

	UFUNCTION(BlueprintPure, Category = "Revolution|Perception")
	float GetDetectionPercentage() const { return DetectionMeter; }

	UFUNCTION(BlueprintPure, Category = "Revolution|Perception")
	ECurfewAlertState GetAlertState() const { return AlertState; }

	UFUNCTION(BlueprintPure, Category = "Revolution|Perception")
	FVector GetDirectionToPlayer(ARevolutionCharacter* TargetPlayer) const;

protected:
	void UpdatePatrol(float DeltaTime);
	void UpdateDetection(float DeltaTime);
	void SetAlertState(ECurfewAlertState NewState);

private:
	int32 CurrentWaypointIndex = 0;
	float WaypointWaitTimer = 0.0f;
	bool bIsWaitingAtWaypoint = false;
	FVector LastKnownPlayerLocation;
	float SearchTimer = 0.0f;
	float ScanLookTimer = 0.0f;
};
