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

	static ConstructorHelpers::FObjectFinder<USoundBase> MunadiSoundFinder(TEXT("/Game/Audio/SFX/SFX_Munadi_Drum.SFX_Munadi_Drum"));
	if (MunadiSoundFinder.Succeeded())
	{
		MunadiDrumSound = MunadiSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> CrowdSoundFinder(TEXT("/Game/Audio/SFX/SFX_Baisakhi_Crowd_Murmur.SFX_Baisakhi_Crowd_Murmur"));
	if (CrowdSoundFinder.Succeeded())
	{
		BaisakhiCrowdSound = CrowdSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> RallySoundFinder(TEXT("/Game/Audio/SFX/SFX_Crowd_Rally_Speech.SFX_Crowd_Rally_Speech"));
	if (RallySoundFinder.Succeeded())
	{
		RallySpeechSound = RallySoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> MarchSoundFinder(TEXT("/Game/Audio/SFX/SFX_Military_Boot_March.SFX_Military_Boot_March"));
	if (MarchSoundFinder.Succeeded())
	{
		MilitaryMarchSound = MarchSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> BugleSoundFinder(TEXT("/Game/Audio/SFX/SFX_Bugle_Call_Charge.SFX_Bugle_Call_Charge"));
	if (BugleSoundFinder.Succeeded())
	{
		BugleChargeSound = BugleSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> PanicSoundFinder(TEXT("/Game/Audio/SFX/SFX_Crowd_Panic_Scream.SFX_Crowd_Panic_Scream"));
	if (PanicSoundFinder.Succeeded())
	{
		CrowdPanicSound = PanicSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> CricketSoundFinder(TEXT("/Game/Audio/SFX/SFX_Night_Cricket_Ambience.SFX_Night_Cricket_Ambience"));
	if (CricketSoundFinder.Succeeded())
	{
		CricketAmbienceSound = CricketSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> WhistleSoundFinder(TEXT("/Game/Audio/SFX/SFX_Police_Whistle_Curfew.SFX_Police_Whistle_Curfew"));
	if (WhistleSoundFinder.Succeeded())
	{
		CurfewWhistleSound = WhistleSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> CanalSoundFinder(TEXT("/Game/Audio/SFX/SFX_Canal_Water_Flow_Gentle.SFX_Canal_Water_Flow_Gentle"));
	if (CanalSoundFinder.Succeeded())
	{
		CanalWaterFlowSound = CanalSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> RahatSoundFinder(TEXT("/Game/Audio/SFX/SFX_Persian_Wheel_Rahat_Creak.SFX_Persian_Wheel_Rahat_Creak"));
	if (RahatSoundFinder.Succeeded())
	{
		RahatCreakSound = RahatSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> TrainSoundFinder(TEXT("/Game/Audio/SFX/SFX_Steam_Locomotive_Idling.SFX_Steam_Locomotive_Idling"));
	if (TrainSoundFinder.Succeeded())
	{
		SteamLocomotiveSound = TrainSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> SignalBellSoundFinder(TEXT("/Game/Audio/SFX/SFX_Railway_Signal_Bell.SFX_Railway_Signal_Bell"));
	if (SignalBellSoundFinder.Succeeded())
	{
		RailwaySignalBellSound = SignalBellSoundFinder.Object;
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
		if (DawnGongCompleteSound && World)
		{
			UGameplayStatics::PlaySound2D(World, DawnGongCompleteSound, 1.0f);
		}
		CurrentStage = ECourierMissionStage::Stage_Afternoon_MunadiProclamation;
		break;

	case ECourierMissionStage::Stage_Afternoon_MunadiProclamation:
		if (MunadiDrumSound && World)
		{
			UGameplayStatics::PlaySound2D(World, MunadiDrumSound, 1.15f);
		}
		CurrentStage = ECourierMissionStage::Stage_Afternoon_BaghNarrowEntry;
		break;

	case ECourierMissionStage::Stage_Afternoon_BaghNarrowEntry:
		if (RallySpeechSound && World)
		{
			UGameplayStatics::PlaySound2D(World, RallySpeechSound, 1.0f);
		}
		else if (BaisakhiCrowdSound && World)
		{
			UGameplayStatics::PlaySound2D(World, BaisakhiCrowdSound, 0.95f);
		}
		CurrentStage = ECourierMissionStage::Stage_ActII_BaisakhiGathering;
		break;

	case ECourierMissionStage::Stage_ActII_BaisakhiGathering:
		if (MilitaryMarchSound && World)
		{
			UGameplayStatics::PlaySound2D(World, MilitaryMarchSound, 1.15f);
		}
		CurrentStage = ECourierMissionStage::Stage_ActII_TheFiring;
		break;

	case ECourierMissionStage::Stage_ActII_TheFiring:
		if (BugleChargeSound && World)
		{
			UGameplayStatics::PlaySound2D(World, BugleChargeSound, 1.25f);
		}
		CurrentStage = ECourierMissionStage::Stage_ActII_FindEscapeRoute;
		break;

	case ECourierMissionStage::Stage_ActII_FindEscapeRoute:
		if (CrowdPanicSound && World)
		{
			UGameplayStatics::PlaySound2D(World, CrowdPanicSound, 1.20f);
		}
		CurrentStage = ECourierMissionStage::Stage_ActII_VaultWallBreach;
		break;

	case ECourierMissionStage::Stage_ActII_VaultWallBreach:
		if (DawnGongCompleteSound && World)
		{
			UGameplayStatics::PlaySound2D(World, DawnGongCompleteSound, 1.0f);
		}
		CurrentStage = ECourierMissionStage::Stage_ActII_Completed;
		break;

	case ECourierMissionStage::Stage_ActII_Completed:
		if (CricketAmbienceSound && World)
		{
			UGameplayStatics::PlaySound2D(World, CricketAmbienceSound, 1.0f);
		}
		CurrentStage = ECourierMissionStage::Stage_ActIII_NightCurfewFall;
		break;

	case ECourierMissionStage::Stage_ActIII_NightCurfewFall:
		if (CurfewWhistleSound && World)
		{
			UGameplayStatics::PlaySound2D(World, CurfewWhistleSound, 1.25f);
		}
		CurrentStage = ECourierMissionStage::Stage_ActIII_EvadeSearchlightPicket;
		break;

	case ECourierMissionStage::Stage_ActIII_EvadeSearchlightPicket:
		if (MilitaryMarchSound && World)
		{
			UGameplayStatics::PlaySound2D(World, MilitaryMarchSound, 1.15f);
		}
		CurrentStage = ECourierMissionStage::Stage_ActIII_AidWoundedSurvivors;
		break;

	case ECourierMissionStage::Stage_ActIII_AidWoundedSurvivors:
		if (DawnGongCompleteSound && World)
		{
			UGameplayStatics::PlaySound2D(World, DawnGongCompleteSound, 1.1f);
		}
		CurrentStage = ECourierMissionStage::Stage_ActIII_Completed;
		break;

	case ECourierMissionStage::Stage_ActIII_Completed:
		if (CanalWaterFlowSound && World)
		{
			UGameplayStatics::PlaySound2D(World, CanalWaterFlowSound, 1.0f);
		}
		CurrentStage = ECourierMissionStage::Stage_ActIV_ReachCanalDistributary;
		break;

	case ECourierMissionStage::Stage_ActIV_ReachCanalDistributary:
		if (RahatCreakSound && World)
		{
			UGameplayStatics::PlaySound2D(World, RahatCreakSound, 1.15f);
		}
		CurrentStage = ECourierMissionStage::Stage_ActIV_PersianWheelContact;
		break;

	case ECourierMissionStage::Stage_ActIV_PersianWheelContact:
		if (PamphletRetrieveSound && World)
		{
			UGameplayStatics::PlaySound2D(World, PamphletRetrieveSound, 1.0f);
		}
		CurrentStage = ECourierMissionStage::Stage_ActIV_BrickKilnSafehouse;
		break;

	case ECourierMissionStage::Stage_ActIV_BrickKilnSafehouse:
		if (DawnGongCompleteSound && World)
		{
			UGameplayStatics::PlaySound2D(World, DawnGongCompleteSound, 1.2f);
		}
		CurrentStage = ECourierMissionStage::Stage_ActIV_Completed;
		break;

	case ECourierMissionStage::Stage_ActIV_Completed:
		if (SteamLocomotiveSound && World)
		{
			UGameplayStatics::PlaySound2D(World, SteamLocomotiveSound, 1.0f);
		}
		CurrentStage = ECourierMissionStage::Stage_ActV_ReachRailwayCutting;
		break;

	case ECourierMissionStage::Stage_ActV_ReachRailwayCutting:
		if (RailwaySignalBellSound && World)
		{
			UGameplayStatics::PlaySound2D(World, RailwaySignalBellSound, 1.15f);
		}
		CurrentStage = ECourierMissionStage::Stage_ActV_ClimbSignalGantry;
		break;

	case ECourierMissionStage::Stage_ActV_ClimbSignalGantry:
		if (PamphletRetrieveSound && World)
		{
			UGameplayStatics::PlaySound2D(World, PamphletRetrieveSound, 1.0f);
		}
		CurrentStage = ECourierMissionStage::Stage_ActV_CrossCivilLinesPalisade;
		break;

	case ECourierMissionStage::Stage_ActV_CrossCivilLinesPalisade:
		if (DawnGongCompleteSound && World)
		{
			UGameplayStatics::PlaySound2D(World, DawnGongCompleteSound, 1.25f);
		}
		CurrentStage = ECourierMissionStage::Stage_Completed;
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

	case ECourierMissionStage::Stage_Afternoon_MunadiProclamation:
		CachedTitle = FText::FromString(TEXT("GENERAL DYER'S MUNADI PROCLAMATION"));
		CachedDirective = FText::FromString(TEXT("The afternoon drum echoes through the Grand Bazaar. Investigate the Town Crier's proclamation drum stand near the police picket."));
		break;

	case ECourierMissionStage::Stage_Afternoon_BaghNarrowEntry:
		CachedTitle = FText::FromString(TEXT("THE ROAD TO JALLIANWALA BAGH"));
		CachedDirective = FText::FromString(TEXT("Follow the Baisakhi festival crowd through the marigold chowk archway toward the historic northern passage into Jallianwala Bagh."));
		break;

	case ECourierMissionStage::Stage_ActII_BaisakhiGathering:
		CachedTitle = FText::FromString(TEXT("ASSEMBLY AT THE WALLED GARDEN"));
		CachedDirective = FText::FromString(TEXT("Navigate the 2.2m claustrophobic corridor gateway into the enclosed garden where thousands of peaceful families have assembled."));
		break;

	case ECourierMissionStage::Stage_ActII_TheFiring:
		CachedTitle = FText::FromString(TEXT("13 APRIL 1919 — THE CENSORED DUSK"));
		CachedDirective = FText::FromString(TEXT("The gates of Jallianwala Bagh are sealed under martial order. As imperial censorship descends, observe the courtyard remnants in solemn remembrance."));
		break;

	case ECourierMissionStage::Stage_ActII_FindEscapeRoute:
		CachedTitle = FText::FromString(TEXT("THE VEIL OF REMEMBRANCE"));
		CachedDirective = FText::FromString(TEXT("Censorship bars the truth from print. Contemplate the sacred courtyard remnants and locate the western brick wall breach to carry the dispatch to safety."));
		break;

	case ECourierMissionStage::Stage_ActII_VaultWallBreach:
		CachedTitle = FText::FromString(TEXT("VAULT THE CRUMBLING WALL BREACH"));
		CachedDirective = FText::FromString(TEXT("Scramble up the collapsed brick rubble talus and vault the 1.8m low wall breach to escape into the rear haveli alleys."));
		break;

	case ECourierMissionStage::Stage_ActII_Completed:
		CachedTitle = FText::FromString(TEXT("ACT II FINALE: ESCAPE FROM JALLIANWALA BAGH"));
		CachedDirective = FText::FromString(TEXT("Kabir vaults into the safety of the back alleys as dusk falls over Amritsar. The peaceful innocence is gone; the revolution has begun."));
		break;

	case ECourierMissionStage::Stage_ActIII_NightCurfewFall:
		CachedTitle = FText::FromString(TEXT("ACT III: THE MARTIAL LAW CURFEW"));
		CachedDirective = FText::FromString(TEXT("Night has descended. General Dyer's strict 8:00 PM curfew is enforced with shoot-on-sight orders. Examine the martial law notice at the central Chowk."));
		break;

	case ECourierMissionStage::Stage_ActIII_EvadeSearchlightPicket:
		CachedTitle = FText::FromString(TEXT("EVADE IMPERIAL SEARCHLIGHTS"));
		CachedDirective = FText::FromString(TEXT("Imperial carbon-arc searchlights sweep across the northern sandbag checkpoint and surrounding rooftops. Evade the illuminated zones using shadows and alleys."));
		break;

	case ECourierMissionStage::Stage_ActIII_AidWoundedSurvivors:
		CachedTitle = FText::FromString(TEXT("CLANDESTINE AID TO THE WOUNDED"));
		CachedDirective = FText::FromString(TEXT("Locate the makeshift charpai stretcher hidden in the secluded Deorhi alleyway to bring fresh water and clean khadi bandages to wounded survivors."));
		break;

	case ECourierMissionStage::Stage_ActIII_Completed:
		CachedTitle = FText::FromString(TEXT("ACT III FINALE: THE CURFEW DEFIED"));
		CachedDirective = FText::FromString(TEXT("Against martial law and curfew patrols, Kabir and the mohalla volunteers provided aid to the wounded. The city now seeks escape lines beyond the colonial cordons."));
		break;

	case ECourierMissionStage::Stage_ActIV_ReachCanalDistributary:
		CachedTitle = FText::FromString(TEXT("OUTSKIRTS: CANAL SLUICE REGULATOR"));
		CachedDirective = FText::FromString(TEXT("Head west beyond the Grand Bazaar perimeter into Zone F. Follow the water channels to the Upper Bari Doab Canal distributary aqueduct and stone sluice gate."));
		break;

	case ECourierMissionStage::Stage_ActIV_PersianWheelContact:
		CachedTitle = FText::FromString(TEXT("PERSIAN WHEEL (RAHAT) RENDEZVOUS"));
		CachedDirective = FText::FromString(TEXT("Approach the turning timber Persian wheel (Rahat) by the canal feeder well where agricultural couriers coordinate nighttime crossings."));
		break;

	case ECourierMissionStage::Stage_ActIV_BrickKilnSafehouse:
		CachedTitle = FText::FromString(TEXT("THE BHATTA BRICK KILN RESISTANCE CACHE"));
		CachedDirective = FText::FromString(TEXT("Locate the clandestine supply cache hidden behind the Bull's trench brick kiln chimney. Secure the bicycle messenger gear and underground resistance literature."));
		break;

	case ECourierMissionStage::Stage_ActIV_Completed:
		CachedTitle = FText::FromString(TEXT("ACT IV FINALE: SAFEHOUSE SECURED"));
		CachedDirective = FText::FromString(TEXT("With the underground canal route established and printing supplies hidden in the bhatta, prepare for the northern railway crossing into the Civil Lines."));
		break;

	case ECourierMissionStage::Stage_ActV_ReachRailwayCutting:
		CachedTitle = FText::FromString(TEXT("NORTH WESTERN RAILWAY CUTTING"));
		CachedDirective = FText::FromString(TEXT("Navigate north toward the monumental brick overpass. Stay low in the shadows of the stone ballast embankment to evade armed cantonment patrols."));
		break;

	case ECourierMissionStage::Stage_ActV_ClimbSignalGantry:
		CachedTitle = FText::FromString(TEXT("SCALE THE SEMAPHORE SIGNAL GANTRY"));
		CachedDirective = FText::FromString(TEXT("Climb the iron maintenance ladder of the 6.5m semaphore signal tower overlooking the junction. Shift the signal arm to trigger a diversion."));
		break;

	case ECourierMissionStage::Stage_ActV_CrossCivilLinesPalisade:
		CachedTitle = FText::FromString(TEXT("BREACH THE CIVIL LINES PERIMETER"));
		CachedDirective = FText::FromString(TEXT("Slip past the cast-iron spearhead palisade railing into the segregated British Civil Lines to deliver the petition to the administrative records office."));
		break;

	case ECourierMissionStage::Stage_Completed:
		CachedTitle = FText::FromString(TEXT("ACT V MILESTONE: INTO THE CANTONMENT"));
		CachedDirective = FText::FromString(TEXT("From humble beginnings in Kot Gurdarshan to the heart of colonial authority, Kabir's courage has united city, village, and railway in an unyielding revolution."));
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
