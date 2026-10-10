@echo off
title PROJECT REVOLUTION - Epic Games Launcher (Unreal Engine)
color 0B
cls
echo ==============================================================================
echo             PROJECT REVOLUTION - UNREAL ENGINE 5.4 INSTALLATION
echo ==============================================================================
echo.
echo Opening Epic Games Launcher to the Unreal Engine Library...
echo.
start "" "com.epicgames.launcher://ue/library"
echo.
echo ------------------------------------------------------------------------------
echo STEPS TO INSTALL UNREAL ENGINE IN EPIC GAMES LAUNCHER:
echo ------------------------------------------------------------------------------
echo 1. Next to "ENGINE VERSIONS", click the yellow "+" icon.
echo 2. Select Unreal Engine 5.4.4 (or 5.5).
echo 3. IMPORTANT DISK-SAVING STEP (Protects your 149 GB SSD):
echo    - Click the small arrow on the version card -> click "Options".
echo    - UNCHECK "Android"   (Saves ~18 GB)
echo    - UNCHECK "iOS"       (Saves ~14 GB)
echo    - UNCHECK "Linux"     (Saves ~16 GB)
echo    - Keep checked: "Core Components" and "Engine Source".
echo 4. Click "Install" to begin downloading (~25 GB instead of ~65 GB).
echo ------------------------------------------------------------------------------
echo.
pause
