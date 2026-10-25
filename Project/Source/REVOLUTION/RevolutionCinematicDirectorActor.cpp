// Copyright Epic Games, Inc. All Rights Reserved.

#include "RevolutionCinematicDirectorActor.h"
#include "LevelSequence.h"
#include "LevelSequenceActor.h"
#include "LevelSequencePlayer.h"
#include "CineCameraActor.h"
#include "RevolutionHUD.h"
#include "Kismet/GameplayStatics.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/Pawn.h"
#include "Sound/SoundMix.h"
#include "REVOLUTION.h"

ARevolutionCinematicDirectorActor::ARevolutionCinematicDirectorActor()
{
	PrimaryActorTick.bCanEverTick = false;
	SetRootComponent(CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot")));
}

void ARevolutionCinematicDirectorActor::BeginPlay()
{
	Super::BeginPlay();

	UWorld* World = GetWorld();
	if (!World) return;

	if (APlayerController* PC = UGameplayStatics::GetPlayerController(World, 0))
	{
		CachedHUD = Cast<ARevolutionHUD>(PC->GetHUD());
	}
}

bool ARevolutionCinematicDirectorActor::PlayCinematicCutscene(ULevelSequence* InSequence, FText ChapterTitle, FText Subtitle, float InBlendInTime)
{
	if (!InSequence)
	{
		UE_LOG(LogREVOLUTION, Warning, TEXT("PlayCinematicCutscene called with null InSequence!"));
		return false;
	}

	UWorld* World = GetWorld();
	if (!World) return false;

	APlayerController* PC = UGameplayStatics::GetPlayerController(World, 0);
	if (PC)
	{
		CachedPlayerPawn = PC->GetPawn();
		if (!CachedHUD.IsValid())
		{
			CachedHUD = Cast<ARevolutionHUD>(PC->GetHUD());
		}

		if (CinematicCamera)
		{
			PC->SetViewTargetWithBlend(CinematicCamera, InBlendInTime, VTBlend_EaseInOut, 2.0f);
		}
	}

	ActiveSequence = InSequence;
	bIsPlaying = true;
	ActiveBlendOutTime = 1.0f;

	// Activate HUD cinematic mode (2.39:1 letterboxing + gold chapter titles + ivory captions)
	if (CachedHUD.IsValid())
	{
		CachedHUD->SetCinematicSequenceActive(true, ChapterTitle, Subtitle);
	}

	// Push cutscene audio ducking mix
	if (CinematicSoundMix)
	{
		UGameplayStatics::PushSoundMixModifier(World, CinematicSoundMix);
	}

	// Create Level Sequence Player
	FMovieSceneSequencePlaybackSettings PlaybackSettings;
	PlaybackSettings.bAutoPlay = false;
	PlaybackSettings.bPauseAtEnd = false;
	PlaybackSettings.bDisableMovementInput = true;
	PlaybackSettings.bDisableLookAtInput = true;
	PlaybackSettings.bHideHud = false; // Custom HUD handles letterboxing and captions

	SequencePlayer = ULevelSequencePlayer::CreateLevelSequencePlayer(
		World,
		InSequence,
		PlaybackSettings,
		SequenceActor
	);

	if (SequencePlayer)
	{
		SequencePlayer->OnFinished.AddDynamic(this, &ARevolutionCinematicDirectorActor::HandleSequenceFinished);
		SequencePlayer->Play();
		UE_LOG(LogREVOLUTION, Log, TEXT("Started Level Sequence playback for '%s'."), *InSequence->GetName());
		return true;
	}

	UE_LOG(LogREVOLUTION, Error, TEXT("Failed to create LevelSequencePlayer for '%s'!"), *InSequence->GetName());
	return false;
}

void ARevolutionCinematicDirectorActor::StopCinematicCutscene(float InBlendOutTime)
{
	if (!bIsPlaying) return;
	bIsPlaying = false;

	if (SequencePlayer)
	{
		SequencePlayer->Stop();
	}

	UWorld* World = GetWorld();
	if (World)
	{
		if (APlayerController* PC = UGameplayStatics::GetPlayerController(World, 0))
		{
			if (CachedPlayerPawn.IsValid())
			{
				PC->SetViewTargetWithBlend(CachedPlayerPawn.Get(), InBlendOutTime, VTBlend_EaseInOut, 2.0f);
			}
		}
	}

	if (CachedHUD.IsValid())
	{
		CachedHUD->SetCinematicSequenceActive(false);
	}

	// Restore gameplay audio mix
	if (CinematicSoundMix && World)
	{
		UGameplayStatics::PopSoundMixModifier(World, CinematicSoundMix);
	}

	FName FinishedSeqName = ActiveSequence ? ActiveSequence->GetFName() : NAME_None;
	OnCinematicCompleted.Broadcast(FinishedSeqName);

	UE_LOG(LogREVOLUTION, Log, TEXT("Cinematic Cutscene '%s' concluded. Blending back to gameplay."), *FinishedSeqName.ToString());
}

void ARevolutionCinematicDirectorActor::UpdateSubtitle(const FText& InSubtitle)
{
	if (CachedHUD.IsValid())
	{
		CachedHUD->SetCinematicSubtitle(InSubtitle);
	}
}

void ARevolutionCinematicDirectorActor::HandleSequenceFinished()
{
	StopCinematicCutscene(ActiveBlendOutTime);
}

bool ARevolutionCinematicDirectorActor::PlayBaisakhiDawnEpilogue()
{
	ULevelSequence* TargetSeq = GoldenSunriseFinaleSequence;
	if (!TargetSeq)
	{
		TargetSeq = Cast<ULevelSequence>(StaticLoadObject(ULevelSequence::StaticClass(), nullptr, TEXT("/Game/Cinematics/LS_Golden_Sunrise_Finale")));
	}

	FText EpilogueTitle = FText::FromString(TEXT("THE BAISAKHI DAWN"));
	FText EpilogueSubtitle = FText::FromString(TEXT("Kot Gurdarshan, April 14, 1919 — As golden morning light crests the terracotta rooftops, Punjab awakens with an unyielding moral resolve."));

	return PlayCinematicCutscene(TargetSeq, EpilogueTitle, EpilogueSubtitle, 1.5f);
}

bool ARevolutionCinematicDirectorActor::PlayMunadiProclamationCutscene()
{
	ULevelSequence* TargetSeq = MunadiProclamationSequence;
	if (!TargetSeq)
	{
		TargetSeq = Cast<ULevelSequence>(StaticLoadObject(ULevelSequence::StaticClass(), nullptr, TEXT("/Game/Cinematics/LS_Munadi_Proclamation")));
	}

	FText ChapterTitle = FText::FromString(TEXT("ACT II: THE GATHERING STORM"));
	FText Subtitle = FText::FromString(TEXT("Amritsar, April 13, 1919 — Afternoon nagara drums echo across Kot Gurdarshan as British town criers beat the Munadi, announcing General Dyer's proclamation banning all assemblies."));

	return PlayCinematicCutscene(TargetSeq, ChapterTitle, Subtitle, 1.25f);
}

