// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "RevolutionMissionSubsystem.h"
#include "RevolutionSaveGame.generated.h"

/**
 * Historical Game State Save Container for REVOLUTION
 * Serializes Kabir's narrative progress, clandestine inventory, checkpoint location,
 * discovered historical codex archival entries, and player audio/accessibility preferences.
 */
UCLASS()
class REVOLUTION_API URevolutionSaveGame : public USaveGame
{
	GENERATED_BODY()

public:
	URevolutionSaveGame();

	/** Target save slot identifier */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|SaveGame")
	FString SaveSlotName;

	/** User index for multi-user / platform split */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|SaveGame")
	int32 UserIndex;

	/** Real-world UTC timestamp when save was committed */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|SaveGame")
	FDateTime SaveTimestamp;

	// --- NARRATIVE PROGRESSION ---
	/** Active historical mission stage in Kabir's journey */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|SaveGame")
	ECourierMissionStage CurrentMissionStage;

	// --- PLAYER SPATIAL TRANSFORM & VITALS ---
	/** Kabir's world space location */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|SaveGame")
	FVector PlayerLocation;

	/** Kabir's world space orientation */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|SaveGame")
	FRotator PlayerRotation;

	/** Kabir's sprint stamina at time of save */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|SaveGame")
	float CurrentStamina;

	// --- CHECKPOINT RESPOND TRANSFORM ---
	/** Active safe respawn checkpoint location */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|SaveGame")
	FVector CheckpointLocation;

	/** Active safe respawn checkpoint rotation */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|SaveGame")
	FRotator CheckpointRotation;

	// --- CLANDESTINE SATCHEL INVENTORY ---
	/** Count of underground Satyagraha handbills carried */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|SaveGame")
	int32 PamphletCount;

	/** Count of clay marble distraction pebbles in pouch */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|SaveGame")
	int32 PebbleCount;

	/** Count of tailor's scout chalk pieces carried */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|SaveGame")
	int32 ChalkCount;

	// --- HISTORICAL CODEX ARCHIVAL STATE ---
	/** Last active or viewed codex entry index */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|SaveGame")
	int32 SelectedCodexIndex;

	// --- AUDIO MIX & ACCESSIBILITY PREFERENCES ---
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|SaveGame")
	float MasterVolume;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|SaveGame")
	float SFXVolume;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|SaveGame")
	float FoleyVolume;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|SaveGame")
	float VoiceVolume;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|SaveGame")
	float AmbienceVolume;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|SaveGame")
	float SubtitleScaleMultiplier;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|SaveGame")
	bool bHandheldSteamOSMode;

	// --- COMMUNITY TRUST ARCHITECTURE ---
	/** Serialized community trust stances keyed by ClusterID (0=Neutral, 1=Cautious, 2=Trusted, 3=Compromised) */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|SaveGame")
	TMap<FName, uint8> CommunityStances;

	/** Serialized numerical trust scores keyed by ClusterID (0-100) */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|SaveGame")
	TMap<FName, int32> CommunityTrustScores;
};
