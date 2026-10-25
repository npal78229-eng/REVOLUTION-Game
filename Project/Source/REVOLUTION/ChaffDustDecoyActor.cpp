// Copyright Epic Games, Inc. All Rights Reserved.

#include "ChaffDustDecoyActor.h"
#include "RevolutionCharacter.h"
#include "CurfewPatrolAI.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SphereComponent.h"
#include "Components/SceneComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/SoundBase.h"
#include "EngineUtils.h"
#include "REVOLUTION.h"

AChaffDustDecoyActor::AChaffDustDecoyActor()
{
	PrimaryActorTick.bCanEverTick = true;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	static ConstructorHelpers::FObjectFinder<UStaticMesh> CubeMeshFinder(TEXT("/Engine/BasicShapes/Cube.Cube"));
	static ConstructorHelpers::FObjectFinder<UStaticMesh> SphereMeshFinder(TEXT("/Engine/BasicShapes/Sphere.Sphere"));

	// 1. Jute ration sack of harvested wheat chaff
	BurlapSackMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("BurlapSackMesh"));
	BurlapSackMesh->SetupAttachment(RootComponent);
	BurlapSackMesh->SetRelativeLocation(FVector(0.0f, 0.0f, 25.0f));
	BurlapSackMesh->SetRelativeScale3D(FVector(0.42f, 0.42f, 0.52f));
	BurlapSackMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	if (CubeMeshFinder.Succeeded())
	{
		BurlapSackMesh->SetStaticMesh(CubeMeshFinder.Object);
	}

	// 2. Woven bamboo winnowing scoop (Chhaj)
	WinnowingScoopMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("WinnowingScoopMesh"));
	WinnowingScoopMesh->SetupAttachment(BurlapSackMesh);
	WinnowingScoopMesh->SetRelativeLocation(FVector(15.0f, 0.0f, 15.0f));
	WinnowingScoopMesh->SetRelativeRotation(FRotator(25.0f, 0.0f, 0.0f));
	WinnowingScoopMesh->SetRelativeScale3D(FVector(0.20f, 0.70f, 0.65f));
	WinnowingScoopMesh->SetCollisionProfileName(TEXT("NoCollision"));
	if (CubeMeshFinder.Succeeded())
	{
		WinnowingScoopMesh->SetStaticMesh(CubeMeshFinder.Object);
	}

	// 3. Billowing particulate dust cloud volume
	DustCloudMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("DustCloudMesh"));
	DustCloudMesh->SetupAttachment(RootComponent);
	DustCloudMesh->SetRelativeLocation(FVector(0.0f, 0.0f, 40.0f));
	DustCloudMesh->SetRelativeScale3D(FVector(0.2f, 0.2f, 0.2f));
	DustCloudMesh->SetCollisionProfileName(TEXT("NoCollision"));
	DustCloudMesh->SetVisibility(false);
	if (SphereMeshFinder.Succeeded())
	{
		DustCloudMesh->SetStaticMesh(SphereMeshFinder.Object);
	}

	// 4. Obscuration zone sphere
	DustSphere = CreateDefaultSubobject<USphereComponent>(TEXT("DustSphere"));
	DustSphere->SetupAttachment(RootComponent);
	DustSphere->SetSphereRadius(280.0f);
	DustSphere->SetCollisionProfileName(TEXT("NoCollision"));

	static ConstructorHelpers::FObjectFinder<USoundBase> RustleSoundFinder(TEXT("/Game/Audio/SFX/SFX_Conceal_Cloth_Rustle.SFX_Conceal_Cloth_Rustle"));
	if (RustleSoundFinder.Succeeded())
	{
		DustReleaseSound = RustleSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> CoughSoundFinder(TEXT("/Game/Audio/SFX/SFX_Drain_Emerge_Gasp.SFX_Drain_Emerge_Gasp"));
	if (CoughSoundFinder.Succeeded())
	{
		WatchmanCoughSound = CoughSoundFinder.Object;
	}
}

void AChaffDustDecoyActor::BeginPlay()
{
	Super::BeginPlay();

	UE_LOG(LogREVOLUTION, Log, TEXT("ChaffDustDecoyActor placed in courtyard granary corner at %s"), *GetActorLocation().ToString());
}

void AChaffDustDecoyActor::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	if (bIsDustActive)
	{
		DustTimer -= DeltaTime;

		// Expand dust cloud billow
		CloudScaleProgress = FMath::Clamp(CloudScaleProgress + (DeltaTime * 1.8f), 0.0f, 1.0f);
		float CurrentScale = FMath::Lerp(0.4f, 2.8f, CloudScaleProgress);
		if (DustCloudMesh)
		{
			DustCloudMesh->SetWorldScale3D(FVector(CurrentScale));
		}

		if (DustTimer <= 0.0f)
		{
			bIsDustActive = false;
			if (DustCloudMesh)
			{
				DustCloudMesh->SetVisibility(false);
			}
			UE_LOG(LogREVOLUTION, Log, TEXT("Wheat chaff dust settled back to ground at %s"), *GetActorLocation().ToString());
		}
	}
}

void AChaffDustDecoyActor::TriggerChaffDust()
{
	if (bIsDischarged) return;

	bIsDischarged = true;
	bIsDustActive = true;
	DustTimer = DustDuration;
	CloudScaleProgress = 0.0f;

	if (DustCloudMesh)
	{
		DustCloudMesh->SetVisibility(true);
	}

	if (DustReleaseSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, DustReleaseSound, GetActorLocation(), 1.0f, 0.9f);
	}

	// Check if any watchman is within immediate range to trigger coughing
	UWorld* World = GetWorld();
	if (World)
	{
		for (TActorIterator<ACurfewPatrolAI> WatchmanIt(World); WatchmanIt; ++WatchmanIt)
		{
			ACurfewPatrolAI* Watchman = *WatchmanIt;
			if (Watchman)
			{
				float Dist = FVector::Dist(Watchman->GetActorLocation(), GetActorLocation());
				if (Dist <= DustRadius * 1.2f)
				{
					if (WatchmanCoughSound)
					{
						UGameplayStatics::PlaySoundAtLocation(this, WatchmanCoughSound, Watchman->GetActorLocation(), 1.0f, 1.15f);
					}
					UE_LOG(LogREVOLUTION, Warning, TEXT("Watchman blinded and coughing in wheat chaff dust cloud at %s!"), *Watchman->GetActorLocation().ToString());
				}
			}
		}
	}

	UE_LOG(LogREVOLUTION, Warning, TEXT("Wheat chaff dust screen triggered at %s! 2.8m visual smoke screen deployed for 7.5s."), *GetActorLocation().ToString());
}

bool AChaffDustDecoyActor::CanInteract_Implementation(const ARevolutionCharacter* Interactor) const
{
	return !bIsDischarged && Interactor != nullptr;
}

FText AChaffDustDecoyActor::GetInteractionPrompt_Implementation() const
{
	return FText::FromString(TEXT("Shake Wheat Chaff Scoop for Dust Screen"));
}

void AChaffDustDecoyActor::OnInteract_Implementation(ARevolutionCharacter* Interactor)
{
	TriggerChaffDust();

	if (Interactor)
	{
		FText Lore = FText::FromString(
			TEXT("Kabir vigorously shakes the woven winnowing tray. A dense, billowing cloud of crushed wheat husk dust and straw chaff erupts across the courtyard corridor.\n\n"
			     "Coinciding with the April Baisakhi harvest, haveli alcoves are stocked with fresh rabi chaff. The thick particulate dust screen hangs in the night air, completely blinding curfew lantern sightlines for several critical seconds.")
		);
		Interactor->StartInspection(FText::FromString(TEXT("Harvest Wheat Chaff Screen (Bhoosa & Chhaj)")), Lore);
	}
}
