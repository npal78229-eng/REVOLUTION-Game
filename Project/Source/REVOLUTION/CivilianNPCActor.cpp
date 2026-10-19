// Copyright Epic Games, Inc. All Rights Reserved.

#include "CivilianNPCActor.h"
#include "RevolutionCharacter.h"
#include "Components/CapsuleComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SphereComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Engine/World.h"
#include "Kismet/GameplayStatics.h"
#include "Kismet/KismetMathLibrary.h"
#include "RevolutionMissionSubsystem.h"
#include "Sound/SoundBase.h"
#include "Sound/SoundAttenuation.h"
#include "Components/AudioComponent.h"
#include "Materials/MaterialInterface.h"
#include "REVOLUTION.h"

ACivilianNPCActor::ACivilianNPCActor()
{
	PrimaryActorTick.bCanEverTick = true;

	// Capsule dimensions for adult civilian
	GetCapsuleComponent()->InitCapsuleSize(34.0f, 88.0f);

	bUseControllerRotationPitch = false;
	bUseControllerRotationYaw = false;
	bUseControllerRotationRoll = false;

	GetCharacterMovement()->bOrientRotationToMovement = true;
	GetCharacterMovement()->RotationRate = FRotator(0.0f, 240.0f, 0.0f);
	GetCharacterMovement()->MaxWalkSpeed = 120.0f;

	// Skeletal mesh setup (Adult Mannequin)
	static ConstructorHelpers::FObjectFinder<USkeletalMesh> MeshFinder(TEXT("/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple.SKM_Manny_Simple"));
	if (MeshFinder.Succeeded())
	{
		GetMesh()->SetSkeletalMesh(MeshFinder.Object);
		GetMesh()->SetRelativeLocation(FVector(0.f, 0.f, -88.f));
		GetMesh()->SetRelativeRotation(FRotator(0.f, -90.f, 0.f));
		GetMesh()->SetRelativeScale3D(FVector(1.0f, 1.0f, 1.0f));
	}

	static ConstructorHelpers::FClassFinder<UAnimInstance> AnimFinder(TEXT("/Game/Characters/Mannequins/Animations/ABP_Manny.ABP_Manny_C"));
	if (AnimFinder.Succeeded())
	{
		GetMesh()->SetAnimInstanceClass(AnimFinder.Class);
	}

	// Proximity Detection Sphere
	ProximitySphere = CreateDefaultSubobject<USphereComponent>(TEXT("ProximitySphere"));
	ProximitySphere->SetupAttachment(RootComponent);
	ProximitySphere->InitSphereRadius(280.0f);
	ProximitySphere->SetCollisionProfileName(TEXT("OverlapAllDynamic"));
	ProximitySphere->SetGenerateOverlapEvents(true);

	// Prop Accessory Mesh (holds profession item)
	PropAccessoryMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("PropAccessoryMesh"));
	PropAccessoryMesh->SetupAttachment(RootComponent);
	PropAccessoryMesh->SetRelativeLocation(FVector(25.0f, 20.0f, 10.0f));
	PropAccessoryMesh->SetCollisionProfileName(TEXT("NoCollision"));

	// Turban / Headwear Mesh
	TurbanMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("TurbanMesh"));
	TurbanMesh->SetupAttachment(RootComponent);
	TurbanMesh->SetRelativeLocation(FVector(0.0f, 0.0f, 75.0f));
	TurbanMesh->SetCollisionProfileName(TEXT("NoCollision"));
}

void ACivilianNPCActor::BeginPlay()
{
	Super::BeginPlay();

	DefaultRotation = GetActorRotation();

	if (GetMesh())
	{
		MeshInitialRelativeLocation = GetMesh()->GetRelativeLocation();
		MeshInitialRelativeRotation = GetMesh()->GetRelativeRotation();
	}

	if (PropAccessoryMesh)
	{
		PropInitialRelativeLocation = PropAccessoryMesh->GetRelativeLocation();
		PropInitialRelativeRotation = PropAccessoryMesh->GetRelativeRotation();
	}

	ProximitySphere->OnComponentBeginOverlap.AddDynamic(this, &ACivilianNPCActor::OnProximityBeginOverlap);
	ProximitySphere->OnComponentEndOverlap.AddDynamic(this, &ACivilianNPCActor::OnProximityEndOverlap);

	ConfigureOccupation(Occupation);

	if (UWorld* World = GetWorld())
	{
		if (URevolutionMissionSubsystem* Subsystem = World->GetSubsystem<URevolutionMissionSubsystem>())
		{
			Subsystem->OnMissionDirectiveChanged.AddDynamic(this, &ACivilianNPCActor::HandleMissionDirectiveChanged);
			SetDialogueModeForStage(Subsystem->GetCurrentStage());
		}
	}

	if (OccupationRoutineSound && !RoutineAudioComp && GetWorld() && GetWorld()->IsGameWorld())
	{
		RoutineAudioComp = UGameplayStatics::SpawnSoundAttached(
			OccupationRoutineSound,
			RootComponent,
			NAME_None,
			FVector::ZeroVector,
			EAttachLocation::KeepRelativeOffset,
			false,
			0.75f,
			1.0f,
			0.0f,
			VoiceAttenuation
		);
	}
}

void ACivilianNPCActor::HandleMissionDirectiveChanged(ECourierMissionStage NewStage, FText Title, FText Directive)
{
	SetDialogueModeForStage(NewStage);
}

void ACivilianNPCActor::SetDialogueModeForStage(ECourierMissionStage NewStage)
{
	const bool bShouldBeActII = (NewStage >= ECourierMissionStage::Stage_Afternoon_MunadiProclamation && NewStage <= ECourierMissionStage::Stage_ActII_Completed);
	if (bShouldBeActII != bIsInActIIMode)
	{
		bIsInActIIMode = bShouldBeActII;
		CurrentDialogueIndex = 0;
		UE_LOG(LogREVOLUTION, Log, TEXT("[%s] Switched dialogue mode: Act II Mode = %s"), *CivilianName.ToString(), bIsInActIIMode ? TEXT("TRUE") : TEXT("FALSE"));
	}
}

void ACivilianNPCActor::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	// State 1: Active Stumble Balance Recovery
	if (bIsStumbled)
	{
		StumbleTimer -= DeltaTime;
		if (StumbleTimer <= 0.0f)
		{
			bIsStumbled = false;
			StumbleTimer = 0.0f;
			ReactionState = ECivilianReactionState::Idle;
			if (GetMesh())
			{
				GetMesh()->SetRelativeLocation(MeshInitialRelativeLocation);
				GetMesh()->SetRelativeRotation(MeshInitialRelativeRotation);
			}
			if (PropAccessoryMesh)
			{
				PropAccessoryMesh->SetRelativeLocation(PropInitialRelativeLocation);
				PropAccessoryMesh->SetRelativeRotation(PropInitialRelativeRotation);
			}
		}
		else
		{
			ReactionState = ECivilianReactionState::Stumbling;
			const float Progress = 1.0f - (StumbleTimer / FMath::Max(0.01f, StumbleDuration));

			// Non-violent procedural balance recovery animation (stagger and spring-back)
			// Progress 0.0 -> 0.35: sudden tilt and offset backwards away from impact
			// Progress 0.35 -> 1.0: spring-damped recovery back to stable upright pose
			float StaggerIntensity;
			if (Progress < 0.35f)
			{
				StaggerIntensity = Progress / 0.35f;
			}
			else
			{
				const float SettleT = (Progress - 0.35f) / 0.65f;
				StaggerIntensity = FMath::Cos(SettleT * UE_HALF_PI);
			}

			if (GetMesh())
			{
				const FVector LocalImpact = GetActorTransform().InverseTransformVectorNoScale(StumbleDirection);
				const FRotator TiltOffset = FRotator(-LocalImpact.X * 14.0f * StaggerIntensity, 0.0f, LocalImpact.Y * 12.0f * StaggerIntensity);
				const FVector PosOffset = -LocalImpact * (28.0f * StaggerIntensity);

				GetMesh()->SetRelativeLocation(MeshInitialRelativeLocation + PosOffset);
				GetMesh()->SetRelativeRotation(MeshInitialRelativeRotation + TiltOffset);
			}

			// Apply gentle world pushback with collision sweep (prevents wall clipping)
			if (Progress < 0.3f)
			{
				const FVector Pushback = StumbleDirection * (StumbleIntensity * 0.25f * DeltaTime);
				AddActorWorldOffset(Pushback, true);
			}
		}
	}
	// State 2: Curious Distraction Investigation (Pebble noise / disturbance)
	else if (ReactionState == ECivilianReactionState::CuriousInvestigating)
	{
		CuriosityTimer -= DeltaTime;
		if (CuriosityTimer <= 0.0f)
		{
			CuriosityTimer = 0.0f;
			ReactionState = ECivilianReactionState::Idle;
		}
		else
		{
			// Smoothly orient head/body toward disturbance location
			const FVector MyLoc = GetActorLocation();
			FRotator TargetRot = UKismetMathLibrary::FindLookAtRotation(MyLoc, CuriosityLookTarget);
			TargetRot.Pitch = 0.0f;
			TargetRot.Roll = 0.0f;
			const FRotator NewRot = FMath::RInterpTo(GetActorRotation(), TargetRot, DeltaTime, 5.0f);
			SetActorRotation(NewRot);
		}
	}
	// State 3: Smoothly orient toward Kabir when player is in close proximity
	else if (bPlayerInProximity && NearbyPlayer.IsValid())
	{
		ReactionState = ECivilianReactionState::FacingPlayer;
		const FVector PlayerLoc = NearbyPlayer->GetActorLocation();
		const FVector MyLoc = GetActorLocation();
		FRotator TargetRot = UKismetMathLibrary::FindLookAtRotation(MyLoc, PlayerLoc);
		TargetRot.Pitch = 0.0f;
		TargetRot.Roll = 0.0f;

		const FRotator NewRot = FMath::RInterpTo(GetActorRotation(), TargetRot, DeltaTime, 4.0f);
		SetActorRotation(NewRot);
	}
	// State 4: Default Idle
	else
	{
		ReactionState = ECivilianReactionState::Idle;
		// Smoothly return to default idle facing
		const FRotator CurrentRot = GetActorRotation();
		if (!CurrentRot.Equals(DefaultRotation, 1.0f))
		{
			const FRotator RestRot = FMath::RInterpTo(CurrentRot, DefaultRotation, DeltaTime, 2.0f);
			SetActorRotation(RestRot);
		}
	}

	// Task 31: Procedural Idle Breathing & Occupational Routine Micro-Gestures
	if (!bIsStumbled && bEnableRoutineAnimations)
	{
		BreathingCycleTime += DeltaTime;
		RoutineCycleTime += DeltaTime;

		// Breathing sinusoidal calculations (15 breaths per minute, 4s cycle)
		const float BreathPhase = BreathingCycleTime * IdleBreathingRate * TWO_PI;
		const float BreathSin = FMath::Sin(BreathPhase);
		const float BreathCos = FMath::Cos(BreathPhase * 0.5f);

		// Idle vertical heave (chest/shoulder breathing)
		const FVector BreathingOffset = FVector(0.0f, 0.0f, BreathSin * IdleBreathingAmplitude);
		// Gentle breathing pitch and roll oscillation
		const FRotator BreathingRotOffset = FRotator(BreathSin * 0.35f, 0.0f, BreathCos * 0.20f);

		// Occupation-specific procedural micro-gestures and prop movement
		FVector RoutineMeshOffset = FVector::ZeroVector;
		FRotator RoutineMeshRot = FRotator::ZeroRotator;
		FVector RoutinePropOffset = FVector::ZeroVector;
		FRotator RoutinePropRot = FRotator::ZeroRotator;

		switch (Occupation)
		{
		case ECivilianOccupation::FatherTailor:
		{
			// 5.0 Hz sewing machine treadle vibration & needle sync
			const float TreadlePhase = RoutineCycleTime * 5.0f * TWO_PI;
			const float TreadleVibe = FMath::Sin(TreadlePhase) * 0.35f;
			RoutinePropOffset.Z += TreadleVibe;

			// Seam inspection forward lean every ~9 seconds
			const float SeamCycle = FMath::Fmod(RoutineCycleTime, 9.0f) / 9.0f;
			if (SeamCycle > 0.65f && SeamCycle < 0.90f)
			{
				const float LeanFactor = FMath::Sin((SeamCycle - 0.65f) / 0.25f * PI);
				RoutineMeshRot.Pitch -= LeanFactor * 3.2f;
				RoutineMeshOffset.X += LeanFactor * 1.5f;
			}
			break;
		}
		case ECivilianOccupation::HalwaiChaiVendor:
		{
			// Ladle / cup circular stirring motion at 0.8 Hz
			const float StirPhase = RoutineCycleTime * 0.8f * TWO_PI;
			RoutinePropOffset.X += FMath::Cos(StirPhase) * 1.2f;
			RoutinePropOffset.Y += FMath::Sin(StirPhase) * 1.2f;

			// Halwai rhythmic upper-body stirring sway
			RoutineMeshRot.Roll += FMath::Sin(StirPhase) * 0.85f;
			break;
		}
		case ECivilianOccupation::BhishtiWaterCarrier:
		{
			// Load-bearing posture with water-carrier shoulder tilt
			RoutineMeshRot.Roll += 1.8f;
			const float MashkPhase = RoutineCycleTime * 0.35f * TWO_PI;
			RoutineMeshRot.Roll += FMath::Sin(MashkPhase) * 0.6f;
			// Goatskin mashk slosh roll
			RoutinePropRot.Roll += FMath::Sin(MashkPhase) * 1.5f;
			break;
		}
		case ECivilianOccupation::ClothMerchant:
		{
			// Fabric examination scan: periodic slow yaw scan & pitch inspection
			const float ScanPhase = RoutineCycleTime * 0.3f * TWO_PI;
			RoutineMeshRot.Yaw += FMath::Sin(ScanPhase) * 2.5f;
			const float InspectCycle = FMath::Fmod(RoutineCycleTime, 8.0f) / 8.0f;
			if (InspectCycle > 0.60f && InspectCycle < 0.88f)
			{
				const float DipFactor = FMath::Sin((InspectCycle - 0.60f) / 0.28f * PI);
				RoutineMeshRot.Pitch -= DipFactor * 2.2f;
			}
			break;
		}
		case ECivilianOccupation::SchoolHeadmaster:
		{
			// Scholarly upright posture with thoughtful nods
			const float NodCycle = FMath::Fmod(RoutineCycleTime, 7.0f) / 7.0f;
			if (NodCycle > 0.70f && NodCycle < 0.92f)
			{
				const float NodFactor = FMath::Sin((NodCycle - 0.70f) / 0.22f * TWO_PI);
				RoutineMeshRot.Pitch -= NodFactor * 1.8f;
			}
			break;
		}
		case ECivilianOccupation::SchoolFriendKartar:
		{
			// Looking up at kites high in the Punjab sky
			const float KiteSkyPhase = RoutineCycleTime * 0.18f * TWO_PI;
			const float LookUpPitch = 12.0f + FMath::Sin(KiteSkyPhase) * 4.0f;
			RoutineMeshRot.Pitch += LookUpPitch;

			// Charkhi kite spool twirling in hand
			RoutinePropRot.Yaw = FMath::Fmod(RoutineCycleTime * 120.0f, 360.0f);
			break;
		}
		case ECivilianOccupation::MunadiTownCrier:
		{
			// Periodic arm/prop rhythm mimicking drumstick striking the dafli drum
			const float DrumBeatPhase = RoutineCycleTime * 4.0f * TWO_PI;
			RoutinePropRot.Pitch += FMath::Sin(DrumBeatPhase) * 12.0f;
			RoutineMeshRot.Pitch += FMath::Sin(RoutineCycleTime * 2.0f * TWO_PI) * 1.5f;
			break;
		}
		case ECivilianOccupation::ProtestElder:
		{
			// Calm elder posture with gentle head sway and dignified nods
			const float ElderPhase = RoutineCycleTime * 0.25f * TWO_PI;
			RoutineMeshRot.Yaw += FMath::Sin(ElderPhase) * 1.8f;
			const float ElderNodCycle = FMath::Fmod(RoutineCycleTime, 6.0f) / 6.0f;
			if (ElderNodCycle > 0.65f && ElderNodCycle < 0.85f)
			{
				const float NodFactor = FMath::Sin((ElderNodCycle - 0.65f) / 0.20f * PI);
				RoutineMeshRot.Pitch -= NodFactor * 2.0f;
			}
			break;
		}
		}

		if (GetMesh())
		{
			GetMesh()->SetRelativeLocation(MeshInitialRelativeLocation + BreathingOffset + RoutineMeshOffset);
			GetMesh()->SetRelativeRotation(MeshInitialRelativeRotation + BreathingRotOffset + RoutineMeshRot);
		}

		if (PropAccessoryMesh)
		{
			PropAccessoryMesh->SetRelativeLocation(PropInitialRelativeLocation + RoutinePropOffset);
			PropAccessoryMesh->SetRelativeRotation(PropInitialRelativeRotation + RoutinePropRot);
		}
	}
}

void ACivilianNPCActor::ConfigureOccupation(ECivilianOccupation NewOccupation)
{
	Occupation = NewOccupation;
	AmbientBarks.Empty();
	ConversationDialogues.Empty();
	ActIIBarks.Empty();
	ActIIDialogues.Empty();
	StumbleBarks.Empty();
	CuriosityBarks.Empty();
	CurrentDialogueIndex = 0;

	if (!VoiceAttenuation)
	{
		VoiceAttenuation = LoadObject<USoundAttenuation>(nullptr, TEXT("/Game/Audio/Attenuation/ATT_Voice_Proximity.ATT_Voice_Proximity"));
	}

	switch (Occupation)
	{
	case ECivilianOccupation::FatherTailor:
		CivilianName = FText::FromString(TEXT("Ram Lubhaya"));
		ProfessionTitle = FText::FromString(TEXT("Master Darzi (Kabir's Father)"));
		HistoricalLore = FText::FromString(
			TEXT("A skilled artisan who operates a 1910s cast-iron Singer sewing machine on the haveli veranda. Having lost his eldest brother to the trenches of the Western Front in the Great War, Ram Lubhaya harbors deep quiet grief. He strives to shield his young son Kabir from political peril, but cannot ignore the intensifying martial oppression surrounding their mohalla.")
		);
		AmbientBarks.Add(FText::FromString(TEXT("Kabir puttar, do not run so fast across the parapet bricks! You'll tear your new kurta.")));
		AmbientBarks.Add(FText::FromString(TEXT("Listen to me, son: if the Kotwal's constables patrol the Deorhi, stay quietly inside the courtyard.")));
		AmbientBarks.Add(FText::FromString(TEXT("English cloth from Manchester has doubled in import duty again. Artisans can scarcely afford plain muslin.")));

		ConversationDialogues.Add(FText::FromString(
			TEXT("Ram Lubhaya: 'Kabir, take this repaired khadi coat down to Lala Karam Chand in the Grand Bazaar. Be alert near the police naka bandi checkpoints; they are questioning anyone carrying bundles.'")
		));
		ConversationDialogues.Add(FText::FromString(
			TEXT("Ram Lubhaya: 'They passed the Rowlatt Act in Delhi. They believe they can arrest any Punjabi without warrant, trial, or advocate. But Dr. Kitchlew and Mahatma Gandhi have called for a complete Hartal.'")
		));
		ConversationDialogues.Add(FText::FromString(
			TEXT("Ram Lubhaya: 'Your mother left warm ginger-cardamom chai by the courtyard stove. Drink a kulhad before going to school.'")
		));

		StumbleBarks.Add(FText::FromString(TEXT("Dhyan naal, Kabir! Look where you're running, son!")));
		StumbleBarks.Add(FText::FromString(TEXT("Arrey puttar, do not rush heedlessly into the veranda!")));
		CuriosityBarks.Add(FText::FromString(TEXT("What made that sharp clatter out in the lane?")));
		CuriosityBarks.Add(FText::FromString(TEXT("Did something drop against the courtyard wall?")));

		InteractionVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_RamLubhaya_Dialogue.SFX_Voice_RamLubhaya_Dialogue"));
		AmbientBarkVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_RamLubhaya_Bark.SFX_Voice_RamLubhaya_Bark"));
		StumbleVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_Civilian_Stumble_01.SFX_Voice_Civilian_Stumble_01"));
		CuriosityVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_Civilian_Curiosity_01.SFX_Voice_Civilian_Curiosity_01"));
		OccupationRoutineSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Routine_SewingMachine_Loop.SFX_Routine_SewingMachine_Loop"));
		break;

	case ECivilianOccupation::HalwaiChaiVendor:
		CivilianName = FText::FromString(TEXT("Hira Halwai"));
		ProfessionTitle = FText::FromString(TEXT("Mohalla Tea & Sweet Stall Owner"));
		HistoricalLore = FText::FromString(
			TEXT("The boisterous, respected owner of the bustling corner tea stall in Zone D. His bubbling brass samovar and fresh jalebi pans are the epicenter of Kot Gurdarshan's news, where tonga drivers, shopkeepers, and underground couriers exchange whispers of the freedom struggle.")
		);
		AmbientBarks.Add(FText::FromString(TEXT("Garam chai! Freshly boiled cardamom and ginger tea in baked kulhads! Two copper paisas!")));
		AmbientBarks.Add(FText::FromString(TEXT("Arrey Kabir! Tell your father that Master Ramlal has not yet cleared his weekly jalebi account!")));
		AmbientBarks.Add(FText::FromString(TEXT("Be careful around the railway crossing, boy. Two British military lorries arrived from Lahore at sunrise.")));

		ConversationDialogues.Add(FText::FromString(
			TEXT("Hira Halwai: 'Here, drink a steaming kulhad of chai, Kabir. The morning dust has an unseasonal chill today.'")
		));
		ConversationDialogues.Add(FText::FromString(
			TEXT("Hira Halwai: 'Everyone at the mandi is speaking of the protest meeting at Jallianwala Bagh. If the British authorities arrest our leaders, this entire province will rise up.'")
		));
		ConversationDialogues.Add(FText::FromString(
			TEXT("Hira Halwai: 'Remember, boy: once you finish your chai, shatter the clay kulhad upon the street. From earth it came, to earth it returns; no colonial taxman can assess the dust of Punjab.'")
		));

		StumbleBarks.Add(FText::FromString(TEXT("Arrey bachke chalo, chhotey! You'll tip over the boiling chai pot!")));
		StumbleBarks.Add(FText::FromString(TEXT("Ohe! This is a bazaar lane, not a racetrack!")));
		CuriosityBarks.Add(FText::FromString(TEXT("Did something fall behind the sweet counter?")));
		CuriosityBarks.Add(FText::FromString(TEXT("Aawaz kithon aayi? What's causing a racket near the street?")));

		InteractionVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_HiraHalwai_Dialogue.SFX_Voice_HiraHalwai_Dialogue"));
		AmbientBarkVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_HiraHalwai_Bark.SFX_Voice_HiraHalwai_Bark"));
		StumbleVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_Civilian_Stumble_02.SFX_Voice_Civilian_Stumble_02"));
		CuriosityVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_Civilian_Curiosity_02.SFX_Voice_Civilian_Curiosity_02"));
		OccupationRoutineSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Routine_ChaiStir_Loop.SFX_Routine_ChaiStir_Loop"));
		break;

	case ECivilianOccupation::BhishtiWaterCarrier:
		CivilianName = FText::FromString(TEXT("Ghasita Bhishti"));
		ProfessionTitle = FText::FromString(TEXT("Traditional Mohalla Water-Carrier"));
		HistoricalLore = FText::FromString(
			TEXT("A generational Punjabi Muslim water-carrier who draws sweet water from the mohalla well into his tanned goatskin mashk. He sprinkles the dusty brick alleys each morning and fills domestic matkas, embodying the deep cross-communal solidarity that unified pre-partition Punjab.")
		);
		AmbientBarks.Add(FText::FromString(TEXT("Bhishti aya! Cold, sweet well water for your courtyards and cooking stoves!")));
		AmbientBarks.Add(FText::FromString(TEXT("Salam, chhotey Kabir. Watch your balance by the well coping; the moss is damp.")));
		AmbientBarks.Add(FText::FromString(TEXT("May the Almighty preserve our well; the canal overseers diverted another tributary to the military cantonment.")));

		ConversationDialogues.Add(FText::FromString(
			TEXT("Ghasita Bhishti: 'I filled your mother's terracotta matkas just before dawn, Kabir. Pure, cold water drawn from forty cubits deep.'")
		));
		ConversationDialogues.Add(FText::FromString(
			TEXT("Ghasita Bhishti: 'In our mohalla, Hindu, Muslim, and Sikh draw from this exact well rope. The British administrators try to divide us with separate cantonment water taps, but we share our water, our grief, and our bread.'")
		));
		ConversationDialogues.Add(FText::FromString(
			TEXT("Ghasita Bhishti: 'The community elders have gathered under the ancient Peepal tree right now, discussing the colonial curfew proclamations.'")
		));

		StumbleBarks.Add(FText::FromString(TEXT("Sambhal ke, beta! Don't puncture the goatskin mashk or slip on the wet flagstones!")));
		StumbleBarks.Add(FText::FromString(TEXT("Ya Allah, watch your footing, Kabir!")));
		CuriosityBarks.Add(FText::FromString(TEXT("A stone rattled against the well curb...")));
		CuriosityBarks.Add(FText::FromString(TEXT("Did something drop from the parapet?")));

		InteractionVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_Ghasita_Dialogue.SFX_Voice_Ghasita_Dialogue"));
		AmbientBarkVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_Ghasita_Bark.SFX_Voice_Ghasita_Bark"));
		StumbleVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_Civilian_Stumble_01.SFX_Voice_Civilian_Stumble_01"));
		CuriosityVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_Civilian_Curiosity_01.SFX_Voice_Civilian_Curiosity_01"));
		OccupationRoutineSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Routine_MashkWater_Loop.SFX_Routine_MashkWater_Loop"));
		break;

	case ECivilianOccupation::ClothMerchant:
		CivilianName = FText::FromString(TEXT("Lala Karam Chand"));
		ProfessionTitle = FText::FromString(TEXT("Textile Merchant (Mandi Bazaar)"));
		HistoricalLore = FText::FromString(
			TEXT("An experienced cloth merchant operating in the Grand Bazaar for three decades. He stands at a poignant crossroads between his unsold stocks of British Manchester-milled textiles and the rising moral tide of the Swadeshi boycott movement calling for handspun Indian khadi.")
		);
		AmbientBarks.Add(FText::FromString(TEXT("Finest cambric, satin, and homespun Khadi! Examine the weave for yourself!")));
		AmbientBarks.Add(FText::FromString(TEXT("Ram Lubhaya's tailoring is the finest stitchwork in the entire district.")));
		AmbientBarks.Add(FText::FromString(TEXT("If the Hartal strikes tomorrow, every merchant shutter will remain padlocked shut.")));

		ConversationDialogues.Add(FText::FromString(
			TEXT("Lala Karam Chand: 'Ah, Kabir! Your father sent the coat? Let me examine the seams... magnificent precision, as always.'")
		));
		ConversationDialogues.Add(FText::FromString(
			TEXT("Lala Karam Chand: 'Look at these imported bolts stamped with the Manchester mills seal. They buy our Punjabi raw cotton for copper coins, ship it overseas, and sell it back to us at ruinous prices. Swadeshi is our only economic breath.'")
		));
		ConversationDialogues.Add(FText::FromString(
			TEXT("Lala Karam Chand: 'Take this payment for your father, and deliver my deepest respects. Tell him to keep the haveli deorhi barred tonight; rumors say the police intend to conduct midnight searches.'")
		));

		StumbleBarks.Add(FText::FromString(TEXT("Watch out, boy! You'll knock over the Swadeshi cloth bolts!")));
		StumbleBarks.Add(FText::FromString(TEXT("Arrey dhyan se! Freshly dyed muslin cannot bear street dust!")));
		CuriosityBarks.Add(FText::FromString(TEXT("What was that clatter near the shop threshold?")));
		CuriosityBarks.Add(FText::FromString(TEXT("Is someone loitering by the cloth bales?")));

		InteractionVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_LalaKaramChand_Dialogue.SFX_Voice_LalaKaramChand_Dialogue"));
		AmbientBarkVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_LalaKaramChand_Bark.SFX_Voice_LalaKaramChand_Bark"));
		StumbleVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_Civilian_Stumble_01.SFX_Voice_Civilian_Stumble_01"));
		CuriosityVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_Civilian_Curiosity_01.SFX_Voice_Civilian_Curiosity_01"));
		OccupationRoutineSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Routine_ClothMerchant_Loop.SFX_Routine_ClothMerchant_Loop"));
		break;

	case ECivilianOccupation::SchoolHeadmaster:
		CivilianName = FText::FromString(TEXT("Pandit Kashi Ram"));
		ProfessionTitle = FText::FromString(TEXT("Headmaster, Vernacular Middle School"));
		HistoricalLore = FText::FromString(
			TEXT("The scholarly headmaster of Kot Gurdarshan Vernacular Middle School in District C. Educated in Lahore, he teaches mathematics, history, Urdu, and Gurmukhi. He views universal literacy and courageous critical thinking as the foundational weapons with which India will liberate itself.")
		);
		AmbientBarks.Add(FText::FromString(TEXT("The morning bell tolls at eight o'clock sharp! Do not linger in the bazaar alleys, boys!")));
		AmbientBarks.Add(FText::FromString(TEXT("Language is the sanctuary of a free people. Practice your Gurmukhi and Urdu calligraphy today.")));
		AmbientBarks.Add(FText::FromString(TEXT("True knowledge is that which no martial emergency decree can ever confiscate.")));

		ConversationDialogues.Add(FText::FromString(
			TEXT("Pandit Kashi Ram: 'Namaste, Kabir. Are you prepared for today's lesson on geography and the history of Punjab?'")
		));
		ConversationDialogues.Add(FText::FromString(
			TEXT("Pandit Kashi Ram: 'When you toll the iron bell in the schoolyard, Kabir, remember: knowledge rings for liberty. Even the mightiest colonial empire cannot hold an educated generation in chains.'")
		));
		ConversationDialogues.Add(FText::FromString(
			TEXT("Pandit Kashi Ram: 'Examine the new decree posted on the municipal board carefully, Kabir. A scholar must always learn to read between the lines that the authorities write.'")
		));

		StumbleBarks.Add(FText::FromString(TEXT("Composure, Kabir! Haste and heedless charging are not the marks of a scholar!")));
		StumbleBarks.Add(FText::FromString(TEXT("Patience, boy! Why run through the courtyard like a stray calf?")));
		CuriosityBarks.Add(FText::FromString(TEXT("Listen... what fell from the schoolhouse eaves?")));
		CuriosityBarks.Add(FText::FromString(TEXT("Was that an impact near the bell tower?")));

		InteractionVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_PanditKashiRam_Dialogue.SFX_Voice_PanditKashiRam_Dialogue"));
		AmbientBarkVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_PanditKashiRam_Bark.SFX_Voice_PanditKashiRam_Bark"));
		StumbleVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_Civilian_Stumble_01.SFX_Voice_Civilian_Stumble_01"));
		CuriosityVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_Civilian_Curiosity_01.SFX_Voice_Civilian_Curiosity_01"));
		OccupationRoutineSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Routine_Schoolmaster_Loop.SFX_Routine_Schoolmaster_Loop"));
		break;

	case ECivilianOccupation::SchoolFriendKartar:
		CivilianName = FText::FromString(TEXT("Kartar Singh"));
		ProfessionTitle = FText::FromString(TEXT("Schoolmate & Childhood Friend (Age 12)"));
		HistoricalLore = FText::FromString(
			TEXT("Kabir's closest schoolmate and friend in Kot Gurdarshan. Full of energetic mischief and infectious curiosity, Kartar loves flying fighter kites from the mohalla rooftops and snacking on jalebis from Hira Halwai's stall. He eagerly looks forward to the upcoming Baisakhi fair at Amritsar, yet senses the growing martial tension as British troop lorries rumble along the Grand Trunk Road.")
		);
		AmbientBarks.Add(FText::FromString(TEXT("Kabir! Look up at the sky! That yellow fighter kite belongs to the boys from Katra Jaimal Singh!")));
		AmbientBarks.Add(FText::FromString(TEXT("Hurry up before Pandit Ji rings the last bell, or we will have to stand outside the verandah!")));
		AmbientBarks.Add(FText::FromString(TEXT("My chacha says tomorrow is Baisakhi! Are we going to see the wrestling matches at the fair?")));

		ConversationDialogues.Add(FText::FromString(
			TEXT("Kartar: 'Kabir! There you are! Did your father finish tailoring the coat for Lala Karam Chand? I've been waiting for you by the Peepal tree.'")
		));
		ConversationDialogues.Add(FText::FromString(
			TEXT("Kartar: 'Look what I found tucked near the Peepal tree roots—a secret printed leaflet about the Hartal! People are saying everyone should close their shops and march peacefully.'")
		));
		ConversationDialogues.Add(FText::FromString(
			TEXT("Kartar: 'Pandit Ji has already entered the classroom. If we don't ring the bell soon, he'll make us write our Gurmukhi alphabet ten times on our slates! Let's race to the school tower!'")
		));

		StumbleBarks.Add(FText::FromString(TEXT("Oye Kabir! Slow down, are the constables chasing you?!")));
		StumbleBarks.Add(FText::FromString(TEXT("Arrey yaar, you almost knocked my kite spool into the mud!")));
		CuriosityBarks.Add(FText::FromString(TEXT("Did you hear that stone clatter? Did someone toss a pebble?")));
		CuriosityBarks.Add(FText::FromString(TEXT("Look over there! Something just hit the brick wall!")));

		InteractionVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_KartarSingh_Dialogue.SFX_Voice_KartarSingh_Dialogue"));
		AmbientBarkVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_KartarSingh_Bark.SFX_Voice_KartarSingh_Bark"));
		StumbleVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_Civilian_Stumble_03.SFX_Voice_Civilian_Stumble_03"));
		CuriosityVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_Civilian_Curiosity_01.SFX_Voice_Civilian_Curiosity_01"));
		OccupationRoutineSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Routine_KartarKite_Loop.SFX_Routine_KartarKite_Loop"));
		break;

	case ECivilianOccupation::MunadiTownCrier:
		CivilianName = FText::FromString(TEXT("Nikka Ram"));
		ProfessionTitle = FText::FromString(TEXT("Town Crier (Munadi-chi)"));
		HistoricalLore = FText::FromString(
			TEXT("A municipal herald contracted to beat the dafli drum and recite official proclamations across the chowks of Amritsar. Bound by duty yet heartbroken, he delivers General Dyer's draconian order banning all peaceful assemblies on the sacred day of Baisakhi.")
		);
		AmbientBarks.Add(FText::FromString(TEXT("Hukm-e-Sarkar! Suno, suno, aiy ahl-e-shahar! Hear the martial decree!")));
		AmbientBarks.Add(FText::FromString(TEXT("By order of Brigadier-General Dyer, all gatherings are forbidden under martial command!")));
		AmbientBarks.Add(FText::FromString(TEXT("Do not assemble in groups of more than four! Disperse to your homes immediately!")));

		ConversationDialogues.Add(FText::FromString(
			TEXT("Nikka Ram: 'Hukm-e-Sarkar! Suno, suno! By decree of the General Officer Commanding: any procession or gathering of more than four persons is declared an unlawful assembly and will be dispersed by fire!'")
		));
		ConversationDialogues.Add(FText::FromString(
			TEXT("Nikka Ram: 'Kabir, tell your father Ram Lubhaya to keep inside the haveli. British riflemen have picketed the main gates and they are arresting anyone who questions the proclamation.'")
		));
		ConversationDialogues.Add(FText::FromString(
			TEXT("Nikka Ram: 'Thousands of pilgrims from the Majha villages know nothing of this decree... God protect our people today.'")
		));

		ActIIBarks.Add(FText::FromString(TEXT("The proclamation has been drummed at nineteen points across the city! No one can plead ignorance!")));
		ActIIBarks.Add(FText::FromString(TEXT("Stay clear of the Hall Gate pickets! The soldiers are locking the city down!")));

		ActIIDialogues.Add(FText::FromString(
			TEXT("Nikka Ram: 'The meeting at Jallianwala Bagh has already started, Kabir! Thousands are flowing through the narrow passage. But General Dyer's column is mobilizing at the Ram Bagh headquarters right now!'")
		));
		ActIIDialogues.Add(FText::FromString(
			TEXT("Nikka Ram: 'Run, Kabir! Warn whoever you can! Dyer has vowed to crush the assembly!'")
		));

		StumbleBarks.Add(FText::FromString(TEXT("Sambhal ke! Don't damage the town crier's drum!")));
		StumbleBarks.Add(FText::FromString(TEXT("Watch your step, boy! The chowk is packed with anxious people!")));
		CuriosityBarks.Add(FText::FromString(TEXT("What was that sharp disturbance in the alley?")));
		CuriosityBarks.Add(FText::FromString(TEXT("Who is running behind the proclamation board?")));

		InteractionVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_RamLubhaya_Dialogue.SFX_Voice_RamLubhaya_Dialogue"));
		AmbientBarkVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_RamLubhaya_Bark.SFX_Voice_RamLubhaya_Bark"));
		StumbleVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_Civilian_Stumble_01.SFX_Voice_Civilian_Stumble_01"));
		CuriosityVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_Civilian_Curiosity_01.SFX_Voice_Civilian_Curiosity_01"));
		OccupationRoutineSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Munadi_Drum.SFX_Munadi_Drum"));
		break;

	case ECivilianOccupation::ProtestElder:
		CivilianName = FText::FromString(TEXT("Bhai Sant Singh"));
		ProfessionTitle = FText::FromString(TEXT("Mohalla Elder & Shopkeeper"));
		HistoricalLore = FText::FromString(
			TEXT("A revered elder citizen of Kot Gurdarshan who witnessed the Rowlatt Satyagraha. He counsels courage, dignified restraint, and inter-communal unity as imperial martial law threatens the peaceful citizens of Amritsar.")
		);
		AmbientBarks.Add(FText::FromString(TEXT("Baisakhi cannot be erased by an imperial decree.")));
		AmbientBarks.Add(FText::FromString(TEXT("Keep the peace, brothers. Do not give them an excuse for violence.")));
		AmbientBarks.Add(FText::FromString(TEXT("Dr. Kitchlew and Dr. Satyapal taught us non-violence. We will not falter.")));

		ConversationDialogues.Add(FText::FromString(
			TEXT("Bhai Sant Singh: 'Kabir, son of Ram Lubhaya. You walk with your father's steady step. Be vigilant; the constables are watching every street corner.'")
		));
		ConversationDialogues.Add(FText::FromString(
			TEXT("Bhai Sant Singh: 'The leaders were deported to Dharamsala without trial. But our voice is not silenced. Truth cannot be arrested.'")
		));
		ConversationDialogues.Add(FText::FromString(
			TEXT("Bhai Sant Singh: 'The community elders have called for a peaceful protest at Jallianwala Bagh at four-thirty. We shall gather with empty hands and pray for freedom.'")
		));

		ActIIBarks.Add(FText::FromString(TEXT("The town crier's drum cannot drown the righteous prayer of Punjab!")));
		ActIIBarks.Add(FText::FromString(TEXT("They have surrounded the city gates with armored pickets!")));

		ActIIDialogues.Add(FText::FromString(
			TEXT("Bhai Sant Singh: 'Kabir, the assembly at the Bagh is peaceful—mothers, children, elders from the villages listening to Hans Raj. But General Dyer has prohibited all gatherings. If you go near the Bagh passage, stay in the alleys!'")
		));
		ActIIDialogues.Add(FText::FromString(
			TEXT("Bhai Sant Singh: 'Take these strike handbills if you must, but never run into their rifle sights. Preserve your life for the freedom that will surely come.'")
		));

		StumbleBarks.Add(FText::FromString(TEXT("Steady, young Kabir! Keep your composure.")));
		StumbleBarks.Add(FText::FromString(TEXT("Patience, child. Hasty rushing leads to stumbles.")));
		CuriosityBarks.Add(FText::FromString(TEXT("Did something fall near the street corner?")));
		CuriosityBarks.Add(FText::FromString(TEXT("I heard footsteps rushing through the lane...")));

		InteractionVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_PanditKashiRam_Dialogue.SFX_Voice_PanditKashiRam_Dialogue"));
		AmbientBarkVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_PanditKashiRam_Bark.SFX_Voice_PanditKashiRam_Bark"));
		StumbleVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_Civilian_Stumble_02.SFX_Voice_Civilian_Stumble_02"));
		CuriosityVoiceSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/Voice/SFX_Voice_Civilian_Curiosity_02.SFX_Voice_Civilian_Curiosity_02"));
		OccupationRoutineSound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Audio/SFX/SFX_Routine_Schoolmaster_Loop.SFX_Routine_Schoolmaster_Loop"));
		break;
	}

	// Attach authentic prop accessory based on occupation
	UStaticMesh* PropMesh = nullptr;
	switch (Occupation)
	{
	case ECivilianOccupation::FatherTailor:
		PropMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Game/Environment/Mohalla/Meshes/SM_Prop_SewingMachine_Singer.SM_Prop_SewingMachine_Singer"));
		if (PropAccessoryMesh)
		{
			PropAccessoryMesh->SetRelativeLocation(FVector(30.0f, 0.0f, -40.0f));
			PropAccessoryMesh->SetRelativeScale3D(FVector(0.55f, 0.55f, 0.55f));
		}
		break;

	case ECivilianOccupation::HalwaiChaiVendor:
		PropMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Game/Environment/Mohalla/Meshes/SM_Prop_ClayChaiCup_Kulhad.SM_Prop_ClayChaiCup_Kulhad"));
		if (PropAccessoryMesh)
		{
			PropAccessoryMesh->SetRelativeLocation(FVector(20.0f, 15.0f, 0.0f));
			PropAccessoryMesh->SetRelativeScale3D(FVector(1.2f, 1.2f, 1.2f));
		}
		break;

	case ECivilianOccupation::BhishtiWaterCarrier:
		PropMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Game/Environment/Mohalla/Meshes/SM_Prop_Bhishti_Mashk.SM_Prop_Bhishti_Mashk"));
		if (PropAccessoryMesh)
		{
			PropAccessoryMesh->SetRelativeLocation(FVector(-15.0f, 25.0f, 10.0f));
			PropAccessoryMesh->SetRelativeRotation(FRotator(0.0f, 90.0f, 20.0f));
			PropAccessoryMesh->SetRelativeScale3D(FVector(0.9f, 0.9f, 0.9f));
		}
		break;

	case ECivilianOccupation::ClothMerchant:
		PropMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Game/Environment/Mohalla/Meshes/SM_Prop_ClothRolls_Manchester.SM_Prop_ClothRolls_Manchester"));
		if (PropAccessoryMesh)
		{
			PropAccessoryMesh->SetRelativeLocation(FVector(25.0f, 10.0f, -20.0f));
			PropAccessoryMesh->SetRelativeScale3D(FVector(0.7f, 0.7f, 0.7f));
		}
		break;

	case ECivilianOccupation::SchoolHeadmaster:
		PropMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Game/Environment/Mohalla/Meshes/SM_School_Blackboard_Easel.SM_School_Blackboard_Easel"));
		if (PropAccessoryMesh)
		{
			PropAccessoryMesh->SetRelativeLocation(FVector(30.0f, -30.0f, -60.0f));
			PropAccessoryMesh->SetRelativeScale3D(FVector(0.35f, 0.35f, 0.35f));
		}
		break;

	case ECivilianOccupation::SchoolFriendKartar:
		PropMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Game/Environment/Mohalla/Meshes/SM_Prop_Kite_Spool_Charkhi.SM_Prop_Kite_Spool_Charkhi"));
		if (PropAccessoryMesh)
		{
			PropAccessoryMesh->SetRelativeLocation(FVector(20.0f, 15.0f, -10.0f));
			PropAccessoryMesh->SetRelativeScale3D(FVector(0.40f, 0.40f, 0.40f));
		}
		if (GetMesh())
		{
			GetMesh()->SetRelativeScale3D(FVector(0.72f, 0.72f, 0.72f));
			GetMesh()->SetRelativeLocation(FVector(0.0f, 0.0f, -64.0f));
		}
		break;

	case ECivilianOccupation::MunadiTownCrier:
		PropMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Game/Environment/Mohalla/Meshes/SM_Munadi_Proclamation_Drum.SM_Munadi_Proclamation_Drum"));
		if (PropAccessoryMesh)
		{
			PropAccessoryMesh->SetRelativeLocation(FVector(25.0f, 0.0f, -20.0f));
			PropAccessoryMesh->SetRelativeRotation(FRotator(0.0f, 0.0f, 0.0f));
			PropAccessoryMesh->SetRelativeScale3D(FVector(0.35f, 0.35f, 0.35f));
		}
		break;

	case ECivilianOccupation::ProtestElder:
		PropMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Game/Environment/Mohalla/Meshes/SM_Prop_Pamphlet_Stack_Rowlatt.SM_Prop_Pamphlet_Stack_Rowlatt"));
		if (PropAccessoryMesh)
		{
			PropAccessoryMesh->SetRelativeLocation(FVector(20.0f, 15.0f, -30.0f));
			PropAccessoryMesh->SetRelativeRotation(FRotator(0.0f, 30.0f, 0.0f));
			PropAccessoryMesh->SetRelativeScale3D(FVector(0.55f, 0.55f, 0.55f));
		}
		break;
	}

	if (PropMesh && PropAccessoryMesh)
	{
		PropAccessoryMesh->SetStaticMesh(PropMesh);
	}

	if (PropAccessoryMesh)
	{
		PropInitialRelativeLocation = PropAccessoryMesh->GetRelativeLocation();
		PropInitialRelativeRotation = PropAccessoryMesh->GetRelativeRotation();
	}

	if (GetMesh())
	{
		MeshInitialRelativeLocation = GetMesh()->GetRelativeLocation();
		MeshInitialRelativeRotation = GetMesh()->GetRelativeRotation();
	}

	ApplyHeritageAttireMaterials();

	if (OccupationRoutineSound)
	{
		if (RoutineAudioComp)
		{
			RoutineAudioComp->Stop();
			RoutineAudioComp->SetSound(OccupationRoutineSound);
			if (bEnableRoutineAnimations)
			{
				RoutineAudioComp->Play();
			}
		}
		else if (GetWorld() && GetWorld()->IsGameWorld())
		{
			RoutineAudioComp = UGameplayStatics::SpawnSoundAttached(
				OccupationRoutineSound,
				RootComponent,
				NAME_None,
				FVector::ZeroVector,
				EAttachLocation::KeepRelativeOffset,
				false,
				0.75f,
				1.0f,
				0.0f,
				VoiceAttenuation
			);
		}
	}
}

void ACivilianNPCActor::OnInteract_Implementation(ARevolutionCharacter* Interactor)
{
	if (!Interactor) return;

	FText CurrentText = AdvanceConversation();

	UE_LOG(LogREVOLUTION, Log, TEXT("Kabir conversed with %s: '%s'"), *CivilianName.ToString(), *CurrentText.ToString());

	// Display via Kabir's inspection lore modal with authentic parchment styling
	Interactor->StartInspection(CivilianName, CurrentText);

	// Play localized authentic voice dialogue
	if (InteractionVoiceSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, InteractionVoiceSound, GetActorLocation(), 1.0f, 1.0f, 0.0f, VoiceAttenuation);
	}

	// Broadcast dialogue event
	OnDialogueSpoken.Broadcast(this, CivilianName, CurrentText);

	// Advance Mission Stage if interacting with the expected NPC for current Act I objective
	if (bCanAdvanceMission)
	{
		if (UWorld* World = GetWorld())
		{
			if (URevolutionMissionSubsystem* Subsystem = World->GetSubsystem<URevolutionMissionSubsystem>())
			{
				const ECourierMissionStage Stage = Subsystem->GetCurrentStage();
				bool bShouldAdvance = false;

				if (Occupation == ECivilianOccupation::FatherTailor && Stage == ECourierMissionStage::Stage_Morning_FatherTailor)
				{
					bShouldAdvance = true;
				}
				else if (Occupation == ECivilianOccupation::BhishtiWaterCarrier && Stage == ECourierMissionStage::Stage_Morning_WellBhishti)
				{
					bShouldAdvance = true;
				}
				else if (Occupation == ECivilianOccupation::ClothMerchant && Stage == ECourierMissionStage::Stage_Morning_DeliverCloth)
				{
					bShouldAdvance = true;
				}
				else if (Occupation == ECivilianOccupation::HalwaiChaiVendor && Stage == ECourierMissionStage::Stage_Morning_ChaiHalwai)
				{
					bShouldAdvance = true;
				}
				else if (Occupation == ECivilianOccupation::MunadiTownCrier && Stage == ECourierMissionStage::Stage_Afternoon_MunadiProclamation)
				{
					bShouldAdvance = true;
				}

				if (bShouldAdvance)
				{
					Subsystem->AdvanceMissionStage();
				}

				if (Interactor->GetPamphletCount() > 0 && (Occupation == ECivilianOccupation::ClothMerchant || Occupation == ECivilianOccupation::HalwaiChaiVendor))
				{
					Interactor->DeliverPamphlets(1);
					UE_LOG(LogREVOLUTION, Log, TEXT("Kabir stealthily passed underground strike handbills to %s!"), *CivilianName.ToString());
				}
			}
		}
	}
}

FText ACivilianNPCActor::GetInteractionPrompt_Implementation() const
{
	return FText::Format(FText::FromString(TEXT("Talk to {0}")), CivilianName);
}

bool ACivilianNPCActor::CanInteract_Implementation(const ARevolutionCharacter* Interactor) const
{
	return true;
}

FText ACivilianNPCActor::AdvanceConversation()
{
	const TArray<FText>& ActiveDialogues = (bIsInActIIMode && ActIIDialogues.Num() > 0) ? ActIIDialogues : ConversationDialogues;
	if (ActiveDialogues.Num() == 0)
	{
		return HistoricalLore;
	}

	FText ChosenDialogue = ActiveDialogues[CurrentDialogueIndex % ActiveDialogues.Num()];
	CurrentDialogueIndex = (CurrentDialogueIndex + 1) % ActiveDialogues.Num();
	return ChosenDialogue;
}

FText ACivilianNPCActor::GetCurrentDialogue() const
{
	const TArray<FText>& ActiveDialogues = (bIsInActIIMode && ActIIDialogues.Num() > 0) ? ActIIDialogues : ConversationDialogues;
	if (ActiveDialogues.Num() == 0)
	{
		return HistoricalLore;
	}
	return ActiveDialogues[CurrentDialogueIndex % ActiveDialogues.Num()];
}

void ACivilianNPCActor::OnProximityBeginOverlap(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
	ARevolutionCharacter* Player = Cast<ARevolutionCharacter>(OtherActor);
	if (!Player) return;

	bPlayerInProximity = true;
	NearbyPlayer = Player;

	// Check bark cooldown
	float CurrentTime = GetWorld()->GetTimeSeconds();
	const TArray<FText>& ActiveBarks = (bIsInActIIMode && ActIIBarks.Num() > 0) ? ActIIBarks : AmbientBarks;
	if (CurrentTime - LastBarkTime >= ProximityBarkCooldown && ActiveBarks.Num() > 0)
	{
		LastBarkTime = CurrentTime;
		int32 RandomIndex = FMath::RandRange(0, ActiveBarks.Num() - 1);
		FText BarkText = ActiveBarks[RandomIndex];

		UE_LOG(LogREVOLUTION, Log, TEXT("[%s Ambient Bark]: %s"), *CivilianName.ToString(), *BarkText.ToString());
		OnDialogueSpoken.Broadcast(this, CivilianName, BarkText);

		// Play localized ambient voice bark
		if (AmbientBarkVoiceSound)
		{
			UGameplayStatics::PlaySoundAtLocation(this, AmbientBarkVoiceSound, GetActorLocation(), 0.95f, 1.0f, 0.0f, VoiceAttenuation);
		}
	}
}

void ACivilianNPCActor::OnProximityEndOverlap(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex)
{
	if (OtherActor == NearbyPlayer.Get())
	{
		bPlayerInProximity = false;
		NearbyPlayer = nullptr;
	}
}

void ACivilianNPCActor::TriggerStumble(const FVector& ImpactDirection, float ImpactForce)
{
	UWorld* World = GetWorld();
	const float CurrentTime = World ? World->GetTimeSeconds() : 0.0f;
	if (CurrentTime - LastStumbleTime < StumbleCooldown && bIsStumbled)
	{
		return;
	}

	LastStumbleTime = CurrentTime;
	bIsStumbled = true;
	StumbleTimer = StumbleDuration;
	ReactionState = ECivilianReactionState::Stumbling;
	StumbleDirection = ImpactDirection.GetSafeNormal2D();
	if (StumbleDirection.IsNearlyZero())
	{
		StumbleDirection = -GetActorForwardVector();
	}
	StumbleIntensity = FMath::Clamp(ImpactForce, 250.0f, 800.0f);

	// Contextual stumble vocalization
	if (StumbleBarks.Num() > 0)
	{
		const int32 BarkIdx = FMath::RandRange(0, StumbleBarks.Num() - 1);
		const FText BarkText = StumbleBarks[BarkIdx];
		UE_LOG(LogREVOLUTION, Log, TEXT("[%s Stumble Reaction]: %s"), *CivilianName.ToString(), *BarkText.ToString());
		OnDialogueSpoken.Broadcast(this, CivilianName, BarkText);
	}

	// Play stumble audio reaction
	if (StumbleVoiceSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, StumbleVoiceSound, GetActorLocation(), 1.0f, FMath::RandRange(0.96f, 1.04f), 0.0f, VoiceAttenuation);
	}
	else if (AmbientBarkVoiceSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, AmbientBarkVoiceSound, GetActorLocation(), 1.0f, 1.15f, 0.0f, VoiceAttenuation);
	}
}

void ACivilianNPCActor::InvestigateCuriosity(const FVector& NoiseLocation)
{
	// Stumble takes precedence over sound curiosity
	if (bIsStumbled)
	{
		return;
	}

	UWorld* World = GetWorld();
	const float CurrentTime = World ? World->GetTimeSeconds() : 0.0f;
	if (CurrentTime - LastCuriosityTime < CuriosityCooldown)
	{
		return;
	}

	LastCuriosityTime = CurrentTime;
	ReactionState = ECivilianReactionState::CuriousInvestigating;
	CuriosityLookTarget = NoiseLocation;
	CuriosityTimer = CuriosityDuration;

	// Contextual curiosity whisper / mutter
	if (CuriosityBarks.Num() > 0)
	{
		const int32 BarkIdx = FMath::RandRange(0, CuriosityBarks.Num() - 1);
		const FText BarkText = CuriosityBarks[BarkIdx];
		UE_LOG(LogREVOLUTION, Log, TEXT("[%s Curiosity Inquiry]: %s"), *CivilianName.ToString(), *BarkText.ToString());
		OnDialogueSpoken.Broadcast(this, CivilianName, BarkText);
	}

	// Play curiosity audio reaction
	if (CuriosityVoiceSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, CuriosityVoiceSound, GetActorLocation(), 0.9f, FMath::RandRange(0.96f, 1.04f), 0.0f, VoiceAttenuation);
	}
	else if (AmbientBarkVoiceSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, AmbientBarkVoiceSound, GetActorLocation(), 0.85f, 0.92f, 0.0f, VoiceAttenuation);
	}
}

void ACivilianNPCActor::NotifyHit(UPrimitiveComponent* MyComp, AActor* Other, UPrimitiveComponent* OtherComp, bool bSelfMoved, FVector HitLocation, FVector HitNormal, FVector NormalImpulse, const FHitResult& Hit)
{
	Super::NotifyHit(MyComp, Other, OtherComp, bSelfMoved, HitLocation, HitNormal, NormalImpulse, Hit);

	ARevolutionCharacter* Player = Cast<ARevolutionCharacter>(Other);
	if (Player)
	{
		const float Speed = Player->GetVelocity().Size();
		if (Player->bIsSprinting || Speed >= 400.0f)
		{
			FVector ImpactDir = Player->GetVelocity().GetSafeNormal();
			if (ImpactDir.IsNearlyZero())
			{
				ImpactDir = (GetActorLocation() - Player->GetActorLocation()).GetSafeNormal();
			}
			TriggerStumble(ImpactDir, Speed);
			Player->HandleCivilianCollision(this);
		}
	}
}

void ACivilianNPCActor::SetRoutineAnimationsEnabled(bool bEnabled)
{
	bEnableRoutineAnimations = bEnabled;
	if (!bEnabled)
	{
		if (GetMesh())
		{
			GetMesh()->SetRelativeLocation(MeshInitialRelativeLocation);
			GetMesh()->SetRelativeRotation(MeshInitialRelativeRotation);
		}
		if (PropAccessoryMesh)
		{
			PropAccessoryMesh->SetRelativeLocation(PropInitialRelativeLocation);
			PropAccessoryMesh->SetRelativeRotation(PropInitialRelativeRotation);
		}
		if (RoutineAudioComp && RoutineAudioComp->IsPlaying())
		{
			RoutineAudioComp->Stop();
		}
	}
	else
	{
		if (RoutineAudioComp && !RoutineAudioComp->IsPlaying())
		{
			RoutineAudioComp->Play();
		}
	}
}

void ACivilianNPCActor::ApplyHeritageAttireMaterials()
{
	USkeletalMeshComponent* SkelMesh = GetMesh();
	if (!SkelMesh)
	{
		return;
	}

	UMaterialInterface* MatUndyedCotton = LoadObject<UMaterialInterface>(nullptr, TEXT("/Game/Environment/Mohalla/Materials/M_ClothUndyedCotton_PBR.M_ClothUndyedCotton_PBR"));
	UMaterialInterface* MatSaffron = LoadObject<UMaterialInterface>(nullptr, TEXT("/Game/Environment/Mohalla/Materials/M_ClothSaffron_PBR.M_ClothSaffron_PBR"));
	UMaterialInterface* MatIndigo = LoadObject<UMaterialInterface>(nullptr, TEXT("/Game/Environment/Mohalla/Materials/M_ClothIndigo_PBR.M_ClothIndigo_PBR"));
	UMaterialInterface* MatAgedTeak = LoadObject<UMaterialInterface>(nullptr, TEXT("/Game/Environment/Mohalla/Materials/M_AgedTeak_PBR.M_AgedTeak_PBR"));

	UMaterialInterface* UpperAttireMat = nullptr;
	UMaterialInterface* LowerAttireMat = nullptr;
	UMaterialInterface* TurbanMat = nullptr;

	switch (Occupation)
	{
	case ECivilianOccupation::FatherTailor:
		UpperAttireMat = MatUndyedCotton;
		LowerAttireMat = MatAgedTeak;
		TurbanMat = MatUndyedCotton;
		break;

	case ECivilianOccupation::HalwaiChaiVendor:
		UpperAttireMat = MatSaffron;
		LowerAttireMat = MatUndyedCotton;
		TurbanMat = MatSaffron;
		break;

	case ECivilianOccupation::BhishtiWaterCarrier:
		UpperAttireMat = MatIndigo;
		LowerAttireMat = MatUndyedCotton;
		TurbanMat = MatIndigo;
		break;

	case ECivilianOccupation::ClothMerchant:
		UpperAttireMat = MatSaffron;
		LowerAttireMat = MatUndyedCotton;
		TurbanMat = MatSaffron;
		break;

	case ECivilianOccupation::SchoolHeadmaster:
		UpperAttireMat = MatUndyedCotton;
		LowerAttireMat = MatUndyedCotton;
		TurbanMat = MatUndyedCotton;
		break;

	case ECivilianOccupation::SchoolFriendKartar:
		UpperAttireMat = MatSaffron;
		LowerAttireMat = MatIndigo;
		TurbanMat = MatSaffron;
		break;

	case ECivilianOccupation::MunadiTownCrier:
		UpperAttireMat = MatSaffron;
		LowerAttireMat = MatUndyedCotton;
		TurbanMat = MatSaffron;
		break;

	case ECivilianOccupation::ProtestElder:
		UpperAttireMat = MatUndyedCotton;
		LowerAttireMat = MatUndyedCotton;
		TurbanMat = MatUndyedCotton;
		break;
	}

	if (UpperAttireMat)
	{
		SkelMesh->SetMaterial(0, UpperAttireMat);
	}
	if (LowerAttireMat)
	{
		SkelMesh->SetMaterial(1, LowerAttireMat);
	}
	if (TurbanMesh && TurbanMat)
	{
		TurbanMesh->SetMaterial(0, TurbanMat);
	}
}
