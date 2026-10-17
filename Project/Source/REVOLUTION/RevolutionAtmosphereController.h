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
};

/**
 * Historical Dynamic Lighting & Atmosphere Controller for REVOLUTION
 * Dynamically controls the 5 historical atmosphere phases across Act I through Act V:
 * 1. Morning Dawn (3200K warm sunrise, Act I)
 * 2. Baisakhi Festival Midday (5200K high spring sun, Act II)
 * 3. Curfew Martial Law Night (8500K moonlight, dense fog, lantern contrast, Act III)
 * 4. Canal Distributary Night (6500K pale river moonlight & ground mist, Act IV)
 * 5. Golden Sunrise Finale (2850K golden dawn triumph break, Act V)
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

	UFUNCTION(BlueprintPure, Category = "Revolution|Atmosphere")
	EHistoricalAtmospherePhase GetCurrentPhase() const { return CurrentPhase; }

	UFUNCTION(BlueprintCallable, Category = "Revolution|Atmosphere")
	void SetAtmospherePhase(EHistoricalAtmospherePhase NewPhase, float InTransitionDuration = 8.0f);

	UFUNCTION()
	void HandleMissionDirectiveChanged(ECourierMissionStage NewStage, FText Title, FText Directive);

	FHistoricalAtmosphereSettings GetSettingsForPhase(EHistoricalAtmospherePhase Phase) const;

private:
	void ApplyAtmosphereSettings(const FHistoricalAtmosphereSettings& Settings);

	float TrainScheduleTimer = 0.0f;
	float TrainMaskDurationTimer = 0.0f;
	const float TrainInterval = 32.0f;
	const float TrainDuration = 8.0f;

	bool bIsTransitioning = false;
	float TransitionDuration = 8.0f;
	float TransitionProgress = 0.0f;

	FHistoricalAtmosphereSettings SourceSettings;
	FHistoricalAtmosphereSettings TargetSettings;
	FHistoricalAtmosphereSettings CurrentSettings;
};
