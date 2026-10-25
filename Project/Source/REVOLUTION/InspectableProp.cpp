// Copyright Epic Games, Inc. All Rights Reserved.

#include "InspectableProp.h"
#include "Components/StaticMeshComponent.h"
#include "RevolutionCharacter.h"
#include "REVOLUTION.h"

AInspectableProp::AInspectableProp()
{
	PrimaryActorTick.bCanEverTick = false;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	MeshComponent = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("MeshComponent"));
	MeshComponent->SetupAttachment(RootComponent);
	MeshComponent->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	MeshComponent->SetGenerateOverlapEvents(true);

	ItemName = FText::FromString(TEXT("Period Artifact"));
	LoreDescription = FText::FromString(TEXT("A historical item from 1920s Punjab."));
	InteractionVerb = FText::FromString(TEXT("Inspect"));
}

void AInspectableProp::OnInteract_Implementation(ARevolutionCharacter* Interactor)
{
	UE_LOG(LogREVOLUTION, Log, TEXT("Kabir inspected: %s - %s"), *ItemName.ToString(), *LoreDescription.ToString());
	if (Interactor)
	{
		Interactor->StartInspection(ItemName, LoreDescription);
	}
}

FText AInspectableProp::GetInteractionPrompt_Implementation() const
{
	return FText::Format(FText::FromString(TEXT("{0} {1}")), InteractionVerb, ItemName);
}

bool AInspectableProp::CanInteract_Implementation(const ARevolutionCharacter* Interactor) const
{
	return true;
}
