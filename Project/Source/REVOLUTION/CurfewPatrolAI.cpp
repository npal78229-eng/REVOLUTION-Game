// Copyright Epic Games, Inc. All Rights Reserved.

#include "CurfewPatrolAI.h"
#include "RevolutionCharacter.h"
#include "Components/CapsuleComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/PointLightComponent.h"
#include "Components/SpotLightComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Engine/World.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/SoundBase.h"
#include "Sound/SoundAttenuation.h"
#include "RevolutionAtmosphereController.h"
#include "RevolutionGameMode.h"
#include "DoorDeorhiActor.h"
#include "ChalkMarkActor.h"
#include "ProclamationBoardActor.h"
#include "ChaffDustDecoyActor.h"
#include "CommunityTrustSubsystem.h"
#include "EngineUtils.h"
#include "REVOLUTION.h"

ACurfewPatrolAI::ACurfewPatrolAI()
{
	PrimaryActorTick.bCanEverTick = true;

	// Capsule dimensions for adult watchman (approx 1.80m tall)
	GetCapsuleComponent()->InitCapsuleSize(34.0f, 88.0f);

	bUseControllerRotationPitch = false;
	bUseControllerRotationYaw = false;
	bUseControllerRotationRoll = false;

	GetCharacterMovement()->bOrientRotationToMovement = true;
	GetCharacterMovement()->RotationRate = FRotator(0.0f, 360.0f, 0.0f);
	GetCharacterMovement()->MaxWalkSpeed = PatrolWalkSpeed;

	// Skeletal mesh setup (Adult Mannequin)
	static ConstructorHelpers::FObjectFinder<USkeletalMesh> MeshFinder(TEXT("/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple.SKM_Manny_Simple"));
	if (MeshFinder.Succeeded())
	{
		GetMesh()->SetSkeletalMesh(MeshFinder.Object);
		GetMesh()->SetRelativeLocation(FVector(0.f, 0.f, -88.f));
		GetMesh()->SetRelativeRotation(FRotator(0.f, -90.f, 0.f));
		GetMesh()->SetRelativeScale3D(FVector(1.0f, 1.0f, 1.0f));
	}

	static ConstructorHelpers::FClassFinder<UAnimInstance> AnimFinder(TEXT("/Game/Characters/Mannequins/Animations/ABP_Manny.ABP_Manny_C"));
	if (AnimFinder.Succeeded())
	{
		GetMesh()->SetAnimInstanceClass(AnimFinder.Class);
	}

	// Hurricane Lantern Static Mesh held by watchman
	LanternMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("LanternMesh"));
	LanternMesh->SetupAttachment(RootComponent);
	LanternMesh->SetRelativeLocation(FVector(30.0f, 25.0f, -5.0f));
	LanternMesh->SetCollisionProfileName(TEXT("NoCollision"));

	static ConstructorHelpers::FObjectFinder<UStaticMesh> LanternMeshFinder(TEXT("/Game/Environment/Mohalla/Meshes/SM_Prop_HurricaneLantern.SM_Prop_HurricaneLantern"));
	if (LanternMeshFinder.Succeeded())
	{
		LanternMesh->SetStaticMesh(LanternMeshFinder.Object);
		LanternMesh->SetRelativeScale3D(FVector(0.75f, 0.75f, 0.75f));
	}

	// 3200K Kerosene Ambient Glow
	LanternLight = CreateDefaultSubobject<UPointLightComponent>(TEXT("LanternLight"));
	LanternLight->SetupAttachment(LanternMesh);
	LanternLight->SetRelativeLocation(FVector(0.0f, 0.0f, 18.0f));
	LanternLight->SetLightColor(FLinearColor(1.0f, 0.78f, 0.40f, 1.0f));
	LanternLight->SetIntensity(1400.0f);
	LanternLight->SetAttenuationRadius(650.0f);
	LanternLight->SetCastShadows(true);

	// Focused Forward Lantern Beam
	LanternBeam = CreateDefaultSubobject<USpotLightComponent>(TEXT("LanternBeam"));
	LanternBeam->SetupAttachment(LanternMesh);
	LanternBeam->SetRelativeLocation(FVector(0.0f, 0.0f, 18.0f));
	LanternBeam->SetRelativeRotation(FRotator(-12.0f, 0.0f, 0.0f));
	LanternBeam->SetLightColor(FLinearColor(1.0f, 0.85f, 0.50f, 1.0f));
	LanternBeam->SetIntensity(3200.0f);
	LanternBeam->SetAttenuationRadius(1100.0f);
	LanternBeam->SetInnerConeAngle(22.0f);
	LanternBeam->SetOuterConeAngle(46.0f);
	LanternBeam->SetCastShadows(true);

	WatchmanTitle = FText::FromString(TEXT("Kot Gurdarshan Chaukidar (Night Watchman)"));

	static ConstructorHelpers::FObjectFinder<USoundBase> CalloutSoundFinder(TEXT("/Game/Audio/SFX/SFX_Watchman_Callout.SFX_Watchman_Callout"));
	if (CalloutSoundFinder.Succeeded())
	{
		WatchmanCalloutSound = CalloutSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> WhistleSoundFinder(TEXT("/Game/Audio/SFX/SFX_Watchman_Whistle.SFX_Watchman_Whistle"));
	if (WhistleSoundFinder.Succeeded())
	{
		WatchmanWhistleSound = WhistleSoundFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> CurfewVoiceFinder(TEXT("/Game/Audio/Voice/SFX_Voice_ConstableGurdial_Curfew.SFX_Voice_ConstableGurdial_Curfew"));
	if (CurfewVoiceFinder.Succeeded())
	{
		CurfewVoiceProclamationSound = CurfewVoiceFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<USoundBase> SuspicionVoiceFinder(TEXT("/Game/Audio/Voice/SFX_Voice_ConstableGurdial_Suspicion.SFX_Voice_ConstableGurdial_Suspicion"));
	if (SuspicionVoiceFinder.Succeeded())
	{
		SuspiciousVoiceSound = SuspicionVoiceFinder.Object;
	}
}

void ACurfewPatrolAI::BeginPlay()
{
	Super::BeginPlay();

	// Enforce upright yaw-only rotation for character capsule
	const FRotator CurrentRot = GetActorRotation();
	if (FMath::Abs(CurrentRot.Pitch) > 0.01f || FMath::Abs(CurrentRot.Roll) > 0.01f)
	{
		SetActorRotation(FRotator(0.0f, CurrentRot.Yaw, 0.0f));
	}

	if (!VoiceAttenuation)
	{
		VoiceAttenuation = LoadObject<USoundAttenuation>(nullptr, TEXT("/Game/Audio/Attenuation/ATT_Voice_Proximity.ATT_Voice_Proximity"));
	}

	if (PatrolWaypoints.IsEmpty())
	{
		PatrolWaypoints.Add(GetActorLocation());
	}
	LastKnownPlayerLocation = GetActorLocation();
}

void ACurfewPatrolAI::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	ARevolutionGameMode* GM = Cast<ARevolutionGameMode>(UGameplayStatics::GetGameMode(this));
	if (GM && GM->IsPlayerApprehended())
	{
		GetCharacterMovement()->StopMovementImmediately();
		return;
	}

	// Update nocturnal wind turbulence flicker on kerosene lantern
	LanternFlickerCycleTimer += DeltaTime;
	if (!bIsLanternFlickering)
	{
		if (LanternFlickerCycleTimer >= LanternFlickerInterval)
		{
			bIsLanternFlickering = true;
			LanternFlickerTimer = 0.0f;
			LanternFlickerCycleTimer = 0.0f;
		}
	}
	else
	{
		LanternFlickerTimer += DeltaTime;
		float FlickerOscillation = 0.38f + 0.22f * FMath::Sin(LanternFlickerTimer * 14.0f);
		if (LanternLight)
		{
			LanternLight->SetIntensity(1400.0f * FlickerOscillation);
		}
		if (LanternBeam)
		{
			LanternBeam->SetIntensity(3200.0f * FlickerOscillation);
		}

		if (LanternFlickerTimer >= LanternFlickerDuration)
		{
			bIsLanternFlickering = false;
			LanternFlickerTimer = 0.0f;
			if (LanternLight)
			{
				LanternLight->SetIntensity(1400.0f);
			}
			if (LanternBeam)
			{
				LanternBeam->SetIntensity(3200.0f);
			}
		}
	}

	UpdateDetection(DeltaTime);
	UpdatePatrol(DeltaTime);
}

bool ACurfewPatrolAI::CanSeePlayer(ARevolutionCharacter* TargetPlayer, float& OutPerceptionIntensity)
{
	OutPerceptionIntensity = 0.0f;
	if (!TargetPlayer || !GetWorld()) return false;

	// If player is concealed inside a hiding spot or low drain conduit, watchman perception is completely broken
	if (TargetPlayer->IsHidingInCover() || TargetPlayer->IsCrawlTraversing())
	{
		return false;
	}

	const FVector WatchmanEye = GetActorLocation() + FVector(0.0f, 0.0f, 70.0f);
	const FVector PlayerBase = TargetPlayer->GetActorLocation();
	const FVector PlayerHead = PlayerBase + FVector(0.0f, 0.0f, TargetPlayer->bIsCrouched ? 35.0f : 68.0f);
	const FVector PlayerChest = PlayerBase + FVector(0.0f, 0.0f, TargetPlayer->bIsCrouched ? 20.0f : 45.0f);

	const float Distance = FVector::Dist(WatchmanEye, PlayerBase);
	const float EffectiveSightRadius = bIsLanternFlickering ? (SightRadius * 0.58f) : SightRadius;
	if (Distance > EffectiveSightRadius)
	{
		return false;
	}

	const FVector DirToPlayer = (PlayerBase - WatchmanEye).GetSafeNormal();
	const FVector Forward = GetActorForwardVector();
	const float DotProduct = FVector::DotProduct(Forward, DirToPlayer);
	const float MinDot = FMath::Cos(FMath::DegreesToRadians(PeripheralVisionAngle));

	// If outside vision cone, check if within hearing radius while player is sprinting
	bool bAudibleHearing = false;
	if (DotProduct < MinDot)
	{
		// Check for sound masking from environmental controller (steam train passing)
		bool bSoundMasked = false;
		for (TActorIterator<ARevolutionAtmosphereController> It(GetWorld()); It; ++It)
		{
			if (It->IsSoundMasked() || It->IsWeatherSoundMasked())
			{
				bSoundMasked = true;
				break;
			}
		}

		float EffectiveHearingRadius = bSoundMasked ? (HearingRadius * 0.22f) : HearingRadius;

		if (Distance <= EffectiveHearingRadius && TargetPlayer->bIsSprinting && TargetPlayer->GetVelocity().SizeSquared() > 100.0f)
		{
			bAudibleHearing = true;
		}
		else
		{
			return false;
		}
	}

	// Line-of-sight raycasts
	FCollisionQueryParams TraceParams;
	TraceParams.AddIgnoredActor(this);
	TraceParams.AddIgnoredActor(TargetPlayer);

	FHitResult HitHead;
	bool bHeadBlocked = GetWorld()->LineTraceSingleByChannel(HitHead, WatchmanEye, PlayerHead, ECC_Visibility, TraceParams);

	FHitResult HitChest;
	bool bChestBlocked = GetWorld()->LineTraceSingleByChannel(HitChest, WatchmanEye, PlayerChest, ECC_Visibility, TraceParams);

	// If both head and chest are blocked by obstacles (e.g. 1.1m parapet wall or brick doorway), LOS is completely broken!
	if (bHeadBlocked && bChestBlocked)
	{
		return false;
	}

	// Check if active wheat chaff particulate dust screen blocks sightlines
	for (TActorIterator<AChaffDustDecoyActor> ChaffIt(GetWorld()); ChaffIt; ++ChaffIt)
	{
		AChaffDustDecoyActor* Chaff = *ChaffIt;
		if (Chaff && Chaff->IsDustCloudActive())
		{
			float DistWatchman = FVector::Dist(GetActorLocation(), Chaff->GetActorLocation());
			float DistPlayer = FVector::Dist(TargetPlayer->GetActorLocation(), Chaff->GetActorLocation());
			if (DistWatchman <= Chaff->DustRadius || DistPlayer <= Chaff->DustRadius)
			{
				return false;
			}
		}
	}

	// Check if Kabir is cloaked in dense locomotive boiler steam (Hitman / Batman Arkham benchmark)
	if (TargetPlayer->IsSteamObscured())
	{
		return false;
	}

	// Calculate base intensity based on distance falloff
	float DistanceFactor = 1.0f - FMath::Clamp(Distance / EffectiveSightRadius, 0.0f, 1.0f);

	// Stance concealment multiplier
	float StanceMultiplier = 1.0f;
	if (TargetPlayer->IsCrowdBlended())
	{
		// Social stealth: blending into civilian groups reduces visual detection profile by 80%
		StanceMultiplier = 0.20f;
	}
	else if (TargetPlayer->bIsCrouched)
	{
		// Crouched behind cover or in alley shadows reduces visibility profile dramatically
		StanceMultiplier = 0.28f;
	}
	else if (TargetPlayer->bIsSprinting)
	{
		// Sprinting movement draws immediate attention
		StanceMultiplier = 1.55f;
	}
	else
	{
		StanceMultiplier = 0.75f;
	}

	// Carrying contraband anti-Rowlatt strike handbills makes the courier profile more conspicuous to British colonial constables
	if (TargetPlayer->GetPamphletCount() > 0)
	{
		StanceMultiplier *= 1.30f;
	}

	// Corner peeking (Dishonored / The Last of Us): only subtle head silhouette exposed around corners
	if (TargetPlayer->IsCornerLeaning())
	{
		StanceMultiplier *= 0.35f;
	}

	// Shadow concealment rating (Thief / Splinter Cell benchmark)
	// In deep shadow (high concealment), sentry perception fill rate is dampened up to 75%
	float ShadowDampening = FMath::Clamp(1.0f - (0.75f * TargetPlayer->GetConcealmentScore()), 0.25f, 1.0f);
	StanceMultiplier *= ShadowDampening;

	// Task 27: Dynamic Weather Dampening (Andhi Dust Storm reduces visibility by 35%)
	for (TActorIterator<ARevolutionAtmosphereController> AtmoIt(GetWorld()); AtmoIt; ++AtmoIt)
	{
		StanceMultiplier *= AtmoIt->GetWeatherVisibilityMultiplier();
		break;
	}

	if (bAudibleHearing)
	{
		OutPerceptionIntensity = 0.35f * StanceMultiplier;
		return true;
	}

	// Partial concealment (e.g. head visible over parapet while standing)
	float CoverageFactor = (bChestBlocked || bHeadBlocked) ? 0.45f : 1.0f;

	// Wind flicker turbulence reduces visual discernment intensity
	float FlickerMultiplier = bIsLanternFlickering ? 0.65f : 1.0f;

	OutPerceptionIntensity = DistanceFactor * StanceMultiplier * CoverageFactor * FlickerMultiplier;
	return OutPerceptionIntensity > 0.05f;
}

void ACurfewPatrolAI::UpdateDetection(float DeltaTime)
{
	ARevolutionCharacter* Player = Cast<ARevolutionCharacter>(UGameplayStatics::GetPlayerCharacter(this, 0));
	if (!Player) return;

	float PerceptionIntensity = 0.0f;
	bool bCanSee = CanSeePlayer(Player, PerceptionIntensity);

	if (bCanSee)
	{
		LastKnownPlayerLocation = Player->GetActorLocation();

		// Accumulate detection
		DetectionMeter = FMath::Clamp(DetectionMeter + (DetectionFillRate * PerceptionIntensity * DeltaTime), 0.0f, 100.0f);

		if (DetectionMeter >= 100.0f)
		{
			SetAlertState(ECurfewAlertState::Alerted);
		}
		else if (DetectionMeter >= 35.0f && AlertState == ECurfewAlertState::Unaware)
		{
			SetAlertState(ECurfewAlertState::Suspicious);
		}
	}
	else
	{
		// Decay detection when line of sight is broken
		DetectionMeter = FMath::Clamp(DetectionMeter - (SuspicionDecayRate * DeltaTime), 0.0f, 100.0f);

		if (AlertState == ECurfewAlertState::Alerted)
		{
			SearchTimer += DeltaTime;
			if (SearchTimer >= 4.0f)
			{
				SetAlertState(ECurfewAlertState::Searching);
				SearchTimer = 0.0f;
			}
		}
		else if (AlertState == ECurfewAlertState::Searching)
		{
			SearchTimer += DeltaTime;
			if (SearchTimer >= 6.0f)
			{
				SetAlertState(ECurfewAlertState::Unaware);
				SearchTimer = 0.0f;
			}
		}
		else if (AlertState == ECurfewAlertState::Suspicious && DetectionMeter <= 5.0f)
		{
			SetAlertState(ECurfewAlertState::Unaware);
		}
	}
}

void ACurfewPatrolAI::UpdatePatrol(float DeltaTime)
{
	FVector Destination = GetActorLocation();

	if (AlertState == ECurfewAlertState::Alerted || AlertState == ECurfewAlertState::Searching)
	{
		// Check if a closed and bolted haveli door is blocking the path in front of watchman
		for (TActorIterator<ADoorDeorhiActor> DoorIt(GetWorld()); DoorIt; ++DoorIt)
		{
			ADoorDeorhiActor* Door = *DoorIt;
			if (Door && !Door->IsDoorOpen() && Door->IsDoorBolted())
			{
				float DistToDoor = FVector::Dist2D(GetActorLocation(), Door->GetActorLocation());
				if (DistToDoor < 155.0f)
				{
					// Watchman is blocked by the bolted door!
					Door->WatchmanBangOnDoor(this);

					// Face the locked door
					FVector DirToDoor = (Door->GetActorLocation() - GetActorLocation()).GetSafeNormal2D();
					if (!DirToDoor.IsNearlyZero())
					{
						SetActorRotation(FMath::RInterpTo(GetActorRotation(), DirToDoor.Rotation(), DeltaTime, 8.0f));
					}

					// Drop alert to searching, reset detection meter, delay pursuit
					DetectionMeter = 25.0f;
					SetAlertState(ECurfewAlertState::Searching);
					SearchTimer = 0.0f;
					GetCharacterMovement()->StopMovementImmediately();
					return;
				}
			}
		}
	}

	if (AlertState == ECurfewAlertState::Alerted)
	{
		// Pursue player or last known location
		ARevolutionCharacter* Player = Cast<ARevolutionCharacter>(UGameplayStatics::GetPlayerCharacter(this, 0));
		Destination = Player ? Player->GetActorLocation() : LastKnownPlayerLocation;
		GetCharacterMovement()->MaxWalkSpeed = AlertChaseSpeed;
		bIsWaitingAtWaypoint = false;

		// Check proximity apprehension (cornered Kabir within 125cm)
		if (Player && !Player->IsHidingInCover() && !Player->IsCrawlTraversing())
		{
			float DistToPlayer = FVector::Dist(GetActorLocation(), Player->GetActorLocation());
			if (DistToPlayer <= 125.0f)
			{
				ARevolutionGameMode* GM = Cast<ARevolutionGameMode>(UGameplayStatics::GetGameMode(this));
				if (GM && !GM->IsPlayerApprehended())
				{
					GM->HandlePlayerApprehended(this, Player);
					return;
				}
			}
		}
	}
	else if (AlertState == ECurfewAlertState::Searching)
	{
		// Cautiously inspect last known location
		Destination = LastKnownPlayerLocation;
		GetCharacterMovement()->MaxWalkSpeed = PatrolWalkSpeed * 1.25f;
		bIsWaitingAtWaypoint = false;
	}
	else if (AlertState == ECurfewAlertState::Suspicious)
	{
		// Pause movement and face sensed disturbance
		GetCharacterMovement()->MaxWalkSpeed = 0.0f;
		FVector SensedDir = (LastKnownPlayerLocation - GetActorLocation()).GetSafeNormal2D();
		if (!SensedDir.IsNearlyZero())
		{
			SetActorRotation(FMath::RInterpTo(GetActorRotation(), SensedDir.Rotation(), DeltaTime, 4.0f));
		}
		return;
	}
	else // ECurfewAlertState::Unaware
	{
		GetCharacterMovement()->MaxWalkSpeed = PatrolWalkSpeed;

		// Check if an uninvestigated tailor's chalk mark is nearby to investigate
		for (TActorIterator<AChalkMarkActor> ChalkIt(GetWorld()); ChalkIt; ++ChalkIt)
		{
			AChalkMarkActor* Mark = *ChalkIt;
			if (Mark && !Mark->bHasBeenInvestigatedByWatchman)
			{
				float DistToMark = FVector::Dist(GetActorLocation(), Mark->GetActorLocation());
				if (DistToMark <= Mark->InvestigationRadius)
				{
					FHitResult HitLOS;
					FCollisionQueryParams TraceParams;
					TraceParams.AddIgnoredActor(this);
					TraceParams.AddIgnoredActor(Mark);
					bool bBlocked = GetWorld()->LineTraceSingleByChannel(HitLOS, GetActorLocation() + FVector(0.0f, 0.0f, 60.0f), Mark->GetActorLocation(), ECC_Visibility, TraceParams);
					if (!bBlocked)
					{
						Mark->bHasBeenInvestigatedByWatchman = true;
						LastKnownPlayerLocation = Mark->GetActorLocation();
						DetectionMeter = FMath::Max(DetectionMeter, 28.0f);
						SetAlertState(ECurfewAlertState::Suspicious);
						bIsWaitingAtWaypoint = true;
						WaypointWaitTimer = 0.0f;
						GetCharacterMovement()->StopMovementImmediately();

						if (WatchmanCalloutSound)
						{
							UGameplayStatics::PlaySoundAtLocation(this, WatchmanCalloutSound, GetActorLocation(), 0.95f);
						}

						UE_LOG(LogREVOLUTION, Log, TEXT("Watchman noticed subversive tailor's chalk mark at %s! Pausing patrol to investigate."), *Mark->GetActorLocation().ToString());
						return;
					}
				}
			}
		}

		// Check if a defaced Section 144 proclamation board is nearby
		for (TActorIterator<AProclamationBoardActor> BoardIt(GetWorld()); BoardIt; ++BoardIt)
		{
			AProclamationBoardActor* Board = *BoardIt;
			if (Board && Board->bIsDefaced && !Board->bHasBeenInvestigatedByWatchman)
			{
				float DistToBoard = FVector::Dist(GetActorLocation(), Board->GetActorLocation());
				if (DistToBoard <= 260.0f)
				{
					Board->bHasBeenInvestigatedByWatchman = true;
					LastKnownPlayerLocation = Board->GetActorLocation();
					DetectionMeter = FMath::Max(DetectionMeter, 35.0f);
					SetAlertState(ECurfewAlertState::Suspicious);
					bIsWaitingAtWaypoint = true;
					WaypointWaitTimer = 0.0f;
					GetCharacterMovement()->StopMovementImmediately();

					if (WatchmanCalloutSound)
					{
						UGameplayStatics::PlaySoundAtLocation(this, WatchmanCalloutSound, GetActorLocation(), 1.0f);
					}

					UE_LOG(LogREVOLUTION, Warning, TEXT("Watchman discovered defaced imperial proclamation board at %s! Pausing patrol in outrage."), *Board->GetActorLocation().ToString());
					return;
				}
			}
		}

		if (PatrolWaypoints.IsEmpty()) return;

		Destination = PatrolWaypoints[CurrentWaypointIndex];

		FVector ToWaypoint = Destination - GetActorLocation();
		ToWaypoint.Z = 0.0f;
		float DistToWaypoint = ToWaypoint.Size();

		if (DistToWaypoint <= WaypointAcceptanceRadius)
		{
			bIsWaitingAtWaypoint = true;
		}

		if (bIsWaitingAtWaypoint)
		{
			WaypointWaitTimer += DeltaTime;
			ScanLookTimer += DeltaTime;

			// Smooth ambient head/lantern scan left and right while pausing at corners
			float SweepAngle = FMath::Sin(ScanLookTimer * 1.5f) * 35.0f;
			FRotator CurrentBaseRot = PatrolWaypoints[CurrentWaypointIndex].Rotation();
			FRotator ScanRot = FRotator(0.0f, GetActorRotation().Yaw + (FMath::Sin(DeltaTime * 2.0f) * 10.0f), 0.0f);

			if (WaypointWaitTimer >= WaypointWaitDuration)
			{
				bIsWaitingAtWaypoint = false;
				WaypointWaitTimer = 0.0f;
				CurrentWaypointIndex = (CurrentWaypointIndex + 1) % PatrolWaypoints.Num();
			}
			return;
		}
	}

	// Move toward target destination
	FVector MoveDir = (Destination - GetActorLocation()).GetSafeNormal2D();
	if (!MoveDir.IsNearlyZero())
	{
		AddMovementInput(MoveDir, 1.0f);
		FRotator TargetRot = MoveDir.Rotation();
		SetActorRotation(FMath::RInterpTo(GetActorRotation(), TargetRot, DeltaTime, 5.0f));
	}
}

void ACurfewPatrolAI::SetAlertState(ECurfewAlertState NewState)
{
	if (AlertState != NewState)
	{
		AlertState = NewState;
		OnWatchmanAlertChanged.Broadcast(AlertState, DetectionMeter);

		if (AlertState == ECurfewAlertState::Suspicious)
		{
			if (SuspiciousVoiceSound)
			{
				UGameplayStatics::PlaySoundAtLocation(this, SuspiciousVoiceSound, GetActorLocation(), 1.0f, 1.0f, 0.0f, VoiceAttenuation);
			}
			else if (WatchmanCalloutSound)
			{
				UGameplayStatics::PlaySoundAtLocation(this, WatchmanCalloutSound, GetActorLocation(), 1.0f);
			}
		}
		else if (AlertState == ECurfewAlertState::Alerted)
		{
			if (CurfewVoiceProclamationSound)
			{
				UGameplayStatics::PlaySoundAtLocation(this, CurfewVoiceProclamationSound, GetActorLocation(), 1.15f, 1.0f, 0.0f, VoiceAttenuation);
			}
			if (WatchmanWhistleSound)
			{
				UGameplayStatics::PlaySoundAtLocation(this, WatchmanWhistleSound, GetActorLocation(), 1.15f);
			}

			if (UWorld* World = GetWorld())
			{
				if (UCommunityTrustSubsystem* TrustSubsystem = World->GetSubsystem<UCommunityTrustSubsystem>())
				{
					FName ClusterID = TrustSubsystem->GetClusterAtLocation(GetActorLocation());
					TrustSubsystem->RecordIncident(
						ClusterID,
						FName(TEXT("Incident_SentryPursuitSpillover")),
						UGameplayStatics::GetPlayerCharacter(this, 0),
						this,
						-25
					);
				}
			}
		}

		FString StateStr;
		switch (AlertState)
		{
		case ECurfewAlertState::Unaware: StateStr = TEXT("Unaware"); break;
		case ECurfewAlertState::Suspicious: StateStr = TEXT("Suspicious"); break;
		case ECurfewAlertState::Searching: StateStr = TEXT("Searching"); break;
		case ECurfewAlertState::Alerted: StateStr = TEXT("ALERTED - Curfew Challenge!"); break;
		}

		UE_LOG(LogREVOLUTION, Log, TEXT("Watchman Alert State -> %s (Detection: %.1f%%)"), *StateStr, DetectionMeter);
	}
}

FVector ACurfewPatrolAI::GetDirectionToPlayer(ARevolutionCharacter* TargetPlayer) const
{
	if (!TargetPlayer) return FVector::ZeroVector;
	return (TargetPlayer->GetActorLocation() - GetActorLocation()).GetSafeNormal2D();
}

void ACurfewPatrolAI::InvestigateSoundLocation(const FVector& DisturbanceLocation)
{
	if (AlertState == ECurfewAlertState::Alerted)
	{
		return;
	}

	LastKnownPlayerLocation = DisturbanceLocation;
	SearchTimer = 0.0f;
	DetectionMeter = FMath::Max(DetectionMeter, 45.0f);

	SetAlertState(ECurfewAlertState::Searching);

	UE_LOG(LogREVOLUTION, Log, TEXT("Watchman diverted by acoustic disturbance to %s"), *DisturbanceLocation.ToString());
}

void ACurfewPatrolAI::ResetPatrolState()
{
	DetectionMeter = 0.0f;
	SetAlertState(ECurfewAlertState::Unaware);
	bIsWaitingAtWaypoint = false;
	WaypointWaitTimer = 0.0f;
	SearchTimer = 0.0f;
	ScanLookTimer = 0.0f;

	if (GetCharacterMovement())
	{
		GetCharacterMovement()->StopMovementImmediately();
		GetCharacterMovement()->MaxWalkSpeed = PatrolWalkSpeed;
	}

	if (PatrolWaypoints.Num() > 0)
	{
		CurrentWaypointIndex = 0;
		SetActorLocation(PatrolWaypoints[0]);
		LastKnownPlayerLocation = PatrolWaypoints[0];
	}

	bIsLanternFlickering = false;
	LanternFlickerTimer = 0.0f;
	LanternFlickerCycleTimer = 0.0f;
	if (LanternLight)
	{
		LanternLight->SetIntensity(1400.0f);
	}
	if (LanternBeam)
	{
		LanternBeam->SetIntensity(3200.0f);
	}

	UE_LOG(LogREVOLUTION, Log, TEXT("Watchman %s reset to unaware patrol at origin waypoint."), *GetName());
}

