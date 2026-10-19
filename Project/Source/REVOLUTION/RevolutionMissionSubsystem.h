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
	Stage_Afternoon_MunadiProclamation UMETA(DisplayName = "9. General Dyer's Munadi Proclamation"),
	Stage_Afternoon_BaghNarrowEntry UMETA(DisplayName = "10. The Road to Jallianwala Bagh"),
	Stage_ActII_BaisakhiGathering UMETA(DisplayName = "11. The Assembly at the Walled Garden"),
	Stage_ActII_TheFiring UMETA(DisplayName = "12. General Dyer Orders Fire"),
	Stage_ActII_FindEscapeRoute UMETA(DisplayName = "13. Panic in the Enclosure"),
	Stage_ActII_VaultWallBreach UMETA(DisplayName = "14. Vault the Crumbling Wall Breach"),
	Stage_ActII_Completed UMETA(DisplayName = "15. Act II Finale: Escape from Jallianwala Bagh"),
	Stage_ActIII_NightCurfewFall UMETA(DisplayName = "16. Act III: The Martial Law Curfew"),
	Stage_ActIII_EvadeSearchlightPicket UMETA(DisplayName = "17. Evade Imperial Searchlight Picket"),
	Stage_ActIII_AidWoundedSurvivors UMETA(DisplayName = "18. Clandestine Aid to the Wounded"),
	Stage_ActIII_Completed UMETA(DisplayName = "19. Act III Finale: The Curfew Defied"),
	Stage_ActIV_ReachCanalDistributary UMETA(DisplayName = "20. Outskirts: Upper Bari Doab Canal Sluice"),
	Stage_ActIV_PersianWheelContact UMETA(DisplayName = "21. Agricultural Feeder & Persian Wheel (Rahat)"),
	Stage_ActIV_BrickKilnSafehouse UMETA(DisplayName = "22. The Bhatta Brick Kiln Resistance Stash"),
	Stage_ActIV_Completed UMETA(DisplayName = "23. Act IV Finale: Safehouse Reached"),
	Stage_ActV_ReachRailwayCutting UMETA(DisplayName = "24. Act V: North Western Railway Cutting"),
	Stage_ActV_ClimbSignalGantry UMETA(DisplayName = "25. Scale the Semaphore Signal Gantry"),
	Stage_ActV_CrossCivilLinesPalisade UMETA(DisplayName = "26. Breach the Civil Lines Perimeter"),
	Stage_Completed UMETA(DisplayName = "27. Act V Milestone: Into the Cantonment"),

	// Legacy aliases for compatibility
	Stage_RetrievePamphlets = Stage_Morning_FatherTailor,
	Stage_RooftopInfiltration = Stage_Morning_RooftopKite,
	Stage_DeliverToStash = Stage_Morning_DeliverCloth,
	Stage_EvadeAndSurvive = Stage_Morning_SchoolBell
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnMissionDirectiveChanged, ECourierMissionStage, NewStage, FText, Title, FText, Directive);

/**
 * World Subsystem managing Kabir's historical 1919 Act I, II, III & IV story mission & courier directives.
 * Features:
 * - Multi-stage Act I, II, III & IV narrative journey: Courtyard -> Bazaar -> School -> Jallianwala Bagh -> Curfew -> Canal Outskirts
 * - Historical period directives and cultural terminology
 * - Dynamic HUD notification broadcasts
 * - Completion gong, munadi drum, bugle charge, panic, curfew whistle, cricket night, canal flow & rahat creak audio synchronization
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

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* MunadiDrumSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* BaisakhiCrowdSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* RallySpeechSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* MilitaryMarchSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* BugleChargeSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* CrowdPanicSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* CricketAmbienceSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* CurfewWhistleSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* CanalWaterFlowSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* RahatCreakSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* SteamLocomotiveSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* RailwaySignalBellSound = nullptr;

	UFUNCTION(BlueprintCallable, Category = "Revolution|Mission")
	void AdvanceMissionStage();

	UFUNCTION(BlueprintCallable, Category = "Revolution|Mission")
	void SetMissionStage(ECourierMissionStage NewStage);

	UFUNCTION(BlueprintPure, Category = "Revolution|Mission")
	ECourierMissionStage GetCurrentStage() const { return CurrentStage; }

	UFUNCTION(BlueprintPure, Category = "Revolution|Mission")
	FText GetCurrentStageTitle() const;

	UFUNCTION(BlueprintPure, Category = "Revolution|Mission")
	FText GetCurrentStageDirective() const;

	UFUNCTION(BlueprintPure, Category = "Revolution|Mission")
	bool IsMissionComplete() const { return CurrentStage == ECourierMissionStage::Stage_Completed; }

	UFUNCTION(BlueprintPure, Category = "Revolution|Mission")
	bool GetActiveObjectiveLocation(FVector& OutLocation, FText& OutObjectiveName) const;

private:
	void UpdateDirectiveStrings();

	FText CachedTitle;
	FText CachedDirective;
};
