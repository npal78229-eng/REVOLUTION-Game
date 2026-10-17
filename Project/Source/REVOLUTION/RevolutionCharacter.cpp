// Copyright Epic Games, Inc. All Rights Reserved.

#include "RevolutionCharacter.h"
#include "Engine/LocalPlayer.h"
#include "Camera/CameraComponent.h"
#include "Components/CapsuleComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/SpringArmComponent.h"
#include "GameFramework/Controller.h"
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "InputActionValue.h"
#include "InputMappingContext.h"
#include "InputAction.h"
#include "UObject/ConstructorHelpers.h"
#include "DrawDebugHelpers.h"
#include "Animation/AnimInstance.h"
#include "InteractableInterface.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/SoundBase.h"
#include "Sound/SoundMix.h"
#include "Sound/SoundClass.h"
#include "PebbleProjectile.h"
#include "ChalkMarkActor.h"
#include "HidingSpotActor.h"
#include "CurfewPatrolAI.h"
#include "CivilianNPCActor.h"
#include "RevolutionGameMode.h"
#include "GameFramework/ProjectileMovementComponent.h"
#include "EngineUtils.h"
#include "REVOLUTION.h"

ARevolutionCharacter::ARevolutionCharacter()
{
	PrimaryActorTick.bCanEverTick = true;

	// Capsule dimensions scaled for 12-year-old Kabir (1.42m height)
	GetCapsuleComponent()->InitCapsuleSize(32.f, 71.0f);

	// Don't rotate when the controller rotates; let it affect the camera only.
	bUseControllerRotationPitch = false;
	bUseControllerRotationYaw = false;
	bUseControllerRotationRoll = false;

	// Configure character movement
	GetCharacterMovement()->bOrientRotationToMovement = true;
	GetCharacterMovement()->RotationRate = FRotator(0.0f, 540.0f, 0.0f);
	GetCharacterMovement()->JumpZVelocity = 500.f;
	GetCharacterMovement()->AirControl = 0.35f;
	GetCharacterMovement()->MaxWalkSpeed = WalkSpeed;
	GetCharacterMovement()->MinAnalogWalkSpeed = 20.f;
	GetCharacterMovement()->BrakingDecelerationWalking = 2000.f;
	GetCharacterMovement()->BrakingDecelerationFalling = 1500.0f;
	GetCharacterMovement()->GetNavAgentPropertiesRef().bCanCrouch = true;

	// Camera boom (pulls in towards the player if there is a collision)
	CameraBoom = CreateDefaultSubobject<USpringArmComponent>(TEXT("CameraBoom"));
	CameraBoom->SetupAttachment(RootComponent);
	CameraBoom->TargetArmLength = 320.0f; // Closer camera for grounded cinematic framing
	CameraBoom->SetRelativeLocation(FVector(0.0f, 0.0f, 20.0f));
	CameraBoom->bUsePawnControlRotation = true;

	// Follow camera
	FollowCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FollowCamera"));
	FollowCamera->SetupAttachment(CameraBoom, USpringArmComponent::SocketName);
	FollowCamera->bUsePawnControlRotation = false;

	CurrentStamina = MaxStamina;

	// Automatic Enhanced Input Asset Binding
	static ConstructorHelpers::FObjectFinder<UInputMappingContext> DefaultMappingContextFinder(TEXT("/Game/Characters/Kabir/Input/IMC_Default.IMC_Default"));
	if (DefaultMappingContextFinder.Succeeded())
	{
		DefaultMappingContext = DefaultMappingContextFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<UInputAction> MoveActionFinder(TEXT("/Game/Characters/Kabir/Input/Actions/IA_Move.IA_Move"));
	if (MoveActionFinder.Succeeded())
	{
		MoveAction = MoveActionFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<UInputAction> LookActionFinder(TEXT("/Game/Characters/Kabir/Input/Actions/IA_Look.IA_Look"));
	if (LookActionFinder.Succeeded())
	{
		LookAction = LookActionFinder.Object;
	}

	static ConstructorHelpers::FObjectFinder<UInputAction> JumpActionFinder(TEXT("/Game/Characters/Kabir/Input/Actions/IA_Jump.IA_Jump"));
	if (JumpActionFinder.Succeeded())
	{
		JumpAction = JumpActionFinder.Object;
	}

	// Automatic Character Mannequin & Animation Setup
	static ConstructorHelpers::FObjectFinder<USkeletalMesh> MeshFinder(TEXT("/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple.SKM_Manny_Simple"));
	if (MeshFinder.Succeeded())
	{
		GetMesh()->SetSkeletalMesh(MeshFinder.Object);
		GetMesh()->SetRelativeLocation(FVector(0.f, 0.f, -71.f));
		GetMesh()->SetRelativeRotation(FRotator(0.f, -90.f, 0.f));
		// Proportion scaling for 12-year-old Kabir (approx 78% of adult mannequin)
		GetMesh()->SetRelativeScale3D(FVector(0.78f, 0.78f, 0.78f));
	}

	static ConstructorHelpers::FClassFinder<UAnimInstance> AnimFinder(TEXT("/Game/Characters/Mannequins/Animations/ABP_Manny.ABP_Manny_C"));
	if (AnimFinder.Succeeded())
	{
		GetMesh()->SetAnimInstanceClass(AnimFinder.Class);
	}

	// Automatic Foley Audio Asset Bindings
	static ConstructorHelpers::FObjectFinder<USoundBase> Brick01Finder(TEXT("/Game/Audio/SFX/SFX_Footstep_Brick_01.SFX_Footstep_Brick_01"));
	if (Brick01Finder.Succeeded()) FootstepBrickSound01 = Brick01Finder.Object;

	static ConstructorHelpers::FObjectFinder<USoundBase> Brick02Finder(TEXT("/Game/Audio/SFX/SFX_Footstep_Brick_02.SFX_Footstep_Brick_02"));
	if (Brick02Finder.Succeeded()) FootstepBrickSound02 = Brick02Finder.Object;

	static ConstructorHelpers::FObjectFinder<USoundBase> Wood01Finder(TEXT("/Game/Audio/SFX/SFX_Footstep_Wood_01.SFX_Footstep_Wood_01"));
	if (Wood01Finder.Succeeded()) FootstepWoodSound01 = Wood01Finder.Object;

	static ConstructorHelpers::FObjectFinder<USoundBase> Wood02Finder(TEXT("/Game/Audio/SFX/SFX_Footstep_Wood_02.SFX_Footstep_Wood_02"));
	if (Wood02Finder.Succeeded()) FootstepWoodSound02 = Wood02Finder.Object;

	static ConstructorHelpers::FObjectFinder<USoundBase> VaultFinder(TEXT("/Game/Audio/SFX/SFX_Vault_Whoosh_Cloth.SFX_Vault_Whoosh_Cloth"));
	if (VaultFinder.Succeeded()) VaultSound = VaultFinder.Object;

	static ConstructorHelpers::FObjectFinder<USoundBase> ParchmentOpenFinder(TEXT("/Game/Audio/SFX/SFX_Parchment_Open.SFX_Parchment_Open"));
	if (ParchmentOpenFinder.Succeeded()) InspectOpenSound = ParchmentOpenFinder.Object;

	static ConstructorHelpers::FObjectFinder<USoundBase> ParchmentCloseFinder(TEXT("/Game/Audio/SFX/SFX_Parchment_Close.SFX_Parchment_Close"));
	if (ParchmentCloseFinder.Succeeded()) InspectCloseSound = ParchmentCloseFinder.Object;

	static ConstructorHelpers::FObjectFinder<USoundBase> PebbleThrowFinder(TEXT("/Game/Audio/SFX/SFX_Pebble_Throw.SFX_Pebble_Throw"));
	if (PebbleThrowFinder.Succeeded()) PebbleThrowSound = PebbleThrowFinder.Object;

	static ConstructorHelpers::FObjectFinder<USoundBase> ChalkSoundFinder(TEXT("/Game/Audio/SFX/SFX_Chalk_Draw.SFX_Chalk_Draw"));
	if (ChalkSoundFinder.Succeeded()) ChalkDrawSound = ChalkSoundFinder.Object;
}

void ARevolutionCharacter::BeginPlay()
{
	Super::BeginPlay();

	// Ensure movement component is in walking mode by default
	if (GetCharacterMovement())
	{
		GetCharacterMovement()->SetMovementMode(MOVE_Walking);
	}

	// Guarantee all blocking state flags are initialized clear
	bIsVaulting = false;
	bIsInspecting = false;
	bIsCrawlTraversing = false;
	bIsSatchelJournalOpen = false;
	bIsHidingInCover = false;

	// Add input mapping context to Enhanced Input Subsystem if controller already assigned
	if (APlayerController* PlayerController = Cast<APlayerController>(Controller))
	{
		if (ULocalPlayer* LP = PlayerController->GetLocalPlayer())
		{
			if (UEnhancedInputLocalPlayerSubsystem* Subsystem = ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(LP))
			{
				if (DefaultMappingContext && !Subsystem->HasMappingContext(DefaultMappingContext))
				{
					Subsystem->AddMappingContext(DefaultMappingContext, 0);
				}
			}

			FInputModeGameOnly InputModeData;
			InputModeData.SetConsumeCaptureMouseDown(false);
			PlayerController->SetInputMode(InputModeData);
			PlayerController->SetShowMouseCursor(false);
		}
	}
}

void ARevolutionCharacter::PossessedBy(AController* NewController)
{
	Super::PossessedBy(NewController);

	if (GetCharacterMovement())
	{
		GetCharacterMovement()->SetMovementMode(MOVE_Walking);
	}

	// Ensure Enhanced Input Mapping Context is registered immediately upon possession
	if (APlayerController* PlayerController = Cast<APlayerController>(NewController))
	{
		if (ULocalPlayer* LP = PlayerController->GetLocalPlayer())
		{
			if (UEnhancedInputLocalPlayerSubsystem* Subsystem = ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(LP))
			{
				if (DefaultMappingContext && !Subsystem->HasMappingContext(DefaultMappingContext))
				{
					Subsystem->AddMappingContext(DefaultMappingContext, 0);
				}
			}

			FInputModeGameOnly InputModeData;
			InputModeData.SetConsumeCaptureMouseDown(false);
			PlayerController->SetInputMode(InputModeData);
			PlayerController->SetShowMouseCursor(false);
		}
	}
}

void ARevolutionCharacter::PawnClientRestart()
{
	Super::PawnClientRestart();

	if (GetCharacterMovement())
	{
		GetCharacterMovement()->SetMovementMode(MOVE_Walking);
	}

	if (APlayerController* PC = Cast<APlayerController>(GetController()))
	{
		if (ULocalPlayer* LP = PC->GetLocalPlayer())
		{
			if (UEnhancedInputLocalPlayerSubsystem* Subsystem = ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(LP))
			{
				if (DefaultMappingContext)
				{
					if (!Subsystem->HasMappingContext(DefaultMappingContext))
					{
						Subsystem->AddMappingContext(DefaultMappingContext, 0);
					}
				}
			}

			FInputModeGameOnly InputModeData;
			InputModeData.SetConsumeCaptureMouseDown(false);
			PC->SetInputMode(InputModeData);
			PC->SetShowMouseCursor(false);
		}
	}
}

void ARevolutionCharacter::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	// Vault traversal interpolation
	if (bIsVaulting)
	{
		VaultProgress += (DeltaTime / FMath::Max(VaultDuration, 0.05f));
		float ClampedProgress = FMath::Clamp(VaultProgress, 0.0f, 1.0f);

		FVector CurrentLocation = FMath::Lerp(VaultStartLocation, VaultTargetLocation, ClampedProgress);
		// Parabolic arc for natural body clearance over 1.1m parapet
		float ArcOffset = VaultArcPeak * FMath::Sin(ClampedProgress * PI);
		CurrentLocation.Z += ArcOffset;

		SetActorLocation(CurrentLocation, true);

		if (VaultProgress >= 1.0f)
		{
			bIsVaulting = false;
			VaultProgress = 0.0f;
			GetCharacterMovement()->SetMovementMode(MOVE_Walking);
		}
	}

	// High mantle traversal interpolation (Athletic pull-up onto haveli walls & ledges)
	if (bIsMantling)
	{
		MantleProgress += (DeltaTime / FMath::Max(MantleDuration, 0.05f));
		float ClampedProgress = FMath::Clamp(MantleProgress, 0.0f, 1.0f);
		float SmoothedProgress = FMath::InterpEaseInOut(0.0f, 1.0f, ClampedProgress, 2.2f);

		FVector CurrentLocation = FMath::Lerp(MantleStartLocation, MantleTargetLocation, SmoothedProgress);
		SetActorLocation(CurrentLocation, true);

		if (MantleProgress >= 1.0f)
		{
			bIsMantling = false;
			MantleProgress = 0.0f;
			GetCharacterMovement()->SetMovementMode(MOVE_Walking);
			GetCharacterMovement()->Velocity = FVector::ZeroVector;
		}
	}

	// Low drain crawlway traversal interpolation
	if (bIsCrawlTraversing)
	{
		CrawlProgress += (DeltaTime / FMath::Max(CurrentCrawlDuration, 0.1f));
		float ClampedProgress = FMath::Clamp(CrawlProgress, 0.0f, 1.0f);
		float SmoothedProgress = FMath::InterpEaseInOut(0.0f, 1.0f, ClampedProgress, 2.0f);

		FVector CurrentLocation = FMath::Lerp(CrawlStartLocation, CrawlTargetLocation, SmoothedProgress);
		SetActorLocation(CurrentLocation, true);

		// Orient smoothly towards travel direction
		FVector TravelDir = (CrawlTargetLocation - CrawlStartLocation).GetSafeNormal2D();
		if (!TravelDir.IsNearlyZero())
		{
			SetActorRotation(TravelDir.Rotation());
		}

		if (CrawlProgress >= 1.0f)
		{
			bIsCrawlTraversing = false;
			CrawlProgress = 0.0f;
			GetCapsuleComponent()->SetCapsuleHalfHeight(58.0f);
			GetCharacterMovement()->SetMovementMode(MOVE_Walking);
			Crouch(); // Keep player in crouched stealth posture upon emerging
		}
	}

	// Stamina management
	if (bIsSprinting && GetCharacterMovement()->Velocity.SizeSquared() > 100.0f)
	{
		CurrentStamina = FMath::Clamp(CurrentStamina - (StaminaDrainRate * DeltaTime), 0.0f, MaxStamina);
		if (CurrentStamina <= 0.0f)
		{
			StopSprinting();
		}
	}
	else if (CurrentStamina < MaxStamina)
	{
		CurrentStamina = FMath::Clamp(CurrentStamina + (StaminaRegenRate * DeltaTime), 0.0f, MaxStamina);
	}

	// Footstep cadence based on movement velocity
	float CurrentSpeed = GetVelocity().Size2D();
	if (CurrentSpeed > 35.0f && GetCharacterMovement()->IsMovingOnGround())
	{
		FootstepDistanceAccumulator += CurrentSpeed * DeltaTime;
		// Step interval: Walk ~ 160cm, Sprint ~ 210cm
		float StepInterval = bIsSprinting ? 210.0f : 160.0f;
		if (FootstepDistanceAccumulator >= StepInterval)
		{
			FootstepDistanceAccumulator = 0.0f;
			PlayFootstepAudio();
		}
	}
	else
	{
		FootstepDistanceAccumulator = 0.0f;
	}

	// Direct keyboard movement fallback (guarantees movement even if Enhanced Input subsystem dropped context)
	if (Controller != nullptr && !bIsVaulting && !bIsMantling && !bIsInspecting && !bIsCrawlTraversing && !bIsSatchelJournalOpen)
	{
		if (APlayerController* PC = Cast<APlayerController>(Controller))
		{
			float ForwardInput = 0.0f;
			float RightInput = 0.0f;

			if (PC->IsInputKeyDown(EKeys::W) || PC->IsInputKeyDown(EKeys::Up)) ForwardInput += 1.0f;
			if (PC->IsInputKeyDown(EKeys::S) || PC->IsInputKeyDown(EKeys::Down)) ForwardInput -= 1.0f;
			if (PC->IsInputKeyDown(EKeys::D) || PC->IsInputKeyDown(EKeys::Right)) RightInput += 1.0f;
			if (PC->IsInputKeyDown(EKeys::A) || PC->IsInputKeyDown(EKeys::Left)) RightInput -= 1.0f;

			if (!FMath::IsNearlyZero(ForwardInput) || !FMath::IsNearlyZero(RightInput))
			{
				const FRotator Rotation = Controller->GetControlRotation();
				const FRotator YawRotation(0, Rotation.Yaw, 0);
				const FVector ForwardDirection = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::X);
				const FVector RightDirection = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::Y);

				if (!FMath::IsNearlyZero(ForwardInput))
				{
					AddMovementInput(ForwardDirection, ForwardInput);
				}
				if (!FMath::IsNearlyZero(RightInput))
				{
					AddMovementInput(RightDirection, RightInput);
				}
			}
		}
	}

	// Dynamic Corner Peeking / Lean interpolation (Dishonored / The Last of Us)
	float TargetLean = 0.0f;
	if (bIsLeaningLeft) TargetLean -= 1.0f;
	if (bIsLeaningRight) TargetLean += 1.0f;
	LeanOffset = FMath::FInterpTo(LeanOffset, TargetLean, DeltaTime, 8.0f);

	if (CameraBoom)
	{
		CameraBoom->SocketOffset = FVector(0.0f, LeanOffset * 48.0f, 0.0f);
		FRotator CurrentBoomRot = CameraBoom->GetRelativeRotation();
		CurrentBoomRot.Roll = LeanOffset * 5.0f;
		CameraBoom->SetRelativeRotation(CurrentBoomRot);
	}

	CheckForInteractables();
	UpdateCrowdBlending(DeltaTime);
	UpdateEnvironmentalConcealment(DeltaTime);

	// Boiler steam obscurity timer decay (Hitman / Batman Arkham benchmark)
	if (bIsSteamObscured)
	{
		SteamObscurityRemainingTime -= DeltaTime;
		if (SteamObscurityRemainingTime <= 0.0f)
		{
			SteamObscurityRemainingTime = 0.0f;
			bIsSteamObscured = false;
		}
	}
}

void ARevolutionCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);

	// 0. Ensure Enhanced Input Mapping Context is registered on Local Player Subsystem
	if (APlayerController* PlayerController = Cast<APlayerController>(GetController()))
	{
		if (UEnhancedInputLocalPlayerSubsystem* Subsystem = ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(PlayerController->GetLocalPlayer()))
		{
			if (DefaultMappingContext && !Subsystem->HasMappingContext(DefaultMappingContext))
			{
				Subsystem->AddMappingContext(DefaultMappingContext, 0);
			}
		}

		FInputModeGameOnly InputModeData;
		InputModeData.SetConsumeCaptureMouseDown(false);
		PlayerController->SetInputMode(InputModeData);
		PlayerController->SetShowMouseCursor(false);
	}

	// 1. Enhanced Input Component Bindings
	if (UEnhancedInputComponent* EnhancedInputComponent = Cast<UEnhancedInputComponent>(PlayerInputComponent))
	{
		if (JumpAction)
		{
			EnhancedInputComponent->BindAction(JumpAction, ETriggerEvent::Started, this, &ARevolutionCharacter::OnJumpPressed);
			EnhancedInputComponent->BindAction(JumpAction, ETriggerEvent::Completed, this, &ARevolutionCharacter::OnJumpReleased);
		}

		if (MoveAction)
		{
			EnhancedInputComponent->BindAction(MoveAction, ETriggerEvent::Triggered, this, &ARevolutionCharacter::Move);
		}

		if (LookAction)
		{
			EnhancedInputComponent->BindAction(LookAction, ETriggerEvent::Triggered, this, &ARevolutionCharacter::Look);
		}

		if (SprintAction)
		{
			EnhancedInputComponent->BindAction(SprintAction, ETriggerEvent::Started, this, &ARevolutionCharacter::StartSprinting);
			EnhancedInputComponent->BindAction(SprintAction, ETriggerEvent::Completed, this, &ARevolutionCharacter::StopSprinting);
		}

		if (CrouchAction)
		{
			EnhancedInputComponent->BindAction(CrouchAction, ETriggerEvent::Started, this, &ARevolutionCharacter::ToggleCrouch);
		}

		if (InteractAction)
		{
			EnhancedInputComponent->BindAction(InteractAction, ETriggerEvent::Started, this, &ARevolutionCharacter::OnInteract);
		}
	}

	// 2. Direct Raw Input Bindings (Guarantees zero-dependency keyboard/mouse response)
	PlayerInputComponent->BindAxis(TEXT("MoveForward"), this, &ARevolutionCharacter::MoveForwardAxis);
	PlayerInputComponent->BindAxis(TEXT("MoveRight"), this, &ARevolutionCharacter::MoveRightAxis);

	PlayerInputComponent->BindAxisKey(EKeys::MouseX, this, &ARevolutionCharacter::TurnAxis);
	PlayerInputComponent->BindAxisKey(EKeys::MouseY, this, &ARevolutionCharacter::LookUpAxis);

	PlayerInputComponent->BindKey(EKeys::SpaceBar, IE_Pressed, this, &ARevolutionCharacter::OnJumpPressed);
	PlayerInputComponent->BindKey(EKeys::SpaceBar, IE_Released, this, &ARevolutionCharacter::OnJumpReleased);

	PlayerInputComponent->BindKey(EKeys::LeftShift, IE_Pressed, this, &ARevolutionCharacter::StartSprinting);
	PlayerInputComponent->BindKey(EKeys::LeftShift, IE_Released, this, &ARevolutionCharacter::StopSprinting);

	PlayerInputComponent->BindKey(EKeys::C, IE_Pressed, this, &ARevolutionCharacter::ToggleCrouch);
	PlayerInputComponent->BindKey(EKeys::E, IE_Pressed, this, &ARevolutionCharacter::OnInteract);
	PlayerInputComponent->BindKey(EKeys::Enter, IE_Pressed, this, &ARevolutionCharacter::OnInteract);
	PlayerInputComponent->BindKey(EKeys::F, IE_Pressed, this, &ARevolutionCharacter::ThrowPebble);
	PlayerInputComponent->BindKey(EKeys::G, IE_Pressed, this, &ARevolutionCharacter::ThrowPebble);
	PlayerInputComponent->BindKey(EKeys::T, IE_Pressed, this, &ARevolutionCharacter::DrawChalkMark);

	PlayerInputComponent->BindKey(EKeys::Tab, IE_Pressed, this, &ARevolutionCharacter::ToggleSatchelJournal);
	PlayerInputComponent->BindKey(EKeys::J, IE_Pressed, this, &ARevolutionCharacter::ToggleSatchelJournal);
	PlayerInputComponent->BindKey(EKeys::Escape, IE_Pressed, this, &ARevolutionCharacter::EndInspection);
	PlayerInputComponent->BindKey(EKeys::One, IE_Pressed, this, &ARevolutionCharacter::SelectSatchelTab1);
	PlayerInputComponent->BindKey(EKeys::Two, IE_Pressed, this, &ARevolutionCharacter::SelectSatchelTab2);
	PlayerInputComponent->BindKey(EKeys::Three, IE_Pressed, this, &ARevolutionCharacter::SelectSatchelTab3);
	PlayerInputComponent->BindKey(EKeys::Four, IE_Pressed, this, &ARevolutionCharacter::SelectSatchelTab4);

	PlayerInputComponent->BindKey(EKeys::Up, IE_Pressed, this, &ARevolutionCharacter::OnMenuUp);
	PlayerInputComponent->BindKey(EKeys::Down, IE_Pressed, this, &ARevolutionCharacter::OnMenuDown);
	PlayerInputComponent->BindKey(EKeys::Left, IE_Pressed, this, &ARevolutionCharacter::OnMenuLeft);
	PlayerInputComponent->BindKey(EKeys::Right, IE_Pressed, this, &ARevolutionCharacter::OnMenuRight);
	PlayerInputComponent->BindKey(EKeys::LeftBracket, IE_Pressed, this, &ARevolutionCharacter::SelectPrevCodexEntry);
	PlayerInputComponent->BindKey(EKeys::RightBracket, IE_Pressed, this, &ARevolutionCharacter::SelectNextCodexEntry);

	// Benchmark Aim & Distraction Mechanics (A Plague Tale / The Last of Us)
	PlayerInputComponent->BindKey(EKeys::RightMouseButton, IE_Pressed, this, &ARevolutionCharacter::StartAimingPebble);
	PlayerInputComponent->BindKey(EKeys::RightMouseButton, IE_Released, this, &ARevolutionCharacter::StopAimingPebble);

	// AAA Benchmark: Corner Peeking & Lean (Dishonored / The Last of Us)
	PlayerInputComponent->BindKey(EKeys::Q, IE_Pressed, this, &ARevolutionCharacter::StartLeanLeft);
	PlayerInputComponent->BindKey(EKeys::Q, IE_Released, this, &ARevolutionCharacter::StopLeanLeft);
	PlayerInputComponent->BindKey(EKeys::E, IE_Pressed, this, &ARevolutionCharacter::StartLeanRight);
	PlayerInputComponent->BindKey(EKeys::E, IE_Released, this, &ARevolutionCharacter::StopLeanRight);

	// AAA Benchmark: Keen Senses / Basant Intuition (Assassin's Creed Eagle Vision / Hitman Instinct)
	PlayerInputComponent->BindKey(EKeys::V, IE_Pressed, this, &ARevolutionCharacter::ToggleKeenSenses);
}

void ARevolutionCharacter::Move(const FInputActionValue& Value)
{
	if (bIsVaulting || bIsMantling || bIsInspecting || bIsCrawlTraversing || bIsSatchelJournalOpen) return;

	FVector2D MovementVector = Value.Get<FVector2D>();

	if (bIsHidingInCover)
	{
		if (MovementVector.SizeSquared() > 0.35f && CurrentHidingSpot)
		{
			CurrentHidingSpot->EjectOccupant();
		}
		return;
	}

	if (Controller != nullptr)
	{
		const FRotator Rotation = Controller->GetControlRotation();
		const FRotator YawRotation(0, Rotation.Yaw, 0);

		const FVector ForwardDirection = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::X);
		const FVector RightDirection = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::Y);

		AddMovementInput(ForwardDirection, MovementVector.Y);
		AddMovementInput(RightDirection, MovementVector.X);
	}
}

void ARevolutionCharacter::Look(const FInputActionValue& Value)
{
	FVector2D LookAxisVector = Value.Get<FVector2D>();

	if (Controller != nullptr)
	{
		AddControllerYawInput(LookAxisVector.X);
		AddControllerPitchInput(LookAxisVector.Y);
	}
}

void ARevolutionCharacter::MoveForwardAxis(float Value)
{
	if (bIsVaulting || bIsMantling || bIsInspecting || bIsCrawlTraversing || bIsSatchelJournalOpen || FMath::IsNearlyZero(Value)) return;

	if (bIsHidingInCover)
	{
		if (FMath::Abs(Value) > 0.4f && CurrentHidingSpot)
		{
			CurrentHidingSpot->EjectOccupant();
		}
		return;
	}

	if (Controller != nullptr)
	{
		const FRotator Rotation = Controller->GetControlRotation();
		const FRotator YawRotation(0, Rotation.Yaw, 0);
		const FVector ForwardDirection = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::X);
		AddMovementInput(ForwardDirection, Value);
	}
}

void ARevolutionCharacter::MoveRightAxis(float Value)
{
	if (bIsVaulting || bIsMantling || bIsInspecting || bIsCrawlTraversing || bIsSatchelJournalOpen || FMath::IsNearlyZero(Value)) return;

	if (bIsHidingInCover)
	{
		if (FMath::Abs(Value) > 0.4f && CurrentHidingSpot)
		{
			CurrentHidingSpot->EjectOccupant();
		}
		return;
	}

	if (Controller != nullptr)
	{
		const FRotator Rotation = Controller->GetControlRotation();
		const FRotator YawRotation(0, Rotation.Yaw, 0);
		const FVector RightDirection = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::Y);
		AddMovementInput(RightDirection, Value);
	}
}

void ARevolutionCharacter::TurnAxis(float Value)
{
	if (!FMath::IsNearlyZero(Value) && Controller != nullptr)
	{
		AddControllerYawInput(Value);
	}
}

void ARevolutionCharacter::LookUpAxis(float Value)
{
	if (!FMath::IsNearlyZero(Value) && Controller != nullptr)
	{
		AddControllerPitchInput(-Value);
	}
}

void ARevolutionCharacter::OnJumpPressed()
{
	ARevolutionGameMode* GM = Cast<ARevolutionGameMode>(UGameplayStatics::GetGameMode(this));
	if (GM && GM->IsPlayerApprehended())
	{
		GM->RespawnPlayerAtCheckpoint();
		return;
	}

	if (bIsInspecting || bIsCrawlTraversing)
	{
		if (bIsInspecting)
		{
			EndInspection();
		}
		return;
	}

	if (bIsHidingInCover && CurrentHidingSpot)
	{
		CurrentHidingSpot->EjectOccupant();
		return;
	}

	TryVaultOrJump();
}

void ARevolutionCharacter::OnJumpReleased()
{
	StopJumping();
}

void ARevolutionCharacter::TryVaultOrJump()
{
	if (bIsVaulting || bIsMantling) return;

	FVector TargetLocation;
	if (DetectVaultableObstacle(TargetLocation))
	{
		bIsVaulting = true;
		VaultProgress = 0.0f;
		VaultStartLocation = GetActorLocation();
		VaultTargetLocation = TargetLocation;

		GetCharacterMovement()->SetMovementMode(MOVE_Flying);
		GetCharacterMovement()->Velocity = FVector::ZeroVector;

		PlayVaultAudio();

		UE_LOG(LogREVOLUTION, Log, TEXT("Kabir vaulting over parapet to %s"), *TargetLocation.ToString());
	}
	else if (DetectMantleableLedge(TargetLocation))
	{
		bIsMantling = true;
		MantleProgress = 0.0f;
		MantleStartLocation = GetActorLocation();
		MantleTargetLocation = TargetLocation;

		GetCharacterMovement()->SetMovementMode(MOVE_Flying);
		GetCharacterMovement()->Velocity = FVector::ZeroVector;

		PlayVaultAudio();

		UE_LOG(LogREVOLUTION, Log, TEXT("Kabir mantling up onto high ledge to %s"), *TargetLocation.ToString());
	}
	else
	{
		ACharacter::Jump();
	}
}

void ARevolutionCharacter::StartSprinting()
{
	if (CurrentStamina > 10.0f)
	{
		bIsSprinting = true;
		GetCharacterMovement()->MaxWalkSpeed = SprintSpeed;
	}
}

void ARevolutionCharacter::StopSprinting()
{
	bIsSprinting = false;
	GetCharacterMovement()->MaxWalkSpeed = WalkSpeed;
}

void ARevolutionCharacter::ToggleCrouch()
{
	if (bIsCrouched)
	{
		UnCrouch();
	}
	else
	{
		Crouch();
	}
}

void ARevolutionCharacter::OnInteract()
{
	ARevolutionGameMode* GM = Cast<ARevolutionGameMode>(UGameplayStatics::GetGameMode(this));
	if (GM && GM->IsPlayerApprehended())
	{
		GM->RespawnPlayerAtCheckpoint();
		return;
	}

	if (bIsSatchelJournalOpen)
	{
		ToggleSatchelJournal();
		return;
	}

	if (bIsInspecting)
	{
		EndInspection();
		return;
	}

	if (bIsHidingInCover && CurrentHidingSpot)
	{
		CurrentHidingSpot->EjectOccupant();
		return;
	}

	if (CurrentInteractableActor && CurrentInteractableActor->Implements<UInteractableInterface>())
	{
		IInteractableInterface::Execute_OnInteract(CurrentInteractableActor, this);
		UE_LOG(LogREVOLUTION, Log, TEXT("Kabir interacted with %s"), *CurrentInteractableActor->GetName());
	}
	else
	{
		UE_LOG(LogREVOLUTION, Log, TEXT("Kabir triggered interact, no interactable in focus."));
	}
}

void ARevolutionCharacter::StartInspection(const FText& InItemName, const FText& InLoreDescription)
{
	bIsInspecting = true;
	InspectedItemName = InItemName;
	InspectedItemLore = InLoreDescription;
	StopSprinting();
	PlayInspectAudio(true);
	OnItemInspected.Broadcast(InItemName, InLoreDescription);
	UE_LOG(LogREVOLUTION, Log, TEXT("Kabir started inspection of: %s"), *InItemName.ToString());
}

void ARevolutionCharacter::EndInspection()
{
	bIsInspecting = false;
	InspectedItemName = FText::GetEmpty();
	InspectedItemLore = FText::GetEmpty();
	PlayInspectAudio(false);
	OnInspectionEnded.Broadcast();
	UE_LOG(LogREVOLUTION, Log, TEXT("Kabir closed inspection"));
}

void ARevolutionCharacter::CheckForInteractables()
{
	if (bIsInspecting || bIsSatchelJournalOpen)
	{
		return;
	}

	if (bIsHidingInCover && CurrentHidingSpot)
	{
		if (CurrentInteractableActor != CurrentHidingSpot)
		{
			CurrentInteractableActor = CurrentHidingSpot;
			OnInteractionFocusChanged.Broadcast(true, CurrentHidingSpot->ExitPrompt);
		}
		return;
	}

	FVector Start = FollowCamera ? FollowCamera->GetComponentLocation() : (GetActorLocation() + FVector(0.f, 0.f, 40.f));
	FVector Forward = FollowCamera ? FollowCamera->GetForwardVector() : GetActorForwardVector();
	FVector End = Start + (Forward * InteractionTraceDistance);

	FHitResult Hit;
	FCollisionQueryParams Params;
	Params.AddIgnoredActor(this);

	AActor* FocusedActor = nullptr;
	FText PromptText = FText::GetEmpty();

	if (GetWorld()->SweepSingleByChannel(Hit, Start, End, FQuat::Identity, ECC_Visibility, FCollisionShape::MakeSphere(35.0f), Params))
	{
		if (Hit.GetActor() && Hit.GetActor()->Implements<UInteractableInterface>())
		{
			if (IInteractableInterface::Execute_CanInteract(Hit.GetActor(), this))
			{
				FocusedActor = Hit.GetActor();
				PromptText = IInteractableInterface::Execute_GetInteractionPrompt(Hit.GetActor());
			}
		}
	}

	if (FocusedActor != CurrentInteractableActor)
	{
		CurrentInteractableActor = FocusedActor;
		bool bHasFocus = (CurrentInteractableActor != nullptr);
		OnInteractionFocusChanged.Broadcast(bHasFocus, PromptText);
	}
}

bool ARevolutionCharacter::DetectVaultableObstacle(FVector& OutVaultLocation)
{
	FVector Start = GetActorLocation() + FVector(0.f, 0.f, 20.f);
	FVector Forward = GetActorForwardVector();
	FVector End = Start + (Forward * 120.f);

	FHitResult Hit;
	FCollisionQueryParams Params;
	Params.AddIgnoredActor(this);

	if (GetWorld()->LineTraceSingleByChannel(Hit, Start, End, ECC_Visibility, Params))
	{
		// Top of obstacle height check (checks from 140cm above down to ground)
		FVector HeightCheckStart = Hit.Location + (Forward * 35.f) + FVector(0.f, 0.f, 140.f);
		FVector HeightCheckEnd = HeightCheckStart - FVector(0.f, 0.f, 160.f);
		FHitResult HeightHit;

		if (GetWorld()->LineTraceSingleByChannel(HeightHit, HeightCheckStart, HeightCheckEnd, ECC_Visibility, Params))
		{
			// Obstacle height relative to character ground base
			float ObstacleHeight = (HeightHit.ImpactPoint.Z - GetActorLocation().Z) + 71.0f;
			if (ObstacleHeight >= 50.f && ObstacleHeight <= 130.f)
			{
				// Vault destination: on top or clearance past obstacle
				OutVaultLocation = HeightHit.ImpactPoint + (Forward * 45.f) + FVector(0.f, 0.f, 71.0f);
				return true;
			}
		}
	}

	return false;
}

bool ARevolutionCharacter::DetectMantleableLedge(FVector& OutMantleLocation)
{
	FVector Start = GetActorLocation() + FVector(0.f, 0.f, 50.f);
	FVector Forward = GetActorForwardVector();
	FVector End = Start + (Forward * 130.f);

	FHitResult Hit;
	FCollisionQueryParams Params;
	Params.AddIgnoredActor(this);

	if (GetWorld()->LineTraceSingleByChannel(Hit, Start, End, ECC_Visibility, Params))
	{
		// Top of high ledge check (checks from 230cm above down to 110cm)
		FVector HeightCheckStart = Hit.Location + (Forward * 35.f) + FVector(0.f, 0.f, 220.f);
		FVector HeightCheckEnd = HeightCheckStart - FVector(0.f, 0.f, 180.f);
		FHitResult HeightHit;

		if (GetWorld()->LineTraceSingleByChannel(HeightHit, HeightCheckStart, HeightCheckEnd, ECC_Visibility, Params))
		{
			// Obstacle height relative to character ground base
			float ObstacleHeight = (HeightHit.ImpactPoint.Z - GetActorLocation().Z) + 71.0f;
			if (ObstacleHeight > 125.f && ObstacleHeight <= 220.f)
			{
				// Mantle destination: landing smoothly on top surface of the ledge with capsule clearance
				OutMantleLocation = HeightHit.ImpactPoint + (Forward * 22.f) + FVector(0.f, 0.f, 72.0f);
				return true;
			}
		}
	}

	return false;
}

void ARevolutionCharacter::PlayFootstepAudio()
{
	FVector Start = GetActorLocation();
	FVector End = Start - FVector(0.f, 0.f, 90.f);

	FHitResult Hit;
	FCollisionQueryParams Params;
	Params.AddIgnoredActor(this);

	bool bOnWood = false;
	if (GetWorld()->LineTraceSingleByChannel(Hit, Start, End, ECC_Visibility, Params))
	{
		if (Hit.GetActor() && Hit.GetActor()->GetName().Contains(TEXT("Wood"), ESearchCase::IgnoreCase))
		{
			bOnWood = true;
		}
		else if (Hit.Component.IsValid() && Hit.Component->GetName().Contains(TEXT("Wood"), ESearchCase::IgnoreCase))
		{
			bOnWood = true;
		}
	}

	bFootstepAlternate = !bFootstepAlternate;
	USoundBase* SoundToPlay = nullptr;
	if (bOnWood)
	{
		SoundToPlay = bFootstepAlternate ? FootstepWoodSound01 : FootstepWoodSound02;
	}
	else
	{
		SoundToPlay = bFootstepAlternate ? FootstepBrickSound01 : FootstepBrickSound02;
	}

	if (SoundToPlay)
	{
		float PitchMod = FMath::RandRange(0.92f, 1.08f);
		float VolumeMod = bIsSprinting ? 0.95f : 0.70f;
		UGameplayStatics::PlaySoundAtLocation(this, SoundToPlay, GetActorLocation() - FVector(0.f, 0.f, 70.f), VolumeMod, PitchMod);
	}
}

void ARevolutionCharacter::PlayVaultAudio()
{
	if (VaultSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, VaultSound, GetActorLocation(), 1.0f, FMath::RandRange(0.95f, 1.05f));
	}
}

void ARevolutionCharacter::PlayInspectAudio(bool bOpen)
{
	USoundBase* SoundToPlay = bOpen ? InspectOpenSound : InspectCloseSound;
	if (SoundToPlay)
	{
		UGameplayStatics::PlaySound2D(this, SoundToPlay, 0.85f, FMath::RandRange(0.96f, 1.04f));
	}
}

void ARevolutionCharacter::ThrowPebble()
{
	if (bIsInspecting || PebbleCount <= 0)
	{
		return;
	}

	UWorld* World = GetWorld();
	if (!World)
	{
		return;
	}

	PebbleCount--;
	bIsAimingPebble = false;

	FVector SpawnLoc = GetActorLocation() + FVector(0.f, 0.f, 30.f);
	FRotator SpawnRot = GetActorRotation();

	if (FollowCamera)
	{
		SpawnLoc = FollowCamera->GetComponentLocation() + (FollowCamera->GetForwardVector() * 50.f);
		SpawnRot = FollowCamera->GetComponentRotation();
		SpawnRot.Pitch = FMath::Clamp(SpawnRot.Pitch + 5.0f, -60.0f, 60.0f);
	}
	else
	{
		SpawnLoc += GetActorForwardVector() * 40.f;
		SpawnRot.Pitch += 8.0f;
	}

	FActorSpawnParameters SpawnParams;
	SpawnParams.Owner = this;
	SpawnParams.Instigator = this;
	SpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

	APebbleProjectile* Pebble = World->SpawnActor<APebbleProjectile>(APebbleProjectile::StaticClass(), SpawnLoc, SpawnRot, SpawnParams);
	if (Pebble && Pebble->ProjectileMovement)
	{
		FVector LaunchDir = SpawnRot.Vector();
		Pebble->ProjectileMovement->Velocity = LaunchDir * Pebble->ProjectileMovement->InitialSpeed;
	}

	if (PebbleThrowSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, PebbleThrowSound, GetActorLocation(), 0.9f, FMath::RandRange(0.95f, 1.05f));
	}

	UE_LOG(LogREVOLUTION, Log, TEXT("Kabir threw distraction pebble! Pebbles remaining: %d"), PebbleCount);
}

void ARevolutionCharacter::StartAimingPebble()
{
	if (PebbleCount > 0 && !bIsInspecting && !bIsSatchelJournalOpen)
	{
		bIsAimingPebble = true;
	}
}

void ARevolutionCharacter::StopAimingPebble()
{
	bIsAimingPebble = false;
}

bool ARevolutionCharacter::CalculatePebbleTrajectory(TArray<FVector>& OutPathPoints, FVector& OutHitLocation, bool& bOutHitValid) const
{
	OutPathPoints.Reset();
	bOutHitValid = false;
	OutHitLocation = FVector::ZeroVector;

	UWorld* World = GetWorld();
	if (!World) return false;

	FVector LaunchPos = FollowCamera ? FollowCamera->GetComponentLocation() + (FollowCamera->GetForwardVector() * 50.f)
	                                 : (GetActorLocation() + GetActorForwardVector() * 40.f + FVector(0.f, 0.f, 30.f));

	FRotator LaunchRot = FollowCamera ? FollowCamera->GetComponentRotation() : GetActorRotation();
	LaunchRot.Pitch = FMath::Clamp(LaunchRot.Pitch + 5.0f, -60.0f, 60.0f);

	FVector InitialVelocity = LaunchRot.Vector() * 1350.0f;
	const FVector Gravity = FVector(0.0f, 0.0f, -980.0f * 1.15f);

	OutPathPoints.Add(LaunchPos);
	FVector PrevPos = LaunchPos;

	FCollisionQueryParams TraceParams;
	TraceParams.AddIgnoredActor(this);

	const float StepTime = 0.05f;
	const int32 MaxSteps = 24;

	for (int32 Step = 1; Step <= MaxSteps; ++Step)
	{
		float T = Step * StepTime;
		FVector CurrentPos = LaunchPos + (InitialVelocity * T) + (0.5f * Gravity * T * T);

		FHitResult Hit;
		if (World->LineTraceSingleByChannel(Hit, PrevPos, CurrentPos, ECC_Visibility, TraceParams))
		{
			OutPathPoints.Add(Hit.ImpactPoint);
			OutHitLocation = Hit.ImpactPoint;
			bOutHitValid = true;
			break;
		}

		OutPathPoints.Add(CurrentPos);
		PrevPos = CurrentPos;
	}

	return OutPathPoints.Num() > 1;
}

void ARevolutionCharacter::UpdateCrowdBlending(float DeltaTime)
{
	if (bIsSprinting || bIsVaulting || bIsMantling || bIsHidingInCover || bIsCrawlTraversing)
	{
		bIsCrowdBlended = false;
		return;
	}

	UWorld* World = GetWorld();
	if (!World)
	{
		bIsCrowdBlended = false;
		return;
	}

	int32 NearbyCiviliansCount = 0;
	const FVector PlayerLoc = GetActorLocation();

	for (TActorIterator<APawn> It(World); It; ++It)
	{
		APawn* NearbyPawn = *It;
		if (NearbyPawn && NearbyPawn != this)
		{
			FString ActorName = NearbyPawn->GetName();
#if WITH_EDITOR
			if (!NearbyPawn->GetActorLabel().IsEmpty())
			{
				ActorName = NearbyPawn->GetActorLabel();
			}
#endif

			if (ActorName.StartsWith(TEXT("NPC_")) || ActorName.Contains(TEXT("Civilian"), ESearchCase::IgnoreCase))
			{
				float Dist = FVector::Dist(PlayerLoc, NearbyPawn->GetActorLocation());
				if (Dist <= CrowdBlendRadius)
				{
					NearbyCiviliansCount++;
				}
			}
		}
	}

	bIsCrowdBlended = (NearbyCiviliansCount >= 1);
}

void ARevolutionCharacter::DrawChalkMark()
{
	if (bIsInspecting || ChalkCount <= 0)
	{
		return;
	}

	UWorld* World = GetWorld();
	if (!World)
	{
		return;
	}

	FVector TraceStart = GetActorLocation() + FVector(0.f, 0.f, 20.f);
	FVector TraceEnd = TraceStart + (GetActorForwardVector() * 180.f);

	if (FollowCamera)
	{
		TraceStart = FollowCamera->GetComponentLocation();
		TraceEnd = TraceStart + (FollowCamera->GetForwardVector() * 220.f);
	}

	FHitResult Hit;
	FCollisionQueryParams Params;
	Params.AddIgnoredActor(this);

	if (World->LineTraceSingleByChannel(Hit, TraceStart, TraceEnd, ECC_Visibility, Params))
	{
		ChalkCount--;

		FVector SpawnLoc = Hit.ImpactPoint + (Hit.ImpactNormal * 1.5f);
		FRotator SpawnRot = Hit.ImpactNormal.Rotation();

		FActorSpawnParameters SpawnParams;
		SpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

		AChalkMarkActor* Mark = World->SpawnActor<AChalkMarkActor>(AChalkMarkActor::StaticClass(), SpawnLoc, SpawnRot, SpawnParams);

		if (ChalkDrawSound)
		{
			UGameplayStatics::PlaySoundAtLocation(this, ChalkDrawSound, Hit.ImpactPoint, 1.0f, FMath::RandRange(0.96f, 1.04f));
		}

		UE_LOG(LogREVOLUTION, Log, TEXT("Kabir inscribed tailor's chalk mark on surface at %s. Chalk remaining: %d"), *SpawnLoc.ToString(), ChalkCount);
	}
}

void ARevolutionCharacter::AddPamphlets(int32 Amount)
{
	PamphletCount = FMath::Clamp(PamphletCount + Amount, 0, MaxPamphlets);
	UE_LOG(LogREVOLUTION, Log, TEXT("Kabir collected %d Satyagraha handbills. Total: %d/%d"), Amount, PamphletCount, MaxPamphlets);
}

bool ARevolutionCharacter::DeliverPamphlets(int32 Amount)
{
	if (PamphletCount >= Amount)
	{
		PamphletCount -= Amount;
		UE_LOG(LogREVOLUTION, Log, TEXT("Kabir delivered %d handbills. Remaining: %d/%d"), Amount, PamphletCount, MaxPamphlets);
		return true;
	}
	return false;
}

void ARevolutionCharacter::EnterHidingSpot(AHidingSpotActor* Spot)
{
	if (!Spot) return;

	bIsHidingInCover = true;
	CurrentHidingSpot = Spot;

	StopSprinting();
	if (bIsCrouched)
	{
		UnCrouch();
	}

	GetCharacterMovement()->StopMovementImmediately();
	GetCharacterMovement()->DisableMovement();

	if (Spot->HidingPoint)
	{
		SetActorLocationAndRotation(Spot->HidingPoint->GetComponentLocation(), Spot->HidingPoint->GetComponentRotation());
	}

	GetMesh()->SetVisibility(false);
	GetCapsuleComponent()->SetCollisionResponseToChannel(ECC_Pawn, ECR_Ignore);

	CurrentInteractableActor = Spot;
	OnInteractionFocusChanged.Broadcast(true, Spot->ExitPrompt);

	UE_LOG(LogREVOLUTION, Log, TEXT("Kabir entered concealment cover in %s"), *Spot->SpotName.ToString());
}

void ARevolutionCharacter::ExitHidingSpot()
{
	bIsHidingInCover = false;

	if (CurrentHidingSpot && CurrentHidingSpot->ExitPoint)
	{
		SetActorLocationAndRotation(CurrentHidingSpot->ExitPoint->GetComponentLocation(), CurrentHidingSpot->ExitPoint->GetComponentRotation());
	}

	GetMesh()->SetVisibility(true);
	GetCapsuleComponent()->SetCollisionResponseToChannel(ECC_Pawn, ECR_Block);
	GetCharacterMovement()->SetMovementMode(MOVE_Walking);

	CurrentHidingSpot = nullptr;
	CurrentInteractableActor = nullptr;
	OnInteractionFocusChanged.Broadcast(false, FText::GetEmpty());

	UE_LOG(LogREVOLUTION, Log, TEXT("Kabir re-emerged from concealment."));
}

void ARevolutionCharacter::StartCrawlTraversal(const FVector& StartLocation, const FVector& TargetLocation, float Duration)
{
	if (bIsCrawlTraversing) return;

	bIsCrawlTraversing = true;
	CrawlProgress = 0.0f;
	CurrentCrawlDuration = FMath::Max(Duration, 0.2f);
	CrawlStartLocation = StartLocation;
	CrawlTargetLocation = TargetLocation;

	StopSprinting();
	GetCharacterMovement()->StopMovementImmediately();
	GetCharacterMovement()->DisableMovement();

	// Lower capsule for low conduit clearance
	GetCapsuleComponent()->SetCapsuleHalfHeight(30.0f);
	SetActorLocation(StartLocation, true);

	UE_LOG(LogREVOLUTION, Log, TEXT("Kabir started low drain crawlway traversal from %s to %s"), *StartLocation.ToString(), *TargetLocation.ToString());
}

void ARevolutionCharacter::ToggleSatchelJournal()
{
	bIsSatchelJournalOpen = !bIsSatchelJournalOpen;
	if (bIsSatchelJournalOpen)
	{
		StopSprinting();
		PlayInspectAudio(true); // Plays SFX_Parchment_Open
		UE_LOG(LogREVOLUTION, Log, TEXT("Kabir opened courier satchel and field journal."));
	}
	else
	{
		PlayInspectAudio(false); // Plays SFX_Parchment_Close
		UE_LOG(LogREVOLUTION, Log, TEXT("Kabir closed courier satchel."));
	}
}

void ARevolutionCharacter::SelectSatchelTab(int32 TabIndex)
{
	if (bIsSatchelJournalOpen)
	{
		ActiveSatchelTab = FMath::Clamp(TabIndex, 0, 3);
		PlayInspectAudio(true);
		UE_LOG(LogREVOLUTION, Log, TEXT("Switched satchel journal tab to %d"), ActiveSatchelTab);
	}
}

void ARevolutionCharacter::StartLeanLeft()
{
	bIsLeaningLeft = true;
}

void ARevolutionCharacter::StopLeanLeft()
{
	bIsLeaningLeft = false;
}

void ARevolutionCharacter::StartLeanRight()
{
	if (CurrentInteractableActor != nullptr)
	{
		OnInteract();
		return;
	}
	bIsLeaningRight = true;
}

void ARevolutionCharacter::StopLeanRight()
{
	bIsLeaningRight = false;
}

void ARevolutionCharacter::ToggleKeenSenses()
{
	bIsKeenSensesActive = !bIsKeenSensesActive;
	UE_LOG(LogREVOLUTION, Log, TEXT("Kabir Keen Senses (Basant Intuition): %s"), bIsKeenSensesActive ? TEXT("ACTIVE") : TEXT("INACTIVE"));
}

void ARevolutionCharacter::UpdateEnvironmentalConcealment(float DeltaTime)
{
	float TargetScore = 0.50f;

	// Stance base concealment
	if (bIsCrouched)
	{
		TargetScore += 0.25f; // Crouching provides substantial low-profile shadow cover
	}
	if (bIsHidingInCover)
	{
		TargetScore = 0.95f; // In hiding spots (tandoor, charpai, sacks), Kabir is virtually invisible
	}
	else if (bIsCrowdBlended)
	{
		TargetScore += 0.22f; // Blending with civilians breaks solitary silhouette
	}
	else if (bIsSprinting)
	{
		TargetScore -= 0.35f; // Fast sprinting silhouette is easily caught in ambient light
	}

	// Check illumination from active sentry lanterns
	UWorld* World = GetWorld();
	if (World)
	{
		FVector KabirPos = GetActorLocation() + FVector(0.0f, 0.0f, 40.0f);
		for (TActorIterator<ACurfewPatrolAI> It(World); It; ++It)
		{
			ACurfewPatrolAI* Sentry = *It;
			if (Sentry && Sentry->LanternLight)
			{
				float Dist = FVector::Dist(KabirPos, Sentry->GetActorLocation());
				if (Dist < 850.0f)
				{
					// Check if light is occluded by walls
					FCollisionQueryParams TraceParams(SCENE_QUERY_STAT(ConcealmentTrace), true, this);
					TraceParams.AddIgnoredActor(Sentry);
					FHitResult Hit;
					bool bBlocked = World->LineTraceSingleByChannel(Hit, Sentry->GetActorLocation() + FVector(0.0f, 0.0f, 50.0f), KabirPos, ECC_Visibility, TraceParams);
					if (!bBlocked)
					{
						// In direct line of lantern glow
						float ProximityRatio = 1.0f - (Dist / 850.0f);
						TargetScore -= (0.45f * ProximityRatio);
					}
				}
			}
		}
	}

	TargetScore = FMath::Clamp(TargetScore, 0.05f, 0.98f);
	EnvironmentalConcealmentScore = FMath::FInterpTo(EnvironmentalConcealmentScore, TargetScore, DeltaTime, 4.0f);
}

void ARevolutionCharacter::TriggerSteamObscurity(float Duration)
{
	bIsSteamObscured = true;
	SteamObscurityRemainingTime = FMath::Max(SteamObscurityRemainingTime, Duration);
	UE_LOG(LogREVOLUTION, Log, TEXT("Steam Obscurity Cloak activated for %.1f seconds."), SteamObscurityRemainingTime);
}

void ARevolutionCharacter::SelectNextCodexEntry()
{
	if (!bIsSatchelJournalOpen) return;
	SelectedCodexIndex = (SelectedCodexIndex + 1) % 17;
	PlayInspectAudio(true);
	UE_LOG(LogREVOLUTION, Log, TEXT("Kabir selected codex entry: %d"), SelectedCodexIndex);
}

void ARevolutionCharacter::SelectPrevCodexEntry()
{
	if (!bIsSatchelJournalOpen) return;
	SelectedCodexIndex = (SelectedCodexIndex - 1 + 17) % 17;
	PlayInspectAudio(true);
	UE_LOG(LogREVOLUTION, Log, TEXT("Kabir selected codex entry: %d"), SelectedCodexIndex);
}

void ARevolutionCharacter::AdjustCurrentSetting(float Delta)
{
	switch (SelectedSettingsIndex)
	{
	case 0:
		MasterVolume = FMath::Clamp(MasterVolume + Delta, 0.0f, 1.0f);
		break;
	case 1:
		SFXVolume = FMath::Clamp(SFXVolume + Delta, 0.0f, 1.0f);
		break;
	case 2:
		FoleyVolume = FMath::Clamp(FoleyVolume + Delta, 0.0f, 1.0f);
		break;
	case 3:
		VoiceVolume = FMath::Clamp(VoiceVolume + Delta, 0.0f, 1.0f);
		break;
	case 4:
		AmbienceVolume = FMath::Clamp(AmbienceVolume + Delta, 0.0f, 1.0f);
		break;
	case 5:
		if (Delta > 0.0f)
		{
			if (SubtitleScaleMultiplier < 0.95f) SubtitleScaleMultiplier = 1.0f;
			else if (SubtitleScaleMultiplier < 1.15f) SubtitleScaleMultiplier = 1.25f;
		}
		else
		{
			if (SubtitleScaleMultiplier > 1.15f) SubtitleScaleMultiplier = 1.0f;
			else if (SubtitleScaleMultiplier > 0.95f) SubtitleScaleMultiplier = 0.85f;
		}
		break;
	default:
		break;
	}

	ApplyAudioSettings();
}

void ARevolutionCharacter::SelectNextSetting()
{
	SelectedSettingsIndex = (SelectedSettingsIndex + 1) % 6;
	PlayInspectAudio(true);
}

void ARevolutionCharacter::SelectPrevSetting()
{
	SelectedSettingsIndex = (SelectedSettingsIndex - 1 + 6) % 6;
	PlayInspectAudio(true);
}

void ARevolutionCharacter::SetSubtitleScaleMultiplier(float InScale)
{
	SubtitleScaleMultiplier = FMath::Clamp(InScale, 0.5f, 2.0f);
}

void ARevolutionCharacter::CycleSubtitleScale()
{
	if (SubtitleScaleMultiplier < 0.95f)
	{
		SubtitleScaleMultiplier = 1.0f; // Medium
	}
	else if (SubtitleScaleMultiplier < 1.15f)
	{
		SubtitleScaleMultiplier = 1.25f; // Large
	}
	else
	{
		SubtitleScaleMultiplier = 0.85f; // Small
	}
}

void ARevolutionCharacter::ApplyAudioSettings()
{
	UWorld* World = GetWorld();
	if (!World) return;

	USoundMix* DefaultMix = Cast<USoundMix>(StaticLoadObject(USoundMix::StaticClass(), nullptr, TEXT("/Game/Audio/SoundMixes/SMix_Default.SMix_Default")));
	if (!DefaultMix) return;

	auto SetClassVol = [&](const TCHAR* ClassPath, float Volume)
	{
		USoundClass* SC = Cast<USoundClass>(StaticLoadObject(USoundClass::StaticClass(), nullptr, ClassPath));
		if (SC)
		{
			UGameplayStatics::SetSoundMixClassOverride(World, DefaultMix, SC, Volume, 1.0f, 0.05f, true);
		}
	};

	SetClassVol(TEXT("/Game/Audio/SoundClasses/SC_Master.SC_Master"), MasterVolume);
	SetClassVol(TEXT("/Game/Audio/SoundClasses/SC_SFX.SC_SFX"), SFXVolume);
	SetClassVol(TEXT("/Game/Audio/SoundClasses/SC_Foley.SC_Foley"), FoleyVolume);
	SetClassVol(TEXT("/Game/Audio/SoundClasses/SC_Voice_Punjabi.SC_Voice_Punjabi"), VoiceVolume);
	SetClassVol(TEXT("/Game/Audio/SoundClasses/SC_Ambience_Mohalla.SC_Ambience_Mohalla"), AmbienceVolume);

	UGameplayStatics::PushSoundMixModifier(World, DefaultMix);
}

void ARevolutionCharacter::OnMenuUp()
{
	if (!bIsSatchelJournalOpen) return;
	if (ActiveSatchelTab == 2)
	{
		SelectPrevCodexEntry();
	}
	else if (ActiveSatchelTab == 3)
	{
		SelectPrevSetting();
	}
}

void ARevolutionCharacter::OnMenuDown()
{
	if (!bIsSatchelJournalOpen) return;
	if (ActiveSatchelTab == 2)
	{
		SelectNextCodexEntry();
	}
	else if (ActiveSatchelTab == 3)
	{
		SelectNextSetting();
	}
}

void ARevolutionCharacter::OnMenuLeft()
{
	if (!bIsSatchelJournalOpen) return;
	if (ActiveSatchelTab == 3)
	{
		AdjustCurrentSetting(-0.05f);
	}
}

void ARevolutionCharacter::OnMenuRight()
{
	if (!bIsSatchelJournalOpen) return;
	if (ActiveSatchelTab == 3)
	{
		AdjustCurrentSetting(0.05f);
	}
}

void ARevolutionCharacter::HandleCivilianCollision(ACivilianNPCActor* HitCivilian)
{
	if (!HitCivilian) return;

	const float Speed = GetVelocity().Size();
	if (bIsSprinting || Speed >= 400.0f)
	{
		FVector ImpactDir = GetVelocity().GetSafeNormal();
		if (ImpactDir.IsNearlyZero())
		{
			ImpactDir = GetActorForwardVector();
		}

		HitCivilian->TriggerStumble(ImpactDir, Speed);

		// Non-violent physical resistance: damp sprint velocity upon colliding with an adult pedestrian in crowded bazaar
		if (UCharacterMovementComponent* MoveComp = GetCharacterMovement())
		{
			MoveComp->Velocity *= 0.45f;
		}

		UE_LOG(LogREVOLUTION, Log, TEXT("Kabir collided with civilian %s (Speed: %.1f) - triggered stumble recovery"), *HitCivilian->GetName(), Speed);
	}
}

void ARevolutionCharacter::NotifyHit(UPrimitiveComponent* MyComp, AActor* Other, UPrimitiveComponent* OtherComp, bool bSelfMoved, FVector HitLocation, FVector HitNormal, FVector NormalImpulse, const FHitResult& Hit)
{
	Super::NotifyHit(MyComp, Other, OtherComp, bSelfMoved, HitLocation, HitNormal, NormalImpulse, Hit);

	if (ACivilianNPCActor* HitCivilian = Cast<ACivilianNPCActor>(Other))
	{
		HandleCivilianCollision(HitCivilian);
	}
}





