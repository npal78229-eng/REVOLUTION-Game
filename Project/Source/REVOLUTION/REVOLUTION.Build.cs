// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class REVOLUTION : ModuleRules
{
	public REVOLUTION(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] { 
			"Core", 
			"CoreUObject", 
			"Engine", 
			"InputCore", 
			"EnhancedInput",
			"UMG",
			"Slate",
			"SlateCore",
			"AIModule",
			"NavigationSystem"
		});

		PrivateDependencyModuleNames.AddRange(new string[] { });
	}
}
