// Copyright Epic Games, Inc. All Rights Reserved.

#include "RevolutionMissionSubsystem.h"
#include "UObject/ConstructorHelpers.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/SoundBase.h"
#include "REVOLUTION.h"

URevolutionMissionSubsystem::URevolutionMissionSubsystem()
{
	static ConstructorHelpers::FObjectFinder<USoundBase> RetrieveSoundFinder(TEXT("/Game/Audio/SFX/SFX_Pamphlet_Retrieve.SFX_Pamphlet_Retrieve"));
	if (RetrieveSoundFinder.Succeeded())
	{
		PamphletRetrieveSound = RetrieveSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> GongSoundFinder(TEXT("/Game/Audio/SFX/SFX_Dawn_Gong_Complete.SFX_Dawn_Gong_Complete"));
	if (GongSoundFinder.Succeeded())
	{
		DawnGongCompleteSound = GongSoundFinder.Object;
	}

	CurrentStage = ECourierMissionStage::Stage_RetrievePamphlets;
}

void URevolutionMissionSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
	Super::Initialize(Collection);

	CurrentStage = ECourierMissionStage::Stage_RetrievePamphlets;
	UpdateDirectiveStrings();

	UE_LOG(LogREVOLUTION, Log, TEXT("RevolutionMissionSubsystem initialized: Stage 1 active."));
}

void URevolutionMissionSubsystem::AdvanceMissionStage()
{
	UWorld* World = GetWorld();

	switch (CurrentStage)
	{
	case ECourierMissionStage::Stage_RetrievePamphlets:
		if (PamphletRetrieveSound && World)
		{
			UGameplayStatics::PlaySound2D(World, PamphletRetrieveSound, 1.0f);
		}
		CurrentStage = ECourierMissionStage::Stage_RooftopInfiltration;
		break;

	case ECourierMissionStage::Stage_RooftopInfiltration:
		CurrentStage = ECourierMissionStage::Stage_DeliverToStash;
		break;

	case ECourierMissionStage::Stage_DeliverToStash:
		if (PamphletRetrieveSound && World)
		{
			UGameplayStatics::PlaySound2D(World, PamphletRetrieveSound, 0.9f, 1.05f);
		}
		CurrentStage = ECourierMissionStage::Stage_EvadeAndSurvive;
		break;

	case ECourierMissionStage::Stage_EvadeAndSurvive:
		CurrentStage = ECourierMissionStage::Stage_Completed;
		if (DawnGongCompleteSound && World)
		{
			UGameplayStatics::PlaySound2D(World, DawnGongCompleteSound, 1.0f);
		}
		break;

	case ECourierMissionStage::Stage_Completed:
		// Already finished
		return;
	}

	UpdateDirectiveStrings();
	OnMissionDirectiveChanged.Broadcast(CurrentStage, CachedTitle, CachedDirective);

	UE_LOG(LogREVOLUTION, Log, TEXT("Mission Stage Advanced to: %s"), *CachedTitle.ToString());
}

void URevolutionMissionSubsystem::UpdateDirectiveStrings()
{
	switch (CurrentStage)
	{
	case ECourierMissionStage::Stage_RetrievePamphlets:
		CachedTitle = FText::FromString(TEXT("RETRIEVE CLANDESTINE PAMPHLETS"));
		CachedDirective = FText::FromString(TEXT("Collect the concealed anti-Rowlatt bulletins near the courtyard charpai."));
		break;

	case ECourierMissionStage::Stage_RooftopInfiltration:
		CachedTitle = FText::FromString(TEXT("CROSS MOONLIT ROOFTOPS"));
		CachedDirective = FText::FromString(TEXT("Ascend the masonry steps and vault the 1.1m parapet. Avoid the watchman's lantern."));
		break;

	case ECourierMissionStage::Stage_DeliverToStash:
		CachedTitle = FText::FromString(TEXT("DEPOSIT IN COURIER STASH"));
		CachedDirective = FText::FromString(TEXT("Slip the bulletins into the hidden courier drop box near the Jharokha balcony."));
		break;

	case ECourierMissionStage::Stage_EvadeAndSurvive:
		CachedTitle = FText::FromString(TEXT("RETURN TO HAVELI COURTYARD"));
		CachedDirective = FText::FromString(TEXT("Evade curfew patrols and return safely to the courtyard daybed before dawn."));
		break;

	case ECourierMissionStage::Stage_Completed:
		CachedTitle = FText::FromString(TEXT("COURIER MISSION ACCOMPLISHED"));
		CachedDirective = FText::FromString(TEXT("Leaflets delivered. The Hartal protest call will circulate across Kot Gurdarshan."));
		break;
	}
}

FText URevolutionMissionSubsystem::GetCurrentStageTitle() const
{
	return CachedTitle;
}

FText URevolutionMissionSubsystem::GetCurrentStageDirective() const
{
	return CachedDirective;
}
