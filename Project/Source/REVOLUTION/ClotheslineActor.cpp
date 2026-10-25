// Copyright Epic Games, Inc. All Rights Reserved.

#include "ClotheslineActor.h"
#include "RevolutionCharacter.h"
#include "Components/BoxComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SceneComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/SoundBase.h"
#include "REVOLUTION.h"

AClotheslineActor::AClotheslineActor()
{
	PrimaryActorTick.bCanEverTick = true;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	static ConstructorHelpers::FObjectFinder<UStaticMesh> CylMeshFinder(TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));
	static ConstructorHelpers::FObjectFinder<UStaticMesh> CubeMeshFinder(TEXT("/Engine/BasicShapes/Cube.Cube"));

	// Left support pole (bamboo/timber post)
	PostLeftMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("PostLeftMesh"));
	PostLeftMesh->SetupAttachment(RootComponent);
	PostLeftMesh->SetRelativeLocation(FVector(0.0f, -120.0f, 75.0f));
	PostLeftMesh->SetRelativeScale3D(FVector(0.08f, 0.08f, 1.5f));
	PostLeftMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	if (CylMeshFinder.Succeeded())
	{
		PostLeftMesh->SetStaticMesh(CylMeshFinder.Object);
	}

	// Right support pole
	PostRightMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("PostRightMesh"));
	PostRightMesh->SetupAttachment(RootComponent);
	PostRightMesh->SetRelativeLocation(FVector(0.0f, 120.0f, 75.0f));
	PostRightMesh->SetRelativeScale3D(FVector(0.08f, 0.08f, 1.5f));
	PostRightMesh->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	if (CylMeshFinder.Succeeded())
	{
		PostRightMesh->SetStaticMesh(CylMeshFinder.Object);
	}

	// Hemp cord line
	LineCordMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("LineCordMesh"));
	LineCordMesh->SetupAttachment(RootComponent);
	LineCordMesh->SetRelativeLocation(FVector(0.0f, 0.0f, 135.0f));
	LineCordMesh->SetRelativeRotation(FRotator(90.0f, 0.0f, 0.0f));
	LineCordMesh->SetRelativeScale3D(FVector(0.02f, 0.02f, 2.4f));
	LineCordMesh->SetCollisionProfileName(TEXT("NoCollision"));
	if (CylMeshFinder.Succeeded())
	{
		LineCordMesh->SetStaticMesh(CylMeshFinder.Object);
	}

	// Hanging Khadi Cloth Sheet 1 (Left - Dhoti / Muslin sheet)
	SheetMesh1 = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("SheetMesh1"));
	SheetMesh1->SetupAttachment(RootComponent);
	SheetMesh1->SetRelativeLocation(FVector(0.0f, -70.0f, 95.0f));
	SheetMesh1->SetRelativeScale3D(FVector(0.03f, 0.65f, 0.85f));
	SheetMesh1->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	if (CubeMeshFinder.Succeeded())
	{
		SheetMesh1->SetStaticMesh(CubeMeshFinder.Object);
	}

	// Hanging Khadi Cloth Sheet 2 (Center - Saffron/Indigo Dupatta)
	SheetMesh2 = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("SheetMesh2"));
	SheetMesh2->SetupAttachment(RootComponent);
	SheetMesh2->SetRelativeLocation(FVector(0.0f, 0.0f, 92.0f));
	SheetMesh2->SetRelativeScale3D(FVector(0.03f, 0.55f, 0.88f));
	SheetMesh2->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	if (CubeMeshFinder.Succeeded())
	{
		SheetMesh2->SetStaticMesh(CubeMeshFinder.Object);
	}

	// Hanging Khadi Cloth Sheet 3 (Right - White Cotton Pagri / Turban Cloth)
	SheetMesh3 = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("SheetMesh3"));
	SheetMesh3->SetupAttachment(RootComponent);
	SheetMesh3->SetRelativeLocation(FVector(0.0f, 70.0f, 96.0f));
	SheetMesh3->SetRelativeScale3D(FVector(0.03f, 0.60f, 0.82f));
	SheetMesh3->SetCollisionProfileName(TEXT("BlockAllDynamic"));
	if (CubeMeshFinder.Succeeded())
	{
		SheetMesh3->SetStaticMesh(CubeMeshFinder.Object);
	}

	// Overlap trigger for brush-through fabric rustle
	ClothPassTrigger = CreateDefaultSubobject<UBoxComponent>(TEXT("ClothPassTrigger"));
	ClothPassTrigger->SetupAttachment(RootComponent);
	ClothPassTrigger->SetRelativeLocation(FVector(0.0f, 0.0f, 85.0f));
	ClothPassTrigger->SetBoxExtent(FVector(40.0f, 130.0f, 65.0f));
	ClothPassTrigger->SetCollisionProfileName(TEXT("Trigger"));

	static ConstructorHelpers::FObjectFinder<USoundBase> SoundFinder(TEXT("/Game/Audio/SFX/SFX_Conceal_Cloth_Rustle.SFX_Conceal_Cloth_Rustle"));
	if (SoundFinder.Succeeded())
	{
		ClothRustleSound = SoundFinder.Object;
	}
}

void AClotheslineActor::BeginPlay()
{
	Super::BeginPlay();

	if (ClothPassTrigger)
	{
		ClothPassTrigger->OnComponentBeginOverlap.AddDynamic(this, &AClotheslineActor::OnClothPassOverlap);
	}

	UE_LOG(LogREVOLUTION, Log, TEXT("ClotheslineActor spawned at %s"), *GetActorLocation().ToString());
}

void AClotheslineActor::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	WindSwayTimer += DeltaTime;

	// Gentle nocturnal wind sway of hung cotton sheets
	if (SheetMesh1)
	{
		float Sway1 = FMath::Sin(WindSwayTimer * 1.8f) * 6.0f;
		SheetMesh1->SetRelativeRotation(FRotator(Sway1, 0.0f, 0.0f));
	}
	if (SheetMesh2)
	{
		float Sway2 = FMath::Sin(WindSwayTimer * 2.1f + 1.2f) * 7.5f;
		SheetMesh2->SetRelativeRotation(FRotator(Sway2, 0.0f, 0.0f));
	}
	if (SheetMesh3)
	{
		float Sway3 = FMath::Sin(WindSwayTimer * 1.6f + 2.4f) * 5.5f;
		SheetMesh3->SetRelativeRotation(FRotator(Sway3, 0.0f, 0.0f));
	}
}

void AClotheslineActor::OnClothPassOverlap(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
	ARevolutionCharacter* Kabir = Cast<ARevolutionCharacter>(OtherActor);
	if (!Kabir) return;

	const float CurrentTime = GetWorld()->GetTimeSeconds();
	if (CurrentTime - LastRustleTime >= 1.2f)
	{
		LastRustleTime = CurrentTime;

		if (ClothRustleSound)
		{
			const float RandomPitch = FMath::RandRange(0.92f, 1.08f);
			UGameplayStatics::PlaySoundAtLocation(this, ClothRustleSound, GetActorLocation(), 0.90f, RandomPitch);
		}

		UE_LOG(LogREVOLUTION, Log, TEXT("Kabir slipped through hung khadi clothesline on rooftop terrace at %s."), *GetActorLocation().ToString());
	}
}
