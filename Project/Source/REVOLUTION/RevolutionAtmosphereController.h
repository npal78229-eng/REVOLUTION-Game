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

/**
 * Historical Dynamic Lighting & Atmosphere Controller for REVOLUTION
 * Controls the transition from Midnight Martial Curfew (8500K moonlight, dense fog, lantern contrast)
 * to 1919 Dawn (2850K warm golden sunrise, morning temple/gurdwara bell chimes, ambient daylight).
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

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* DawnTempleBellSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Atmosphere")
	float TransitionDuration = 5.0f;

	UFUNCTION()
	void HandleMissionDirectiveChanged(ECourierMissionStage NewStage, FText Title, FText Directive);

private:
	bool bIsTransitioningToDawn = false;
	float TransitionProgress = 0.0f;

	FRotator NightRotation;
	FRotator DawnRotation;

	float NightSunIntensity = 2.5f;
	float DawnSunIntensity = 16.0f;

	FLinearColor NightSunColor = FLinearColor(0.60f, 0.72f, 0.95f, 1.0f);
	FLinearColor DawnSunColor = FLinearColor(1.0f, 0.76f, 0.52f, 1.0f);

	float NightSkyLightIntensity = 0.25f;
	float DawnSkyLightIntensity = 1.05f;
};
