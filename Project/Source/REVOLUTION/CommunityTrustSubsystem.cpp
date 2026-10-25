// Copyright Epic Games, Inc. All Rights Reserved.

#include "CommunityTrustSubsystem.h"
#include "DoorDeorhiActor.h"
#include "CivilianNPCActor.h"
#include "RevolutionSaveGame.h"
#include "TimerManager.h"
#include "Engine/World.h"

UCommunityTrustSubsystem::UCommunityTrustSubsystem()
{
	// Default canonical clusters for 1919 Punjab
	static const FName DefaultClusters[] = {
		FName(TEXT("Cluster_UBDC_CanalBasti")),
		FName(TEXT("Cluster_KotGurdarshan_Bazaar")),
		FName(TEXT("Cluster_Bhatta_BrickKiln"))
	};

	for (const FName& ClusterID : DefaultClusters)
	{
		FCommunityClusterState State;
		State.ClusterID = ClusterID;
		State.Stance = ECommunityStance::Neutral;
		State.NumericalTrustScore = 50;
		State.LastIncidentTime = -1000.0f;
		ClusterStates.Add(ClusterID, State);
	}
}

void UCommunityTrustSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
	Super::Initialize(Collection);

	if (UWorld* World = GetWorld())
	{
		World->GetTimerManager().SetTimer(
			CooldownTimerHandle,
			this,
			&UCommunityTrustSubsystem::EvaluateCooldownTimer,
			5.0f,
			true
		);
	}

	UE_LOG(LogTemp, Log, TEXT("UCommunityTrustSubsystem initialized with %d clusters."), ClusterStates.Num());
}

void UCommunityTrustSubsystem::Deinitialize()
{
	if (UWorld* World = GetWorld())
	{
		World->GetTimerManager().ClearTimer(CooldownTimerHandle);
	}

	ClusterStates.Empty();
	RegisteredDoors.Empty();
	RegisteredCivilians.Empty();

	Super::Deinitialize();
}

ECommunityStance UCommunityTrustSubsystem::GetClusterStance(FName ClusterID) const
{
	if (const FCommunityClusterState* Found = ClusterStates.Find(ClusterID))
	{
		return Found->Stance;
	}
	return ECommunityStance::Neutral;
}

int32 UCommunityTrustSubsystem::GetClusterScore(FName ClusterID) const
{
	if (const FCommunityClusterState* Found = ClusterStates.Find(ClusterID))
	{
		return Found->NumericalTrustScore;
	}
	return 50;
}

FName UCommunityTrustSubsystem::GetClusterAtLocation(const FVector& Location) const
{
	// Canal Basti (Zone F / Act IV Outskirts)
	if (Location.X < -500.0f && Location.Y <= 2400.0f)
	{
		return FName(TEXT("Cluster_UBDC_CanalBasti"));
	}
	// Brick Kiln (Zone G / Act IV Climax)
	if (Location.X < -500.0f && Location.Y > 2400.0f)
	{
		return FName(TEXT("Cluster_Bhatta_BrickKiln"));
	}
	// Default to Walled City / Kot Gurdarshan Bazaar
	return FName(TEXT("Cluster_KotGurdarshan_Bazaar"));
}

void UCommunityTrustSubsystem::SetClusterStance(FName ClusterID, ECommunityStance NewStance)
{
	FCommunityClusterState& State = ClusterStates.FindOrAdd(ClusterID);
	State.ClusterID = ClusterID;
	
	if (State.Stance != NewStance)
	{
		State.Stance = NewStance;
		
		// Align numerical score with direct stance override
		switch (NewStance)
		{
		case ECommunityStance::Compromised: State.NumericalTrustScore = 15; break;
		case ECommunityStance::Cautious:    State.NumericalTrustScore = 35; break;
		case ECommunityStance::Neutral:     State.NumericalTrustScore = 50; break;
		case ECommunityStance::Trusted:     State.NumericalTrustScore = 85; break;
		}

		PropagateStanceToWorld(ClusterID, NewStance);
		OnStanceChanged.Broadcast(ClusterID, NewStance);
	}
}

void UCommunityTrustSubsystem::AdjustClusterScore(FName ClusterID, int32 ScoreDelta, FName IncidentTag, AActor* Witness)
{
	FCommunityClusterState& State = ClusterStates.FindOrAdd(ClusterID);
	State.ClusterID = ClusterID;
	
	const int32 OldScore = State.NumericalTrustScore;
	State.NumericalTrustScore = FMath::Clamp(OldScore + ScoreDelta, 0, 100);

	if (UWorld* World = GetWorld())
	{
		State.LastIncidentTime = World->GetTimeSeconds();
	}

	const ECommunityStance NewStance = CalculateStanceFromScore(State.NumericalTrustScore);
	if (NewStance != State.Stance)
	{
		State.Stance = NewStance;
		PropagateStanceToWorld(ClusterID, NewStance);
		OnStanceChanged.Broadcast(ClusterID, NewStance);
	}
}

void UCommunityTrustSubsystem::RecordIncident(FName ClusterID, FName IncidentTag, AActor* Instigator, AActor* Witness, int32 TrustDelta)
{
	FCommunityClusterState& State = ClusterStates.FindOrAdd(ClusterID);
	State.ClusterID = ClusterID;

	FCommunityIncidentRecord Record;
	Record.IncidentTag = IncidentTag;
	Record.ClusterID = ClusterID;
	Record.Timestamp = GetWorld() ? GetWorld()->GetTimeSeconds() : 0.0f;
	Record.WitnessActorName = Witness ? Witness->GetName() : TEXT("Unseen");
	Record.TrustDelta = TrustDelta;

	State.IncidentHistory.Add(Record);

	AdjustClusterScore(ClusterID, TrustDelta, IncidentTag, Witness);
	OnIncidentLogged.Broadcast(ClusterID, IncidentTag, TrustDelta);

	UE_LOG(LogTemp, Warning, TEXT("[CommunityTrust] Incident '%s' in '%s' (Delta: %d). New Score: %d, Stance: %d"),
		*IncidentTag.ToString(), *ClusterID.ToString(), TrustDelta, State.NumericalTrustScore, (int32)State.Stance);
}

TArray<FCommunityIncidentRecord> UCommunityTrustSubsystem::GetIncidentHistory(FName ClusterID) const
{
	if (const FCommunityClusterState* Found = ClusterStates.Find(ClusterID))
	{
		return Found->IncidentHistory;
	}
	return TArray<FCommunityIncidentRecord>();
}

void UCommunityTrustSubsystem::RegisterClusterDoor(FName ClusterID, ADoorDeorhiActor* Door)
{
	if (!Door) return;

	TArray<TWeakObjectPtr<ADoorDeorhiActor>>& Doors = RegisteredDoors.FindOrAdd(ClusterID);
	if (!Doors.Contains(Door))
	{
		Doors.Add(Door);
	}

	// Immediately apply current stance to newly registered door
	const ECommunityStance CurrentStance = GetClusterStance(ClusterID);
	Door->ApplyCommunityStance(CurrentStance);
}

void UCommunityTrustSubsystem::RegisterClusterCivilian(FName ClusterID, ACivilianNPCActor* Civilian)
{
	if (!Civilian) return;

	TArray<TWeakObjectPtr<ACivilianNPCActor>>& Civilians = RegisteredCivilians.FindOrAdd(ClusterID);
	if (!Civilians.Contains(Civilian))
	{
		Civilians.Add(Civilian);
	}

	// Immediately apply current stance to newly registered civilian
	const ECommunityStance CurrentStance = GetClusterStance(ClusterID);
	Civilian->OnCommunityStanceChanged(ClusterID, CurrentStance);
}

void UCommunityTrustSubsystem::PopulateFromSaveGame(const URevolutionSaveGame* SaveGame)
{
	if (!SaveGame) return;

	for (const auto& Pair : SaveGame->CommunityStances)
	{
		const FName ClusterID = Pair.Key;
		const uint8 StanceVal = Pair.Value;
		const ECommunityStance Stance = static_cast<ECommunityStance>(FMath::Clamp<uint8>(StanceVal, 0, 3));

		FCommunityClusterState& State = ClusterStates.FindOrAdd(ClusterID);
		State.ClusterID = ClusterID;
		State.Stance = Stance;

		if (const int32* ScorePtr = SaveGame->CommunityTrustScores.Find(ClusterID))
		{
			State.NumericalTrustScore = *ScorePtr;
		}
		else
		{
			State.NumericalTrustScore = 50;
		}

		PropagateStanceToWorld(ClusterID, State.Stance);
	}
}

void UCommunityTrustSubsystem::WriteToSaveGame(URevolutionSaveGame* SaveGame) const
{
	if (!SaveGame) return;

	SaveGame->CommunityStances.Empty();
	SaveGame->CommunityTrustScores.Empty();

	for (const auto& Pair : ClusterStates)
	{
		SaveGame->CommunityStances.Add(Pair.Key, static_cast<uint8>(Pair.Value.Stance));
		SaveGame->CommunityTrustScores.Add(Pair.Key, Pair.Value.NumericalTrustScore);
	}
}

void UCommunityTrustSubsystem::ResetClusterToDefault(FName ClusterID)
{
	FCommunityClusterState& State = ClusterStates.FindOrAdd(ClusterID);
	State.ClusterID = ClusterID;
	State.Stance = ECommunityStance::Neutral;
	State.NumericalTrustScore = 50;
	State.LastIncidentTime = -1000.0f;
	State.IncidentHistory.Empty();

	PropagateStanceToWorld(ClusterID, ECommunityStance::Neutral);
	OnStanceChanged.Broadcast(ClusterID, ECommunityStance::Neutral);
}

ECommunityStance UCommunityTrustSubsystem::CalculateStanceFromScore(int32 Score) const
{
	if (Score <= 25) return ECommunityStance::Compromised;
	if (Score <= 45) return ECommunityStance::Cautious;
	if (Score <= 75) return ECommunityStance::Neutral;
	return ECommunityStance::Trusted;
}

void UCommunityTrustSubsystem::PropagateStanceToWorld(FName ClusterID, ECommunityStance Stance)
{
	// Update registered doors
	if (TArray<TWeakObjectPtr<ADoorDeorhiActor>>* DoorList = RegisteredDoors.Find(ClusterID))
	{
		for (int32 i = DoorList->Num() - 1; i >= 0; --i)
		{
			if ((*DoorList)[i].IsValid())
			{
				(*DoorList)[i]->ApplyCommunityStance(Stance);
			}
			else
			{
				DoorList->RemoveAt(i);
			}
		}
	}

	// Update registered civilians
	if (TArray<TWeakObjectPtr<ACivilianNPCActor>>* CivList = RegisteredCivilians.Find(ClusterID))
	{
		for (int32 i = CivList->Num() - 1; i >= 0; --i)
		{
			if ((*CivList)[i].IsValid())
			{
				(*CivList)[i]->OnCommunityStanceChanged(ClusterID, Stance);
			}
			else
			{
				CivList->RemoveAt(i);
			}
		}
	}
}

void UCommunityTrustSubsystem::EvaluateCooldownTimer()
{
	const float CurrentTime = GetWorld() ? GetWorld()->GetTimeSeconds() : 0.0f;

	for (auto& Pair : ClusterStates)
	{
		FCommunityClusterState& State = Pair.Value;

		// If at least 45 seconds have passed without incidents, tension gradually subsides towards Neutral (50)
		if (CurrentTime - State.LastIncidentTime >= 45.0f)
		{
			if (State.NumericalTrustScore < 50)
			{
				// Slowly cool down tension (+3 points per 5 seconds)
				State.NumericalTrustScore = FMath::Min(50, State.NumericalTrustScore + 3);
				const ECommunityStance NewStance = CalculateStanceFromScore(State.NumericalTrustScore);

				if (NewStance != State.Stance)
				{
					State.Stance = NewStance;
					PropagateStanceToWorld(State.ClusterID, NewStance);
					OnStanceChanged.Broadcast(State.ClusterID, NewStance);
				}
			}
		}
	}
}
