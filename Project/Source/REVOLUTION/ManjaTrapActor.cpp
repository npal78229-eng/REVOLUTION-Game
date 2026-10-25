// Copyright Epic Games, Inc. All Rights Reserved.

#include "ManjaTrapActor.h"
#include "RevolutionCharacter.h"
#include "CurfewPatrolAI.h"
#include "Components/StaticMeshComponent.h"
#include "Components/BoxComponent.h"
#include "Components/SceneComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/SoundBase.h"
#include "EngineUtils.h"
#include "REVOLUTION.h"

AManjaTrapActor::AManjaTrapActor()
{
	PrimaryActorTick.bCanEverTick = false;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	static ConstructorHelpers::FObjectFinder<UStaticMesh> CubeMeshFinder(TEXT("/Engine/BasicShapes/Cube.Cube"));
	static ConstructorHelpers::FObjectFinder<UStaticMesh> CylinderMeshFinder(TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));

	// 1. Left anchor parapet brick pillar
	PostLeftMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("PostLeftMesh"));
	PostLeftMesh->SetupAttachment(RootComponent);
	PostLeftMesh->SetRelativeLocation(FVector(0.0f, -85.0f, 25.0f));
	PostLeftMesh->SetRelativeScale3D(FVector(0.18f, 0.18f, 0.50f));
	PostLeftMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	if (CubeMeshFinder.Succeeded())
	{
		PostLeftMesh->SetStaticMesh(CubeMeshFinder.Object);
	}

	// 2. Right anchor parapet brick pillar
	PostRightMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("PostRightMesh"));
	PostRightMesh->SetupAttachment(RootComponent);
	PostRightMesh->SetRelativeLocation(FVector(0.0f, 85.0f, 25.0f));
	PostRightMesh->SetRelativeScale3D(FVector(0.18f, 0.18f, 0.50f));
	PostRightMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	if (CubeMeshFinder.Succeeded())
	{
		PostRightMesh->SetStaticMesh(CubeMeshFinder.Object);
	}

	// 3. Taut glass-powder coated kite string line (Manja)
	StringLineMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("StringLineMesh"));
	StringLineMesh->SetupAttachment(RootComponent);
	StringLineMesh->SetRelativeLocation(FVector(0.0f, 0.0f, 38.0f));
	StringLineMesh->SetRelativeScale3D(FVector(0.015f, 1.70f, 0.015f));
	StringLineMesh->SetCollisionProfileName(TEXT("NoCollision"));
	if (CubeMeshFinder.Succeeded())
	{
		StringLineMesh->SetStaticMesh(CubeMeshFinder.Object);
	}

	// 4. Discarded wooden kite spool (Charkhi)
	SpoolMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("SpoolMesh"));
	SpoolMesh->SetupAttachment(RootComponent);
	SpoolMesh->SetRelativeLocation(FVector(8.0f, -75.0f, 6.0f));
	SpoolMesh->SetRelativeRotation(FRotator(0.0f, 25.0f, 85.0f));
	SpoolMesh->SetRelativeScale3D(FVector(0.14f, 0.14f, 0.22f));
	SpoolMesh->SetCollisionProfileName(TEXT("NoCollision"));
	if (CylinderMeshFinder.Succeeded())
	{
		SpoolMesh->SetStaticMesh(CylinderMeshFinder.Object);
	}

	// 5. Snag overlap detection trigger box
	SnagTrigger = CreateDefaultSubobject<UBoxComponent>(TEXT("SnagTrigger"));
	SnagTrigger->SetupAttachment(RootComponent);
	SnagTrigger->SetRelativeLocation(FVector(0.0f, 0.0f, 40.0f));
	SnagTrigger->SetBoxExtent(FVector(20.0f, 85.0f, 28.0f));
	SnagTrigger->SetCollisionProfileName(TEXT("OverlapAllDynamic"));
	SnagTrigger->OnComponentBeginOverlap.AddDynamic(this, &AManjaTrapActor::OnOverlapBegin);

	static ConstructorHelpers::FObjectFinder<USoundBase> SnapSoundFinder(TEXT("/Game/Audio/SFX/SFX_Pebble_Throw.SFX_Pebble_Throw"));
	if (SnapSoundFinder.Succeeded())
	{
		StringSnapSound = SnapSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> CollectSoundFinder(TEXT("/Game/Audio/SFX/SFX_Conceal_Cloth_Rustle.SFX_Conceal_Cloth_Rustle"));
	if (CollectSoundFinder.Succeeded())
	{
		CollectTwineSound = CollectSoundFinder.Object;
	}
}

void AManjaTrapActor::BeginPlay()
{
	Super::BeginPlay();

	UE_LOG(LogREVOLUTION, Log, TEXT("ManjaTrapActor strung across rooftop parapet at %s"), *GetActorLocation().ToString());
}

void AManjaTrapActor::OnOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
	if (bIsDisarmed) return;

	ARevolutionCharacter* Kabir = Cast<ARevolutionCharacter>(OtherActor);
	if (!Kabir) return;

	// If Kabir is crouching, he slips underneath the taut kite line safely without snagging
	if (Kabir->bIsCrouched)
	{
		return;
	}

	// Kabir walked upright or sprinted into the glass kite string!
	bIsDisarmed = true;

	if (StringLineMesh)
	{
		StringLineMesh->SetVisibility(false);
	}

	if (StringSnapSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, StringSnapSound, GetActorLocation(), 1.0f, 1.35f);
	}

	// Alert patrol watchman below on ground
	UWorld* World = GetWorld();
	if (World)
	{
		for (TActorIterator<ACurfewPatrolAI> WatchmanIt(World); WatchmanIt; ++WatchmanIt)
		{
			ACurfewPatrolAI* Watchman = *WatchmanIt;
			if (Watchman)
			{
				float Dist = FVector::Dist(Watchman->GetActorLocation(), GetActorLocation());
				if (Dist <= AlertRadiusWatchman)
				{
					Watchman->InvestigateSoundLocation(GetActorLocation());
					UE_LOG(LogREVOLUTION, Warning, TEXT("Watchman alerted by rooftop kite line snap at %s!"), *GetActorLocation().ToString());
				}
			}
		}
	}

	UE_LOG(LogREVOLUTION, Warning, TEXT("Kabir snagged on rooftop glass kite line (Manja) at %s! Twang alerted watchman."), *GetActorLocation().ToString());
}

void AManjaTrapActor::DisarmTrap(ARevolutionCharacter* Kabir)
{
	if (bIsDisarmed || !Kabir) return;

	bIsDisarmed = true;

	if (StringLineMesh)
	{
		StringLineMesh->SetVisibility(false);
	}

	if (CollectTwineSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, CollectTwineSound, GetActorLocation(), 0.9f);
	}

	FText DisarmLore = FText::FromString(
		TEXT("Carefully sliding his pocket knife along the terracotta brick coping, Kabir severs and rolls up the discarded Basant kite twine.\n\n"
		     "In Punjabi spring festivals, cotton thread was steeped in crushed glass, rice paste, and gum acacia to slice through rival kites in sky battles. Tangled on rooftops after the festival, these razor-sharp lines pose a nocturnal hazard to couriers, but disarmed, the strong cord is safely secured in Kabir's satchel.")
	);
	Kabir->StartInspection(FText::FromString(TEXT("Glass-Coated Kite Line (Basant Manja)")), DisarmLore);

	UE_LOG(LogREVOLUTION, Log, TEXT("Kabir quietly disarmed rooftop kite line hazard at %s."), *GetActorLocation().ToString());
}

bool AManjaTrapActor::CanInteract_Implementation(const ARevolutionCharacter* Interactor) const
{
	return !bIsDisarmed && Interactor != nullptr;
}

FText AManjaTrapActor::GetInteractionPrompt_Implementation() const
{
	return FText::FromString(TEXT("Carefully Untangle & Disarm Glass Kite Line"));
}

void AManjaTrapActor::OnInteract_Implementation(ARevolutionCharacter* Interactor)
{
	DisarmTrap(Interactor);
}
