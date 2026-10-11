// Copyright Epic Games, Inc. All Rights Reserved.

#include "PariahDogActor.h"
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

APariahDogActor::APariahDogActor()
{
	PrimaryActorTick.bCanEverTick = true;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	static ConstructorHelpers::FObjectFinder<UStaticMesh> SphereMeshFinder(TEXT("/Engine/BasicShapes/Sphere.Sphere"));
	static ConstructorHelpers::FObjectFinder<UStaticMesh> CubeMeshFinder(TEXT("/Engine/BasicShapes/Cube.Cube"));

	// 1. Worn burlap sack / straw bedding mat in alley nook
	BeddingMatMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("BeddingMatMesh"));
	BeddingMatMesh->SetupAttachment(RootComponent);
	BeddingMatMesh->SetRelativeLocation(FVector(0.0f, 0.0f, 2.0f));
	BeddingMatMesh->SetRelativeScale3D(FVector(0.65f, 0.45f, 0.04f));
	BeddingMatMesh->SetCollisionProfileName(TEXT("NoCollision"));
	if (CubeMeshFinder.Succeeded())
	{
		BeddingMatMesh->SetStaticMesh(CubeMeshFinder.Object);
	}

	// 2. Curled sleeping pariah dog body
	DogBodyMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("DogBodyMesh"));
	DogBodyMesh->SetupAttachment(RootComponent);
	DogBodyMesh->SetRelativeLocation(FVector(0.0f, 0.0f, 14.0f));
	DogBodyMesh->SetRelativeScale3D(FVector(0.42f, 0.30f, 0.22f));
	DogBodyMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	if (SphereMeshFinder.Succeeded())
	{
		DogBodyMesh->SetStaticMesh(SphereMeshFinder.Object);
	}

	// 3. Dog head and muzzle (animates when disturbed, barking, or sniffing decoy)
	DogHeadMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("DogHeadMesh"));
	DogHeadMesh->SetupAttachment(DogBodyMesh);
	DogHeadMesh->SetRelativeLocation(FVector(32.0f, 6.0f, 4.0f));
	DogHeadMesh->SetRelativeScale3D(FVector(0.55f, 0.55f, 0.55f));
	DogHeadMesh->SetCollisionProfileName(TEXT("NoCollision"));
	if (SphereMeshFinder.Succeeded())
	{
		DogHeadMesh->SetStaticMesh(SphereMeshFinder.Object);
	}

	// 4. Vigilance sphere
	VigilanceSphere = CreateDefaultSubobject<USphereComponent>(TEXT("VigilanceSphere"));
	VigilanceSphere->SetupAttachment(RootComponent);
	VigilanceSphere->SetSphereRadius(550.0f);
	VigilanceSphere->SetCollisionProfileName(TEXT("NoCollision"));

	static ConstructorHelpers::FObjectFinder<USoundBase> BarkSoundFinder(TEXT("/Game/Audio/SFX/SFX_Watchman_Callout.SFX_Watchman_Callout"));
	if (BarkSoundFinder.Succeeded())
	{
		BarkSound = BarkSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> GrowlSoundFinder(TEXT("/Game/Audio/SFX/SFX_Drain_Emerge_Gasp.SFX_Drain_Emerge_Gasp"));
	if (GrowlSoundFinder.Succeeded())
	{
		GrowlSound = GrowlSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> SootheSoundFinder(TEXT("/Game/Audio/SFX/SFX_Conceal_Cloth_Rustle.SFX_Conceal_Cloth_Rustle"));
	if (SootheSoundFinder.Succeeded())
	{
		SootheSound = SootheSoundFinder.Object;
	}
}

void APariahDogActor::BeginPlay()
{
	Super::BeginPlay();

	UE_LOG(LogREVOLUTION, Log, TEXT("PariahDogActor resting in alleyway shadows at %s"), *GetActorLocation().ToString());
}

void APariahDogActor::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	if (bIsPacified)
	{
		CurrentState = EPariahDogState::Pacified;
		if (DogHeadMesh)
		{
			DogHeadMesh->SetRelativeRotation(FRotator::ZeroRotator);
		}
		return;
	}

	// Distracted by pebble impact decoy
	if (bIsDistracted)
	{
		DistractionTimer -= DeltaTime;
		if (DogHeadMesh)
		{
			FVector DirToDecoy = (DecoyTargetLocation - GetActorLocation()).GetSafeNormal2D();
			float YawOffset = DirToDecoy.Rotation().Yaw - GetActorRotation().Yaw;
			DogHeadMesh->SetRelativeRotation(FRotator(18.0f, YawOffset, 0.0f));
		}

		if (DistractionTimer <= 0.0f)
		{
			bIsDistracted = false;
			CurrentState = EPariahDogState::Sleeping;
			if (DogHeadMesh)
			{
				DogHeadMesh->SetRelativeRotation(FRotator::ZeroRotator);
			}
			UE_LOG(LogREVOLUTION, Log, TEXT("Pariah dog returned to sleeping after pebble investigation at %s"), *GetActorLocation().ToString());
		}
		return;
	}

	UWorld* World = GetWorld();
	if (!World) return;

	ARevolutionCharacter* Player = Cast<ARevolutionCharacter>(UGameplayStatics::GetPlayerCharacter(this, 0));
	if (!Player) return;

	float DistToPlayer = FVector::Dist(GetActorLocation(), Player->GetActorLocation());

	if (CurrentState == EPariahDogState::Barking)
	{
		BarkTimer -= DeltaTime;
		BarkCooldownTimer += DeltaTime;

		if (DogHeadMesh)
		{
			DogHeadMesh->SetRelativeRotation(FRotator(35.0f, FMath::Sin(BarkCooldownTimer * 8.0f) * 12.0f, 0.0f));
		}

		if (BarkCooldownTimer >= 2.0f)
		{
			BarkCooldownTimer = 0.0f;
			if (BarkSound)
			{
				UGameplayStatics::PlaySoundAtLocation(this, BarkSound, GetActorLocation(), 1.0f, FMath::RandRange(1.1f, 1.25f));
			}
			AlertNearbyWatchmen();
		}

		if (BarkTimer <= 0.0f)
		{
			// Check if player has backed away or is crouching
			if (Player->bIsCrouched || DistToPlayer > WalkAlertRadius)
			{
				CurrentState = EPariahDogState::Disturbed;
				DisturbedTimer = 1.5f;
				if (DogHeadMesh)
				{
					DogHeadMesh->SetRelativeRotation(FRotator(15.0f, 0.0f, 0.0f));
				}
				UE_LOG(LogREVOLUTION, Log, TEXT("Pariah dog stopped barking, remaining watchful at %s"), *GetActorLocation().ToString());
			}
			else
			{
				// Still standing right in front of dog - continue barking
				BarkTimer = 3.0f;
			}
		}
		return;
	}

	if (CurrentState == EPariahDogState::Disturbed)
	{
		if (Player->bIsSprinting && DistToPlayer <= SprintAlertRadius)
		{
			TriggerBarkAlert();
			return;
		}

		if (!Player->bIsCrouched && DistToPlayer <= WalkAlertRadius)
		{
			DisturbedTimer += DeltaTime;
			if (DisturbedTimer >= 1.2f)
			{
				TriggerBarkAlert();
			}
		}
		else
		{
			DisturbedTimer -= DeltaTime * 0.7f;
			if (DisturbedTimer <= 0.0f)
			{
				CurrentState = EPariahDogState::Sleeping;
				if (DogHeadMesh)
				{
					DogHeadMesh->SetRelativeRotation(FRotator::ZeroRotator);
				}
				UE_LOG(LogREVOLUTION, Log, TEXT("Pariah dog calmed down and returned to sleep at %s"), *GetActorLocation().ToString());
			}
		}
		return;
	}

	if (CurrentState == EPariahDogState::Sleeping)
	{
		// Check sprinting footsteps
		if (Player->bIsSprinting && DistToPlayer <= SprintAlertRadius)
		{
			UE_LOG(LogREVOLUTION, Warning, TEXT("Kabir's sprinting footsteps startled sleeping pariah dog at %s!"), *GetActorLocation().ToString());
			TriggerBarkAlert();
			return;
		}

		// Check upright walking within immediate perimeter
		if (!Player->bIsCrouched && DistToPlayer <= WalkAlertRadius)
		{
			CurrentState = EPariahDogState::Disturbed;
			DisturbedTimer = 0.3f;
			if (DogHeadMesh)
			{
				DogHeadMesh->SetRelativeRotation(FRotator(18.0f, 0.0f, 0.0f));
			}
			if (GrowlSound)
			{
				UGameplayStatics::PlaySoundAtLocation(this, GrowlSound, GetActorLocation(), 0.85f, 0.9f);
			}
			UE_LOG(LogREVOLUTION, Log, TEXT("Pariah dog stirred by upright footsteps at %s (Growling)"), *GetActorLocation().ToString());
		}
	}
}

void APariahDogActor::TriggerBarkAlert()
{
	CurrentState = EPariahDogState::Barking;
	BarkTimer = 4.5f;
	BarkCooldownTimer = 0.0f;

	if (DogHeadMesh)
	{
		DogHeadMesh->SetRelativeRotation(FRotator(35.0f, 0.0f, 0.0f));
	}

	if (BarkSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, BarkSound, GetActorLocation(), 1.0f, 1.15f);
	}

	AlertNearbyWatchmen();

	UE_LOG(LogREVOLUTION, Warning, TEXT("Pariah dog barking fiercely at %s! Alerting colonial curfew watchmen!"), *GetActorLocation().ToString());
}

void APariahDogActor::AlertNearbyWatchmen()
{
	UWorld* World = GetWorld();
	if (!World) return;

	for (TActorIterator<ACurfewPatrolAI> WatchmanIt(World); WatchmanIt; ++WatchmanIt)
	{
		ACurfewPatrolAI* Watchman = *WatchmanIt;
		if (Watchman)
		{
			float DistToWatchman = FVector::Dist(Watchman->GetActorLocation(), GetActorLocation());
			if (DistToWatchman <= WatchmanAlertRadius)
			{
				Watchman->InvestigateSoundLocation(GetActorLocation());
				UE_LOG(LogREVOLUTION, Warning, TEXT("Curfew watchman at %s heard dog barking! Diverting patrol to investigate."), *Watchman->GetActorLocation().ToString());
			}
		}
	}
}

void APariahDogActor::DistractWithPebble(const FVector& DecoyLocation)
{
	if (bIsPacified) return;

	bIsDistracted = true;
	CurrentState = EPariahDogState::Distracted;
	DistractionTimer = 8.5f;
	DecoyTargetLocation = DecoyLocation;

	UE_LOG(LogREVOLUTION, Log, TEXT("Pariah dog diverted by clay marble clatter towards %s! (Distracted for 8.5s)"), *DecoyLocation.ToString());
}

void APariahDogActor::SootheDog(ARevolutionCharacter* Kabir)
{
	if (!Kabir) return;

	bIsPacified = true;
	bIsDistracted = false;
	CurrentState = EPariahDogState::Pacified;

	if (DogHeadMesh)
	{
		DogHeadMesh->SetRelativeRotation(FRotator::ZeroRotator);
	}

	if (SootheSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, SootheSound, GetActorLocation(), 0.9f, 1.0f);
	}

	FText DogLore = FText::FromString(
		TEXT("Crouching low in the doorframe shadows, Kabir gently clicks his tongue and strokes the stray dog's dusty flank.\n\n"
		     "Recognizing the familiar scent of a mohalla artisan's child rather than the leather boots of colonial constables, the dog lets out a soft sigh and curls back into deep sleep. Kabir can now pass this alleyway corner in total silence.")
	);
	Kabir->StartInspection(FText::FromString(TEXT("Sleeping Mohalla Stray Dog (Desi Kutta)")), DogLore);

	UE_LOG(LogREVOLUTION, Log, TEXT("Kabir softly soothed the pariah dog at %s. Pacified for the night."), *GetActorLocation().ToString());
}

bool APariahDogActor::CanInteract_Implementation(const ARevolutionCharacter* Interactor) const
{
	return Interactor && Interactor->bIsCrouched && !bIsPacified && CurrentState != EPariahDogState::Barking;
}

FText APariahDogActor::GetInteractionPrompt_Implementation() const
{
	return FText::FromString(TEXT("Softly Shush Sleeping Mohalla Dog"));
}

void APariahDogActor::OnInteract_Implementation(ARevolutionCharacter* Interactor)
{
	SootheDog(Interactor);
}
