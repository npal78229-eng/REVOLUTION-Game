// Copyright Epic Games, Inc. All Rights Reserved.

#include "HandpumpActor.h"
#include "RevolutionCharacter.h"
#include "CurfewPatrolAI.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SceneComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/SoundBase.h"
#include "EngineUtils.h"
#include "REVOLUTION.h"

AHandpumpActor::AHandpumpActor()
{
	PrimaryActorTick.bCanEverTick = true;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	static ConstructorHelpers::FObjectFinder<UStaticMesh> CylMeshFinder(TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));
	static ConstructorHelpers::FObjectFinder<UStaticMesh> CubeMeshFinder(TEXT("/Engine/BasicShapes/Cube.Cube"));

	// Stone masonry plinth base
	BasePedestalMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("BasePedestalMesh"));
	BasePedestalMesh->SetupAttachment(RootComponent);
	BasePedestalMesh->SetRelativeScale3D(FVector(0.55f, 0.55f, 0.12f));
	BasePedestalMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	if (CylMeshFinder.Succeeded())
	{
		BasePedestalMesh->SetStaticMesh(CylMeshFinder.Object);
	}

	// Vertical Cast-Iron Cylinder Body
	CylinderBodyMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("CylinderBodyMesh"));
	CylinderBodyMesh->SetupAttachment(RootComponent);
	CylinderBodyMesh->SetRelativeLocation(FVector(0.0f, 0.0f, 12.0f));
	CylinderBodyMesh->SetRelativeScale3D(FVector(0.22f, 0.22f, 0.75f));
	CylinderBodyMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	if (CylMeshFinder.Succeeded())
	{
		CylinderBodyMesh->SetStaticMesh(CylMeshFinder.Object);
	}

	// Water discharge spout
	WaterSpoutMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("WaterSpoutMesh"));
	WaterSpoutMesh->SetupAttachment(CylinderBodyMesh);
	WaterSpoutMesh->SetRelativeLocation(FVector(60.0f, 0.0f, 25.0f));
	WaterSpoutMesh->SetRelativeRotation(FRotator(25.0f, 0.0f, 0.0f));
	WaterSpoutMesh->SetRelativeScale3D(FVector(0.40f, 0.25f, 0.15f));
	WaterSpoutMesh->SetCollisionProfileName(TEXT("NoCollision"));
	if (CylMeshFinder.Succeeded())
	{
		WaterSpoutMesh->SetStaticMesh(CylMeshFinder.Object);
	}

	// Rocker Lever Arm (pivot at top)
	LeverArmMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("LeverArmMesh"));
	LeverArmMesh->SetupAttachment(CylinderBodyMesh);
	LeverArmMesh->SetRelativeLocation(FVector(-35.0f, 0.0f, 85.0f));
	LeverArmMesh->SetRelativeScale3D(FVector(0.70f, 0.08f, 0.08f));
	LeverArmMesh->SetCollisionProfileName(TEXT("NoCollision"));
	if (CubeMeshFinder.Succeeded())
	{
		LeverArmMesh->SetStaticMesh(CubeMeshFinder.Object);
	}

	RestLeverRotation = FRotator(18.0f, 0.0f, 0.0f);
	DepressedLeverRotation = FRotator(-26.0f, 0.0f, 0.0f);
	LeverArmMesh->SetRelativeRotation(RestLeverRotation);

	static ConstructorHelpers::FObjectFinder<USoundBase> SoundFinder(TEXT("/Game/Audio/SFX/SFX_Iron_Latch_Slide.SFX_Iron_Latch_Slide"));
	if (SoundFinder.Succeeded())
	{
		PumpStrokeSound = SoundFinder.Object;
	}
}

void AHandpumpActor::BeginPlay()
{
	Super::BeginPlay();

	UE_LOG(LogREVOLUTION, Log, TEXT("HandpumpActor spawned at %s"), *GetActorLocation().ToString());
}

void AHandpumpActor::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	if (bIsPumping)
	{
		LeverAnimationProgress += DeltaTime * 2.2f;

		// Smooth stroke: down then back up
		float StrokeCurve = FMath::Sin(FMath::Clamp(LeverAnimationProgress, 0.0f, 1.0f) * PI);
		FRotator CurrentRot = FMath::Lerp(RestLeverRotation, DepressedLeverRotation, StrokeCurve);
		LeverArmMesh->SetRelativeRotation(CurrentRot);

		if (LeverAnimationProgress >= 1.0f)
		{
			bIsPumping = false;
			LeverAnimationProgress = 0.0f;
			LeverArmMesh->SetRelativeRotation(RestLeverRotation);
		}
	}
}

bool AHandpumpActor::CanInteract_Implementation(const ARevolutionCharacter* Interactor) const
{
	const float CurrentTime = GetWorld() ? GetWorld()->GetTimeSeconds() : 0.0f;
	return (CurrentTime - LastPumpTime >= PumpCooldown) && !bIsPumping;
}

FText AHandpumpActor::GetInteractionPrompt_Implementation() const
{
	const float CurrentTime = GetWorld() ? GetWorld()->GetTimeSeconds() : 0.0f;
	if (CurrentTime - LastPumpTime < PumpCooldown)
	{
		return FText::FromString(TEXT("Handpump (Pressure Building...)"));
	}
	return InteractionPrompt;
}

void AHandpumpActor::OnInteract_Implementation(ARevolutionCharacter* Interactor)
{
	const float CurrentTime = GetWorld()->GetTimeSeconds();
	if (CurrentTime - LastPumpTime < PumpCooldown || bIsPumping)
	{
		return;
	}

	LastPumpTime = CurrentTime;
	bIsPumping = true;
	LeverAnimationProgress = 0.0f;

	// 1. Play mechanical lever stroke sound
	if (PumpStrokeSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, PumpStrokeSound, GetActorLocation(), 1.15f, 0.85f);
	}

	UE_LOG(LogREVOLUTION, Warning, TEXT("Kabir operated Cast-Iron Handpump at %s! Emitting acoustic distraction (Radius: %.0fcm)"), *GetActorLocation().ToString(), AcousticAlertRadius);

	// 2. Alert curfew watchmen in acoustic radius
	int32 AlertedWatchmen = 0;
	for (TActorIterator<ACurfewPatrolAI> It(GetWorld()); It; ++It)
	{
		ACurfewPatrolAI* Watchman = *It;
		if (Watchman)
		{
			float Dist = FVector::Dist(GetActorLocation(), Watchman->GetActorLocation());
			if (Dist <= AcousticAlertRadius)
			{
				Watchman->InvestigateSoundLocation(GetActorLocation());
				AlertedWatchmen++;
			}
		}
	}

	UE_LOG(LogREVOLUTION, Log, TEXT("Handpump acoustic distraction lured %d Watchmen towards courtyard!"), AlertedWatchmen);

	// 3. First-time inspection lore card
	if (Interactor && Interactor->GetVelocity().SizeSquared() < 100.0f)
	{
		Interactor->StartInspection(
			PumpName,
			FText::FromString(TEXT("A heavy British-manufactured cast-iron courtyard handpump (nalka). In 1919 Punjab, domestic groundwater came entirely from these hand pumps and masonry wells. The loud mechanical clanking of its rocker lever and cascading water can be heard across adjoining alleyways, making it an effective acoustic distraction against curfew patrols."))
		);
	}
}
