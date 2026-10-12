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
echo   [W, A, S, D] : Movement (Walk, Jog, Sprint)
echo   [Left Shift] : Sprint (with stamina meter)
echo   [Spacebar]   : Jump / Vault over 1.1m Rooftop Parapets
echo   [C]          : Crouch (Stealth through low arches and behind crates)
echo   [E]          : Interact (Talk to NPCs / Inspect Artifacts / Toll Bell)
echo   [Tab]        : Satchel Journal (Act I Objectives and Historical Lore)
echo   [Mouse]      : Third-Person Orbital Camera
echo.
start "" "C:\Program Files\Epic Games\UE_5.5\Engine\Binaries\Win64\UnrealEditor.exe" "C:\Users\npal7\PROJECT\REVOLUTION\Project\REVOLUTION.uproject" -game -ResX=1280 -ResY=720 -RCWebControlEnable
