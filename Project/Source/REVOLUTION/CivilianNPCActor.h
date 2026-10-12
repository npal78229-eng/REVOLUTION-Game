// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "InteractableInterface.h"
#include "CivilianNPCActor.generated.h"

class USphereComponent;
class UStaticMeshComponent;
class ARevolutionCharacter;

UENUM(BlueprintType)
enum class ECivilianOccupation : uint8
{
	FatherTailor UMETA(DisplayName = "Ram Lubhaya (Master Tailor / Kabir's Father)"),
	HalwaiChaiVendor UMETA(DisplayName = "Hira Halwai (Tea & Jalebi Vendor)"),
	BhishtiWaterCarrier UMETA(DisplayName = "Ghasita Bhishti (Traditional Water-Carrier)"),
	SchoolHeadmaster UMETA(DisplayName = "Pandit Kashi Ram (Vernacular School Headmaster)"),
	ClothMerchant UMETA(DisplayName = "Lala Karam Chand (Textile Merchant)"),
	SchoolFriendKartar UMETA(DisplayName = "Kartar Singh (Schoolmate & Friend)")
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

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Dialogue")
	int32 CurrentDialogueIndex = 0;

	UPROPERTY(BlueprintAssignable, Category = "Revolution|Dialogue")
	FOnCivilianDialogueSpoken OnDialogueSpoken;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Dialogue")
	float ProximityBarkCooldown = 15.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Mission")
	bool bCanAdvanceMission = true;

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
	FRotator DefaultRotation;
	bool bPlayerInProximity = false;
	TWeakObjectPtr<ARevolutionCharacter> NearbyPlayer;

	UFUNCTION()
	void OnProximityBeginOverlap(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);

	UFUNCTION()
	void OnProximityEndOverlap(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex);
};
