// Copyright Epic Games, Inc. All Rights Reserved.

#include "RevolutionSaveGame.h"

URevolutionSaveGame::URevolutionSaveGame()
{
	SaveSlotName = TEXT("RevolutionSave_Slot0");
	UserIndex = 0;
	SaveTimestamp = FDateTime::Now();

	CurrentMissionStage = ECourierMissionStage::Stage_Morning_FatherTailor;

	PlayerLocation = FVector(10.0f, 20.0f, 15.0f);
	PlayerRotation = FRotator::ZeroRotator;
	CurrentStamina = 100.0f;

	CheckpointLocation = FVector(10.0f, 20.0f, 15.0f);
	CheckpointRotation = FRotator::ZeroRotator;

	PamphletCount = 0;
	PebbleCount = 5;
	ChalkCount = 8;
	SelectedCodexIndex = 0;

	MasterVolume = 1.0f;
	SFXVolume = 1.0f;
	FoleyVolume = 1.0f;
	VoiceVolume = 1.0f;
	AmbienceVolume = 1.0f;
	SubtitleScaleMultiplier = 1.0f;
	bHandheldSteamOSMode = false;
}
