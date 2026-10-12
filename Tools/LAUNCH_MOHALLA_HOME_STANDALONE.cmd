@echo off
title PROJECT REVOLUTION - Play L_Mohalla_Home (Daytime)
color 0E
cls
echo ==============================================================================
echo             PROJECT REVOLUTION - PLAY L_MOHALLA_HOME (DAYTIME)
echo ==============================================================================
echo.
echo Launching L_Mohalla_Home with BP_Mohalla_Daytime_GameMode...
echo Remote Control is ENABLED (-RCWebControlEnable) so Claude stays connected!
echo.
echo Controls:
echo   [W, A, S, D] : Move Kabir
echo   [Left Shift] : Sprint
echo   [Spacebar]   : Jump / Vault
echo   [E]          : Inspect Objects (Lantern, Charpai, etc.)
echo   [Mouse]      : Camera
echo.
start "" "C:\Program Files\Epic Games\UE_5.5\Engine\Binaries\Win64\UnrealEditor.exe" "C:\Users\npal7\PROJECT\REVOLUTION\Project\REVOLUTION.uproject" /Game/Maps/L_Mohalla_Home -game -ResX=1280 -ResY=720 -RCWebControlEnable
