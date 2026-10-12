// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "RevolutionMissionSubsystem.generated.h"

class USoundBase;

UENUM(BlueprintType)
enum class ECourierMissionStage : uint8
{
	Stage_Morning_FatherTailor UMETA(DisplayName = "1. Father's Tailor Dispatch"),
	Stage_Morning_RooftopKite UMETA(DisplayName = "2. Rooftop Basant Kite"),
	Stage_Morning_WellBhishti UMETA(DisplayName = "3. Mohalla Well & Bhishti"),
	Stage_Morning_DeliverCloth UMETA(DisplayName = "4. Grand Bazaar Cloth Guild"),
	Stage_Morning_ChaiHalwai UMETA(DisplayName = "5. Halwai Tea Stall Rumors"),
	Stage_Morning_ProclamationBoard UMETA(DisplayName = "6. Colonial Proclamation Notice"),
	Stage_Morning_SchoolBell UMETA(DisplayName = "7. Ring Middle School Bell"),
	Stage_Morning_ClassroomDesk UMETA(DisplayName = "8. Classroom 4B Student Desk"),
	Stage_Completed UMETA(DisplayName = "9. Mission Accomplished"),

	// Legacy aliases for compatibility
	Stage_RetrievePamphlets = Stage_Morning_FatherTailor,
	Stage_RooftopInfiltration = Stage_Morning_RooftopKite,
	Stage_DeliverToStash = Stage_Morning_DeliverCloth,
	Stage_EvadeAndSurvive = Stage_Morning_SchoolBell
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnMissionDirectiveChanged, ECourierMissionStage, NewStage, FText, Title, FText, Directive);

/**
 * World Subsystem managing Kabir's historical 1919 Act I story mission & courier directives.
 * Features:
 * - Multi-stage Act I narrative journey from courtyard to bazaar to school
 * - Historical period directives and cultural terminology
 * - Dynamic HUD notification broadcasts
 * - Completion gong & school bell audio synchronization
 */
UCLASS()
class REVOLUTION_API URevolutionMissionSubsystem : public UWorldSubsystem
{
	GENERATED_BODY()

public:
	URevolutionMissionSubsystem();

	virtual void Initialize(FSubsystemCollectionBase& Collection) override;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Mission")
	ECourierMissionStage CurrentStage = ECourierMissionStage::Stage_Morning_FatherTailor;

	UPROPERTY(BlueprintAssignable, Category = "Revolution|Mission")
	FOnMissionDirectiveChanged OnMissionDirectiveChanged;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* PamphletRetrieveSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* DawnGongCompleteSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* SchoolBellSound = nullptr;

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
