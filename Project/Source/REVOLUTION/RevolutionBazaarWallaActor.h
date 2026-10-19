// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "RevolutionBazaarWallaActor.generated.h"

class USphereComponent;
class UAudioComponent;
class USoundBase;
class USoundAttenuation;

UENUM(BlueprintType)
enum class EPunjabiDialect : uint8
{
	Majhi UMETA(DisplayName = "Majhi (Amritsar / Lahore Urban Vernacular)"),
	Doabi UMETA(DisplayName = "Doabi (Jalandhar / Hoshiarpur Agrarian Vernacular)")
};

/**
 * Historical Punjabi Bazaar Crowd Walla Actor (Task 26)
 * Generates organic, period-accurate vendor calls and crowd walla across Majhi and Doabi dialects.
 * Features:
 * - Asynchronous organic periodic vocal intervals
 * - Spatialized with ATT_Voice_Proximity and routed to SC_Voice_Punjabi
 * - Curfew silencing integration (silenced during CurfewNight martial law)
 * - Proximity inspection prompt showcasing English translation & cultural context
 */
UCLASS()
class REVOLUTION_API ARevolutionBazaarWallaActor : public AActor
{
	GENERATED_BODY()

public:
	ARevolutionBazaarWallaActor();

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

public:
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* SceneRoot;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USphereComponent* AudibilitySphere;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UAudioComponent* WallaAudioComponent;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Walla")
	EPunjabiDialect Dialect = EPunjabiDialect::Majhi;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Walla")
	FText VendorTitle;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Walla")
	FText PunjabiPhrase;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Walla", meta = (MultiLine = true))
	FText EnglishTranslation;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* PrimaryWallaSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundAttenuation* VoiceAttenuation = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Walla")
	float MinCallInterval = 12.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Walla")
	float MaxCallInterval = 25.0f;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Walla")
	float NextCallTimer = 0.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Walla")
	bool bIsSilencedByCurfew = false;

	UFUNCTION(BlueprintCallable, Category = "Revolution|Walla")
	void PlayWallaCall();

	UFUNCTION(BlueprintCallable, Category = "Revolution|Walla")
	void SetCurfewSilenced(bool bSilenced);

	UFUNCTION(BlueprintPure, Category = "Revolution|Walla")
	bool IsCurfewSilenced() const { return bIsSilencedByCurfew; }
};
