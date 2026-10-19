// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "InteractableInterface.h"
#include "RevolutionMissionSubsystem.h"
#include "CivilianNPCActor.generated.h"

class USphereComponent;
class UStaticMeshComponent;
class ARevolutionCharacter;
class USoundBase;
class USoundAttenuation;

UENUM(BlueprintType)
enum class ECivilianOccupation : uint8
{
	FatherTailor UMETA(DisplayName = "Ram Lubhaya (Master Tailor / Kabir's Father)"),
	HalwaiChaiVendor UMETA(DisplayName = "Hira Halwai (Tea & Jalebi Vendor)"),
	BhishtiWaterCarrier UMETA(DisplayName = "Ghasita Bhishti (Traditional Water-Carrier)"),
	SchoolHeadmaster UMETA(DisplayName = "Pandit Kashi Ram (Vernacular School Headmaster)"),
	ClothMerchant UMETA(DisplayName = "Lala Karam Chand (Textile Merchant)"),
	SchoolFriendKartar UMETA(DisplayName = "Kartar Singh (Schoolmate & Friend)"),
	MunadiTownCrier UMETA(DisplayName = "Nikka Ram (Town Crier / Munadi Drummer)"),
	ProtestElder UMETA(DisplayName = "Bhai Sant Singh (Community Elder / Mohalla Elder)")
};

UENUM(BlueprintType)
enum class ECivilianReactionState : uint8
{
	Idle UMETA(DisplayName = "Idle / Working"),
	FacingPlayer UMETA(DisplayName = "Facing Player"),
	Stumbling UMETA(DisplayName = "Stumbling / Balance Recovery"),
	CuriousInvestigating UMETA(DisplayName = "Curious / Investigating Noise")
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnCivilianDialogueSpoken, ACivilianNPCActor*, NPC, const FText&, SpeakerName, const FText&, DialogueText);

/**
 * Historical Punjabi Civilian NPC (Mohalla Resident / Artisan / Family / Vendor)
 * Populates Kot Gurdarshan with grounded, culturally researched characters of April 1919.
 * Features:
 * - 5 authentic historical archetypes with unique lore, perspectives, and visual props
 * - Proximity awareness: turns to face Kabir naturally when approached
 * - Ambient period barks in English with authentic Punjabi/Urdu terms
 * - Direct interactive multi-stage conversation (via IInteractableInterface)
 * - Integration with Kabir's Satchel Journal & Inspection Modal
 */
UCLASS()
class REVOLUTION_API ACivilianNPCActor : public ACharacter, public IInteractableInterface
{
	GENERATED_BODY()

public:
	ACivilianNPCActor();

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

public:
	// --- COMPONENTS ---
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USphereComponent* ProximitySphere;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* PropAccessoryMesh;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* TurbanMesh;

	// --- OCCUPATION & IDENTITY ---
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Civilian")
	ECivilianOccupation Occupation = ECivilianOccupation::FatherTailor;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Civilian")
	FText CivilianName;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Civilian")
	FText ProfessionTitle;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Civilian", meta = (MultiLine = true))
	FText HistoricalLore;

	// --- DIALOGUE & INTERACTION ---
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Dialogue")
	TArray<FText> AmbientBarks;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Dialogue")
	TArray<FText> ConversationDialogues;

	// --- TASK 36: ACT II CRISIS DIALOGUES & BARKS ---
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Dialogue")
	TArray<FText> ActIIBarks;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Dialogue")
	TArray<FText> ActIIDialogues;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Dialogue")
	bool bIsInActIIMode = false;

	UFUNCTION(BlueprintCallable, Category = "Revolution|Dialogue")
	void SetDialogueModeForStage(ECourierMissionStage NewStage);

	UFUNCTION(BlueprintCallable, Category = "Revolution|Dialogue")
	void HandleMissionDirectiveChanged(ECourierMissionStage NewStage, FText Title, FText Directive);

	UFUNCTION(BlueprintPure, Category = "Revolution|Dialogue")
	bool IsInActIIMode() const { return bIsInActIIMode; }

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Dialogue")
	int32 CurrentDialogueIndex = 0;

	UPROPERTY(BlueprintAssignable, Category = "Revolution|Dialogue")
	FOnCivilianDialogueSpoken OnDialogueSpoken;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Dialogue")
	float ProximityBarkCooldown = 15.0f;

	// --- AUDIO & VOICE LOCALIZATION ---
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* InteractionVoiceSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* AmbientBarkVoiceSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundAttenuation* VoiceAttenuation = nullptr;

	// --- DYNAMIC PEDESTRIAN REACTION & STUMBLE SYSTEM (TASK 22) ---
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Reaction")
	ECivilianReactionState ReactionState = ECivilianReactionState::Idle;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Reaction")
	bool bIsStumbled = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Reaction")
	float StumbleDuration = 1.25f;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Reaction")
	float StumbleTimer = 0.0f;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Reaction")
	FVector StumbleDirection = FVector::ZeroVector;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Reaction")
	float StumbleIntensity = 0.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Reaction")
	float StumbleCooldown = 1.5f;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Reaction")
	FVector CuriosityLookTarget = FVector::ZeroVector;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Reaction")
	float CuriosityTimer = 0.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Reaction")
	float CuriosityDuration = 3.5f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Reaction")
	float CuriosityHearingRadius = 750.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Reaction")
	float CuriosityCooldown = 5.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Dialogue")
	TArray<FText> StumbleBarks;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Dialogue")
	TArray<FText> CuriosityBarks;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* StumbleVoiceSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* CuriosityVoiceSound = nullptr;

	UFUNCTION(BlueprintCallable, Category = "Revolution|Reaction")
	void TriggerStumble(const FVector& ImpactDirection, float ImpactForce);

	UFUNCTION(BlueprintCallable, Category = "Revolution|Reaction")
	void InvestigateCuriosity(const FVector& NoiseLocation);

	UFUNCTION(BlueprintPure, Category = "Revolution|Reaction")
	ECivilianReactionState GetReactionState() const { return ReactionState; }

	UFUNCTION(BlueprintPure, Category = "Revolution|Reaction")
	bool IsStumbling() const { return bIsStumbled; }

	UFUNCTION(BlueprintPure, Category = "Revolution|Reaction")
	bool IsCuriousInvestigating() const { return ReactionState == ECivilianReactionState::CuriousInvestigating; }

	virtual void NotifyHit(UPrimitiveComponent* MyComp, AActor* Other, UPrimitiveComponent* OtherComp, bool bSelfMoved, FVector HitLocation, FVector HitNormal, FVector NormalImpulse, const FHitResult& Hit) override;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Mission")
	bool bCanAdvanceMission = true;

	// --- TASK 31: SKELETAL IDLE ANIMATIONS & ROUTINE LIFE SYSTEM ---
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Animation")
	bool bEnableRoutineAnimations = true;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Animation")
	float RoutineCycleTime = 0.0f;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Animation")
	float BreathingCycleTime = 0.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Animation")
	float IdleBreathingRate = 0.25f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Animation")
	float IdleBreathingAmplitude = 1.25f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* OccupationRoutineSound = nullptr;

	UPROPERTY(Transient, BlueprintReadOnly, Category = "Revolution|Audio")
	class UAudioComponent* RoutineAudioComp = nullptr;

	UFUNCTION(BlueprintPure, Category = "Revolution|Animation")
	bool IsRoutineAnimationActive() const { return bEnableRoutineAnimations; }

	UFUNCTION(BlueprintPure, Category = "Revolution|Animation")
	float GetRoutineCycleTime() const { return RoutineCycleTime; }

	UFUNCTION(BlueprintCallable, Category = "Revolution|Animation")
	void SetRoutineAnimationsEnabled(bool bEnabled);

	UFUNCTION(BlueprintCallable, Category = "Revolution|Animation")
	void SimulateRoutineTick(float DeltaTime) { Tick(DeltaTime); }

	UFUNCTION(BlueprintCallable, Category = "Revolution|Civilian")
	void ApplyHeritageAttireMaterials();

	// IInteractableInterface Implementation
	virtual void OnInteract_Implementation(ARevolutionCharacter* Interactor) override;
	virtual FText GetInteractionPrompt_Implementation() const override;
	virtual bool CanInteract_Implementation(const ARevolutionCharacter* Interactor) const override;

	/** Configures archetype defaults (names, lore, dialogues, and accessories) */
	UFUNCTION(BlueprintCallable, Category = "Revolution|Civilian")
	void ConfigureOccupation(ECivilianOccupation NewOccupation);

	/** Cycles to the next conversation dialogue line */
	UFUNCTION(BlueprintCallable, Category = "Revolution|Dialogue")
	FText AdvanceConversation();

	UFUNCTION(BlueprintPure, Category = "Revolution|Dialogue")
	FText GetCurrentDialogue() const;

private:
	float LastBarkTime = -100.0f;
	float LastStumbleTime = -100.0f;
	float LastCuriosityTime = -100.0f;
	FRotator DefaultRotation;
	bool bPlayerInProximity = false;
	TWeakObjectPtr<ARevolutionCharacter> NearbyPlayer;
	FVector MeshInitialRelativeLocation;
	FRotator MeshInitialRelativeRotation;
	FVector PropInitialRelativeLocation;
	FRotator PropInitialRelativeRotation;

	UFUNCTION()
	void OnProximityBeginOverlap(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);

	UFUNCTION()
	void OnProximityEndOverlap(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex);
};
