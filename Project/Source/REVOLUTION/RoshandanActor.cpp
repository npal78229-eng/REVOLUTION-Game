// Copyright Epic Games, Inc. All Rights Reserved.

#include "RoshandanActor.h"
#include "RevolutionCharacter.h"
#include "CurfewPatrolAI.h"
#include "Components/BoxComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SceneComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/SoundBase.h"
#include "EngineUtils.h"
#include "REVOLUTION.h"

ARoshandanActor::ARoshandanActor()
{
	PrimaryActorTick.bCanEverTick = false;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	static ConstructorHelpers::FObjectFinder<UStaticMesh> CubeMeshFinder(TEXT("/Engine/BasicShapes/Cube.Cube"));

	// Low masonry brick curb around the lightwell
	ShaftCurbMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("ShaftCurbMesh"));
	ShaftCurbMesh->SetupAttachment(RootComponent);
	ShaftCurbMesh->SetRelativeScale3D(FVector(0.90f, 0.90f, 0.15f));
	ShaftCurbMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	if (CubeMeshFinder.Succeeded())
	{
		ShaftCurbMesh->SetStaticMesh(CubeMeshFinder.Object);
	}

	// Forged Iron Grille Lattice
	IronGrilleMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("IronGrilleMesh"));
	IronGrilleMesh->SetupAttachment(RootComponent);
	IronGrilleMesh->SetRelativeLocation(FVector(0.0f, 0.0f, 8.0f));
	IronGrilleMesh->SetRelativeScale3D(FVector(0.75f, 0.75f, 0.04f));
	IronGrilleMesh->SetCollisionProfileName(TEXT("NoCollision"));
	if (CubeMeshFinder.Succeeded())
	{
		IronGrilleMesh->SetStaticMesh(CubeMeshFinder.Object);
	}

	InteractionBox = CreateDefaultSubobject<UBoxComponent>(TEXT("InteractionBox"));
	InteractionBox->SetupAttachment(RootComponent);
	InteractionBox->SetBoxExtent(FVector(75.0f, 75.0f, 40.0f));
	InteractionBox->SetCollisionProfileName(TEXT("Trigger"));

	static ConstructorHelpers::FObjectFinder<USoundBase> DropSoundFinder(TEXT("/Game/Audio/SFX/SFX_Pebble_Throw.SFX_Pebble_Throw"));
	if (DropSoundFinder.Succeeded())
	{
		PebbleDropSound = DropSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> ImpactSoundFinder(TEXT("/Game/Audio/SFX/SFX_Pebble_Impact.SFX_Pebble_Impact"));
	if (ImpactSoundFinder.Succeeded())
	{
		GroundImpactSound = ImpactSoundFinder.Object;
	}
}

void ARoshandanActor::BeginPlay()
{
	Super::BeginPlay();

	UE_LOG(LogREVOLUTION, Log, TEXT("RoshandanActor spawned at %s (Drop Target: %s)"), *GetActorLocation().ToString(), *DropTargetLocation.ToString());
}

bool ARoshandanActor::CanInteract_Implementation(const ARevolutionCharacter* Interactor) const
{
	const float CurrentTime = GetWorld() ? GetWorld()->GetTimeSeconds() : 0.0f;
	if (CurrentTime - LastDropTime < DropCooldown)
	{
		return false;
	}
	return Interactor && Interactor->GetPebbleCount() > 0;
}

FText ARoshandanActor::GetInteractionPrompt_Implementation() const
{
	const float CurrentTime = GetWorld() ? GetWorld()->GetTimeSeconds() : 0.0f;
	if (CurrentTime - LastDropTime < DropCooldown)
	{
		return FText::FromString(TEXT("Roshandan Lightwell (Cooldown)"));
	}
	return FText::FromString(TEXT("Drop Clay Marble Down Lightwell"));
}

void ARoshandanActor::OnInteract_Implementation(ARevolutionCharacter* Interactor)
{
	if (!Interactor || Interactor->GetPebbleCount() <= 0)
	{
		UE_LOG(LogREVOLUTION, Log, TEXT("Cannot drop pebble down roshandan: no pebbles in satchel."));
		return;
	}

	const float CurrentTime = GetWorld()->GetTimeSeconds();
	if (CurrentTime - LastDropTime < DropCooldown)
	{
		return;
	}

	LastDropTime = CurrentTime;

	// 1. Consume 1 clay marble from courier satchel
	Interactor->PebbleCount = FMath::Max(0, Interactor->PebbleCount - 1);

	// 2. Play drop sound at rooftop lightwell
	if (PebbleDropSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, PebbleDropSound, GetActorLocation(), 1.0f);
	}

	// 3. Play ground impact echo at courtyard floor below
	if (GroundImpactSound)
	{
		const float RandomPitch = FMath::RandRange(0.85f, 1.10f);
		UGameplayStatics::PlaySoundAtLocation(this, GroundImpactSound, DropTargetLocation, 1.25f, RandomPitch);
	}

	UE_LOG(LogREVOLUTION, Warning, TEXT("Kabir dropped clay marble through Roshandan to courtyard floor %s! (Remaining: %d)"), *DropTargetLocation.ToString(), Interactor->GetPebbleCount());

	// 4. Divert watchmen in courtyard below
	int32 AlertedWatchmen = 0;
	for (TActorIterator<ACurfewPatrolAI> It(GetWorld()); It; ++It)
	{
		ACurfewPatrolAI* Watchman = *It;
		if (Watchman)
		{
			const float Dist = FVector::Dist(Watchman->GetActorLocation(), DropTargetLocation);
			if (Dist <= AcousticAlertRadius)
			{
				Watchman->InvestigateSoundLocation(DropTargetLocation);
				AlertedWatchmen++;
			}
		}
	}

	UE_LOG(LogREVOLUTION, Log, TEXT("Roshandan vertical decoy alerted %d Watchmen in courtyard below!"), AlertedWatchmen);

	// 5. Educational historical inspection on calm interaction
	if (Interactor->GetVelocity().SizeSquared() < 100.0f)
	{
		Interactor->StartInspection(
			RoshandanName,
			FText::FromString(TEXT("A traditional Punjabi haveli ventilation shaft (roshandan) cut into the brick terrace floor, protected by forged iron bars. Dropping a clay marble down the opening creates a loud echo on the courtyard flagstones 4 meters below, allowing young rooftop scouts to divert curfew watchmen without descending."))
		);
	}
}
