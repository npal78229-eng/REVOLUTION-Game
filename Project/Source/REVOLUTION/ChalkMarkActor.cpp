// Copyright Epic Games, Inc. All Rights Reserved.

#include "ChalkMarkActor.h"
#include "Components/SceneComponent.h"
#include "Components/StaticMeshComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "REVOLUTION.h"

AChalkMarkActor::AChalkMarkActor()
{
	PrimaryActorTick.bCanEverTick = false;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	GlyphMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("GlyphMesh"));
	GlyphMesh->SetupAttachment(RootComponent);
	GlyphMesh->SetCollisionProfileName(TEXT("NoCollision"));
	GlyphMesh->SetRelativeScale3D(FVector(0.12f, 0.12f, 0.015f));

	static ConstructorHelpers::FObjectFinder<UStaticMesh> MeshFinder(TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));
	if (MeshFinder.Succeeded())
	{
		GlyphMesh->SetStaticMesh(MeshFinder.Object);
	}
}

void AChalkMarkActor::BeginPlay()
{
	Super::BeginPlay();

	UE_LOG(LogREVOLUTION, Log, TEXT("ChalkMarkActor placed at %s"), *GetActorLocation().ToString());
}
