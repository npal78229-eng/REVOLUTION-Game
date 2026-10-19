// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "RevolutionMissionSubsystem.h"
#include "RevolutionAtmosphereController.generated.h"

class ADirectionalLight;
class ASkyLight;
class AExponentialHeightFog;
class USoundBase;
class USoundMix;
class UAudioComponent;

/**
 * Historical Dynamic Lighting & Atmosphere Phase for REVOLUTION (Kot Gurdarshan / Amritsar, April 1919)
 */
UENUM(BlueprintType)
enum class EHistoricalAtmospherePhase : uint8
{
	MorningDawn UMETA(DisplayName = "1. Morning Dawn (Act I)"),
	BaisakhiMidday UMETA(DisplayName = "2. Baisakhi Festival Midday (Act II)"),
	CurfewNight UMETA(DisplayName = "3. Curfew Martial Law Night (Act III)"),
	CanalNight UMETA(DisplayName = "4. Canal Distributary Night (Act IV)"),
	GoldenSunrise UMETA(DisplayName = "5. Golden Sunrise Finale (Act V)")
};

/**
 * Historical Weather State for REVOLUTION (April 1919 Northern India)
 */
UENUM(BlueprintType)
enum class EHistoricalWeatherState : uint8
{
	ClearSky UMETA(DisplayName = "1. Clear Spring Sky (High Visibility)"),
	GoldenHaze UMETA(DisplayName = "2. Golden Hour River Haze (Soft Inscattering)"),
	DustStormAndhi UMETA(DisplayName = "3. Andhi Dust Storm (Ochre Squall & Sentry Dampening)"),
	CurfewSmog UMETA(DisplayName = "4. Curfew Urban Smog (Martial Night Haze)")
};

USTRUCT(BlueprintType)
struct FHistoricalAtmosphereSettings
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Atmosphere")
	FRotator SunRotation = FRotator(-15.0f, 75.0f, 0.0f);

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Atmosphere")
	float SunIntensity = 14.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Atmosphere")
	FLinearColor SunColor = FLinearColor(1.0f, 0.82f, 0.60f, 1.0f);

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Atmosphere")
	float SunTemperature = 3200.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Atmosphere")
	float SkyLightIntensity = 0.85f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Atmosphere")
	FLinearColor SkyLightColor = FLinearColor(0.82f, 0.88f, 1.0f, 1.0f);

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Atmosphere")
	float FogDensity = 0.012f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Atmosphere")
	float FogHeightFalloff = 0.25f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Atmosphere")
	FLinearColor FogInscatteringColor = FLinearColor(0.85f, 0.75f, 0.60f, 1.0f);

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Atmosphere")
	EHistoricalWeatherState WeatherState = EHistoricalWeatherState::ClearSky;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Atmosphere")
	float VolumetricFogScatteringDistribution = 0.20f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Atmosphere")
	float VolumetricFogExtinctionScale = 1.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Atmosphere")
	float WindIntensity = 0.15f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Atmosphere")
	FLinearColor DirectionalInscatteringColor = FLinearColor(0.85f, 0.75f, 0.60f, 1.0f);
};

/**
 * Historical Dynamic Lighting & Atmosphere Controller for REVOLUTION
 * Dynamically controls the 5 historical atmosphere phases across Act I through Act V
 * and 4 historical weather states (Task 27):
 * 1. Morning Dawn / Golden Haze (3200K warm sunrise, soft mist, Act I)
 * 2. Baisakhi Festival Midday (5200K high spring sun, crisp visibility, Act II)
 * 3. Andhi Dust Storm (Warm ochre convective squall, 35% sentry sight dampening)
 * 4. Curfew Martial Law Night (8500K moonlight, urban smog, lantern contrast, Act III)
 * 5. Canal Distributary Night (6500K pale river moonlight & ground mist, Act IV)
 * 6. Golden Sunrise Finale (2850K golden dawn triumph break, Act V)
 */
UCLASS()
class REVOLUTION_API ARevolutionAtmosphereController : public AActor
{
	GENERATED_BODY()

public:
	ARevolutionAtmosphereController();

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

public:
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Atmosphere")
	ADirectionalLight* SunMoonLight = nullptr;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Atmosphere")
	ASkyLight* SkyLightActor = nullptr;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Atmosphere")
	AExponentialHeightFog* HeightFogActor = nullptr;

	// Audio Assets for Atmosphere Phases & Foley
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* DawnTempleBellSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* CurfewWhistleSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* CanalWaterSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* TrainDistantSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* DustStormWindSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* GoldenHazeBreezeSound = nullptr;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UAudioComponent* WeatherAudioComponent = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundMix* DefaultSoundMix = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundMix* CurfewSoundMix = nullptr;

	// Periodic Environmental Sound Masking (North Western Railway Train)
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Stealth")
	bool bIsSoundMasked = false;

	UFUNCTION(BlueprintPure, Category = "Revolution|Stealth")
	bool IsSoundMasked() const { return bIsSoundMasked; }

	// Current Atmosphere Phase State
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Atmosphere")
	EHistoricalAtmospherePhase CurrentPhase = EHistoricalAtmospherePhase::MorningDawn;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Weather")
	EHistoricalWeatherState CurrentWeather = EHistoricalWeatherState::GoldenHaze;

	UFUNCTION(BlueprintPure, Category = "Revolution|Atmosphere")
	EHistoricalAtmospherePhase GetCurrentPhase() const { return CurrentPhase; }

	UFUNCTION(BlueprintPure, Category = "Revolution|Weather")
	EHistoricalWeatherState GetCurrentWeatherState() const { return CurrentWeather; }

	UFUNCTION(BlueprintPure, Category = "Revolution|Weather")
	float GetWeatherVisibilityMultiplier() const;

	UFUNCTION(BlueprintPure, Category = "Revolution|Weather")
	bool IsWeatherSoundMasked() const;

	UFUNCTION(BlueprintCallable, Category = "Revolution|Atmosphere")
	void SetAtmospherePhase(EHistoricalAtmospherePhase NewPhase, float InTransitionDuration = 8.0f);

	UFUNCTION(BlueprintCallable, Category = "Revolution|Weather")
	void SetWeatherState(EHistoricalWeatherState NewWeather, float InTransitionDuration = 6.0f);

	UFUNCTION(BlueprintCallable, Category = "Revolution|Weather")
	void TriggerDustStorm(float Duration = 30.0f);

	UFUNCTION(BlueprintCallable, Category = "Revolution|Atmosphere")
	void HandleMissionDirectiveChanged(ECourierMissionStage NewStage, FText Title, FText Directive);

	FHistoricalAtmosphereSettings GetSettingsForPhase(EHistoricalAtmospherePhase Phase) const;
	FHistoricalAtmosphereSettings GetSettingsForWeather(EHistoricalWeatherState Weather) const;

private:
	void ApplyAtmosphereSettings(const FHistoricalAtmosphereSettings& Settings);

	float TrainScheduleTimer = 0.0f;
	float TrainMaskDurationTimer = 0.0f;
	const float TrainInterval = 32.0f;
	const float TrainDuration = 8.0f;

	float DustStormRemainingTimer = 0.0f;

	bool bIsTransitioning = false;
	float TransitionDuration = 8.0f;
	float TransitionProgress = 0.0f;

	FHistoricalAtmosphereSettings SourceSettings;
	FHistoricalAtmosphereSettings TargetSettings;
	FHistoricalAtmosphereSettings CurrentSettings;
};
