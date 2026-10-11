// Copyright Epic Games, Inc. All Rights Reserved.

#include "TelegraphWireActor.h"
#include "RevolutionCharacter.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SceneComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/SoundBase.h"
#include "REVOLUTION.h"

ATelegraphWireActor::ATelegraphWireActor()
{
	PrimaryActorTick.bCanEverTick = false;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	static ConstructorHelpers::FObjectFinder<UStaticMesh> CubeMeshFinder(TEXT("/Engine/BasicShapes/Cube.Cube"));
	static ConstructorHelpers::FObjectFinder<UStaticMesh> CylinderMeshFinder(TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));

	// 1. Weathered timber utility post
	UtilityPoleMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("UtilityPoleMesh"));
	UtilityPoleMesh->SetupAttachment(RootComponent);
	UtilityPoleMesh->SetRelativeLocation(FVector(0.0f, 0.0f, 110.0f));
	UtilityPoleMesh->SetRelativeScale3D(FVector(0.18f, 0.18f, 2.20f));
	UtilityPoleMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	if (CylinderMeshFinder.Succeeded())
	{
		UtilityPoleMesh->SetStaticMesh(CylinderMeshFinder.Object);
	}

	// 2. Horizontal wooden crossarm
	CrossarmMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("CrossarmMesh"));
	CrossarmMesh->SetupAttachment(RootComponent);
	CrossarmMesh->SetRelativeLocation(FVector(0.0f, 0.0f, 205.0f));
	CrossarmMesh->SetRelativeScale3D(FVector(0.14f, 1.25f, 0.14f));
	CrossarmMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	if (CubeMeshFinder.Succeeded())
	{
		CrossarmMesh->SetStaticMesh(CubeMeshFinder.Object);
	}

	// 3. Left porcelain bell insulator
	InsulatorLeftMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("InsulatorLeftMesh"));
	InsulatorLeftMesh->SetupAttachment(CrossarmMesh);
	InsulatorLeftMesh->SetRelativeLocation(FVector(0.0f, -48.0f, 12.0f));
	InsulatorLeftMesh->SetRelativeScale3D(FVector(0.55f, 0.55f, 0.85f));
	InsulatorLeftMesh->SetCollisionProfileName(TEXT("NoCollision"));
	if (CylinderMeshFinder.Succeeded())
	{
		InsulatorLeftMesh->SetStaticMesh(CylinderMeshFinder.Object);
	}

	// 4. Right porcelain bell insulator
	InsulatorRightMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("InsulatorRightMesh"));
	InsulatorRightMesh->SetupAttachment(CrossarmMesh);
	InsulatorRightMesh->SetRelativeLocation(FVector(0.0f, 48.0f, 12.0f));
	InsulatorRightMesh->SetRelativeScale3D(FVector(0.55f, 0.55f, 0.85f));
	InsulatorRightMesh->SetCollisionProfileName(TEXT("NoCollision"));
	if (CylinderMeshFinder.Succeeded())
	{
		InsulatorRightMesh->SetStaticMesh(CylinderMeshFinder.Object);
	}

	// 5. Active taut copper military telegraph wire
	TelegraphWireMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("TelegraphWireMesh"));
	TelegraphWireMesh->SetupAttachment(CrossarmMesh);
	TelegraphWireMesh->SetRelativeLocation(FVector(0.0f, 0.0f, 14.0f));
	TelegraphWireMesh->SetRelativeScale3D(FVector(0.02f, 2.40f, 0.02f));
	TelegraphWireMesh->SetCollisionProfileName(TEXT("NoCollision"));
	if (CubeMeshFinder.Succeeded())
	{
		TelegraphWireMesh->SetStaticMesh(CubeMeshFinder.Object);
	}

	// 6. Severed dangling wire coil (hidden until cut)
	SeveredWireMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("SeveredWireMesh"));
	SeveredWireMesh->SetupAttachment(CrossarmMesh);
	SeveredWireMesh->SetRelativeLocation(FVector(0.0f, -48.0f, -45.0f));
	SeveredWireMesh->SetRelativeScale3D(FVector(0.03f, 0.03f, 0.75f));
	SeveredWireMesh->SetCollisionProfileName(TEXT("NoCollision"));
	SeveredWireMesh->SetVisibility(false);
	if (CylinderMeshFinder.Succeeded())
	{
		SeveredWireMesh->SetStaticMesh(CylinderMeshFinder.Object);
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> SnipSoundFinder(TEXT("/Game/Audio/SFX/SFX_Iron_Latch_Slide.SFX_Iron_Latch_Slide"));
	if (SnipSoundFinder.Succeeded())
	{
		WireCutSound = SnipSoundFinder.Object;
	}
}

void ATelegraphWireActor::BeginPlay()
{
	Super::BeginPlay();

	UE_LOG(LogREVOLUTION, Log, TEXT("TelegraphWireActor mounted on rooftop parapet at %s"), *GetActorLocation().ToString());
}

bool ATelegraphWireActor::CanInteract_Implementation(const ARevolutionCharacter* Interactor) const
{
	return !bIsWireCut && Interactor != nullptr;
}

FText ATelegraphWireActor::GetInteractionPrompt_Implementation() const
{
	return FText::FromString(TEXT("Cut Imperial Military Telegraph Line"));
}

void ATelegraphWireActor::CutTelegraphLine(ARevolutionCharacter* Kabir)
{
	if (bIsWireCut || !Kabir) return;

	bIsWireCut = true;

	if (TelegraphWireMesh)
	{
		TelegraphWireMesh->SetVisibility(false);
	}

	if (SeveredWireMesh)
	{
		SeveredWireMesh->SetVisibility(true);
	}

	if (WireCutSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, WireCutSound, GetActorLocation(), 1.0f, 1.25f);
	}

	FText SabotageLore = FText::FromString(
		TEXT("With a sharp snip of his father's tailor shears, Kabir cuts through the high-gauge copper telegraph line.\n\n"
		     "The severed wire recoils into the dark alley below with a muted metallic hum. Throughout April 1919, cutting telegraph lines ('Taar Katna') across Punjab severed railway communication between district headquarters and the military division in Lahore, preventing colonial magistrates from summoning armored train reinforcements during the Hartal.")
	);
	Kabir->StartInspection(FText::FromString(TEXT("Severed Colonial Telegraph Wire")), SabotageLore);

	UE_LOG(LogREVOLUTION, Warning, TEXT("Kabir successfully cut the colonial military telegraph line at %s! Kot Gurdarshan isolated from Lahore Cantonment."), *GetActorLocation().ToString());
}

void ATelegraphWireActor::OnInteract_Implementation(ARevolutionCharacter* Interactor)
{
	CutTelegraphLine(Interactor);
}
