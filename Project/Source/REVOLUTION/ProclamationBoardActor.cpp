// Copyright Epic Games, Inc. All Rights Reserved.

#include "ProclamationBoardActor.h"
#include "RevolutionCharacter.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SceneComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/SoundBase.h"
#include "REVOLUTION.h"

AProclamationBoardActor::AProclamationBoardActor()
{
	PrimaryActorTick.bCanEverTick = false;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	static ConstructorHelpers::FObjectFinder<UStaticMesh> CubeMeshFinder(TEXT("/Engine/BasicShapes/Cube.Cube"));

	// Wooden notice board backing mounted against masonry wall
	BoardFrameMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("BoardFrameMesh"));
	BoardFrameMesh->SetupAttachment(RootComponent);
	BoardFrameMesh->SetRelativeScale3D(FVector(0.08f, 0.70f, 0.95f));
	BoardFrameMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	if (CubeMeshFinder.Succeeded())
	{
		BoardFrameMesh->SetStaticMesh(CubeMeshFinder.Object);
	}

	// Weathered printed imperial parchment notice
	ParchmentNoticeMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("ParchmentNoticeMesh"));
	ParchmentNoticeMesh->SetupAttachment(BoardFrameMesh);
	ParchmentNoticeMesh->SetRelativeLocation(FVector(6.0f, 0.0f, 0.0f));
	ParchmentNoticeMesh->SetRelativeScale3D(FVector(0.02f, 0.88f, 0.88f));
	ParchmentNoticeMesh->SetCollisionProfileName(TEXT("NoCollision"));
	if (CubeMeshFinder.Succeeded())
	{
		ParchmentNoticeMesh->SetStaticMesh(CubeMeshFinder.Object);
	}

	// Tailor's chalk defiance strike mark (hidden until defaced)
	ChalkDefaceMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("ChalkDefaceMesh"));
	ChalkDefaceMesh->SetupAttachment(ParchmentNoticeMesh);
	ChalkDefaceMesh->SetRelativeLocation(FVector(2.0f, 0.0f, 0.0f));
	ChalkDefaceMesh->SetRelativeRotation(FRotator(0.0f, 35.0f, 0.0f));
	ChalkDefaceMesh->SetRelativeScale3D(FVector(0.03f, 0.80f, 0.08f));
	ChalkDefaceMesh->SetCollisionProfileName(TEXT("NoCollision"));
	ChalkDefaceMesh->SetVisibility(false);
	if (CubeMeshFinder.Succeeded())
	{
		ChalkDefaceMesh->SetStaticMesh(CubeMeshFinder.Object);
	}

	ProclamationTitle = FText::FromString(TEXT("IMPERIAL PROCLAMATION — SECTION 144 CR.P.C."));
	ProclamationBody = FText::FromString(
		TEXT("BY ORDER OF THE DISTRICT MAGISTRATE, KOT GURDARSHAN (APRIL 1919).\n\n"
		     "1. All public gatherings exceeding four persons are prohibited under Section 144 of the Code of Criminal Procedure.\n"
		     "2. Curfew is proclaimed from 8:00 PM until 5:00 AM. Any native found abroad after curfew hours without an imperial transit permit shall be detained immediately for magistrate interrogation under summary martial regulations.\n"
		     "3. Sedition, circulation of clandestine anti-Rowlatt pamphlets, and incitement to hartal (general strike) shall be dealt with under emergency wartime penal codes.\n\n"
		     "GOD SAVE THE KING-EMPEROR")
	);

	static ConstructorHelpers::FObjectFinder<USoundBase> ChalkSoundFinder(TEXT("/Game/Audio/SFX/SFX_Chalk_Draw.SFX_Chalk_Draw"));
	if (ChalkSoundFinder.Succeeded())
	{
		ChalkDefaceSound = ChalkSoundFinder.Object;
	}
}

void AProclamationBoardActor::BeginPlay()
{
	Super::BeginPlay();

	UE_LOG(LogREVOLUTION, Log, TEXT("ProclamationBoardActor mounted on wall at %s"), *GetActorLocation().ToString());
}

bool AProclamationBoardActor::CanInteract_Implementation(const ARevolutionCharacter* Interactor) const
{
	return Interactor != nullptr;
}

FText AProclamationBoardActor::GetInteractionPrompt_Implementation() const
{
	if (!bIsDefaced)
	{
		return FText::FromString(TEXT("Read & Deface Section 144 Edict"));
	}
	return FText::FromString(TEXT("Inspect Defaced Imperial Decree"));
}

void AProclamationBoardActor::DefaceNoticeWithChalk(ARevolutionCharacter* Kabir)
{
	if (bIsDefaced || !Kabir || Kabir->GetChalkCount() <= 0)
	{
		return;
	}

	bIsDefaced = true;
	Kabir->ChalkCount = FMath::Max(0, Kabir->ChalkCount - 1);

	if (ChalkDefaceMesh)
	{
		ChalkDefaceMesh->SetVisibility(true);
	}

	if (ChalkDefaceSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, ChalkDefaceSound, GetActorLocation(), 1.0f);
	}

	UE_LOG(LogREVOLUTION, Warning, TEXT("Kabir defaced the Section 144 Proclamation Board at %s with tailor's chalk! (Remaining Chalk: %d)"), *GetActorLocation().ToString(), Kabir->GetChalkCount());
}

void AProclamationBoardActor::OnInteract_Implementation(ARevolutionCharacter* Interactor)
{
	if (!Interactor) return;

	// If not yet defaced and Kabir has chalk, deface it as an act of resistance
	if (!bIsDefaced && Interactor->GetChalkCount() > 0)
	{
		DefaceNoticeWithChalk(Interactor);

		FText DefacedLore = FText::FromString(
			TEXT("With a bold sweep of father's tailor's chalk, Kabir strikes through the King-Emperor's decree, scribbling the resistance call across the parchment: 'HARTAL TOMORROW — INQUILAB ZINDABAD'. When the patrol watchman spots this defaced proclamation, he will stop in outrage, creating a diversion.")
		);
		Interactor->StartInspection(FText::FromString(TEXT("Defaced Section 144 Edict")), DefacedLore);
	}
	else
	{
		Interactor->StartInspection(ProclamationTitle, ProclamationBody);
	}
}
