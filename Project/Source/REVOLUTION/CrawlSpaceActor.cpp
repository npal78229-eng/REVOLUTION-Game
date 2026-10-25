// Copyright Epic Games, Inc. All Rights Reserved.

#include "CrawlSpaceActor.h"
#include "RevolutionCharacter.h"
#include "Components/SceneComponent.h"
#include "Components/StaticMeshComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Sound/SoundBase.h"
#include "Kismet/GameplayStatics.h"
#include "REVOLUTION.h"

ACrawlSpaceActor::ACrawlSpaceActor()
{
	PrimaryActorTick.bCanEverTick = false;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	ConduitMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("ConduitMesh"));
	ConduitMesh->SetupAttachment(RootComponent);
	ConduitMesh->SetRelativeScale3D(FVector(0.35f, 0.50f, 0.28f));
	ConduitMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));

	static ConstructorHelpers::FObjectFinder<UStaticMesh> MeshFinder(TEXT("/Game/Environment/Mohalla/Meshes/SM_Roof_Parapet_4m_A.SM_Roof_Parapet_4m_A"));
	if (MeshFinder.Succeeded())
	{
		ConduitMesh->SetStaticMesh(MeshFinder.Object);
	}

	PointA = CreateDefaultSubobject<USceneComponent>(TEXT("PointA"));
	PointA->SetupAttachment(RootComponent);
	PointA->SetRelativeLocation(FVector(-85.0f, 0.0f, 0.0f));

	PointB = CreateDefaultSubobject<USceneComponent>(TEXT("PointB"));
	PointB->SetupAttachment(RootComponent);
	PointB->SetRelativeLocation(FVector(85.0f, 0.0f, 0.0f));

	static ConstructorHelpers::FObjectFinder<USoundBase> ScrapeSoundFinder(TEXT("/Game/Audio/SFX/SFX_Crawl_Brick_Scrape.SFX_Crawl_Brick_Scrape"));
	if (ScrapeSoundFinder.Succeeded())
	{
		ScrapeSound = ScrapeSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> EmergeSoundFinder(TEXT("/Game/Audio/SFX/SFX_Drain_Emerge_Gasp.SFX_Drain_Emerge_Gasp"));
	if (EmergeSoundFinder.Succeeded())
	{
		EmergeSound = EmergeSoundFinder.Object;
	}
}

bool ACrawlSpaceActor::CanInteract_Implementation(const ARevolutionCharacter* Interactor) const
{
	if (!Interactor) return false;
	return !bIsTraversing && !Interactor->IsCrawlTraversing();
}

FText ACrawlSpaceActor::GetInteractionPrompt_Implementation() const
{
	return CrawlPrompt;
}

void ACrawlSpaceActor::GetCrawlEndpoints(const FVector& InteractorLoc, FVector& OutStart, FVector& OutEnd) const
{
	FVector LocA = PointA ? PointA->GetComponentLocation() : GetActorLocation();
	FVector LocB = PointB ? PointB->GetComponentLocation() : GetActorLocation();

	float DistA = FVector::DistSquared(InteractorLoc, LocA);
	float DistB = FVector::DistSquared(InteractorLoc, LocB);

	if (DistA <= DistB)
	{
		OutStart = LocA;
		OutEnd = LocB;
	}
	else
	{
		OutStart = LocB;
		OutEnd = LocA;
	}
}

void ACrawlSpaceActor::OnInteract_Implementation(ARevolutionCharacter* Interactor)
{
	if (!Interactor || bIsTraversing) return;

	FVector StartLoc, EndLoc;
	GetCrawlEndpoints(Interactor->GetActorLocation(), StartLoc, EndLoc);

	bIsTraversing = true;

	if (ScrapeSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, ScrapeSound, GetActorLocation(), 0.95f, FMath::RandRange(0.95f, 1.05f));
	}

	Interactor->StartCrawlTraversal(StartLoc, EndLoc, CrawlDuration);

	UE_LOG(LogREVOLUTION, Log, TEXT("Kabir squeezing into haveli drainage arch: %s"), *DrainName.ToString());
}

void ACrawlSpaceActor::FinishTraversal()
{
	bIsTraversing = false;

	if (EmergeSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, EmergeSound, GetActorLocation(), 0.90f, FMath::RandRange(0.95f, 1.05f));
	}

	UE_LOG(LogREVOLUTION, Log, TEXT("Kabir emerged from haveli drain traversal."));
}
