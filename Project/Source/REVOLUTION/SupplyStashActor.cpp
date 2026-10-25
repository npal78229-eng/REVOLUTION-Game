// Copyright Epic Games, Inc. All Rights Reserved.

#include "SupplyStashActor.h"
#include "RevolutionCharacter.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SceneComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/SoundBase.h"
#include "REVOLUTION.h"

ASupplyStashActor::ASupplyStashActor()
{
	PrimaryActorTick.bCanEverTick = false;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	StashMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("StashMesh"));
	StashMesh->SetupAttachment(RootComponent);
	StashMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	StashMesh->SetRelativeScale3D(FVector(0.35f, 0.35f, 0.25f));

	static ConstructorHelpers::FObjectFinder<UStaticMesh> MeshFinder(TEXT("/Game/Environment/Mohalla/Meshes/SM_Prop_ClayChaiCup_Kulhad.SM_Prop_ClayChaiCup_Kulhad"));
	if (MeshFinder.Succeeded())
	{
		StashMesh->SetStaticMesh(MeshFinder.Object);
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> PebbleSoundFinder(TEXT("/Game/Audio/SFX/SFX_Pebble_Throw.SFX_Pebble_Throw"));
	if (PebbleSoundFinder.Succeeded())
	{
		PickupSound = PebbleSoundFinder.Object;
	}
}

void ASupplyStashActor::BeginPlay()
{
	Super::BeginPlay();

	// Load appropriate pickup sound if Chalk or Pamphlet type
	if (StashType == ESupplyStashType::Chalk)
	{
		USoundBase* ChalkSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Chalk_Draw.SFX_Chalk_Draw"));
		if (ChalkSound)
		{
			PickupSound = ChalkSound;
		}
	}
	else if (StashType == ESupplyStashType::Pamphlets)
	{
		USoundBase* PaperSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Pamphlet_Retrieve.SFX_Pamphlet_Retrieve"));
		if (PaperSound)
		{
			PickupSound = PaperSound;
		}
	}

	UE_LOG(LogREVOLUTION, Log, TEXT("SupplyStashActor (%s) spawned at %s"), *StashTitle.ToString(), *GetActorLocation().ToString());
}

bool ASupplyStashActor::CanInteract_Implementation(const ARevolutionCharacter* Interactor) const
{
	if (bIsCollected || !Interactor)
	{
		return false;
	}

	if (StashType == ESupplyStashType::Pebbles)
	{
		return Interactor->GetPebbleCount() < Interactor->MaxPebbles;
	}
	else if (StashType == ESupplyStashType::Chalk)
	{
		return Interactor->GetChalkCount() < Interactor->MaxChalk;
	}
	else // ESupplyStashType::Pamphlets
	{
		return Interactor->GetPamphletCount() < Interactor->MaxPamphlets;
	}
}

FText ASupplyStashActor::GetInteractionPrompt_Implementation() const
{
	if (bIsCollected)
	{
		return FText::GetEmpty();
	}

	if (StashType == ESupplyStashType::Pebbles)
	{
		return FText::FromString(FString::Printf(TEXT("Gather Clay Marbles (+%d)"), ReplenishAmount));
	}
	else if (StashType == ESupplyStashType::Chalk)
	{
		return FText::FromString(FString::Printf(TEXT("Take Tailor's Chalk (+%d)"), ReplenishAmount));
	}
	else
	{
		return FText::FromString(FString::Printf(TEXT("Take Satyagraha Handbills (+%d)"), ReplenishAmount));
	}
}

void ASupplyStashActor::OnInteract_Implementation(ARevolutionCharacter* Interactor)
{
	if (bIsCollected || !Interactor)
	{
		return;
	}

	bIsCollected = true;

	if (StashType == ESupplyStashType::Pebbles)
	{
		Interactor->PebbleCount = FMath::Min(Interactor->MaxPebbles, Interactor->PebbleCount + ReplenishAmount);
		UE_LOG(LogREVOLUTION, Log, TEXT("Kabir gathered %d pebbles. Total: %d/%d"), ReplenishAmount, Interactor->GetPebbleCount(), Interactor->MaxPebbles);
	}
	else if (StashType == ESupplyStashType::Chalk)
	{
		Interactor->ChalkCount = FMath::Min(Interactor->MaxChalk, Interactor->ChalkCount + ReplenishAmount);
		UE_LOG(LogREVOLUTION, Log, TEXT("Kabir retrieved %d chalk pieces. Total: %d/%d"), ReplenishAmount, Interactor->GetChalkCount(), Interactor->MaxChalk);
	}
	else // ESupplyStashType::Pamphlets
	{
		Interactor->AddPamphlets(ReplenishAmount);
	}

	// Play tactile gather audio
	if (PickupSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, PickupSound, GetActorLocation(), 1.0f);
	}

	// Hide or disable mesh
	if (StashMesh)
	{
		StashMesh->SetVisibility(false);
		StashMesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	}

	// Inspect lore card upon collection
	if (Interactor->GetVelocity().SizeSquared() < 100.0f)
	{
		Interactor->StartInspection(StashTitle, LoreDescription);
	}
}
