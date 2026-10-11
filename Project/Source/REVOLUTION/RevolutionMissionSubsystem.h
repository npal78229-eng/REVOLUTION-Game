// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "RevolutionMissionSubsystem.generated.h"

class USoundBase;

UENUM(BlueprintType)
enum class ECourierMissionStage : uint8
{
	Stage_RetrievePamphlets UMETA(DisplayName = "1. Retrieve Leaflets"),
	Stage_RooftopInfiltration UMETA(DisplayName = "2. Rooftop Infiltration"),
	Stage_DeliverToStash UMETA(DisplayName = "3. Deposit in Courier Stash"),
	Stage_EvadeAndSurvive UMETA(DisplayName = "4. Return to Courtyard"),
	Stage_Completed UMETA(DisplayName = "5. Mission Accomplished")
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnMissionDirectiveChanged, ECourierMissionStage, NewStage, FText, Title, FText, Directive);

/**
 * World Subsystem managing Kabir's historical 1919 anti-Rowlatt courier mission.
 * Features:
 * - Multi-stage clandestine objective tracking
 * - Historical period directives
 * - Dynamic HUD notification broadcasts
 * - Completion gong & pickup audio synchronization
 */
UCLASS()
class REVOLUTION_API URevolutionMissionSubsystem : public UWorldSubsystem
{
	GENERATED_BODY()

public:
	URevolutionMissionSubsystem();

	virtual void Initialize(FSubsystemCollectionBase& Collection) override;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Mission")
	ECourierMissionStage CurrentStage = ECourierMissionStage::Stage_RetrievePamphlets;

	UPROPERTY(BlueprintAssignable, Category = "Revolution|Mission")
	FOnMissionDirectiveChanged OnMissionDirectiveChanged;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* PamphletRetrieveSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* DawnGongCompleteSound = nullptr;

	UFUNCTION(BlueprintCallable, Category = "Revolution|Mission")
	void AdvanceMissionStage();

	UFUNCTION(BlueprintPure, Category = "Revolution|Mission")
	ECourierMissionStage GetCurrentStage() const { return CurrentStage; }

	UFUNCTION(BlueprintPure, Category = "Revolution|Mission")
	FText GetCurrentStageTitle() const;

	UFUNCTION(BlueprintPure, Category = "Revolution|Mission")
	FText GetCurrentStageDirective() const;

	UFUNCTION(BlueprintPure, Category = "Revolution|Mission")
	bool IsMissionComplete() const { return CurrentStage == ECourierMissionStage::Stage_Completed; }

private:
	void UpdateDirectiveStrings();

	FText CachedTitle;
	FText CachedDirective;
};
