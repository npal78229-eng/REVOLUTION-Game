// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "PebbleProjectile.generated.h"

class USphereComponent;
class UStaticMeshComponent;
class UProjectileMovementComponent;
class USoundBase;

/**
 * Tactical Distraction Projectile (Pebble / Terracotta Marble)
 * Used by 12-year-old scout Kabir to divert curfew watchmen and colonial constables.
 * On bounce/impact against walls or brick streets, emits an acoustic alert that
 * causes nearby ACurfewPatrolAI watchmen to break patrol and investigate the disturbance.
 */
UCLASS()
class REVOLUTION_API APebbleProjectile : public AActor
{
	GENERATED_BODY()

public:
	APebbleProjectile();

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USphereComponent* CollisionComponent;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* MeshComponent;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UProjectileMovementComponent* ProjectileMovement;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Audio")
	USoundBase* ImpactSound = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Stealth")
	float SoundAlertRadius = 850.0f; // Audible distraction range in centimeters

	UFUNCTION()
	void OnHit(UPrimitiveComponent* HitComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, FVector NormalImpulse, const FHitResult& Hit);

protected:
	virtual void BeginPlay() override;

private:
	bool bHasAlertedWatchman = false;
};
