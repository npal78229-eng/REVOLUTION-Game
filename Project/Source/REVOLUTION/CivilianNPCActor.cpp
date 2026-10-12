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

	ProximitySphere->OnComponentBeginOverlap.AddDynamic(this, &ACivilianNPCActor::OnProximityBeginOverlap);
	ProximitySphere->OnComponentEndOverlap.AddDynamic(this, &ACivilianNPCActor::OnProximityEndOverlap);

	ConfigureOccupation(Occupation);
}

void ACivilianNPCActor::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	// Smoothly orient toward Kabir when player is in close proximity
	if (bPlayerInProximity && NearbyPlayer.IsValid())
	{
		FVector PlayerLoc = NearbyPlayer->GetActorLocation();
		FVector MyLoc = GetActorLocation();
		FRotator TargetRot = UKismetMathLibrary::FindLookAtRotation(MyLoc, PlayerLoc);
		TargetRot.Pitch = 0.0f;
		TargetRot.Roll = 0.0f;

		FRotator NewRot = FMath::RInterpTo(GetActorRotation(), TargetRot, DeltaTime, 4.0f);
		SetActorRotation(NewRot);
	}
	else
	{
		// Smoothly return to default idle facing
		FRotator CurrentRot = GetActorRotation();
		if (!CurrentRot.Equals(DefaultRotation, 1.0f))
		{
			FRotator RestRot = FMath::RInterpTo(CurrentRot, DefaultRotation, DeltaTime, 2.0f);
			SetActorRotation(RestRot);
		}
	}
}

void ACivilianNPCActor::ConfigureOccupation(ECivilianOccupation NewOccupation)
{
	Occupation = NewOccupation;
	AmbientBarks.Empty();
	ConversationDialogues.Empty();
	CurrentDialogueIndex = 0;

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
	}

	if (PropMesh && PropAccessoryMesh)
	{
		PropAccessoryMesh->SetStaticMesh(PropMesh);
	}
}

void ACivilianNPCActor::OnInteract_Implementation(ARevolutionCharacter* Interactor)
{
	if (!Interactor) return;

	FText CurrentText = AdvanceConversation();

	UE_LOG(LogREVOLUTION, Log, TEXT("Kabir conversed with %s: '%s'"), *CivilianName.ToString(), *CurrentText.ToString());

	// Display via Kabir's inspection lore modal with authentic parchment styling
	Interactor->StartInspection(CivilianName, CurrentText);

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

				if (bShouldAdvance)
				{
					Subsystem->AdvanceMissionStage();
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
	if (ConversationDialogues.Num() == 0)
	{
		return HistoricalLore;
	}

	FText ChosenDialogue = ConversationDialogues[CurrentDialogueIndex];
	CurrentDialogueIndex = (CurrentDialogueIndex + 1) % ConversationDialogues.Num();
	return ChosenDialogue;
}

FText ACivilianNPCActor::GetCurrentDialogue() const
{
	if (ConversationDialogues.Num() == 0)
	{
		return HistoricalLore;
	}
	return ConversationDialogues[CurrentDialogueIndex];
}

void ACivilianNPCActor::OnProximityBeginOverlap(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
	ARevolutionCharacter* Player = Cast<ARevolutionCharacter>(OtherActor);
	if (!Player) return;

	bPlayerInProximity = true;
	NearbyPlayer = Player;

	// Check bark cooldown
	float CurrentTime = GetWorld()->GetTimeSeconds();
	if (CurrentTime - LastBarkTime >= ProximityBarkCooldown && AmbientBarks.Num() > 0)
	{
		LastBarkTime = CurrentTime;
		int32 RandomIndex = FMath::RandRange(0, AmbientBarks.Num() - 1);
		FText BarkText = AmbientBarks[RandomIndex];

		UE_LOG(LogREVOLUTION, Log, TEXT("[%s Ambient Bark]: %s"), *CivilianName.ToString(), *BarkText.ToString());
		OnDialogueSpoken.Broadcast(this, CivilianName, BarkText);
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
