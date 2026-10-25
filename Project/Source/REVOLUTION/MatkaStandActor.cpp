// Copyright Epic Games, Inc. All Rights Reserved.

#include "MatkaStandActor.h"
#include "RevolutionCharacter.h"
#include "CurfewPatrolAI.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SceneComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/SoundBase.h"
#include "EngineUtils.h"
#include "REVOLUTION.h"

AMatkaStandActor::AMatkaStandActor()
{
	PrimaryActorTick.bCanEverTick = false;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	static ConstructorHelpers::FObjectFinder<UStaticMesh> CylinderMeshFinder(TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));
	static ConstructorHelpers::FObjectFinder<UStaticMesh> SphereMeshFinder(TEXT("/Engine/BasicShapes/Sphere.Sphere"));

	// 1. Carved teak tripod stand
	TripodStandMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("TripodStandMesh"));
	TripodStandMesh->SetupAttachment(RootComponent);
	TripodStandMesh->SetRelativeLocation(FVector(0.0f, 0.0f, 25.0f));
	TripodStandMesh->SetRelativeScale3D(FVector(0.38f, 0.38f, 0.50f));
	TripodStandMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	if (CylinderMeshFinder.Succeeded())
	{
		TripodStandMesh->SetStaticMesh(CylinderMeshFinder.Object);
	}

	// 2. Bulbous terracotta water pot (Ghara)
	ClayMatkaMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("ClayMatkaMesh"));
	ClayMatkaMesh->SetupAttachment(RootComponent);
	ClayMatkaMesh->SetRelativeLocation(FVector(0.0f, 0.0f, 48.0f));
	ClayMatkaMesh->SetRelativeScale3D(FVector(0.42f, 0.42f, 0.46f));
	ClayMatkaMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	if (SphereMeshFinder.Succeeded())
	{
		ClayMatkaMesh->SetStaticMesh(SphereMeshFinder.Object);
	}

	// 3. Brass drinking ladle (Katori with handle)
	BrassLadleMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("BrassLadleMesh"));
	BrassLadleMesh->SetupAttachment(ClayMatkaMesh);
	BrassLadleMesh->SetRelativeLocation(FVector(12.0f, 0.0f, 22.0f));
	BrassLadleMesh->SetRelativeRotation(FRotator(15.0f, 35.0f, 75.0f));
	BrassLadleMesh->SetRelativeScale3D(FVector(0.12f, 0.12f, 0.42f));
	BrassLadleMesh->SetCollisionProfileName(TEXT("NoCollision"));
	if (CylinderMeshFinder.Succeeded())
	{
		BrassLadleMesh->SetStaticMesh(CylinderMeshFinder.Object);
	}

	// 4. Cool well-water surface
	WaterSurfaceMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("WaterSurfaceMesh"));
	WaterSurfaceMesh->SetupAttachment(ClayMatkaMesh);
	WaterSurfaceMesh->SetRelativeLocation(FVector(0.0f, 0.0f, 18.0f));
	WaterSurfaceMesh->SetRelativeScale3D(FVector(0.70f, 0.70f, 0.04f));
	WaterSurfaceMesh->SetCollisionProfileName(TEXT("NoCollision"));
	if (CylinderMeshFinder.Succeeded())
	{
		WaterSurfaceMesh->SetStaticMesh(CylinderMeshFinder.Object);
	}

	StandTitle = FText::FromString(TEXT("COURTYARD EARTHEN MATKA STAND (GHARA)"));
	StandLore = FText::FromString(
		TEXT("A porous terracotta pot sitting on a carved shisham tripod stand in the haveli courtyard.\n\n"
		     "Filled with fresh well-water drawn at dusk and steeped with dried vetiver roots (khus-khus), natural capillary evaporation through the unglazed clay keeps the water chilled even during sultry April nights.\n\n"
		     "A brass ladle (katori) rests on the rim. Drinking restores Kabir's physical stamina immediately, while tipping the ladle creates a splashing clatter that diverts patrolling watchmen.")
	);

	static ConstructorHelpers::FObjectFinder<USoundBase> SipSoundFinder(TEXT("/Game/Audio/SFX/SFX_Drain_Emerge_Gasp.SFX_Drain_Emerge_Gasp"));
	if (SipSoundFinder.Succeeded())
	{
		DrinkSound = SipSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> ClankSoundFinder(TEXT("/Game/Audio/SFX/SFX_Iron_Latch_Slide.SFX_Iron_Latch_Slide"));
	if (ClankSoundFinder.Succeeded())
	{
		WaterSplashSound = ClankSoundFinder.Object;
	}
}

void AMatkaStandActor::BeginPlay()
{
	Super::BeginPlay();

	UE_LOG(LogREVOLUTION, Log, TEXT("MatkaStandActor placed in courtyard alcove at %s"), *GetActorLocation().ToString());
}

bool AMatkaStandActor::CanInteract_Implementation(const ARevolutionCharacter* Interactor) const
{
	return Interactor != nullptr;
}

FText AMatkaStandActor::GetInteractionPrompt_Implementation() const
{
	return FText::FromString(TEXT("Drink Cool Water [E] / Clank Ladle Decoy"));
}

void AMatkaStandActor::DrinkWater(ARevolutionCharacter* Kabir)
{
	if (!Kabir) return;

	Kabir->CurrentStamina = Kabir->MaxStamina;

	if (DrinkSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, DrinkSound, GetActorLocation(), 0.9f, 1.05f);
	}

	FText DrinkFeedback = FText::FromString(
		TEXT("Kabir lifts the brass ladle, drinking deeply of the sweet, earth-chilled well-water.\n\n"
		     "The cooling draught quenches his parched throat and calms his hammering heart. Kabir's sprint stamina is fully restored (100%).")
	);
	Kabir->StartInspection(StandTitle, DrinkFeedback);

	UE_LOG(LogREVOLUTION, Log, TEXT("Kabir drank from courtyard earthen matka! Stamina restored to %.1f / %.1f."), Kabir->CurrentStamina, Kabir->MaxStamina);
}

void AMatkaStandActor::TriggerWaterDecoy()
{
	if (WaterSplashSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, WaterSplashSound, GetActorLocation(), 1.0f, 1.15f);
	}

	UWorld* World = GetWorld();
	if (World)
	{
		for (TActorIterator<ACurfewPatrolAI> WatchmanIt(World); WatchmanIt; ++WatchmanIt)
		{
			ACurfewPatrolAI* Watchman = *WatchmanIt;
			if (Watchman)
			{
				float Dist = FVector::Dist(Watchman->GetActorLocation(), GetActorLocation());
				if (Dist <= DecoyAlertRadius)
				{
					Watchman->InvestigateSoundLocation(GetActorLocation());
					UE_LOG(LogREVOLUTION, Log, TEXT("Curfew watchman diverted by courtyard matka ladle splash at %s!"), *GetActorLocation().ToString());
				}
			}
		}
	}
}

void AMatkaStandActor::OnInteract_Implementation(ARevolutionCharacter* Interactor)
{
	if (!Interactor) return;

	// If Kabir is low on stamina (< 80%), drinking takes priority; otherwise triggers inspect/drink
	DrinkWater(Interactor);
}
