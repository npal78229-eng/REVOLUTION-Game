// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "ChalkMarkActor.generated.h"

class UStaticMeshComponent;

/**
 * Clandestine Scout Chalk Mark (Kharri Mitti)
 * Placed by 12-year-old scout Kabir on brick walls, doorposts, and parapets
 * to designate safe stealth traversal routes, vantage points, and drop stashes.
 * Automatically appears as an orienting waypoint on the player's Mohalla compass.
 */
UCLASS()
class REVOLUTION_API AChalkMarkActor : public AActor
{
	GENERATED_BODY()

public:
	AChalkMarkActor();

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	USceneComponent* SceneRoot;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	UStaticMeshComponent* GlyphMesh;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Scout")
	FText MarkLabel = FText::FromString(TEXT("Scout Route Mark"));

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Scout")
	FLinearColor ChalkColor = FLinearColor(0.95f, 0.94f, 0.90f, 0.88f);

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Revolution|Scout")
	bool bHasBeenInvestigatedByWatchman = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Revolution|Scout")
	float InvestigationRadius = 240.0f;

protected:
	virtual void BeginPlay() override;
};
