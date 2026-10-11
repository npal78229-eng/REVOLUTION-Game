// Copyright Epic Games, Inc. All Rights Reserved.

#include "LithoPressActor.h"
#include "RevolutionCharacter.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SceneComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/SoundBase.h"
#include "REVOLUTION.h"

ALithoPressActor::ALithoPressActor()
{
	PrimaryActorTick.bCanEverTick = false;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	static ConstructorHelpers::FObjectFinder<UStaticMesh> CubeMeshFinder(TEXT("/Engine/BasicShapes/Cube.Cube"));
	static ConstructorHelpers::FObjectFinder<UStaticMesh> CylinderMeshFinder(TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));

	// 1. Heavy teak timber workbench plinth
	TimberTableMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("TimberTableMesh"));
	TimberTableMesh->SetupAttachment(RootComponent);
	TimberTableMesh->SetRelativeLocation(FVector(0.0f, 0.0f, 35.0f));
	TimberTableMesh->SetRelativeScale3D(FVector(1.10f, 0.75f, 0.70f));
	TimberTableMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	if (CubeMeshFinder.Succeeded())
	{
		TimberTableMesh->SetStaticMesh(CubeMeshFinder.Object);
	}

	// 2. Fine-grained Bavarian lithography limestone slab
	LithoStoneMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("LithoStoneMesh"));
	LithoStoneMesh->SetupAttachment(TimberTableMesh);
	LithoStoneMesh->SetRelativeLocation(FVector(0.0f, 0.0f, 52.0f));
	LithoStoneMesh->SetRelativeScale3D(FVector(0.75f, 0.58f, 0.12f));
	LithoStoneMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	if (CubeMeshFinder.Succeeded())
	{
		LithoStoneMesh->SetStaticMesh(CubeMeshFinder.Object);
	}

	// 3. Heavy cast-iron scraper and pressure roller cylinder
	RollerAssemblyMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("RollerAssemblyMesh"));
	RollerAssemblyMesh->SetupAttachment(LithoStoneMesh);
	RollerAssemblyMesh->SetRelativeLocation(FVector(0.0f, 0.0f, 25.0f));
	RollerAssemblyMesh->SetRelativeRotation(FRotator(0.0f, 0.0f, 90.0f));
	RollerAssemblyMesh->SetRelativeScale3D(FVector(0.35f, 0.35f, 0.95f));
	RollerAssemblyMesh->SetCollisionProfileName(TEXT("NoCollision"));
	if (CylinderMeshFinder.Succeeded())
	{
		RollerAssemblyMesh->SetStaticMesh(CylinderMeshFinder.Object);
	}

	// 4. Flat slate ink grinding slab with leather brayer
	InkPaletteMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("InkPaletteMesh"));
	InkPaletteMesh->SetupAttachment(TimberTableMesh);
	InkPaletteMesh->SetRelativeLocation(FVector(35.0f, -22.0f, 51.0f));
	InkPaletteMesh->SetRelativeScale3D(FVector(0.24f, 0.24f, 0.06f));
	InkPaletteMesh->SetCollisionProfileName(TEXT("NoCollision"));
	if (CubeMeshFinder.Succeeded())
	{
		InkPaletteMesh->SetStaticMesh(CubeMeshFinder.Object);
	}

	// 5. Stack of freshly printed anti-Rowlatt leaflets on rag paper
	LeafletStackMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("LeafletStackMesh"));
	LeafletStackMesh->SetupAttachment(TimberTableMesh);
	LeafletStackMesh->SetRelativeLocation(FVector(-35.0f, 20.0f, 52.0f));
	LeafletStackMesh->SetRelativeScale3D(FVector(0.28f, 0.38f, 0.08f));
	LeafletStackMesh->SetCollisionProfileName(TEXT("NoCollision"));
	if (CubeMeshFinder.Succeeded())
	{
		LeafletStackMesh->SetStaticMesh(CubeMeshFinder.Object);
	}

	PressTitle = FText::FromString(TEXT("CLANDESTINE LITHOGRAPHIC PRESS (PATHAR DI CHHAPAKHANA)"));
	PressLore = FText::FromString(
		TEXT("Tucked inside this subterranean haveli workshop alcove sits a hand-cranked flatbed limestone lithographic press.\n\n"
		     "Following the passage of the Rowlatt Act in March 1919 and strict pre-censorship under the Indian Press Act of 1910, colonial magistrates seized vernacular printing presses and demanded ruinous security deposits without trial.\n\n"
		     "In response, freedom committees across Lahore, Amritsar, and Kot Gurdarshan retreated into private haveli basements. Urdu and Gurmukhi calligraphy is etched in reverse onto polished Bavarian limestone using greasy ink (lampblack, mutton tallow, and soap), dampened with water, and hand-rolled onto country rag paper to produce thousands of underground strike notices ('Hartal - Inquilab Zindabad') before dawn.")
	);

	static ConstructorHelpers::FObjectFinder<USoundBase> RollerSoundFinder(TEXT("/Game/Audio/SFX/SFX_Iron_Latch_Slide.SFX_Iron_Latch_Slide"));
	if (RollerSoundFinder.Succeeded())
	{
		PressOperateSound = RollerSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> PaperSoundFinder(TEXT("/Game/Audio/SFX/SFX_Pamphlet_Retrieve.SFX_Pamphlet_Retrieve"));
	if (PaperSoundFinder.Succeeded())
	{
		LeafletRetrieveSound = PaperSoundFinder.Object;
	}
}

void ALithoPressActor::BeginPlay()
{
	Super::BeginPlay();

	UE_LOG(LogREVOLUTION, Log, TEXT("LithoPressActor initialized in workshop cellar at %s"), *GetActorLocation().ToString());
}

bool ALithoPressActor::CanInteract_Implementation(const ARevolutionCharacter* Interactor) const
{
	return Interactor != nullptr;
}

FText ALithoPressActor::GetInteractionPrompt_Implementation() const
{
	if (!bHasBeenOperated)
	{
		return FText::FromString(TEXT("Operate Litho Press & Take Fresh Bulletins"));
	}
	return FText::FromString(TEXT("Inspect Lithographic Hand Press (Pathar di Chhapakhana)"));
}

void ALithoPressActor::OperatePress(ARevolutionCharacter* Kabir)
{
	if (!Kabir) return;

	bHasBeenOperated = true;

	if (PressOperateSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, PressOperateSound, GetActorLocation(), 0.95f, 0.92f);
	}

	if (LeafletRetrieveSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, LeafletRetrieveSound, GetActorLocation(), 1.0f);
	}

	// Replenish 1 tailor's chalk or 1 clay marble from the lithographer's stone kit
	if (Kabir->ChalkCount < Kabir->MaxChalk)
	{
		Kabir->ChalkCount = FMath::Min(Kabir->MaxChalk, Kabir->ChalkCount + 1);
		UE_LOG(LogREVOLUTION, Log, TEXT("Kabir retrieved fine chalk residue from litho workshop bench! (Chalk: %d)"), Kabir->ChalkCount);
	}
	else if (Kabir->PebbleCount < Kabir->MaxPebbles)
	{
		Kabir->PebbleCount = FMath::Min(Kabir->MaxPebbles, Kabir->PebbleCount + 1);
		UE_LOG(LogREVOLUTION, Log, TEXT("Kabir retrieved a smooth stone grinding weight from litho press! (Pebbles: %d)"), Kabir->PebbleCount);
	}

	UE_LOG(LogREVOLUTION, Warning, TEXT("Kabir operated clandestine lithographic press at %s! Fresh anti-Rowlatt leaflets pulled."), *GetActorLocation().ToString());
}

void ALithoPressActor::OnInteract_Implementation(ARevolutionCharacter* Interactor)
{
	if (!Interactor) return;

	if (!bHasBeenOperated)
	{
		OperatePress(Interactor);

		FText OperatedLore = FText::FromString(
			TEXT("Kabir pulls down the heavy iron scraper bar. The stone roller glides over the dampened limestone slab with a mechanical clank. The crisp, pungent aroma of fresh lampblack ink and linseed oil fills the cellar as Kabir lifts a fresh batch of anti-Rowlatt handbills.\n\n"
			     "'HARTAL ON SUNDAY: All bazaar shops to remain shuttered. No trains to be boarded. Inquilab Zindabad!'\n\n"
			     "Kabir tucks the fresh sheets securely inside his satchel.")
		);
		Interactor->StartInspection(PressTitle, OperatedLore);
	}
	else
	{
		Interactor->StartInspection(PressTitle, PressLore);
	}
}
