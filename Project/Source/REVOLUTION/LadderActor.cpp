// Copyright Epic Games, Inc. All Rights Reserved.

#include "LadderActor.h"
#include "RevolutionCharacter.h"
#include "Components/SceneComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/BoxComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Sound/SoundBase.h"
#include "Kismet/GameplayStatics.h"
#include "TimerManager.h"
#include "REVOLUTION.h"

ALadderActor::ALadderActor()
{
	PrimaryActorTick.bCanEverTick = false;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	LadderMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("LadderMesh"));
	LadderMesh->SetupAttachment(RootComponent);
	LadderMesh->SetRelativeScale3D(FVector(0.010f, 0.010f, 0.0116f));
	LadderMesh->SetCollisionProfileName(TEXT("BlockAll"));
	LadderMesh->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);

	static ConstructorHelpers::FObjectFinder<UStaticMesh> MeshFinder(TEXT("/Game/Environment/Mohalla/Meshes/SM_Prop_Makeshift_Timber_Ladder.SM_Prop_Makeshift_Timber_Ladder"));
	if (MeshFinder.Succeeded())
	{
		LadderMesh->SetStaticMesh(MeshFinder.Object);
	}

	InteractionTrigger = CreateDefaultSubobject<UBoxComponent>(TEXT("InteractionTrigger"));
	InteractionTrigger->SetupAttachment(RootComponent);
	InteractionTrigger->SetBoxExtent(FVector(90.0f, 120.0f, 220.0f));
	InteractionTrigger->SetRelativeLocation(FVector(0.0f, 0.0f, 200.0f));
	InteractionTrigger->SetCollisionProfileName(TEXT("OverlapAllDynamic"));

	BottomMountPoint = CreateDefaultSubobject<USceneComponent>(TEXT("BottomMountPoint"));
	BottomMountPoint->SetupAttachment(RootComponent);
	BottomMountPoint->SetRelativeLocation(FVector(0.0f, -50.0f, 0.0f));

	TopDismountPoint = CreateDefaultSubobject<USceneComponent>(TEXT("TopDismountPoint"));
	TopDismountPoint->SetupAttachment(RootComponent);
	TopDismountPoint->SetRelativeLocation(FVector(0.0f, 60.0f, 400.0f));

	static ConstructorHelpers::FObjectFinder<USoundBase> CreakSoundFinder(TEXT("/Game/Audio/SFX/SFX_Ladder_Rung_Creak.SFX_Ladder_Rung_Creak"));
	if (CreakSoundFinder.Succeeded())
	{
		ClimbSound = CreakSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> DismountSoundFinder(TEXT("/Game/Audio/SFX/SFX_Ladder_Dismount.SFX_Ladder_Dismount"));
	if (DismountSoundFinder.Succeeded())
	{
		DismountSound = DismountSoundFinder.Object;
	}
}

void ALadderActor::BeginPlay()
{
	Super::BeginPlay();
}

bool ALadderActor::IsCloserToBottom(const FVector& InteractorLoc) const
{
	FVector BottomLoc = BottomMountPoint ? BottomMountPoint->GetComponentLocation() : GetActorLocation();
	FVector TopLoc = TopDismountPoint ? TopDismountPoint->GetComponentLocation() : (GetActorLocation() + FVector(0.f, 0.f, 400.f));
	float MidpointZ = (BottomLoc.Z + TopLoc.Z) * 0.5f;
	return InteractorLoc.Z < MidpointZ;
}

bool ALadderActor::CanInteract_Implementation(const ARevolutionCharacter* Interactor) const
{
	if (!Interactor) return false;
	return !bIsTraversing && !Interactor->IsClimbingLadder() && !Interactor->IsMantling() && !Interactor->IsCrawlTraversing();
}

FText ALadderActor::GetInteractionPrompt_Implementation() const
{
	APawn* PlayerPawn = UGameplayStatics::GetPlayerPawn(GetWorld(), 0);
	if (PlayerPawn)
	{
		return IsCloserToBottom(PlayerPawn->GetActorLocation()) ? AscendPrompt : DescendPrompt;
	}
	return AscendPrompt;
}

void ALadderActor::OnInteract_Implementation(ARevolutionCharacter* Interactor)
{
	if (!Interactor || bIsTraversing) return;

	bIsTraversing = true;

	FVector BottomLoc = BottomMountPoint ? BottomMountPoint->GetComponentLocation() : GetActorLocation();
	FVector TopLoc = TopDismountPoint ? TopDismountPoint->GetComponentLocation() : (GetActorLocation() + FVector(0.f, 0.f, 400.f));

	bool bAscending = IsCloserToBottom(Interactor->GetActorLocation());
	FVector StartLoc = bAscending ? BottomLoc : TopLoc;
	FVector TargetLoc = bAscending ? TopLoc : BottomLoc;

	if (ClimbSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, ClimbSound, GetActorLocation(), 1.0f, FMath::RandRange(0.96f, 1.04f));
	}

	Interactor->StartLadderClimb(StartLoc, TargetLoc, ClimbDuration, bAscending);

	FTimerHandle FinishTimerHandle;
	GetWorldTimerManager().SetTimer(FinishTimerHandle, this, &ALadderActor::FinishTraversal, ClimbDuration + 0.1f, false);

	UE_LOG(LogREVOLUTION, Log, TEXT("Kabir started vertical ladder traversal (%s) on %s"),
		bAscending ? TEXT("Ascending to Terrace") : TEXT("Descending to Courtyard"), *LadderName.ToString());
}

void ALadderActor::FinishTraversal()
{
	bIsTraversing = false;
	if (DismountSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, DismountSound, GetActorLocation(), 0.95f, 1.0f);
	}
	UE_LOG(LogREVOLUTION, Log, TEXT("Ladder traversal finished on %s"), *LadderName.ToString());
}
