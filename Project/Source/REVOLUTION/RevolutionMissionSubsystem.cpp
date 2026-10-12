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

	static ConstructorHelpers::FObjectFinder<USoundBase> BellSoundFinder(TEXT("/Game/Audio/SFX/SFX_Dawn_Temple_Bell.SFX_Dawn_Temple_Bell"));
	if (BellSoundFinder.Succeeded())
	{
		SchoolBellSound = BellSoundFinder.Object;
	}

	CurrentStage = ECourierMissionStage::Stage_Morning_FatherTailor;
}

void URevolutionMissionSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
	Super::Initialize(Collection);

	CurrentStage = ECourierMissionStage::Stage_Morning_FatherTailor;
	UpdateDirectiveStrings();

	UE_LOG(LogREVOLUTION, Log, TEXT("RevolutionMissionSubsystem initialized: Act I 'The Morning Courier' active."));
}

void URevolutionMissionSubsystem::AdvanceMissionStage()
{
	UWorld* World = GetWorld();

	switch (CurrentStage)
	{
	case ECourierMissionStage::Stage_Morning_FatherTailor:
		if (PamphletRetrieveSound && World)
		{
			UGameplayStatics::PlaySound2D(World, PamphletRetrieveSound, 1.0f);
		}
		CurrentStage = ECourierMissionStage::Stage_Morning_RooftopKite;
		break;

	case ECourierMissionStage::Stage_Morning_RooftopKite:
		CurrentStage = ECourierMissionStage::Stage_Morning_WellBhishti;
		break;

	case ECourierMissionStage::Stage_Morning_WellBhishti:
		CurrentStage = ECourierMissionStage::Stage_Morning_DeliverCloth;
		break;

	case ECourierMissionStage::Stage_Morning_DeliverCloth:
		if (PamphletRetrieveSound && World)
		{
			UGameplayStatics::PlaySound2D(World, PamphletRetrieveSound, 0.9f, 1.05f);
		}
		CurrentStage = ECourierMissionStage::Stage_Morning_ChaiHalwai;
		break;

	case ECourierMissionStage::Stage_Morning_ChaiHalwai:
		CurrentStage = ECourierMissionStage::Stage_Morning_ProclamationBoard;
		break;

	case ECourierMissionStage::Stage_Morning_ProclamationBoard:
		CurrentStage = ECourierMissionStage::Stage_Morning_SchoolBell;
		break;

	case ECourierMissionStage::Stage_Morning_SchoolBell:
		if (SchoolBellSound && World)
		{
			UGameplayStatics::PlaySound2D(World, SchoolBellSound, 1.25f);
		}
		CurrentStage = ECourierMissionStage::Stage_Morning_ClassroomDesk;
		break;

	case ECourierMissionStage::Stage_Morning_ClassroomDesk:
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
	case ECourierMissionStage::Stage_Morning_FatherTailor:
		CachedTitle = FText::FromString(TEXT("FATHER'S TAILOR DISPATCH"));
		CachedDirective = FText::FromString(TEXT("Speak with father Ram Lubhaya at the veranda sewing machine to collect the repaired khadi coat."));
		break;

	case ECourierMissionStage::Stage_Morning_RooftopKite:
		CachedTitle = FText::FromString(TEXT("SURVEY FROM THE ROOFTOP"));
		CachedDirective = FText::FromString(TEXT("Ascend the courtyard masonry stairs to the 1F terrace and check your fighter kite spool on the north parapet."));
		break;

	case ECourierMissionStage::Stage_Morning_WellBhishti:
		CachedTitle = FText::FromString(TEXT("COMMUNAL WELL SQUARE"));
		CachedDirective = FText::FromString(TEXT("Descend through the Deorhi gateway into Zone C. Greet Ghasita Bhishti drawing water at the communal stone well."));
		break;

	case ECourierMissionStage::Stage_Morning_DeliverCloth:
		CachedTitle = FText::FromString(TEXT("DELIVER TO LALA KARAM CHAND"));
		CachedDirective = FText::FromString(TEXT("Enter the Grand Bazaar thoroughfare and deliver the khadi coat to Lala Karam Chand at the textile stall."));
		break;

	case ECourierMissionStage::Stage_Morning_ChaiHalwai:
		CachedTitle = FText::FromString(TEXT("MORNING CHAI & BAZAAR RUMORS"));
		CachedDirective = FText::FromString(TEXT("Stop at Hira Halwai's tea stall across the street. Drink a hot kulhad of chai and listen to rumors of the Rowlatt Act."));
		break;

	case ECourierMissionStage::Stage_Morning_ProclamationBoard:
		CachedTitle = FText::FromString(TEXT("INSPECT SECTION 144 NOTICE"));
		CachedDirective = FText::FromString(TEXT("Examine the British martial law decree posted on the wooden proclamation board near the municipal police naka."));
		break;

	case ECourierMissionStage::Stage_Morning_SchoolBell:
		CachedTitle = FText::FromString(TEXT("TOLL THE MORNING SCHOOL BELL"));
		CachedDirective = FText::FromString(TEXT("Pass through the school gate into District C. Ring the central iron bell tower to signal morning classes for Pandit Kashi Ram."));
		break;

	case ECourierMissionStage::Stage_Morning_ClassroomDesk:
		CachedTitle = FText::FromString(TEXT("TAKE YOUR DESK IN CLASSROOM 4B"));
		CachedDirective = FText::FromString(TEXT("Enter Classroom 4B and sit at your student desk before morning literacy and arithmetic lessons begin."));
		break;

	case ECourierMissionStage::Stage_Completed:
		CachedTitle = FText::FromString(TEXT("ACT I: THE MORNING COURIER COMPLETE"));
		CachedDirective = FText::FromString(TEXT("The morning rhythm of April 1919 has unfolded. The seeds of freedom are planted as the town prepares for the Hartal."));
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
