// Copyright Epic Games, Inc. All Rights Reserved.

#include "RestitutionDropActor.h"
#include "RevolutionCharacter.h"
#include "CommunityTrustSubsystem.h"
#include "Components/SceneComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SphereComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/SoundBase.h"
#include "REVOLUTION.h"

ARestitutionDropActor::ARestitutionDropActor()
{
	PrimaryActorTick.bCanEverTick = false;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	PropMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("PropMesh"));
	PropMesh->SetupAttachment(RootComponent);
	PropMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));

	InteractionTrigger = CreateDefaultSubobject<USphereComponent>(TEXT("InteractionTrigger"));
	InteractionTrigger->SetupAttachment(RootComponent);
	InteractionTrigger->SetSphereRadius(180.0f);
	InteractionTrigger->SetCollisionProfileName(TEXT("Trigger"));

	static ConstructorHelpers::FObjectFinder<UStaticMesh> MeshFinder(TEXT("/Game/Environment/Mohalla/Meshes/SM_Prop_ClayChaiCup_Kulhad.SM_Prop_ClayChaiCup_Kulhad"));
	if (MeshFinder.Succeeded())
	{
		PropMesh->SetStaticMesh(MeshFinder.Object);
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> SoundFinder(TEXT("/Game/Audio/SFX/SFX_Pebble_Impact.SFX_Pebble_Impact"));
	if (SoundFinder.Succeeded())
	{
		PaymentSound = SoundFinder.Object;
	}

	RestitutionPrompt = FText::FromString(TEXT("Leave 2 Copper Annas (Restitution for Broken Terracotta)"));
	PaidPrompt = FText::FromString(TEXT("Restitution Already Left on Potter's Bench"));
}

void ARestitutionDropActor::BeginPlay()
{
	Super::BeginPlay();
	UE_LOG(LogREVOLUTION, Log, TEXT("RestitutionDropActor spawned at %s for cluster '%s'"),
		*GetActorLocation().ToString(), *CommunityClusterID.ToString());
}

void ARestitutionDropActor::OnInteract_Implementation(ARevolutionCharacter* Interactor)
{
	if (bHasBeenPaid)
	{
		return;
	}

	bHasBeenPaid = true;

	if (PaymentSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, PaymentSound, GetActorLocation(), 1.0f, 1.15f);
	}

	if (UWorld* World = GetWorld())
	{
		if (UCommunityTrustSubsystem* TrustSubsystem = World->GetSubsystem<UCommunityTrustSubsystem>())
		{
			TrustSubsystem->AdjustClusterScore(
				CommunityClusterID,
				RestitutionTrustBonus,
				FName(TEXT("Restitution_Reparation_Paid")),
				Interactor
			);

			UE_LOG(LogREVOLUTION, Warning, TEXT("[Restitution] Kabir deposited reparation in cluster '%s'. Trust +%d!"),
				*CommunityClusterID.ToString(), RestitutionTrustBonus);
		}
	}
}

FText ARestitutionDropActor::GetInteractionPrompt_Implementation() const
{
	return bHasBeenPaid ? PaidPrompt : RestitutionPrompt;
}

bool ARestitutionDropActor::CanInteract_Implementation(const ARevolutionCharacter* Interactor) const
{
	return !bHasBeenPaid;
}

void ARestitutionDropActor::ResetRestitution()
{
	bHasBeenPaid = false;
}
