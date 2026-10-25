// Copyright Epic Games, Inc. All Rights Reserved.

#include "CheckpointBarrierActor.h"
#include "RevolutionCharacter.h"
#include "Components/StaticMeshComponent.h"
#include "Components/PointLightComponent.h"
#include "Components/SceneComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/SoundBase.h"
#include "REVOLUTION.h"

ACheckpointBarrierActor::ACheckpointBarrierActor()
{
	PrimaryActorTick.bCanEverTick = true;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	static ConstructorHelpers::FObjectFinder<UStaticMesh> CubeMeshFinder(TEXT("/Engine/BasicShapes/Cube.Cube"));
	static ConstructorHelpers::FObjectFinder<UStaticMesh> CylinderMeshFinder(TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));

	// 1. Heavy horizontal timber beam
	BarrierCrossbarMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("BarrierCrossbarMesh"));
	BarrierCrossbarMesh->SetupAttachment(RootComponent);
	BarrierCrossbarMesh->SetRelativeLocation(FVector(0.0f, 0.0f, 65.0f));
	BarrierCrossbarMesh->SetRelativeScale3D(FVector(0.18f, 2.40f, 0.22f));
	BarrierCrossbarMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	if (CubeMeshFinder.Succeeded())
	{
		BarrierCrossbarMesh->SetStaticMesh(CubeMeshFinder.Object);
	}

	// 2. Left support post
	PostLeftMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("PostLeftMesh"));
	PostLeftMesh->SetupAttachment(RootComponent);
	PostLeftMesh->SetRelativeLocation(FVector(0.0f, -95.0f, 40.0f));
	PostLeftMesh->SetRelativeScale3D(FVector(0.20f, 0.20f, 0.80f));
	PostLeftMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	if (CubeMeshFinder.Succeeded())
	{
		PostLeftMesh->SetStaticMesh(CubeMeshFinder.Object);
	}

	// 3. Right support post
	PostRightMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("PostRightMesh"));
	PostRightMesh->SetupAttachment(RootComponent);
	PostRightMesh->SetRelativeLocation(FVector(0.0f, 95.0f, 40.0f));
	PostRightMesh->SetRelativeScale3D(FVector(0.20f, 0.20f, 0.80f));
	PostRightMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	if (CubeMeshFinder.Succeeded())
	{
		PostRightMesh->SetStaticMesh(CubeMeshFinder.Object);
	}

	// 4. Barbed wire coil obstruction
	WireMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("WireMesh"));
	WireMesh->SetupAttachment(BarrierCrossbarMesh);
	WireMesh->SetRelativeLocation(FVector(0.0f, 0.0f, 15.0f));
	WireMesh->SetRelativeScale3D(FVector(0.85f, 0.95f, 0.55f));
	WireMesh->SetCollisionProfileName(TEXT("NoCollision"));
	if (CubeMeshFinder.Succeeded())
	{
		WireMesh->SetStaticMesh(CubeMeshFinder.Object);
	}

	// 5. Hanging red storm hurricane lantern (Lal Batti)
	RedLanternMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("RedLanternMesh"));
	RedLanternMesh->SetupAttachment(BarrierCrossbarMesh);
	RedLanternMesh->SetRelativeLocation(FVector(10.0f, 0.0f, -18.0f));
	RedLanternMesh->SetRelativeScale3D(FVector(0.12f, 0.12f, 0.22f));
	RedLanternMesh->SetCollisionProfileName(TEXT("NoCollision"));
	if (CylinderMeshFinder.Succeeded())
	{
		RedLanternMesh->SetStaticMesh(CylinderMeshFinder.Object);
	}

	// 6. Crimson curfew warning point light
	RedLanternLight = CreateDefaultSubobject<UPointLightComponent>(TEXT("RedLanternLight"));
	RedLanternLight->SetupAttachment(RedLanternMesh);
	RedLanternLight->SetRelativeLocation(FVector(0.0f, 0.0f, 0.0f));
	RedLanternLight->SetLightColor(FColor(245, 38, 22));
	RedLanternLight->SetIntensity(1950.0f);
	RedLanternLight->SetAttenuationRadius(450.0f);
	RedLanternLight->CastShadows = true;

	// 7. Military warning plaque
	WarningPlaqueMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("WarningPlaqueMesh"));
	WarningPlaqueMesh->SetupAttachment(BarrierCrossbarMesh);
	WarningPlaqueMesh->SetRelativeLocation(FVector(10.0f, -40.0f, 0.0f));
	WarningPlaqueMesh->SetRelativeScale3D(FVector(0.04f, 0.40f, 0.25f));
	WarningPlaqueMesh->SetCollisionProfileName(TEXT("NoCollision"));
	if (CubeMeshFinder.Succeeded())
	{
		WarningPlaqueMesh->SetStaticMesh(CubeMeshFinder.Object);
	}

	BarrierTitle = FText::FromString(TEXT("COLONIAL POLICE CHECKPOINT (NAKA BANDI)"));
	BarrierLore = FText::FromString(
		TEXT("Heavy teak barricades and barbed wire coils seal off the main bazaar thoroughfare leading towards the Kot Gurdarshan railway telegraph outpost.\n\n"
		     "Under Section 144 martial regulations decreed by the colonial administration in April 1919, armed Gurkha and Punjab Police pickets inspect all travelers along trunk roads. Any youth caught outside without a magistrate's transit permit is arrested under summary military orders.\n\n"
		     "With the ground roads barricaded, Kabir's only viable courier path lies above—across the contiguous flat rooftops, clotheslines, and brick parapets of the old mohalla.")
	);

	static ConstructorHelpers::FObjectFinder<USoundBase> CreakSoundFinder(TEXT("/Game/Audio/SFX/SFX_Teak_Door_Creak.SFX_Teak_Door_Creak"));
	if (CreakSoundFinder.Succeeded())
	{
		LanternCreakSound = CreakSoundFinder.Object;
	}
}

void ACheckpointBarrierActor::BeginPlay()
{
	Super::BeginPlay();

	UE_LOG(LogREVOLUTION, Log, TEXT("CheckpointBarrierActor erected at %s blocking bazaar exit"), *GetActorLocation().ToString());
}

void ACheckpointBarrierActor::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	// Gentle subtle wind pulse on the red warning lantern flame
	LightPulseTimer += DeltaTime;
	if (RedLanternLight)
	{
		float Flicker = FMath::Sin(LightPulseTimer * 3.5f) * 180.0f + FMath::Cos(LightPulseTimer * 7.0f) * 90.0f;
		RedLanternLight->SetIntensity(1950.0f + Flicker);
	}
}

bool ACheckpointBarrierActor::CanInteract_Implementation(const ARevolutionCharacter* Interactor) const
{
	return Interactor != nullptr;
}

FText ACheckpointBarrierActor::GetInteractionPrompt_Implementation() const
{
	return FText::FromString(TEXT("Examine Colonial Barricade (Naka Bandi)"));
}

void ACheckpointBarrierActor::OnInteract_Implementation(ARevolutionCharacter* Interactor)
{
	if (!Interactor) return;

	if (LanternCreakSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, LanternCreakSound, GetActorLocation(), 0.75f, 1.1f);
	}

	Interactor->StartInspection(BarrierTitle, BarrierLore);
	UE_LOG(LogREVOLUTION, Log, TEXT("Kabir surveyed colonial police barricade at %s"), *GetActorLocation().ToString());
}
