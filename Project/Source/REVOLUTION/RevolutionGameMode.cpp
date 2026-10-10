// Copyright Epic Games, Inc. All Rights Reserved.

#include "RevolutionGameMode.h"
#include "RevolutionCharacter.h"
#include "UObject/ConstructorHelpers.h"

ARevolutionGameMode::ARevolutionGameMode()
{
	// Set default pawn class to our C++ character
	DefaultPawnClass = ARevolutionCharacter::StaticClass();
}
