// Copyright Epic Games, Inc. All Rights Reserved.

#include "PersianWheelActor.h"
#include "RevolutionCharacter.h"
#include "CommunityTrustSubsystem.h"
#include "Components/SceneComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SphereComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/SoundBase.h"
#include "REVOLUTION.h"

APersianWheelActor::APersianWheelActor()
{
	PrimaryActorTick.bCanEverTick = false;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	WheelMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("WheelMesh"));
	WheelMesh->SetupAttachment(RootComponent);
	WheelMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));

	InteractionTrigger = CreateDefaultSubobject<USphereComponent>(TEXT("InteractionTrigger"));
	InteractionTrigger->SetupAttachment(RootComponent);
	InteractionTrigger->SetSphereRadius(240.0f);
	InteractionTrigger->SetCollisionProfileName(TEXT("Trigger"));

	static ConstructorHelpers::FObjectFinder<UStaticMesh> MeshFinder(
		TEXT("/Game/Environment/Mohalla/Meshes/SM_Persian_Wheel_Rahat_Timber.SM_Persian_Wheel_Rahat_Timber")
	);
	if (MeshFinder.Succeeded())
	{
		WheelMesh->SetStaticMesh(MeshFinder.Object);
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> SoundFinder(
		TEXT("/Game/Audio/SFX/SFX_Persian_Wheel_Rahat_Creak.SFX_Persian_Wheel_Rahat_Creak")
	);
	if (SoundFinder.Succeeded())
	{
		WheelCreakSound = SoundFinder.Object;
	}

	LaborPrompt = FText::FromString(TEXT("Push Timber Draught Beam to Clear Irrigation Flume (Manual Reparation)"));
	ClearedPrompt = FText::FromString(TEXT("Irrigation Flume Flowing Freely into Potter Rahim's Terracotta Pits"));
}

void APersianWheelActor::BeginPlay()
{
	Super::BeginPlay();
	UE_LOG(LogREVOLUTION, Log, TEXT("PersianWheelActor spawned at %s for cluster '%s'"),
		*GetActorLocation().ToString(), *CommunityClusterID.ToString());
}

void APersianWheelActor::OnInteract_Implementation(ARevolutionCharacter* Interactor)
{
	if (bFlumeCleared)
	{
		return;
	}

	bFlumeCleared = true;

	if (WheelCreakSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, WheelCreakSound, GetActorLocation(), 1.25f, 0.95f);
	}

	OnFlumeCleared.Broadcast(CommunityClusterID);

	if (UWorld* World = GetWorld())
	{
		if (UCommunityTrustSubsystem* TrustSubsystem = World->GetSubsystem<UCommunityTrustSubsystem>())
		{
			TrustSubsystem->AdjustClusterScore(
				CommunityClusterID,
				LaborTrustBonus,
				FName(TEXT("Incident_PersianWheelFlumeCleared")),
				Interactor
			);

			UE_LOG(LogREVOLUTION, Warning,
				TEXT("[PersianWheel] Kabir pushed the timber draught beam and unjammed the flume! Cluster '%s' trust +%d! Water flowing freely to Kumhar Rahim's clay pits."),
				*CommunityClusterID.ToString(), LaborTrustBonus);
		}
	}
}

FText APersianWheelActor::GetInteractionPrompt_Implementation() const
{
	return bFlumeCleared ? ClearedPrompt : LaborPrompt;
}

bool APersianWheelActor::CanInteract_Implementation(const ARevolutionCharacter* Interactor) const
{
	return !bFlumeCleared;
}

void APersianWheelActor::ResetFlumeState()
{
	bFlumeCleared = false;
}

UCommunityTrustSubsystem* APersianWheelActor::GetCommunityTrustSubsystem() const
{
	return GetWorld() ? GetWorld()->GetSubsystem<UCommunityTrustSubsystem>() : nullptr;
}
