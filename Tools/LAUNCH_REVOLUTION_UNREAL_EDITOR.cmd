@echo off
title PROJECT REVOLUTION - Unreal Engine 5.5 Editor
color 0E
cls
echo ==============================================================================
echo                PROJECT REVOLUTION - UNREAL ENGINE 5.5 EDITOR
echo ==============================================================================
echo.
echo Launching REVOLUTION in Unreal Editor 5.5...
echo Default Map: L_Validation_Gym (1919 Mohalla, Bazaar, Well & School Compound)
echo C++ Architecture: ARevolutionCharacter with 1.1m Vaulting Trace
echo Renderer: Software Lumen Ray Tracing (Optimized for GTX 1650)
echo.
start "" "C:\Program Files\Epic Games\UE_5.5\Engine\Binaries\Win64\UnrealEditor.exe" "C:\Users\npal7\PROJECT\REVOLUTION\Project\REVOLUTION.uproject" /Game/Maps/L_Validation_Gym -RCWebControlEnable
