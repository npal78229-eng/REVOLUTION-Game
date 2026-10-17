// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "RevolutionCinematicDirectorActor.generated.h"

class ULevelSequence;
class ALevelSequenceActor;
class ULevelSequencePlayer;
class ACineCameraActor;
class ARevolutionHUD;
class USoundMix;

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnCinematicSequenceCompleted, FName, SequenceName);

/**
 * Historical Cinematic Cutscene Director for REVOLUTION
 * Coordinates Level Sequence playback, smooth camera blending (SetViewTargetWithBlend),
 * letterbox presentation, and subtitle captioning with ARevolutionHUD.
 */
UCLASS()
class REVOLUTION_API ARevolutionCinematicDirectorActor : public AActor
{
	GENERATED_BODY()

public:
	ARevolutionCinematicDirectorActor();

protected:
	virtual void BeginPlay() override;

public:
	/** Active Level Sequence asset being played */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Cinematic")
	ULevelSequence* ActiveSequence = nullptr;

	/** Spawned Level Sequence Actor */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Cinematic")
	ALevelSequenceActor* SequenceActor = nullptr;

	/** Active Level Sequence Player instance */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Cinematic")
	ULevelSequencePlayer* SequencePlayer = nullptr;

	/** Optional dedicated Cine Camera Actor to blend to */
	UPROPERTY(EditInstanceOnly, BlueprintReadWrite, Category = "Revolution|Cinematic")
	ACineCameraActor* CinematicCamera = nullptr;

	/** Dynamic delegate fired when cinematic playback finishes */
	UPROPERTY(BlueprintAssignable, Category = "Revolution|Cinematic")
	FOnCinematicSequenceCompleted OnCinematicCompleted;

	/** Plays a Level Sequence cutscene with smooth camera blend and HUD letterboxing */
	UFUNCTION(BlueprintCallable, Category = "Revolution|Cinematic")
	bool PlayCinematicCutscene(ULevelSequence* InSequence, FText ChapterTitle, FText Subtitle, float InBlendInTime = 1.25f);

	/** Immediately stops the active cutscene and blends back to gameplay camera */
	UFUNCTION(BlueprintCallable, Category = "Revolution|Cinematic")
	void StopCinematicCutscene(float InBlendOutTime = 1.0f);

	/** Updates the active subtitle caption during cutscene playback */
	UFUNCTION(BlueprintCallable, Category = "Revolution|Cinematic")
	void UpdateSubtitle(const FText& InSubtitle);

	/** Returns whether a cinematic sequence is currently running */
	UFUNCTION(BlueprintPure, Category = "Revolution|Cinematic")
	bool IsCinematicPlaying() const { return bIsPlaying; }

	/** Pre-configured sequences */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Cinematic")
	ULevelSequence* MunadiProclamationSequence = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Cinematic")
	ULevelSequence* GoldenSunriseFinaleSequence = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundMix* CinematicSoundMix = nullptr;

private:
	UFUNCTION()
	void HandleSequenceFinished();

	bool bIsPlaying = false;
	float ActiveBlendOutTime = 1.0f;
	TWeakObjectPtr<APawn> CachedPlayerPawn;
	TWeakObjectPtr<ARevolutionHUD> CachedHUD;
};
