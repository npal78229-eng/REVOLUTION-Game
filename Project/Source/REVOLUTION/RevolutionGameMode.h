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
};
