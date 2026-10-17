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
	virtual void PawnClientRestart() override;
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

	/** Gamepad specific axis handlers with active input tracking */
	void GamepadMoveForwardAxis(float Value);
	void GamepadMoveRightAxis(float Value);
	void GamepadTurnAxis(float Value);
	void GamepadLookUpAxis(float Value);

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

	// --- HIGH MANTLE TRAVERSAL SYSTEM (1.25m - 2.15m Haveli Walls, Ledges & Platforms) ---
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Traversal")
	bool bIsMantling = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Traversal")
	float MantleDuration = 0.55f;

	UFUNCTION(BlueprintPure, Category = "Revolution|Traversal")
	bool IsMantling() const { return bIsMantling; }

	/** Detects whether an obstacle in front is within high mantle range (125cm - 215cm) */
	UFUNCTION(BlueprintCallable, Category = "Revolution|Traversal")
	bool DetectMantleableLedge(FVector& OutMantleLocation);

	/** Executes vault or high mantle traversal over detected obstacle */
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

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Stealth")
	bool bIsAimingPebble = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* PebbleThrowSound = nullptr;

	UFUNCTION(BlueprintCallable, Category = "Revolution|Stealth")
	void StartAimingPebble();

	UFUNCTION(BlueprintCallable, Category = "Revolution|Stealth")
	void StopAimingPebble();

	UFUNCTION(BlueprintPure, Category = "Revolution|Stealth")
	bool IsAimingPebble() const { return bIsAimingPebble; }

	UFUNCTION(BlueprintCallable, Category = "Revolution|Stealth")
	bool CalculatePebbleTrajectory(TArray<FVector>& OutPathPoints, FVector& OutHitLocation, bool& bOutHitValid) const;

	UFUNCTION(BlueprintCallable, Category = "Revolution|Stealth")
	void ThrowPebble();

	UFUNCTION(BlueprintPure, Category = "Revolution|Stealth")
	int32 GetPebbleCount() const { return PebbleCount; }

	// --- SOCIAL STEALTH & CROWD BLENDING (Assassin's Creed / Hitman) ---
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Stealth")
	bool bIsCrowdBlended = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Stealth")
	float CrowdBlendRadius = 320.0f;

	UFUNCTION(BlueprintPure, Category = "Revolution|Stealth")
	bool IsCrowdBlended() const { return bIsCrowdBlended; }

	void UpdateCrowdBlending(float DeltaTime);

	// --- AAA BENCHMARK: CORNER PEEKING & LEAN MECHANIC (Dishonored / The Last of Us) ---
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Stealth")
	float LeanOffset = 0.0f; // -1.0 (Left) to +1.0 (Right)

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Stealth")
	bool bIsLeaningLeft = false;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Stealth")
	bool bIsLeaningRight = false;

	UFUNCTION(BlueprintCallable, Category = "Revolution|Stealth")
	void StartLeanLeft();

	UFUNCTION(BlueprintCallable, Category = "Revolution|Stealth")
	void StopLeanLeft();

	UFUNCTION(BlueprintCallable, Category = "Revolution|Stealth")
	void StartLeanRight();

	UFUNCTION(BlueprintCallable, Category = "Revolution|Stealth")
	void StopLeanRight();

	UFUNCTION(BlueprintPure, Category = "Revolution|Stealth")
	bool IsCornerLeaning() const { return FMath::Abs(LeanOffset) > 0.15f; }

	UFUNCTION(BlueprintPure, Category = "Revolution|Stealth")
	float GetLeanOffset() const { return LeanOffset; }

	// --- AAA BENCHMARK: ENVIRONMENTAL CONCEALMENT & SHADOW METER (Thief / Splinter Cell) ---
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Stealth")
	float EnvironmentalConcealmentScore = 0.5f; // 0.0 = fully exposed, 1.0 = deep shadow/concealed

	UFUNCTION(BlueprintPure, Category = "Revolution|Stealth")
	float GetConcealmentScore() const { return EnvironmentalConcealmentScore; }

	void UpdateEnvironmentalConcealment(float DeltaTime);

	// --- AAA BENCHMARK: LOCOMOTIVE BOILER STEAM OBSCURITY (Hitman / Batman Arkham) ---
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Stealth")
	bool bIsSteamObscured = false;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Stealth")
	float SteamObscurityRemainingTime = 0.0f;

	UFUNCTION(BlueprintCallable, Category = "Revolution|Stealth")
	void TriggerSteamObscurity(float Duration);

	UFUNCTION(BlueprintPure, Category = "Revolution|Stealth")
	bool IsSteamObscured() const { return bIsSteamObscured; }

	UFUNCTION(BlueprintPure, Category = "Revolution|Stealth")
	float GetSteamObscurityRemainingTime() const { return SteamObscurityRemainingTime; }

	// --- AAA BENCHMARK: KEEN SENSES / BASANT INTUITION (Assassin's Creed / Hitman) ---
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Stealth")
	bool bIsKeenSensesActive = false;

	UFUNCTION(BlueprintCallable, Category = "Revolution|Stealth")
	void ToggleKeenSenses();

	UFUNCTION(BlueprintPure, Category = "Revolution|Stealth")
	bool IsKeenSensesActive() const { return bIsKeenSensesActive; }

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

	// --- UNDERGROUND SATYAGRAHA PAMPHLETS SYSTEM ---
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Stealth")
	int32 PamphletCount = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Stealth")
	int32 MaxPamphlets = 5;

	UFUNCTION(BlueprintPure, Category = "Revolution|Stealth")
	int32 GetPamphletCount() const { return PamphletCount; }

	UFUNCTION(BlueprintCallable, Category = "Revolution|Stealth")
	void AddPamphlets(int32 Amount);

	UFUNCTION(BlueprintCallable, Category = "Revolution|Stealth")
	bool DeliverPamphlets(int32 Amount);

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
	int32 ActiveSatchelTab = 0; // 0 = Satchel Equipment, 1 = Mohalla Map, 2 = Historical Codex, 3 = Settings & Controls

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

	UFUNCTION(BlueprintCallable, Category = "Revolution|Satchel")
	void SelectSatchelTab4() { SelectSatchelTab(3); }

	UFUNCTION(BlueprintPure, Category = "Revolution|Satchel")
	bool IsSatchelJournalOpen() const { return bIsSatchelJournalOpen; }

	UFUNCTION(BlueprintPure, Category = "Revolution|Satchel")
	int32 GetActiveSatchelTab() const { return ActiveSatchelTab; }

	// --- HISTORICAL CODEX ARCHIVAL NAVIGATION ---
	UPROPERTY(VisibleAnywhere, BlueprintReadWrite, Category = "Revolution|Satchel")
	int32 SelectedCodexIndex = 0;

	UFUNCTION(BlueprintCallable, Category = "Revolution|Satchel")
	void SelectNextCodexEntry();

	UFUNCTION(BlueprintCallable, Category = "Revolution|Satchel")
	void SelectPrevCodexEntry();

	// --- QUALITY-OF-LIFE, ACCESSIBILITY & AUDIO SETTINGS ---
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Settings")
	float SubtitleScaleMultiplier = 1.0f; // 0.85 = Small, 1.0 = Medium, 1.25 = Large

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Settings")
	float MasterVolume = 1.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Settings")
	float SFXVolume = 1.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Settings")
	float FoleyVolume = 1.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Settings")
	float VoiceVolume = 1.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Settings")
	float AmbienceVolume = 1.0f;

	UPROPERTY(VisibleAnywhere, BlueprintReadWrite, Category = "Revolution|Settings")
	int32 SelectedSettingsIndex = 0; // 0=Master, 1=SFX, 2=Foley, 3=Voice, 4=Ambience, 5=SubtitleSize, 6=HandheldSteamOS

	// --- STEAMOS & HANDHELD PROTON SCALABILITY PROFILE (TASK 23) ---
	UPROPERTY(VisibleAnywhere, BlueprintReadWrite, Category = "Revolution|Input")
	bool bIsUsingGamepad = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Settings")
	bool bHandheldSteamOSMode = false;

	UFUNCTION(BlueprintPure, Category = "Revolution|Input")
	bool IsUsingGamepad() const { return bIsUsingGamepad; }

	UFUNCTION(BlueprintCallable, Category = "Revolution|Input")
	void SetUsingGamepad(bool bInUsingGamepad) { bIsUsingGamepad = bInUsingGamepad; }

	UFUNCTION(BlueprintPure, Category = "Revolution|Settings")
	bool IsHandheldModeEnabled() const { return bHandheldSteamOSMode; }

	UFUNCTION(BlueprintCallable, Category = "Revolution|Settings")
	void ToggleHandheldMode();

	UFUNCTION(BlueprintCallable, Category = "Revolution|Settings")
	void ApplyHandheldScalability(bool bEnable);

	UFUNCTION(BlueprintCallable, Category = "Revolution|Settings")
	void AdjustCurrentSetting(float Delta);

	UFUNCTION(BlueprintCallable, Category = "Revolution|Settings")
	void SelectNextSetting();

	UFUNCTION(BlueprintCallable, Category = "Revolution|Settings")
	void SelectPrevSetting();

	UFUNCTION(BlueprintCallable, Category = "Revolution|Settings")
	void SetSubtitleScaleMultiplier(float InScale);

	UFUNCTION(BlueprintCallable, Category = "Revolution|Settings")
	void CycleSubtitleScale();

	UFUNCTION(BlueprintPure, Category = "Revolution|Settings")
	float GetSubtitleScaleMultiplier() const { return SubtitleScaleMultiplier; }

	UFUNCTION(BlueprintCallable, Category = "Revolution|Settings")
	void ApplyAudioSettings();

	UFUNCTION(BlueprintCallable, Category = "Revolution|Satchel")
	void OnMenuUp();

	UFUNCTION(BlueprintCallable, Category = "Revolution|Satchel")
	void OnMenuDown();

	UFUNCTION(BlueprintCallable, Category = "Revolution|Satchel")
	void OnMenuLeft();

	UFUNCTION(BlueprintCallable, Category = "Revolution|Satchel")
	void OnMenuRight();

	// --- PEDESTRIAN CROWD COLLISION & STUMBLE REACTION (TASK 22) ---
	UFUNCTION(BlueprintCallable, Category = "Revolution|Locomotion")
	void HandleCivilianCollision(class ACivilianNPCActor* HitCivilian);

	virtual void NotifyHit(UPrimitiveComponent* MyComp, AActor* Other, UPrimitiveComponent* OtherComp, bool bSelfMoved, FVector HitLocation, FVector HitNormal, FVector NormalImpulse, const FHitResult& Hit) override;

private:
	FVector VaultStartLocation;
	FVector VaultTargetLocation;
	float VaultProgress = 0.0f;

	FVector MantleStartLocation;
	FVector MantleTargetLocation;
	float MantleProgress = 0.0f;

	FVector CrawlStartLocation;
	FVector CrawlTargetLocation;
	float CrawlProgress = 0.0f;
	float CurrentCrawlDuration = 1.6f;

	float FootstepDistanceAccumulator = 0.0f;
	bool bFootstepAlternate = false;
};
