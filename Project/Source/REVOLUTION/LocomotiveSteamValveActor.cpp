// Copyright Epic Games, Inc. All Rights Reserved.

#include "LocomotiveSteamValveActor.h"
#include "RevolutionCharacter.h"
#include "CurfewPatrolAI.h"
#include "RevolutionMissionSubsystem.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SceneComponent.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/SoundBase.h"
#include "EngineUtils.h"
#include "Engine/World.h"
#include "REVOLUTION.h"

ALocomotiveSteamValveActor::ALocomotiveSteamValveActor()
{
	PrimaryActorTick.bCanEverTick = true;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	ValveMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("ValveMesh"));
	ValveMesh->SetupAttachment(RootComponent);
	ValveMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	ValveMesh->SetRelativeScale3D(FVector(0.35f, 0.35f, 0.35f));

	SteamPlumeMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("SteamPlumeMesh"));
	SteamPlumeMesh->SetupAttachment(RootComponent);
	SteamPlumeMesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	SteamPlumeMesh->SetRelativeScale3D(FVector(1.0f, 1.0f, 1.0f));
	SteamPlumeMesh->SetVisibility(false);

	ValveTitle = FText::FromString(TEXT("Broad-Gauge Locomotive Pressure Relief Valve"));
	ValveLore = FText::FromString(
		TEXT("Venting the British 4-6-0 steam locomotive's high-pressure boiler releases an immense shroud of scalding white vapor across the railway cutting. The sudden hiss blinds sentry line-of-sight and lures colonial pickets away from the Civil Lines security palisade.")
	);
}

void ALocomotiveSteamValveActor::BeginPlay()
{
	Super::BeginPlay();

	if (!SteamHissSound)
	{
		SteamHissSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Locomotive_Steam_Hiss.SFX_Locomotive_Steam_Hiss"));
	}

	if (SteamPlumeMesh && !SteamPlumeMesh->GetStaticMesh())
	{
		UStaticMesh* PlaneMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Plane.Plane"));
		if (PlaneMesh)
		{
			SteamPlumeMesh->SetStaticMesh(PlaneMesh);
			SteamPlumeMesh->SetRelativeRotation(FRotator(90.0f, 0.0f, 0.0f));
		}
	}

	if (SteamPlumeMesh && !SteamPlumeMaterial)
	{
		SteamPlumeMaterial = LoadObject<UMaterialInterface>(nullptr, TEXT("/Game/VFX/Smoke/Materials/MI_Smoke_Locomotive_Steam.MI_Smoke_Locomotive_Steam"));
		if (SteamPlumeMaterial)
		{
			SteamPlumeMesh->SetMaterial(0, SteamPlumeMaterial);
		}
	}
}

void ALocomotiveSteamValveActor::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	if (VentCooldownTimer > 0.0f)
	{
		VentCooldownTimer = FMath::Max(0.0f, VentCooldownTimer - DeltaTime);

		if (SteamPlumeMesh && SteamObscurityDuration > 0.0f)
		{
			const float NormalizedRemaining = VentCooldownTimer / SteamObscurityDuration;
			// RDR2 Billowing expansion: scales outward from 1.0 up to 4.5
			const float CurrentScale = FMath::Lerp(4.5f, 1.0f, NormalizedRemaining);
			SteamPlumeMesh->SetWorldScale3D(FVector(CurrentScale, CurrentScale, CurrentScale * 1.5f));

			if (VentCooldownTimer <= 0.0f)
			{
				SteamPlumeMesh->SetVisibility(false);
			}
		}
	}
}

bool ALocomotiveSteamValveActor::CanInteract_Implementation(const ARevolutionCharacter* Interactor) const
{
	return VentCooldownTimer <= 0.0f;
}

FText ALocomotiveSteamValveActor::GetInteractionPrompt_Implementation() const
{
	if (VentCooldownTimer > 0.0f)
	{
		return FText::FromString(TEXT("Boiler Pressure Recharging..."));
	}
	return FText::FromString(TEXT("Vent High-Pressure Boiler Steam"));
}

void ALocomotiveSteamValveActor::OnInteract_Implementation(ARevolutionCharacter* Interactor)
{
	if (VentCooldownTimer > 0.0f) return;

	VentCooldownTimer = SteamObscurityDuration;
	bHasBeenVented = true;

	if (SteamPlumeMesh)
	{
		SteamPlumeMesh->SetVisibility(true);
		SteamPlumeMesh->SetWorldScale3D(FVector(1.0f, 1.0f, 1.0f));
	}

	UWorld* World = GetWorld();
	if (!World) return;

	// 1. Play high-pressure boiler hiss audio
	if (SteamHissSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, SteamHissSound, GetActorLocation(), 1.0f);
	}

	// 2. Cloak player with steam obscurity (Hitman / Batman Arkham benchmark)
	if (Interactor)
	{
		Interactor->TriggerSteamObscurity(SteamObscurityDuration);
		Interactor->StartInspection(ValveTitle, ValveLore);
	}

	// 3. Acoustic Distraction: Divert nearby curfew sentries to investigate the steam leak
	int32 DivertedCount = 0;
	for (TActorIterator<ACurfewPatrolAI> It(World); It; ++It)
	{
		ACurfewPatrolAI* Sentry = *It;
		if (Sentry && FVector::Dist(GetActorLocation(), Sentry->GetActorLocation()) <= DistractionRadius)
		{
			Sentry->InvestigateSoundLocation(GetActorLocation());
			DivertedCount++;
		}
	}

	UE_LOG(LogREVOLUTION, Log, TEXT("LocomotiveSteamValve vented! Cloaked player and diverted %d curfew sentries."), DivertedCount);

	// 4. Progress mission if waiting for palisade crossing
	if (URevolutionMissionSubsystem* MissionSubsystem = World->GetSubsystem<URevolutionMissionSubsystem>())
	{
		if (MissionSubsystem->GetCurrentStage() == ECourierMissionStage::Stage_ActV_CrossCivilLinesPalisade)
		{
			MissionSubsystem->AdvanceMissionStage();
		}
	}
}
