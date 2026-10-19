// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "RevolutionGameMode.generated.h"

class ACurfewPatrolAI;
class ARevolutionCharacter;

UCLASS(minimalapi)
class ARevolutionGameMode : public AGameModeBase
{
	GENERATED_BODY()

public:
	ARevolutionGameMode();

protected:
	virtual void BeginPlay() override;

	/** Ensures interactive period artifacts and traversal obstacles exist in the courtyard */
	void SpawnDefaultMohallaProps();

	virtual AActor* ChoosePlayerStart_Implementation(AController* Player) override;
	virtual APawn* SpawnDefaultPawnAtTransform_Implementation(AController* NewPlayer, const FTransform& SpawnTransform) override;

public:
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Curfew")
	bool bIsPlayerApprehended = false;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Curfew")
	float ApprehensionTimer = 0.0f;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Curfew")
	FVector CheckpointLocation = FVector(10.0f, 20.0f, 15.0f);

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Curfew")
	FRotator CheckpointRotation = FRotator(0.0f, 0.0f, 0.0f);

	/** Called when a colonial watchman corners and catches Kabir */
	UFUNCTION(BlueprintCallable, Category = "Revolution|Curfew")
	void HandlePlayerApprehended(ACurfewPatrolAI* Watchman, ARevolutionCharacter* CaughtPlayer);

	/** Respawns player at last safe checkpoint */
	UFUNCTION(BlueprintCallable, Category = "Revolution|Curfew")
	void RespawnPlayerAtCheckpoint();

	/** Update latest safe checkpoint location */
	UFUNCTION(BlueprintCallable, Category = "Revolution|Curfew")
	void SetCheckpoint(const FVector& NewLocation, const FRotator& NewRotation);

	UFUNCTION(BlueprintPure, Category = "Revolution|Curfew")
	bool IsPlayerApprehended() const { return bIsPlayerApprehended; }

	// --- TASK 30: PERSISTENT SAVE / LOAD SYSTEM ---
	/** Saves complete player and mission state to disk slot */
	UFUNCTION(BlueprintCallable, Category = "Revolution|SaveGame")
	bool SaveGameToSlot(const FString& SlotName = TEXT("RevolutionSave_Slot0"), int32 UserIndex = 0);

	/** Loads complete player and mission state from disk slot */
	UFUNCTION(BlueprintCallable, Category = "Revolution|SaveGame")
	bool LoadGameFromSlot(const FString& SlotName = TEXT("RevolutionSave_Slot0"), int32 UserIndex = 0);

	/** Checks whether a save file exists in the specified slot */
	UFUNCTION(BlueprintPure, Category = "Revolution|SaveGame")
	bool DoesSaveGameExist(const FString& SlotName = TEXT("RevolutionSave_Slot0"), int32 UserIndex = 0) const;

	/** Deletes a save game file from disk */
	UFUNCTION(BlueprintCallable, Category = "Revolution|SaveGame")
	bool DeleteSaveSlot(const FString& SlotName = TEXT("RevolutionSave_Slot0"), int32 UserIndex = 0);

	/** Timestamp of last saved game */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|SaveGame")
	FDateTime LastSaveTimestamp;

	/** Utility to repair BlendSpace sample data using native C++ API */
	UFUNCTION(BlueprintCallable, Category = "Revolution|Animation")
	static bool FixKabirBlendSpace();
};
