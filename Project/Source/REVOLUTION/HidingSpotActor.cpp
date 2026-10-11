// Copyright Epic Games, Inc. All Rights Reserved.

#include "HidingSpotActor.h"
#include "RevolutionCharacter.h"
#include "Components/SceneComponent.h"
#include "Components/StaticMeshComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Sound/SoundBase.h"
#include "Kismet/GameplayStatics.h"
#include "REVOLUTION.h"

AHidingSpotActor::AHidingSpotActor()
{
	PrimaryActorTick.bCanEverTick = false;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	CoverMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("CoverMesh"));
	CoverMesh->SetupAttachment(RootComponent);
	CoverMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));

	static ConstructorHelpers::FObjectFinder<UStaticMesh> MeshFinder(TEXT("/Game/Environment/Mohalla/Meshes/SM_Prop_GrainSack_Jute_01.SM_Prop_GrainSack_Jute_01"));
	if (MeshFinder.Succeeded())
	{
		CoverMesh->SetStaticMesh(MeshFinder.Object);
	}

	HidingPoint = CreateDefaultSubobject<USceneComponent>(TEXT("HidingPoint"));
	HidingPoint->SetupAttachment(RootComponent);
	HidingPoint->SetRelativeLocation(FVector(0.0f, 0.0f, 0.0f));

	ExitPoint = CreateDefaultSubobject<USceneComponent>(TEXT("ExitPoint"));
	ExitPoint->SetupAttachment(RootComponent);
	ExitPoint->SetRelativeLocation(FVector(0.0f, 90.0f, 0.0f));

	static ConstructorHelpers::FObjectFinder<USoundBase> RustleSoundFinder(TEXT("/Game/Audio/SFX/SFX_Conceal_Cloth_Rustle.SFX_Conceal_Cloth_Rustle"));
	if (RustleSoundFinder.Succeeded())
	{
		ClothRustleSound = RustleSoundFinder.Object;
	}
}

bool AHidingSpotActor::CanInteract_Implementation(const ARevolutionCharacter* Interactor) const
{
	if (!Interactor) return false;
	// Can interact if spot is free, OR if the current interactor is already hiding inside (to exit)
	return !bIsOccupied || (Occupant == Interactor);
}

FText AHidingSpotActor::GetInteractionPrompt_Implementation() const
{
	return bIsOccupied ? ExitPrompt : ConcealPrompt;
}

void AHidingSpotActor::OnInteract_Implementation(ARevolutionCharacter* Interactor)
{
	if (!Interactor) return;

	if (bIsOccupied && Occupant == Interactor)
	{
		EjectOccupant();
	}
	else if (!bIsOccupied)
	{
		bIsOccupied = true;
		Occupant = Interactor;

		Interactor->EnterHidingSpot(this);

		if (ClothRustleSound)
		{
			UGameplayStatics::PlaySoundAtLocation(this, ClothRustleSound, GetActorLocation(), 0.95f, FMath::RandRange(0.95f, 1.05f));
		}

		UE_LOG(LogREVOLUTION, Log, TEXT("Kabir concealed in hiding spot: %s"), *SpotName.ToString());
	}
}

void AHidingSpotActor::EjectOccupant()
{
	if (Occupant)
	{
		ARevolutionCharacter* CachedOccupant = Occupant;
		bIsOccupied = false;
		Occupant = nullptr;

		CachedOccupant->ExitHidingSpot();

		if (ClothRustleSound)
		{
			UGameplayStatics::PlaySoundAtLocation(this, ClothRustleSound, GetActorLocation(), 0.95f, FMath::RandRange(0.95f, 1.05f));
		}

		UE_LOG(LogREVOLUTION, Log, TEXT("Kabir exited hiding spot: %s"), *SpotName.ToString());
	}
}
