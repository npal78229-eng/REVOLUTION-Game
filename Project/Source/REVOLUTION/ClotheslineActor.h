// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "ClotheslineActor.generated.h"

class UBoxComponent;
class UStaticMeshComponent;
class USoundBase;

/**
 * Historical Rooftop Cloth Drying Line (Tangan / Sukhne)
 * Hemp cordage strung between terrace posts, draped with khadi cotton sheets and pagris.
 * Tactical Stealth Mechanics:
 * - Provides dynamic line-of-sight visual blockage against patrol watchmen.
 * - Brushing through the hanging textiles triggers tactile fabric rustle foley (SFX_Conceal_Cloth_Rustle).
 * - Gentle ambient wind sway adds atmospheric grounded realism to the Punjab rooftop night.
 */
UCLASS()
class REVOLUTION_API AClotheslineActor : public AActor
{
	GENERATED_BODY()

public:
	AClotheslineActor();

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* SceneRoot;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UBoxComponent* ClothPassTrigger;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* PostLeftMesh;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* PostRightMesh;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* LineCordMesh;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* SheetMesh1;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* SheetMesh2;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* SheetMesh3;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* ClothRustleSound = nullptr;

	UFUNCTION()
	void OnClothPassOverlap(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

private:
	float LastRustleTime = -10.0f;
	float WindSwayTimer = 0.0f;
};
