// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "CommunityTrustTypes.h"
#include "CommunityTrustSubsystem.generated.h"

class ADoorDeorhiActor;
class ACivilianNPCActor;
class URevolutionSaveGame;

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnCommunityStanceChanged, FName, ClusterID, ECommunityStance, NewStance);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnCommunityIncidentLogged, FName, ClusterID, FName, IncidentTag, int32, TrustDelta);

/**
 * World Subsystem managing localized community trust clusters ("Izzat & Vishwas") across 1919 Punjab.
 * Features:
 * - Localized cluster partitioning (e.g., Canal Basti, Kot Gurdarshan Bazaar, Bhatta Kiln)
 * - Incident perception logging and trust delta tracking
 * - Automatic coordination with registered ADoorDeorhiActor (barring/unbarring kundi bolts)
 * - Automatic stance synchronization with ACivilianNPCActor dialogue barks
 * - Persistence integration with URevolutionSaveGame
 * - Passive tension cooldown timer (recovering from Compromised to Cautious over peaceful duration)
 */
UCLASS()
class REVOLUTION_API UCommunityTrustSubsystem : public UWorldSubsystem
{
	GENERATED_BODY()

public:
	UCommunityTrustSubsystem();

	virtual void Initialize(FSubsystemCollectionBase& Collection) override;
	virtual void Deinitialize() override;

	// --- CLUSTER QUERIES & MODIFIERS ---

	/** Returns current stance of a cluster */
	UFUNCTION(BlueprintPure, Category = "Revolution|CommunityTrust")
	ECommunityStance GetClusterStance(FName ClusterID) const;

	/** Returns current numerical trust score (0-100) */
	UFUNCTION(BlueprintPure, Category = "Revolution|CommunityTrust")
	int32 GetClusterScore(FName ClusterID) const;

	/** Resolves canonical cluster ID based on world coordinates */
	UFUNCTION(BlueprintPure, Category = "Revolution|CommunityTrust")
	FName GetClusterAtLocation(const FVector& Location) const;

	/** Directly sets a cluster stance */
	UFUNCTION(BlueprintCallable, Category = "Revolution|CommunityTrust")
	void SetClusterStance(FName ClusterID, ECommunityStance NewStance);

	/** Adjusts trust score with delta and updates stance accordingly */
	UFUNCTION(BlueprintCallable, Category = "Revolution|CommunityTrust")
	void AdjustClusterScore(FName ClusterID, int32 ScoreDelta, FName IncidentTag = NAME_None, AActor* Witness = nullptr);

	/** Records an incident witnessed by an NPC or sentry */
	UFUNCTION(BlueprintCallable, Category = "Revolution|CommunityTrust")
	void RecordIncident(FName ClusterID, FName IncidentTag, AActor* Instigator, AActor* Witness, int32 TrustDelta = -20);

	/** Returns full incident history for a given cluster */
	UFUNCTION(BlueprintCallable, Category = "Revolution|CommunityTrust")
	TArray<FCommunityIncidentRecord> GetIncidentHistory(FName ClusterID) const;

	/** Registers an interactive deorhi / canal door to react to cluster stance shifts */
	UFUNCTION(BlueprintCallable, Category = "Revolution|CommunityTrust")
	void RegisterClusterDoor(FName ClusterID, ADoorDeorhiActor* Door);

	/** Registers a civilian NPC to receive stance updates and deliver matching barks */
	UFUNCTION(BlueprintCallable, Category = "Revolution|CommunityTrust")
	void RegisterClusterCivilian(FName ClusterID, ACivilianNPCActor* Civilian);

	// --- SAVE / LOAD PERSISTENCE ---

	/** Restores cluster states from a loaded save game */
	UFUNCTION(BlueprintCallable, Category = "Revolution|CommunityTrust")
	void PopulateFromSaveGame(const URevolutionSaveGame* SaveGame);

	/** Writes current cluster states into save game */
	UFUNCTION(BlueprintCallable, Category = "Revolution|CommunityTrust")
	void WriteToSaveGame(URevolutionSaveGame* SaveGame) const;

	// --- RESTITUTION & RESET ---

	/** Resets cluster to default Neutral state */
	UFUNCTION(BlueprintCallable, Category = "Revolution|CommunityTrust")
	void ResetClusterToDefault(FName ClusterID);

	// --- DELEGATES ---

	UPROPERTY(BlueprintAssignable, Category = "Revolution|CommunityTrust")
	FOnCommunityStanceChanged OnStanceChanged;

	UPROPERTY(BlueprintAssignable, Category = "Revolution|CommunityTrust")
	FOnCommunityIncidentLogged OnIncidentLogged;

protected:
	/** Periodic evaluation of calm/peace cooldown */
	void EvaluateCooldownTimer();

private:
	/** Internal cluster registry */
	UPROPERTY()
	TMap<FName, FCommunityClusterState> ClusterStates;

	/** Weak references to cluster doors */
	TMap<FName, TArray<TWeakObjectPtr<ADoorDeorhiActor>>> RegisteredDoors;

	/** Weak references to cluster civilians */
	TMap<FName, TArray<TWeakObjectPtr<ACivilianNPCActor>>> RegisteredCivilians;

	/** Cooldown timer handle */
	FTimerHandle CooldownTimerHandle;

	/** Updates stance enum based on numerical score */
	ECommunityStance CalculateStanceFromScore(int32 Score) const;

	/** Broadcasts stance updates to registered doors and NPCs */
	void PropagateStanceToWorld(FName ClusterID, ECommunityStance Stance);
};
