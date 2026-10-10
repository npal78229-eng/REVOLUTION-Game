// Copyright Epic Games, Inc. All Rights Reserved.

#include "RevolutionGameMode.h"
#include "RevolutionCharacter.h"
#include "RevolutionHUD.h"
#include "InspectableProp.h"
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
}
