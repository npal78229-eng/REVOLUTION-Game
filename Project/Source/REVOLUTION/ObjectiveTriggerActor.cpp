// Copyright Epic Games, Inc. All Rights Reserved.

#include "ObjectiveTriggerActor.h"
#include "RevolutionCharacter.h"
#include "RevolutionMissionSubsystem.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SceneComponent.h"
#include "Engine/World.h"
#include "REVOLUTION.h"

AObjectiveTriggerActor::AObjectiveTriggerActor()
{
	PrimaryActorTick.bCanEverTick = false;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	MeshComponent = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("MeshComponent"));
	MeshComponent->SetupAttachment(RootComponent);
	MeshComponent->SetCollisionProfileName(TEXT("BlockAllDynamic"));
}

bool AObjectiveTriggerActor::CanInteract_Implementation(const ARevolutionCharacter* Interactor) const
{
	if (bHasBeenTriggered)
	{
		return false;
	}

	if (const UWorld* World = GetWorld())
	{
		if (const URevolutionMissionSubsystem* Subsystem = World->GetSubsystem<URevolutionMissionSubsystem>())
		{
			return Subsystem->GetCurrentStage() == RequiredMissionStage;
		}
	}

	return true;
}

FText AObjectiveTriggerActor::GetInteractionPrompt_Implementation() const
{
	return InteractionPrompt;
}

void AObjectiveTriggerActor::OnInteract_Implementation(ARevolutionCharacter* Interactor)
{
	if (bHasBeenTriggered)
	{
		return;
	}

	bHasBeenTriggered = true;

	if (UWorld* World = GetWorld())
	{
		if (URevolutionMissionSubsystem* Subsystem = World->GetSubsystem<URevolutionMissionSubsystem>())
		{
			Subsystem->AdvanceMissionStage();
		}
	}

	if (bHideMeshOnTrigger && MeshComponent)
	{
		MeshComponent->SetVisibility(false);
		MeshComponent->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	}

	if (Interactor)
	{
		Interactor->StartInspection(ItemTitle, HistoricalLoreUponInteraction);
	}

	UE_LOG(LogREVOLUTION, Log, TEXT("ObjectiveTriggerActor triggered: %s"), *ItemTitle.ToString());
}
