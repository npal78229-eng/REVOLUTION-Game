// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "TerracottaHazardActor.generated.h"

class UBoxComponent;
class UStaticMeshComponent;
class USoundBase;
class ARevolutionCharacter;

/**
 * Brittle Terracotta Roof Shingles & Broken Earthen Pottery Hazard (Khaprail / Matka Chura)
 * Scattered across Punjabi haveli rooftops and alley corners.
 * Tactical Stealth Mechanics:
 * - Walking or sprinting upright crunches the brittle earthenware shards, generating an acoustic alert that summons curfew watchmen.
 * - Crouching allows 12-year-old Kabir to tread softly and pass in absolute silence without triggering an acoustic disturbance.
 */
UCLASS()
class REVOLUTION_API ATerracottaHazardActor : public AActor
{
	GENERATED_BODY()

public:
	ATerracottaHazardActor();

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* SceneRoot;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UBoxComponent* HazardTrigger;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* ShardClusterMesh;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Hazard")
	FText HazardName = FText::FromString(TEXT("Brittle Terracotta Shingles (Khaprail)"));

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Hazard")
	float AcousticAlertRadius = 750.0f; // 7.5 meters noise propagation

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Hazard")
	float CrunchCooldown = 1.6f; // Minimum seconds between sound alerts

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* ShardCrunchSound = nullptr;

	// --- COMMUNITY TRUST INTEGRATION ---
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|CommunityTrust")
	FName CommunityClusterID = FName(TEXT("Cluster_UBDC_CanalBasti"));

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|CommunityTrust")
	int32 TrustPenaltyOnCrunch = -15;

	UFUNCTION()
	void OnHazardOverlap(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

private:
	float LastCrunchTime = -10.0f;
	bool bPlayerIsInside = false;
	TWeakObjectPtr<ARevolutionCharacter> OverlappingPlayer;
};
