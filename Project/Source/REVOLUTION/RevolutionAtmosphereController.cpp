// Copyright Epic Games, Inc. All Rights Reserved.

#include "RevolutionAtmosphereController.h"
#include "Engine/DirectionalLight.h"
#include "Engine/SkyLight.h"
#include "Engine/ExponentialHeightFog.h"
#include "Components/DirectionalLightComponent.h"
#include "Components/SkyLightComponent.h"
#include "Components/ExponentialHeightFogComponent.h"
#include "Components/AudioComponent.h"
#include "Kismet/GameplayStatics.h"
#include "UObject/ConstructorHelpers.h"
#include "Sound/SoundBase.h"
#include "Sound/SoundMix.h"
#include "EngineUtils.h"
#include "REVOLUTION.h"

ARevolutionAtmosphereController::ARevolutionAtmosphereController()
{
	PrimaryActorTick.bCanEverTick = true;

	CurrentPhase = EHistoricalAtmospherePhase::MorningDawn;
	CurrentWeather = EHistoricalWeatherState::GoldenHaze;
	CurrentSettings = GetSettingsForPhase(CurrentPhase);
	TargetSettings = CurrentSettings;
	SourceSettings = CurrentSettings;

	WeatherAudioComponent = CreateDefaultSubobject<UAudioComponent>(TEXT("WeatherAudioComponent"));
	WeatherAudioComponent->SetupAttachment(RootComponent);
	WeatherAudioComponent->bAutoActivate = false;

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

	static ConstructorHelpers::FObjectFinder<USoundBase> WhistleSoundFinder(TEXT("/Game/Audio/SFX/SFX_Police_Whistle_Curfew.SFX_Police_Whistle_Curfew"));
	if (WhistleSoundFinder.Succeeded())
	{
		CurfewWhistleSound = WhistleSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> CanalSoundFinder(TEXT("/Game/Audio/SFX/SFX_Canal_Water_Flow_Gentle.SFX_Canal_Water_Flow_Gentle"));
	if (CanalSoundFinder.Succeeded())
	{
		CanalWaterSound = CanalSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> DustWindFinder(TEXT("/Game/Audio/Weather/SFX_Weather_DustStorm_Wind_Loop.SFX_Weather_DustStorm_Wind_Loop"));
	if (DustWindFinder.Succeeded())
	{
		DustStormWindSound = DustWindFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> BreezeFinder(TEXT("/Game/Audio/Weather/SFX_Weather_GoldenHaze_Breeze.SFX_Weather_GoldenHaze_Breeze"));
	if (BreezeFinder.Succeeded())
	{
		GoldenHazeBreezeSound = BreezeFinder.Object;
	}
}

FHistoricalAtmosphereSettings ARevolutionAtmosphereController::GetSettingsForPhase(EHistoricalAtmospherePhase Phase) const
{
	FHistoricalAtmosphereSettings Settings;

	switch (Phase)
	{
	case EHistoricalAtmospherePhase::MorningDawn:
		// Act I: 1919 Morning Dawn — warm golden sunlight breaking over haveli parapets, soft morning mist
		Settings.SunRotation = FRotator(-15.0f, 75.0f, 0.0f);
		Settings.SunIntensity = 14.0f;
		Settings.SunColor = FLinearColor(1.0f, 0.82f, 0.60f, 1.0f);
		Settings.SunTemperature = 3200.0f;
		Settings.SkyLightIntensity = 0.85f;
		Settings.SkyLightColor = FLinearColor(0.82f, 0.88f, 1.0f, 1.0f);
		Settings.FogDensity = 0.012f;
		Settings.FogHeightFalloff = 0.25f;
		Settings.FogInscatteringColor = FLinearColor(0.85f, 0.75f, 0.60f, 1.0f);
		Settings.WeatherState = EHistoricalWeatherState::GoldenHaze;
		Settings.VolumetricFogScatteringDistribution = 0.45f;
		Settings.VolumetricFogExtinctionScale = 1.0f;
		Settings.WindIntensity = 0.20f;
		Settings.DirectionalInscatteringColor = FLinearColor(0.95f, 0.78f, 0.50f, 1.0f);
		break;

	case EHistoricalAtmospherePhase::BaisakhiMidday:
		// Act II: Baisakhi Festival Midday — bright, vibrant Punjabi spring sun, crisp visibility in bazaars
		Settings.SunRotation = FRotator(-62.0f, 165.0f, 0.0f);
		Settings.SunIntensity = 28.0f;
		Settings.SunColor = FLinearColor(1.0f, 0.96f, 0.90f, 1.0f);
		Settings.SunTemperature = 5200.0f;
		Settings.SkyLightIntensity = 1.25f;
		Settings.SkyLightColor = FLinearColor(0.75f, 0.85f, 1.0f, 1.0f);
		Settings.FogDensity = 0.004f;
		Settings.FogHeightFalloff = 0.15f;
		Settings.FogInscatteringColor = FLinearColor(0.80f, 0.85f, 0.95f, 1.0f);
		Settings.WeatherState = EHistoricalWeatherState::ClearSky;
		Settings.VolumetricFogScatteringDistribution = 0.20f;
		Settings.VolumetricFogExtinctionScale = 0.8f;
		Settings.WindIntensity = 0.10f;
		Settings.DirectionalInscatteringColor = FLinearColor(0.85f, 0.85f, 0.90f, 1.0f);
		break;

	case EHistoricalAtmospherePhase::CurfewNight:
		// Act III: Martial Law Curfew Night — sharp high-contrast moonlight, cold blue shadows, dense urban smog
		Settings.SunRotation = FRotator(-68.0f, 40.0f, 0.0f);
		Settings.SunIntensity = 2.2f;
		Settings.SunColor = FLinearColor(0.55f, 0.68f, 0.95f, 1.0f);
		Settings.SunTemperature = 8500.0f;
		Settings.SkyLightIntensity = 0.20f;
		Settings.SkyLightColor = FLinearColor(0.40f, 0.55f, 0.85f, 1.0f);
		Settings.FogDensity = 0.040f;
		Settings.FogHeightFalloff = 0.35f;
		Settings.FogInscatteringColor = FLinearColor(0.15f, 0.20f, 0.35f, 1.0f);
		Settings.WeatherState = EHistoricalWeatherState::CurfewSmog;
		Settings.VolumetricFogScatteringDistribution = 0.65f;
		Settings.VolumetricFogExtinctionScale = 1.8f;
		Settings.WindIntensity = 0.30f;
		Settings.DirectionalInscatteringColor = FLinearColor(0.15f, 0.20f, 0.35f, 1.0f);
		break;

	case EHistoricalAtmospherePhase::CanalNight:
		// Act IV: Upper Bari Doab Outskirts — pale river moonlight, heavy ground fog rolling off water canals
		Settings.SunRotation = FRotator(-48.0f, 25.0f, 0.0f);
		Settings.SunIntensity = 3.2f;
		Settings.SunColor = FLinearColor(0.65f, 0.78f, 0.92f, 1.0f);
		Settings.SunTemperature = 6500.0f;
		Settings.SkyLightIntensity = 0.32f;
		Settings.SkyLightColor = FLinearColor(0.45f, 0.60f, 0.80f, 1.0f);
		Settings.FogDensity = 0.058f;
		Settings.FogHeightFalloff = 0.45f;
		Settings.FogInscatteringColor = FLinearColor(0.20f, 0.30f, 0.40f, 1.0f);
		Settings.WeatherState = EHistoricalWeatherState::GoldenHaze;
		Settings.VolumetricFogScatteringDistribution = 0.55f;
		Settings.VolumetricFogExtinctionScale = 1.5f;
		Settings.WindIntensity = 0.25f;
		Settings.DirectionalInscatteringColor = FLinearColor(0.25f, 0.35f, 0.50f, 1.0f);
		break;

	case EHistoricalAtmospherePhase::GoldenSunrise:
		// Act V: Golden Sunrise Finale — triumphant golden dawn breaking across the North Western Railway cutting
		Settings.SunRotation = FRotator(-6.5f, 85.0f, 0.0f);
		Settings.SunIntensity = 22.0f;
		Settings.SunColor = FLinearColor(1.0f, 0.74f, 0.45f, 1.0f);
		Settings.SunTemperature = 2850.0f;
		Settings.SkyLightIntensity = 1.15f;
		Settings.SkyLightColor = FLinearColor(0.95f, 0.80f, 0.65f, 1.0f);
		Settings.FogDensity = 0.018f;
		Settings.FogHeightFalloff = 0.20f;
		Settings.FogInscatteringColor = FLinearColor(0.95f, 0.70f, 0.45f, 1.0f);
		Settings.WeatherState = EHistoricalWeatherState::GoldenHaze;
		Settings.VolumetricFogScatteringDistribution = 0.75f;
		Settings.VolumetricFogExtinctionScale = 1.2f;
		Settings.WindIntensity = 0.25f;
		Settings.DirectionalInscatteringColor = FLinearColor(1.0f, 0.75f, 0.40f, 1.0f);
		break;
	}

	return Settings;
}

FHistoricalAtmosphereSettings ARevolutionAtmosphereController::GetSettingsForWeather(EHistoricalWeatherState Weather) const
{
	FHistoricalAtmosphereSettings Settings = GetSettingsForPhase(CurrentPhase);
	Settings.WeatherState = Weather;

	switch (Weather)
	{
	case EHistoricalWeatherState::ClearSky:
		Settings.FogDensity = 0.003f;
		Settings.VolumetricFogScatteringDistribution = 0.20f;
		Settings.VolumetricFogExtinctionScale = 0.8f;
		Settings.WindIntensity = 0.10f;
		break;

	case EHistoricalWeatherState::GoldenHaze:
		Settings.FogDensity = 0.016f;
		Settings.FogInscatteringColor = FLinearColor(0.92f, 0.78f, 0.55f, 1.0f);
		Settings.VolumetricFogScatteringDistribution = 0.55f;
		Settings.VolumetricFogExtinctionScale = 1.2f;
		Settings.WindIntensity = 0.22f;
		Settings.DirectionalInscatteringColor = FLinearColor(0.96f, 0.80f, 0.52f, 1.0f);
		break;

	case EHistoricalWeatherState::DustStormAndhi:
		// Northern Indian pre-monsoonal Andhi dust squall: rich ochre alluvial particulate haze
		Settings.SunIntensity *= 0.60f;
		Settings.SunColor = FLinearColor(1.0f, 0.68f, 0.35f, 1.0f);
		Settings.SunTemperature = 3800.0f;
		Settings.FogDensity = 0.075f;
		Settings.FogHeightFalloff = 0.30f;
		Settings.FogInscatteringColor = FLinearColor(0.92f, 0.64f, 0.32f, 1.0f);
		Settings.VolumetricFogScatteringDistribution = 0.75f;
		Settings.VolumetricFogExtinctionScale = 2.4f;
		Settings.WindIntensity = 0.85f;
		Settings.DirectionalInscatteringColor = FLinearColor(0.92f, 0.62f, 0.28f, 1.0f);
		break;

	case EHistoricalWeatherState::CurfewSmog:
		Settings.FogDensity = 0.045f;
		Settings.FogInscatteringColor = FLinearColor(0.18f, 0.22f, 0.38f, 1.0f);
		Settings.VolumetricFogScatteringDistribution = 0.65f;
		Settings.VolumetricFogExtinctionScale = 1.8f;
		Settings.WindIntensity = 0.35f;
		Settings.DirectionalInscatteringColor = FLinearColor(0.15f, 0.20f, 0.35f, 1.0f);
		break;
	}

	return Settings;
}

void ARevolutionAtmosphereController::BeginPlay()
{
	Super::BeginPlay();

	UWorld* World = GetWorld();
	if (!World) return;

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

	EHistoricalAtmospherePhase InitialPhase = EHistoricalAtmospherePhase::MorningDawn;

	if (URevolutionMissionSubsystem* Subsystem = World->GetSubsystem<URevolutionMissionSubsystem>())
	{
		Subsystem->OnMissionDirectiveChanged.AddDynamic(this, &ARevolutionAtmosphereController::HandleMissionDirectiveChanged);
		ECourierMissionStage InitStage = Subsystem->GetCurrentStage();

		if (InitStage <= ECourierMissionStage::Stage_Morning_ClassroomDesk)
		{
			InitialPhase = EHistoricalAtmospherePhase::MorningDawn;
		}
		else if (InitStage <= ECourierMissionStage::Stage_ActII_Completed)
		{
			InitialPhase = EHistoricalAtmospherePhase::BaisakhiMidday;
		}
		else if (InitStage <= ECourierMissionStage::Stage_ActIII_Completed)
		{
			InitialPhase = EHistoricalAtmospherePhase::CurfewNight;
		}
		else if (InitStage < ECourierMissionStage::Stage_Completed)
		{
			InitialPhase = EHistoricalAtmospherePhase::CanalNight;
		}
		else
		{
			InitialPhase = EHistoricalAtmospherePhase::GoldenSunrise;
		}
	}

	SetAtmospherePhase(InitialPhase, 0.0f);
	UE_LOG(LogREVOLUTION, Log, TEXT("RevolutionAtmosphereController initialized with Historical Phase %d and Weather %d."), (int32)InitialPhase, (int32)CurrentWeather);
}

void ARevolutionAtmosphereController::ApplyAtmosphereSettings(const FHistoricalAtmosphereSettings& Settings)
{
	CurrentSettings = Settings;
	CurrentWeather = Settings.WeatherState;

	if (SunMoonLight)
	{
		SunMoonLight->SetMobility(EComponentMobility::Movable);
		SunMoonLight->SetActorRotation(Settings.SunRotation);

		if (UDirectionalLightComponent* LightComp = Cast<UDirectionalLightComponent>(SunMoonLight->GetComponentByClass(UDirectionalLightComponent::StaticClass())))
		{
			LightComp->SetMobility(EComponentMobility::Movable);
			LightComp->SetIntensity(Settings.SunIntensity);
			LightComp->SetLightColor(Settings.SunColor);
			LightComp->SetTemperature(Settings.SunTemperature);
			LightComp->SetUseTemperature(true);
		}
	}

	if (SkyLightActor)
	{
		if (USkyLightComponent* SkyComp = Cast<USkyLightComponent>(SkyLightActor->GetComponentByClass(USkyLightComponent::StaticClass())))
		{
			SkyComp->SetIntensity(Settings.SkyLightIntensity);
			SkyComp->SetLightColor(Settings.SkyLightColor);
		}
	}

	if (HeightFogActor)
	{
		if (UExponentialHeightFogComponent* FogComp = Cast<UExponentialHeightFogComponent>(HeightFogActor->GetComponentByClass(UExponentialHeightFogComponent::StaticClass())))
		{
			FogComp->SetFogDensity(Settings.FogDensity);
			FogComp->SetFogHeightFalloff(Settings.FogHeightFalloff);
			FogComp->SetFogInscatteringColor(Settings.FogInscatteringColor);
			FogComp->SetDirectionalInscatteringColor(Settings.DirectionalInscatteringColor);
			FogComp->SetVolumetricFog(true);
			FogComp->SetVolumetricFogScatteringDistribution(Settings.VolumetricFogScatteringDistribution);
			FogComp->SetVolumetricFogExtinctionScale(Settings.VolumetricFogExtinctionScale);
		}
	}
}

float ARevolutionAtmosphereController::GetWeatherVisibilityMultiplier() const
{
	if (CurrentWeather == EHistoricalWeatherState::DustStormAndhi)
	{
		return 0.65f; // 35% reduction in sentry visual perception!
	}
	return 1.0f;
}

bool ARevolutionAtmosphereController::IsWeatherSoundMasked() const
{
	return CurrentWeather == EHistoricalWeatherState::DustStormAndhi;
}

void ARevolutionAtmosphereController::SetAtmospherePhase(EHistoricalAtmospherePhase NewPhase, float InTransitionDuration)
{
	CurrentPhase = NewPhase;
	TargetSettings = GetSettingsForPhase(NewPhase);

	if (InTransitionDuration <= 0.0f)
	{
		bIsTransitioning = false;
		ApplyAtmosphereSettings(TargetSettings);
	}
	else
	{
		SourceSettings = CurrentSettings;
		TransitionDuration = InTransitionDuration;
		TransitionProgress = 0.0f;
		bIsTransitioning = true;
	}

	switch (NewPhase)
	{
	case EHistoricalAtmospherePhase::MorningDawn:
	case EHistoricalAtmospherePhase::GoldenSunrise:
		if (DawnTempleBellSound)
		{
			UGameplayStatics::PlaySound2D(this, DawnTempleBellSound, 0.9f);
		}
		break;
	case EHistoricalAtmospherePhase::CurfewNight:
		if (CurfewWhistleSound)
		{
			UGameplayStatics::PlaySound2D(this, CurfewWhistleSound, 0.85f);
		}
		break;
	case EHistoricalAtmospherePhase::CanalNight:
		if (CanalWaterSound)
		{
			UGameplayStatics::PlaySound2D(this, CanalWaterSound, 0.80f);
		}
		break;
	default:
		break;
	}

	if (UWorld* World = GetWorld())
	{
		if (NewPhase == EHistoricalAtmospherePhase::CurfewNight)
		{
			if (DefaultSoundMix)
			{
				UGameplayStatics::PopSoundMixModifier(World, DefaultSoundMix);
			}
			if (CurfewSoundMix)
			{
				UGameplayStatics::PushSoundMixModifier(World, CurfewSoundMix);
				UE_LOG(LogREVOLUTION, Log, TEXT("RevolutionAtmosphereController: Pushed CurfewSoundMix modifier."));
			}
		}
		else
		{
			if (CurfewSoundMix)
			{
				UGameplayStatics::PopSoundMixModifier(World, CurfewSoundMix);
			}
			if (DefaultSoundMix)
			{
				UGameplayStatics::PushSoundMixModifier(World, DefaultSoundMix);
			}
		}
	}

	UE_LOG(LogREVOLUTION, Log, TEXT("RevolutionAtmosphereController: Transitioning to Atmosphere Phase %d over %.1f seconds."), (int32)NewPhase, InTransitionDuration);
}

void ARevolutionAtmosphereController::SetWeatherState(EHistoricalWeatherState NewWeather, float InTransitionDuration)
{
	CurrentWeather = NewWeather;
	TargetSettings = GetSettingsForWeather(NewWeather);

	if (InTransitionDuration <= 0.0f)
	{
		bIsTransitioning = false;
		ApplyAtmosphereSettings(TargetSettings);
	}
	else
	{
		SourceSettings = CurrentSettings;
		TransitionDuration = InTransitionDuration;
		TransitionProgress = 0.0f;
		bIsTransitioning = true;
	}

	if (WeatherAudioComponent)
	{
		if (CurrentWeather == EHistoricalWeatherState::DustStormAndhi && DustStormWindSound)
		{
			WeatherAudioComponent->SetSound(DustStormWindSound);
			WeatherAudioComponent->FadeIn(2.0f, 0.90f);
		}
		else if (CurrentWeather == EHistoricalWeatherState::GoldenHaze && GoldenHazeBreezeSound)
		{
			WeatherAudioComponent->SetSound(GoldenHazeBreezeSound);
			WeatherAudioComponent->FadeIn(3.0f, 0.70f);
		}
		else
		{
			WeatherAudioComponent->FadeOut(2.0f, 0.0f);
		}
	}

	UE_LOG(LogREVOLUTION, Log, TEXT("RevolutionAtmosphereController: Set Weather State to %d."), (int32)NewWeather);
}

void ARevolutionAtmosphereController::TriggerDustStorm(float Duration)
{
	DustStormRemainingTimer = Duration;
	SetWeatherState(EHistoricalWeatherState::DustStormAndhi, 4.0f);
	UE_LOG(LogREVOLUTION, Log, TEXT("Triggered Andhi Dust Storm for %.1f seconds."), Duration);
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

	// Dust storm timer countdown
	if (DustStormRemainingTimer > 0.0f)
	{
		DustStormRemainingTimer -= DeltaTime;
		if (DustStormRemainingTimer <= 0.0f)
		{
			DustStormRemainingTimer = 0.0f;
			// Restore weather matching current phase
			SetWeatherState(GetSettingsForPhase(CurrentPhase).WeatherState, 6.0f);
			UE_LOG(LogREVOLUTION, Log, TEXT("Andhi Dust Storm subsided: Restored phase weather."));
		}
	}

	// Smooth Atmosphere Phase / Weather Interpolation
	if (bIsTransitioning)
	{
		TransitionProgress = FMath::Clamp(TransitionProgress + (DeltaTime / TransitionDuration), 0.0f, 1.0f);
		float Alpha = FMath::SmoothStep(0.0f, 1.0f, TransitionProgress);

		FHistoricalAtmosphereSettings InterpSettings;
		InterpSettings.SunRotation = FRotator(
			FMath::Lerp(SourceSettings.SunRotation.Pitch, TargetSettings.SunRotation.Pitch, Alpha),
			FMath::Lerp(SourceSettings.SunRotation.Yaw, TargetSettings.SunRotation.Yaw, Alpha),
			FMath::Lerp(SourceSettings.SunRotation.Roll, TargetSettings.SunRotation.Roll, Alpha)
		);
		InterpSettings.SunIntensity = FMath::Lerp(SourceSettings.SunIntensity, TargetSettings.SunIntensity, Alpha);
		InterpSettings.SunColor = FMath::Lerp(SourceSettings.SunColor, TargetSettings.SunColor, Alpha);
		InterpSettings.SunTemperature = FMath::Lerp(SourceSettings.SunTemperature, TargetSettings.SunTemperature, Alpha);
		InterpSettings.SkyLightIntensity = FMath::Lerp(SourceSettings.SkyLightIntensity, TargetSettings.SkyLightIntensity, Alpha);
		InterpSettings.SkyLightColor = FMath::Lerp(SourceSettings.SkyLightColor, TargetSettings.SkyLightColor, Alpha);
		InterpSettings.FogDensity = FMath::Lerp(SourceSettings.FogDensity, TargetSettings.FogDensity, Alpha);
		InterpSettings.FogHeightFalloff = FMath::Lerp(SourceSettings.FogHeightFalloff, TargetSettings.FogHeightFalloff, Alpha);
		InterpSettings.FogInscatteringColor = FMath::Lerp(SourceSettings.FogInscatteringColor, TargetSettings.FogInscatteringColor, Alpha);
		InterpSettings.VolumetricFogScatteringDistribution = FMath::Lerp(SourceSettings.VolumetricFogScatteringDistribution, TargetSettings.VolumetricFogScatteringDistribution, Alpha);
		InterpSettings.VolumetricFogExtinctionScale = FMath::Lerp(SourceSettings.VolumetricFogExtinctionScale, TargetSettings.VolumetricFogExtinctionScale, Alpha);
		InterpSettings.WindIntensity = FMath::Lerp(SourceSettings.WindIntensity, TargetSettings.WindIntensity, Alpha);
		InterpSettings.DirectionalInscatteringColor = FMath::Lerp(SourceSettings.DirectionalInscatteringColor, TargetSettings.DirectionalInscatteringColor, Alpha);
		InterpSettings.WeatherState = TargetSettings.WeatherState;

		ApplyAtmosphereSettings(InterpSettings);

		if (TransitionProgress >= 1.0f)
		{
			bIsTransitioning = false;
			ApplyAtmosphereSettings(TargetSettings);
			UE_LOG(LogREVOLUTION, Log, TEXT("RevolutionAtmosphereController: Atmosphere transition complete."));
		}
	}
}

void ARevolutionAtmosphereController::HandleMissionDirectiveChanged(ECourierMissionStage NewStage, FText Title, FText Directive)
{
	EHistoricalAtmospherePhase DesiredPhase = CurrentPhase;

	if (NewStage <= ECourierMissionStage::Stage_Morning_ClassroomDesk)
	{
		DesiredPhase = EHistoricalAtmospherePhase::MorningDawn;
	}
	else if (NewStage <= ECourierMissionStage::Stage_ActII_Completed)
	{
		DesiredPhase = EHistoricalAtmospherePhase::BaisakhiMidday;
	}
	else if (NewStage <= ECourierMissionStage::Stage_ActIII_Completed)
	{
		DesiredPhase = EHistoricalAtmospherePhase::CurfewNight;
	}
	else if (NewStage < ECourierMissionStage::Stage_Completed)
	{
		DesiredPhase = EHistoricalAtmospherePhase::CanalNight;
	}
	else
	{
		DesiredPhase = EHistoricalAtmospherePhase::GoldenSunrise;
	}

	if (DesiredPhase != CurrentPhase)
	{
		SetAtmospherePhase(DesiredPhase, 10.0f);
	}
}
