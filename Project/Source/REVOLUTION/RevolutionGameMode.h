// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "RevolutionGameMode.generated.h"

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
};
