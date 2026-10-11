// Copyright Epic Games, Inc. All Rights Reserved.

#include "PebbleProjectile.h"
#include "CurfewPatrolAI.h"
#include "PigeonFlockActor.h"
#include "Components/SphereComponent.h"
#include "Components/StaticMeshComponent.h"
#include "GameFramework/ProjectileMovementComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/SoundBase.h"
#include "EngineUtils.h"
#include "REVOLUTION.h"

APebbleProjectile::APebbleProjectile()
{
	PrimaryActorTick.bCanEverTick = false;

	CollisionComponent = CreateDefaultSubobject<USphereComponent>(TEXT("SphereComp"));
	CollisionComponent->InitSphereRadius(8.0f);
	CollisionComponent->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	CollisionComponent->OnComponentHit.AddDynamic(this, &APebbleProjectile::OnHit);
	CollisionComponent->SetNotifyRigidBodyCollision(true);
	RootComponent = CollisionComponent;

	MeshComponent = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("MeshComp"));
	MeshComponent->SetupAttachment(RootComponent);
	MeshComponent->SetRelativeScale3D(FVector(0.08f, 0.08f, 0.08f));
	MeshComponent->SetCollisionProfileName(TEXT("NoCollision"));

	static ConstructorHelpers::FObjectFinder<UStaticMesh> MeshFinder(TEXT("/Engine/BasicShapes/Sphere.Sphere"));
	if (MeshFinder.Succeeded())
	{
		MeshComponent->SetStaticMesh(MeshFinder.Object);
	}

	ProjectileMovement = CreateDefaultSubobject<UProjectileMovementComponent>(TEXT("ProjectileComp"));
	ProjectileMovement->UpdatedComponent = CollisionComponent;
	ProjectileMovement->InitialSpeed = 1350.0f;
	ProjectileMovement->MaxSpeed = 1500.0f;
	ProjectileMovement->bRotationFollowsVelocity = true;
	ProjectileMovement->bShouldBounce = true;
	ProjectileMovement->Bounciness = 0.45f;
	ProjectileMovement->Friction = 0.6f;
	ProjectileMovement->ProjectileGravityScale = 1.15f;

	static ConstructorHelpers::FObjectFinder<USoundBase> SoundFinder(TEXT("/Game/Audio/SFX/SFX_Pebble_Impact.SFX_Pebble_Impact"));
	if (SoundFinder.Succeeded())
	{
		ImpactSound = SoundFinder.Object;
	}

	InitialLifeSpan = 4.0f;
}

void APebbleProjectile::BeginPlay()
{
	Super::BeginPlay();
}

void APebbleProjectile::OnHit(UPrimitiveComponent* HitComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, FVector NormalImpulse, const FHitResult& Hit)
{
	if (ImpactSound)
	{
		float PitchMod = FMath::RandRange(0.92f, 1.08f);
		UGameplayStatics::PlaySoundAtLocation(this, ImpactSound, Hit.ImpactPoint, 0.95f, PitchMod);
	}

	if (!bHasAlertedWatchman)
	{
		bHasAlertedWatchman = true;

		UWorld* World = GetWorld();
		if (World)
		{
			for (TActorIterator<ACurfewPatrolAI> It(World); It; ++It)
			{
				ACurfewPatrolAI* Watchman = *It;
				if (Watchman)
				{
					float Dist = FVector::Dist(Watchman->GetActorLocation(), Hit.ImpactPoint);
					if (Dist <= SoundAlertRadius)
					{
						Watchman->InvestigateSoundLocation(Hit.ImpactPoint);
					}
				}
			}

			for (TActorIterator<APigeonFlockActor> FlockIt(World); FlockIt; ++FlockIt)
			{
				APigeonFlockActor* Flock = *FlockIt;
				if (Flock && !Flock->HasScattered())
				{
					float DistToFlock = FVector::Dist(Flock->GetActorLocation(), Hit.ImpactPoint);
					if (DistToFlock <= 250.0f)
					{
						Flock->TriggerScatterFlock();
					}
				}
			}
		}

		UE_LOG(LogREVOLUTION, Log, TEXT("Pebble impact clatter at %s"), *Hit.ImpactPoint.ToString());
	}
}
