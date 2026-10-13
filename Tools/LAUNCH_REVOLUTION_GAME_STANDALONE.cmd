@echo off
title PROJECT REVOLUTION - Standalone Playable Game
color 0A
cls
echo ==============================================================================
echo                PROJECT REVOLUTION - STANDALONE GAME
echo ==============================================================================
echo.
echo Launching REVOLUTION in Standalone Game Mode (1280x720, Software Lumen)...
echo Default Map: /Game/Maps/L_Validation_Gym
echo Protagonist: Kabir (12-Year-Old Son of Master Tailor)
echo Level Content: 160 Actors across 5 Historical Districts
echo.
start "" "C:\Program Files\Epic Games\UE_5.5\Engine\Binaries\Win64\UnrealEditor.exe" "C:\Users\npal7\PROJECT\REVOLUTION\Project\REVOLUTION.uproject" -game -ResX=1280 -ResY=720 -log
