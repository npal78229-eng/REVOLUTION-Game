@echo off
title PROJECT REVOLUTION - Standalone Game Client
color 0A
cls
echo ==============================================================================
echo             PROJECT REVOLUTION - PLAY STANDALONE GAME (PIE)
echo ==============================================================================
echo.
echo Launching standalone game client (1280x720 windowed, Software Lumen)...
echo Controls:
echo   [W, A, S, D] : Movement (Walk 3.8 km/h, Jog 5.2 km/h)
echo   [Left Shift] : Sprint (7.2 km/h with stamina drain)
echo   [Spacebar]   : Jump / Vault over 1.1m Rooftop Parapets
echo   [Mouse]      : Third-Person Orbital Camera
echo.
start "" "C:\Program Files\Epic Games\UE_5.5\Engine\Binaries\Win64\UnrealEditor.exe" "C:\Users\npal7\PROJECT\REVOLUTION\Project\REVOLUTION.uproject" -game -ResX=1280 -ResY=720 -log
