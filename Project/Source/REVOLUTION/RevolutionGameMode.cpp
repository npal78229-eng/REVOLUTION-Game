// Copyright Epic Games, Inc. All Rights Reserved.

#include "RevolutionGameMode.h"
#include "RevolutionCharacter.h"
#include "RevolutionHUD.h"
#include "RevolutionSaveGame.h"
#include "RevolutionMissionSubsystem.h"
#include "InspectableProp.h"
#include "CurfewPatrolAI.h"
#include "ObjectiveTriggerActor.h"
#include "RevolutionAtmosphereController.h"
#include "HidingSpotActor.h"
#include "DoorDeorhiActor.h"
#include "PigeonFlockActor.h"
#include "CrawlSpaceActor.h"
#include "TerracottaHazardActor.h"
#include "HandpumpActor.h"
#include "ClotheslineActor.h"
#include "RoshandanActor.h"
#include "SupplyStashActor.h"
#include "ProclamationBoardActor.h"
#include "LithoPressActor.h"
#include "PariahDogActor.h"
#include "CheckpointBarrierActor.h"
#include "ManjaTrapActor.h"
#include "ChaffDustDecoyActor.h"
#include "TelegraphWireActor.h"
#include "MatkaStandActor.h"
#include "CurfewGongActor.h"
#include "CivilianNPCActor.h"
#include "LocomotiveSteamValveActor.h"
#include "Engine/World.h"
#include "Engine/StaticMesh.h"
#include "Components/StaticMeshComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Kismet/GameplayStatics.h"
#include "EngineUtils.h"
#include "GameFramework/PlayerStart.h"
#include "Animation/BlendSpace.h"
#include "Animation/AnimSequence.h"
#include "Misc/PackageName.h"
#include "UObject/SavePackage.h"
#include "REVOLUTION.h"

ARevolutionGameMode::ARevolutionGameMode()
{
	// Set default pawn class to our C++ character
	DefaultPawnClass = ARevolutionCharacter::StaticClass();

	// Set default HUD class to our historical cinematic HUD
	HUDClass = ARevolutionHUD::StaticClass();
}

void ARevolutionGameMode::BeginPlay()
{
	Super::BeginPlay();

	SpawnDefaultMohallaProps();
}

AActor* ARevolutionGameMode::ChoosePlayerStart_Implementation(AController* Player)
{
	UWorld* World = GetWorld();
	if (World)
	{
		for (TActorIterator<APlayerStart> It(World); It; ++It)
		{
			APlayerStart* Start = *It;
			if (Start)
			{
				UE_LOG(LogREVOLUTION, Warning, TEXT("[REVOLUTION_GAMEMODE] ChoosePlayerStart selected: %s at %s"), *Start->GetName(), *Start->GetActorLocation().ToString());
				return Start;
			}
		}
	}

	return Super::ChoosePlayerStart_Implementation(Player);
}

APawn* ARevolutionGameMode::SpawnDefaultPawnAtTransform_Implementation(AController* NewPlayer, const FTransform& SpawnTransform)
{
	FActorSpawnParameters SpawnInfo;
	SpawnInfo.Instigator = GetInstigator();
	SpawnInfo.ObjectFlags |= RF_Transient;
	SpawnInfo.bDeferConstruction = false;
	SpawnInfo.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AdjustIfPossibleButAlwaysSpawn;

	UClass* PawnClass = GetDefaultPawnClassForController(NewPlayer);
	if (PawnClass && GetWorld())
	{
		APawn* SpawnedPawn = GetWorld()->SpawnActor<APawn>(PawnClass, SpawnTransform, SpawnInfo);
		if (SpawnedPawn)
		{
			UE_LOG(LogREVOLUTION, Warning, TEXT("[REVOLUTION_GAMEMODE] Successfully spawned player pawn (%s) at %s"), *PawnClass->GetName(), *SpawnedPawn->GetActorLocation().ToString());
			return SpawnedPawn;
		}
	}

	return Super::SpawnDefaultPawnAtTransform_Implementation(NewPlayer, SpawnTransform);
}

void ARevolutionGameMode::SpawnDefaultMohallaProps()
{
	UWorld* World = GetWorld();
	if (!World) return;

	// Check if any AInspectableProp is already in the world
	int32 ExistingCount = 0;
	for (TActorIterator<AInspectableProp> It(World); It; ++It)
	{
		ExistingCount++;
	}

	if (ExistingCount > 0)
	{
		UE_LOG(LogREVOLUTION, Log, TEXT("Mohalla props already present in level: %d found."), ExistingCount);
		return;
	}

	UE_LOG(LogREVOLUTION, Log, TEXT("Populating default 1919 Mohalla inspectable artifacts into world..."));

	struct FPropDef
	{
		const TCHAR* MeshPath;
		FVector Location;
		FRotator Rotation;
		const TCHAR* Name;
		const TCHAR* Lore;
		const TCHAR* Verb;
	};

	const FPropDef Props[] = {
		{
			TEXT("/Game/Environment/Mohalla/Meshes/SM_Prop_HurricaneLantern.SM_Prop_HurricaneLantern"),
			FVector(80.0f, 160.0f, 25.0f),
			FRotator(0.0f, 20.0f, 0.0f),
			TEXT("Dietz No. 2 Hurricane Lantern"),
			TEXT("A cold-blast tin lantern used by night watchmen and railway switchmen across Punjab. During the stringent 8:00 PM British curfews of April 1919, shuttered courtyards relied on these shielded lamps to move silently between adjoining roofs without alerting street constables."),
			TEXT("Inspect Lantern")
		},
		{
			TEXT("/Game/Environment/Mohalla/Meshes/SM_Prop_Charpai_RopeBed.SM_Prop_Charpai_RopeBed"),
			FVector(120.0f, 160.0f, 10.0f),
			FRotator(0.0f, 45.0f, 0.0f),
			TEXT("Woven Moonj Charpai (Daybed)"),
			TEXT("A traditional wooden frame laced with wild river-grass (moonj) cordage. Set out in the open haveli courtyard during sweltering summers, where Kabir's father repairs tailored coats and discusses whisperings of the Rowlatt Act resistance."),
			TEXT("Inspect Charpai")
		},
		{
			TEXT("/Game/Environment/Mohalla/Meshes/SM_Prop_ClayChaiCup_Kulhad.SM_Prop_ClayChaiCup_Kulhad"),
			FVector(50.0f, 120.0f, 15.0f),
			FRotator(0.0f, -15.0f, 0.0f),
			TEXT("Terracotta Kulhad (Chai Cup)"),
			TEXT("An unglazed earthen cup crafted by local Kumhars on the pottery wheels of the old bazaar. Discarded onto the mud floor after drinking so the baked clay dissolves back into the earth, preserving ritual purity and leaving no trace."),
			TEXT("Inspect Kulhad")
		},
		{
			TEXT("/Game/Environment/Mohalla/Meshes/SM_Prop_GrainSack_Jute_01.SM_Prop_GrainSack_Jute_01"),
			FVector(-160.0f, 140.0f, 10.0f),
			FRotator(0.0f, 105.0f, 0.0f),
			TEXT("Burlap Jute Ration Sack"),
			TEXT("A coarse gunny sack stamped with the British imperial crown and grain procurement seals. Requisitioned wheat intended for wartime rationing in Mesopotamia, leaving Punjabi mandi markets stretched thin by inflation."),
			TEXT("Inspect Ration Sack")
		},
		{
			TEXT("/Game/Environment/Mohalla/Meshes/SM_Prop_Kite_Spool_Charkhi.SM_Prop_Kite_Spool_Charkhi"),
			FVector(0.0f, 220.0f, 410.0f),
			FRotator(0.0f, -35.0f, 0.0f),
			TEXT("Hardwood Charkhi (Kite Spool)"),
			TEXT("A polished wooden spool strung with glass-coated cotton line used during Basant festivals. The young rooftop scouts of Kot Gurdarshan use high-flying fighter kites with colored tails to signal curfew patrols across the railway tracks."),
			TEXT("Inspect Charkhi")
		},
		{
			TEXT("/Game/Environment/Mohalla/Meshes/SM_Prop_GrainSack_Jute_01.SM_Prop_GrainSack_Jute_01"),
			FVector(130.0f, 90.0f, 10.0f),
			FRotator(0.0f, 20.0f, 0.0f),
			TEXT("Stack of Moonj Hemp Sacks"),
			TEXT("Coarse woven hemp sacks stacked in the haveli courtyard. Artisans and cloth merchants stored cotton bolts and indigo-dyed fabric inside during curfew shutdowns."),
			TEXT("Inspect Hemp Sacks")
		},
		{
			TEXT("/Game/Environment/Mohalla/Meshes/SM_Balcony_Jharokha_Wood_A.SM_Balcony_Jharokha_Wood_A"),
			FVector(-200.0f, -80.0f, 320.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			TEXT("Carved Teak Jharokha (Overhang Balcony)"),
			TEXT("An overhanging wooden lattice balcony typical of Walled City mohallas. Women and elders observe bazaar commerce below without being viewed from the street, and scouts use its high vantage to monitor British garrison patrols."),
			TEXT("Inspect Jharokha")
		},
		{
			TEXT("/Game/Environment/Mohalla/Meshes/SM_Roof_Stairs_Masonry_01.SM_Roof_Stairs_Masonry_01"),
			FVector(180.0f, -120.0f, 10.0f),
			FRotator(0.0f, 180.0f, 0.0f),
			TEXT("Masonry Rooftop Steps"),
			TEXT("Narrow baked-brick stairs ascending from the family courtyard to the rooftop terrace. Interconnected rooftops formed the primary courier and escape routes for revolutionaries avoiding street curfews."),
			TEXT("Inspect Steps")
		},
		{
			TEXT("/Game/Environment/Mohalla/Meshes/SM_Roof_Parapet_4m_A.SM_Roof_Parapet_4m_A"),
			FVector(0.0f, 260.0f, 400.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			TEXT("Low Brick Roof Parapet"),
			TEXT("A 1.1-meter high baked clay brick parapet dividing adjoining haveli terraces. Kabir traverses these rooftop boundaries through quick vaults to deliver clandestine pamphlets before dawn."),
			TEXT("Inspect Parapet")
		}
	};

	FActorSpawnParameters SpawnParams;
	SpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

	for (const FPropDef& P : Props)
	{
		AInspectableProp* PropActor = World->SpawnActor<AInspectableProp>(AInspectableProp::StaticClass(), P.Location, P.Rotation, SpawnParams);
		if (PropActor)
		{
			PropActor->ItemName = FText::FromString(P.Name);
			PropActor->LoreDescription = FText::FromString(P.Lore);
			PropActor->InteractionVerb = FText::FromString(P.Verb);

			UStaticMesh* Mesh = LoadObject<UStaticMesh>(nullptr, P.MeshPath);
			if (Mesh && PropActor->MeshComponent)
			{
				PropActor->MeshComponent->SetStaticMesh(Mesh);
			}

			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned InspectableProp: %s at %s"), P.Name, *P.Location.ToString());
		}
	}

	// 2. Spawn Historical Curfew Watchman (Chaukidar with Kerosene Lantern)
	int32 ExistingWatchmen = 0;
	for (TActorIterator<ACurfewPatrolAI> It(World); It; ++It)
	{
		ExistingWatchmen++;
	}

	if (ExistingWatchmen == 0)
	{
		FActorSpawnParameters WatchmanSpawnParams;
		WatchmanSpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

		ACurfewPatrolAI* Watchman = World->SpawnActor<ACurfewPatrolAI>(ACurfewPatrolAI::StaticClass(), FVector(-20.0f, -220.0f, 10.0f), FRotator(0.0f, 90.0f, 0.0f), WatchmanSpawnParams);
		if (Watchman)
		{
			Watchman->WatchmanTitle = FText::FromString(TEXT("Kot Gurdarshan Chaukidar (Night Watchman)"));
			Watchman->PatrolWaypoints.Empty();
			Watchman->PatrolWaypoints.Add(FVector(-20.0f, -200.0f, 10.0f));  // Gateway threshold
			Watchman->PatrolWaypoints.Add(FVector(110.0f, -140.0f, 10.0f));  // Masonry steps base
			Watchman->PatrolWaypoints.Add(FVector(110.0f, 100.0f, 10.0f));   // Courtyard east side
			Watchman->PatrolWaypoints.Add(FVector(-140.0f, 80.0f, 10.0f));   // Jute ration sacks alley corner

			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Curfew Patrol Watchman with Kerosene Lantern at (-20, -220, 10)."));
		}
	}

	// 3. Spawn Act I Story Triggers (Rooftop Kite Survey, School Bell Toll, Classroom 4B Desk)
	int32 ExistingTriggers = 0;
	for (TActorIterator<AObjectiveTriggerActor> It(World); It; ++It)
	{
		ExistingTriggers++;
	}

	if (ExistingTriggers == 0)
	{
		FActorSpawnParameters TriggerSpawnParams;
		TriggerSpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

		// Objective Trigger: Rooftop Terrace Kite Spool Survey
		AObjectiveTriggerActor* RooftopKiteTrigger = World->SpawnActor<AObjectiveTriggerActor>(
			AObjectiveTriggerActor::StaticClass(),
			FVector(240.0f, 320.0f, 410.0f),
			FRotator(0.0f, -45.0f, 0.0f),
			TriggerSpawnParams
		);
		if (RooftopKiteTrigger)
		{
			RooftopKiteTrigger->RequiredMissionStage = ECourierMissionStage::Stage_Morning_RooftopKite;
			RooftopKiteTrigger->InteractionPrompt = FText::FromString(TEXT("Survey from Rooftop"));
			RooftopKiteTrigger->ItemTitle = FText::FromString(TEXT("Basant Charkhi & Rooftop Vantage"));
			RooftopKiteTrigger->HistoricalLoreUponInteraction = FText::FromString(
				TEXT("From this high brick terrace ledge, Kabir spots the morning activity below. Beyond the haveli deorhi archway, water-carrier Ghasita Bhishti is drawing water at the communal stone well. The bazaar and school bell tower rise in the distance.")
			);
			RooftopKiteTrigger->bHideMeshOnTrigger = false;

			UStaticMesh* SpoolMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Game/Environment/Mohalla/Meshes/SM_Prop_Kite_Spool_Charkhi.SM_Prop_Kite_Spool_Charkhi"));
			if (SpoolMesh && RooftopKiteTrigger->MeshComponent)
			{
				RooftopKiteTrigger->MeshComponent->SetStaticMesh(SpoolMesh);
				RooftopKiteTrigger->MeshComponent->SetRelativeScale3D(FVector(0.6f, 0.6f, 0.6f));
			}

			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Mission Objective: Rooftop Kite Survey at (240, 320, 410)."));
		}

		// Objective Trigger: Vernacular Middle School Central Iron Bell Tower
		AObjectiveTriggerActor* SchoolBellTrigger = World->SpawnActor<AObjectiveTriggerActor>(
			AObjectiveTriggerActor::StaticClass(),
			FVector(1350.0f, 1350.0f, 60.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			TriggerSpawnParams
		);
		if (SchoolBellTrigger)
		{
			SchoolBellTrigger->RequiredMissionStage = ECourierMissionStage::Stage_Morning_SchoolBell;
			SchoolBellTrigger->InteractionPrompt = FText::FromString(TEXT("Ring Morning School Bell"));
			SchoolBellTrigger->ItemTitle = FText::FromString(TEXT("Wrought Iron Bell Tower"));
			SchoolBellTrigger->HistoricalLoreUponInteraction = FText::FromString(
				TEXT("Kabir pulls the hemp rope. The bronze bell clatters across the brick courtyards of Kot Gurdarshan, heralding morning classes for Headmaster Pandit Kashi Ram. Knowledge is the one weapon no colonial edict can take away.")
			);
			SchoolBellTrigger->bHideMeshOnTrigger = false;

			USoundBase* BellSFX = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Dawn_Temple_Bell.SFX_Dawn_Temple_Bell"));
			if (BellSFX)
			{
				SchoolBellTrigger->TriggerSound = BellSFX;
			}

			UStaticMesh* BellMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Game/Environment/Mohalla/Meshes/SM_School_Bell_Tower_Iron.SM_School_Bell_Tower_Iron"));
			if (BellMesh && SchoolBellTrigger->MeshComponent)
			{
				SchoolBellTrigger->MeshComponent->SetStaticMesh(BellMesh);
				SchoolBellTrigger->MeshComponent->SetRelativeScale3D(FVector(0.4f, 0.4f, 0.4f));
			}

			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Mission Objective: School Bell Tower at (1350, 1350, 60)."));
		}

		// Objective Trigger: Classroom 4B Student Desk & Slate
		AObjectiveTriggerActor* DeskTrigger = World->SpawnActor<AObjectiveTriggerActor>(
			AObjectiveTriggerActor::StaticClass(),
			FVector(1150.0f, 1850.0f, 35.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			TriggerSpawnParams
		);
		if (DeskTrigger)
		{
			DeskTrigger->RequiredMissionStage = ECourierMissionStage::Stage_Morning_ClassroomDesk;
			DeskTrigger->InteractionPrompt = FText::FromString(TEXT("Take Student Desk"));
			DeskTrigger->ItemTitle = FText::FromString(TEXT("Classroom 4B Student Bench"));
			DeskTrigger->HistoricalLoreUponInteraction = FText::FromString(
				TEXT("Kabir sits at the wooden desk and sets down his slate. Through the open archway, elders whisper of the town-wide Hartal. The morning errands are done; the seeds of freedom are planted. Act I prologue complete.")
			);
			DeskTrigger->bHideMeshOnTrigger = false;
			DeskTrigger->bTriggerCinematicSequence = true;
			DeskTrigger->CinematicChapterTitle = FText::FromString(TEXT("ACT II: THE GATHERING STORM"));
			DeskTrigger->CinematicSubtitle = FText::FromString(TEXT("Amritsar, April 13, 1919 — Afternoon nagara drums echo across Kot Gurdarshan as British town criers beat the Munadi, announcing General Dyer's proclamation banning all assemblies."));

			USoundBase* GongSFX = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Dawn_Gong_Complete.SFX_Dawn_Gong_Complete"));
			if (GongSFX)
			{
				DeskTrigger->TriggerSound = GongSFX;
			}

			UStaticMesh* DeskMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Game/Environment/Mohalla/Meshes/SM_School_Desk_Bench_Wood.SM_School_Desk_Bench_Wood"));
			if (DeskMesh && DeskTrigger->MeshComponent)
			{
				DeskTrigger->MeshComponent->SetStaticMesh(DeskMesh);
				DeskTrigger->MeshComponent->SetRelativeScale3D(FVector(0.5f, 0.5f, 0.5f));
			}

			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Mission Objective: Classroom 4B Student Desk at (1150, 1850, 35)."));
		}

		// Objective Trigger: General Dyer's Munadi Proclamation Drum (Grand Bazaar Chowk)
		AObjectiveTriggerActor* MunadiDrumTrigger = World->SpawnActor<AObjectiveTriggerActor>(
			AObjectiveTriggerActor::StaticClass(),
			FVector(80.0f, 1920.0f, 50.0f),
			FRotator(0.0f, -30.0f, 0.0f),
			TriggerSpawnParams
		);
		if (MunadiDrumTrigger)
		{
			MunadiDrumTrigger->RequiredMissionStage = ECourierMissionStage::Stage_Afternoon_MunadiProclamation;
			MunadiDrumTrigger->InteractionPrompt = FText::FromString(TEXT("Hear General Dyer's Proclamation"));
			MunadiDrumTrigger->ItemTitle = FText::FromString(TEXT("General Dyer's Curfew Proclamation (Munadi)"));
			MunadiDrumTrigger->HistoricalLoreUponInteraction = FText::FromString(
				TEXT("On the morning of April 13, 1919, British town criers beat nagara drums across Amritsar, reading General Dyer's proclamation banning all public assemblies under martial law. Most citizens in the bazaars and visiting villagers never heard it.")
			);
			MunadiDrumTrigger->bHideMeshOnTrigger = false;

			USoundBase* DrumSFX = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Munadi_Drum.SFX_Munadi_Drum"));
			if (DrumSFX)
			{
				MunadiDrumTrigger->TriggerSound = DrumSFX;
			}

			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Mission Objective: Munadi Proclamation Drum at (80, 1920, 50)."));
		}

		// Objective Trigger: The Historic Narrow Gateway of Jallianwala Bagh
		AObjectiveTriggerActor* JallianwalaGateTrigger = World->SpawnActor<AObjectiveTriggerActor>(
			AObjectiveTriggerActor::StaticClass(),
			FVector(900.0f, 2250.0f, 50.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			TriggerSpawnParams
		);
		if (JallianwalaGateTrigger)
		{
			JallianwalaGateTrigger->RequiredMissionStage = ECourierMissionStage::Stage_Afternoon_BaghNarrowEntry;
			JallianwalaGateTrigger->InteractionPrompt = FText::FromString(TEXT("Enter Jallianwala Bagh Passage"));
			JallianwalaGateTrigger->ItemTitle = FText::FromString(TEXT("The Historic Choke-Point of Jallianwala Bagh"));
			JallianwalaGateTrigger->HistoricalLoreUponInteraction = FText::FromString(
				TEXT("The entrance to Jallianwala Bagh was an extraordinarily narrow alley, barely 2.2 meters wide between high brick haveli walls. Over 20,000 peaceful men, women, and children have gathered for the Baisakhi festival and peaceful assembly. Unbeknownst to them, General Dyer's troops are marching toward this choke-point.")
			);
			JallianwalaGateTrigger->bHideMeshOnTrigger = false;

			USoundBase* CrowdSFX = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Baisakhi_Crowd_Murmur.SFX_Baisakhi_Crowd_Murmur"));
			if (CrowdSFX)
			{
				JallianwalaGateTrigger->TriggerSound = CrowdSFX;
			}

			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Mission Objective: Jallianwala Narrow Gateway at (900, 2250, 50)."));
		}

		// Objective Trigger: The Martyrs' Well (Shahidi Kua)
		AObjectiveTriggerActor* ShahidiWellTrigger = World->SpawnActor<AObjectiveTriggerActor>(
			AObjectiveTriggerActor::StaticClass(),
			FVector(1200.0f, 2950.0f, 50.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			TriggerSpawnParams
		);
		if (ShahidiWellTrigger)
		{
			ShahidiWellTrigger->RequiredMissionStage = ECourierMissionStage::Stage_ActII_BaisakhiGathering;
			ShahidiWellTrigger->InteractionPrompt = FText::FromString(TEXT("Examine the Martyrs' Well (Shahidi Kua)"));
			ShahidiWellTrigger->ItemTitle = FText::FromString(TEXT("The Martyrs' Well (Shahidi Kua)"));
			ShahidiWellTrigger->HistoricalLoreUponInteraction = FText::FromString(
				TEXT("A deep brick masonry well in the northern quadrangle of Jallianwala Bagh. When the 9th Bhopal and Gurkha rifles opened fire on the trapped crowd without warning, hundreds jumped into the narrow shaft to escape the hail of bullets. Over 120 bodies were later recovered from its depths.")
			);
			ShahidiWellTrigger->bHideMeshOnTrigger = false;

			USoundBase* MarchSFX = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Military_Boot_March.SFX_Military_Boot_March"));
			if (MarchSFX)
			{
				ShahidiWellTrigger->TriggerSound = MarchSFX;
			}

			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Mission Objective: Shahidi Kua Martyrs' Well at (1200, 2950, 50)."));
		}

		// Objective Trigger: The Peaceful Assembly Pandal & Speakers Dais
		AObjectiveTriggerActor* PandalTrigger = World->SpawnActor<AObjectiveTriggerActor>(
			AObjectiveTriggerActor::StaticClass(),
			FVector(1450.0f, 3100.0f, 50.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			TriggerSpawnParams
		);
		if (PandalTrigger)
		{
			PandalTrigger->RequiredMissionStage = ECourierMissionStage::Stage_ActII_BaisakhiGathering;
			PandalTrigger->InteractionPrompt = FText::FromString(TEXT("Listen to Assembly Speakers"));
			PandalTrigger->ItemTitle = FText::FromString(TEXT("The Peaceful Baisakhi Assembly Dais"));
			PandalTrigger->HistoricalLoreUponInteraction = FText::FromString(
				TEXT("On April 13, 1919, over 20,000 citizens from across Punjab gathered peacefully in this walled garden. Speakers peacefully passed resolutions demanding the repeal of the Rowlatt Act and the release of arrested leaders Dr. Saifuddin Kitchlew and Dr. Satyapal, unaware that General Dyer had blocked the sole exit.")
			);
			PandalTrigger->bHideMeshOnTrigger = false;

			USoundBase* RallySFX = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Crowd_Rally_Speech.SFX_Crowd_Rally_Speech"));
			if (RallySFX)
			{
				PandalTrigger->TriggerSound = RallySFX;
			}

			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Mission Objective: Baisakhi Pandal Dais at (1450, 3100, 50)."));
		}

		// Objective Trigger: General Dyer Orders Fire (Bugle Call & Rifle Firing Line)
		AObjectiveTriggerActor* TheFiringTrigger = World->SpawnActor<AObjectiveTriggerActor>(
			AObjectiveTriggerActor::StaticClass(),
			FVector(1250.0f, 2800.0f, 50.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			TriggerSpawnParams
		);
		if (TheFiringTrigger)
		{
			TheFiringTrigger->RequiredMissionStage = ECourierMissionStage::Stage_ActII_TheFiring;
			TheFiringTrigger->InteractionPrompt = FText::FromString(TEXT("Hear Dyer's Firing Command"));
			TheFiringTrigger->ItemTitle = FText::FromString(TEXT("The Orders of General Dyer (April 13, 1919)"));
			TheFiringTrigger->HistoricalLoreUponInteraction = FText::FromString(
				TEXT("Without giving any warning to disperse, Brigadier-General Reginald Dyer deployed 50 Gurkha and Baluch riflemen across the raised bank at the narrow mouth of Jallianwala Bagh. A sharp bugle call echoed across the garden, followed instantly by the deafening crack of .303 Lee-Enfield volleys. The crowd had no way to escape through the blocked gateway.")
			);
			TheFiringTrigger->bHideMeshOnTrigger = false;

			USoundBase* BugleSFX = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Bugle_Call_Charge.SFX_Bugle_Call_Charge"));
			if (BugleSFX)
			{
				TheFiringTrigger->TriggerSound = BugleSFX;
			}

			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Mission Objective: The Firing Trigger at (1250, 2800, 50)."));
		}

		// Objective Trigger: Panic in the Enclosure & Stampede Debris
		AObjectiveTriggerActor* FindEscapeTrigger = World->SpawnActor<AObjectiveTriggerActor>(
			AObjectiveTriggerActor::StaticClass(),
			FVector(950.0f, 3100.0f, 50.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			TriggerSpawnParams
		);
		if (FindEscapeTrigger)
		{
			FindEscapeTrigger->RequiredMissionStage = ECourierMissionStage::Stage_ActII_FindEscapeRoute;
			FindEscapeTrigger->InteractionPrompt = FText::FromString(TEXT("Evade Stampede and Seek Escape"));
			FindEscapeTrigger->ItemTitle = FText::FromString(TEXT("Panic in the Trapped Enclosure"));
			FindEscapeTrigger->HistoricalLoreUponInteraction = FText::FromString(
				TEXT("As rifle fire tore into the dense crowd, sheer pandemonium erupted. Desperate mothers, fathers, and children ran in waves toward the 5-meter blind haveli walls, only to find them insurmountable. Hundreds of turbans and shoes were lost in the stampede. Kabir must keep his footing and search for a damaged low wall section.")
			);
			FindEscapeTrigger->bHideMeshOnTrigger = false;

			USoundBase* PanicSFX = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Crowd_Panic_Scream.SFX_Crowd_Panic_Scream"));
			if (PanicSFX)
			{
				FindEscapeTrigger->TriggerSound = PanicSFX;
			}

			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Mission Objective: Find Escape Route Trigger at (950, 3100, 50)."));
		}

		// Objective Trigger: Vault the Crumbling Wall Breach
		AObjectiveTriggerActor* VaultBreachTrigger = World->SpawnActor<AObjectiveTriggerActor>(
			AObjectiveTriggerActor::StaticClass(),
			FVector(680.0f, 3320.0f, 50.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			TriggerSpawnParams
		);
		if (VaultBreachTrigger)
		{
			VaultBreachTrigger->RequiredMissionStage = ECourierMissionStage::Stage_ActII_VaultWallBreach;
			VaultBreachTrigger->InteractionPrompt = FText::FromString(TEXT("Vault Crumbling Wall Breach"));
			VaultBreachTrigger->ItemTitle = FText::FromString(TEXT("The Crumbling Boundary Wall Breach"));
			VaultBreachTrigger->HistoricalLoreUponInteraction = FText::FromString(
				TEXT("A damaged 1.8-meter low section of rear haveli brickwork with collapsed rubble beneath offers a slender chance of survival. With a burst of agility, 12-year-old Kabir scrambles up the fallen bricks, grabs the fractured coping ledge, and vaults over into the adjoining back alleyways of Amritsar, surviving the massacre.")
			);
			VaultBreachTrigger->bHideMeshOnTrigger = false;

			USoundBase* CompleteSFX = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Dawn_Gong_Complete.SFX_Dawn_Gong_Complete"));
			if (CompleteSFX)
			{
				VaultBreachTrigger->TriggerSound = CompleteSFX;
			}

			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Mission Objective: Vault Breach Trigger at (680, 3320, 50)."));
		}

		// Objective Trigger: Martial Law Curfew Notice (Act III Step 16)
		AObjectiveTriggerActor* CurfewNoticeTrigger = World->SpawnActor<AObjectiveTriggerActor>(
			AObjectiveTriggerActor::StaticClass(),
			FVector(-80.0f, 1850.0f, 50.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			TriggerSpawnParams
		);
		if (CurfewNoticeTrigger)
		{
			CurfewNoticeTrigger->RequiredMissionStage = ECourierMissionStage::Stage_ActIII_NightCurfewFall;
			CurfewNoticeTrigger->InteractionPrompt = FText::FromString(TEXT("Examine Martial Law Curfew Notice"));
			CurfewNoticeTrigger->ItemTitle = FText::FromString(TEXT("General Dyer's 8:00 PM Curfew Proclamation"));
			CurfewNoticeTrigger->HistoricalLoreUponInteraction = FText::FromString(
				TEXT("Following the firing at Jallianwala Bagh, General Dyer clamped an inflexible 8:00 PM curfew upon Amritsar. Any citizen found outside their home was liable to be shot on sight. Mothers and fathers were prohibited from searching for their wounded and dying children overnight in the dark garden.")
			);
			CurfewNoticeTrigger->bHideMeshOnTrigger = false;

			USoundBase* WhistleSFX = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Police_Whistle_Curfew.SFX_Police_Whistle_Curfew"));
			if (WhistleSFX)
			{
				CurfewNoticeTrigger->TriggerSound = WhistleSFX;
			}

			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Mission Objective: Curfew Notice Trigger at (-80, 1850, 50)."));
		}

		// Objective Trigger: Evade Searchlight Picket (Act III Step 17)
		AObjectiveTriggerActor* SearchlightPicketTrigger = World->SpawnActor<AObjectiveTriggerActor>(
			AObjectiveTriggerActor::StaticClass(),
			FVector(0.0f, 2260.0f, 50.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			TriggerSpawnParams
		);
		if (SearchlightPicketTrigger)
		{
			SearchlightPicketTrigger->RequiredMissionStage = ECourierMissionStage::Stage_ActIII_EvadeSearchlightPicket;
			SearchlightPicketTrigger->InteractionPrompt = FText::FromString(TEXT("Slip Past Searchlight Picket"));
			SearchlightPicketTrigger->ItemTitle = FText::FromString(TEXT("Imperial Carbon-Arc Searchlight Picket"));
			SearchlightPicketTrigger->HistoricalLoreUponInteraction = FText::FromString(
				TEXT("High-intensity carbon-arc searchlights mounted on heavy iron tripods illuminated key intersections and sandbag bunkers. Young couriers used knowledge of narrow covered mohalla alleys and rooftop blind spots to slip past the illuminated sweep cones.")
			);
			SearchlightPicketTrigger->bHideMeshOnTrigger = false;

			USoundBase* MarchSFX = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Military_Boot_March.SFX_Military_Boot_March"));
			if (MarchSFX)
			{
				SearchlightPicketTrigger->TriggerSound = MarchSFX;
			}

			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Mission Objective: Searchlight Picket Trigger at (0, 2260, 50)."));
		}

		// Objective Trigger: Aid Wounded Survivors with Makeshift Stretcher (Act III Step 18)
		AObjectiveTriggerActor* SecretStretcherClinicTrigger = World->SpawnActor<AObjectiveTriggerActor>(
			AObjectiveTriggerActor::StaticClass(),
			FVector(-120.0f, 950.0f, 50.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			TriggerSpawnParams
		);
		if (SecretStretcherClinicTrigger)
		{
			SecretStretcherClinicTrigger->RequiredMissionStage = ECourierMissionStage::Stage_ActIII_AidWoundedSurvivors;
			SecretStretcherClinicTrigger->InteractionPrompt = FText::FromString(TEXT("Deliver First Aid to Stretcher"));
			SecretStretcherClinicTrigger->ItemTitle = FText::FromString(TEXT("Makeshift Stretcher & Clandestine Medical Relief"));
			SecretStretcherClinicTrigger->HistoricalLoreUponInteraction = FText::FromString(
				TEXT("Defying the mortal danger of the martial law curfew, Amritsar residents like Ratan Devi crept through dark kucha alleys to carry water and bandages to survivors. Makeshift woven charpais served as stretchers to carry the injured into secret community shelters.")
			);
			SecretStretcherClinicTrigger->bHideMeshOnTrigger = false;

			USoundBase* CompleteSFX = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Dawn_Gong_Complete.SFX_Dawn_Gong_Complete"));
			if (CompleteSFX)
			{
				SecretStretcherClinicTrigger->TriggerSound = CompleteSFX;
			}

			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Mission Objective: Secret Stretcher Clinic Trigger at (-120, 950, 50)."));
		}

		// Objective Trigger: Canal Sluice Regulator (Act IV Step 20)
		AObjectiveTriggerActor* CanalAqueductTrigger = World->SpawnActor<AObjectiveTriggerActor>(
			AObjectiveTriggerActor::StaticClass(),
			FVector(-950.0f, 2200.0f, 50.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			TriggerSpawnParams
		);
		if (CanalAqueductTrigger)
		{
			CanalAqueductTrigger->RequiredMissionStage = ECourierMissionStage::Stage_ActIV_ReachCanalDistributary;
			CanalAqueductTrigger->InteractionPrompt = FText::FromString(TEXT("Inspect Canal Sluice Regulator"));
			CanalAqueductTrigger->ItemTitle = FText::FromString(TEXT("Upper Bari Doab Canal Distributary"));
			CanalAqueductTrigger->HistoricalLoreUponInteraction = FText::FromString(
				TEXT("Engineered as part of the extensive British canal irrigation network across Punjab, the Upper Bari Doab distributary channels brought life to agricultural fields. For independence couriers, its masonry bridges and stone sluice banks served as critical escape routes beyond urban cordons.")
			);
			CanalAqueductTrigger->bHideMeshOnTrigger = false;

			USoundBase* WaterSFX = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Canal_Water_Flow_Gentle.SFX_Canal_Water_Flow_Gentle"));
			if (WaterSFX)
			{
				CanalAqueductTrigger->TriggerSound = WaterSFX;
			}

			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Mission Objective: Canal Aqueduct Trigger at (-950, 2200, 50)."));
		}

		// Objective Trigger: Persian Wheel Rahat (Act IV Step 21)
		AObjectiveTriggerActor* PersianWheelTrigger = World->SpawnActor<AObjectiveTriggerActor>(
			AObjectiveTriggerActor::StaticClass(),
			FVector(-1150.0f, 2050.0f, 50.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			TriggerSpawnParams
		);
		if (PersianWheelTrigger)
		{
			PersianWheelTrigger->RequiredMissionStage = ECourierMissionStage::Stage_ActIV_PersianWheelContact;
			PersianWheelTrigger->InteractionPrompt = FText::FromString(TEXT("Meet Contact at Persian Wheel (Rahat)"));
			PersianWheelTrigger->ItemTitle = FText::FromString(TEXT("The Punjabi Rahat (Persian Wheel Well)"));
			PersianWheelTrigger->HistoricalLoreUponInteraction = FText::FromString(
				TEXT("The traditional Rahat has irrigated Punjabi soil for centuries, using bullocks circling a geared timber crown wheel to lift chains of clay water pots. Rural farmers sympathetic to the anti-colonial cause used its continuous wooden groans and water cascades to mask clandestine exchanges.")
			);
			PersianWheelTrigger->bHideMeshOnTrigger = false;

			USoundBase* RahatSFX = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Persian_Wheel_Rahat_Creak.SFX_Persian_Wheel_Rahat_Creak"));
			if (RahatSFX)
			{
				PersianWheelTrigger->TriggerSound = RahatSFX;
			}

			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Mission Objective: Persian Wheel Trigger at (-1150, 2050, 50)."));
		}

		// Objective Trigger: Brick Kiln Resistance Cache (Act IV Step 22)
		AObjectiveTriggerActor* BrickKilnCacheTrigger = World->SpawnActor<AObjectiveTriggerActor>(
			AObjectiveTriggerActor::StaticClass(),
			FVector(-1180.0f, 2520.0f, 50.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			TriggerSpawnParams
		);
		if (BrickKilnCacheTrigger)
		{
			BrickKilnCacheTrigger->RequiredMissionStage = ECourierMissionStage::Stage_ActIV_BrickKilnSafehouse;
			BrickKilnCacheTrigger->InteractionPrompt = FText::FromString(TEXT("Secure Resistance Safe Cache"));
			BrickKilnCacheTrigger->ItemTitle = FText::FromString(TEXT("The Bhatta Brick Kiln Resistance Stash"));
			BrickKilnCacheTrigger->HistoricalLoreUponInteraction = FText::FromString(
				TEXT("Bull's trench brick kilns on the rural outskirts provided perfect industrial hideouts. Tucked beneath weathered burlap tarpaulins and drying brick hacks, couriers stored lithographed pamphlets, ink supplies, and bicycles to connect village freedom fighters with town centers.")
			);
			BrickKilnCacheTrigger->bHideMeshOnTrigger = false;

			USoundBase* CompleteSFX = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Dawn_Gong_Complete.SFX_Dawn_Gong_Complete"));
			if (CompleteSFX)
			{
				BrickKilnCacheTrigger->TriggerSound = CompleteSFX;
			}

			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Mission Objective: Brick Kiln Cache Trigger at (-1180, 2520, 50)."));
		}

		// Objective Trigger: Railway Overpass (Act V Step 24)
		AObjectiveTriggerActor* RailwayOverpassTrigger = World->SpawnActor<AObjectiveTriggerActor>(
			AObjectiveTriggerActor::StaticClass(),
			FVector(900.0f, 3900.0f, 50.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			TriggerSpawnParams
		);
		if (RailwayOverpassTrigger)
		{
			RailwayOverpassTrigger->RequiredMissionStage = ECourierMissionStage::Stage_ActV_ReachRailwayCutting;
			RailwayOverpassTrigger->InteractionPrompt = FText::FromString(TEXT("Scout Railway Cutting"));
			RailwayOverpassTrigger->ItemTitle = FText::FromString(TEXT("The North Western Railway Cutting"));
			RailwayOverpassTrigger->HistoricalLoreUponInteraction = FText::FromString(
				TEXT("Constructed by the colonial Public Works Department, the North Western Railway broad-gauge tracks formed a rigid physical and social barrier dividing indigenous walled towns from European Civil Lines. Under martial law, military steam locomotives patrolled the tracks.")
			);
			RailwayOverpassTrigger->bHideMeshOnTrigger = false;

			USoundBase* TrainSFX = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Steam_Locomotive_Idling.SFX_Steam_Locomotive_Idling"));
			if (TrainSFX)
			{
				RailwayOverpassTrigger->TriggerSound = TrainSFX;
			}

			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Mission Objective: Railway Overpass Trigger at (900, 3900, 50)."));
		}

		// Objective Trigger: Semaphore Signal Gantry (Act V Step 25)
		AObjectiveTriggerActor* SignalGantryTrigger = World->SpawnActor<AObjectiveTriggerActor>(
			AObjectiveTriggerActor::StaticClass(),
			FVector(1160.0f, 3960.0f, 50.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			TriggerSpawnParams
		);
		if (SignalGantryTrigger)
		{
			SignalGantryTrigger->RequiredMissionStage = ECourierMissionStage::Stage_ActV_ClimbSignalGantry;
			SignalGantryTrigger->InteractionPrompt = FText::FromString(TEXT("Shift Railway Semaphore Lever"));
			SignalGantryTrigger->ItemTitle = FText::FromString(TEXT("The Junction Semaphore Signal Gantry"));
			SignalGantryTrigger->HistoricalLoreUponInteraction = FText::FromString(
				TEXT("Standing 6.5 meters tall, the lattice iron semaphore tower controlled broad-gauge troop and freight movements. By shifting the mechanical counterbalance lever, couriers altered junction signals to divert colonial military transport trains.")
			);
			SignalGantryTrigger->bHideMeshOnTrigger = false;

			USoundBase* BellSFX = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Railway_Signal_Bell.SFX_Railway_Signal_Bell"));
			if (BellSFX)
			{
				SignalGantryTrigger->TriggerSound = BellSFX;
			}

			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Mission Objective: Semaphore Signal Gantry Trigger at (1160, 3960, 50)."));
		}

		// Objective Trigger: Civil Lines Palisade Perimeter (Act V Step 26)
		AObjectiveTriggerActor* CivilLinesPalisadeTrigger = World->SpawnActor<AObjectiveTriggerActor>(
			AObjectiveTriggerActor::StaticClass(),
			FVector(900.0f, 4200.0f, 50.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			TriggerSpawnParams
		);
		if (CivilLinesPalisadeTrigger)
		{
			CivilLinesPalisadeTrigger->RequiredMissionStage = ECourierMissionStage::Stage_ActV_CrossCivilLinesPalisade;
			CivilLinesPalisadeTrigger->InteractionPrompt = FText::FromString(TEXT("Breach Civil Lines Palisade"));
			CivilLinesPalisadeTrigger->ItemTitle = FText::FromString(TEXT("The Segregated Cantonment Perimeter"));
			CivilLinesPalisadeTrigger->HistoricalLoreUponInteraction = FText::FromString(
				TEXT("Cast-iron spearhead palisades separated the colonial club and administrative cantonment from Indian citizens. Slipping through this boundary marked the culmination of Kabir's courier journey, carrying the unified demands of the people into the imperial administration.")
			);
			CivilLinesPalisadeTrigger->bHideMeshOnTrigger = false;

			USoundBase* CompleteSFX = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Dawn_Gong_Complete.SFX_Dawn_Gong_Complete"));
			if (CompleteSFX)
			{
				CivilLinesPalisadeTrigger->TriggerSound = CompleteSFX;
			}

			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Mission Objective: Civil Lines Palisade Trigger at (900, 4200, 50)."));
		}

		// Objective Trigger: Cantonment Veranda Archive Cabinet (Act V Climax Infiltration)
		AObjectiveTriggerActor* CantonmentArchiveTrigger = World->SpawnActor<AObjectiveTriggerActor>(
			AObjectiveTriggerActor::StaticClass(),
			FVector(820.0f, 4520.0f, 75.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			TriggerSpawnParams
		);
		if (CantonmentArchiveTrigger)
		{
			CantonmentArchiveTrigger->RequiredMissionStage = ECourierMissionStage::Stage_Completed;
			CantonmentArchiveTrigger->InteractionPrompt = FText::FromString(TEXT("Secure Clandestine Imperial Dispatches"));
			CantonmentArchiveTrigger->ItemTitle = FText::FromString(TEXT("The Clandestine Telegraph Dispatches"));
			CantonmentArchiveTrigger->HistoricalLoreUponInteraction = FText::FromString(
				TEXT("Intercepted telegraph cables between the Deputy Commissioner of Amritsar and the Punjab Secretariat in Lahore reveal the military's suppression of press reporting and the truth of the April 1919 uprising. Securing these dispatches ensures the sacrifice of Kot Gurdarshan can never be forgotten.")
			);
			CantonmentArchiveTrigger->bHideMeshOnTrigger = false;

			USoundBase* TelegraphSFX = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Telegraph_Chirp_Ticker.SFX_Telegraph_Chirp_Ticker"));
			if (TelegraphSFX)
			{
				CantonmentArchiveTrigger->TriggerSound = TelegraphSFX;
			}

			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Mission Objective: Cantonment Veranda Archive Trigger at (820, 4520, 75)."));
		}

		// Locomotive Boiler Steam Pressure Relief Valve (Hitman / Batman Arkham benchmark)
		FActorSpawnParameters SteamValveParams;
		SteamValveParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		ALocomotiveSteamValveActor* SteamValve = World->SpawnActor<ALocomotiveSteamValveActor>(
			ALocomotiveSteamValveActor::StaticClass(),
			FVector(1000.0f, 3880.0f, 90.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			SteamValveParams
		);
		if (SteamValve)
		{
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned LocomotiveSteamValveActor on boiler at (1000, 3880, 90)."));
		}

		// Cantonment Gate Sentinel (Punjab Imperial Police Picket)
		FActorSpawnParameters SentrySpawnParams;
		SentrySpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		ACurfewPatrolAI* CantonmentSentry = World->SpawnActor<ACurfewPatrolAI>(
			ACurfewPatrolAI::StaticClass(),
			FVector(650.0f, 4220.0f, 10.0f),
			FRotator(0.0f, -90.0f, 0.0f),
			SentrySpawnParams
		);
		if (CantonmentSentry)
		{
			CantonmentSentry->WatchmanTitle = FText::FromString(TEXT("Punjab Imperial Police Cantonment Sentinel"));
			CantonmentSentry->PatrolWaypoints.Empty();
			CantonmentSentry->PatrolWaypoints.Add(FVector(650.0f, 4220.0f, 10.0f)); // Guardhouse picket
			CantonmentSentry->PatrolWaypoints.Add(FVector(800.0f, 4220.0f, 10.0f)); // Civil lines gate
			CantonmentSentry->PatrolWaypoints.Add(FVector(950.0f, 4220.0f, 10.0f)); // Palisade perimeter
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Cantonment Sentinel at (650, 4220, 10)."));
		}
	}

	// 4. Ensure Dynamic Atmosphere Controller exists for Curfew Night-to-Dawn Transition
	int32 ExistingAtmosphere = 0;
	for (TActorIterator<ARevolutionAtmosphereController> It(World); It; ++It)
	{
		ExistingAtmosphere++;
	}

	if (ExistingAtmosphere == 0)
	{
		FActorSpawnParameters AtmoSpawnParams;
		AtmoSpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

		ARevolutionAtmosphereController* Atmosphere = World->SpawnActor<ARevolutionAtmosphereController>(
			ARevolutionAtmosphereController::StaticClass(),
			FVector::ZeroVector,
			FRotator::ZeroRotator,
			AtmoSpawnParams
		);
		if (Atmosphere)
		{
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned RevolutionAtmosphereController for dynamic Curfew-to-Dawn lighting."));
		}
	}

	// 5. Spawn Environmental Hiding Spots (Jute sack barricades & Haveli deorhi alcove)
	int32 ExistingHidingSpots = 0;
	for (TActorIterator<AHidingSpotActor> It(World); It; ++It)
	{
		ExistingHidingSpots++;
	}

	if (ExistingHidingSpots == 0)
	{
		FActorSpawnParameters HidingSpawnParams;
		HidingSpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

		// Hiding Spot 1: Alley corner jute ration sacks
		AHidingSpotActor* Spot1 = World->SpawnActor<AHidingSpotActor>(
			AHidingSpotActor::StaticClass(),
			FVector(-175.0f, 155.0f, 10.0f),
			FRotator(0.0f, 45.0f, 0.0f),
			HidingSpawnParams
		);
		if (Spot1)
		{
			Spot1->SpotName = FText::FromString(TEXT("Jute Ration Sacks Stack"));
			Spot1->ConcealPrompt = FText::FromString(TEXT("Crouch Behind Sacks"));
			Spot1->ExitPrompt = FText::FromString(TEXT("Emerge From Sacks"));
			if (Spot1->CoverMesh)
			{
				Spot1->CoverMesh->SetRelativeScale3D(FVector(1.1f, 1.1f, 1.0f));
			}
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Environmental Hiding Spot 1 (Jute Sacks) at (-175, 155, 10)."));
		}

		// Hiding Spot 2: Deorhi threshold shadow alcove
		AHidingSpotActor* Spot2 = World->SpawnActor<AHidingSpotActor>(
			AHidingSpotActor::StaticClass(),
			FVector(-45.0f, -220.0f, 10.0f),
			FRotator(0.0f, -90.0f, 0.0f),
			HidingSpawnParams
		);
		if (Spot2)
		{
			Spot2->SpotName = FText::FromString(TEXT("Haveli Deorhi Shadow Alcove"));
			Spot2->ConcealPrompt = FText::FromString(TEXT("Conceal in Archway Shadow"));
			Spot2->ExitPrompt = FText::FromString(TEXT("Step Out of Shadow"));
			if (Spot2->CoverMesh)
			{
				Spot2->CoverMesh->SetRelativeScale3D(FVector(0.9f, 0.9f, 1.2f));
			}
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Environmental Hiding Spot 2 (Deorhi Alcove) at (-45, -220, 10)."));
		}
	}

	// 6. Spawn Interactive Haveli Deorhi Door with Iron Kundi Latch
	int32 ExistingDoors = 0;
	for (TActorIterator<ADoorDeorhiActor> DoorIt(World); DoorIt; ++DoorIt)
	{
		ExistingDoors++;
	}

	if (ExistingDoors == 0)
	{
		FActorSpawnParameters DoorSpawnParams;
		DoorSpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

		ADoorDeorhiActor* DeorhiDoor = World->SpawnActor<ADoorDeorhiActor>(
			ADoorDeorhiActor::StaticClass(),
			FVector(-20.0f, -240.0f, 10.0f),
			FRotator(0.0f, 90.0f, 0.0f),
			DoorSpawnParams
		);
		if (DeorhiDoor)
		{
			DeorhiDoor->bIsBolted = true;
			DeorhiDoor->bIsOpen = false;
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Interactive Deorhi Door with Iron Kundi at (-20, -240, 10)."));
		}
	}

	// 7. Spawn Haveli Rooftop Pigeon Flock (Kabootar)
	int32 ExistingFlocks = 0;
	for (TActorIterator<APigeonFlockActor> FlockIt(World); FlockIt; ++FlockIt)
	{
		ExistingFlocks++;
	}

	if (ExistingFlocks == 0)
	{
		FActorSpawnParameters FlockSpawnParams;
		FlockSpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

		APigeonFlockActor* RooftopFlock = World->SpawnActor<APigeonFlockActor>(
			APigeonFlockActor::StaticClass(),
			FVector(0.0f, 255.0f, 435.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			FlockSpawnParams
		);
		if (RooftopFlock)
		{
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Haveli Rooftop Pigeon Flock at (0, 255, 435)."));
		}
	}

	// 8. Spawn Haveli Low Drain Crawlway (Mori / Parnala Arch)
	int32 ExistingCrawlways = 0;
	for (TActorIterator<ACrawlSpaceActor> CrawlIt(World); CrawlIt; ++CrawlIt)
	{
		ExistingCrawlways++;
	}

	if (ExistingCrawlways == 0)
	{
		FActorSpawnParameters CrawlSpawnParams;
		CrawlSpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

		ACrawlSpaceActor* DrainCrawlway = World->SpawnActor<ACrawlSpaceActor>(
			ACrawlSpaceActor::StaticClass(),
			FVector(-120.0f, 90.0f, 10.0f),
			FRotator(0.0f, 90.0f, 0.0f),
			CrawlSpawnParams
		);
		if (DrainCrawlway)
		{
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Haveli Low Drain Crawlway at (-120, 90, 10)."));
		}
	}

	// 9. Spawn Brittle Terracotta Roof Shingles & Broken Pottery Hazards (Khaprail)
	int32 ExistingHazards = 0;
	for (TActorIterator<ATerracottaHazardActor> HazIt(World); HazIt; ++HazIt)
	{
		ExistingHazards++;
	}

	if (ExistingHazards == 0)
	{
		FActorSpawnParameters HazSpawnParams;
		HazSpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

		// Hazard 1: Rooftop terrace shingle pile near parapet vault approach
		ATerracottaHazardActor* RoofHazard = World->SpawnActor<ATerracottaHazardActor>(
			ATerracottaHazardActor::StaticClass(),
			FVector(60.0f, -40.0f, 405.0f),
			FRotator(0.0f, 15.0f, 0.0f),
			HazSpawnParams
		);
		if (RoofHazard)
		{
			RoofHazard->HazardName = FText::FromString(TEXT("Rooftop Brittle Terracotta Shingles (Khaprail)"));
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Terracotta Hazard 1 (Rooftop Shingles) at (60, -40, 405)."));
		}

		// Hazard 2: Courtyard narrow passage broken earthen pots debris
		ATerracottaHazardActor* CourtyardHazard = World->SpawnActor<ATerracottaHazardActor>(
			ATerracottaHazardActor::StaticClass(),
			FVector(-80.0f, -110.0f, 10.0f),
			FRotator(0.0f, -30.0f, 0.0f),
			HazSpawnParams
		);
		if (CourtyardHazard)
		{
			CourtyardHazard->HazardName = FText::FromString(TEXT("Courtyard Broken Earthen Kulhad Shards"));
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Terracotta Hazard 2 (Courtyard Shards) at (-80, -110, 10)."));
		}
	}

	// 10. Spawn Historical Cast-Iron Courtyard Handpump (Nalka Acoustic Decoy)
	int32 ExistingHandpumps = 0;
	for (TActorIterator<AHandpumpActor> PumpIt(World); PumpIt; ++PumpIt)
	{
		ExistingHandpumps++;
	}

	if (ExistingHandpumps == 0)
	{
		FActorSpawnParameters PumpSpawnParams;
		PumpSpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

		AHandpumpActor* Handpump = World->SpawnActor<AHandpumpActor>(
			AHandpumpActor::StaticClass(),
			FVector(30.0f, 150.0f, 10.0f),
			FRotator(0.0f, -45.0f, 0.0f),
			PumpSpawnParams
		);
		if (Handpump)
		{
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Cast-Iron Courtyard Handpump (Nalka) at (30, 150, 10)."));
		}
	}

	// 11. Spawn Historical Rooftop Clothesline (Tangan / Sukhne Cloth Drying Line)
	int32 ExistingClotheslines = 0;
	for (TActorIterator<AClotheslineActor> LineIt(World); LineIt; ++LineIt)
	{
		ExistingClotheslines++;
	}

	if (ExistingClotheslines == 0)
	{
		FActorSpawnParameters LineSpawnParams;
		LineSpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

		AClotheslineActor* Clothesline = World->SpawnActor<AClotheslineActor>(
			AClotheslineActor::StaticClass(),
			FVector(-20.0f, 180.0f, 405.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			LineSpawnParams
		);
		if (Clothesline)
		{
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Rooftop Clothesline (Sukhne) at (-20, 180, 405)."));
		}
	}

	// 12. Spawn Historical Haveli Rooftop Roshandan (Lightwell / Ventilation Opening)
	int32 ExistingRoshandans = 0;
	for (TActorIterator<ARoshandanActor> RoshIt(World); RoshIt; ++RoshIt)
	{
		ExistingRoshandans++;
	}

	if (ExistingRoshandans == 0)
	{
		FActorSpawnParameters RoshSpawnParams;
		RoshSpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

		ARoshandanActor* Roshandan = World->SpawnActor<ARoshandanActor>(
			ARoshandanActor::StaticClass(),
			FVector(30.0f, 60.0f, 405.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			RoshSpawnParams
		);
		if (Roshandan)
		{
			Roshandan->DropTargetLocation = FVector(30.0f, 60.0f, 15.0f);
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Haveli Rooftop Roshandan at (30, 60, 405) with courtyard drop target (30, 60, 15)."));
		}
	}

	// 13. Spawn Historical Equipment Supply Stashes (Pebble Bowls & Tailor's Chalk Slabs)
	int32 ExistingStashes = 0;
	for (TActorIterator<ASupplyStashActor> StashIt(World); StashIt; ++StashIt)
	{
		ExistingStashes++;
	}

	if (ExistingStashes == 0)
	{
		FActorSpawnParameters StashSpawnParams;
		StashSpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

		// Stash 1: Tailor's Chalk Slabs in Father's Sewing Box near Courtyard Charpai
		ASupplyStashActor* ChalkStash = World->SpawnActor<ASupplyStashActor>(
			ASupplyStashActor::StaticClass(),
			FVector(145.0f, 150.0f, 12.0f),
			FRotator(0.0f, 25.0f, 0.0f),
			StashSpawnParams
		);
		if (ChalkStash)
		{
			ChalkStash->StashType = ESupplyStashType::Chalk;
			ChalkStash->ReplenishAmount = 3;
			ChalkStash->StashTitle = FText::FromString(TEXT("Father's Tailor Chalk Tin (Kharri Mitti)"));
			ChalkStash->LoreDescription = FText::FromString(
				TEXT("Triangular calcium-carbonate tailor's chalk biscuits imported through Karachi and Amritsar cloth mandis. Kabir's father drafts suit outlines with them, while Kabir uses them to leave clandestine scout runes on haveli doorposts.")
			);
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Supply Stash 1 (Tailor Chalk) at (145, 150, 12)."));
		}

		// Stash 2: Courtyard Clay Marbles Bowl near Handpump Stone Plinth
		ASupplyStashActor* PebbleStash1 = World->SpawnActor<ASupplyStashActor>(
			ASupplyStashActor::StaticClass(),
			FVector(45.0f, 130.0f, 12.0f),
			FRotator(0.0f, -15.0f, 0.0f),
			StashSpawnParams
		);
		if (PebbleStash1)
		{
			PebbleStash1->StashType = ESupplyStashType::Pebbles;
			PebbleStash1->ReplenishAmount = 2;
			PebbleStash1->StashTitle = FText::FromString(TEXT("Courtyard River Pebble Cache"));
			PebbleStash1->LoreDescription = FText::FromString(
				TEXT("Smooth, water-worn gravel gathered along canal banks. Used to create sharp acoustic clatter against brick alleyways to divert night watchmen away from haveli deorhi gates.")
			);
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Supply Stash 2 (Courtyard Pebbles) at (45, 130, 12)."));
		}

		// Stash 3: Rooftop Terrace Basant Clay Marble Cache near Parapet
		ASupplyStashActor* PebbleStash2 = World->SpawnActor<ASupplyStashActor>(
			ASupplyStashActor::StaticClass(),
			FVector(-40.0f, 220.0f, 405.0f),
			FRotator(0.0f, 45.0f, 0.0f),
			StashSpawnParams
		);
		if (PebbleStash2)
		{
			PebbleStash2->StashType = ESupplyStashType::Pebbles;
			PebbleStash2->ReplenishAmount = 2;
			PebbleStash2->StashTitle = FText::FromString(TEXT("Rooftop Clay Marble Cache"));
			PebbleStash2->LoreDescription = FText::FromString(
				TEXT("Sun-baked earthen marbles stashed by neighborhood boys behind the terrace parapet. Ideal for dropping through the rooftop Roshandan lightwell into the courtyard below.")
			);
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Supply Stash 3 (Rooftop Pebbles) at (-40, 220, 405)."));
		}
	}

	// 14. Spawn Historical British Proclamation Board (Section 144 Curfew Decree)
	int32 ExistingBoards = 0;
	for (TActorIterator<AProclamationBoardActor> BoardIt(World); BoardIt; ++BoardIt)
	{
		ExistingBoards++;
	}

	if (ExistingBoards == 0)
	{
		FActorSpawnParameters BoardSpawnParams;
		BoardSpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

		AProclamationBoardActor* Board = World->SpawnActor<AProclamationBoardActor>(
			AProclamationBoardActor::StaticClass(),
			FVector(-65.0f, -225.0f, 65.0f),
			FRotator(0.0f, 90.0f, 0.0f),
			BoardSpawnParams
		);
		if (Board)
		{
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Section 144 Proclamation Board on haveli gateway wall at (-65, -225, 65)."));
		}
	}

	// 15. Spawn Historical Clandestine Lithographic Press (Pathar di Chhapakhana)
	int32 ExistingPresses = 0;
	for (TActorIterator<ALithoPressActor> PressIt(World); PressIt; ++PressIt)
	{
		ExistingPresses++;
	}

	if (ExistingPresses == 0)
	{
		FActorSpawnParameters PressSpawnParams;
		PressSpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

		ALithoPressActor* Press = World->SpawnActor<ALithoPressActor>(
			ALithoPressActor::StaticClass(),
			FVector(115.0f, 185.0f, 10.0f),
			FRotator(0.0f, -90.0f, 0.0f),
			PressSpawnParams
		);
		if (Press)
		{
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Clandestine Lithographic Press in haveli cellar alcove at (115, 185, 10)."));
		}
	}

	// 16. Spawn Historical Mohalla Pariah Dog (Desi Kutta Vigilance Decoy)
	int32 ExistingDogs = 0;
	for (TActorIterator<APariahDogActor> DogIt(World); DogIt; ++DogIt)
	{
		ExistingDogs++;
	}

	if (ExistingDogs == 0)
	{
		FActorSpawnParameters DogSpawnParams;
		DogSpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

		APariahDogActor* Dog = World->SpawnActor<APariahDogActor>(
			APariahDogActor::StaticClass(),
			FVector(-155.0f, -40.0f, 10.0f),
			FRotator(0.0f, 65.0f, 0.0f),
			DogSpawnParams
		);
		if (Dog)
		{
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Mohalla Pariah Dog in shadowed alleyway alcove at (-155, -40, 10)."));
		}
	}

	// 17. Spawn Historical Colonial Police Checkpoint Barricade (Naka Bandi)
	int32 ExistingBarriers = 0;
	for (TActorIterator<ACheckpointBarrierActor> BarrierIt(World); BarrierIt; ++BarrierIt)
	{
		ExistingBarriers++;
	}

	if (ExistingBarriers == 0)
	{
		FActorSpawnParameters BarrierSpawnParams;
		BarrierSpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

		ACheckpointBarrierActor* Barrier = World->SpawnActor<ACheckpointBarrierActor>(
			ACheckpointBarrierActor::StaticClass(),
			FVector(-20.0f, -270.0f, 10.0f),
			FRotator(0.0f, 90.0f, 0.0f),
			BarrierSpawnParams
		);
		if (Barrier)
		{
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Colonial Police Checkpoint Barricade with Red Lantern at (-20, -270, 10)."));
		}
	}

	// 18. Spawn Historical Basant Glass-Coated Kite Thread Snag Hazard (Manja Trap)
	int32 ExistingTraps = 0;
	for (TActorIterator<AManjaTrapActor> TrapIt(World); TrapIt; ++TrapIt)
	{
		ExistingTraps++;
	}

	if (ExistingTraps == 0)
	{
		FActorSpawnParameters TrapSpawnParams;
		TrapSpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

		AManjaTrapActor* ManjaTrap = World->SpawnActor<AManjaTrapActor>(
			AManjaTrapActor::StaticClass(),
			FVector(25.0f, 120.0f, 405.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			TrapSpawnParams
		);
		if (ManjaTrap)
		{
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Basant Glass Kite String Trap on rooftop terrace at (25, 120, 405)."));
		}
	}

	// 19. Spawn Historical Wheat Chaff Winnowing Scoop Decoy (Bhoosa Dust Screen)
	int32 ExistingChaff = 0;
	for (TActorIterator<AChaffDustDecoyActor> ChaffIt(World); ChaffIt; ++ChaffIt)
	{
		ExistingChaff++;
	}

	if (ExistingChaff == 0)
	{
		FActorSpawnParameters ChaffSpawnParams;
		ChaffSpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

		AChaffDustDecoyActor* Chaff = World->SpawnActor<AChaffDustDecoyActor>(
			AChaffDustDecoyActor::StaticClass(),
			FVector(85.0f, 60.0f, 10.0f),
			FRotator(0.0f, 35.0f, 0.0f),
			ChaffSpawnParams
		);
		if (Chaff)
		{
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Harvest Wheat Chaff Decoy in courtyard granary corner at (85, 60, 10)."));
		}
	}

	// 20. Spawn Historical British Military Telegraph Line Sabotage Post
	int32 ExistingWires = 0;
	for (TActorIterator<ATelegraphWireActor> WireIt(World); WireIt; ++WireIt)
	{
		ExistingWires++;
	}

	if (ExistingWires == 0)
	{
		FActorSpawnParameters WireSpawnParams;
		WireSpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

		ATelegraphWireActor* WirePost = World->SpawnActor<ATelegraphWireActor>(
			ATelegraphWireActor::StaticClass(),
			FVector(60.0f, 240.0f, 435.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			WireSpawnParams
		);
		if (WirePost)
		{
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned British Telegraph Wire Sabotage Post on rooftop parapet at (60, 240, 435)."));
		}
	}

	// 21. Spawn Historical Courtyard Earthen Matka Water Stand (Ghara)
	int32 ExistingMatkas = 0;
	for (TActorIterator<AMatkaStandActor> MatkaIt(World); MatkaIt; ++MatkaIt)
	{
		ExistingMatkas++;
	}

	if (ExistingMatkas == 0)
	{
		FActorSpawnParameters MatkaSpawnParams;
		MatkaSpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

		AMatkaStandActor* Matka = World->SpawnActor<AMatkaStandActor>(
			AMatkaStandActor::StaticClass(),
			FVector(140.0f, -40.0f, 10.0f),
			FRotator(0.0f, 45.0f, 0.0f),
			MatkaSpawnParams
		);
		if (Matka)
		{
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Courtyard Earthen Matka Stand at (140, -40, 10)."));
		}
	}

	// 22. Spawn Historical Municipal Curfew Bell / Gong (Chaukidar Ghanta)
	int32 ExistingGongs = 0;
	for (TActorIterator<ACurfewGongActor> GongIt(World); GongIt; ++GongIt)
	{
		ExistingGongs++;
	}

	if (ExistingGongs == 0)
	{
		FActorSpawnParameters GongSpawnParams;
		GongSpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

		ACurfewGongActor* Gong = World->SpawnActor<ACurfewGongActor>(
			ACurfewGongActor::StaticClass(),
			FVector(-60.0f, -200.0f, 180.0f),
			FRotator(0.0f, 90.0f, 0.0f),
			GongSpawnParams
		);
		if (Gong)
		{
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Municipal Curfew Gong on gateway tower at (-60, -200, 180)."));
		}
	}

	// 23. Spawn Historical Foliage & Nature (Sacred Peepal Tree & Courtyard Tulsi Pedestal)
	int32 ExistingTulsi = 0;
	for (TActorIterator<AInspectableProp> PropIt(World); PropIt; ++PropIt)
	{
		if (PropIt->ItemName.ToString().Contains(TEXT("Tulsi")))
		{
			ExistingTulsi++;
		}
	}

	if (ExistingTulsi == 0)
	{
		FActorSpawnParameters FoliageSpawnParams;
		FoliageSpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

		// Sacred Peepal Tree with Chabutra Shrine in Zone C Well Square
		AInspectableProp* PeepalTree = World->SpawnActor<AInspectableProp>(
			AInspectableProp::StaticClass(),
			FVector(380.0f, 1350.0f, 0.0f),
			FRotator(0.0f, 45.0f, 0.0f),
			FoliageSpawnParams
		);
		if (PeepalTree)
		{
			PeepalTree->ItemName = FText::FromString(TEXT("Sacred Peepal Tree (Bodhi Chabutra)"));
			PeepalTree->LoreDescription = FText::FromString(
				TEXT("An ancient sacred Peepal tree (Ficus religiosa) revered by both Hindu and Sikh residents. Around its raised Lahori brick chabutra (plinth), elders gather at twilight to discuss political news from Lahore and light earthen mustard-oil lamps.")
			);
			PeepalTree->InteractionVerb = FText::FromString(TEXT("Rest Under"));
			UStaticMesh* PeepalMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Game/Environment/Mohalla/Meshes/SM_Foliage_PeepalTree_Shrine.SM_Foliage_PeepalTree_Shrine"));
			if (PeepalMesh && PeepalTree->MeshComponent)
			{
				PeepalTree->MeshComponent->SetStaticMesh(PeepalMesh);
			}
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Sacred Peepal Tree with Chabutra Shrine at (380, 1350, 0)."));
		}

		// Courtyard Sacred Tulsi Planter Pedestal in Zone A Haveli Courtyard
		AInspectableProp* TulsiPedestal = World->SpawnActor<AInspectableProp>(
			AInspectableProp::StaticClass(),
			FVector(120.0f, 80.0f, 10.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			FoliageSpawnParams
		);
		if (TulsiPedestal)
		{
			TulsiPedestal->ItemName = FText::FromString(TEXT("Courtyard Tulsi Chaura (Holy Basil Shrine)"));
			TulsiPedestal->LoreDescription = FText::FromString(
				TEXT("A carved brick pedestal holding a thriving holy basil (Tulsi) plant in the inner family courtyard. Each morning before sunrise, Kabir's mother Parvati waters the plant and lights a small clay diya, praying for peace and the safe return of family members.")
			);
			TulsiPedestal->InteractionVerb = FText::FromString(TEXT("Pay Respects at"));
			UStaticMesh* TulsiMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Game/Environment/Mohalla/Meshes/SM_Prop_Tulsi_Pedestal.SM_Prop_Tulsi_Pedestal"));
			if (TulsiMesh && TulsiPedestal->MeshComponent)
			{
				TulsiPedestal->MeshComponent->SetStaticMesh(TulsiMesh);
			}
			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Courtyard Tulsi Chaura Pedestal at (120, 80, 10)."));
		}
	}

	// 24. Spawn Historical Civilian NPCs (Ram Lubhaya, Hira Halwai, Ghasita Bhishti, Lala Karam Chand, Pandit Kashi Ram)
	int32 ExistingCivilians = 0;
	for (TActorIterator<ACivilianNPCActor> CivIt(World); CivIt; ++CivIt)
	{
		ExistingCivilians++;
	}

	if (ExistingCivilians == 0)
	{
		FActorSpawnParameters CivSpawnParams;
		CivSpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

		struct FCivDef
		{
			ECivilianOccupation Occupation;
			FVector Location;
			FRotator Rotation;
			const TCHAR* LogName;
		};

		const FCivDef CiviliansToSpawn[] = {
			{ ECivilianOccupation::FatherTailor, FVector(200.0f, 480.0f, 10.0f), FRotator(0.0f, 90.0f, 0.0f), TEXT("Ram Lubhaya (Father Tailor)") },
			{ ECivilianOccupation::BhishtiWaterCarrier, FVector(-80.0f, 1320.0f, 10.0f), FRotator(0.0f, 45.0f, 0.0f), TEXT("Ghasita Bhishti (Water-Carrier)") },
			{ ECivilianOccupation::HalwaiChaiVendor, FVector(-200.0f, 1680.0f, 10.0f), FRotator(0.0f, 90.0f, 0.0f), TEXT("Hira Halwai (Tea Stall Owner)") },
			{ ECivilianOccupation::ClothMerchant, FVector(200.0f, 1980.0f, 10.0f), FRotator(0.0f, -90.0f, 0.0f), TEXT("Lala Karam Chand (Cloth Merchant)") },
			{ ECivilianOccupation::SchoolHeadmaster, FVector(1350.0f, 1420.0f, 10.0f), FRotator(0.0f, -90.0f, 0.0f), TEXT("Pandit Kashi Ram (School Headmaster)") },
			{ ECivilianOccupation::SchoolFriendKartar, FVector(450.0f, 1380.0f, 88.0f), FRotator(0.0f, -90.0f, 0.0f), TEXT("Kartar Singh (Schoolmate & Friend)") },
			{ ECivilianOccupation::MunadiTownCrier, FVector(60.0f, 1920.0f, 10.0f), FRotator(0.0f, 30.0f, 0.0f), TEXT("Nikka Ram (Munadi Town Crier)") },
			{ ECivilianOccupation::ProtestElder, FVector(140.0f, 1860.0f, 10.0f), FRotator(0.0f, 120.0f, 0.0f), TEXT("Bhai Sant Singh (Protest Elder)") }
		};

		for (const FCivDef& Def : CiviliansToSpawn)
		{
			ACivilianNPCActor* NewCiv = World->SpawnActor<ACivilianNPCActor>(
				ACivilianNPCActor::StaticClass(),
				Def.Location,
				Def.Rotation,
				CivSpawnParams
			);
			if (NewCiv)
			{
				NewCiv->ConfigureOccupation(Def.Occupation);
				UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Civilian NPC: %s at %s"), Def.LogName, *Def.Location.ToString());
			}
		}
	}
	else
	{
		// If level has existing civilians, ensure Munadi Town Crier and Protest Elder exist in Grand Bazaar Chowk
		bool bHasMunadi = false;
		bool bHasElder = false;
		for (TActorIterator<ACivilianNPCActor> CivIt(World); CivIt; ++CivIt)
		{
			if (CivIt->Occupation == ECivilianOccupation::MunadiTownCrier) bHasMunadi = true;
			if (CivIt->Occupation == ECivilianOccupation::ProtestElder) bHasElder = true;
		}

		FActorSpawnParameters CivSpawnParams;
		CivSpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

		if (!bHasMunadi)
		{
			ACivilianNPCActor* MunadiCiv = World->SpawnActor<ACivilianNPCActor>(
				ACivilianNPCActor::StaticClass(),
				FVector(60.0f, 1920.0f, 10.0f),
				FRotator(0.0f, 30.0f, 0.0f),
				CivSpawnParams
			);
			if (MunadiCiv)
			{
				MunadiCiv->ConfigureOccupation(ECivilianOccupation::MunadiTownCrier);
				UE_LOG(LogREVOLUTION, Log, TEXT("Spawned missing Civilian NPC: Nikka Ram (Munadi Town Crier) at (60, 1920, 10)"));
			}
		}

		if (!bHasElder)
		{
			ACivilianNPCActor* ElderCiv = World->SpawnActor<ACivilianNPCActor>(
				ACivilianNPCActor::StaticClass(),
				FVector(140.0f, 1860.0f, 10.0f),
				FRotator(0.0f, 120.0f, 0.0f),
				CivSpawnParams
			);
			if (ElderCiv)
			{
				ElderCiv->ConfigureOccupation(ECivilianOccupation::ProtestElder);
				UE_LOG(LogREVOLUTION, Log, TEXT("Spawned missing Civilian NPC: Bhai Sant Singh (Protest Elder) at (140, 1860, 10)"));
			}
		}
	}
}

void ARevolutionGameMode::HandlePlayerApprehended(ACurfewPatrolAI* Watchman, ARevolutionCharacter* CaughtPlayer)
{
	if (bIsPlayerApprehended) return;

	bIsPlayerApprehended = true;
	ApprehensionTimer = 0.0f;

	UE_LOG(LogREVOLUTION, Warning, TEXT("=== SECTION 144 APPREHENSION: Kabir cornered by Curfew Watchman! ==="));

	if (CaughtPlayer)
	{
		// Halt player locomotion immediately
		if (CaughtPlayer->GetCharacterMovement())
		{
			CaughtPlayer->GetCharacterMovement()->StopMovementImmediately();
			CaughtPlayer->GetCharacterMovement()->DisableMovement();
		}

		if (CaughtPlayer->IsHidingInCover())
		{
			CaughtPlayer->ExitHidingSpot();
		}

		CaughtPlayer->bIsSatchelJournalOpen = false;

		// Face Kabir towards apprehending watchman
		if (Watchman)
		{
			FVector DirToWatchman = (Watchman->GetActorLocation() - CaughtPlayer->GetActorLocation()).GetSafeNormal2D();
			if (!DirToWatchman.IsNearlyZero())
			{
				CaughtPlayer->SetActorRotation(DirToWatchman.Rotation());
			}
		}
	}

	if (Watchman)
	{
		// Halt watchman pursuit and face Kabir
		if (Watchman->GetCharacterMovement())
		{
			Watchman->GetCharacterMovement()->StopMovementImmediately();
		}

		if (CaughtPlayer)
		{
			FVector DirToPlayer = (CaughtPlayer->GetActorLocation() - Watchman->GetActorLocation()).GetSafeNormal2D();
			if (!DirToPlayer.IsNearlyZero())
			{
				Watchman->SetActorRotation(DirToPlayer.Rotation());
			}
		}

		// Play watchman whistle and challenge callout
		if (Watchman->WatchmanWhistleSound)
		{
			UGameplayStatics::PlaySoundAtLocation(this, Watchman->WatchmanWhistleSound, Watchman->GetActorLocation(), 1.25f);
		}
		if (Watchman->WatchmanCalloutSound)
		{
			UGameplayStatics::PlaySoundAtLocation(this, Watchman->WatchmanCalloutSound, Watchman->GetActorLocation(), 1.0f);
		}
	}
}

void ARevolutionGameMode::RespawnPlayerAtCheckpoint()
{
	if (!bIsPlayerApprehended) return;

	UE_LOG(LogREVOLUTION, Log, TEXT("Respawning Kabir at checkpoint: %s"), *CheckpointLocation.ToString());

	bIsPlayerApprehended = false;
	ApprehensionTimer = 0.0f;

	ARevolutionCharacter* Kabir = Cast<ARevolutionCharacter>(UGameplayStatics::GetPlayerCharacter(this, 0));
	if (Kabir)
	{
		// Teleport to latest safe checkpoint
		Kabir->TeleportTo(CheckpointLocation, CheckpointRotation, false, true);

		// Restore player movement
		if (Kabir->GetCharacterMovement())
		{
			Kabir->GetCharacterMovement()->SetMovementMode(MOVE_Walking);
			Kabir->GetCharacterMovement()->Velocity = FVector::ZeroVector;
		}

		// Replenish minimum consumable gear for next attempt
		Kabir->ChalkCount = FMath::Max(Kabir->ChalkCount, 4);
		Kabir->PebbleCount = FMath::Max(Kabir->PebbleCount, 3);
		Kabir->CurrentStamina = Kabir->MaxStamina;
		Kabir->UnCrouch();
	}

	// Reset all curfew watchmen in level to their initial unaware patrol routine
	for (TActorIterator<ACurfewPatrolAI> It(GetWorld()); It; ++It)
	{
		It->ResetPatrolState();
	}
}

void ARevolutionGameMode::SetCheckpoint(const FVector& NewLocation, const FRotator& NewRotation)
{
	CheckpointLocation = NewLocation;
	CheckpointRotation = NewRotation;
	UE_LOG(LogREVOLUTION, Log, TEXT("Checkpoint updated to %s (Yaw: %.1f)"), *NewLocation.ToString(), NewRotation.Yaw);
}

bool ARevolutionGameMode::FixKabirBlendSpace()
{
#if WITH_EDITOR
	UBlendSpace* BS = LoadObject<UBlendSpace>(nullptr, TEXT("/Game/Characters/Kabir_AAA/Animations/KabirAAA_BS_MM_WalkRun.KabirAAA_BS_MM_WalkRun"));
	if (!BS)
	{
		UE_LOG(LogREVOLUTION, Error, TEXT("[FixKabirBlendSpace] Failed to load KabirAAA_BS_MM_WalkRun"));
		return false;
	}

	UAnimSequence* Idle = LoadObject<UAnimSequence>(nullptr, TEXT("/Game/Characters/Kabir_AAA/Animations/KabirAAA_MM_Idle2.KabirAAA_MM_Idle2"));
	UAnimSequence* Walk = LoadObject<UAnimSequence>(nullptr, TEXT("/Game/Characters/Kabir_AAA/Animations/KabirAAA_MM_Walk_Fwd2.KabirAAA_MM_Walk_Fwd2"));
	UAnimSequence* Run = LoadObject<UAnimSequence>(nullptr, TEXT("/Game/Characters/Kabir_AAA/Animations/KabirAAA_MM_Run_Fwd2.KabirAAA_MM_Run_Fwd2"));

	if (!Idle || !Walk || !Run)
	{
		UE_LOG(LogREVOLUTION, Error, TEXT("[FixKabirBlendSpace] Failed to load one or more anim sequences (Idle=%s, Walk=%s, Run=%s)"),
			Idle ? TEXT("OK") : TEXT("Missing"),
			Walk ? TEXT("OK") : TEXT("Missing"),
			Run ? TEXT("OK") : TEXT("Missing"));
		return false;
	}

	while (BS->GetNumberOfBlendSamples() > 0)
	{
		BS->DeleteSample(0);
	}

	BS->AddSample(Idle, FVector(0.0f, 0.0f, 0.0f));
	BS->AddSample(Walk, FVector(230.0f, 0.0f, 0.0f));
	BS->AddSample(Run, FVector(500.0f, 0.0f, 0.0f));

	BS->ValidateSampleData();
	BS->MarkPackageDirty();

	UPackage* Package = BS->GetOutermost();
	Package->MarkPackageDirty();
	FString PackageFileName = FPackageName::LongPackageNameToFilename(Package->GetName(), FPackageName::GetAssetPackageExtension());
	FSavePackageArgs SaveArgs;
	SaveArgs.TopLevelFlags = RF_Public | RF_Standalone;
	bool bSaved = UPackage::SavePackage(Package, BS, *PackageFileName, SaveArgs);
	UE_LOG(LogREVOLUTION, Warning, TEXT("[FixKabirBlendSpace] Saved BlendSpace to %s: %s"), *PackageFileName, bSaved ? TEXT("SUCCESS") : TEXT("FAILED"));

	// Also assign authentic historical PBR materials directly to SK_Kabir_Protagonist_AAA asset
	USkeletalMesh* Mesh = LoadObject<USkeletalMesh>(nullptr, TEXT("/Game/Characters/Kabir_AAA/SK_Kabir_Protagonist_AAA.SK_Kabir_Protagonist_AAA"));
	if (Mesh)
	{
		static const TCHAR* MatPaths[] = {
			TEXT("/Game/Characters/Kabir_v04_RigB/Kabir_Skin.Kabir_Skin"),
			TEXT("/Game/Environment/Mohalla/Materials/M_AgedTeak_PBR.M_AgedTeak_PBR"),
			TEXT("/Game/Characters/Kabir_v04_RigB/Kabir_Sclera.Kabir_Sclera"),
			TEXT("/Game/Characters/Kabir_v04_RigB/Kabir_Iris.Kabir_Iris"),
			TEXT("/Game/Characters/Kabir_v04_RigB/Kabir_Hair_001.Kabir_Hair_001"),
			TEXT("/Game/Environment/Mohalla/Materials/M_AgedTeak_PBR.M_AgedTeak_PBR"),
			TEXT("/Game/Environment/Mohalla/Materials/M_ClothUndyedCotton_PBR.M_ClothUndyedCotton_PBR"),
			TEXT("/Game/Characters/Kabir_v04_RigB/Kabir_Shorts_Cotton.Kabir_Shorts_Cotton"),
			TEXT("/Game/Environment/Mohalla/Materials/M_ClothSaffron_PBR.M_ClothSaffron_PBR"),
			TEXT("/Game/Environment/Mohalla/Materials/M_WroughtIron_PBR.M_WroughtIron_PBR")
		};
		for (int32 i = 0; i < 10; ++i)
		{
			if (UMaterialInterface* M = LoadObject<UMaterialInterface>(nullptr, MatPaths[i]))
			{
				if (Mesh->GetMaterials().IsValidIndex(i))
				{
					Mesh->GetMaterials()[i].MaterialInterface = M;
				}
			}
		}
		Mesh->MarkPackageDirty();
		UPackage* MeshPkg = Mesh->GetOutermost();
		MeshPkg->MarkPackageDirty();
		FString MeshFileName = FPackageName::LongPackageNameToFilename(MeshPkg->GetName(), FPackageName::GetAssetPackageExtension());
		bool bMeshSaved = UPackage::SavePackage(MeshPkg, Mesh, *MeshFileName, SaveArgs);
		UE_LOG(LogREVOLUTION, Warning, TEXT("[FixKabirBlendSpace] Saved SK_Kabir_Protagonist_AAA with 10 authentic materials: %s"), bMeshSaved ? TEXT("SUCCESS") : TEXT("FAILED"));
	}

	return bSaved;
#else
	return false;
#endif
}

// ============================================================================
// TASK 30: PERSISTENT SAVE / LOAD SYSTEM IMPLEMENTATION
// ============================================================================

bool ARevolutionGameMode::SaveGameToSlot(const FString& SlotName, int32 UserIndex)
{
	URevolutionSaveGame* SaveInst = Cast<URevolutionSaveGame>(UGameplayStatics::CreateSaveGameObject(URevolutionSaveGame::StaticClass()));
	if (!SaveInst)
	{
		UE_LOG(LogREVOLUTION, Error, TEXT("[SaveGame] Failed to allocate URevolutionSaveGame instance!"));
		return false;
	}

	SaveInst->SaveSlotName = SlotName;
	SaveInst->UserIndex = UserIndex;
	SaveInst->SaveTimestamp = FDateTime::UtcNow();
	LastSaveTimestamp = SaveInst->SaveTimestamp;

	// Persist checkpoint transform
	SaveInst->CheckpointLocation = CheckpointLocation;
	SaveInst->CheckpointRotation = CheckpointRotation;

	// Persist narrative mission stage
	if (URevolutionMissionSubsystem* Subsystem = GetWorld()->GetSubsystem<URevolutionMissionSubsystem>())
	{
		SaveInst->CurrentMissionStage = Subsystem->GetCurrentStage();
	}

	// Persist Kabir's dynamic location, inventory, and settings
	if (APlayerController* PC = UGameplayStatics::GetPlayerController(GetWorld(), 0))
	{
		if (ARevolutionCharacter* Kabir = Cast<ARevolutionCharacter>(PC->GetPawn()))
		{
			SaveInst->PlayerLocation = Kabir->GetActorLocation();
			SaveInst->PlayerRotation = Kabir->GetActorRotation();
			SaveInst->CurrentStamina = Kabir->CurrentStamina;
			SaveInst->PamphletCount = Kabir->GetPamphletCount();
			SaveInst->PebbleCount = Kabir->GetPebbleCount();
			SaveInst->ChalkCount = Kabir->GetChalkCount();
			SaveInst->SelectedCodexIndex = Kabir->SelectedCodexIndex;
			SaveInst->MasterVolume = Kabir->MasterVolume;
			SaveInst->SFXVolume = Kabir->SFXVolume;
			SaveInst->FoleyVolume = Kabir->FoleyVolume;
			SaveInst->VoiceVolume = Kabir->VoiceVolume;
			SaveInst->AmbienceVolume = Kabir->AmbienceVolume;
			SaveInst->SubtitleScaleMultiplier = Kabir->SubtitleScaleMultiplier;
			SaveInst->bHandheldSteamOSMode = Kabir->bHandheldSteamOSMode;
		}
	}

	const bool bSaved = UGameplayStatics::SaveGameToSlot(SaveInst, SlotName, UserIndex);
	if (bSaved)
	{
		UE_LOG(LogREVOLUTION, Log, TEXT("[SaveGame] Successfully committed state to slot '%s' (User %d). Timestamp: %s"), *SlotName, UserIndex, *SaveInst->SaveTimestamp.ToString());
	}
	else
	{
		UE_LOG(LogREVOLUTION, Error, TEXT("[SaveGame] Failed to write slot '%s' to disk!"), *SlotName);
	}

	return bSaved;
}

bool ARevolutionGameMode::LoadGameFromSlot(const FString& SlotName, int32 UserIndex)
{
	if (!UGameplayStatics::DoesSaveGameExist(SlotName, UserIndex))
	{
		UE_LOG(LogREVOLUTION, Warning, TEXT("[SaveGame] Slot '%s' does not exist on disk!"), *SlotName);
		return false;
	}

	URevolutionSaveGame* SaveInst = Cast<URevolutionSaveGame>(UGameplayStatics::LoadGameFromSlot(SlotName, UserIndex));
	if (!SaveInst)
	{
		UE_LOG(LogREVOLUTION, Error, TEXT("[SaveGame] Failed to deserialize URevolutionSaveGame from slot '%s'!"), *SlotName);
		return false;
	}

	LastSaveTimestamp = SaveInst->SaveTimestamp;

	// Restore checkpoint transform
	CheckpointLocation = SaveInst->CheckpointLocation;
	CheckpointRotation = SaveInst->CheckpointRotation;

	// Restore narrative mission stage
	if (URevolutionMissionSubsystem* Subsystem = GetWorld()->GetSubsystem<URevolutionMissionSubsystem>())
	{
		Subsystem->SetMissionStage(SaveInst->CurrentMissionStage);
	}

	// Restore Kabir's location, vitals, inventory and settings
	if (APlayerController* PC = UGameplayStatics::GetPlayerController(GetWorld(), 0))
	{
		if (ARevolutionCharacter* Kabir = Cast<ARevolutionCharacter>(PC->GetPawn()))
		{
			Kabir->TeleportTo(SaveInst->PlayerLocation, SaveInst->PlayerRotation);
			Kabir->CurrentStamina = SaveInst->CurrentStamina;
			Kabir->PamphletCount = SaveInst->PamphletCount;
			Kabir->PebbleCount = SaveInst->PebbleCount;
			Kabir->ChalkCount = SaveInst->ChalkCount;
			Kabir->SelectedCodexIndex = SaveInst->SelectedCodexIndex;
			Kabir->MasterVolume = SaveInst->MasterVolume;
			Kabir->SFXVolume = SaveInst->SFXVolume;
			Kabir->FoleyVolume = SaveInst->FoleyVolume;
			Kabir->VoiceVolume = SaveInst->VoiceVolume;
			Kabir->AmbienceVolume = SaveInst->AmbienceVolume;
			Kabir->SubtitleScaleMultiplier = SaveInst->SubtitleScaleMultiplier;
			Kabir->bHandheldSteamOSMode = SaveInst->bHandheldSteamOSMode;

			Kabir->ApplyAudioSettings();
			Kabir->ApplyHandheldScalability(SaveInst->bHandheldSteamOSMode);
		}
	}

	UE_LOG(LogREVOLUTION, Log, TEXT("[SaveGame] Successfully restored state from slot '%s' (User %d). Timestamp: %s"), *SlotName, UserIndex, *SaveInst->SaveTimestamp.ToString());
	return true;
}

bool ARevolutionGameMode::DoesSaveGameExist(const FString& SlotName, int32 UserIndex) const
{
	return UGameplayStatics::DoesSaveGameExist(SlotName, UserIndex);
}

bool ARevolutionGameMode::DeleteSaveSlot(const FString& SlotName, int32 UserIndex)
{
	const bool bDeleted = UGameplayStatics::DeleteGameInSlot(SlotName, UserIndex);
	UE_LOG(LogREVOLUTION, Log, TEXT("[SaveGame] Delete save slot '%s' (User %d): %s"), *SlotName, UserIndex, bDeleted ? TEXT("SUCCESS") : TEXT("FAILED/NOT_FOUND"));
	return bDeleted;
}


