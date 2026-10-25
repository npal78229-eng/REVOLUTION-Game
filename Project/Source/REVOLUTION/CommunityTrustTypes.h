// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "CommunityTrustTypes.generated.h"

/**
 * Discrete behavioral stance of a localized community cluster towards Kabir
 * Inspired by the cultural principles of 'Izzat' (dignity/honor) and 'Vishwas' (trust) in 1919 Punjab.
 */
UENUM(BlueprintType)
enum class ECommunityStance : uint8
{
	Neutral UMETA(DisplayName = "Neutral (Observant)"),
	Cautious UMETA(DisplayName = "Cautious (Guarded)"),
	Trusted UMETA(DisplayName = "Trusted (Vishwas / Sheltering)"),
	Compromised UMETA(DisplayName = "Compromised (Barred / Hostile Rejection)")
};

/**
 * Record of an observed disturbance or restorative act within a community cluster
 */
USTRUCT(BlueprintType)
struct FCommunityIncidentRecord
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|CommunityTrust")
	FName IncidentTag = NAME_None;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|CommunityTrust")
	float Timestamp = 0.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|CommunityTrust")
	FName ClusterID = NAME_None;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|CommunityTrust")
	FString WitnessActorName;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|CommunityTrust")
	int32 TrustDelta = 0;
};

/**
 * Persistent state of a geographical community cluster
 */
USTRUCT(BlueprintType)
struct FCommunityClusterState
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|CommunityTrust")
	FName ClusterID = NAME_None;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|CommunityTrust")
	ECommunityStance Stance = ECommunityStance::Neutral;

	/** Numerical trust score: 0 to 100.
	 * 0-25: Compromised
	 * 26-45: Cautious
	 * 46-75: Neutral
	 * 76-100: Trusted
	 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|CommunityTrust")
	int32 NumericalTrustScore = 50;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|CommunityTrust")
	float LastIncidentTime = -1000.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|CommunityTrust")
	TArray<FCommunityIncidentRecord> IncidentHistory;
};
