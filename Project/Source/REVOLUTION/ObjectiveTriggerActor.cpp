// Copyright Epic Games, Inc. All Rights Reserved.

#include "ObjectiveTriggerActor.h"
#include "RevolutionCharacter.h"
#include "RevolutionMissionSubsystem.h"
#include "RevolutionGameMode.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SceneComponent.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/SoundBase.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "RevolutionCinematicDirectorActor.h"
#include "REVOLUTION.h"

AObjectiveTriggerActor::AObjectiveTriggerActor()
{
	PrimaryActorTick.bCanEverTick = false;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	MeshComponent = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("MeshComponent"));
	MeshComponent->SetupAttachment(RootComponent);
	MeshComponent->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	MeshComponent->SetCollisionResponseToAllChannels(ECR_Ignore);
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
			if (Subsystem->GetCurrentStage() != RequiredMissionStage)
			{
				return false;
			}
		}
	}

	if (bRequireStealthForInteraction && Interactor)
	{
		const bool bIsCrouched = Interactor->bIsCrouched;
		const bool bIsConcealed = Interactor->GetConcealmentScore() > 0.25f;
		const bool bIsCrowdBlended = Interactor->bIsCrowdBlended;
		if (!bIsCrouched && !bIsConcealed && !bIsCrowdBlended)
		{
			return false;
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

	if (TriggerSound && GetWorld())
	{
		UGameplayStatics::PlaySoundAtLocation(this, TriggerSound, GetActorLocation(), 1.0f);
	}

	if (UWorld* World = GetWorld())
	{
		if (URevolutionMissionSubsystem* Subsystem = World->GetSubsystem<URevolutionMissionSubsystem>())
		{
			Subsystem->AdvanceMissionStage();
		}

		if (ARevolutionGameMode* GM = Cast<ARevolutionGameMode>(World->GetAuthGameMode()))
		{
			FVector CheckpointPos = GetActorLocation() + FVector(0.0f, 0.0f, 15.0f);
			GM->SetCheckpoint(CheckpointPos, GetActorRotation());
		}

		// TASK 35: Act I Finale to Act II Cinematic Handoff
		if (RequiredMissionStage == ECourierMissionStage::Stage_Morning_ClassroomDesk || bTriggerCinematicSequence)
		{
			for (TActorIterator<ARevolutionCinematicDirectorActor> It(World); It; ++It)
			{
				ARevolutionCinematicDirectorActor* Director = *It;
				if (Director)
				{
					if (CinematicSequence)
					{
						Director->PlayCinematicCutscene(CinematicSequence, CinematicChapterTitle, CinematicSubtitle, 1.25f);
					}
					else
					{
						Director->PlayMunadiProclamationCutscene();
					}
					break;
				}
			}
		}
	}

	if (bHideMeshOnTrigger && MeshComponent)
	{
		MeshComponent->SetVisibility(false);
		MeshComponent->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	}

	if (Interactor)
	{
		if (AwardPamphletsOnTrigger > 0)
		{
			Interactor->AddPamphlets(AwardPamphletsOnTrigger);
		}
		Interactor->StartInspection(ItemTitle, HistoricalLoreUponInteraction);
	}

	UE_LOG(LogREVOLUTION, Log, TEXT("ObjectiveTriggerActor triggered: %s (Pamphlets awarded: %d)"), *ItemTitle.ToString(), AwardPamphletsOnTrigger);
}
