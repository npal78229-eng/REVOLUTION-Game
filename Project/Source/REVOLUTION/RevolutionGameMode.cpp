// Copyright Epic Games, Inc. All Rights Reserved.

#include "RevolutionGameMode.h"
#include "RevolutionCharacter.h"
#include "RevolutionHUD.h"
#include "InspectableProp.h"
#include "CurfewPatrolAI.h"
#include "ObjectiveTriggerActor.h"
#include "RevolutionAtmosphereController.h"
#include "HidingSpotActor.h"
#include "DoorDeorhiActor.h"
#include "PigeonFlockActor.h"
#include "Engine/World.h"
#include "Engine/StaticMesh.h"
#include "Components/StaticMeshComponent.h"
#include "EngineUtils.h"
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

	// 3. Spawn Clandestine Mission Triggers (Leaflet Pickup, Rooftop Route, Courier Stash, Courtyard Return)
	int32 ExistingTriggers = 0;
	for (TActorIterator<AObjectiveTriggerActor> It(World); It; ++It)
	{
		ExistingTriggers++;
	}

	if (ExistingTriggers == 0)
	{
		FActorSpawnParameters TriggerSpawnParams;
		TriggerSpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

		// Objective 1 Trigger: Clandestine Leaflet Dispatch near courtyard charpai
		AObjectiveTriggerActor* LeafletTrigger = World->SpawnActor<AObjectiveTriggerActor>(
			AObjectiveTriggerActor::StaticClass(),
			FVector(115.0f, 135.0f, 25.0f),
			FRotator(0.0f, 15.0f, 0.0f),
			TriggerSpawnParams
		);
		if (LeafletTrigger)
		{
			LeafletTrigger->RequiredMissionStage = ECourierMissionStage::Stage_RetrievePamphlets;
			LeafletTrigger->InteractionPrompt = FText::FromString(TEXT("Retrieve Leaflets"));
			LeafletTrigger->ItemTitle = FText::FromString(TEXT("Anti-Rowlatt Pamphlet Dispatch"));
			LeafletTrigger->HistoricalLoreUponInteraction = FText::FromString(
				TEXT("Urdu and Gurmukhi leaflets printed in secret calling for an immediate town-wide Hartal (general shutdown). Kabir tucks them under his vest to cross the rooftops unseen.")
			);
			LeafletTrigger->bHideMeshOnTrigger = true;

			UStaticMesh* LeafletMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Game/Environment/Mohalla/Meshes/SM_Prop_GrainSack_Jute_01.SM_Prop_GrainSack_Jute_01"));
			if (LeafletMesh && LeafletTrigger->MeshComponent)
			{
				LeafletTrigger->MeshComponent->SetStaticMesh(LeafletMesh);
				LeafletTrigger->MeshComponent->SetRelativeScale3D(FVector(0.28f, 0.28f, 0.28f));
			}

			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Mission Objective 1: Pamphlet Pickup at (115, 135, 25)."));
		}

		// Objective 2 Trigger: Rooftop Terrace Parapet Waypoint
		AObjectiveTriggerActor* RooftopTrigger = World->SpawnActor<AObjectiveTriggerActor>(
			AObjectiveTriggerActor::StaticClass(),
			FVector(0.0f, 240.0f, 410.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			TriggerSpawnParams
		);
		if (RooftopTrigger)
		{
			RooftopTrigger->RequiredMissionStage = ECourierMissionStage::Stage_RooftopInfiltration;
			RooftopTrigger->InteractionPrompt = FText::FromString(TEXT("Survey Rooftop Route"));
			RooftopTrigger->ItemTitle = FText::FromString(TEXT("Mohalla Rooftop Vantage"));
			RooftopTrigger->HistoricalLoreUponInteraction = FText::FromString(
				TEXT("From this high brick terrace ledge, Kabir spots the colonial patrol lantern below in the alley. The drop box near the Jharokha balcony is now reachable across the rooftops.")
			);
			RooftopTrigger->bHideMeshOnTrigger = false;

			UStaticMesh* SpoolMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Game/Environment/Mohalla/Meshes/SM_Prop_Kite_Spool_Charkhi.SM_Prop_Kite_Spool_Charkhi"));
			if (SpoolMesh && RooftopTrigger->MeshComponent)
			{
				RooftopTrigger->MeshComponent->SetStaticMesh(SpoolMesh);
				RooftopTrigger->MeshComponent->SetRelativeScale3D(FVector(0.6f, 0.6f, 0.6f));
			}

			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Mission Objective 2: Rooftop Waypoint at (0, 240, 410)."));
		}

		// Objective 3 Trigger: Secret Courier Stash Box near upper Jharokha Balcony
		AObjectiveTriggerActor* StashTrigger = World->SpawnActor<AObjectiveTriggerActor>(
			AObjectiveTriggerActor::StaticClass(),
			FVector(-190.0f, -60.0f, 325.0f),
			FRotator(0.0f, 90.0f, 0.0f),
			TriggerSpawnParams
		);
		if (StashTrigger)
		{
			StashTrigger->RequiredMissionStage = ECourierMissionStage::Stage_DeliverToStash;
			StashTrigger->InteractionPrompt = FText::FromString(TEXT("Deposit in Courier Stash"));
			StashTrigger->ItemTitle = FText::FromString(TEXT("Underground Mohalla Courier Stash"));
			StashTrigger->HistoricalLoreUponInteraction = FText::FromString(
				TEXT("A carved sandalwood lockbox hidden behind the cedar jharokha lattice. Fellow anti-Rowlatt dispatch riders will retrieve the bulletins here before dawn to distribute along the railway lines.")
			);
			StashTrigger->bHideMeshOnTrigger = false;

			UStaticMesh* StashMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Game/Environment/Mohalla/Meshes/SM_Prop_Charpai_RopeBed.SM_Prop_Charpai_RopeBed"));
			if (StashMesh && StashTrigger->MeshComponent)
			{
				StashTrigger->MeshComponent->SetStaticMesh(StashMesh);
				StashTrigger->MeshComponent->SetRelativeScale3D(FVector(0.20f, 0.20f, 0.25f));
			}

			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Mission Objective 3: Courier Stash at (-190, -60, 325)."));
		}

		// Objective 4 Trigger: Safe Return Spot in Courtyard
		AObjectiveTriggerActor* ReturnTrigger = World->SpawnActor<AObjectiveTriggerActor>(
			AObjectiveTriggerActor::StaticClass(),
			FVector(10.0f, 20.0f, 15.0f),
			FRotator(0.0f, 0.0f, 0.0f),
			TriggerSpawnParams
		);
		if (ReturnTrigger)
		{
			ReturnTrigger->RequiredMissionStage = ECourierMissionStage::Stage_EvadeAndSurvive;
			ReturnTrigger->InteractionPrompt = FText::FromString(TEXT("Conclude Courier Mission"));
			ReturnTrigger->ItemTitle = FText::FromString(TEXT("Haveli Family Courtyard"));
			ReturnTrigger->HistoricalLoreUponInteraction = FText::FromString(
				TEXT("The courtyard deorhi gate clicks shut. As dawn breaks over the haveli terracotta roofs, temple and gurdwara bells herald the town-wide Hartal. All bazaar shops will remain shut in protest against wartime emergency laws.")
			);
			ReturnTrigger->bHideMeshOnTrigger = true;

			UStaticMesh* LanternMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Game/Environment/Mohalla/Meshes/SM_Prop_HurricaneLantern.SM_Prop_HurricaneLantern"));
			if (LanternMesh && ReturnTrigger->MeshComponent)
			{
				ReturnTrigger->MeshComponent->SetStaticMesh(LanternMesh);
				ReturnTrigger->MeshComponent->SetRelativeScale3D(FVector(0.4f, 0.4f, 0.4f));
			}

			UE_LOG(LogREVOLUTION, Log, TEXT("Spawned Mission Objective 4: Return Courtyard Trigger at (10, 20, 15)."));
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
}
