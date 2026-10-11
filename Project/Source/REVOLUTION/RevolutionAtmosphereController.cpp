// Copyright Epic Games, Inc. All Rights Reserved.

#include "RevolutionAtmosphereController.h"
#include "Engine/DirectionalLight.h"
#include "Engine/SkyLight.h"
#include "Engine/ExponentialHeightFog.h"
#include "Components/DirectionalLightComponent.h"
#include "Components/SkyLightComponent.h"
#include "Components/ExponentialHeightFogComponent.h"
#include "Kismet/GameplayStatics.h"
#include "UObject/ConstructorHelpers.h"
#include "Sound/SoundBase.h"
#include "EngineUtils.h"
#include "REVOLUTION.h"

ARevolutionAtmosphereController::ARevolutionAtmosphereController()
{
	PrimaryActorTick.bCanEverTick = true;

	NightRotation = FRotator(-68.0f, 40.0f, 0.0f);
	DawnRotation = FRotator(-6.5f, 85.0f, 0.0f);

	NightSunIntensity = 2.5f;
	DawnSunIntensity = 16.0f;

	NightSunColor = FLinearColor(0.60f, 0.72f, 0.95f, 1.0f);
	DawnSunColor = FLinearColor(1.0f, 0.76f, 0.52f, 1.0f);

	NightSkyLightIntensity = 0.25f;
	DawnSkyLightIntensity = 1.05f;

	static ConstructorHelpers::FObjectFinder<USoundBase> BellSoundFinder(TEXT("/Game/Audio/SFX/SFX_Dawn_Temple_Bell.SFX_Dawn_Temple_Bell"));
	if (BellSoundFinder.Succeeded())
	{
		DawnTempleBellSound = BellSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> TrainSoundFinder(TEXT("/Game/Audio/SFX/SFX_Train_Distant_Rumble.SFX_Train_Distant_Rumble"));
	if (TrainSoundFinder.Succeeded())
	{
		TrainDistantSound = TrainSoundFinder.Object;
	}
}

void ARevolutionAtmosphereController::BeginPlay()
{
	Super::BeginPlay();

	UWorld* World = GetWorld();
	if (!World) return;

	// Locate environment lighting actors
	for (TActorIterator<ADirectionalLight> It(World); It; ++It)
	{
		SunMoonLight = *It;
		break;
	}

	for (TActorIterator<ASkyLight> It(World); It; ++It)
	{
		SkyLightActor = *It;
		break;
	}

	for (TActorIterator<AExponentialHeightFog> It(World); It; ++It)
	{
		HeightFogActor = *It;
		break;
	}

	// Apply Initial Curfew Midnight Atmosphere
	if (SunMoonLight)
	{
		SunMoonLight->SetMobility(EComponentMobility::Movable);
		if (UDirectionalLightComponent* LightComp = Cast<UDirectionalLightComponent>(SunMoonLight->GetComponentByClass(UDirectionalLightComponent::StaticClass())))
		{
			LightComp->SetMobility(EComponentMobility::Movable);
			LightComp->SetIntensity(NightSunIntensity);
			LightComp->SetLightColor(NightSunColor);
			LightComp->SetTemperature(8500.0f);
			LightComp->SetUseTemperature(true);
		}
		SunMoonLight->SetActorRotation(NightRotation);
	}

	if (SkyLightActor)
	{
		if (USkyLightComponent* SkyComp = Cast<USkyLightComponent>(SkyLightActor->GetComponentByClass(USkyLightComponent::StaticClass())))
		{
			SkyComp->SetIntensity(NightSkyLightIntensity);
		}
	}

	// Subscribe to mission events for the dawn break trigger
	if (URevolutionMissionSubsystem* Subsystem = World->GetSubsystem<URevolutionMissionSubsystem>())
	{
		Subsystem->OnMissionDirectiveChanged.AddDynamic(this, &ARevolutionAtmosphereController::HandleMissionDirectiveChanged);
	}

	UE_LOG(LogREVOLUTION, Log, TEXT("RevolutionAtmosphereController initialized with Curfew Nocturnal lighting."));
}

void ARevolutionAtmosphereController::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	// Periodic Environmental Sound Masking (North Western Railway Steam Train)
	if (!bIsSoundMasked)
	{
		TrainScheduleTimer += DeltaTime;
		if (TrainScheduleTimer >= TrainInterval)
		{
			TrainScheduleTimer = 0.0f;
			bIsSoundMasked = true;
			TrainMaskDurationTimer = 0.0f;

			if (TrainDistantSound)
			{
				UGameplayStatics::PlaySound2D(this, TrainDistantSound, 0.85f);
			}

			UE_LOG(LogREVOLUTION, Log, TEXT("North Western Railway train rumble echoing across Kot Gurdarshan: Footstep noise masked!"));
		}
	}
	else
	{
		TrainMaskDurationTimer += DeltaTime;
		if (TrainMaskDurationTimer >= TrainDuration)
		{
			bIsSoundMasked = false;
			TrainMaskDurationTimer = 0.0f;
			UE_LOG(LogREVOLUTION, Log, TEXT("Train rumble faded: Environmental acoustic masking ended."));
		}
	}

	if (bIsTransitioningToDawn)
	{
		TransitionProgress = FMath::Clamp(TransitionProgress + (DeltaTime / TransitionDuration), 0.0f, 1.0f);
		float Alpha = FMath::SmoothStep(0.0f, 1.0f, TransitionProgress);

		if (SunMoonLight)
		{
			FRotator CurrRot = FMath::Lerp(NightRotation, DawnRotation, Alpha);
			SunMoonLight->SetActorRotation(CurrRot);

			if (UDirectionalLightComponent* LightComp = Cast<UDirectionalLightComponent>(SunMoonLight->GetComponentByClass(UDirectionalLightComponent::StaticClass())))
			{
				LightComp->SetIntensity(FMath::Lerp(NightSunIntensity, DawnSunIntensity, Alpha));
				LightComp->SetLightColor(FMath::Lerp(NightSunColor, DawnSunColor, Alpha));
				LightComp->SetTemperature(FMath::Lerp(8500.0f, 2850.0f, Alpha));
			}
		}

		if (SkyLightActor)
		{
			if (USkyLightComponent* SkyComp = Cast<USkyLightComponent>(SkyLightActor->GetComponentByClass(USkyLightComponent::StaticClass())))
			{
				SkyComp->SetIntensity(FMath::Lerp(NightSkyLightIntensity, DawnSkyLightIntensity, Alpha));
			}
		}

		if (TransitionProgress >= 1.0f)
		{
			bIsTransitioningToDawn = false;
			UE_LOG(LogREVOLUTION, Log, TEXT("Atmospheric dawn transition complete: April 1919 morning light established."));
		}
	}
}

void ARevolutionAtmosphereController::HandleMissionDirectiveChanged(ECourierMissionStage NewStage, FText Title, FText Directive)
{
	if (NewStage == ECourierMissionStage::Stage_Completed)
	{
		bIsTransitioningToDawn = true;
		TransitionProgress = 0.0f;

		if (DawnTempleBellSound)
		{
			UGameplayStatics::PlaySound2D(this, DawnTempleBellSound, 1.0f);
		}

		UE_LOG(LogREVOLUTION, Log, TEXT("Mission complete! Initiating historical 1919 dawn atmosphere transition."));
	}
}
