// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "InteractableInterface.h"
#include "PersianWheelActor.generated.h"

class USceneComponent;
class UStaticMeshComponent;
class USphereComponent;
class USoundBase;
class ARevolutionCharacter;

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnFlumeCleared, FName, ClusterID);

/**
 * Historical Punjabi Persian Wheel (Rahat) Flume Irrigation Mechanism at the Upper Bari Doab Canal (UBDC).
 * Provides a manual labor restitution / basti solidarity mechanic for Kabir:
 * Clearing the jammed timber sluice gate and turning the draught timber arm restores water flow
 * to Kumhar Rahim's terracotta clay pits, granting +35 Vishwas to Cluster_UBDC_CanalBasti
 * and restoring community standing without needing copper coin payments.
 */
UCLASS()
class REVOLUTION_API APersianWheelActor : public AActor, public IInteractableInterface
{
	GENERATED_BODY()

public:
	APersianWheelActor();

protected:
	virtual void BeginPlay() override;

public:
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* SceneRoot;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* WheelMesh;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USphereComponent* InteractionTrigger;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|CommunityTrust")
	FName CommunityClusterID = FName(TEXT("Cluster_UBDC_CanalBasti"));

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|CommunityTrust")
	int32 LaborTrustBonus = 35;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Flume")
	bool bFlumeCleared = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Flume")
	FText LaborPrompt;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Flume")
	FText ClearedPrompt;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* WheelCreakSound;

	UPROPERTY(BlueprintAssignable, Category = "Revolution|Flume")
	FOnFlumeCleared OnFlumeCleared;

	// IInteractableInterface
	virtual void OnInteract_Implementation(ARevolutionCharacter* Interactor) override;
	virtual FText GetInteractionPrompt_Implementation() const override;
	virtual bool CanInteract_Implementation(const ARevolutionCharacter* Interactor) const override;

	UFUNCTION(BlueprintCallable, Category = "Revolution|Flume")
	void ResetFlumeState();

	UFUNCTION(BlueprintPure, Category = "Revolution|Flume")
	bool IsFlumeCleared() const { return bFlumeCleared; }

	UFUNCTION(BlueprintPure, Category = "Revolution|CommunityTrust")
	class UCommunityTrustSubsystem* GetCommunityTrustSubsystem() const;
};
