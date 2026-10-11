// Copyright Epic Games, Inc. All Rights Reserved.

#include "TerracottaHazardActor.h"
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

ATerracottaHazardActor::ATerracottaHazardActor()
{
	PrimaryActorTick.bCanEverTick = true;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	HazardTrigger = CreateDefaultSubobject<UBoxComponent>(TEXT("HazardTrigger"));
	HazardTrigger->SetupAttachment(RootComponent);
	HazardTrigger->SetBoxExtent(FVector(65.0f, 65.0f, 25.0f));
	HazardTrigger->SetCollisionProfileName(TEXT("Trigger"));

	ShardClusterMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("ShardClusterMesh"));
	ShardClusterMesh->SetupAttachment(RootComponent);
	ShardClusterMesh->SetCollisionProfileName(TEXT("NoCollision"));
	ShardClusterMesh->SetRelativeScale3D(FVector(0.35f, 0.35f, 0.08f));

	static ConstructorHelpers::FObjectFinder<UStaticMesh> MeshFinder(TEXT("/Game/Environment/Mohalla/Meshes/SM_Prop_ClayChaiCup_Kulhad.SM_Prop_ClayChaiCup_Kulhad"));
	if (MeshFinder.Succeeded())
	{
		ShardClusterMesh->SetStaticMesh(MeshFinder.Object);
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> CrunchSoundFinder(TEXT("/Game/Audio/SFX/SFX_Pebble_Impact.SFX_Pebble_Impact"));
	if (CrunchSoundFinder.Succeeded())
	{
		ShardCrunchSound = CrunchSoundFinder.Object;
	}
}

void ATerracottaHazardActor::BeginPlay()
{
	Super::BeginPlay();

	if (HazardTrigger)
	{
		HazardTrigger->OnComponentBeginOverlap.AddDynamic(this, &ATerracottaHazardActor::OnHazardOverlap);
	}

	UE_LOG(LogREVOLUTION, Log, TEXT("TerracottaHazardActor spawned at %s"), *GetActorLocation().ToString());
}

void ATerracottaHazardActor::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	// Check if overlapping player is moving upright inside hazard zone
	if (OverlappingPlayer.IsValid() && HazardTrigger)
	{
		if (!HazardTrigger->IsOverlappingActor(OverlappingPlayer.Get()))
		{
			OverlappingPlayer.Reset();
			bPlayerIsInside = false;
			return;
		}

		ARevolutionCharacter* Kabir = OverlappingPlayer.Get();
		const float Speed = Kabir->GetVelocity().Size2D();
		const float CurrentTime = GetWorld()->GetTimeSeconds();

		// If Kabir moves upright with speed > 130cm/s, crunch the earthenware shards!
		if (!Kabir->bIsCrouched && Speed > 130.0f && (CurrentTime - LastCrunchTime >= CrunchCooldown))
		{
			LastCrunchTime = CurrentTime;

			// Play crisp earthenware crunch sound
			if (ShardCrunchSound)
			{
				const float RandomPitch = FMath::RandRange(0.88f, 1.15f);
				UGameplayStatics::PlaySoundAtLocation(this, ShardCrunchSound, GetActorLocation(), 1.0f, RandomPitch);
			}

			UE_LOG(LogREVOLUTION, Warning, TEXT("Kabir crunched brittle terracotta roof tiles at %s! Speed: %.1f"), *GetActorLocation().ToString(), Speed);

			// Alert all curfew patrol watchmen within acoustic alert radius
			int32 AlertedCount = 0;
			for (TActorIterator<ACurfewPatrolAI> It(GetWorld()); It; ++It)
			{
				ACurfewPatrolAI* Watchman = *It;
				if (Watchman)
				{
					const float Dist = FVector::Dist(GetActorLocation(), Watchman->GetActorLocation());
					if (Dist <= AcousticAlertRadius)
					{
						Watchman->InvestigateSoundLocation(GetActorLocation());
						AlertedCount++;
					}
				}
			}

			if (AlertedCount > 0)
			{
				UE_LOG(LogREVOLUTION, Log, TEXT("Terracotta crunch alerted %d Curfew Patrol Watchmen!"), AlertedCount);
			}
		}
	}
}

void ATerracottaHazardActor::OnHazardOverlap(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
	ARevolutionCharacter* Kabir = Cast<ARevolutionCharacter>(OtherActor);
	if (Kabir)
	{
		OverlappingPlayer = Kabir;
		bPlayerIsInside = true;

		// Immediate check on initial entry
		const float Speed = Kabir->GetVelocity().Size2D();
		const float CurrentTime = GetWorld()->GetTimeSeconds();

		if (!Kabir->bIsCrouched && Speed > 130.0f && (CurrentTime - LastCrunchTime >= CrunchCooldown))
		{
			LastCrunchTime = CurrentTime;

			if (ShardCrunchSound)
			{
				UGameplayStatics::PlaySoundAtLocation(this, ShardCrunchSound, GetActorLocation(), 1.0f, 1.0f);
			}

			for (TActorIterator<ACurfewPatrolAI> It(GetWorld()); It; ++It)
			{
				ACurfewPatrolAI* Watchman = *It;
				if (Watchman && FVector::Dist(GetActorLocation(), Watchman->GetActorLocation()) <= AcousticAlertRadius)
				{
					Watchman->InvestigateSoundLocation(GetActorLocation());
				}
			}
		}
	}
}
