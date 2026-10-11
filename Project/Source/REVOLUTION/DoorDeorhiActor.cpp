// Copyright Epic Games, Inc. All Rights Reserved.

#include "DoorDeorhiActor.h"
#include "RevolutionCharacter.h"
#include "CurfewPatrolAI.h"
#include "Components/SceneComponent.h"
#include "Components/StaticMeshComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Sound/SoundBase.h"
#include "Kismet/GameplayStatics.h"
#include "REVOLUTION.h"

ADoorDeorhiActor::ADoorDeorhiActor()
{
	PrimaryActorTick.bCanEverTick = true;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	DoorHinge = CreateDefaultSubobject<USceneComponent>(TEXT("DoorHinge"));
	DoorHinge->SetupAttachment(RootComponent);
	DoorHinge->SetRelativeLocation(FVector(0.0f, -48.0f, 0.0f));

	DoorMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("DoorMesh"));
	DoorMesh->SetupAttachment(DoorHinge);
	DoorMesh->SetRelativeLocation(FVector(0.0f, 48.0f, 0.0f));
	DoorMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));

	static ConstructorHelpers::FObjectFinder<UStaticMesh> MeshFinder(TEXT("/Game/Environment/Mohalla/Meshes/SM_Door_Deorhi_Teak_01.SM_Door_Deorhi_Teak_01"));
	if (MeshFinder.Succeeded())
	{
		DoorMesh->SetStaticMesh(MeshFinder.Object);
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> LatchSoundFinder(TEXT("/Game/Audio/SFX/SFX_Iron_Latch_Slide.SFX_Iron_Latch_Slide"));
	if (LatchSoundFinder.Succeeded())
	{
		LatchSlideSound = LatchSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> CreakSoundFinder(TEXT("/Game/Audio/SFX/SFX_Teak_Door_Creak.SFX_Teak_Door_Creak"));
	if (CreakSoundFinder.Succeeded())
	{
		DoorCreakSound = CreakSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> SlamSoundFinder(TEXT("/Game/Audio/SFX/SFX_Door_Slam_Wood.SFX_Door_Slam_Wood"));
	if (SlamSoundFinder.Succeeded())
	{
		DoorSlamSound = SlamSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> LathiSoundFinder(TEXT("/Game/Audio/SFX/SFX_Door_Banging_Lathi.SFX_Door_Banging_Lathi"));
	if (LathiSoundFinder.Succeeded())
	{
		LathiBangSound = LathiSoundFinder.Object;
	}
}

void ADoorDeorhiActor::BeginPlay()
{
	Super::BeginPlay();

	TargetYaw = bIsOpen ? MaxOpenAngle : 0.0f;
	CurrentYaw = TargetYaw;
	DoorHinge->SetRelativeRotation(FRotator(0.0f, CurrentYaw, 0.0f));
}

void ADoorDeorhiActor::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	if (bIsSwinging)
	{
		CurrentYaw = FMath::FInterpConstantTo(CurrentYaw, TargetYaw, DeltaTime, SwingSpeed);
		DoorHinge->SetRelativeRotation(FRotator(0.0f, CurrentYaw, 0.0f));

		if (FMath::IsNearlyEqual(CurrentYaw, TargetYaw, 0.5f))
		{
			CurrentYaw = TargetYaw;
			DoorHinge->SetRelativeRotation(FRotator(0.0f, CurrentYaw, 0.0f));
			bIsSwinging = false;

			if (!bIsOpen && DoorSlamSound)
			{
				UGameplayStatics::PlaySoundAtLocation(this, DoorSlamSound, GetActorLocation(), 0.95f, FMath::RandRange(0.95f, 1.05f));
			}
		}
	}
}

bool ADoorDeorhiActor::IsOnInteriorLatchSide(const FVector& Location) const
{
	FVector Dir = (Location - GetActorLocation()).GetSafeNormal2D();
	float Dot = FVector::DotProduct(GetActorForwardVector().GetSafeNormal2D(), Dir);
	return Dot >= -0.15f;
}

bool ADoorDeorhiActor::CanInteract_Implementation(const ARevolutionCharacter* Interactor) const
{
	if (!Interactor) return false;

	if (bIsOpen)
	{
		return true;
	}

	if (bIsBolted)
	{
		// Can only unbolt from the interior courtyard side where the kundi iron latch is mounted
		return IsOnInteriorLatchSide(Interactor->GetActorLocation());
	}

	// Unbolted and closed: can be opened from either side
	return true;
}

FText ADoorDeorhiActor::GetInteractionPrompt_Implementation() const
{
	if (bIsOpen)
	{
		return FText::FromString(TEXT("Slam Door Shut"));
	}

	if (bIsBolted)
	{
		return FText::FromString(TEXT("Slide Iron Bolt (Unbolt)"));
	}

	return FText::FromString(TEXT("Push Door Open"));
}

void ADoorDeorhiActor::OnInteract_Implementation(ARevolutionCharacter* Interactor)
{
	if (!Interactor) return;

	if (bIsOpen)
	{
		// Slam door shut
		SetDoorOpen(false);

		// If player is on latch side, automatically drop bolt to barricade
		if (IsOnInteriorLatchSide(Interactor->GetActorLocation()))
		{
			SetBolted(true);
		}
	}
	else if (bIsBolted)
	{
		if (IsOnInteriorLatchSide(Interactor->GetActorLocation()))
		{
			SetBolted(false);
			// Auto push open right after sliding bolt
			SetDoorOpen(true);
		}
	}
	else
	{
		// Closed and unbolted: open it
		SetDoorOpen(true);
	}
}

void ADoorDeorhiActor::SetDoorOpen(bool bOpen)
{
	if (bIsOpen == bOpen) return;

	bIsOpen = bOpen;
	TargetYaw = bIsOpen ? MaxOpenAngle : 0.0f;
	bIsSwinging = true;

	if (bIsOpen && DoorCreakSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, DoorCreakSound, GetActorLocation(), 0.95f, FMath::RandRange(0.92f, 1.04f));
	}

	UE_LOG(LogREVOLUTION, Log, TEXT("Deorhi Door state changed: %s"), bIsOpen ? TEXT("OPEN") : TEXT("CLOSED"));
}

void ADoorDeorhiActor::SetBolted(bool bBolted)
{
	if (bIsBolted == bBolted) return;

	bIsBolted = bBolted;

	if (LatchSlideSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, LatchSlideSound, GetActorLocation(), 1.0f, FMath::RandRange(0.96f, 1.04f));
	}

	UE_LOG(LogREVOLUTION, Log, TEXT("Deorhi Iron Bolt state changed: %s"), bIsBolted ? TEXT("BOLTED") : TEXT("UNBOLTED"));
}

void ADoorDeorhiActor::WatchmanBangOnDoor(ACurfewPatrolAI* Watchman)
{
	float CurrentTime = GetWorld() ? GetWorld()->GetTimeSeconds() : 0.0f;
	if (CurrentTime - LastBangTime < 3.0f)
	{
		return;
	}

	LastBangTime = CurrentTime;

	if (LathiBangSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, LathiBangSound, GetActorLocation(), 1.0f, FMath::RandRange(0.95f, 1.05f));
	}

	UE_LOG(LogREVOLUTION, Log, TEXT("Curfew Patrol Watchman banging bamboo lathi against locked Deorhi door!"));
}
