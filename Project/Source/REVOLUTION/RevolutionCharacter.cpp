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
}

void ARevolutionCharacter::BeginPlay()
{
	Super::BeginPlay();

	// Add input mapping context to Enhanced Input Subsystem
	if (APlayerController* PlayerController = Cast<APlayerController>(Controller))
	{
		if (UEnhancedInputLocalPlayerSubsystem* Subsystem = ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(PlayerController->GetLocalPlayer()))
		{
			if (DefaultMappingContext)
			{
				Subsystem->AddMappingContext(DefaultMappingContext, 0);
			}
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

	CheckForInteractables();
}

void ARevolutionCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);

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
	PlayerInputComponent->BindAxisKey(EKeys::MouseX, this, &ARevolutionCharacter::TurnAxis);
	PlayerInputComponent->BindAxisKey(EKeys::MouseY, this, &ARevolutionCharacter::LookUpAxis);

	PlayerInputComponent->BindKey(EKeys::SpaceBar, IE_Pressed, this, &ARevolutionCharacter::OnJumpPressed);
	PlayerInputComponent->BindKey(EKeys::SpaceBar, IE_Released, this, &ARevolutionCharacter::OnJumpReleased);

	PlayerInputComponent->BindKey(EKeys::LeftShift, IE_Pressed, this, &ARevolutionCharacter::StartSprinting);
	PlayerInputComponent->BindKey(EKeys::LeftShift, IE_Released, this, &ARevolutionCharacter::StopSprinting);

	PlayerInputComponent->BindKey(EKeys::C, IE_Pressed, this, &ARevolutionCharacter::ToggleCrouch);
	PlayerInputComponent->BindKey(EKeys::E, IE_Pressed, this, &ARevolutionCharacter::OnInteract);
}

void ARevolutionCharacter::Move(const FInputActionValue& Value)
{
	if (bIsVaulting || bIsInspecting) return;

	FVector2D MovementVector = Value.Get<FVector2D>();

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
	if (bIsVaulting || bIsInspecting || FMath::IsNearlyZero(Value)) return;

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
	if (bIsVaulting || bIsInspecting || FMath::IsNearlyZero(Value)) return;

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
	if (bIsInspecting)
	{
		EndInspection();
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
	if (bIsVaulting) return;

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
	if (bIsInspecting)
	{
		EndInspection();
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
	if (bIsInspecting)
	{
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
