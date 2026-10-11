// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "InteractableInterface.h"
#include "HandpumpActor.generated.h"

class UStaticMeshComponent;
class USoundBase;
class ARevolutionCharacter;

/**
 * Historical Cast-Iron Courtyard Handpump (Nalka / Lever Pump)
 * Ubiquitous groundwater fixture in early 20th-century Punjabi havelis.
 * Tactical Stealth Gameplay:
 * - Kabir can interact [E] to pump the cast-iron rocker lever.
 * - Produces an authentic mechanical metallic clank and gushing water sound.
 * - Creates a reverberating acoustic distraction within 950cm, luring curfew watchmen
 *   away from doorways and alleys into the courtyard to investigate.
 * - Cooldown prevents repetitive spam while rewarding timed tactical misdirection.
 */
UCLASS()
class REVOLUTION_API AHandpumpActor : public AActor, public IInteractableInterface
{
	GENERATED_BODY()

public:
	AHandpumpActor();

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* SceneRoot;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* BasePedestalMesh;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* CylinderBodyMesh;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* LeverArmMesh;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* WaterSpoutMesh;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Handpump")
	FText PumpName = FText::FromString(TEXT("Cast-Iron Courtyard Handpump (Nalka)"));

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Handpump")
	FText InteractionPrompt = FText::FromString(TEXT("Pump Water (Acoustic Decoy)"));

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Handpump")
	float AcousticAlertRadius = 950.0f; // 9.5 meters acoustic propagation

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Handpump")
	float PumpCooldown = 6.0f; // Seconds before lever can be pumped again

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Handpump")
	bool bIsPumping = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* PumpStrokeSound = nullptr;

	// IInteractableInterface Implementation
	virtual void OnInteract_Implementation(ARevolutionCharacter* Interactor) override;
	virtual FText GetInteractionPrompt_Implementation() const override;
	virtual bool CanInteract_Implementation(const ARevolutionCharacter* Interactor) const override;

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

private:
	float LastPumpTime = -10.0f;
	float LeverAnimationProgress = 0.0f;
	FRotator RestLeverRotation;
	FRotator DepressedLeverRotation;
};
