// Copyright Epic Games, Inc. All Rights Reserved.

#include "CurfewGongActor.h"
#include "RevolutionCharacter.h"
#include "CurfewPatrolAI.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SceneComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/SoundBase.h"
#include "EngineUtils.h"
#include "REVOLUTION.h"

ACurfewGongActor::ACurfewGongActor()
{
	PrimaryActorTick.bCanEverTick = false;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	static ConstructorHelpers::FObjectFinder<UStaticMesh> CubeMeshFinder(TEXT("/Engine/BasicShapes/Cube.Cube"));
	static ConstructorHelpers::FObjectFinder<UStaticMesh> CylinderMeshFinder(TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));

	// 1. Heavy timber gallows suspension frame
	TimberFrameMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("TimberFrameMesh"));
	TimberFrameMesh->SetupAttachment(RootComponent);
	TimberFrameMesh->SetRelativeLocation(FVector(0.0f, 0.0f, 65.0f));
	TimberFrameMesh->SetRelativeScale3D(FVector(0.22f, 1.15f, 1.35f));
	TimberFrameMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	if (CubeMeshFinder.Succeeded())
	{
		TimberFrameMesh->SetStaticMesh(CubeMeshFinder.Object);
	}

	// 2. Heavy cast-bronze circular gong
	BronzeGongMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("BronzeGongMesh"));
	BronzeGongMesh->SetupAttachment(TimberFrameMesh);
	BronzeGongMesh->SetRelativeLocation(FVector(6.0f, 0.0f, 5.0f));
	BronzeGongMesh->SetRelativeRotation(FRotator(0.0f, 0.0f, 90.0f));
	BronzeGongMesh->SetRelativeScale3D(FVector(0.55f, 0.55f, 0.06f));
	BronzeGongMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	if (CylinderMeshFinder.Succeeded())
	{
		BronzeGongMesh->SetStaticMesh(CylinderMeshFinder.Object);
	}

	// 3. Wrought-iron striker mallet
	IronStrikerMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("IronStrikerMesh"));
	IronStrikerMesh->SetupAttachment(TimberFrameMesh);
	IronStrikerMesh->SetRelativeLocation(FVector(14.0f, 32.0f, -12.0f));
	IronStrikerMesh->SetRelativeRotation(FRotator(18.0f, 0.0f, 25.0f));
	IronStrikerMesh->SetRelativeScale3D(FVector(0.06f, 0.06f, 0.40f));
	IronStrikerMesh->SetCollisionProfileName(TEXT("NoCollision"));
	if (CylinderMeshFinder.Succeeded())
	{
		IronStrikerMesh->SetStaticMesh(CylinderMeshFinder.Object);
	}

	GongTitle = FText::FromString(TEXT("MUNICIPAL CURFEW GONG (CHAUKIDAR GHANTA)"));
	GongLore = FText::FromString(
		TEXT("A heavy cast-bronze gong suspended from teak rafters above the outer deorhi gateway arch.\n\n"
		     "Under British municipal curfew regulations in April 1919, police constables struck this gong at 8:00 PM to order all native residents off the streets, and at 5:00 AM to sound morning roll call.\n\n"
		     "Striking the gong produces a reverberating boom that echoes across the entire town, creating an emergency sector diversion that draws all patrol watchmen to the gateway.")
	);

	static ConstructorHelpers::FObjectFinder<USoundBase> TollSoundFinder(TEXT("/Game/Audio/SFX/SFX_Curfew_Bell_Toll.SFX_Curfew_Bell_Toll"));
	if (TollSoundFinder.Succeeded())
	{
		GongTollSound = TollSoundFinder.Object;
	}
}

void ACurfewGongActor::BeginPlay()
{
	Super::BeginPlay();

	UE_LOG(LogREVOLUTION, Log, TEXT("CurfewGongActor suspended above gateway arch at %s"), *GetActorLocation().ToString());
}

bool ACurfewGongActor::CanInteract_Implementation(const ARevolutionCharacter* Interactor) const
{
	return Interactor != nullptr;
}

FText ACurfewGongActor::GetInteractionPrompt_Implementation() const
{
	return FText::FromString(TEXT("Strike Municipal Curfew Gong (Town-Wide Diversion)"));
}

void ACurfewGongActor::StrikeGong(ARevolutionCharacter* Kabir)
{
	if (!Kabir) return;

	bHasBeenStruck = true;

	if (GongTollSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, GongTollSound, GetActorLocation(), 1.4f, 0.95f);
	}

	// Divert all curfew watchmen across the sector to the gateway arch
	UWorld* World = GetWorld();
	if (World)
	{
		for (TActorIterator<ACurfewPatrolAI> WatchmanIt(World); WatchmanIt; ++WatchmanIt)
		{
			ACurfewPatrolAI* Watchman = *WatchmanIt;
			if (Watchman)
			{
				float Dist = FVector::Dist(Watchman->GetActorLocation(), GetActorLocation());
				if (Dist <= SectorAlertRadius)
				{
					Watchman->InvestigateSoundLocation(GetActorLocation());
					UE_LOG(LogREVOLUTION, Warning, TEXT("Watchman summoned to gateway arch by Curfew Gong toll at %s!"), *GetActorLocation().ToString());
				}
			}
		}
	}

	FText StrikeFeedback = FText::FromString(
		TEXT("Kabir swings the iron mallet with both hands into the bronze disk.\n\n"
		     "A deafening, reverberating toll booms across Kot Gurdarshan, shaking the rooftop parapets. Convinced an emergency uprising or curfew breach has occurred at the outer gateway, colonial night watchmen immediately break their patrols to converge upon the entrance.")
	);
	Kabir->StartInspection(GongTitle, StrikeFeedback);

	UE_LOG(LogREVOLUTION, Warning, TEXT("Kabir struck the Municipal Curfew Gong at %s! Town-wide diversion triggered across 35m radius."), *GetActorLocation().ToString());
}

void ACurfewGongActor::OnInteract_Implementation(ARevolutionCharacter* Interactor)
{
	StrikeGong(Interactor);
}
