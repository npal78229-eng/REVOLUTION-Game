@echo off
title PROJECT REVOLUTION - Visual Studio 2022 Setup
color 0A
cls
echo ==============================================================================
echo           PROJECT REVOLUTION - VISUAL STUDIO 2022 FOR UNREAL ENGINE
echo ==============================================================================
echo.
echo Launching Visual Studio 2022 Community Installer with pre-selected workloads:
echo   [x] Game development with C++ (Unreal Engine C++ Support)
echo   [x] Desktop development with C++
echo   [x] Windows 11 SDK (10.0.22621.0)
echo   [x] MSVC v143 x64/x86 Build Tools
echo.
echo NOTE: Windows will display a User Account Control (UAC) prompt asking:
echo       "Do you want to allow this app to make changes to your device?"
echo       Please click "YES" to proceed.
echo.
echo ==============================================================================
echo.

"C:\Users\npal7\Downloads\VisualStudioSetup.exe" --add Microsoft.VisualStudio.Workload.NativeGame --add Microsoft.VisualStudio.Workload.NativeDesktop --add Microsoft.VisualStudio.Component.Windows11SDK.22621 --add Microsoft.VisualStudio.Component.VC.UnrealEngine --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64

echo.
echo Visual Studio Setup launcher has exited.
echo If the Visual Studio Installer window is open, click "Install" or "Modify" to complete.
echo.
pause
