// Copyright Epic Games, Inc. All Rights Reserved.

#include "PigeonFlockActor.h"
#include "RevolutionCharacter.h"
#include "CurfewPatrolAI.h"
#include "Components/SceneComponent.h"
#include "Components/StaticMeshComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Sound/SoundBase.h"
#include "Kismet/GameplayStatics.h"
#include "EngineUtils.h"
#include "REVOLUTION.h"

APigeonFlockActor::APigeonFlockActor()
{
	PrimaryActorTick.bCanEverTick = true;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	static ConstructorHelpers::FObjectFinder<UStaticMesh> BirdMeshFinder(TEXT("/Game/Environment/Mohalla/Meshes/SM_Prop_ClayChaiCup_Kulhad.SM_Prop_ClayChaiCup_Kulhad"));
	static ConstructorHelpers::FObjectFinder<USoundBase> ScatterSoundFinder(TEXT("/Game/Audio/SFX/SFX_Pigeon_Flock_Scatter.SFX_Pigeon_Flock_Scatter"));
	static ConstructorHelpers::FObjectFinder<USoundBase> CooSoundFinder(TEXT("/Game/Audio/SFX/SFX_Pigeon_Coo_Calm.SFX_Pigeon_Coo_Calm"));

	if (ScatterSoundFinder.Succeeded())
	{
		ScatterSound = ScatterSoundFinder.Object;
	}

	if (CooSoundFinder.Succeeded())
	{
		CalmCooSound = CooSoundFinder.Object;
	}

	// Create 5 roosting bird mesh representations along a parapet ledge
	const FVector RelativePositions[] = {
		FVector(-45.0f, -6.0f, 0.0f),
		FVector(-20.0f,  4.0f, 0.0f),
		FVector(  5.0f, -3.0f, 0.0f),
		FVector( 28.0f,  6.0f, 0.0f),
		FVector( 52.0f, -2.0f, 0.0f)
	};

	for (int32 i = 0; i < 5; ++i)
	{
		FName CompName = *FString::Printf(TEXT("BirdMesh_%d"), i);
		UStaticMeshComponent* Bird = CreateDefaultSubobject<UStaticMeshComponent>(CompName);
		Bird->SetupAttachment(RootComponent);
		Bird->SetRelativeLocation(RelativePositions[i]);
		Bird->SetRelativeScale3D(FVector(0.18f, 0.14f, 0.16f));
		Bird->SetCollisionProfileName(TEXT("NoCollision"));

		if (BirdMeshFinder.Succeeded())
		{
			Bird->SetStaticMesh(BirdMeshFinder.Object);
		}

		BirdMeshes.Add(Bird);
	}
}

void APigeonFlockActor::BeginPlay()
{
	Super::BeginPlay();

	BirdInitialOffsets.Empty();
	BirdFlightVelocities.Empty();

	for (int32 i = 0; i < BirdMeshes.Num(); ++i)
	{
		if (BirdMeshes[i])
		{
			BirdInitialOffsets.Add(BirdMeshes[i]->GetRelativeLocation());

			// Randomized escape flight velocity (upward and outward into nocturnal sky)
			float Angle = FMath::DegreesToRadians(FMath::RandRange(20.0f, 160.0f));
			float SpeedHoriz = FMath::RandRange(240.0f, 420.0f);
			float SpeedVert = FMath::RandRange(380.0f, 560.0f);

			FVector Vel(
				FMath::Cos(Angle) * SpeedHoriz,
				FMath::Sin(Angle) * SpeedHoriz,
				SpeedVert
			);
			BirdFlightVelocities.Add(Vel);
		}
	}

	NextCooInterval = FMath::RandRange(8.0f, 16.0f);
}

void APigeonFlockActor::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	if (bIsScatterTriggered)
	{
		ScatterFlightTimer += DeltaTime;

		for (int32 i = 0; i < BirdMeshes.Num(); ++i)
		{
			if (BirdMeshes[i] && i < BirdInitialOffsets.Num() && i < BirdFlightVelocities.Num())
			{
				FVector NewOffset = BirdInitialOffsets[i] + (BirdFlightVelocities[i] * ScatterFlightTimer);

				// Add rapid wing flap vertical flutter
				NewOffset.Z += FMath::Sin((ScatterFlightTimer * 28.0f) + (float)i * 1.5f) * 8.0f;

				BirdMeshes[i]->SetRelativeLocation(NewOffset);

				// Pitch upwards into flight
				FRotator FlightRot(35.0f, BirdFlightVelocities[i].Rotation().Yaw, 0.0f);
				BirdMeshes[i]->SetRelativeRotation(FlightRot);
			}
		}

		if (ScatterFlightTimer >= FlightDuration)
		{
			for (UStaticMeshComponent* Bird : BirdMeshes)
			{
				if (Bird)
				{
					Bird->SetVisibility(false);
				}
			}

			SetActorTickEnabled(false);
		}
		return;
	}

	// 1. Ambient nocturnal coo timer
	CooTimer += DeltaTime;
	if (CooTimer >= NextCooInterval)
	{
		CooTimer = 0.0f;
		NextCooInterval = FMath::RandRange(14.0f, 26.0f);

		if (CalmCooSound)
		{
			UGameplayStatics::PlaySoundAtLocation(this, CalmCooSound, GetActorLocation(), 0.65f, FMath::RandRange(0.95f, 1.05f));
		}
	}

	// 2. Player proximity & movement state check
	ARevolutionCharacter* Kabir = Cast<ARevolutionCharacter>(UGameplayStatics::GetPlayerCharacter(this, 0));
	if (Kabir)
	{
		float Dist = FVector::Dist(GetActorLocation(), Kabir->GetActorLocation());

		// Determine spook threshold
		float SpookRadius = WalkSpookRadius;
		if (Kabir->bIsSprinting)
		{
			SpookRadius = SprintSpookRadius;
		}
		else if (Kabir->bIsCrouched)
		{
			SpookRadius = CrouchSpookRadius;
		}

		if (Dist <= SpookRadius)
		{
			TriggerScatterFlock();
		}
	}
}

void APigeonFlockActor::TriggerScatterFlock()
{
	if (bIsScatterTriggered) return;

	bIsScatterTriggered = true;
	ScatterFlightTimer = 0.0f;

	if (ScatterSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, ScatterSound, GetActorLocation(), 1.0f, FMath::RandRange(0.96f, 1.04f));
	}

	// Alert all nearby curfew patrol watchmen of the sudden rooftop wing flutter disturbance
	int32 AlertedCount = 0;
	for (TActorIterator<ACurfewPatrolAI> It(GetWorld()); It; ++It)
	{
		ACurfewPatrolAI* Watchman = *It;
		if (Watchman)
		{
			float DistToWatchman = FVector::Dist(GetActorLocation(), Watchman->GetActorLocation());
			if (DistToWatchman <= AudibleAlertRadius)
			{
				Watchman->InvestigateSoundLocation(GetActorLocation());
				AlertedCount++;
			}
		}
	}

	UE_LOG(LogREVOLUTION, Log, TEXT("Haveli rooftop pigeon flock startled! Flew off into the night. Alerted %d watchmen below."), AlertedCount);
}
