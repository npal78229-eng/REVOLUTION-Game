// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "Logging/LogMacros.h"
#include "RevolutionCharacter.generated.h"

class USpringArmComponent;
class UCameraComponent;
class UInputMappingContext;
class UInputAction;
class USoundBase;
class AHidingSpotActor;
struct FInputActionValue;

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnInteractionFocusChanged, bool, bHasFocus, FText, PromptText);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnItemInspected, FText, ItemName, FText, LoreDescription);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnInspectionEnded);

UCLASS(config=Game)
class REVOLUTION_API ARevolutionCharacter : public ACharacter
{
	GENERATED_BODY()

	/** Camera boom positioning the camera behind the character */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera", meta = (AllowPrivateAccess = "true"))
	USpringArmComponent* CameraBoom;

	/** Follow camera */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera", meta = (AllowPrivateAccess = "true"))
	UCameraComponent* FollowCamera;
	
	/** MappingContext for default gameplay */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Input", meta = (AllowPrivateAccess = "true"))
	UInputMappingContext* DefaultMappingContext;

	/** Move Input Action */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Input", meta = (AllowPrivateAccess = "true"))
	UInputAction* MoveAction;

	/** Look Input Action */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Input", meta = (AllowPrivateAccess = "true"))
	UInputAction* LookAction;

	/** Jump Input Action */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Input", meta = (AllowPrivateAccess = "true"))
	UInputAction* JumpAction;

	/** Sprint Input Action */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Input", meta = (AllowPrivateAccess = "true"))
	UInputAction* SprintAction;

	/** Crouch Input Action */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Input", meta = (AllowPrivateAccess = "true"))
	UInputAction* CrouchAction;

	/** Interact Input Action */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Input", meta = (AllowPrivateAccess = "true"))
	UInputAction* InteractAction;

public:
	ARevolutionCharacter();

protected:
	virtual void BeginPlay() override;
	virtual void PossessedBy(AController* NewController) override;
	virtual void Tick(float DeltaTime) override;

	/** Called for movement input */
	void Move(const FInputActionValue& Value);

	/** Called for looking input */
	void Look(const FInputActionValue& Value);

	/** Direct axis and action bindings for guaranteed zero-dependency input */
	void MoveForwardAxis(float Value);
	void MoveRightAxis(float Value);
	void TurnAxis(float Value);
	void LookUpAxis(float Value);

	/** Jump or vault */
	void OnJumpPressed();
	void OnJumpReleased();

	/** Sprint start / stop */
	void StartSprinting();
	void StopSprinting();

	/** Crouch toggle */
	void ToggleCrouch();

	/** Interact attempt */
	void OnInteract();

	virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

public:
	/** Returns CameraBoom subobject **/
	FORCEINLINE class USpringArmComponent* GetCameraBoom() const { return CameraBoom; }
	/** Returns FollowCamera subobject **/
	FORCEINLINE class UCameraComponent* GetFollowCamera() const { return FollowCamera; }

	// --- LOCOMOTION & STAMINA PARAMETERS (12-Year-Old Kabir) ---
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Locomotion")
	float WalkSpeed = 380.0f; // 3.8 km/h

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Locomotion")
	float SprintSpeed = 720.0f; // 7.2 km/h sprint

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Stamina")
	float MaxStamina = 100.0f;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Stamina")
	float CurrentStamina = 100.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Stamina")
	float StaminaDrainRate = 18.0f; // Drain per second

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Stamina")
	float StaminaRegenRate = 22.0f; // Recovery per second

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Locomotion")
	bool bIsSprinting = false;

	// --- VAULTING TRAVERSAL SYSTEM (1.1m Parapets & Obstacles) ---
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Traversal")
	bool bIsVaulting = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Traversal")
	float VaultDuration = 0.35f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Traversal")
	float VaultArcPeak = 25.0f;

	/** Detects whether an obstacle in front is within vaulting height range (50cm - 125cm) */
	UFUNCTION(BlueprintCallable, Category = "Revolution|Traversal")
	bool DetectVaultableObstacle(FVector& OutVaultLocation);

	/** Executes vault traversal over detected obstacle */
	UFUNCTION(BlueprintCallable, Category = "Revolution|Traversal")
	void TryVaultOrJump();

	// --- LOW DRAIN CRAWLWAY TRAVERSAL SYSTEM (80cm Conduits & Foundation Breaches) ---
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Traversal")
	bool bIsCrawlTraversing = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Traversal")
	float CrawlTraversalDuration = 1.6f;

	UFUNCTION(BlueprintCallable, Category = "Revolution|Traversal")
	void StartCrawlTraversal(const FVector& StartLocation, const FVector& TargetLocation, float Duration);

	UFUNCTION(BlueprintPure, Category = "Revolution|Traversal")
	bool IsCrawlTraversing() const { return bIsCrawlTraversing; }

	// --- INTERACTION & INSPECTION SYSTEM ---
	UPROPERTY(BlueprintAssignable, Category = "Revolution|Interaction")
	FOnInteractionFocusChanged OnInteractionFocusChanged;

	UPROPERTY(BlueprintAssignable, Category = "Revolution|Interaction")
	FOnItemInspected OnItemInspected;

	UPROPERTY(BlueprintAssignable, Category = "Revolution|Interaction")
	FOnInspectionEnded OnInspectionEnded;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Interaction")
	AActor* CurrentInteractableActor = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Interaction")
	float InteractionTraceDistance = 180.0f;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Interaction")
	bool bIsInspecting = false;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Interaction")
	FText InspectedItemName;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Interaction")
	FText InspectedItemLore;

	UFUNCTION(BlueprintCallable, Category = "Revolution|Interaction")
	void StartInspection(const FText& InItemName, const FText& InLoreDescription);

	UFUNCTION(BlueprintCallable, Category = "Revolution|Interaction")
	void EndInspection();

	UFUNCTION(BlueprintPure, Category = "Revolution|Interaction")
	bool IsInspecting() const { return bIsInspecting; }

	UFUNCTION(BlueprintPure, Category = "Revolution|Interaction")
	FText GetInspectedItemName() const { return InspectedItemName; }

	UFUNCTION(BlueprintPure, Category = "Revolution|Interaction")
	FText GetInspectedItemLore() const { return InspectedItemLore; }

	void CheckForInteractables();

	// --- AUDIO & HISTORICAL FOLEY ---
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* FootstepBrickSound01 = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* FootstepBrickSound02 = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* FootstepWoodSound01 = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* FootstepWoodSound02 = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* VaultSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* InspectOpenSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* InspectCloseSound = nullptr;

	UFUNCTION(BlueprintCallable, Category = "Revolution|Audio")
	void PlayFootstepAudio();

	UFUNCTION(BlueprintCallable, Category = "Revolution|Audio")
	void PlayVaultAudio();

	UFUNCTION(BlueprintCallable, Category = "Revolution|Audio")
	void PlayInspectAudio(bool bOpen);

	// --- STEALTH DISTRACTION SYSTEM (Clay Marbles / Pebbles) ---
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Stealth")
	int32 PebbleCount = 5;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Stealth")
	int32 MaxPebbles = 8;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* PebbleThrowSound = nullptr;

	UFUNCTION(BlueprintCallable, Category = "Revolution|Stealth")
	void ThrowPebble();

	UFUNCTION(BlueprintPure, Category = "Revolution|Stealth")
	int32 GetPebbleCount() const { return PebbleCount; }

	// --- TAILOR'S CHALK SCOUT MARKING SYSTEM ---
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Stealth")
	int32 ChalkCount = 8;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Stealth")
	int32 MaxChalk = 10;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* ChalkDrawSound = nullptr;

	UFUNCTION(BlueprintCallable, Category = "Revolution|Stealth")
	void DrawChalkMark();

	UFUNCTION(BlueprintPure, Category = "Revolution|Stealth")
	int32 GetChalkCount() const { return ChalkCount; }

	// --- CONCEALMENT & HIDING SPOT SYSTEM ---
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Concealment")
	bool bIsHidingInCover = false;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Concealment")
	AHidingSpotActor* CurrentHidingSpot = nullptr;

	UFUNCTION(BlueprintCallable, Category = "Revolution|Concealment")
	void EnterHidingSpot(AHidingSpotActor* Spot);

	UFUNCTION(BlueprintCallable, Category = "Revolution|Concealment")
	void ExitHidingSpot();

	UFUNCTION(BlueprintPure, Category = "Revolution|Concealment")
	bool IsHidingInCover() const { return bIsHidingInCover; }

	// --- COURIER SATCHEL & FIELD JOURNAL SYSTEM ---
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Satchel")
	bool bIsSatchelJournalOpen = false;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Satchel")
	int32 ActiveSatchelTab = 0; // 0 = Satchel Equipment, 1 = Mohalla Map, 2 = Dispatches & Lore

	UFUNCTION(BlueprintCallable, Category = "Revolution|Satchel")
	void ToggleSatchelJournal();

	UFUNCTION(BlueprintCallable, Category = "Revolution|Satchel")
	void SelectSatchelTab(int32 TabIndex);

	UFUNCTION(BlueprintCallable, Category = "Revolution|Satchel")
	void SelectSatchelTab1() { SelectSatchelTab(0); }

	UFUNCTION(BlueprintCallable, Category = "Revolution|Satchel")
	void SelectSatchelTab2() { SelectSatchelTab(1); }

	UFUNCTION(BlueprintCallable, Category = "Revolution|Satchel")
	void SelectSatchelTab3() { SelectSatchelTab(2); }

	UFUNCTION(BlueprintPure, Category = "Revolution|Satchel")
	bool IsSatchelJournalOpen() const { return bIsSatchelJournalOpen; }

	UFUNCTION(BlueprintPure, Category = "Revolution|Satchel")
	int32 GetActiveSatchelTab() const { return ActiveSatchelTab; }

private:
	FVector VaultStartLocation;
	FVector VaultTargetLocation;
	float VaultProgress = 0.0f;

	FVector CrawlStartLocation;
	FVector CrawlTargetLocation;
	float CrawlProgress = 0.0f;
	float CurrentCrawlDuration = 1.6f;

	float FootstepDistanceAccumulator = 0.0f;
	bool bFootstepAlternate = false;
};
