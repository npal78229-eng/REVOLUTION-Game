// Copyright Epic Games, Inc. All Rights Reserved.

#include "RevolutionBazaarWallaActor.h"
#include "Components/SphereComponent.h"
#include "Components/AudioComponent.h"
#include "Kismet/GameplayStatics.h"

ARevolutionBazaarWallaActor::ARevolutionBazaarWallaActor()
{
	PrimaryActorTick.bCanEverTick = true;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	AudibilitySphere = CreateDefaultSubobject<USphereComponent>(TEXT("AudibilitySphere"));
	AudibilitySphere->SetupAttachment(RootComponent);
	AudibilitySphere->SetSphereRadius(1800.0f);
	AudibilitySphere->SetCollisionResponseToAllChannels(ECR_Ignore);
	AudibilitySphere->SetCollisionResponseToChannel(ECC_Pawn, ECR_Overlap);

	WallaAudioComponent = CreateDefaultSubobject<UAudioComponent>(TEXT("WallaAudioComponent"));
	WallaAudioComponent->SetupAttachment(RootComponent);
	WallaAudioComponent->bAutoActivate = false;

	VendorTitle = FText::FromString(TEXT("Bazaar Hawker"));
	PunjabiPhrase = FText::FromString(TEXT("Taaza saag te gobi lai lo ji!"));
	EnglishTranslation = FText::FromString(TEXT("Buy fresh greens and cauliflower! Fresh from the Majha soil!"));
}

void ARevolutionBazaarWallaActor::BeginPlay()
{
	Super::BeginPlay();

	// Initialize random timer offset so multiple vendors do not shout simultaneously
	NextCallTimer = FMath::RandRange(2.0f, MinCallInterval);
}

void ARevolutionBazaarWallaActor::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	if (bIsSilencedByCurfew)
	{
		if (WallaAudioComponent && WallaAudioComponent->IsPlaying())
		{
			WallaAudioComponent->Stop();
		}
		return;
	}

	NextCallTimer -= DeltaTime;
	if (NextCallTimer <= 0.0f)
	{
		PlayWallaCall();
		NextCallTimer = FMath::RandRange(MinCallInterval, MaxCallInterval);
	}
}

void ARevolutionBazaarWallaActor::PlayWallaCall()
{
	if (bIsSilencedByCurfew || !PrimaryWallaSound)
	{
		return;
	}

	if (WallaAudioComponent)
	{
		WallaAudioComponent->SetSound(PrimaryWallaSound);
		if (VoiceAttenuation)
		{
			WallaAudioComponent->AttenuationSettings = VoiceAttenuation;
		}
		// Apply subtle random pitch modulation (+/- 3%) for natural human speech variance
		float PitchMultiplier = FMath::RandRange(0.97f, 1.03f);
		WallaAudioComponent->SetPitchMultiplier(PitchMultiplier);
		WallaAudioComponent->Play();
	}
}

void ARevolutionBazaarWallaActor::SetCurfewSilenced(bool bSilenced)
{
	bIsSilencedByCurfew = bSilenced;
	if (bIsSilencedByCurfew && WallaAudioComponent && WallaAudioComponent->IsPlaying())
	{
		WallaAudioComponent->Stop();
	}
}
